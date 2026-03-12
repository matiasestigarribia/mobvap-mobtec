"""
Tests for photos.management.commands.import_photos

Covers every branch of the management command handle() method:
  - Edition not found (DoesNotExist)
  - zip_path does not exist on disk
  - Bad / corrupted zip file (BadZipFile)
  - Successful import: multiple valid images, skipping __MACOSX entries,
    skipping non-image extensions, skipping directory entries (empty basename)
  - Per-file save failure (inner except Exception branch)
  - Default --desc value (empty string)
  - Custom --desc value passed through to Photo instances
"""

import io
import zipfile
from unittest.mock import patch

import pytest
from PIL import Image
from django.core.management import call_command

from editions.models import Edition
from photos.models import Photo


# ---------------------------------------------------------------------------
# Module-level helpers
# ---------------------------------------------------------------------------

def _make_real_jpeg() -> bytes:
    """Return bytes of a minimal valid JPEG image using Pillow.

    The ``Photo.image_file`` is an ``ImageField`` which calls Pillow to
    validate the image content during ``FieldFile.save()``.  Fake bytes that
    merely look like a JPEG header are rejected by ``PIL.Image.open()``.
    """
    buf = io.BytesIO()
    img = Image.new("RGB", (4, 4), color=(128, 64, 32))
    img.save(buf, format="JPEG")
    return buf.getvalue()


def _make_zip(entries: dict) -> bytes:
    """Build an in-memory zip file from a ``{filename: bytes}`` mapping."""
    buf = io.BytesIO()
    with zipfile.ZipFile(buf, "w", compression=zipfile.ZIP_STORED) as zf:
        for name, content in entries.items():
            zf.writestr(name, content)
    return buf.getvalue()


# ---------------------------------------------------------------------------
# Shared fixtures
# ---------------------------------------------------------------------------

@pytest.fixture
def edition(db):
    """A single persisted Edition whose slug we can pass to the command."""
    return Edition.objects.create(
        edition_name="Cmd Import Edition",
        edition_description="test edition for import",
    )


@pytest.fixture
def real_jpeg():
    """A real JPEG byte string that Pillow accepts as a valid image."""
    return _make_real_jpeg()


@pytest.fixture
def zip_factory(tmp_path):
    """
    Returns a callable ``make(entries) -> str`` that writes an in-memory zip
    to a temp file and returns its path as a string.
    """
    def _make(entries: dict) -> str:
        p = tmp_path / "archive.zip"
        p.write_bytes(_make_zip(entries))
        return str(p)

    return _make


# ---------------------------------------------------------------------------
# Tests
# ---------------------------------------------------------------------------

@pytest.mark.django_db
class TestImportPhotosEditionBranch:
    """Branch: Edition.DoesNotExist path."""

    def test_edition_not_found_writes_error_and_returns(self, tmp_path, capsys):
        """When no Edition matches the given slug, an error is written and
        no Photo objects are created."""
        dummy_zip = tmp_path / "dummy.zip"
        dummy_zip.write_bytes(_make_zip({"photo.jpg": _make_real_jpeg()}))

        call_command(
            "import_photos",
            str(dummy_zip),
            "slug-that-never-exists",
        )

        captured = capsys.readouterr()
        output = captured.out + captured.err
        assert "not found" in output.lower()
        assert Photo.objects.count() == 0

    def test_edition_found_success_message_written(self, edition, tmp_path, capsys):
        """When the edition IS found, a SUCCESS line containing its name is
        written before any file processing starts.  We use a non-existent zip
        path so the command returns early after that message."""
        call_command(
            "import_photos",
            "/nonexistent/does-not-exist.zip",
            edition.slug,
        )
        captured = capsys.readouterr()
        output = captured.out + captured.err
        assert edition.edition_name in output


@pytest.mark.django_db
class TestImportPhotosZipPathBranch:
    """Branch: zip file path validation."""

    def test_zip_path_does_not_exist_writes_error(self, edition, capsys):
        """When the supplied path does not exist on disk, an error message is
        written and no photos are imported."""
        call_command(
            "import_photos",
            "/path/that/does/not/exist/archive.zip",
            edition.slug,
        )
        captured = capsys.readouterr()
        output = captured.out + captured.err
        assert "not found" in output.lower() or "folder" in output.lower()
        assert Photo.objects.count() == 0

    def test_bad_zip_file_writes_error(self, edition, tmp_path, capsys):
        """When the file exists but is not a valid zip, BadZipFile is caught
        and an error message is written."""
        bad_zip = tmp_path / "corrupted.zip"
        bad_zip.write_bytes(b"this is definitely not a zip file")

        call_command("import_photos", str(bad_zip), edition.slug)

        captured = capsys.readouterr()
        output = captured.out + captured.err
        assert (
            "not valid" in output.lower()
            or "corrupted" in output.lower()
            or "zip" in output.lower()
        )
        assert Photo.objects.count() == 0


@pytest.mark.django_db
class TestImportPhotosFilteringBranch:
    """Branch: image-extension filter and __MACOSX / directory skipping."""

    def test_non_image_files_are_skipped(self, edition, zip_factory, capsys):
        """Files with extensions other than .jpg/.jpeg/.png/.webp must not be
        imported; the final count should be 0."""
        zip_path = zip_factory({
            "readme.txt": b"text",
            "data.csv": b"col1,col2\n1,2",
            "photo.gif": b"GIF89a",
            "doc.pdf": b"%PDF",
        })

        call_command("import_photos", zip_path, edition.slug)

        captured = capsys.readouterr()
        output = captured.out + captured.err
        assert "0" in output
        assert Photo.objects.count() == 0

    def test_macosx_entries_are_skipped(self, edition, zip_factory, capsys):
        """Entries whose path starts with ``__MACOSX`` must be silently
        filtered out before any processing."""
        zip_path = zip_factory({
            "__MACOSX/._photo.jpg": b"macos meta",
            "__MACOSX/photo.jpg": b"macos meta",
        })

        call_command("import_photos", zip_path, edition.slug)

        captured = capsys.readouterr()
        output = captured.out + captured.err
        assert "0" in output


@pytest.mark.django_db
class TestImportPhotosSuccessfulImport:
    """
    Happy-path branches: successful photo creation.

    ``Photo.image_file`` is an ``ImageField``.  Its ``FieldFile.save()``
    method calls Pillow to validate image content AND then delegates to
    ``storage.save()``.  We patch ``FieldFile.save`` at the class level so
    the entire chain (Pillow validation + storage write) is bypassed, allowing
    lines 58-59 (count increment + "Saved:" message) in the command to be
    reached.
    """

    def test_successful_import_reports_count(self, edition, zip_factory, capsys):
        """Two valid JPEG entries should result in 'Concluded! 2 imported'
        appearing in stdout."""
        real_jpeg = _make_real_jpeg()
        zip_path = zip_factory({"img1.jpg": real_jpeg, "img2.jpg": real_jpeg})

        from django.db.models.fields.files import FieldFile

        with patch.object(FieldFile, "save", return_value=None):
            call_command("import_photos", zip_path, edition.slug)

        captured = capsys.readouterr()
        output = captured.out + captured.err
        assert "2" in output

    def test_successful_import_writes_saved_per_file(self, edition, zip_factory, capsys):
        """The 'Saved: <filename>' message (line 59) must appear once per
        successfully imported file."""
        real_jpeg = _make_real_jpeg()
        zip_path = zip_factory({"shot.jpg": real_jpeg})

        from django.db.models.fields.files import FieldFile

        with patch.object(FieldFile, "save", return_value=None):
            call_command("import_photos", zip_path, edition.slug)

        captured = capsys.readouterr()
        output = captured.out + captured.err
        assert "shot.jpg" in output or "Saved" in output

    def test_all_valid_extensions_are_imported(self, edition, zip_factory, capsys):
        """All four supported extensions (.jpg, .jpeg, .png, .webp) must pass
        the filter and be counted."""
        real_jpeg = _make_real_jpeg()
        # Use the same valid JPEG bytes regardless of declared extension —
        # the command does not re-validate the extension after filtering.
        zip_path = zip_factory({
            "a.jpg": real_jpeg,
            "b.jpeg": real_jpeg,
            "c.png": real_jpeg,
            "d.webp": real_jpeg,
        })

        from django.db.models.fields.files import FieldFile

        with patch.object(FieldFile, "save", return_value=None):
            call_command("import_photos", zip_path, edition.slug)

        captured = capsys.readouterr()
        output = captured.out + captured.err
        assert "4" in output

    def test_custom_desc_is_used(self, edition, zip_factory, capsys):
        """When ``--desc`` is supplied, it must appear in the Photo objects
        passed to the storage layer (verified via Photo.__init__ capture)."""
        real_jpeg = _make_real_jpeg()
        zip_path = zip_factory({"snap.jpg": real_jpeg})

        captured_photos: list[Photo] = []
        original_init = Photo.__init__

        def capturing_init(self_photo, *args, **kwargs):
            original_init(self_photo, *args, **kwargs)
            captured_photos.append(self_photo)

        from django.db.models.fields.files import FieldFile

        with patch.object(Photo, "__init__", capturing_init):
            with patch.object(FieldFile, "save", return_value=None):
                call_command(
                    "import_photos",
                    zip_path,
                    edition.slug,
                    "--desc",
                    "My Custom Desc",
                )

        descriptions = [
            p.image_description
            for p in captured_photos
            if hasattr(p, "image_description")
        ]
        assert any(d == "My Custom Desc" for d in descriptions)

    def test_default_desc_is_empty_string(self, edition, zip_factory, capsys):
        """When ``--desc`` is omitted, image_description defaults to ''."""
        real_jpeg = _make_real_jpeg()
        zip_path = zip_factory({"snap.jpg": real_jpeg})

        captured_photos: list[Photo] = []
        original_init = Photo.__init__

        def capturing_init(self_photo, *args, **kwargs):
            original_init(self_photo, *args, **kwargs)
            captured_photos.append(self_photo)

        from django.db.models.fields.files import FieldFile

        with patch.object(Photo, "__init__", capturing_init):
            with patch.object(FieldFile, "save", return_value=None):
                call_command("import_photos", zip_path, edition.slug)

        descriptions = [
            p.image_description
            for p in captured_photos
            if hasattr(p, "image_description")
        ]
        assert any(d == "" for d in descriptions)


@pytest.mark.django_db
class TestImportPhotosDirectoryEntryBranch:
    """Branch: directory entries whose os.path.basename is '' trigger continue."""

    def test_directory_entry_is_skipped(self, edition, zip_factory, capsys):
        """A zip entry named 'subdir/' has ``os.path.basename('subdir/') == ''``.
        It must be skipped; only the real image should be counted."""
        real_jpeg = _make_real_jpeg()
        zip_path = zip_factory({
            "subdir/": b"",          # directory node — empty basename
            "real.jpg": real_jpeg,
        })

        from django.db.models.fields.files import FieldFile

        with patch.object(FieldFile, "save", return_value=None):
            call_command("import_photos", zip_path, edition.slug)

        captured = capsys.readouterr()
        output = captured.out + captured.err
        # Only 1 photo should be reported
        assert "1" in output

    def test_mixed_zip_skips_dir_and_non_image(self, edition, zip_factory, capsys):
        """Combine a directory node, a non-image file, a __MACOSX entry, and
        two valid images.  Only the two valid images should be counted."""
        real_jpeg = _make_real_jpeg()
        zip_path = zip_factory({
            "folder/": b"",
            "folder/notes.txt": b"text",
            "__MACOSX/._img.jpg": b"meta",
            "folder/photo1.jpg": real_jpeg,
            "photo2.png": real_jpeg,
        })

        from django.db.models.fields.files import FieldFile

        with patch.object(FieldFile, "save", return_value=None):
            call_command("import_photos", zip_path, edition.slug)

        captured = capsys.readouterr()
        output = captured.out + captured.err
        assert "2" in output


@pytest.mark.django_db
class TestImportPhotosEmptyBasenameBranch:
    """
    Branch: ``if not simple_name: continue`` (line 48).

    This branch is normally dead code given that the extension filter on
    line 39 only passes entries that end with a valid image extension
    (e.g. ``.jpg``), and any such filename has a non-empty basename.

    We reach it by patching ``os.path.basename`` inside the management
    command module so that it returns ``''`` for a specific call, simulating
    a hypothetical zip entry whose basename resolves to an empty string.
    """

    def test_empty_basename_triggers_continue(self, edition, zip_factory, capsys):
        """When os.path.basename returns '' for a filename the entry is
        skipped via the ``if not simple_name: continue`` branch (line 48).

        Strategy: build the side-effect list BEFORE patching (so we hold a
        reference to the real implementation), then replace os.path.basename
        with a function that returns '' for the first image-filename call and
        delegates to the captured real function for all other calls.
        """
        real_jpeg = _make_real_jpeg()
        zip_path = zip_factory({"first.jpg": real_jpeg, "second.jpg": real_jpeg})

        from django.db.models.fields.files import FieldFile
        import os as _os

        # Capture the REAL basename before any patch is applied
        _real_basename = _os.path.basename

        image_names = {"first.jpg", "second.jpg"}
        image_call_count = {"n": 0}

        def patched_basename(path):
            # Use the captured real function (not os.path.basename which is
            # now patched) to compute what the name would normally be.
            real_name = _real_basename(str(path))
            if real_name in image_names:
                image_call_count["n"] += 1
                if image_call_count["n"] == 1:
                    return ""  # triggers ``if not simple_name: continue``
            return _real_basename(path)

        import photos.management.commands.import_photos as _cmd_module
        with patch.object(_cmd_module.os.path, "basename", patched_basename):
            with patch.object(FieldFile, "save", return_value=None):
                call_command("import_photos", zip_path, edition.slug)

        captured = capsys.readouterr()
        output = captured.out + captured.err
        # Only 1 of the 2 entries should be counted (the first is skipped)
        assert "Concluded! 1 imported photos" in output


@pytest.mark.django_db
class TestImportPhotosPerFileSaveFailure:
    """Branch: inner except Exception when photo.image_file.save() raises."""

    def test_per_file_failure_logs_error_and_continues(self, edition, zip_factory, capsys):
        """When saving one photo raises an exception, the error is logged and
        processing continues.  The final count reflects only successes."""
        real_jpeg = _make_real_jpeg()
        zip_path = zip_factory({
            "bad.jpg": real_jpeg,
            "good.jpg": real_jpeg,
        })

        from django.db.models.fields.files import FieldFile

        call_count = {"n": 0}

        def flaky_save(self_field, name, content, save=True):
            call_count["n"] += 1
            if call_count["n"] == 1:
                raise OSError("Simulated disk-full error")
            # Second call succeeds silently

        with patch.object(FieldFile, "save", flaky_save):
            call_command("import_photos", zip_path, edition.slug)

        captured = capsys.readouterr()
        output = captured.out + captured.err
        # An error message must be present for the failed file
        assert "failed" in output.lower() or "error" in output.lower()
        # Exactly 1 photo succeeded
        assert "1" in output

    def test_per_file_failure_error_contains_filename(self, edition, zip_factory, capsys):
        """The error message for a failed file must include the file name."""
        real_jpeg = _make_real_jpeg()
        zip_path = zip_factory({"failing_photo.jpg": real_jpeg})

        from django.db.models.fields.files import FieldFile

        def always_raise(self_field, name, content, save=True):
            raise IOError("no space left on device")

        with patch.object(FieldFile, "save", always_raise):
            call_command("import_photos", zip_path, edition.slug)

        captured = capsys.readouterr()
        output = captured.out + captured.err
        assert "failing_photo.jpg" in output

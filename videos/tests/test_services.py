"""
Tests for videos.services

Covers every branch of ``process_video`` and ``generate_thumbnail``:

process_video:
  - Normal path: temp file written, generate_thumbnail called, thumbnail
    file wrapped in Django File, original file seeked, both temp files removed.
  - Thumbnail generation fails (returns None): thumbnail_file is None,
    original file still returned, temp video file is cleaned up.
  - Thumbnail path returned but file does not exist on disk: thumbnail_file
    is None, no os.remove attempt on thumbnail.

generate_thumbnail:
  - Normal path: ffmpeg succeeds, output path returned.
  - ffmpeg raises ffmpeg.Error: exception caught, None returned.

All ffmpeg calls, tempfile operations, and os.path.exists / os.remove calls
are mocked so tests run without ffmpeg installed and without touching disk.
"""

import os
from io import BytesIO
from unittest.mock import MagicMock, call, patch

import pytest
from django.core.files import File
from django.core.files.uploadedfile import SimpleUploadedFile


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _make_uploaded_file(name: str = "test.mp4", content: bytes = b"fake-video") -> SimpleUploadedFile:
    """Return a SimpleUploadedFile that mimics an uploaded video."""
    f = SimpleUploadedFile(name, content, content_type="video/mp4")
    return f


# ---------------------------------------------------------------------------
# Tests for generate_thumbnail
# ---------------------------------------------------------------------------

class TestGenerateThumbnail:
    """Unit tests for ``videos.services.generate_thumbnail``."""

    def test_success_returns_output_path(self):
        """When ffmpeg.run() succeeds, the expected output path is returned."""
        from videos.services import generate_thumbnail

        input_path = "/tmp/video.mp4"
        expected_output = "/tmp/video.jpeg"

        # Build a mock chain: ffmpeg.input(...).output(...).run(...)
        mock_run = MagicMock(return_value=(b"", b""))
        mock_output = MagicMock()
        mock_output.run = mock_run
        mock_input = MagicMock()
        mock_input.output = MagicMock(return_value=mock_output)

        with patch("videos.services.ffmpeg.input", return_value=mock_input) as mock_ffmpeg_input:
            result = generate_thumbnail(input_path)

        mock_ffmpeg_input.assert_called_once_with(input_path, ss="00:00:05")
        mock_input.output.assert_called_once_with(expected_output, vframes=1)
        mock_output.run.assert_called_once_with(capture_stdout=True, capture_stderr=True)
        assert result == expected_output

    def test_ffmpeg_error_returns_none(self):
        """When ffmpeg raises ``ffmpeg.Error``, the exception is caught and
        ``None`` is returned (no re-raise)."""
        import ffmpeg as _ffmpeg
        from videos.services import generate_thumbnail

        # Build a mock ffmpeg chain whose run() raises ffmpeg.Error
        mock_error = _ffmpeg.Error("ffmpeg", b"", b"ffmpeg not found")
        mock_run = MagicMock(side_effect=mock_error)
        mock_output = MagicMock()
        mock_output.run = mock_run
        mock_input = MagicMock()
        mock_input.output = MagicMock(return_value=mock_output)

        with patch("videos.services.ffmpeg.input", return_value=mock_input):
            result = generate_thumbnail("/tmp/video.mp4")

        assert result is None

    def test_output_path_is_jpeg_extension(self):
        """The output filename is always the input stem with .jpeg extension."""
        from videos.services import generate_thumbnail

        mock_run = MagicMock(return_value=(b"", b""))
        mock_output = MagicMock()
        mock_output.run = mock_run
        mock_input = MagicMock()
        mock_input.output = MagicMock(return_value=mock_output)

        with patch("videos.services.ffmpeg.input", return_value=mock_input):
            result = generate_thumbnail("/path/to/my_video.avi")

        assert result == "/path/to/my_video.jpeg"


# ---------------------------------------------------------------------------
# Tests for process_video
# ---------------------------------------------------------------------------

class TestProcessVideo:
    """Unit tests for ``videos.services.process_video``.

    All disk I/O (tempfile, os.path.exists, os.remove) and ffmpeg calls are
    mocked so tests run purely in memory.
    """

    # ------------------------------------------------------------------
    # Happy path: thumbnail is generated and exists on disk
    # ------------------------------------------------------------------

    def test_happy_path_returns_tuple_with_thumbnail(self):
        """When generate_thumbnail succeeds and the thumbnail file exists,
        process_video returns (original_file, File-wrapped-thumbnail)."""
        from videos.services import process_video

        uploaded = _make_uploaded_file()
        thumbnail_path = "/tmp/tmpABCD.jpeg"
        temp_video_path = "/tmp/tmpABCD.mp4"

        mock_temp_file = MagicMock()
        mock_temp_file.name = temp_video_path
        mock_temp_file.__enter__ = MagicMock(return_value=mock_temp_file)
        mock_temp_file.__exit__ = MagicMock(return_value=False)
        mock_temp_file.write = MagicMock()

        mock_thumbnail_handle = MagicMock(spec=BytesIO)

        with patch("videos.services.tempfile.NamedTemporaryFile", return_value=mock_temp_file):
            with patch("videos.services.generate_thumbnail", return_value=thumbnail_path):
                with patch("videos.services.os.path.exists", return_value=True):
                    with patch("videos.services.os.remove") as mock_remove:
                        with patch("builtins.open", return_value=mock_thumbnail_handle):
                            result_video, result_thumbnail = process_video(uploaded)

        # The original uploaded file is returned after seek(0)
        assert result_video is uploaded
        # A File wrapper around the thumbnail handle is returned
        assert result_thumbnail is not None
        assert isinstance(result_thumbnail, File)
        # Both temp files were removed
        remove_calls = [c.args[0] for c in mock_remove.call_args_list]
        assert temp_video_path in remove_calls
        assert thumbnail_path in remove_calls

    # ------------------------------------------------------------------
    # generate_thumbnail returns None: no thumbnail file created
    # ------------------------------------------------------------------

    def test_thumbnail_generation_fails_returns_none_thumbnail(self):
        """When generate_thumbnail returns None, thumbnail_file is None in
        the returned tuple but the original video file is still returned."""
        from videos.services import process_video

        uploaded = _make_uploaded_file()
        temp_video_path = "/tmp/tmpABCD.mp4"

        mock_temp_file = MagicMock()
        mock_temp_file.name = temp_video_path
        mock_temp_file.__enter__ = MagicMock(return_value=mock_temp_file)
        mock_temp_file.__exit__ = MagicMock(return_value=False)

        with patch("videos.services.tempfile.NamedTemporaryFile", return_value=mock_temp_file):
            with patch("videos.services.generate_thumbnail", return_value=None):
                with patch("videos.services.os.path.exists", return_value=False):
                    with patch("videos.services.os.remove") as mock_remove:
                        result_video, result_thumbnail = process_video(uploaded)

        assert result_video is uploaded
        assert result_thumbnail is None
        # Only the temp video file should be removed (thumbnail path is None)
        mock_remove.assert_called_once_with(temp_video_path)

    # ------------------------------------------------------------------
    # generate_thumbnail returns a path but the file does not exist
    # ------------------------------------------------------------------

    def test_thumbnail_path_returned_but_file_missing(self):
        """When generate_thumbnail returns a path but ``os.path.exists``
        returns False for it, thumbnail_file remains None and os.remove is
        NOT called for the non-existent thumbnail."""
        from videos.services import process_video

        uploaded = _make_uploaded_file()
        thumbnail_path = "/tmp/tmpABCD.jpeg"
        temp_video_path = "/tmp/tmpABCD.mp4"

        mock_temp_file = MagicMock()
        mock_temp_file.name = temp_video_path
        mock_temp_file.__enter__ = MagicMock(return_value=mock_temp_file)
        mock_temp_file.__exit__ = MagicMock(return_value=False)

        def fake_exists(path):
            # thumbnail file does not exist on disk
            return False

        with patch("videos.services.tempfile.NamedTemporaryFile", return_value=mock_temp_file):
            with patch("videos.services.generate_thumbnail", return_value=thumbnail_path):
                with patch("videos.services.os.path.exists", side_effect=fake_exists):
                    with patch("videos.services.os.remove") as mock_remove:
                        result_video, result_thumbnail = process_video(uploaded)

        assert result_video is uploaded
        assert result_thumbnail is None
        # Only the temp video is removed; thumbnail is not (it doesn't exist)
        mock_remove.assert_called_once_with(temp_video_path)

    # ------------------------------------------------------------------
    # Verify temp file chunks are written
    # ------------------------------------------------------------------

    def test_uploaded_file_chunks_written_to_temp(self):
        """process_video writes all chunks of the uploaded file to the
        temp file before calling generate_thumbnail."""
        from videos.services import process_video

        chunk_data = [b"chunk1", b"chunk2", b"chunk3"]
        uploaded = MagicMock()
        uploaded.name = "video.mp4"
        uploaded.chunks = MagicMock(return_value=iter(chunk_data))
        uploaded.seek = MagicMock()

        temp_video_path = "/tmp/tmpXYZW.mp4"

        mock_temp_file = MagicMock()
        mock_temp_file.name = temp_video_path
        mock_temp_file.__enter__ = MagicMock(return_value=mock_temp_file)
        mock_temp_file.__exit__ = MagicMock(return_value=False)

        with patch("videos.services.tempfile.NamedTemporaryFile", return_value=mock_temp_file):
            with patch("videos.services.generate_thumbnail", return_value=None):
                with patch("videos.services.os.path.exists", return_value=False):
                    with patch("videos.services.os.remove"):
                        process_video(uploaded)

        # Each chunk must be written to the temp file
        expected_calls = [call(chunk) for chunk in chunk_data]
        mock_temp_file.write.assert_has_calls(expected_calls)

    # ------------------------------------------------------------------
    # Verify original file is seeked back to 0 before returning
    # ------------------------------------------------------------------

    def test_uploaded_file_seeked_to_zero_after_processing(self):
        """process_video calls ``uploaded_file.seek(0)`` before returning,
        so the caller can re-read the file from the beginning."""
        from videos.services import process_video

        uploaded = MagicMock()
        uploaded.name = "clip.mp4"
        uploaded.chunks = MagicMock(return_value=iter([b"data"]))
        uploaded.seek = MagicMock()

        temp_video_path = "/tmp/tmpSEEK.mp4"
        mock_temp_file = MagicMock()
        mock_temp_file.name = temp_video_path
        mock_temp_file.__enter__ = MagicMock(return_value=mock_temp_file)
        mock_temp_file.__exit__ = MagicMock(return_value=False)

        with patch("videos.services.tempfile.NamedTemporaryFile", return_value=mock_temp_file):
            with patch("videos.services.generate_thumbnail", return_value=None):
                with patch("videos.services.os.path.exists", return_value=False):
                    with patch("videos.services.os.remove"):
                        process_video(uploaded)

        uploaded.seek.assert_called_once_with(0)

    # ------------------------------------------------------------------
    # Verify thumbnail File object name is derived from uploaded file name
    # ------------------------------------------------------------------

    def test_thumbnail_file_name_derived_from_video_name(self):
        """The thumbnail File wrapper's name attribute should be the stem of
        the uploaded filename with .jpeg extension."""
        from videos.services import process_video

        uploaded = _make_uploaded_file(name="my_summer_video.mp4")
        thumbnail_path = "/tmp/tmpABCD.jpeg"
        temp_video_path = "/tmp/tmpABCD.mp4"

        mock_temp_file = MagicMock()
        mock_temp_file.name = temp_video_path
        mock_temp_file.__enter__ = MagicMock(return_value=mock_temp_file)
        mock_temp_file.__exit__ = MagicMock(return_value=False)

        mock_file_handle = MagicMock()

        with patch("videos.services.tempfile.NamedTemporaryFile", return_value=mock_temp_file):
            with patch("videos.services.generate_thumbnail", return_value=thumbnail_path):
                with patch("videos.services.os.path.exists", return_value=True):
                    with patch("videos.services.os.remove"):
                        with patch("builtins.open", return_value=mock_file_handle):
                            _, result_thumbnail = process_video(uploaded)

        assert result_thumbnail is not None
        assert result_thumbnail.name == "my_summer_video.jpeg"

    # ------------------------------------------------------------------
    # Verify NamedTemporaryFile is called with correct suffix
    # ------------------------------------------------------------------

    def test_temp_file_created_with_correct_suffix(self):
        """NamedTemporaryFile is called with ``delete=False`` and a suffix
        matching the uploaded file's extension."""
        from videos.services import process_video

        uploaded = _make_uploaded_file(name="recording.avi")

        mock_temp_file = MagicMock()
        mock_temp_file.name = "/tmp/tmpABC.avi"
        mock_temp_file.__enter__ = MagicMock(return_value=mock_temp_file)
        mock_temp_file.__exit__ = MagicMock(return_value=False)

        with patch("videos.services.tempfile.NamedTemporaryFile", return_value=mock_temp_file) as mock_ntf:
            with patch("videos.services.generate_thumbnail", return_value=None):
                with patch("videos.services.os.path.exists", return_value=False):
                    with patch("videos.services.os.remove"):
                        process_video(uploaded)

        mock_ntf.assert_called_once_with(delete=False, suffix=".avi")

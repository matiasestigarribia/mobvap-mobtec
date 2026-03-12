"""
Shared pytest fixtures and factory-boy factories for the mobvap_mobtec test suite.

Coverage targets: 90%+ line coverage, 85%+ branch coverage.
External services (GCS, Azure AI, ffmpeg) must always be mocked — never hit real infrastructure in unit tests.
"""

import io
from unittest.mock import patch

import factory
import pytest
from django.core.files.base import ContentFile
from django.db.models.signals import post_save
from django.test import Client
from rest_framework.test import APIClient

from comments.models import Comment
from editions.models import Edition
from homepagecontents.models import HomePageContent
from photos.models import Photo
from rulespagecontents.models import RulesPageContent
from videos.models import Video


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _make_jpeg_bytes() -> bytes:
    """Return a minimal valid JPEG byte string using Pillow."""
    from PIL import Image

    buf = io.BytesIO()
    img = Image.new("RGB", (1, 1), color=(255, 0, 0))
    img.save(buf, format="JPEG")
    return buf.getvalue()


# ---------------------------------------------------------------------------
# Factories
# ---------------------------------------------------------------------------

class EditionFactory(factory.django.DjangoModelFactory):
    """Factory for :class:`editions.models.Edition`.

    ``slug`` is intentionally omitted — the model's ``save()`` generates it
    automatically from ``edition_name``.
    """

    class Meta:
        model = Edition

    edition_name = factory.Sequence(lambda n: f"Edicao {n}")
    edition_description = factory.Faker("paragraph")
    preview_image1 = factory.django.ImageField(format="JPEG")
    preview_image2 = factory.django.ImageField(format="JPEG")


class PhotoFactory(factory.django.DjangoModelFactory):
    """Factory for :class:`photos.models.Photo`.

    ``edition`` is provided via SubFactory so the FK is always satisfied.
    """

    class Meta:
        model = Photo

    edition = factory.SubFactory(EditionFactory)
    image_file = factory.django.ImageField(format="JPEG")
    image_title = factory.Faker("sentence", nb_words=4)
    image_description = factory.Faker("paragraph")


@factory.django.mute_signals(post_save)
class VideoFactory(factory.django.DjangoModelFactory):
    """Factory for :class:`videos.models.Video`.

    ``process_video`` is called inside ``Video.save()`` (not in a signal), so
    we patch it via ``_create`` to prevent ffmpeg from being invoked during
    tests.  The ``@mute_signals(post_save)`` decorator is kept for completeness
    in case any future signal is wired up.
    """

    class Meta:
        model = Video

    edition = factory.SubFactory(EditionFactory)
    video_file = factory.django.FileField(filename="test.mp4", data=b"fake-mp4-data")
    video_thumbnail = factory.django.ImageField(format="JPEG")
    video_title = factory.Faker("sentence", nb_words=5)
    video_description = factory.Faker("paragraph")

    @classmethod
    def _create(cls, model_class, *args, **kwargs):
        """Override _create to patch process_video before the model is saved."""
        # Build a fake return value that mirrors what process_video returns:
        # (uploaded_file, thumbnail_file)
        fake_thumbnail = ContentFile(b"fake-thumbnail-data", name="test.jpeg")

        with patch("videos.models.process_video") as mock_process:
            mock_process.return_value = (kwargs.get("video_file"), fake_thumbnail)
            instance = super()._create(model_class, *args, **kwargs)
        return instance


class CommentFactory(factory.django.DjangoModelFactory):
    """Factory for :class:`comments.models.Comment`."""

    class Meta:
        model = Comment

    comment_author = factory.Faker("name")
    comment_text = factory.Faker("paragraph")
    comment_status = "approved"
    azure_safety_response = {}


class HomePageContentFactory(factory.django.DjangoModelFactory):
    """Factory for :class:`homepagecontents.models.HomePageContent`.

    All non-optional fields are provided with sensible defaults.
    """

    class Meta:
        model = HomePageContent

    home_title = factory.Faker("sentence", nb_words=4)
    youtube_url = "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
    block_content1_title = factory.Faker("sentence", nb_words=3)
    block_content1_text = factory.Faker("paragraph")
    youtube_url2 = None
    block_content2_title = factory.Faker("sentence", nb_words=3)
    block_content2_text = factory.Faker("paragraph")
    schedule_table_title = factory.Faker("sentence", nb_words=3)
    schedule_table_html = "<table><tr><td>Test</td></tr></table>"
    block_content3_title = factory.Faker("sentence", nb_words=3)
    block_content3_text = factory.Faker("paragraph")
    block_content4_title = "."
    block_content4_text = "."


class RulesPageContentFactory(factory.django.DjangoModelFactory):
    """Factory for :class:`rulespagecontents.models.RulesPageContent`.

    PDF fields are left empty — they are nullable/blankable in the model.
    """

    class Meta:
        model = RulesPageContent

    rules_title = factory.Faker("sentence", nb_words=4)
    rules_text = factory.Faker("paragraph")
    pdf_file_mobvap = None
    pdf_file_mobtec = None


# ---------------------------------------------------------------------------
# pytest fixtures
# ---------------------------------------------------------------------------

@pytest.fixture
def edition(db):
    """A single persisted Edition instance."""
    return EditionFactory()


@pytest.fixture
def photo(db, edition):
    """A single persisted Photo instance linked to the shared edition fixture."""
    return PhotoFactory(edition=edition)


@pytest.fixture
def video(db, edition):
    """A single persisted Video instance linked to the shared edition fixture.

    ffmpeg / process_video is suppressed inside VideoFactory._create.
    """
    return VideoFactory(edition=edition)


@pytest.fixture
def comment(db):
    """A single persisted Comment instance with status='approved'."""
    return CommentFactory()


@pytest.fixture
def homepage_content(db):
    """A single persisted HomePageContent instance."""
    return HomePageContentFactory()


@pytest.fixture
def rules_content(db):
    """A single persisted RulesPageContent instance."""
    return RulesPageContentFactory()


@pytest.fixture
def client():
    """Standard Django test client (unauthenticated)."""
    return Client()


@pytest.fixture
def api_client():
    """DRF APIClient (unauthenticated)."""
    return APIClient()

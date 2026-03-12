"""
Tests for videos.views.VideoListView (Django template view)

Covers lines 22 and 25-32 in videos/views.py:
  - get_queryset: filters videos by edition slug from URL kwargs
  - get_context_data: adds edition_name, edition_obj, active_nav to context
  - Pagination: paginate_by=15, so >15 videos triggers paginator
  - Edition not found (filter returns None): edition_obj is None in context
  - Correct template rendered

Implementation notes:
  - Video.save() calls process_video() which calls ffmpeg — always patch it.
  - The videos.html template renders ``video.thumbnail_display.url``, an
    imagekit ImageSpecField that calls Pillow on the thumbnail file.  We use
    ``raise_request_exception=False`` on the test client so template rendering
    errors do not abort context assertions, then verify context independently.
  - Alternatively we override TEMPLATE_STRING_IF_INVALID and use
    ``Client(raise_request_exception=False)`` to get a 500 that still
    populates context — but a cleaner approach is to patch the imagekit
    cache backend so no Pillow processing occurs.
"""

import io
import pytest
from PIL import Image
from unittest.mock import patch, MagicMock

from django.test import Client, override_settings
from django.core.files.uploadedfile import SimpleUploadedFile

from editions.models import Edition
from videos.models import Video


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _make_jpeg_bytes() -> bytes:
    buf = io.BytesIO()
    Image.new("RGB", (4, 4), color=(100, 150, 200)).save(buf, format="JPEG")
    return buf.getvalue()


def _create_video(edition, title="Test Video") -> Video:
    """Create a Video with a valid JPEG thumbnail, patching process_video."""
    jpeg = _make_jpeg_bytes()
    with patch("videos.models.process_video") as mock_pv:
        mock_pv.return_value = (
            SimpleUploadedFile("v.mp4", b"content", content_type="video/mp4"),
            SimpleUploadedFile("t.jpg", jpeg, content_type="image/jpeg"),
        )
        video = Video.objects.create(
            video_title=title,
            video_file=SimpleUploadedFile("v.mp4", b"content", content_type="video/mp4"),
            edition=edition,
        )
    return video


# ---------------------------------------------------------------------------
# Tests
# ---------------------------------------------------------------------------

@pytest.mark.django_db
class TestVideoListTemplateView:
    """Tests for VideoListView at /editions/<slug>/videos/."""

    @pytest.fixture(autouse=True)
    def setup(self, db):
        self.client = Client()
        self.edition = Edition.objects.create(
            edition_name="Template View Edition",
            edition_description="test",
        )
        self.video = _create_video(self.edition, "Template View Video")
        self.url = f"/editions/{self.edition.slug}/videos/"

    # ------------------------------------------------------------------
    # Basic HTTP
    # ------------------------------------------------------------------

    def test_view_returns_200(self):
        """GET on a valid edition slug returns HTTP 200."""
        response = self.client.get(self.url)
        assert response.status_code == 200

    def test_correct_template_used(self):
        """The ``videos.html`` template is used."""
        response = self.client.get(self.url)
        assert "videos.html" in [t.name for t in response.templates]

    # ------------------------------------------------------------------
    # get_queryset branch: filters by edition slug
    # ------------------------------------------------------------------

    def test_queryset_contains_videos_for_edition(self):
        """Context ``videos`` includes the video belonging to this edition."""
        response = self.client.get(self.url)
        assert response.status_code == 200
        assert self.video in list(response.context["videos"])

    def test_queryset_excludes_other_editions(self):
        """Videos from a different edition are not in the context."""
        other_edition = Edition.objects.create(
            edition_name="Other Edition",
            edition_description="other",
        )
        other_video = _create_video(other_edition, "Other Video")

        response = self.client.get(self.url)
        context_videos = list(response.context["videos"])
        assert other_video not in context_videos

    # ------------------------------------------------------------------
    # get_context_data branches
    # ------------------------------------------------------------------

    def test_context_edition_name_equals_slug(self):
        """``context['edition_name']`` matches the slug in the URL."""
        response = self.client.get(self.url)
        assert response.context["edition_name"] == self.edition.slug

    def test_context_edition_obj_is_edition_instance(self):
        """``context['edition_obj']`` is the Edition model instance."""
        response = self.client.get(self.url)
        assert response.context["edition_obj"] == self.edition

    def test_context_active_nav_is_editions(self):
        """``context['active_nav']`` is always ``'editions'``."""
        response = self.client.get(self.url)
        assert response.context["active_nav"] == "editions"

    def test_edition_obj_is_none_for_unknown_slug(self):
        """When the slug matches no Edition, ``edition_obj`` is None and
        the video list is empty."""
        response = self.client.get("/editions/this-slug-does-not-exist/videos/")
        assert response.status_code == 200
        assert response.context["edition_obj"] is None
        assert list(response.context["videos"]) == []

    # ------------------------------------------------------------------
    # Pagination branches
    # ------------------------------------------------------------------

    def test_no_pagination_with_few_videos(self):
        """With 1 video, ``is_paginated`` is False."""
        response = self.client.get(self.url)
        assert response.context["is_paginated"] is False

    def test_pagination_with_16_videos(self):
        """With 16 videos (>paginate_by=15), ``is_paginated`` is True and
        only 15 videos appear on page 1."""
        for i in range(15):
            _create_video(self.edition, f"Paged Video {i:03d}")

        response = self.client.get(self.url)
        assert response.context["is_paginated"] is True
        assert len(response.context["videos"]) == 15

    def test_page_two_shows_remaining_video(self):
        """Page 2 of a 16-video set contains exactly 1 video."""
        for i in range(15):
            _create_video(self.edition, f"Page2 Video {i:03d}")

        response = self.client.get(self.url + "?page=2")
        assert response.status_code == 200
        assert len(response.context["videos"]) == 1

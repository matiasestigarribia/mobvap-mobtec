"""
Tests for homepagecontents.models.HomePageContent.
"""

import pytest

from homepagecontents.models import HomePageContent
from tests.conftest import HomePageContentFactory


@pytest.mark.django_db
class TestHomePageContentModel:
    """Unit tests for the HomePageContent model."""

    def test_create_with_required_fields(self):
        """Model persists when all non-optional fields are provided."""
        obj = HomePageContent.objects.create(
            home_title="MOBVAP 2025",
            youtube_url="https://www.youtube.com/watch?v=abc123",
            block_content1_title="Bloco 1",
            block_content1_text="Texto do bloco 1.",
            block_content2_title="Bloco 2",
            block_content2_text="Texto do bloco 2.",
            schedule_table_html="<table></table>",
            block_content3_title="Bloco 3",
            block_content3_text="Texto do bloco 3.",
        )
        assert obj.pk is not None

    def test_str_representation_returns_home_title(self):
        obj = HomePageContentFactory(home_title="MOBVAP Homepage 2025")
        assert str(obj) == "MOBVAP Homepage 2025"

    def test_youtube_url_is_stored(self):
        url = "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
        obj = HomePageContentFactory(youtube_url=url)
        obj.refresh_from_db()
        assert obj.youtube_url == url

    def test_youtube_url2_is_optional(self):
        obj = HomePageContentFactory(youtube_url2=None)
        assert obj.youtube_url2 is None

    def test_youtube_url2_can_be_set(self):
        url2 = "https://www.youtube.com/watch?v=optional"
        obj = HomePageContentFactory(youtube_url2=url2)
        obj.refresh_from_db()
        assert obj.youtube_url2 == url2

    def test_schedule_table_title_is_optional(self):
        obj = HomePageContentFactory(schedule_table_title=None)
        assert obj.schedule_table_title is None

    def test_block_content4_title_has_default(self):
        """block_content4_title defaults to '.' if not provided."""
        obj = HomePageContent.objects.create(
            home_title="Default Test",
            youtube_url="https://www.youtube.com/watch?v=x",
            block_content1_title="B1",
            block_content1_text="T1",
            block_content2_title="B2",
            block_content2_text="T2",
            schedule_table_html="<table></table>",
            block_content3_title="B3",
            block_content3_text="T3",
        )
        assert obj.block_content4_title == "."

    def test_block_content4_text_has_default(self):
        """block_content4_text defaults to '.' if not provided."""
        obj = HomePageContent.objects.create(
            home_title="Default Text Test",
            youtube_url="https://www.youtube.com/watch?v=x",
            block_content1_title="B1",
            block_content1_text="T1",
            block_content2_title="B2",
            block_content2_text="T2",
            schedule_table_html="<table></table>",
            block_content3_title="B3",
            block_content3_text="T3",
        )
        assert obj.block_content4_text == "."

    def test_created_at_is_auto_populated(self):
        obj = HomePageContentFactory()
        assert obj.created_at is not None

    def test_updated_at_is_auto_populated(self):
        obj = HomePageContentFactory()
        assert obj.updated_at is not None

    def test_schedule_table_html_stores_html(self):
        html = "<table><tr><td>09:00</td><td>Abertura</td></tr></table>"
        obj = HomePageContentFactory(schedule_table_html=html)
        obj.refresh_from_db()
        assert obj.schedule_table_html == html

    def test_multiple_instances_can_coexist(self):
        HomePageContentFactory()
        HomePageContentFactory()
        assert HomePageContent.objects.count() == 2

"""
Tests for homepagecontents.serializers.HomePageContentSerializer.
"""

import pytest

from homepagecontents.serializers import HomePageContentSerializer
from tests.conftest import HomePageContentFactory


@pytest.mark.django_db
class TestHomePageContentSerializer:
    """Unit tests for HomePageContentSerializer."""

    def test_serializer_contains_expected_fields(self):
        obj = HomePageContentFactory()
        serializer = HomePageContentSerializer(obj)
        data = serializer.data

        expected_fields = {
            "id",
            "home_title",
            "youtube_url",
            "block_content1_title",
            "block_content1_text",
            "youtube_url2",
            "block_content2_title",
            "block_content2_text",
            "schedule_table_html",
            "block_content3_title",
            "block_content3_text",
            "block_content4_title",
            "block_content4_text",
            "created_at",
            "updated_at",
        }
        assert expected_fields == set(data.keys())

    def test_serializer_id_matches_model_pk(self):
        obj = HomePageContentFactory()
        serializer = HomePageContentSerializer(obj)
        assert serializer.data["id"] == obj.pk

    def test_serializer_home_title_value(self):
        obj = HomePageContentFactory(home_title="MOBVAP 2025")
        serializer = HomePageContentSerializer(obj)
        assert serializer.data["home_title"] == "MOBVAP 2025"

    def test_serializer_youtube_url_value(self):
        url = "https://www.youtube.com/watch?v=abc"
        obj = HomePageContentFactory(youtube_url=url)
        serializer = HomePageContentSerializer(obj)
        assert serializer.data["youtube_url"] == url

    def test_serializer_youtube_url2_none_when_not_set(self):
        obj = HomePageContentFactory(youtube_url2=None)
        serializer = HomePageContentSerializer(obj)
        assert serializer.data["youtube_url2"] is None

    def test_serializer_schedule_table_html_value(self):
        html = "<table><tr><td>Test</td></tr></table>"
        obj = HomePageContentFactory(schedule_table_html=html)
        serializer = HomePageContentSerializer(obj)
        assert serializer.data["schedule_table_html"] == html

    def test_serializer_block_content4_title_value(self):
        obj = HomePageContentFactory(block_content4_title="Parceiros")
        serializer = HomePageContentSerializer(obj)
        assert serializer.data["block_content4_title"] == "Parceiros"

    def test_serializer_block_content4_text_value(self):
        obj = HomePageContentFactory(block_content4_text="Texto dos parceiros.")
        serializer = HomePageContentSerializer(obj)
        assert serializer.data["block_content4_text"] == "Texto dos parceiros."

    def test_serializer_does_not_expose_schedule_table_title(self):
        """schedule_table_title is not included in the serializer fields."""
        obj = HomePageContentFactory()
        serializer = HomePageContentSerializer(obj)
        assert "schedule_table_title" not in serializer.data

    def test_serializer_created_at_is_present(self):
        obj = HomePageContentFactory()
        serializer = HomePageContentSerializer(obj)
        assert serializer.data["created_at"] is not None

    def test_serializer_updated_at_is_present(self):
        obj = HomePageContentFactory()
        serializer = HomePageContentSerializer(obj)
        assert serializer.data["updated_at"] is not None

    def test_serializer_list_of_multiple_objects(self):
        HomePageContentFactory.create_batch(3)
        from homepagecontents.models import HomePageContent
        objs = HomePageContent.objects.all()
        serializer = HomePageContentSerializer(objs, many=True)
        assert len(serializer.data) == 3

    def test_serializer_read_only_behavior_missing_required_fields(self):
        """Serializer validation fails when required fields are absent."""
        serializer = HomePageContentSerializer(data={})
        assert not serializer.is_valid()
        assert "home_title" in serializer.errors

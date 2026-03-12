"""
Tests for rulespagecontents.serializers.RulesPageContentSerializer.
"""

import pytest

from rulespagecontents.models import RulesPageContent
from rulespagecontents.serializers import RulesPageContentSerializer
from tests.conftest import RulesPageContentFactory


@pytest.mark.django_db
class TestRulesPageContentSerializer:
    """Unit tests for RulesPageContentSerializer."""

    def test_serializer_contains_expected_fields(self):
        obj = RulesPageContentFactory()
        serializer = RulesPageContentSerializer(obj)
        data = serializer.data

        expected_fields = {"id", "rules_title", "rules_text", "created_at", "updated_at"}
        assert expected_fields == set(data.keys())

    def test_serializer_does_not_expose_pdf_fields(self):
        """PDF file fields are intentionally excluded from the serializer."""
        obj = RulesPageContentFactory()
        serializer = RulesPageContentSerializer(obj)
        data = serializer.data

        assert "pdf_file_mobvap" not in data
        assert "pdf_file_mobtec" not in data

    def test_serializer_does_not_expose_featured_image(self):
        """No featured_image field exists on the model or serializer (bug was fixed)."""
        obj = RulesPageContentFactory()
        serializer = RulesPageContentSerializer(obj)
        data = serializer.data

        assert "featured_image" not in data

    def test_serializer_id_matches_model_pk(self):
        obj = RulesPageContentFactory()
        serializer = RulesPageContentSerializer(obj)
        assert serializer.data["id"] == obj.pk

    def test_serializer_rules_title_value(self):
        obj = RulesPageContentFactory(rules_title="Regulamento Oficial")
        serializer = RulesPageContentSerializer(obj)
        assert serializer.data["rules_title"] == "Regulamento Oficial"

    def test_serializer_rules_text_value(self):
        obj = RulesPageContentFactory(rules_text="Texto completo.")
        serializer = RulesPageContentSerializer(obj)
        assert serializer.data["rules_text"] == "Texto completo."

    def test_serializer_created_at_is_present(self):
        obj = RulesPageContentFactory()
        serializer = RulesPageContentSerializer(obj)
        assert serializer.data["created_at"] is not None

    def test_serializer_updated_at_is_present(self):
        obj = RulesPageContentFactory()
        serializer = RulesPageContentSerializer(obj)
        assert serializer.data["updated_at"] is not None

    def test_serializer_list_of_multiple_objects(self):
        objs = RulesPageContentFactory.create_batch(3)
        serializer = RulesPageContentSerializer(objs, many=True)
        assert len(serializer.data) == 3

    def test_serializer_read_only_behavior(self):
        """Serializer is used in a ReadOnlyModelViewSet; validate is_valid on empty data."""
        serializer = RulesPageContentSerializer(data={})
        # rules_title and rules_text are required — validation should fail
        assert not serializer.is_valid()
        assert "rules_title" in serializer.errors
        assert "rules_text" in serializer.errors

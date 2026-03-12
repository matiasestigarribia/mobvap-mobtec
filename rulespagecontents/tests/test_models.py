"""
Tests for rulespagecontents.models.RulesPageContent.
"""

import pytest

from rulespagecontents.models import RulesPageContent
from tests.conftest import RulesPageContentFactory


@pytest.mark.django_db
class TestRulesPageContentModel:
    """Unit tests for the RulesPageContent model."""

    def test_create_rules_page_content_with_required_fields(self):
        """Model can be created with only the required fields."""
        obj = RulesPageContent.objects.create(
            rules_title="Regulamento 2025",
            rules_text="Texto completo do regulamento.",
        )
        assert obj.pk is not None

    def test_str_representation_returns_title(self):
        obj = RulesPageContentFactory(rules_title="Regulamento MOBVAP")
        assert str(obj) == "Regulamento MOBVAP"

    def test_rules_title_max_length(self):
        """rules_title accepts strings up to 200 characters."""
        long_title = "A" * 200
        obj = RulesPageContentFactory(rules_title=long_title)
        assert len(obj.rules_title) == 200

    def test_rules_text_is_stored(self):
        obj = RulesPageContentFactory(rules_text="Texto do regulamento detalhado.")
        obj.refresh_from_db()
        assert obj.rules_text == "Texto do regulamento detalhado."

    def test_pdf_file_mobvap_is_optional(self):
        """pdf_file_mobvap can be None/blank."""
        obj = RulesPageContentFactory(pdf_file_mobvap=None)
        assert not obj.pdf_file_mobvap

    def test_pdf_file_mobtec_is_optional(self):
        """pdf_file_mobtec can be None/blank."""
        obj = RulesPageContentFactory(pdf_file_mobtec=None)
        assert not obj.pdf_file_mobtec

    def test_created_at_is_auto_populated(self):
        obj = RulesPageContentFactory()
        assert obj.created_at is not None

    def test_updated_at_is_auto_populated(self):
        obj = RulesPageContentFactory()
        assert obj.updated_at is not None

    def test_verbose_name_plural(self):
        assert RulesPageContent._meta.verbose_name_plural == "Rules Page Contents"

    def test_multiple_instances_can_coexist(self):
        RulesPageContentFactory(rules_title="Regulamento 2024")
        RulesPageContentFactory(rules_title="Regulamento 2025")
        assert RulesPageContent.objects.count() == 2

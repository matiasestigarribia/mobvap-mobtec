"""
Tests for rulespagecontents views:
- RulesPageContentViewSet (DRF ReadOnlyModelViewSet at /api/v1/rules/)
- RulesPageView (Django TemplateView at /rules/)
"""

import pytest
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from rulespagecontents.models import RulesPageContent
from tests.conftest import RulesPageContentFactory


# ---------------------------------------------------------------------------
# RulesPageContentViewSet — /api/v1/rules/
# ---------------------------------------------------------------------------

@pytest.mark.django_db
class TestRulesPageContentViewSet:
    """API tests for the read-only rules viewset."""

    def test_list_returns_200(self, api_client):
        response = api_client.get("/api/v1/rules/")
        assert response.status_code == status.HTTP_200_OK

    def test_list_returns_all_rules_objects(self, api_client):
        RulesPageContentFactory.create_batch(2)
        response = api_client.get("/api/v1/rules/")

        results = response.data if isinstance(response.data, list) else response.data.get("results", response.data)
        assert len(results) == 2

    def test_list_response_contains_expected_fields(self, api_client):
        RulesPageContentFactory()
        response = api_client.get("/api/v1/rules/")

        results = response.data if isinstance(response.data, list) else response.data.get("results", response.data)
        item = results[0]
        expected_fields = {"id", "rules_title", "rules_text", "created_at", "updated_at"}
        assert expected_fields.issubset(set(item.keys()))

    def test_list_does_not_expose_pdf_fields(self, api_client):
        RulesPageContentFactory()
        response = api_client.get("/api/v1/rules/")

        results = response.data if isinstance(response.data, list) else response.data.get("results", response.data)
        item = results[0]
        assert "pdf_file_mobvap" not in item
        assert "pdf_file_mobtec" not in item

    def test_list_does_not_expose_featured_image(self, api_client):
        RulesPageContentFactory()
        response = api_client.get("/api/v1/rules/")

        results = response.data if isinstance(response.data, list) else response.data.get("results", response.data)
        item = results[0]
        assert "featured_image" not in item

    def test_post_returns_405_method_not_allowed(self, api_client):
        data = {"rules_title": "Hack", "rules_text": "Intruder"}
        response = api_client.post("/api/v1/rules/", data)
        assert response.status_code == status.HTTP_405_METHOD_NOT_ALLOWED

    def test_put_returns_405_method_not_allowed(self, api_client):
        obj = RulesPageContentFactory()
        data = {"rules_title": "Updated", "rules_text": "Updated text"}
        response = api_client.put(f"/api/v1/rules/{obj.pk}/", data)
        assert response.status_code == status.HTTP_405_METHOD_NOT_ALLOWED

    def test_delete_returns_405_method_not_allowed(self, api_client):
        obj = RulesPageContentFactory()
        response = api_client.delete(f"/api/v1/rules/{obj.pk}/")
        assert response.status_code == status.HTTP_405_METHOD_NOT_ALLOWED

    def test_retrieve_single_object_returns_200(self, api_client):
        obj = RulesPageContentFactory()
        response = api_client.get(f"/api/v1/rules/{obj.pk}/")
        assert response.status_code == status.HTTP_200_OK
        assert response.data["id"] == obj.pk

    def test_retrieve_nonexistent_object_returns_404(self, api_client):
        response = api_client.get("/api/v1/rules/99999/")
        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_list_empty_when_no_rules_objects(self, api_client):
        response = api_client.get("/api/v1/rules/")
        results = response.data if isinstance(response.data, list) else response.data.get("results", response.data)
        assert len(results) == 0


# ---------------------------------------------------------------------------
# RulesPageView — template view at /rules/
# ---------------------------------------------------------------------------

@pytest.mark.django_db
class TestRulesPageView:
    """Template view tests for the rules page."""

    def test_get_returns_200(self, client):
        response = client.get(reverse("rules-page"))
        assert response.status_code == 200

    def test_get_uses_correct_template(self, client):
        response = client.get(reverse("rules-page"))
        assert "rules.html" in [t.name for t in response.templates]

    def test_get_sets_active_nav_context(self, client):
        response = client.get(reverse("rules-page"))
        assert response.context["active_nav"] == "rules"

    def test_get_passes_first_rules_content_to_context(self, db, client):
        obj = RulesPageContentFactory(rules_title="Regulamento 2025")
        response = client.get(reverse("rules-page"))
        assert response.context["rules_content"] is not None
        assert response.context["rules_content"].pk == obj.pk

    def test_get_rules_content_is_none_when_no_records(self, db, client):
        """TemplateView should not crash when no RulesPageContent exists."""
        assert RulesPageContent.objects.count() == 0
        response = client.get(reverse("rules-page"))
        assert response.status_code == 200
        assert response.context["rules_content"] is None

    def test_post_to_rules_page_returns_405(self, client):
        """TemplateView does not handle POST."""
        response = client.post(reverse("rules-page"), data={})
        assert response.status_code == 405

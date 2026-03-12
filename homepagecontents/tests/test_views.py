"""
Tests for homepagecontents views:
- HomePageContentViewSet (DRF ReadOnlyModelViewSet at /api/v1/home/)
- HomePageView (Django TemplateView at /home/ and /)
"""

import pytest
from django.urls import reverse
from rest_framework import status

from homepagecontents.models import HomePageContent
from tests.conftest import HomePageContentFactory


# ---------------------------------------------------------------------------
# HomePageContentViewSet — /api/v1/home/
# ---------------------------------------------------------------------------

@pytest.mark.django_db
class TestHomePageContentViewSet:
    """API tests for the read-only home content viewset."""

    def test_list_returns_200(self, api_client):
        response = api_client.get("/api/v1/home/")
        assert response.status_code == status.HTTP_200_OK

    def test_list_returns_all_home_objects(self, api_client):
        HomePageContentFactory.create_batch(2)
        response = api_client.get("/api/v1/home/")

        results = response.data if isinstance(response.data, list) else response.data.get("results", response.data)
        assert len(results) == 2

    def test_list_response_contains_expected_fields(self, api_client):
        HomePageContentFactory()
        response = api_client.get("/api/v1/home/")

        results = response.data if isinstance(response.data, list) else response.data.get("results", response.data)
        item = results[0]
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
        assert expected_fields.issubset(set(item.keys()))

    def test_list_does_not_expose_schedule_table_title(self, api_client):
        """schedule_table_title is excluded from the serializer."""
        HomePageContentFactory()
        response = api_client.get("/api/v1/home/")

        results = response.data if isinstance(response.data, list) else response.data.get("results", response.data)
        item = results[0]
        assert "schedule_table_title" not in item

    def test_post_returns_405_method_not_allowed(self, api_client):
        data = {"home_title": "Hacked"}
        response = api_client.post("/api/v1/home/", data)
        assert response.status_code == status.HTTP_405_METHOD_NOT_ALLOWED

    def test_put_returns_405_method_not_allowed(self, api_client):
        obj = HomePageContentFactory()
        response = api_client.put(f"/api/v1/home/{obj.pk}/", {"home_title": "x"})
        assert response.status_code == status.HTTP_405_METHOD_NOT_ALLOWED

    def test_delete_returns_405_method_not_allowed(self, api_client):
        obj = HomePageContentFactory()
        response = api_client.delete(f"/api/v1/home/{obj.pk}/")
        assert response.status_code == status.HTTP_405_METHOD_NOT_ALLOWED

    def test_retrieve_single_object_returns_200(self, api_client):
        obj = HomePageContentFactory()
        response = api_client.get(f"/api/v1/home/{obj.pk}/")
        assert response.status_code == status.HTTP_200_OK
        assert response.data["id"] == obj.pk

    def test_retrieve_nonexistent_object_returns_404(self, api_client):
        response = api_client.get("/api/v1/home/99999/")
        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_list_empty_when_no_objects(self, api_client):
        response = api_client.get("/api/v1/home/")
        results = response.data if isinstance(response.data, list) else response.data.get("results", response.data)
        assert len(results) == 0

    def test_list_home_title_matches_factory_value(self, api_client):
        HomePageContentFactory(home_title="MOBVAP 2025")
        response = api_client.get("/api/v1/home/")

        results = response.data if isinstance(response.data, list) else response.data.get("results", response.data)
        assert results[0]["home_title"] == "MOBVAP 2025"


# ---------------------------------------------------------------------------
# HomePageView — template view at / and /home/
# ---------------------------------------------------------------------------

@pytest.mark.django_db
class TestHomePageView:
    """Template view tests for the home page."""

    def test_get_home_path_returns_200(self, client):
        response = client.get(reverse("home-page"))
        assert response.status_code == 200

    def test_get_index_path_returns_200(self, client):
        response = client.get(reverse("index"))
        assert response.status_code == 200

    def test_get_uses_correct_template(self, client):
        response = client.get(reverse("home-page"))
        assert "home.html" in [t.name for t in response.templates]

    def test_get_sets_active_nav_context(self, client):
        response = client.get(reverse("home-page"))
        assert response.context["active_nav"] == "home"

    def test_get_passes_first_home_content_to_context(self, db, client):
        obj = HomePageContentFactory(home_title="MOBVAP 2025")
        response = client.get(reverse("home-page"))
        assert response.context["home_content"] is not None
        assert response.context["home_content"].pk == obj.pk

    def test_get_home_content_is_none_when_no_records(self, db, client):
        """TemplateView must not crash when HomePageContent table is empty."""
        assert HomePageContent.objects.count() == 0
        response = client.get(reverse("home-page"))
        assert response.status_code == 200
        assert response.context["home_content"] is None

    def test_post_to_home_page_returns_405(self, client):
        """TemplateView does not handle POST."""
        response = client.post(reverse("home-page"), data={})
        assert response.status_code == 405

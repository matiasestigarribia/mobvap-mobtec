import pytest
from django.test import TestCase, override_settings, Client as DjangoClient
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from editions.models import Edition

from tests.conftest import EditionFactory


@override_settings(SECURE_SSL_REDIRECT=False)
class EditionViewTest(TestCase):

    def setUp(self):
        self.client = APIClient()
        self.edition = Edition.objects.create(
            edition_name="Test Edition",
            edition_description='Desc'
        )

    def test_list_editions_success(self):
        response = self.client.get('/api/v1/editions/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_create_edition_method_not_allowed(self):
        data = {'edition_name': 'Hacker Edition'}
        response = self.client.post('/api/v1/editions/', data)

        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_delete_edition_method_not_allowed(self):

        response = self.client.delete(f'/api/v1/editions/{self.edition.edition_name}/')
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)


# ---------------------------------------------------------------------------
# Additional pytest-style tests — Step 5b expansion
# ---------------------------------------------------------------------------

@pytest.mark.django_db
class TestEditionApiDataStructure:
    """Verify data structure and content returned by the editions API."""

    def test_list_response_contains_expected_fields(self, api_client):
        EditionFactory()
        response = api_client.get("/api/v1/editions/")
        assert response.status_code == status.HTTP_200_OK

        results = response.data if isinstance(response.data, list) else response.data.get("results", response.data)
        item = results[0]
        expected_fields = {
            "id", "edition_name", "edition_description",
            "preview_image1", "preview_image2", "created_at", "updated_at",
        }
        assert expected_fields.issubset(set(item.keys()))

    def test_list_returns_multiple_editions(self, api_client):
        EditionFactory.create_batch(3)
        response = api_client.get("/api/v1/editions/")
        results = response.data if isinstance(response.data, list) else response.data.get("results", response.data)
        assert len(results) == 3

    def test_list_empty_when_no_editions(self, api_client):
        response = api_client.get("/api/v1/editions/")
        results = response.data if isinstance(response.data, list) else response.data.get("results", response.data)
        assert len(results) == 0

    def test_retrieve_edition_by_name_returns_200(self, api_client):
        edition = EditionFactory()
        response = api_client.get(f"/api/v1/editions/{edition.edition_name}/")
        assert response.status_code == status.HTTP_200_OK
        assert response.data["edition_name"] == edition.edition_name

    def test_retrieve_nonexistent_edition_returns_404(self, api_client):
        response = api_client.get("/api/v1/editions/does-not-exist/")
        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_put_edition_returns_405(self, api_client):
        edition = EditionFactory()
        response = api_client.put(f"/api/v1/editions/{edition.edition_name}/", {"edition_name": "x"})
        assert response.status_code == status.HTTP_405_METHOD_NOT_ALLOWED

    def test_edition_name_in_response_matches_stored_value(self, api_client):
        EditionFactory(edition_name="Edicao Especial")
        response = api_client.get("/api/v1/editions/")
        results = response.data if isinstance(response.data, list) else response.data.get("results", response.data)
        names = [item["edition_name"] for item in results]
        assert "Edicao Especial" in names


@pytest.mark.django_db
class TestEditionPageTemplateView:
    """Django template view tests for /editions/."""

    def test_get_editions_page_returns_200(self, client):
        response = client.get(reverse("editions-list"))
        assert response.status_code == 200

    def test_get_editions_page_uses_correct_template(self, client):
        response = client.get(reverse("editions-list"))
        assert "editions.html" in [t.name for t in response.templates]

    def test_get_editions_page_sets_active_nav(self, db, client):
        response = client.get(reverse("editions-list"))
        assert response.context["active_nav"] == "editions"

    def test_get_editions_page_lists_all_editions(self, db, client):
        EditionFactory.create_batch(2)
        response = client.get(reverse("editions-list"))
        assert len(response.context["editions"]) == 2

    def test_get_editions_page_empty_state(self, db, client):
        response = client.get(reverse("editions-list"))
        assert response.status_code == 200
        assert list(response.context["editions"]) == []

    def test_get_editions_page_pagination_page_1(self, db, client):
        """With 7 editions and paginate_by=6, page 1 has 6 items."""
        EditionFactory.create_batch(7)
        response = client.get(reverse("editions-list") + "?page=1")
        assert response.status_code == 200
        assert len(response.context["editions"]) == 6

    def test_get_editions_page_pagination_page_2(self, db, client):
        """Page 2 contains the remaining 1 edition."""
        EditionFactory.create_batch(7)
        response = client.get(reverse("editions-list") + "?page=2")
        assert response.status_code == 200
        assert len(response.context["editions"]) == 1

    def test_post_to_editions_page_returns_405(self, client):
        response = client.post(reverse("editions-list"), data={})
        assert response.status_code == 405

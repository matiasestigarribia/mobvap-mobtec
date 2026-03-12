import pytest
from django.test import TestCase, override_settings
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from editions.models import Edition
from photos.models import Photo

from tests.conftest import EditionFactory, PhotoFactory


@override_settings(SECURE_SSL_REDIRECT=False)
class PhotoViewTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        
        self.edition = Edition.objects.create(
            edition_name="Edition View",
            edition_description="Desc"
        )
        self.photo = Photo.objects.create(
            image_title="Photo 1",
            edition=self.edition,
            image_file='path/false/photo.jpg'
        )
        
        self.list_url = f'/api/v1/editions/{self.edition.slug}/photos/'
    
    def test_list_photos_success(self):
        response = self.client.get(self.list_url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        if 'results' in response.data:
            self.assertEqual(len(response.data['results']), 1)
        else:
            self.assertEqual(len(response.data), 1)
    
    def test_create_photo_forbidden(self):
        data = {'image_title': 'Hacker Photo'}
        response = self.client.post(self.list_url, data)
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)


# ---------------------------------------------------------------------------
# Additional pytest-style tests — Step 5b expansion
# ---------------------------------------------------------------------------

@pytest.mark.django_db
class TestPhotoApiDataStructure:
    """Verify data structure, edition scoping, and empty state for the photos API."""

    def test_list_response_contains_expected_fields(self, api_client):
        edition = EditionFactory()
        PhotoFactory(edition=edition)
        url = f"/api/v1/editions/{edition.slug}/photos/"
        response = api_client.get(url)
        assert response.status_code == status.HTTP_200_OK

        results = response.data if isinstance(response.data, list) else response.data.get("results", response.data)
        item = results[0]
        expected_fields = {
            "id", "image_file", "image_title", "image_description",
            "edition", "created_at", "updated_at",
        }
        assert expected_fields.issubset(set(item.keys()))

    def test_list_is_filtered_by_edition_slug(self, api_client):
        """Photos from a different edition must not appear in the response."""
        edition_a = EditionFactory()
        edition_b = EditionFactory()
        photo_a = PhotoFactory(edition=edition_a)
        PhotoFactory(edition=edition_b)

        url = f"/api/v1/editions/{edition_a.slug}/photos/"
        response = api_client.get(url)
        results = response.data if isinstance(response.data, list) else response.data.get("results", response.data)

        ids = [item["id"] for item in results]
        assert photo_a.id in ids
        assert len(ids) == 1

    def test_list_returns_multiple_photos_for_edition(self, api_client):
        edition = EditionFactory()
        PhotoFactory.create_batch(3, edition=edition)
        url = f"/api/v1/editions/{edition.slug}/photos/"
        response = api_client.get(url)
        results = response.data if isinstance(response.data, list) else response.data.get("results", response.data)
        assert len(results) == 3

    def test_list_empty_state_when_no_photos_for_edition(self, api_client):
        """API returns an empty list when the edition has no photos."""
        edition = EditionFactory()
        url = f"/api/v1/editions/{edition.slug}/photos/"
        response = api_client.get(url)
        results = response.data if isinstance(response.data, list) else response.data.get("results", response.data)
        assert results == []

    def test_retrieve_single_photo_returns_200(self, api_client):
        edition = EditionFactory()
        photo = PhotoFactory(edition=edition)
        url = f"/api/v1/editions/{edition.slug}/photos/{photo.pk}/"
        response = api_client.get(url)
        assert response.status_code == status.HTTP_200_OK
        assert response.data["id"] == photo.pk

    def test_retrieve_photo_nested_edition_id_matches(self, api_client):
        """The 'edition' field in the response is the FK pk of the edition."""
        edition = EditionFactory()
        photo = PhotoFactory(edition=edition)
        url = f"/api/v1/editions/{edition.slug}/photos/{photo.pk}/"
        response = api_client.get(url)
        assert response.data["edition"] == edition.pk

    def test_delete_photo_returns_405(self, api_client):
        edition = EditionFactory()
        photo = PhotoFactory(edition=edition)
        url = f"/api/v1/editions/{edition.slug}/photos/{photo.pk}/"
        response = api_client.delete(url)
        assert response.status_code == status.HTTP_405_METHOD_NOT_ALLOWED

    def test_put_photo_returns_405(self, api_client):
        edition = EditionFactory()
        photo = PhotoFactory(edition=edition)
        url = f"/api/v1/editions/{edition.slug}/photos/{photo.pk}/"
        response = api_client.put(url, {"image_title": "Updated"})
        assert response.status_code == status.HTTP_405_METHOD_NOT_ALLOWED


@pytest.mark.django_db
class TestPhotoListTemplateView:
    """Django template view tests for /editions/<slug>/photos/."""

    def test_get_photo_list_returns_200(self, client):
        edition = EditionFactory()
        PhotoFactory(edition=edition)
        url = reverse("photo-list-by-edition", kwargs={"edition_name": edition.slug})
        response = client.get(url)
        assert response.status_code == 200

    def test_get_photo_list_uses_correct_template(self, client):
        edition = EditionFactory()
        url = reverse("photo-list-by-edition", kwargs={"edition_name": edition.slug})
        response = client.get(url)
        assert "photos.html" in [t.name for t in response.templates]

    def test_get_photo_list_sets_active_nav(self, client):
        edition = EditionFactory()
        url = reverse("photo-list-by-edition", kwargs={"edition_name": edition.slug})
        response = client.get(url)
        assert response.context["active_nav"] == "editions"

    def test_get_photo_list_only_shows_photos_for_edition(self, client):
        edition_a = EditionFactory()
        edition_b = EditionFactory()
        photo_a = PhotoFactory(edition=edition_a)
        PhotoFactory(edition=edition_b)

        url = reverse("photo-list-by-edition", kwargs={"edition_name": edition_a.slug})
        response = client.get(url)
        photo_ids = [p.id for p in response.context["photos"]]
        assert photo_a.id in photo_ids
        assert len(photo_ids) == 1

    def test_get_photo_list_empty_state(self, client):
        """Template view returns 200 with empty list when edition has no photos."""
        edition = EditionFactory()
        url = reverse("photo-list-by-edition", kwargs={"edition_name": edition.slug})
        response = client.get(url)
        assert response.status_code == 200
        assert list(response.context["photos"]) == []

    def test_get_photo_list_passes_edition_obj_to_context(self, client):
        edition = EditionFactory()
        PhotoFactory(edition=edition)
        url = reverse("photo-list-by-edition", kwargs={"edition_name": edition.slug})
        response = client.get(url)
        assert response.context["edition_obj"] is not None
        assert response.context["edition_obj"].pk == edition.pk

    def test_get_photo_list_pagination_page_1(self, client):
        """With 16 photos and paginate_by=15, page 1 has 15 items."""
        edition = EditionFactory()
        PhotoFactory.create_batch(16, edition=edition)
        url = reverse("photo-list-by-edition", kwargs={"edition_name": edition.slug}) + "?page=1"
        response = client.get(url)
        assert response.status_code == 200
        assert len(response.context["photos"]) == 15

    def test_get_photo_list_pagination_page_2(self, client):
        """Page 2 contains the remaining 1 photo."""
        edition = EditionFactory()
        PhotoFactory.create_batch(16, edition=edition)
        url = reverse("photo-list-by-edition", kwargs={"edition_name": edition.slug}) + "?page=2"
        response = client.get(url)
        assert response.status_code == 200
        assert len(response.context["photos"]) == 1

    def test_post_to_photo_list_returns_405(self, client):
        edition = EditionFactory()
        url = reverse("photo-list-by-edition", kwargs={"edition_name": edition.slug})
        response = client.post(url, data={})
        assert response.status_code == 405

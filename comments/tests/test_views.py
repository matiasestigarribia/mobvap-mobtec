"""
Tests for comments views:
- CommentPageView (Django ListView with POST handling)
- CommentViewSet (DRF ReadOnlyModelViewSet, approved-only filter)

The post_save signal calls moderate_comment (Azure AI) on every Comment.objects.create().
All tests that call create() mock comments.signals.moderate_comment to avoid Azure calls
and to control the resulting comment_status predictably.
"""

import pytest
from unittest.mock import patch
from django.urls import reverse
from rest_framework import status

from comments.models import Comment
from tests.conftest import CommentFactory


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

# Patch target: the signal module imports moderate_comment from services,
# so we patch it at the point the signal uses it.
_SIGNAL_PATCH = "comments.signals.moderate_comment"


def _mock_moderate_pending(*args, **kwargs):
    """Simulate Azure returning 'pending' (mid-severity text)."""
    return ("pending", None)


def _mock_moderate_approved(*args, **kwargs):
    """Simulate Azure approving the comment."""
    return ("approved", {"categories_analysis": []})


# ---------------------------------------------------------------------------
# CommentPageView — template/list view with POST
# ---------------------------------------------------------------------------

@pytest.mark.django_db
class TestCommentPageViewGet:
    """GET /comments/ renders the template with approved comments."""

    def test_get_returns_200(self, client):
        response = client.get(reverse("comments-page"))
        assert response.status_code == 200

    def test_get_uses_correct_template(self, client):
        response = client.get(reverse("comments-page"))
        assert "comments.html" in [t.name for t in response.templates]

    def test_get_only_shows_approved_comments(self, db, client):
        # Freeze the signal so factory-set statuses are not overridden by Azure
        with patch(_SIGNAL_PATCH, return_value=("approved", None)):
            approved = CommentFactory(comment_status="approved")
        with patch(_SIGNAL_PATCH, return_value=("pending", None)):
            CommentFactory(comment_status="pending")
        with patch(_SIGNAL_PATCH, return_value=("not_approved", None)):
            CommentFactory(comment_status="not_approved")

        response = client.get(reverse("comments-page"))

        comment_ids = [c.id for c in response.context["comments"]]
        assert approved.id in comment_ids
        assert len(comment_ids) == 1

    def test_get_sets_active_nav_context(self, db, client):
        response = client.get(reverse("comments-page"))
        assert response.context["active_nav"] == "comments"

    def test_get_empty_state_no_approved_comments(self, db, client):
        with patch(_SIGNAL_PATCH, return_value=("pending", None)):
            CommentFactory(comment_status="pending")
        response = client.get(reverse("comments-page"))
        assert response.status_code == 200
        assert list(response.context["comments"]) == []


@pytest.mark.django_db
class TestCommentPageViewPost:
    """POST /comments/ creates a comment (signal sets status) and redirects."""

    def test_post_valid_data_creates_comment(self, client):
        with patch(_SIGNAL_PATCH, side_effect=_mock_moderate_pending):
            data = {"nome": "Joao Silva", "comentario": "Excelente evento!"}
            client.post(reverse("comments-page"), data)

        assert Comment.objects.filter(comment_author="Joao Silva").exists()

    def test_post_valid_data_comment_starts_with_model_default_pending(self, client):
        """The view itself creates the Comment without specifying status.
        The model default is 'pending'; the signal then updates it.
        We verify the comment is created — the exact post-signal status is
        controlled by mocking the signal."""
        with patch(_SIGNAL_PATCH, side_effect=_mock_moderate_pending):
            data = {"nome": "Maria Costa", "comentario": "Muito bom!"}
            client.post(reverse("comments-page"), data)

        comment = Comment.objects.get(comment_author="Maria Costa")
        # After the signal mock returns 'pending', status is 'pending'
        assert comment.comment_status == "pending"

    def test_post_valid_data_signal_can_set_approved(self, client):
        """When Azure approves the comment the status becomes 'approved'."""
        with patch(_SIGNAL_PATCH, side_effect=_mock_moderate_approved):
            data = {"nome": "Luis Approved", "comentario": "Otimo!"}
            client.post(reverse("comments-page"), data)

        comment = Comment.objects.get(comment_author="Luis Approved")
        assert comment.comment_status == "approved"

    def test_post_valid_data_redirects(self, client):
        with patch(_SIGNAL_PATCH, side_effect=_mock_moderate_pending):
            data = {"nome": "Carlos Rocha", "comentario": "Parabens!"}
            response = client.post(reverse("comments-page"), data)

        assert response.status_code == 302
        assert response["Location"] == reverse("comments-page")

    def test_post_missing_nome_does_not_create_comment(self, client):
        initial_count = Comment.objects.count()
        data = {"comentario": "Sem nome"}
        client.post(reverse("comments-page"), data)

        assert Comment.objects.count() == initial_count

    def test_post_missing_comentario_does_not_create_comment(self, client):
        initial_count = Comment.objects.count()
        data = {"nome": "Anonimo"}
        client.post(reverse("comments-page"), data)

        assert Comment.objects.count() == initial_count

    def test_post_missing_both_fields_does_not_create_comment(self, client):
        initial_count = Comment.objects.count()
        client.post(reverse("comments-page"), {})

        assert Comment.objects.count() == initial_count

    def test_post_missing_fields_still_redirects(self, client):
        """View always redirects regardless of validation outcome."""
        response = client.post(reverse("comments-page"), {})
        assert response.status_code == 302

    def test_post_stores_correct_author_and_text(self, client):
        with patch(_SIGNAL_PATCH, side_effect=_mock_moderate_pending):
            data = {"nome": "Ana Ferreira", "comentario": "Evento incrivel!"}
            client.post(reverse("comments-page"), data)

        comment = Comment.objects.get(comment_author="Ana Ferreira")
        assert comment.comment_text == "Evento incrivel!"

    def test_post_pending_comment_does_not_appear_in_page_list(self, client):
        """Comments in 'pending' status must not appear in the GET list."""
        with patch(_SIGNAL_PATCH, side_effect=_mock_moderate_pending):
            data = {"nome": "Pedro Nunes", "comentario": "Espetacular!"}
            client.post(reverse("comments-page"), data)

        response = client.get(reverse("comments-page"))
        comment_ids = [c.id for c in response.context["comments"]]
        pending = Comment.objects.get(comment_author="Pedro Nunes")
        assert pending.id not in comment_ids


# ---------------------------------------------------------------------------
# CommentViewSet — DRF API (approved-only, list + create)
# ---------------------------------------------------------------------------

@pytest.mark.django_db
class TestCommentViewSetList:
    """GET /api/v1/comments/ returns only approved comments."""

    def test_list_returns_200(self, api_client):
        response = api_client.get("/api/v1/comments/")
        assert response.status_code == status.HTTP_200_OK

    def test_list_returns_only_approved_comments(self, api_client):
        with patch(_SIGNAL_PATCH, return_value=("approved", None)):
            approved = CommentFactory(comment_status="approved")
        with patch(_SIGNAL_PATCH, return_value=("pending", None)):
            CommentFactory(comment_status="pending")
        with patch(_SIGNAL_PATCH, return_value=("not_approved", None)):
            CommentFactory(comment_status="not_approved")

        response = api_client.get("/api/v1/comments/")

        ids = [item["id"] for item in response.data]
        assert approved.id in ids
        assert len(ids) == 1

    def test_list_empty_when_no_approved_comments(self, api_client):
        with patch(_SIGNAL_PATCH, return_value=("pending", None)):
            CommentFactory(comment_status="pending")
        response = api_client.get("/api/v1/comments/")
        assert response.data == []

    def test_list_response_contains_expected_fields(self, api_client):
        with patch(_SIGNAL_PATCH, return_value=("approved", None)):
            CommentFactory(comment_status="approved")
        response = api_client.get("/api/v1/comments/")

        assert len(response.data) == 1
        item = response.data[0]
        expected_fields = {"id", "comment_author", "comment_text", "created_at", "updated_at"}
        assert expected_fields.issubset(set(item.keys()))

    def test_list_does_not_expose_azure_safety_response(self, api_client):
        with patch(_SIGNAL_PATCH, return_value=("approved", None)):
            CommentFactory(comment_status="approved")
        response = api_client.get("/api/v1/comments/")

        item = response.data[0]
        assert "azure_safety_response" not in item

    def test_list_does_not_expose_comment_status(self, api_client):
        with patch(_SIGNAL_PATCH, return_value=("approved", None)):
            CommentFactory(comment_status="approved")
        response = api_client.get("/api/v1/comments/")

        item = response.data[0]
        assert "comment_status" not in item

    def test_list_ordered_by_most_recent_first(self, api_client):
        with patch(_SIGNAL_PATCH, return_value=("approved", None)):
            first = CommentFactory(comment_status="approved")
            second = CommentFactory(comment_status="approved")

        response = api_client.get("/api/v1/comments/")

        ids = [item["id"] for item in response.data]
        # Model Meta ordering = ['-created_at'] — most recently created is first
        assert ids[0] == second.id
        assert ids[1] == first.id

    def test_post_to_api_creates_comment_via_viewset(self, api_client):
        """CommentViewSet mixes in CreateModelMixin so POST is accepted."""
        with patch(_SIGNAL_PATCH, side_effect=_mock_moderate_pending):
            data = {"comment_author": "API User", "comment_text": "Via API"}
            response = api_client.post("/api/v1/comments/", data, format="json")

        assert response.status_code == status.HTTP_201_CREATED

    def test_post_to_api_comment_not_in_approved_list(self, api_client):
        """A freshly POSTed comment with 'pending' status won't appear in GET list."""
        with patch(_SIGNAL_PATCH, side_effect=_mock_moderate_pending):
            api_client.post(
                "/api/v1/comments/",
                {"comment_author": "Hidden", "comment_text": "Should not show"},
                format="json",
            )

        response = api_client.get("/api/v1/comments/")
        authors = [item["comment_author"] for item in response.data]
        assert "Hidden" not in authors

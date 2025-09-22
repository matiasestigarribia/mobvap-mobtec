from rest_framework.routers import SimpleRouter
from .views import CommentViewSet


router = SimpleRouter()
router.register(r'', CommentViewSet, basename='comments')

urlpatterns = router.urls

from rest_framework_nested import routers
from .views import EditionViewSet
from photos.views import PhotoViewSet
from videos.views import VideoViewSet


router = routers.SimpleRouter()
router.register(r'editions', EditionViewSet, basename='editions')

editions_router = routers.NestedSimpleRouter(router, r'editions', lookup='edition')
editions_router.register(r'photos', PhotoViewSet, basename='edition-photos')
editions_router.register(r'videos', VideoViewSet, basename='edition-videos')

urlpatterns = router.urls + editions_router.urls

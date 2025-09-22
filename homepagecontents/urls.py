from rest_framework.routers import SimpleRouter
from .views import HomePageContentViewSet


router = SimpleRouter()
router.register(r'home', HomePageContentViewSet, basename='home-api')

urlpatterns = router.urls

from rest_framework.routers import SimpleRouter
from .views import RulesPageContentViewSet

router = SimpleRouter()
router.register(r'rules', RulesPageContentViewSet, basename='rules')

urlpatterns = router.urls

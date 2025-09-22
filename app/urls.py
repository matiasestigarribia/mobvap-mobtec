from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from homepagecontents.views import HomePageView
from rulespagecontents.views import RulesPageView
from editions.views import EditionPageView
from comments.views import CommentPageView
from photos.views import PhotoListView
from videos.views import VideoListView

urlpatterns = [
    path("admin/", admin.site.urls),

    path('api/v1/', include('editions.urls')),
    path('api/v1/', include('homepagecontents.urls')),
    path('api/v1/', include('rulespagecontents.urls')),
    path('api/v1/comments/', include('comments.urls')),

    path('home/', HomePageView.as_view(), name='home-page'),
    path('rules/', RulesPageView.as_view(), name='rules-page'),
    path('comments/', CommentPageView.as_view(), name='comments-page'),
    path('editions/', EditionPageView.as_view(), name='editions-list'),
    path('editions/<str:edition_name>/photos/', PhotoListView.as_view(), name='photo-list-by-edition'),
    path('editions/<str:edition_name>/videos/', VideoListView.as_view(), name='video-list-by-edition'),
]

if settings.DEBUG and settings.STATICFILES_DIRS:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATICFILES_DIRS)

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

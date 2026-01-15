from rest_framework import viewsets
from django.views.generic import ListView
from .models import Video
from .serializers import VideoSerializer


class VideoViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = VideoSerializer

    def get_queryset(self):
        slug = self.kwargs.get('edition_edition_name')
        return Video.objects.filter(edition__slug=slug)


class VideoListView(ListView):
    model = Video
    template_name = 'videos.html'
    context_object_name = 'videos'
    paginate_by = 15

    def get_queryset(self):
        return Video.objects.filter(edition__slug=self.kwargs['edition_name'])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['edition_name'] = self.kwargs['edition_name']
        context['active_nav'] = 'editions'
        return context

from rest_framework import viewsets
from django.views.generic import ListView
from .models import Photo
from .serializers import PhotoSerializer


class PhotoViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Photo.objects.all()
    serializer_class = PhotoSerializer

    def get_queryset(self):
        edition_name_from_url = self.kwargs['edition_edition_name']
        return Photo.objects.filter(edition__edition_name=edition_name_from_url)


class PhotoListView(ListView):
    model = Photo
    template_name = 'photos.html'
    context_object_name = 'photos'
    paginate_by = 15

    def get_queryset(self):
        return Photo.objects.filter(edition__edition_name=self.kwargs['edition_name'])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['edition_name'] = self.kwargs['edition_name']
        context['active_nav'] = 'editions'
        return context

from rest_framework import viewsets
from django.views.generic import ListView
from .models import Edition
from .serializers import EditionSerializer


class EditionViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Edition.objects.all()
    serializer_class = EditionSerializer
    lookup_field = 'edition_name'


class EditionPageView(ListView):
    model = Edition
    template_name = 'editions.html'
    context_object_name = 'editions'
    paginate_by = 6
    active_nav = 'editions'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['active_nav'] = 'editions'

        return context

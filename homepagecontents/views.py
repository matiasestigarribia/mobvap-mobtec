from rest_framework import viewsets
from django.views.generic import TemplateView
from .models import HomePageContent
from .serializers import HomePageContentSerializer


class HomePageContentViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = HomePageContent.objects.all()
    serializer_class = HomePageContentSerializer


class HomePageView(TemplateView):
    template_name = 'home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['home_content'] = HomePageContent.objects.first()

        context['active_nav'] = 'home'

        return context

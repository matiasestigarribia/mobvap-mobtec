from rest_framework import viewsets
from django.views.generic import TemplateView
from .models import RulesPageContent
from .serializers import RulesPageContentSerializer


class RulesPageContentViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = RulesPageContent.objects.all()
    serializer_class = RulesPageContentSerializer


class RulesPageView(TemplateView):
    template_name = 'rules.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['rules_content'] = RulesPageContent.objects.first()
        context['active_nav'] = 'rules'

        return context

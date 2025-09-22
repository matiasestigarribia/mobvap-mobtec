from rest_framework import viewsets, mixins
from django.contrib import messages
from django.views.generic import ListView
from django.shortcuts import redirect
from .models import Comment
from .serializers import CommentSerializer


class CommentViewSet(mixins.ListModelMixin,
                     mixins.CreateModelMixin,
                     viewsets.GenericViewSet):

    serializer_class = CommentSerializer

    def get_queryset(self):
        return Comment.objects.filter(comment_status='approved').order_by('-created_at')


class CommentPageView(ListView):
    model = Comment
    template_name = 'comments.html'
    context_object_name = 'comments'
    paginate_by = 20

    def get_queryset(self):
        return Comment.objects.filter(comment_status='approved')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['active_nav'] = 'comments'

        return context

    def post(self, request, *args, **kwargs):

        author_name = request.POST.get('nome')
        comment_text = request.POST.get('comentario')

        if author_name and comment_text:
            Comment.objects.create(
                comment_author=author_name,
                comment_text=comment_text
            )
            messages.success(request, 'Obrigado pelo seu comentário! Ele está aguardando aprovação.')

        return redirect('comments-page')

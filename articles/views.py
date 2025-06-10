from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.exceptions import PermissionDenied
from rest_framework.filters import SearchFilter
from django_filters.rest_framework import DjangoFilterBackend
from django.utils.translation import gettext as _
from .models import Article, Approval
from .serializers import ArticleSerializer, ApprovalSerializer
from django.contrib.auth import get_user_model

User = get_user_model()

from docx import Document
import os

class ArticleViewSet(viewsets.ModelViewSet):
    def perform_create(self, serializer):
        article = serializer.save(author=self.request.user)
        monitors = User.objects.filter(is_monitor=True)
        for monitor in monitors:
            Approval.objects.create(article=article, monitor=monitor)
        
        # Generate .docx file
        doc = Document()
        doc.add_heading(article.title, 0)
        doc.add_paragraph(article.content)
        doc_path = os.path.join('articles', f'{article.id}_{article.title}.docx')
        os.makedirs('articles', exist_ok=True)
        doc.save(doc_path)
        
        return Response({"message": _("Article created"), "doc_path": doc_path}, status=status.HTTP_201_CREATED)

class ArticleViewSet(viewsets.ModelViewSet):
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_fields = ['author', 'created_at']
    search_fields = ['title', 'content']

    def perform_create(self, serializer):
        article = serializer.save(author=self.request.user)
        monitors = User.objects.filter(is_monitor=True)
        for monitor in monitors:
            Approval.objects.create(article=article, monitor=monitor)
        return Response({"message": _("Article created")}, status=status.HTTP_201_CREATED)

    def perform_update(self, serializer):
        if self.request.user == self.get_object().author:
            serializer.save()
        else:
            raise PermissionDenied(_("You can only edit your own articles"))

    def perform_destroy(self, instance):
        if self.request.user == instance.author:
            instance.delete()
        else:
            raise PermissionDenied(_("You can only delete your own articles"))

class ApprovalViewSet(viewsets.ModelViewSet):
    queryset = Approval.objects.all()
    serializer_class = ApprovalSerializer
    permission_classes = [IsAuthenticated]

    def perform_update(self, serializer):
        if self.request.user.is_monitor:
            serializer.save()
        else:
            raise PermissionDenied(_("Only monitors can approve articles"))
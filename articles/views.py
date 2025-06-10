from rest_framework import generics, permissions
from .models import Article
from .serializers import ArticleSerializer, ArticleModerationSerializer
from rest_framework.filters import SearchFilter
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.permissions import IsAuthenticated

class IsAuthorOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.author == request.user

class IsModeratorOrAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role in ['moderator', 'admin']

class ArticleListCreateView(generics.ListCreateAPIView):
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_fields = ['status', 'author']
    search_fields = ['title_uz', 'title_en', 'content_uz', 'content_en']

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

class ArticleDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer
    permission_classes = [IsAuthenticated, IsAuthorOrReadOnly]

class ArticleModerationView(generics.UpdateAPIView):
    queryset = Article.objects.all()
    serializer_class = ArticleModerationSerializer
    permission_classes = [IsAuthenticated, IsModeratorOrAdmin]

    def perform_update(self, serializer):
        serializer.save(moderator=self.request.user)
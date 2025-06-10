from django.urls import path
from .views import ArticleListCreateView, ArticleDetailView, ArticleModerationView

urlpatterns = [
    path('', ArticleListCreateView.as_view(), name='article_list_create'),
    path('<int:pk>/', ArticleDetailView.as_view(), name='article_detail'),
    path('<int:pk>/moderate/', ArticleModerationView.as_view(), name='article_moderate'),
]
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ArticleViewSet, ApprovalViewSet

router = DefaultRouter()
router.register(r'articles', ArticleViewSet)
router.register(r'approvals', ApprovalViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
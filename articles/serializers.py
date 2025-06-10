from rest_framework import serializers
from .models import Article, Approval
from accounts.serializers import UserSerializer

class ArticleSerializer(serializers.ModelSerializer):
    author = UserSerializer(read_only=True)
    class Meta:
        model = Article
        fields = ['id', 'title', 'content', 'author', 'status', 'created_at']
        read_only_fields = ['author', 'status', 'created_at']

class ApprovalSerializer(serializers.ModelSerializer):
    article = ArticleSerializer(read_only=True)
    monitor = UserSerializer(read_only=True)
    class Meta:
        model = Approval
        fields = ['id', 'article', 'monitor', 'status', 'created_at']
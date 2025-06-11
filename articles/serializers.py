from rest_framework import serializers
from .models import Article, Approval
from accounts.serializers import UserSerializer
from rest_framework import serializers
from .models import FAQ
from rest_framework import serializers
from .models import Article

class ArticleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Article
        fields = ['id', 'title', 'content', 'author', 'status', 'created_at', 'view_count']
        read_only_fields = ['author', 'status', 'created_at', 'view_count']


class ArticleSerializer(serializers.ModelSerializer):
    author = UserSerializer(read_only=True)
    class Meta:
        model = Article
        fields = ['id', 'title', 'content', 'author', 'status', 'created_at','view_count']
        read_only_fields = ['author', 'status', 'created_at', 'view_count']

class ApprovalSerializer(serializers.ModelSerializer):
    article = ArticleSerializer(read_only=True)
    monitor = UserSerializer(read_only=True)
    class Meta:
        model = Approval
        fields = ['id', 'article', 'monitor', 'status', 'created_at']
        
        

class ArticleUploadSerializer(serializers.Serializer):
    file = serializers.FileField()


class FAQSerializer(serializers.ModelSerializer):
    class Meta:
        model = FAQ
        fields = ['id', 'question', 'answer']
        read_only_fields = ['id']
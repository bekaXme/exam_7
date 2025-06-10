from rest_framework import serializers
from .models import Article
from django.utils import translation

class ArticleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Article
        fields = ['id', 'title_uz', 'title_en', 'content_uz', 'content_en', 'author', 'status', 'created_at', 'updated_at', 'moderator']
        read_only_fields = ['id', 'author', 'status', 'created_at', 'updated_at', 'moderator']

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        lang = translation.get_language()
        if lang == 'en':
            representation['title'] = representation.pop('title_en')
            representation['content'] = representation.pop('content_en')
            representation.pop('title_uz')
            representation.pop('content_uz')
        else:
            representation['title'] = representation.pop('title_uz')
            representation['content'] = representation.pop('content_uz')
            representation.pop('title_en')
            representation.pop('content_en')
        return representation

class ArticleModerationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Article
        fields = ['status', 'moderator']
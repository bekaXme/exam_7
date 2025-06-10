from django.contrib import admin
from .models import Article

@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ['title_uz', 'author', 'status', 'created_at', 'moderator']
    list_filter = ['status', 'author', 'moderator']
    search_fields = ['title_uz', 'title_en', 'content_uz', 'content_en']
from django.db import models
from accounts.models import User

class Article(models.Model):
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('declined', 'Declined'),
    )
    
    title_uz = models.CharField(max_length=255)
    title_en = models.CharField(max_length=255)
    content_uz = models.TextField()
    content_en = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='articles')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    moderator = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='moderated_articles')

    def __str__(self):
        return self.title_uz
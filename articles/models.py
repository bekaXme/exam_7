from django.db import models
from django.utils.translation import gettext_lazy as _
from django.conf import settings

class Article(models.Model):
    STATUS = (
        ('P', 'Pending'),
        ('A', 'Approved'),
        ('R', 'Rejected'),
    )
    title = models.CharField(max_length=255)
    content = models.TextField()
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='articles'
    )
    status = models.CharField(max_length=1, choices=STATUS, default='P')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

class Approval(models.Model):
    STATUS = (
        ('P', 'Pending'),
        ('A', 'Approved'),
        ('R', 'Rejected'),
    )
    article = models.ForeignKey(Article, on_delete=models.CASCADE, related_name='approvals')
    monitor = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='monitor_approvals'
    )
    status = models.CharField(max_length=1, choices=STATUS, default='P')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.article.title} - {self.monitor.username}"
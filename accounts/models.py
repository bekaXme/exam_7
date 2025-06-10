from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _

class User(AbstractUser):
    ROLE = (
        ('', _('')),
        ('user', _('User')),
        ('monitor', 'Monitor'),
        ('admin', 'Admin'),
    )
    role = models.CharField(max_length=100, choices=ROLE, blank=True, null=True)
    is_monitor = models.BooleanField(default=False)

    def __str__(self):
        return self.username
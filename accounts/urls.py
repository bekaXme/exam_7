from django.urls import path
from .views import (
    RegisterView, LoginView, PasswordChangeView, PasswordResetView,
    PasswordResetConfirmView, PasswordChangeConfirmView, ProfileView
)

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('password/change/', PasswordChangeView.as_view(), name='password_change'),
    path('password/change/confirm/', PasswordChangeConfirmView.as_view(), name='password_change_confirm'),
    path('password/reset/', PasswordResetView.as_view(), name='password_reset'),
    path('password/reset/confirm/', PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('profile/', ProfileView.as_view(), name='profile'),
]
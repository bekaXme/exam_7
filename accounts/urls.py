from django.urls import path
from .views import RegisterView, LoginView, ProfileView, PasswordChangeView, PasswordResetView, SetMonitorView, PasswordResetConfirmView

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('profile/', ProfileView.as_view(), name='profile'),
    path('password/change/', PasswordChangeView.as_view(), name='password_change'),
    path('password/reset/', PasswordResetView.as_view(), name='password_reset'),
    path('set-monitor/<int:user_id>/', SetMonitorView.as_view(), name='set-monitor'),
    path('password/reset/confirm/<uidb64>/<token>/', PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
]
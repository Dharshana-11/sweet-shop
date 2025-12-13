from django.urls import path
from .views import health_check, register_user

urlpatterns = [
    path('health/', health_check),
    path('auth/register', register_user, name='register')
]

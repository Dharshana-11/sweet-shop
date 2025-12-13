from django.urls import path
from .views import sweets_list

urlpatterns = [
    path('', sweets_list, name="sweets-list"),
]

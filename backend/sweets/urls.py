from django.urls import path
from .views import sweets_list, sweets_search

urlpatterns = [
    path('', sweets_list, name="sweets-list"),
    path('search/', sweets_search, name="sweets-search"),
]

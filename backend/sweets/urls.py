from django.urls import path
from .views import sweets_list, sweets_search, update_sweet

urlpatterns = [
    path('', sweets_list, name="sweets-list"),
    path('search/', sweets_search, name="sweets-search"),
    path('<int:id>/', update_sweet, name="sweets-update"),
]

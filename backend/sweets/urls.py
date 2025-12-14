from django.urls import path
from .views import sweets_list, sweets_search, update_sweet, delete_sweet, purchase_sweet, restock_sweet

urlpatterns = [
    path('', sweets_list, name="sweets-list"),
    path('search/', sweets_search, name="sweets-search"),
    path('<int:id>/', update_sweet, name="sweets-update"),
    path('<int:id>/delete/', delete_sweet, name="sweets-delete"),
    path('<int:id>/purchase/', purchase_sweet, name="sweets-purchase"),
    path('<int:id>/restock/', restock_sweet, name="sweets-restock"),
]

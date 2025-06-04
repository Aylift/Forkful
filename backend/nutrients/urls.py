from django.urls import path
from .views import IngredientListView, IngredientDetailView


urlpatterns = [
    path('ingredients/', IngredientListView.as_view(), name='ingredient_list'),
    path('ingredients/<int:pk>/', IngredientDetailView.as_view(), name='ingredient_detail')
]
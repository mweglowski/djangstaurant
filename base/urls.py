from django.urls import path
from . import views

urlpatterns = [
	path("", views.HomeView.as_view(), name="home"),
	path("menu/", views.menu, name="menu"),
	path("inventory/", views.inventory, name="inventory"),
	path("ingredient/add", views.IngredientAddView.as_view(), name="ingredientadd")
]
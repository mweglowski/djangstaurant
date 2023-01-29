from django.urls import path
from . import views

urlpatterns = [
	path("", views.HomeView.as_view(), name="home"),
	path("menu/", views.menu, name="menu"),
	path("inventory/", views.inventory, name="inventory"),
	path("ingredient/add", views.IngredientAddView.as_view(), name="ingredientadd"),
	path("new-purchase/", views.new_purchase, name="newpurchase"),
	path("new-purchase/<menu_item_id>", views.new_purchase, name="newpurchase")
]
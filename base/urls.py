from django.urls import path
from . import views

urlpatterns = [
	path("", views.HomeView.as_view(), name="home"),
	path("menu/", views.menu, name="menu"),
	path("menu/new-item", views.new_menu_item, name="newmenuitem"),
	path("menu/new-item/add-ingredient", views.new_menu_item_add_ingredient, name="new_menu_item_add_ingredient"),
	path("inventory/", views.inventory, name="inventory"),
	path("inventory/ingredient/add", views.ingredient_add_view, name="ingredientadd"),
	path("inventory/ingredient/delete", views.ingredient_delete_view, name="ingredientdelete"),
	path("inventory/ingredient/delete/<id>", views.ingredient_delete_confirm_view, name="ingredient_delete_confirm"),
	path("purchases/", views.purchases_view, name="purchases"),
	path("new-purchase/", views.new_purchase, name="newpurchase"),
	path("new-purchase/<menu_item_id>", views.new_purchase, name="newpurchase")
]
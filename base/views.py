from django.shortcuts import render, redirect
from django.views.generic import TemplateView, CreateView
from .forms import IngredientAddForm, NewPurchaseForm
from .models import Ingredient, MenuItem, MenuItemRequirement

# /home
class HomeView(TemplateView):
	template_name = "home.html"

# /menu
def menu(request):
	menu_items = MenuItem.objects.all()
	context = {}
	context["menu_items"] = menu_items
	# context["menu_items"] = []
	# for item in menu_items:
	# 	context["menu_items"].append({
	# 		"id": item.id,
	# 		"name": item.name,
	# 		"price": item.price
	# 	})

	return render(request, "menu/menu.html", context)


# /inventory
def inventory(request):
	ingredients = Ingredient.objects.all()

	# TRANSFORMING FROM FLOAT TO INT
	transformed_ings = []
	for ing in ingredients:
		next_ing = {
			"name": ing.name,
			"unit": ing.unit
		}
		if ing.amount > int(ing.amount):
			next_ing["amount"] = ing.amount
		else:
			next_ing["amount"] = int(ing.amount)
			
		transformed_ings.append(next_ing)
	print(transformed_ings)

	context = {}
	context["ingredients"] = transformed_ings
	return render(request, "inventory.html", context)


# /ingredient/add
class IngredientAddView(CreateView):
	model = Ingredient
	form_class = IngredientAddForm 
	template_name = "add_ingredient/add_ingredient.html"


# /new-purchase
def new_purchase(request, menu_item_id):
	menu_item_id = int(menu_item_id)
	item = MenuItem.objects.all()[menu_item_id - 1]
	context = {}
	context["item"] = item

	if request.method == "POST":
		form = NewPurchaseForm(request.POST)
		print("PURCHASED MENU ITEM ID -->", form["id"].value())

		# SUBTRACTING AMOUNTS OF SPECIFIC INGREDIENTS
		menu_item_id = int(form["id"].value())

		required_ingredient_amount = MenuItemRequirement.objects.get(menu_item_id=menu_item_id).ingredient_amount

		ingredient_name = MenuItemRequirement.objects.get(menu_item_id=menu_item_id).ingredient_id
		
		ingredient_in_storage = Ingredient.objects.get(name=ingredient_name)

		print(ingredient_in_storage.amount)

		ingredient_in_storage.amount -= required_ingredient_amount

		print(ingredient_in_storage.amount)
		
		ingredient_in_storage.save()

		return redirect('menu')

	

	return render(request, "purchases/new_purchase.html", context)

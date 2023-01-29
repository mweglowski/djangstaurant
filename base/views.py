from django.shortcuts import render, redirect
from django.views.generic import TemplateView
from .forms import IngredientAddForm, NewPurchaseForm, MenuItemAddForm
from .models import Ingredient, MenuItem, MenuItemRequirement, Purchase

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

# /menu/new-item
def new_menu_item(request):
	if request.method == "POST":
		form = MenuItemAddForm(request.POST)

		name = form["name"].value()
		price = float(form["price"].value())
		food_type = form["food_type"].value()
		menu_item = MenuItem(name=name, price=price, food_type=food_type)
		menu_item.save()
		
		return redirect(f"/menu/new-item/add-ingredient", {"item_id": menu_item.id})

	return render(request, "menu/new_menu_item.html")


# /menu/new-item/add-ingredient
def new_menu_item_add_ingredient(request):
	# CHECKING REQUEST METHOD AS USUAL
	

	return render(request, "menu/new_menu_item_add_ingredient.html")


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
# class IngredientAddView(CreateView):
# 	model = Ingredient
# 	form_class = IngredientAddForm 
# 	template_name = "add_ingredient/add_ingredient.html"

# /ingredient/add
def ingredient_add_view(request):
	if request.method == "POST":
		form = IngredientAddForm(request.POST)
		name = form["name"].value()
		unit = form["unit"].value()
		amount = form["amount"].value()
		new_ingredient = Ingredient(name=name, unit=unit, amount=amount)
		new_ingredient.save()

		return redirect('inventory')

	return render(request, "add_ingredient/add_ingredient.html")

# /purchases
def purchases_view(request):
	purchases = Purchase.objects.all()
	purchases_transformed = []
	for purchase in purchases:
		# GET MENU ITEM 
		menu_item = purchase.menu_item_id
		# GET MENU ITEM NAME
		menu_item_name = menu_item.name
		# GET PRICE OF MENU ITEM
		menu_item_price = menu_item.price
		# GET DATE OF PURCHASE
		menu_item_purchase_date = purchase.date

		# APPEND NEW PURCHASE OBJECT TO TRANSFORMED PURCHASES
		purchases_transformed.append({
			"item_name": menu_item_name,
			"price": menu_item_price,
			"date": menu_item_purchase_date
		})

	return render(request, "purchases/purchases.html", {"purchases": purchases_transformed})


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

		# CREATING NEW PURCHASE
		another_purchase = Purchase(menu_item_id=item)
		another_purchase.save()
		print(another_purchase)

		return redirect('menu')

	return render(request, "purchases/new_purchase.html", context)

from django.shortcuts import render, redirect
from django.contrib import messages
from django.views.generic import TemplateView
from .forms import IngredientAddForm, NewPurchaseForm, MenuItemAddForm, MenuItemRequirementAddForm
from .models import Ingredient, MenuItem, MenuItemRequirement, Purchase

from .helper_functions import get_menu_item_ingredient_list

# /home
class HomeView(TemplateView):
	template_name = "home.html"

# /menu
def menu(request):
	menu_items = MenuItem.objects.all()
	context = {}
	# context["menu_items"] = menu_items
	context["menu_items"] = []
	for item in menu_items:
		# GET REQUIRED INGREDIENTS
		ingredient_list_string = get_menu_item_ingredient_list(item)

		context["menu_items"].append({
			"id": item.id,
			"name": item.name,
			"price": item.price,
			"ingredient_list": ingredient_list_string,
		})

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
		
		# STORE MENU ITEM NAME IN SESSION
		request.session['new-menu-item-name'] = name
		request.session['new-menu-item-price'] = price

		return redirect(f"/menu/new-item/add-ingredient")

	return render(request, "menu/new_menu_item.html")


# /menu/new-item/add-ingredient
def new_menu_item_add_ingredient(request):
	# GET NEW MENU ITEM NAME AND PRICE FROM SESSION STORAGE
	new_menu_item_name = request.session['new-menu-item-name']
	new_menu_item_price = request.session['new-menu-item-price']

	context = {}
	context["name"] = new_menu_item_name
	context["price"] = new_menu_item_price

	if request.method == "POST":
		form = request.POST

		# GET INGREDIENT NAME
		ing_name = form.get("name")

		# GET INGREDIENT UNIT
		ing_unit = form.get("unit")

		# GET REQUIRED INGREDIENT AMOUNT
		ing_amount = form.get("amount")

		# GET MENU ITEM
		menu_item = MenuItem.objects.filter(name=new_menu_item_name).first()

		# GET INGREDIENT AND IF INGREDIENT DOES NOT EXIST CREATE ONE WITH AMOUNT OF 0
		if not Ingredient.objects.filter(name=ing_name).exists():
			# CREATE
			Ingredient.objects.create(name=ing_name, unit=ing_unit)
			ingredient = Ingredient.objects.filter(name=ing_name).first()
			ingredient.save()

			new_requirement = MenuItemRequirement(menu_item_id=menu_item, ingredient_id=ingredient, ingredient_amount=ing_amount)
			new_requirement.save()
		else:
			# GET INGREDIENT
			ingredient = Ingredient.objects.get(name=ing_name)

			new_requirement = MenuItemRequirement(menu_item_id=menu_item, ingredient_id=ingredient, ingredient_amount=ing_amount)
			new_requirement.save()

	return render(request, "menu/new_menu_item_add_ingredient.html", context)

# /menu/item/delete
def menu_item_delete(request):
	menu_items = MenuItem.objects.all()
	context = {}
	# context["menu_items"] = menu_items
	context["menu_items"] = []
	for item in menu_items:
		# GET REQUIRED INGREDIENTS
		item_requirements = MenuItemRequirement.objects.filter(menu_item_id=item)

		ingredient_list_string = ""
		if len(item_requirements) != 0:
			for req in item_requirements:
				if not req.ingredient_id:
					break

				ingredient = req.ingredient_id.name
				ingredient_list_string += ingredient + ', '

		ingredient_list_string = ingredient_list_string[:-2]

		context["menu_items"].append({
			"id": item.id,
			"name": item.name,
			"price": item.price,
			"ingredient_list": ingredient_list_string,
		})

	return render(request, "menu/menu_item_delete.html", context)

# /menu/item/delete/<id>
def menu_item_delete_confirm(request, id):
	if request.method == "POST":
		# GET MENU ITEM VIA id
		menu_item = MenuItem.objects.get(id=id)

		# DELETE MENU ITEM REQUIREMENTS
		requirements = MenuItemRequirement.objects.filter(menu_item_id=menu_item)
		for req in requirements:
			req.delete()

		# DELETE MENU ITEM
		menu_item.delete()

		return redirect("/menu")

	return render(request, "menu/menu_item_delete_confirm.html")


# /inventory
def inventory(request):
	ingredients = Ingredient.objects.all()

	# TRANSFORMING FROM FLOAT TO INT
	transformed_ings = []
	for ing in ingredients:
		if ing.amount == 0:
			continue
		
		next_ing = {
			"name": ing.name,
			"unit": ing.unit
		}
		if ing.amount > int(ing.amount):
			next_ing["amount"] = ing.amount
		else:
			next_ing["amount"] = int(ing.amount)
			
		transformed_ings.append(next_ing)

	context = {}
	context["ingredients"] = transformed_ings
	return render(request, "inventory/inventory.html", context)


# /ingredient/add
# class IngredientAddView(CreateView):
# 	model = Ingredient
# 	form_class = IngredientAddForm 
# 	template_name = "add_ingredient/add_ingredient.html"

# /inventory/ingredient/add
def ingredient_add_view(request):
	if request.method == "POST":
		form = IngredientAddForm(request.POST)
		name = form["name"].value()
		unit = form["unit"].value()
		amount = float(form["amount"].value())

		if Ingredient.objects.filter(name=name):
			ing_in_storage = Ingredient.objects.get(name=name)
			ing_in_storage.amount += amount
			ing_in_storage.save()
		else:
			new_ingredient = Ingredient(name=name, unit=unit, amount=amount)
			new_ingredient.save()

		return redirect('inventory')

	return render(request, "add_ingredient/add_ingredient.html")

# /inventory/ingredient/update
def ingredient_update_view(request):
	ingredients = Ingredient.objects.all()

	# TRANSFORMING FROM FLOAT TO INT
	transformed_ings = []
	for ing in ingredients:
		next_ing = {
			"id": ing.id,
			"name": ing.name,
			"unit": ing.unit
		}
		if ing.amount > int(ing.amount):
			next_ing["amount"] = ing.amount
		else:
			next_ing["amount"] = int(ing.amount)
			
		transformed_ings.append(next_ing)

	context = {}
	context["ingredients"] = transformed_ings

	return render(request, "update_ingredient/update_ingredient.html", context)

# /inventory/ingredient/update/<id>
def ingredient_update_form_view(request, id):
	ing = Ingredient.objects.get(id=id)
	context = {}
	context["name"] = ing.name
	context["unit"] = ing.unit
	context["amount"] = ing.amount
	
	if request.method == "POST":
		# GET DATA FROM FORM AND UPDATE INGREDIENT
		form = request.POST
		messages.info(request, 'updating')

		ing.name = form.get("name")
		ing.unit = form.get("unit")
		ing.amount = float(form.get("amount"))
		ing.save()

		return redirect("/inventory/")

	return render(request, "update_ingredient/update_ingredient_form.html", context)


# /inventory/ingredient/delete
def ingredient_delete_view(request):
	ingredients = Ingredient.objects.all()

	# TRANSFORMING FROM FLOAT TO INT
	transformed_ings = []
	for ing in ingredients:
		if ing.amount == 0:
			continue

		next_ing = {
			"id": ing.id,
			"name": ing.name,
			"unit": ing.unit
		}
		if ing.amount > int(ing.amount):
			next_ing["amount"] = ing.amount
		else:
			next_ing["amount"] = int(ing.amount)
			
		transformed_ings.append(next_ing)

	context = {}
	context["ingredients"] = transformed_ings

	return render(request, "delete_ingredient/delete_ingredient.html", context)

# /inventory/ingredient/delete/<id>
def ingredient_delete_confirm_view(request, id):
	if request.method == "POST":
		# DELETE INGREDIENT (SET AMOUNT TO 0)
		ing_to_delete = Ingredient.objects.get(id=id)
		ing_to_delete.amount = 0.0
		ing_to_delete.save()

		return redirect("/inventory/")

	return render(request, "delete_ingredient/delete_ingredient_confirm.html")

# /purchases
def purchases_view(request):
	purchases = Purchase.objects.all()
	purchases_transformed = []

	for purchase in purchases:

		# LOADING PURCHASE ONLY IF ITEM IS IN THE MENU AND HAS NOT BEEN DELETED
		if purchase.menu_item_id:
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
	# GET MENU ITEM INGREDIENT LIST
	ingredient_list_string = get_menu_item_ingredient_list(item)
	
	# SAVE IT TO CONTEXT
	context["ingredient_list"] = ingredient_list_string

	if request.method == "POST":
		form = NewPurchaseForm(request.POST)

		# SUBTRACTING AMOUNTS OF SPECIFIC INGREDIENTS
		menu_item_id = int(form["id"].value())

		requirements = MenuItemRequirement.objects.filter(menu_item_id=menu_item_id)
		# FOR EVERY REQUIREMENT DECREASE THE AMOUNT OF SPECIFIC INGREDIENT
		for req in requirements:
			required_ingredient_amount = req.ingredient_amount

			ingredient_name = req.ingredient_id.name
			print(ingredient_name)

			ingredient_in_storage = Ingredient.objects.filter(name=ingredient_name)[0]
			print(ingredient_in_storage)

			ingredient_in_storage.amount -= required_ingredient_amount
			
			ingredient_in_storage.save()

		# CREATING NEW PURCHASE
		another_purchase = Purchase(menu_item_id=item)
		another_purchase.save()

		return redirect('menu')

	return render(request, "purchases/new_purchase.html", context)

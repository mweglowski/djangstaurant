from django.shortcuts import render
from django.views.generic import TemplateView, CreateView
from .forms import IngredientCreateForm
from .models import Ingredient

# /home
class HomeView(TemplateView):
	template_name = "home.html"

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


class IngredientCreateView(CreateView):
	model = Ingredient
	form_class = IngredientCreateForm 
	template_name = "ingredient_create_form.html"

	
from django import forms
from .models import Ingredient, Purchase, MenuItem

class IngredientAddForm(forms.ModelForm):
	class Meta:
		model = Ingredient
		fields = "__all__"

class MenuItemAddForm(forms.ModelForm):
	class Meta:
		model = MenuItem
		fields = "__all__"

# TUTAJ NIE TRZEBA WALIDACJI CZY WYSTARCZY SKLADNIKOW BO WCZESNIEJ ITEMY KTORE NIE BEDA MIALY SKLADNIKOW NIE BEDA MOZLIWE DO KUPIENIA, PRZYCISK BEDZIE ZABLOKOWANY W MENU
class NewPurchaseForm(forms.ModelForm):
	# ODEJMOWANIE AMOUNT SKLADNIKOW OD MODELI

	class Meta:
		model = Purchase
		fields = "__all__"
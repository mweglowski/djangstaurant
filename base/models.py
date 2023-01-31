from django.db import models
import datetime

class Ingredient(models.Model):
	id = models.IntegerField(primary_key=True)
	name = models.CharField(max_length=100)
	unit = models.CharField(max_length=10)
	amount = models.FloatField(default=0.00)

	def get_absolute_url(self):
		return "/inventory"

	def __str__(self):
		return f"{self.name}"


class MenuItem(models.Model):
	id = models.IntegerField(primary_key=True)
	name = models.CharField(max_length=100)
	price = models.FloatField(default=0.0)
	food_type = models.CharField(max_length=50, default="cocktail")

	def __str__(self):
		return f"{self.name}"


class MenuItemRequirement(models.Model):
	id = models.IntegerField(primary_key=True)
	menu_item_id = models.ForeignKey(MenuItem, on_delete=models.SET_NULL, null=True)
	ingredient_id = models.ForeignKey(Ingredient, on_delete=models.SET_NULL, null=True)
	ingredient_amount = models.FloatField(default=0.00)

	def __str__(self):
		return f"{self.menu_item_id} - {self.ingredient_id}"


class Purchase(models.Model):
	id = models.IntegerField(primary_key=True)
	menu_item_id = models.ForeignKey(MenuItem, on_delete=models.SET_NULL, null=True)
	date = models.DateField(default=datetime.date.today())

	def __str__(self):
		return f"{self.date}: {self.menu_item_id}"

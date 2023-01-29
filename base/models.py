from django.db import models


class Ingredient(models.Model):
	id = models.IntegerField(primary_key=True)
	name = models.CharField(max_length=100)
	unit = models.CharField(max_length=10)
	amount = models.FloatField(default=0.0)

	def get_absolute_url(self):
		return "/inventory"

	def __str__(self):
		return f"{self.name}"


class MenuItem(models.Model):
	id = models.IntegerField(primary_key=True)
	name = models.CharField(max_length=100)
	price = models.FloatField(default=0.0)
	food_type = models.CharField(max_length=50, default="cocktail")

	def get_absolute_url(self):
		return "/menu"

	def __str__(self):
		return f"{self.name}"


class MenuItemRequirement(models.Model):
	id = models.IntegerField(primary_key=True)
	menu_item_id = models.ForeignKey(MenuItem, on_delete=models.CASCADE)
	ingredient_id = models.ForeignKey(Ingredient, on_delete=models.CASCADE)
	ingredient_amount = models.FloatField(default=0.0)

	def get_absolute_url(self):
		return "/menu"

	def __str__(self):
		return f"MenuItemRequirement: {self.id}"


class Purchase(models.Model):
	id = models.IntegerField(primary_key=True)
	menu_item_id = models.ForeignKey(MenuItem, on_delete=models.CASCADE)
	date = models.DateField()

	def __str__(self):
		return f"Purchase: {self.date}"

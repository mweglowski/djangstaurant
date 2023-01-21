from django.db import models

# Create your models here.
class Ingredient(models.Model):
	name = models.CharField(max_length=100)
	unit = models.CharField(max_length=10)
	amount = models.FloatField(default=0.0)

	def get_absolute_url(self):
		return "/inventory"

	def __str__(self):
		return f"{self.name}"

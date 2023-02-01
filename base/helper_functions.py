from .models import MenuItemRequirement

def get_menu_item_ingredient_list(item):
	item_requirements = MenuItemRequirement.objects.filter(menu_item_id=item)

	ingredient_list_string = ""
	if len(item_requirements) != 0:
		for req in item_requirements:
			if not req.ingredient_id:
				break

			ingredient = req.ingredient_id.name
			ingredient_list_string += ingredient + ', '

	ingredient_list_string = ingredient_list_string[:-2]
	return ingredient_list_string
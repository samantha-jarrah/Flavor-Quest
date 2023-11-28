import json

def create_json_str(recipe_type, cuisine_types, diet_types, intolerances, include_ingredients, exclude_ingredients):
    """Create json_str from recipe parameters"""

    json_data = {}
    if recipe_type:
        json_data["query"] = recipe_type
    if cuisine_types:
        json_data["cuisine"] = cuisine_types
    if diet_types:
        json_data["diet"] = diet_types
    if intolerances:
        json_data["intolerances"] = intolerances
    if include_ingredients:
        json_data["includeIngredients"] = include_ingredients
    if exclude_ingredients:
        json_data["excludeIngredients"] = exclude_ingredients
    json_data["instructionsRequired"] = "true"
    json_data["fillIngredients"] = "true"
    json_data["addRecipeInformation"] = "true"
    return json.dumps(json_data)
    
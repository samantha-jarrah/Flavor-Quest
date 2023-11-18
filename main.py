import click
import re
import requests

# clears the terminal
click.clear()

@click.command()
def start():
    # Greet User
    greeting()

    # Gather recipe type
    recipe_type = get_recipe_type()

    # Gather cuisine types
    while True:
        cuisine_types = get_cuisine_types()

        if cuisine_types is False:
            click.echo("Going back to re-enter recipe type.")
            recipe_type = get_recipe_type()
        else:
            break

    # Gather diet types
    while True:
        diet_types = get_diet_types()

        if diet_types is False:
            click.echo("Going back to re-enter cuisine types.")
            cuisine_types = get_cuisine_types()
        else:
            break

    # Gather food intolerances
    while True:
        intolerances = get_intolerances()

        if intolerances is False:
            click.echo("Going back to re-enter diet types.")
            diet_types = get_diet_types()
        else:
            break

    # Gather ingredients to include
    while True:
        include_ingredients = get_include_ingredients()

        if include_ingredients is False:
            click.echo("Going back to re-enter food intolerances.")
            intolerances = get_intolerances()
        else:
            break

    # Gather ingredients to exclude
    while True:
        exclude_ingredients = get_exclude_ingredients()

        if exclude_ingredients is False:
            click.echo("Going back to re-enter ingredients to include.")
            include_ingredients = get_include_ingredients()
        else:
            break
    
    # Gather meal types
    while True:
        meal_types = get_meal_types()

        if meal_types is False:
            click.echo("Going back to re-enter ingredients to exclude.")
            exclude_ingredients = get_exclude_ingredients()
        else:
            break

    # create JSON_str to send to microservice
    json_str = '{'
    if recipe_type:
        json_str = json_str + f'"query" : "{recipe_type}", '

    if cuisine_types:
        json_str = json_str + '"cuisine": "'
        for cuisine in cuisine_types:
            json_str = json_str + f'{cuisine}, '
        json_str = json_str + '", '
    
    if diet_types:
        json_str = json_str + '"diet": "'
        for diet in diet_types:
            json_str = json_str + f'{diet}, '
        json_str = json_str + '", '

    if intolerances:
        json_str = json_str + '"intolerances": "'
        for intolerance in intolerances:
            json_str = json_str + f'{intolerance}, '
        json_str = json_str + '", '

    if include_ingredients:
        json_str = json_str + '"includeIngredients": "'
        for ingredient in include_ingredients:
            json_str = json_str + f'{ingredient}, '
        json_str = json_str + '", '

    if exclude_ingredients:
        json_str = json_str + '"excludeIngredients": "'
        for ingredient in exclude_ingredients:
            json_str = json_str + f'{ingredient}, '
        json_str = json_str + '", '

    json_str = json_str + '"instructionsRequired": "true", "fillIngredients": "true", "addRecipeInformation": "true"}'
    # print("json_str=", json_str)
    flask_url = "http://localhost:8003/"
    response = requests.get(flask_url, params={"json_str": json_str})

    if response.text == "Sorry no recipe was found, try again":
        print("Sorry, No recipe found!")
    else:
        recipe = response.json()
        print(recipe)
    
    

# functions below

def greeting():
    """Greets the user and explains the purpose of Flavor Quest."""
    greeting = click.style("Welcome to Flavor Quest!", fg="green", bg="white", bold=True)
    click.echo(greeting)
    click.echo("\n")
    instructions = click.style("After answering just a few, quick, questions about your food intolerances, cuisine preferences, and more, we will show you a tasty recipe to try. If at any point you want to skip a question, enter 0, or if you’d like to see more details about the question, enter 1. Lastly, if you want to go back and change your response, enter 'Back'.", italic=True)
    click.echo(instructions)
    click.echo("\n")

def get_recipe_type():
    """Asks user what general recipe type they are interested in."""

    options = click.style("Enter 0 to skip this step.", italic=True)

    while True:
        click.echo("What type of recipe are you interested in? You may only enter 1 recipe type. examples - Pasta, Lamb Stew, Chicken Potato Casserole")
        recipe_type_prompt = click.style("Recipe Type", bold=True, fg="yellow")
        click.echo(options)
        recipe_type_input = click.prompt(recipe_type_prompt, type=str)
        click.echo("\n")
        recipe_type_result = process_recipe_type_input(recipe_type_input)
        
        if recipe_type_result is not None:
            return recipe_type_result
        
def process_recipe_type_input(recipe_type_input):

     # user wants to skip entering recipe type
    if recipe_type_input.strip() == "0":
        recipe_type_input = []
        return recipe_type_input
    
    # process recipe type input, strip whitespace, make lowercase, and ensure it is a valid response
    recipe_type_input = recipe_type_input.split(",")
    recipe_type_input = recipe_type_input[0].strip().lower()

    # check if recipe type are valid (cannot contain numbers or special symbols besides apostrophes)
    pattern = "^[a-zA-Z' ]+$"
    if re.match(pattern, recipe_type_input):
        return recipe_type_input
    else:
        click.echo("Your recipe type contained numbers or special characters. Try again.")
        return None


def get_cuisine_types():
    """Asks the user what cuisine types they are interested in. Can be skipped or user can see cuisine options."""
    
    possible_cuisines = ["African", "Asian", "American", "British", "Cajun", "Caribbean", "Chinese", "Eastern European", "European", "French", "German",
"Greek", "Indian", "Irish", "Italian", "Japanese", "Jewish", "Korean", "Latin American", "Mediterranean", "Mexican", "Middle Eastern", "Nordic", "Southern", "Spanish", "Thai", "Vietnamese"]

    while True:
        click.echo("What cuisine types are you interested in? (separate by commas)")
        options = click.style("Enter 0 to skip this step or 1 to see cuisine options.", italic=True)
        click.echo(options)
        cuisine_prompt = click.style("Cuisine Types", bold=True, fg="yellow")
        cuisine_input = click.prompt(cuisine_prompt, type=str)
        click.echo("\n")
        cuisine_result = process_cuisine_input(cuisine_input, possible_cuisines)
        
        if cuisine_result is not None:
            return cuisine_result

def process_cuisine_input(cuisine_types, possible_cuisines):
    """
    Checks if user wants to skip cuisine types, see cuisine options, go back, or entered cuisine types.
    If user entered cuisine types, checks if they are valid.
    """

    # user wants to skip entering options for cuisine types
    if cuisine_types.strip() == "0":
        cuisine_types = []
        return cuisine_types

    # user wants to see cuisine options
    elif cuisine_types.strip() == "1":
        click.echo("\nHere are the cuisine types you can choose from:")
        click.echo(", ".join(possible_cuisines))
        click.echo("\n")
        cuisine_types = None
        return cuisine_types
    
    elif cuisine_types.strip().lower() == "back":
        cuisine_types = False
        return cuisine_types

    # process cuisine_types input, seperate by commas, strip whitespace, and make lowercase
    cuisine_types = cuisine_types.split(",")
    cuisine_types = [cuisine.strip().lower() for cuisine in cuisine_types]

    # check if cuisine types are valid
    for cuisine in cuisine_types:
        if cuisine.title() not in possible_cuisines:
            click.echo("You entred an invalid cuisine type or have a misspelling. Please try again.")
            return None

    return cuisine_types
    
def get_diet_types():
    possible_diets = ["Gluten Free", "Ketogenic", "Vegetarian", "Lacto-Vegetarian", "Ovo-Vegetarian", "Vegan", "Pescetarian", "Paleo", "Primal", "Low FODMAP", "Whole30"]

    while True:
        click.echo("List all diet types that your recipe must follow (separate by commas)")
        options = click.style("0 = skip, 1 = show options, 'Back'= Return to previous prompt", italic=True)
        click.echo(options)
        diet_prompt = click.style("Diet Types", bold=True, fg="yellow")
        diet_input = click.prompt(diet_prompt, type=str)
        click.echo("\n")
        diet_result = process_diet_input(diet_input, possible_diets)
        
        if diet_result is not None:
            return diet_result
        
def process_diet_input(diet_types, possible_diets):
    """
    Checks if user wants to skip diet types, see diet options, go back to the previous prompt, or entered diet types.
    If user entered diet types, checks if they are valid.
    """

    # user wants to skip entering options for diet types
    if diet_types.strip() == "0":
        diet_types = []
        return diet_types

    # user wants to see diet options
    elif diet_types.strip() == "1":
        click.echo("\nHere are the diet types you can choose from:")
        click.echo(", ".join(possible_diets))
        click.echo("\n")
        diet_types = None
        return diet_types
    
    elif diet_types.strip().lower() == "back":
        diet_types = False
        return diet_types

    # process diet_types input, seperate by commas, strip whitespace, and make lowercase
    diet_types = diet_types.split(",")
    diet_types = [diet.strip().lower() for diet in diet_types]

    # check if diet types are valid
    for diet in diet_types:
        if diet.title() not in possible_diets:
            click.echo("You entred an invalid diet type or have a misspelling. Please try again.")
            return None

    return diet_types

def get_intolerances():
    possible_intolerances = ["Dairy", "Egg", "Gluten", "Grain", "Peanut", "Seafood", "Sesame", "Shellfish", "Soy", "Sulfite", "Tree Nut", "Wheat"]

    while True:
        click.echo("List all food intolerances that your recipe must exclude (separate by commas)")
        options = click.style("0 = skip, 1 = show options, 'Back'= Return to previous prompt", italic=True)
        click.echo(options)
        intolerance_prompt = click.style("Food Intolerances", bold=True, fg="yellow")
        intolerance_input = click.prompt(intolerance_prompt, type=str)
        click.echo("\n")
        intolerance_result = process_intolerance_input(intolerance_input, possible_intolerances)
        
        if intolerance_result is not None:
            return intolerance_result
        
def process_intolerance_input(intolerance_input, possible_intolerances):
    """
    Checks if user wants to skip food intolerance input, see intolerance options, go back to the previous prompt, or entered intolerances.
    If user entered intolerances, checks if they are valid.
    """

    # user wants to skip entering food intolerances
    if intolerance_input.strip() == "0":
        intolerance_result = []
        return intolerance_result

    # user wants to see intolerance options
    elif intolerance_input.strip() == "1":
        click.echo("\nHere are the food intolerances you can choose from:")
        click.echo(", ".join(possible_intolerances))
        click.echo("\n")
        intolerance_result = None
        return intolerance_result
    
    elif intolerance_input.lower() == "back":
        intolerance_result = False
        return intolerance_result

    # process intolerance_input, seperate by commas, strip whitespace, and make lowercase
    intolerance_input = intolerance_input.split(",")
    intolerance_input = [intolerance.strip().lower() for intolerance in intolerance_input]

    # check if intolerances are valid
    for intolerance in intolerance_input:
        if intolerance.title() not in possible_intolerances:
            click.echo("You entred an invalid food intolerance or have a misspelling. Please try again.")
            return None

    return intolerance_input

def get_include_ingredients():
    """Get ingredients that must be included in recipe"""

    while True:
        click.echo("List all ingredients that must be included in your recipe (separate by commas)")
        options = click.style("0 = skip, 'Back'= Return to previous prompt", italic=True)
        click.echo(options)
        include_ingredient_prompt = click.style("Ingredients to Include", bold=True, fg="yellow")
        include_ingredient_input = click.prompt(include_ingredient_prompt, type=str)
        click.echo("\n")
        include_ingredient_result = process_ingredient_input(include_ingredient_input)
        
        if include_ingredient_result is not None:
            return include_ingredient_result
        
def get_exclude_ingredients():
    """Get ingredients that must be excluded in recipe"""

    while True:
        click.echo("List all ingredients that must be excluded from your recipe (separate by commas)")
        options = click.style("0 = skip, 'Back'= Return to previous prompt", italic=True)
        click.echo(options)
        exclude_ingredient_prompt = click.style("Ingredients to Exclude", bold=True, fg="yellow")
        exclude_ingredient_input = click.prompt(exclude_ingredient_prompt, type=str)
        click.echo("\n")
        exclude_ingredient_result = process_ingredient_input(exclude_ingredient_input)
        
        if exclude_ingredient_result is not None:
            return exclude_ingredient_result
        
def process_ingredient_input(ingredient_input):
    """
    Checks if user wants to skip ingredient input, go back to the previous prompt, or entered ingredients.
    If user entered ingredients, checks if they are valid.
    """

    # user wants to skip entering ingredients
    if ingredient_input.strip() == "0":
        ingredient_result = []
        return ingredient_result
    
    elif ingredient_input.lower() == "back":
        ingredient_result = False
        return ingredient_result

    # process ingredient_input, seperate by commas, strip whitespace, and make lowercase
    ingredient_input = ingredient_input.split(",")
    ingredient_input = [ingredient.strip().lower() for ingredient in ingredient_input]

    # check if ingredients are valid (cannot contain numbers or special symbols besides apostrophes)
    pattern = "^[a-zA-Z' ]+$"
    for ingredient in ingredient_input:
        if re.match(pattern, ingredient):
            continue
        else:
            click.echo("One or more of your ingredients contained numbers or special characters. Try again.")
            return None

    return ingredient_input

def get_meal_types():
    possible_meal_types = ["Main Course", "Side Dish", "Dessert", "Appetizer", "Salad", "Bread", "Breakfast", "Soup", "Beverage", "Sauce", "Marinade", "Fingerfood", "Snack", "Drink"]

    while True:
        click.echo("List all meal types that you are interested in (separate by commas)")
        options = click.style("0 = skip, 1 = show options, 'Back'= Return to previous prompt", italic=True)
        click.echo(options)
        meal_type_prompt = click.style("Meal Types", bold=True, fg="yellow")
        meal_type_input = click.prompt(meal_type_prompt, type=str)
        click.echo("\n")
        meal_type_result = process_meal_type_input(meal_type_input, possible_meal_types)
        
        if meal_type_result is not None:
            return meal_type_result
        
def process_meal_type_input(meal_type_input, possible_meal_types):
    """
    Checks if user wants to skip meal type input, see meal type options, go back to the previous prompt, or entered meal types.
    If user entered meal types, checks if they are valid.
    """

    # user wants to skip entering meal types
    if meal_type_input.strip() == "0":
        meal_type_result = []
        return meal_type_result

    # user wants to see meal type options
    elif meal_type_input.strip() == "1":
        click.echo("\nHere are the meal types you can choose from:")
        click.echo(", ".join(possible_meal_types))
        click.echo("\n")
        meal_type_result = None
        return meal_type_result
    
    elif meal_type_input.lower() == "back":
        meal_type_result = False
        return meal_type_result

    # process meal_type_input, seperate by commas, strip whitespace, and make lowercase
    meal_type_input = meal_type_input.split(",")
    meal_type_input = [meal.strip().lower() for meal in meal_type_input]

    # check if meal types are valid
    for meal in meal_type_input:
        if meal.title() not in possible_meal_types:
            click.echo("You entred an invalid meal type or have a misspelling. Please try again.")
            return None

    return meal_type_input

if __name__ == '__main__':
    start()
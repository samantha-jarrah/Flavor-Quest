import json
import click
from flavor_quest_functions import (
    get_recipe_type,
    get_cuisine_types,
    get_diet_types,
    get_intolerances,
    get_include_ingredients,
    get_exclude_ingredients,
    get_meal_types,
    create_json_str,
    make_request,
    greeting,
)

@click.command()
def recipe_search():
    """
    Returns a pdf of a recipe that satifies given parameters
    """

    # clears the terminal
    click.clear()
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

    json_str = create_json_str(recipe_type, cuisine_types, diet_types, intolerances, include_ingredients, exclude_ingredients)
    flask_url = "http://localhost:8003/"
    make_request(flask_url, json_str)   # make API request using user parameters
    
@click.command()
def random_recipe():
    """Returns a completely random recipe"""
    json_str = json.dumps({"instructionsRequired": "true", "fillIngredients": "true", "addRecipeInformation": "true"})
    flask_url = "http://localhost:8003/"
    make_request(flask_url, json_str)
    
if __name__ == '__main__':
    cli = click.Group()   # create click group to hold commands

    cli.add_command(recipe_search)
    cli.add_command(random_recipe)
    cli()

import click
click.clear()

@click.command()
def start():
    greeting()
    cuisine_types = get_cuisine_types()
    diet_types = get_diet_types()
    

def greeting():
    """Greets the user and explains the purpose of Flavor Quest."""
    greeting = click.style("Welcome to Flavor Quest!", fg="green", bg="white", bold=True)
    click.echo(greeting)
    click.echo("\n")
    instructions = click.style("After answering just a few, quick, questions about your food intolerances, cuisine preferences, and more, we will show you a tasty recipe to try. If at any point you want to skip a question, enter 0, or if you’d like to see more details about the question, enter 1. Lastly, if you want to go back and change your response, enter 'Back'.", italic=True)
    click.echo(instructions)
    click.echo("\n")

def get_cuisine_types():
    """Asks the user what cuisine types they are interested in. Can be skipped or user can see cuisine options."""
    
    possible_cuisines = ["African", "Asian", "American", "British", "Cajun", "Caribbean", "Chinese", "Eastern European", "European", "French", "German",
"Greek", "Indian", "Irish", "Italian", "Japanese", "Jewish", "Korean", "Latin American", "Mediterranean", "Mexican", "Middle Eastern", "Nordic", "Southern", "Spanish", "Thai", "Vietnamese"]

    while True:
        click.echo("What cuisine types are you interested in? (separate by commas)")
        options = click.style("Enter 0 to skip this step or 1 to see cuisine options.", italic=True)
        click.echo(options)
        click.echo("\n")
        cuisine_prompt = click.style("Cuisine Types", bold=True, fg="yellow")
        cuisine_input = click.prompt(cuisine_prompt, type=str)
        cuisine_result = process_cuisine_input(cuisine_input, possible_cuisines)
        
        if cuisine_result is not None:
            return cuisine_result

def process_cuisine_input(cuisine_types, possible_cuisines):
    """
    Checks if user wants to skip cuisine types, see cuisine options, or entered cuisine types.
    If user entered cuisine types, checks if they are valid.
    """

    # user wants to skip entering options for cuisine types
    if cuisine_types.strip() == "0":
        cuisine_types = []
        return cuisine_types

    # user wants to see cuisine options
    elif cuisine_types == "1":
        click.echo("\nHere are the cuisine types you can choose from:")
        click.echo(", ".join(possible_cuisines))
        click.echo("\n")
        cuisine_types = None
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
        click.echo("\n")
        diet_prompt = click.style("Diet Types", bold=True, fg="yellow")
        diet_input = click.prompt(diet_prompt, type=str)
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
    elif diet_types == "1":
        click.echo("\nHere are the diet types you can choose from:")
        click.echo(", ".join(possible_diets))
        click.echo("\n")
        diet_types = None
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

if __name__ == '__main__':
    start()
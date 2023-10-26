import click

@click.command()
def start():
    greeting()
    cuisine_types = get_cuisine_types()
    click.echo(f"cuisine_types={cuisine_types}")
    diet_types = get_diet_types()
    click.echo(f"diet_types={diet_types}")
    

def greeting():
    """Greets the user and explains the purpose of Flavor Quest."""

    click.echo("Welcome to Flavor Quest!\n")
    click.echo("After answering just a few, quick, questions about your food intolerances, cuisine preferences, and more, we will show you a tasty recipe try. If at any point you want to skip a question, enter 0, or if you’d like to see more details about the question, enter 1. Lastly, if you want to go back and change your response, enter 'Back'.\n")
    # get_cuisine_types()

def get_cuisine_types():
    """Asks the user what cuisine types they are interested in. Can be skipped or user can see cuisine options."""
    
    possible_cuisines = ["African", "Asian", "American", "British", "Cajun", "Caribbean", "Chinese", "Eastern European", "European", "French", "German",
"Greek", "Indian", "Irish", "Italian", "Japanese", "Jewish", "Korean", "Latin American", "Mediterranean", "Mexican", "Middle Eastern", "Nordic", "Southern", "Spanish", "Thai", "Vietnamese"]

    while True:
        click.echo("What cuisine types are you interested in? (separate by commas)")
        click.echo("Enter 0 to skip this step or 1 to see cuisine options.")
        cuisine_input = click.prompt("Cuisine Types", type=str)
        cuisine_result = process_cuisine_input(cuisine_input, possible_cuisines)
        
        if cuisine_result is not None:
            return cuisine_result

def process_cuisine_input(cuisine_types, possible_cuisines):
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
    click.echo("Made it to diet prompt!")

if __name__ == '__main__':
    start()
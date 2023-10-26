import click

@click.command()
def start():
    greeting()

def greeting():
    click.echo("Welcome to Flavor Quest!\n")
    click.echo("After answering just a few, quick, questions about your food intolerances, cuisine preferences, and more, we will show you a tasty recipe try. If at any point you want to skip a question, enter 0, or if you’d like to see more details about the question, enter 1. Lastly, if you want to go back and change your response, enter 'Back'.\n")
    get_cuisine_types()

def get_cuisine_types():
    click.echo("What cuisine types are you intrested in? (seperate by commas)")
    click.echo("Enter 0 to skip this step or 1 to see cuisine options.")
    cuisine_types = click.prompt("Cuisine Types", type=str)
    click.echo(cuisine_types)

if __name__ == '__main__':
    start()
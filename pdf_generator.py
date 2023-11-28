import os
from io import BytesIO
import requests
from reportlab.platypus import SimpleDocTemplate, Paragraph, Image
from reportlab.lib.styles import getSampleStyleSheet

def build_recipe_pdf(recipe):
    """
    Parses recipe input and saves into list of flowables 
    to be rendered in PDF using reportlab library
    """

    recipe_name = recipe['title']
    webpage = recipe['sourceUrl']
    servings = recipe["servings"]
    time = recipe["readyInMinutes"]
    file_name = f"{recipe_name}.pdf"

    image_url = recipe["image"]
    response = requests.get(image_url)
    image_data = BytesIO(response.content)

    pdf_path = os.path.abspath(file_name) # where pdf will be saved to computer
    pdf = SimpleDocTemplate(file_name)

    ingredients = []   
    steps = {}   # recipe steps, key=number, value=instruction
    for ingredient in recipe["extendedIngredients"]:
        ingredients.append(ingredient["original"])

    for i in recipe["analyzedInstructions"]:
        for j in i["steps"]:
            steps[j[str("number")]] = j["step"]

    flowables = []   # what gets rendered on pdf

    sss = getSampleStyleSheet()
    # append to flowables: recipe title, sourceURL, servings, 
    # time to make, image, ingredients, instructions
    flowables.append(Paragraph(recipe_name.title(), sss["Title"]))
    flowables.append(Paragraph(f"Recipe from: {webpage}", sss["Heading5"]))
    flowables.append(Paragraph(f"{servings} servings", sss["Heading6"]))
    flowables.append(Paragraph(f"Time to make (minutes): {time}", sss["Heading6"]))
    flowables.append(Image(image_data))
    flowables.append(Paragraph("Ingredients", sss["Heading3"]))

    for ingredient in ingredients:
        flowables.append(Paragraph(f"- {ingredient}", sss["Normal"]))

    flowables.append(Paragraph("Instructions", sss["Heading3"]))

    for num, direction in steps.items():
        flowables.append(Paragraph(f"{num}) {direction}"))
    pdf.build(flowables)
    return pdf_path

import os
from io import BytesIO
import requests
from reportlab.platypus import SimpleDocTemplate, Paragraph, Image
from reportlab.lib.styles import getSampleStyleSheet
# from reportlab.lib import utils


def build_recipe_pdf(recipe):
    """Parses recipe input and saves into list of flowables to be rendered in PDF using reportlab library"""

    recipe_name = recipe['title']
    webpage = recipe['sourceUrl']
    servings = recipe["servings"]
    time = recipe["readyInMinutes"]
    file_name = f"{recipe_name}.pdf"

    image_url = recipe["image"]
    response = requests.get(image_url)
    image_data = BytesIO(response.content)

    pdf_path = os.path.abspath(file_name)   # where pdf will be saved to computer
    pdf = SimpleDocTemplate(file_name)

    ingredients = []
    steps = {}
    for ingredient in recipe["extendedIngredients"]:
        ingredients.append(ingredient["original"])

    for i in recipe["analyzedInstructions"]:
        for j in i["steps"]:
            steps[j[str("number")]] = j["step"]

    flowables = []

    sss = getSampleStyleSheet()

    flowables.append(Paragraph(recipe_name.title(), sss["Title"])) # recipe title
    flowables.append(Paragraph(f"Recipe from: {webpage}", sss["Heading5"]))   # source URL
    flowables.append(Paragraph(f"{servings} servings", sss["Heading6"]))   # servings
    flowables.append(Paragraph(f"Time to make: {time}", sss["Heading6"]))   # time to make recipe
    flowables.append(Image(image_data))
    flowables.append(Paragraph("Ingredients", sss["Heading3"]))  # ingredient header

    for ingredient in ingredients:   # ingredient list
        flowables.append(Paragraph(f"- {ingredient}", sss["Normal"]))

    flowables.append(Paragraph("Instructions", sss["Heading3"]))  # instruction header

    for num, direction in steps.items():   # instructions
        flowables.append(Paragraph(f"{num}) {direction}"))
    pdf.build(flowables)
    return pdf_path
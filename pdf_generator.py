import os
import html
from io import BytesIO
import requests
from reportlab.platypus import SimpleDocTemplate, Paragraph, Image
from reportlab.lib.styles import getSampleStyleSheet

def build_recipe_pdf(recipe):
    """
    Parses recipe input and saves into list of flowables 
    to be rendered in PDF using reportlab library
    """

    file_name = f"{recipe['title']}.pdf"
    response = requests.get(recipe["image"])
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
    # append to flowables: recipe title, sourceURL, servings, time to make, image, ingredients, instructions
    flowables.append(Paragraph(html.escape(recipe['title']).title(), sss["Title"]))
    flowables.append(Paragraph(f"Recipe from: {html.escape(recipe['sourceUrl'])}", sss["Heading5"]))
    flowables.append(Paragraph(f"{html.escape(str(recipe['servings']))} servings", sss["Heading6"]))
    flowables.append(Paragraph(f"Time to make (minutes): {recipe['readyInMinutes']}", sss["Heading6"]))
    flowables.append(Image(image_data))
    flowables.append(Paragraph("Ingredients", sss["Heading3"]))

    for ingredient in ingredients:
        ingr = html.escape(ingredient)
        flowables.append(Paragraph(f"- {ingr}", sss["Normal"]))

    flowables.append(Paragraph("Instructions", sss["Heading3"]))

    for num, direction in steps.items():
        direc = html.escape(direction)
        flowables.append(Paragraph(f"{num}) {direc}"))
    pdf.build(flowables)
    return pdf_path

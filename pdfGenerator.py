from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import SimpleDocTemplate, Paragraph, Image
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.utils import ImageReader
import os

def buildRecipePDF(recipe):
    recipeName = recipe['title']
    webpage = recipe['sourceUrl']
    servings = recipe["servings"]
    time = recipe["readyInMinutes"]
    # summary = recipe["summary"]
    file_name = f"{recipeName}.pdf"
    imageURL = recipe["image"]
    pdf_path = os.path.abspath(file_name)
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
    # print(sss.list())

    flowables.append(Paragraph(recipeName.title(), sss["Title"])) # recipe title
    flowables.append(Paragraph(f"Recipe from: {webpage}", sss["Heading4"]))   # source URL
    flowables.append(Paragraph(f"{servings} servings", sss["Heading4"]))   # servings
    flowables.append(Paragraph(f"Time to make: {time}", sss["Heading4"]))   # time to make recipe
    # flowables.append(Image(image, width=200, height=200))
    # flowables.append(Paragraph(summary, sss["Normal"]))
    flowables.append(Paragraph("Ingredients", sss["Heading3"]))  # ingredient header

    for ingredient in ingredients:   # ingredient list
        flowables.append(Paragraph(f"- {ingredient}", sss["Normal"]))

    flowables.append(Paragraph("Instructions", sss["Heading3"]))  # instruction header

    for num, direction in steps.items():   # instructions
        flowables.append(Paragraph(f"{num}) {direction}"))
    pdf.build(flowables)
    return pdf_path


from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import SimpleDocTemplate, Paragraph
from reportlab.lib.styles import getSampleStyleSheet

def buildRecipePDF(recipe):
    recipeName = recipe['title']
    webpage = recipe['sourceUrl']
    servings = recipe["servings"]
    time = recipe["readyInMinutes"]
    summary = recipe["summary"]

    ingredients = []
    steps = {}
    for ingredient in recipe["extendedIngredients"]:
        ingredients.append(ingredient["original"])

    for i in recipe["analyzedInstructions"]:
        for j in i["steps"]:
            steps[j[str("number")]] = j["step"]

    fileName = f"{recipeName}.pdf"  # use f-string to get recipe title
    pdf = SimpleDocTemplate(fileName)

    flowables = []

    sss = getSampleStyleSheet()
    # print(sss.list())

    flowables.append(Paragraph(recipeName.title(), sss["Title"])) # recipe title
    flowables.append(Paragraph(f"Recipe from: {webpage}", sss["Heading4"]))   # source URL
    flowables.append(Paragraph(f"{servings} servings", sss["Heading4"]))   # servings
    flowables.append(Paragraph(f"Time to make: {time}", sss["Heading4"]))   # time to make recipe
    flowables.append(Paragraph(summary, sss["Normal"]))
    flowables.append(Paragraph("Ingredients", sss["Heading3"]))  # ingredient header

    for ingredient in ingredients:   # ingredient list
        flowables.append(Paragraph(f"- {ingredient}", sss["Normal"]))

    flowables.append(Paragraph("Instructions", sss["Heading3"]))  # instruction header

    for num, direction in steps.items():   # instructions
        flowables.append(Paragraph(f"{num}) {direction}"))
    pdf.build(flowables)


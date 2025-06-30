import pdfplumber

with pdfplumber.open("133010341530993119.pdf") as pdf:
    page = pdf.pages[0]
    text = page.extract_text()
    print(text)

import os
from pypdf import PdfWriter
path = "E:\Programing(Documents)\deep python\Python-Source-Code\exercises\Exercise 8 - Merge the PDF"
files = os.listdir(path)


merger = PdfWriter()

for pdfFile in files:
    if(pdfFile.endswith(".pdf")):
        merger.append(pdfFile)
merger.write("merged-pdf.pdf")
merger.close()
import PyPDF2
import pytesseract
import os
import re

from docx import Document
from PIL import Image


def main():
    rootdir = 'I:\\test'
    for subdir, dirs, files in os.walk(rootdir):
        for file in files:
            links = []
            if file.endswith('.pdf') or file.endswith('.Pdf') or file.endswith('.PDF'):
                pdf_reader(subdir, file, links)
            elif file.endswith('.jpg') or file.endswith('.png') or file.endswith('.jpeg') or file.endswith('.tif'):
                image_reader(subdir, file, links)
            elif file.endswith('.txt'):
                txt_reader(subdir, file, links)
            elif file.endswith('.docx'):
                docx_reader(subdir, file, links)
            else:
                try:
                    print(file.title().split('.')[1])
                    # pass
                except IndexError:
                    continue
                continue
            if len(links) > 0:
                print(subdir + '\\' + file + ':', links)


def txt_reader(subdir, file, links):
    txt = open(subdir + "\\" + file, 'r').read()
    links_found = re.findall(r'farmingdale.edu/.*\b', txt, re.IGNORECASE)
    # checks to see if any links were found
    if len(links_found) > 0:
        links.append(links_found)


def docx_reader(subdir, file, links):
    doc = Document(subdir + "\\" + file)
    full_text = ''
    for para in doc.paragraphs:
        full_text += para.text+'\n'
    links_found = re.findall(r'farmingdale.edu/.*\b', full_text, re.IGNORECASE)
    # checks to see if any links were found
    if len(links_found) > 0:
        links.append(links_found)


def pdf_reader(subdir, file, links):
    pdf = PyPDF2.PdfFileReader(open(subdir + '\\' + file, 'rb'))
    for i in range(0, pdf.numPages):
        page = pdf.getPage(i).extractText()
        links_found = re.findall(r'farmingdale.edu/.*\b', page, re.IGNORECASE)
        # checks to see if any links were found
        if len(links_found) > 0:
            links.append(links_found)


def image_reader(subdir, file, links):
    img = pytesseract.image_to_string(Image.open(subdir + '\\' + file))
    links_found = re.findall(r'farmingdale.edu/.*\b', img, re.IGNORECASE)
    if len(links_found) > 0:
        links.append(links_found)


if __name__ == '__main__':
    main()

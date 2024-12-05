# from docx import Document
import pymupdf
import os
from pprint import pprint


def read_txt(file):
    with open(file, "r", encoding="utf-8") as f:
        raw_text = f.read()
    return raw_text


# def read_docx(file):
#     doc = Document(file)
#     text = []
#     for paragraph in doc.paragraphs:
#         text.append(paragraph.text)
#     return "\n".join(text)


def read_pdf(file):
    if file is None:
        print("File tidak ada")
        return "File tidak boleh kosong"
    try:
        doc = pymupdf.open(file)
        raw_text = []
        for page in doc:
            raw_text.append(page.get_text().encode("utf8"))
        return b"\n".join(raw_text).decode()
    except Exception as e:
        print(e)


_, ext = os.path.splitext("./document.pdf")
pprint(read_pdf("./document.pdf"))

import re
from datetime import date, datetime
import datetime
from pytesseract import image_to_string
import PIL
from PIL import Image
from pdfminer.layout import LAParams
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import TextConverter
from io import StringIO
from pdfminer.pdfpage import PDFPage
from pdf2image import convert_from_path
import pytesseract as pt
import MDSLib as ML


from gettext import gettext
from logging import disable
from re import S, T, X
from statistics import mode
import pdfplumber as pp
from pdfminer.layout import LAParams
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import TextConverter
from io import StringIO
from pdfminer.pdfpage import PDFPage
import pymssql
import os
import subprocess
#Livraria das funções de OCR
import sys
from datetime import date 
from decimal import Decimal
from MDSLib import sprint

caminho_PDF = ''

#PLUMBER
pdf_name = caminho_PDF
doc = convert_from_path(pdf_name)
texto = ''
for page_number, page_data in enumerate(doc):
    txt = pt.image_to_string(page_data, lang='por')
    print(page_number)
    texto = ''.join((texto, txt))
    texto = texto.lower()
#print(texto)

#TESSERACT
resource_manager = PDFResourceManager(caching=True)
out_text = StringIO()
codec = 'utf-8'
laParams = LAParams()
text_converter = TextConverter(resource_manager, out_text, laparams=laParams)
fp = open(caminho_PDF, 'rb')
interpreter = PDFPageInterpreter(resource_manager, text_converter)
for page in PDFPage.get_pages(fp, pagenos=set(), maxpages=0, password="", caching=True, check_extractable=True):
    interpreter.process_page(page)
text = out_text.getvalue()
fp.close()
text_converter.close()
out_text.close()
text = text.lower()
#print(text)

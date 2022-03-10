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
import MDSLib as ML
import sys
from datetime import date 
from decimal import Decimal
from MDSLib import sprint


caminho_PDF = ''

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
print(text)


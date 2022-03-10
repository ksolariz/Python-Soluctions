from time import sleep
import pyautogui
#import pyodbc       
import clipboard
import base64
from os import getenv
import keyboard
from datetime import datetime,date
from ftplib import FTP
import io
import os
import sys
import time
import wave
import json
import shutil
import tempfile
import traceback
import unicodedata
from io import BytesIO
from pathlib import Path
import lxml.html
import pymssql
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.chrome.options import Options
import lxml.html as lhtml
import requests
import importlib
import selenium_util
importlib.reload(selenium_util)
from selenium_util import *
import glob
import MDSLib as ML
import OCRCentral as OCR
import globalConf as GC
#----------------------------------------------------------------------
caminho_relatorio = GC.caminho_relatorio

chrome_options = Options()
chrome_options.add_experimental_option("prefs", {
"download.default_directory": caminho_relatorio,
"download.prompt_for_download": False, "plugins.always_open_pdf_externally": True
})

dataHoje = date.today().strftime('%Y-%m-%d')
print(dataHoje)


driver = webdriver.Chrome(executable_path=GC.caminho_chromedriver, options=chrome_options)

#CONEXÃO COM BANCO DE DADOS
conn = pymssql.connect(server=GC.server, user=GC.user, password=GC.password, database=GC.database)
cursor = conn.cursor()

driver.get(GC.caminho_login_localiza)
driver.maximize_window()

user = ""
password = ""
data_emissaoIni = '20/10/2021'
data_emissaoFim = '20/11/2021'
# Login e senha
txt_login = aguardar_query(Query(driver).by_id('Login'))
txt_login.clear()
txt_login.send_keys(user)
txt_pass = aguardar_query(Query(driver).by_id('Senha'))
txt_pass.clear()
txt_pass.send_keys(password)
aguardar_query(Query(driver).by_id('botaoLogin')).click()
time.sleep(1)

#inputLink = driver.find_element_by_xpath('//*[@id="bodyInformacoesGerais"]/h1[1]/span').click()
inputLink = aguardar_query(Query(driver).by_xpath('//*[@id="bodyInformacoesGerais"]/h1[1]/span')).click()

xpath = '//*[@id="DataEmissaoInicio"]'
driver.find_element_by_xpath(xpath).send_keys(data_emissaoIni)
xpath = '//*[@id="DataEmissaoFinal"]'
driver.find_element_by_xpath(xpath).send_keys(data_emissaoFim)

xpath = '//*[@id="FiltroStatusPagamento"]/option[5]'
driver.find_element_by_xpath(xpath).click()

#Filtrar
driver.execute_script('ValidarEEnviarFormulario();')

time.sleep(5)
xpath = '/html/body/div[6]/div/form/div[2]/div[2]/label'
qtdRelatorios = driver.find_element_by_xpath(xpath).get_attribute("innerText")
qtdRelatorios = qtdRelatorios.replace('Quantidade:','')
qtdRelatorios = qtdRelatorios.strip()
valorLoop = int(qtdRelatorios) / 10

print('Quantidade: ' + qtdRelatorios)


for y in range(2,int(valorLoop + 1)):
#for y in range(2,3):    

    for x in range(1,11):
    #for x in range(1,11):    
        
            xpath = f'/html/body/div[6]/div/form/div[2]/table/tbody/tr[{x}]/td[1]/input'
            driver.find_element_by_xpath(xpath).click()
            time.sleep(1)
            driver.execute_script('ExibirModalImprimirSelecionadas()')
            time.sleep(3)
            driver.execute_script('aoConfirmarImpressaoFaturaDemonstrativo()')
            time.sleep(13)
            driver.find_element_by_xpath(xpath).click()
            time.sleep(7)
            list_of_files = glob.glob(caminho_relatorio+'*') # * means all if need specific format then *.csv
            latest_file = max(list_of_files, key=os.path.getmtime)
            latest_file = latest_file.replace("\\", "/")
            #print(latest_file)
            #PEGA APENAS O NOME DO ULTIMO ARQUIVO BAIXADO
            nome_arquivo = latest_file.split('/') 
            nome_arquivo = nome_arquivo[-1]
           
            insert = f'''
            
            INSERT INTO INFORMACOES_RESERVA_COCKPIT(
                dataDownload,
                NOME_DOC,
                MEIO_DE_ENTRADA,
                FORNECEDOR,
                DATA_ABERTURA,
                Atividade

            )
            VALUES(
                '{dataHoje}',
                '{nome_arquivo}',
                'Localiza',
                'Itpower',
                '{dataHoje}',
                'A iniciar'

            )
            
            
            '''
            print(insert)
            cursor.execute(insert)
            conn.commit()
            cursor.execute('select @@identity')
            id = cursor.fetchone()
            id = id[0]
            print('O ID É: ' + str(id))
            time.sleep(3)
            OCR.ocrAvipam(id)

       
    try:        
        driver.execute_script(f"Paginar('idFormFiltrarFaturas', {y})")
        time.sleep(3)
    except:
        print('Me passei de fato 2(dois)')
        pass
        

driver.quit()


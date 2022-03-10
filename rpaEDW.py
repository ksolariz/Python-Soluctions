from re import X
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
import lxml.html as lhtml
import requests
import importlib
import selenium_util
importlib.reload(selenium_util)
from selenium_util import *
import globalConf as GC

def roboEDW(id):

    conn = pymssql.connect(server=GC.server, user=GC.user, password=GC.password, database=GC.database)
    cursor = conn.cursor()
    update = f'''
        UPDATE INFORMACOES_RESERVA_COCKPIT SET
        atividade = 'Em andamento'
        where ID_RESERVA = {id}
    
    '''
    cursor.execute(update)
    conn.commit()

    select = f'''

        SELECT * from INFORMACOES_RESERVA_COCKPIT
        where ID_RESERVA = {id}

    '''
    cursor.execute(select)
    row = cursor.fetchone()
    reserva = row[7]
    data_boleto = row[15]
    data_vencimento_boleto = row[17]
    diariaValorLiq = row[31].replace(',','.')
    dataRetorno = row[32]
    dataSaida = row[33]
    usuario = row[34]
    totalGasto = row[35].replace(',','.')
    nome = row[39]
    sobrenome = row[40]
    taxaDeAluguel = row[48].replace(',','.')
    diariaValorTotal = row[25].replace(',','.')
    totalCascoValorTotal = row[26].replace(',','.')
    totalRCF = row[27].replace(',','.')
    combustivel = row[29].replace(',','.')
    LavagemCarro = row[30].replace(',','.')
    totalGasto = row[35].replace(',','.')
    num_doc = row[50]
    descontoInco = row[51]
    somaArray = '0.00'
    if diariaValorTotal == '':
        diariaValorTotal = '0.00'
    elif totalCascoValorTotal == '':
        totalCascoValorTotal = '0.00'
    elif totalRCF == '':
        totalRCF = '0.00'
    elif combustivel == '':
        combustivel = '0.00'
    else:
        arrSoma = [float(diariaValorTotal) , float(totalRCF) , float(totalCascoValorTotal),float(combustivel),]
        somaArray = sum(arrSoma)


    somaExtra = '0.00'
    if totalCascoValorTotal == '':
        totalCascoValorTotal = '0.00'
    elif totalRCF == '':
        totalRCF = '0.00'
    elif combustivel == '':
        combustivel = '0.00'
    else:
        arrSomaExt = [float(totalCascoValorTotal),float(combustivel),float(totalRCF)]
        somaExtra = sum(arrSomaExt)
    print(usuario)
    print(dataRetorno)
    print(dataSaida)


    dataHoje = date.today().strftime('%d/%m/%Y')
    #VARIAVEIS QUE RECEBE A RESPOSTAS DA ANALISE
    checkDatas = ''
    checkNomes = ''
    checkFornecedor = ''
    checkDiaria = ''
    checkTaxas = ''
    chechTarifa = ''

    #-------------------------------------------
    user = ""
    password = ""
    statusRPA = ''
    headless = False 
    
    driver = webdriver.Chrome(executable_path=GC.caminho_chromedriver)

    def buscaReserva(num, nu_rs):
        print("Iniciou Robo EDW")
        StatusRPA = ''
        statusProcesso = 'Não cadastrado' 

        if headless:
            driver.set_window_size(1920, 1080)
        else:
            driver.maximize_window()

        driver.get(GC.Url_EDW_1)
        StatusRPA = 'Iniciando login no EDW'
        txt_login = aguardar_query(Query(driver).by_id('txtLogin'))
        txt_login.clear()
        txt_login.send_keys(user)
        txt_pass = aguardar_query(Query(driver).by_id('txtSenha'))
        txt_pass.clear()
        txt_pass.send_keys(password)
        aguardar_query(Query(driver).by_id('btnLogin')).click()
        time.sleep(1)
        
        driver.get(GC.Url_EDW_2)

        print(f'num - {num} nu_rs -{id}')
        #num_reserva, estado, formaPag = ""
        #CTM
        #txtCtm = aguardar_query(Query(driver).by_id('ctl00_ContentPlaceHolder1_txtCodReq'))
        txtCtm = aguardar_query(Query(driver).by_id('ctl00_ContentPlaceHolder1_txtConfirmaFornec'))
        txtCtm.clear()
        txtCtm.send_keys(num) 

        aguardar_query(Query(driver).by_id('ctl00_ContentPlaceHolder1_btnPesquisar')).click()
        time.sleep(2)
        try:
            xpath = '//*[@id="ctl00_ContentPlaceHolder1_grdResult"]/tbody/tr[2]/td[1]/a'
            driver.find_element_by_xpath(xpath).click()
        except:
            localizado = "Nao localizado"
            print(localizado)
            
        localizado = 'False'
        try:
            xpath = '//*[@id="ctl00_ContentPlaceHolder1_grdResult_ctl01_Img1"]'
            driver.find_element_by_xpath(xpath).click()
            localizado = 'True'
            print('Não localizou')
        except:
            pass

        if localizado == 'True':
            StatusRPA = 'Consulta não localizada'
            conn = pymssql.connect(server=GC.server, user=GC.user, password=GC.password, database=GC.database)
            cursor = conn.cursor()
            update = f'''UPDATE INFORMACOES_RESERVA_COCKPIT SET 
            startRPA = 1,
            NAO_LOCALIADO = 1,
            statusRPA = '{StatusRPA}',
            atividade = '{statusProcesso}'
            WHERE ID_RESERVA = {id}'''
            cursor.execute(update)
            conn.commit()
            conn.close()
            driver.close()
        else:

            StatusRPA = 'Iniciando consulta da reserva EDW'
            
            body = driver.find_element_by_tag_name('html').get_attribute('outerHTML')
            body = lhtml.fromstring(body)

            num_reserva = body.xpath('//*[@id="ctl00_ContentPlaceHolder1_grdResult"]/tbody/tr[2]/td[1]/a/text()')
            print(f'Numero lista: {num_reserva[0]}')
            
            num_reserva = num_reserva[0]
            print(num_reserva)

            estado = body.xpath('//*[@id="ctl00_ContentPlaceHolder1_grdResult"]/tbody/tr[2]/td[3]/text()')
            estado = estado[0]
            print('Estado: ' + estado)

            formaPag = body.xpath('//*[@id="ctl00_ContentPlaceHolder1_grdResult"]/tbody/tr[2]/td[4]/text()')
            formaPag = formaPag[0] 
            print('Formapag: ' + formaPag)

            NomeCliente = body.xpath('//*[@id="ctl00_ContentPlaceHolder1_grdResult"]/tbody/tr[2]/td[35]/text()')
            NomeCliente = NomeCliente[0]
            print('Nome: ' + NomeCliente)
            conn = pymssql.connect(server=GC.server, user=GC.user, password=GC.password, database=GC.database)
            cursor = conn.cursor()
            update = f'''UPDATE INFORMACOES_RESERVA_COCKPIT SET 
                            ESTADO = '{estado}',
                            NUM_RESERVA = '{num_reserva}',
                            NOME_CLIENTE = '{NomeCliente}',
                            FORMA_PAGAMENTO = '{formaPag}'
                            WHERE ID_RESERVA = {nu_rs}'''
            cursor.execute(update)
            conn.commit()
            conn.close()
            print(update + ' foi 2')
            driver.close()
            driver.switch_to.window(driver.window_handles [ 0 ])
            StatusRPA = 'Iniciando validação de Datas'
            xpath = '//*[@id="ctl00_ContentPlaceHolder1_txtCheckIn"]'
            checkDataRetorno = driver.find_element_by_xpath(xpath).get_attribute('value')
            xpath = '//*[@id="ctl00_ContentPlaceHolder1_txtCheckOut"]'
            checkDataSaida = driver.find_element_by_xpath(xpath).get_attribute('value')

            dataApoio = ''
            if dataRetorno == checkDataRetorno:
                dataApoio = 'true'
            if dataSaida == checkDataSaida and dataApoio == 'true':
                checkDatas = 'OK'
            else:
                checkDatas = 'NOK'
            StatusRPA = 'Iniciando validação de nomes'
            xpath = '//*[@id="ctl00_ContentPlaceHolder1_txtHNomePax_Nome"]'
            nomeEDW = driver.find_element_by_xpath(xpath).get_attribute('value')
            xpath = '//*[@id="ctl00_ContentPlaceHolder1_txtHNomePax_Sobrenome"]'
            sobrenomeEDW = driver.find_element_by_xpath(xpath).get_attribute('value')
            somaNomeEDW = nomeEDW + ' ' + sobrenomeEDW
            checkApoio = ''

            if nome in somaNomeEDW:
                checkApoio = 'true'
            if sobrenome in somaNomeEDW and checkApoio == 'true':
                checkNomes = 'OK'
            else:
                checkNomes = 'NOK'
            StatusRPA = 'Iniciando validação de fornecedor'
            xpath = '//*[@id="ctl00_ContentPlaceHolder1_txtCia"]'
            fornecedor = driver.find_element_by_xpath(xpath).get_attribute('value')

            if 'LOCALIZA' in fornecedor:
                checkFornecedor = 'OK'
            else:
                checkFornecedor = 'NOK'
            StatusRPA = 'Iniciando validação de diária'
            xpath = '//*[@id="ctl00_ContentPlaceHolder1_txtDiaria"]'
            diaria = driver.find_element_by_xpath(xpath).get_attribute('value')


            if float(diariaValorLiq) == float(diaria):
                checkDiaria = 'OK'
            elif float(diariaValorLiq) < float(diaria):
                checkDiaria = 'OK'
            else:
                checkDiaria = 'NOK'

            if float(somaArray) > float(taxaDeAluguel):
                checkTaxas = 'NOK'
            else:
                checkTaxas = 'OK'

            StatusRPA = 'Alterando valores diária'
            xpath = '//*[@id="ctl00_ContentPlaceHolder1_txtDiaria"]'
            driver.find_element_by_xpath(xpath).clear()
            driver.find_element_by_xpath(xpath).send_keys(diariaValorTotal)

            StatusRPA = 'Alterando valores taxaEmReais'
            xpath = '//*[@id="ctl00_ContentPlaceHolder1_txtTaxas"]'
            driver.find_element_by_xpath(xpath).clear()
            driver.find_element_by_xpath(xpath).send_keys(taxaDeAluguel)

            StatusRPA = 'Alterando valores extras'
            xpath = '//*[@id="ctl00_ContentPlaceHolder1_txtExtras"]'
            driver.find_element_by_xpath(xpath).clear()
            driver.find_element_by_xpath(xpath).send_keys(str(somaExtra) + '0')

            StatusRPA = 'Alterando data de emissão'
            xpath = '//*[@id="ctl00_ContentPlaceHolder1_txtEmissaoTKT"]'
            driver.find_element_by_xpath(xpath).clear()
            driver.find_element_by_xpath(xpath).send_keys(dataHoje)

            StatusRPA = 'Alterando valores NrWk'
            xpath = '//*[@id="ctl00_ContentPlaceHolder1_txtNrWorkflow"]'
            driver.find_element_by_xpath(xpath).clear()
            driver.find_element_by_xpath(xpath).send_keys(id)

            StatusRPA = 'Alterando data de nota fiscal'
            xpath = '//*[@id="ctl00_ContentPlaceHolder1_txtDataNotaFiscal"]'
            driver.find_element_by_xpath(xpath).click()
            sleep(5)
            driver.find_element_by_xpath(xpath).send_keys(data_boleto)

            StatusRPA = 'Alterando vencimento de boleto'
            xpath = '//*[@id="ctl00_ContentPlaceHolder1_txtDATA_SUP"]'
            driver.find_element_by_xpath(xpath).clear()
            driver.find_element_by_xpath(xpath).send_keys(data_vencimento_boleto)

            StatusRPA = 'Alterando número de documento'
            xpath = '//*[@id="ctl00_ContentPlaceHolder1_txtNumFaturaHotel"]'
            driver.find_element_by_xpath(xpath).clear()
            driver.find_element_by_xpath(xpath).send_keys(num_doc)

            StatusRPA = 'Alterando valores de comissão'
            xpath = '//*[@id="ctl00_ContentPlaceHolder1_txtTOTCOMNOR"]'
            driver.find_element_by_xpath(xpath).clear()
            driver.find_element_by_xpath(xpath).send_keys(descontoInco)

            StatusRPA = 'Iniciando validação de Tarifa'
            xpath = '//*[@id="ctl00_ContentPlaceHolder1_lblTOTALPNR"]'
            tarifaTaxas = driver.find_element_by_xpath(xpath).get_attribute('innerText')

            if totalGasto == tarifaTaxas:
                chechTarifa = 'OK'
            else:
                chechTarifa = 'NOK'

            StatusRPA = 'Concluído'
            statusProcesso = 'Concluído'
            conn = pymssql.connect(server=GC.server, user=GC.user, password=GC.password, database=GC.database)
            cursor = conn.cursor()
            update = f'''UPDATE INFORMACOES_RESERVA_COCKPIT SET 
                        analiseCheckIn = '{checkDatas}',
                        analiseFornecedor = '{checkFornecedor}',
                        analiseDiaria = '{checkDiaria}',
                        analiseNomes = '{checkNomes}',
                        analiseTaxa = '{checkTaxas}',
                        analiseTarifa = '{chechTarifa}',
                        statusRPA = '{StatusRPA}',
                        startRPA = '1',
                        ATIVIDADE = '{statusProcesso}'

                        WHERE ID_RESERVA = {id}'''

            print(update)
            cursor.execute(update)
            conn.commit()
            driver.close()
            conn.close()


    buscaReserva(reserva, id)






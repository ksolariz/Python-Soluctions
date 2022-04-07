from datetime import date, datetime
from time import sleep
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
import sys
import pymssql
#from inserts import update_relatorio
import globalConfig as GC


"""Download do relatorio no site da seguradora Massas"""
    
def dayrange():
    now = datetime.now()
    t = now.strftime("%d/%m/%Y")
    d =now.strftime("01/%m/%Y")
    return ([t,d])

#GUARDA O CAMINHO DO RELATÓRIO
caminho_pdf = GC.caminho_extrato_global    
#print(caminho_relatorio)



#GUARDA NOME DA SEGURADORA PARA PODER USAR NO INSERT PADRÃO
seguradora = 'Massas'

def massas():
    dataini = datetime.now()
    
   

    #acessa as configs do chrome driver
    chrome_options = Options()
    chrome_options.add_experimental_option("prefs", {
    "download.default_directory": caminho_pdf,
    "download.prompt_for_download": False, "plugins.always_open_pdf_externally": True
    })
    #coloca extensão no chromedriver    
    chrome_options.add_extension(GC.extensao_quiver)

    #especificar onde esta o chromedriver para ser executado
    driver = webdriver.Chrome(options=chrome_options, executable_path =GC.chrome_driver)
    
    def click(xpath):
        driver.find_element_by_xpath(xpath).click()
        sleep(4)
    def sendKey(xpath, value):
        driver.find_element_by_xpath(xpath).send_keys(value)
        sleep(4)
    def send_keys(xpath, value):
        driver.find_element(By.XPATH,xpath).send_keys(value)

    def existe(xpath):
        try:
                driver.find_element(By.XPATH,xpath);
                return 1
        except:
                return 2

    conn = pymssql.connect(server=GC.server, user=GC.user, password=GC.password, database=GC.database)
    cursor = conn.cursor()

    try:
        select_cocorretor = f'''select distinct partner,regional from USERS_PARTNER'''
        cursor.execute(select_cocorretor)
        listaLoop = cursor.fetchall()
        #print(listaLoop)
    except:
        print('Erro select Partnet e Regional')


    location = GC.Quiver #- Financeiro 3
    driver.get(location)
    sleep(5)
    driver.maximize_window()

    driver.execute_script("SelecionaModuloJQuery('FrmPortal.aspx?pagina=Cocorretagem','CO_CORRETAGEM','Professional','CO_CORRETAGEM','Co-corretagem');")
    sleep(3)
    driver.execute_script("SelecionaModuloJQuery('Fast/FrmAjax.aspx?pagina=BaixaComissoes&PARAM=4','CO_CORRETAGEM_BAIXACOMISSOES','Professional','CO_CORRETAGEM_BAIXACOMISSOES','Baixa de Comissões'); ")
    
    mudaFrameInicio = 0
    mudaFrameSeg = 0
    try:
        driver.switch_to.frame('ZonaInterna')
        sleep(1)
    except:
        pass

    nivel = '/html/body/form/div[5]/div/div[2]/div[1]/div/div/div[2]/div[1]/div[1]/div/span/span[1]/span/span[1]'
    click(nivel)
    sleep(1)
    corretora = '/html/body/span[2]/span/span[2]/ul/li[2]'
    click(corretora)
    sleep(1)

    #VARIAVEL ESTÁ SENDO USADA PARA VALIDAR EXCLUSIVAMENTE A REPETIÇÃO DA VIGENCIA LÁ EM BAIXO
    insere_vigencia = 0
    
    
    
    for x in range(0,len(listaLoop)):
    
        if mudaFrameSeg == 1:
                driver.switch_to.default_content()
                print('Entrou na ZonaInterna Inicio')
                driver.switch_to.frame('ZonaInterna')
                sleep(1)

        #Retorna uma lista com um array
        #No loop ele vai escolhendo as listas que contém o cocorretor e a divisão a ser inserida.
        listaTupla = listaLoop[x]
        cocorretor = listaTupla[0]
        divisao = listaTupla[1]
        print(divisao)
        print(cocorretor)

        click_divisao_producao='/html/body/form/div[5]/div/div[2]/div[1]/div/div/div[2]/div[1]/div[2]/div/span/span[1]/span/span[1]'
        click(click_divisao_producao)
        sleep(1)
        campo_divisao_producao='/html/body/span[2]/span/span[1]/input'

        send_keys(campo_divisao_producao,divisao)
        sleep(2)
        driver.find_element(By.XPATH,campo_divisao_producao).send_keys(Keys.DOWN)
        driver.find_element(By.XPATH,campo_divisao_producao).send_keys(Keys.ENTER)
        sleep(1)
        click_cocorretor='/html/body/form/div[5]/div/div[2]/div[1]/div/div/div[2]/div[2]/div[1]/div/div/span/span[1]/span/span[1]'
        click(click_cocorretor)
        sleep(1)
        
     
        
        campo_cocorretor='/html/body/span[2]/span/span[1]/input'
        cocorretor = cocorretor.split(" ")
        cocorretor = cocorretor[0]
        if 'RR' in cocorretor:
            send_keys(campo_cocorretor,'RR')
            send_keys(campo_cocorretor,' PARCERIA')
        else:
            send_keys(campo_cocorretor,cocorretor)
        sleep(2)
        driver.find_element(By.XPATH,campo_cocorretor).send_keys(Keys.DOWN)
        driver.find_element(By.XPATH,campo_cocorretor).send_keys(Keys.ENTER)
        print(x)
        try:
            conn = pymssql.connect(server=GC.server, user=GC.user, password=GC.password, database=GC.database)
            cursor = conn.cursor()
            select_seguradora = f''' 
                select distinct seguradora from [FINANCEIRO_3_ARQUIVOS_EXTRATOS_COMISSAO] where status_ocr=1
                
                 '''
            cursor.execute(select_seguradora)
            lista = cursor.fetchall()
        except:
            print('Erro ao selecionar as seguradoras')
            
        entra_zona_interna=0
        for z in range(0,len(lista)):

            if mudaFrameSeg == 1:
                driver.switch_to.default_content()
                print('Entrou na ZonaInterna Seg')
                driver.switch_to.frame('ZonaInterna')
                sleep(1)
            
            seguradora = lista[z]
            seguradora= seguradora[0]
            print(seguradora)
            if seguradora == 'BERKLEY INTERNATIONAL DO BRASIL SEGUROS S/A':
                seguradora = 'BERKLEY'

            click_seguradora='/html/body/form/div[5]/div/div[2]/div[1]/div/div/div[2]/div[2]/div[2]/div/span/span[1]/span/span[1]'
            click(click_seguradora)
            sleep(1)
            campo_seguradora='/html/body/span[2]/span/span[1]/input'
            try:
                seguradora = seguradora.split(" ")
                seguradora = seguradora[0]+' '+seguradora[1]
            except:
                pass
            send_keys(campo_seguradora,seguradora)
            sleep(2)
            driver.find_element(By.XPATH,campo_cocorretor).send_keys(Keys.DOWN)
            driver.find_element(By.XPATH,campo_cocorretor).send_keys(Keys.ENTER)
            sleep(2)
            
            #ESSA VALIDAÇÃO É PARA ELE COLOCAR A VIGÊNCIA APENAS UMA VEZ JÁ QUE SEMPRE IRÁ SER IGUAL APÓS SER INSERIDA NESSA DETERMINADA CONSULTA
            
            if insere_vigencia == 0:
                date = datetime.now()
                year = date.strftime("%Y")
                month = date.strftime("%m")
                day = date.strftime("%d")
                print(f"Current Year -> {year}")
                sleep(5)
                primeiro_janeiro = '01/01/'+year
                print(primeiro_janeiro)
                inicio_periodo = '/html/body/form/div[5]/div/div[2]/div[1]/div/div/div[2]/div[4]/div[1]/div/div/input'
                driver.find_element(By.XPATH,inicio_periodo).clear()
                sleep(5)
                sendKey(inicio_periodo,primeiro_janeiro)
                sleep(5)
                final_periodo = '/html/body/form/div[5]/div/div[2]/div[1]/div/div/div[2]/div[4]/div[2]/div/div/input'
                driver.find_element(By.XPATH,final_periodo).clear()
                sleep(1)
                sendKey(final_periodo,day+'/'+month+'/'+year)
                insere_vigencia = 1
            

            sleep(2)

            xpath_rodar_baixa='/html/body/form/div[5]/div/div[2]/div[2]/div/div/input[2]'
            click(xpath_rodar_baixa)

            sleep(2)
            mudaFrameSeg = 1
            mudaFrameInicio = 1
            driver.switch_to.default_content()
            xpath_ok_popup='/html/body/div[3]/div/div[3]/button[1]'
            click(xpath_ok_popup)
            
            
    driver.quit()
            

massas()

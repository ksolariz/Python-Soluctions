
from datetime import date, datetime
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
import sys
import pymssql
from Inserts import update_relatorio
import globalConfig as GC

"""Download do relatorio no site da seguradora Zurich"""
    
def dayrange():
    now = datetime.now()
    t = now.strftime("%d/%m/%Y")
    d =now.strftime("01/%m/%Y")
    return ([t,d])

#GUARDA O CAMINHO DO RELATÓRIO
caminho_pdf = GC.caminho_pdf_global    
#print(caminho_relatorio)

conn = pymssql.connect(server=GC.server, user=GC.user, password=GC.password, database=GC.database)
cursor = conn.cursor()

#GUARDA NOME DA SEGURADORA PARA PODER USAR NO INSERT PADRÃO
seguradora = 'Zurich'



def rpa_pdf_zurich(id_dados):
    dataini = datetime.now()
    try:
        try:
            select_dados = f'''select id_dados, cnpj_cpf, tipo_documento,corretora from dados_relatorios_apolice where id_dados = {id_dados}  '''
            cursor.execute(select_dados)
            row = cursor.fetchone()
            #print(row)

            id_pdf = row[0]
            cnpjCpf = row[1]
            tipoDocumento = row[2]
            corretora = row[3]

        except:
            print('erro')
            
        print(id_pdf)
        print(cnpjCpf)
        print(corretora)
        
        
        login_depara = ''
        if corretora == 'LAZAM-MDS BLUMENAU':
            login_depara = 'ZURICH - LAZAM BNU - 170655'
            
        elif corretora == 'LAZAM-MDS CAMPINAS':
            login_depara = 'ZURICH - LAZAM SP - 544535'
            
        elif corretora == 'LAZAM-MDS CURITIBA':
            login_depara = 'ZURICH - LAZAM CTBA - 411001'
            
        elif corretora == 'LAZAM-MDS JARAGUA DO SUL':
            login_depara == 'ZURICH - LAZAM BNU - 170655'
            
        elif corretora == 'LAZAM-MDS JOINVILLE':
            login_depara == 'ZURICH - LAZAM JVL - 170815'
            
        elif corretora == 'MDS-MG':
            login_depara = 'ZURICH - LAZAM MG - 660707'
        
        elif corretora == 'LAZAM-MDS PORTO ALEGRE':
            login_depara = 'ZURICH - LAZAM POA - 432025'
            
        elif corretora == 'LAZAM-MDS REFICE':
            login_depara = 'ZURICH - LAZAM SSA - 290254'
            
        elif corretora == 'LAZAM-MDS RIO DE JANEIRO':
            login_depara = 'ZURICH - LAZAM RJ - 342019'
            
        elif corretora == 'LAZAM-MDS SALVADOR':
            login_depara = 'ZURICH - LAZAM SSA - 290254'
            
        elif corretora == 'LAZAM-MDS COR E ADM DE':
            login_depara = 'ZURICH - LAZAM SP - 544535'
        
        print(login_depara)
        
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
            time.sleep(2)
        def sendKey(xpath, value):
            driver.find_element_by_xpath(xpath).send_keys(value)
            time.sleep(2)

        #faz login site da quiver
        location = GC.Quiver #- renovacao automatica
        driver.get(location)
        time.sleep(5)
        
        driver.maximize_window()

        statusErro = 'Erro - Link/Modal'

        # MODAL DE SEGURADORAS
        driver.execute_script("janelaForm('Links', 530, 660, '../Fast/FrmAjax.aspx?pagina=LinksExternos&Tipo=Menu&IDSESSAO=' + GetIdSessao());")
        time.sleep(2)

        # OPÇÃO DA SEGURADORA  
        driver.switch_to.frame('LinksExternos')
        driver.find_element_by_partial_link_text('ZURICH - LAZAM BNU - 170655').click() 
        time.sleep(10)
        
        statusErro = 'Erro - Login'

        driver.switch_to.default_content()

        driver.switch_to.window(driver.window_handles [ 1 ])

        driver.get('https://espacoparceiros.zurich.com.br/ApoliceCorretor')
        time.sleep(2)
        
        xpath = '/html/body/main/div[6]/div[2]/form/table/tbody/tr[4]/td/div/label/input'
        sendKey(xpath, cnpjCpf)
        time.sleep(2)
        
        driver.find_element(By.NAME,'txtCpfCnpj').click()
        time.sleep(5)
        
        xpath = '/html/body/main/div[6]/div[2]/form/div/div/button'
        click(xpath)
        time.sleep(5)

        try:
            resultFrase = '/html/body/main/div[6]/div[3]/div[1]/div/p'
            result = driver.find_element(By.XPATH,resultFrase)
            
            if result:
                statusErro = 'Documento Não Encontrado'             
        except:
            pass
        
        if statusErro == 'Documento Não Encontrado':
            print('Entrei no if de repeticao')
                    
            lista_depara = ['ZURICH - LAZAM BNU - 170655','ZURICH - LAZAM SP - 544535','ZURICH - LAZAM CTBA - 411001','ZURICH - LAZAM BNU - 170655','ZURICH - LAZAM JVL - 170815','ZURICH - LAZAM MG - 660707','ZURICH - LAZAM POA - 432025','ZURICH - LAZAM SSA - 290254','ZURICH - LAZAM RJ - 342019','ZURICH - LAZAM SSA - 290254','ZURICH - LAZAM SP - 544535']
            
            tamanho_depara = len(lista_depara)
            updateParam = f''' update dados_relatorios_apolice  set param_evidencia = 1
                                where id_dados = {id_dados}'''
            cursor.execute(updateParam)
            conn.commit()  
            for x in range(tamanho_depara):
                
                if login_depara == lista_depara[x]:
                    x = x+1
                    
                if x > tamanho_depara:
                    break
                    
                driver.switch_to_window(driver.window_handles[1])
                driver.close()
                driver.switch_to_window(driver.window_handles[0])
        
                # OPÇÃO DA SEGURADORA  
                driver.switch_to.frame('LinksExternos')
                print(lista_depara[x])
                driver.find_element_by_partial_link_text(lista_depara[x]).click() 
                time.sleep(10)
                statusErro = 'Erro - Login'

                driver.switch_to.default_content()

                driver.switch_to.window(driver.window_handles [ 1 ])

                driver.get('https://espacoparceiros.zurich.com.br/ApoliceCorretor')
                time.sleep(2)
                
                xpath = '/html/body/main/div[6]/div[2]/form/table/tbody/tr[4]/td/div/label/input'
                sendKey(xpath, cnpjCpf)
                time.sleep(2)
                
                driver.find_element(By.NAME,'txtCpfCnpj').click()
                time.sleep(5)
                
                xpath = '/html/body/main/div[6]/div[2]/form/div/div/button'
                click(xpath)
                time.sleep(5)
                
                data_atual = date.today()
                
                
                try:
                    resultFrase = '/html/body/main/div[6]/div[3]/div[1]/div/p'
                    result = driver.find_element(By.XPATH,resultFrase)
                    
                    if result:
                        statusErro = 'Documento Não Encontrado'
                        path_to_save =   'Evidencia-' +str(id_dados)+ '-Baixa_Apolice_Endosso-'+str(data_atual)+'-N-'+(str(x))+'.png'
                        driver.save_screenshot(GC.caminho_evidencia + path_to_save)
                        insertLoop = f'''INSERT INTO backlog_evidencias_apolice(id_dados,login,corretora,evidencia) values({id_dados},'{lista_depara[x]}','{corretora}','{path_to_save}')  '''           
                        cursor.execute(insertLoop)
                        conn.commit()  
                    
                except:
                    pass
                    break
        
        xpath = '/html/body/main/div[6]/div[3]/div[2]/div/div/div[1]/table/tbody/tr/td[1]/a'
        click(xpath)
        time.sleep(5)
        
        xpath = '/html/body/main/div[6]/div[5]/div/div/header/ul/li[1]/a'
        click(xpath)
        time.sleep(10)

        statusErro = 'Baixou pdf com sucesso'

        update_relatorio(driver, dataini,id_dados, statusErro)
    except:
        pass
        update_relatorio(driver, dataini,id_dados, statusErro)

#rpa_pdf_zurich(1046)

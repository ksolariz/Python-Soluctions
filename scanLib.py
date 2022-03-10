import re
from datetime import datetime, date


#Procura a palavra 'textA' dentro do 'text', ignora as 'ignore' ocorrências
#Em seguida, pula as 'jump' linhas e para no delimitador 'deli'
def find(text, textA, deli, ignore=0, jump=0): 

    textA = text.split(textA)
    

    textA = textA[1+ignore].split('\n')
    
    textA = textA[jump]
    
    textA = textA.split(deli)
    
    textA = textA[0]

    print(textA)
    return textA

#Conta o numero de linhas de 'textA' até 'deli' ignorando as 'ignore' ocorrências
#reduzindo as 'reduce' qtd de linhas
def count(text, textA, deli, ignore=0, reduce=0): 

    textA = text.split(textA)

    textA = textA[1+ignore].split(deli)
    textA = textA[0].split('\n')
    print(len(textA) - reduce)
    return(len(textA)-reduce)


def cpfcnpj(string):
    string = string.replace('.', '').replace('-','').replace('/','')
    if len(string) <14:
        newstring = string[:3] + '.'+string[3:6] + '.'+string[6:9]+ '-'+string[-2:]
    else:
        newstring = string[:2] + '.'+string[2:5] + '.'+string[5:8]+ '/'+string[-6:-2]+'-'+string[-2:]
    print(newstring)


def removeText(string):
    string = re.findall('\d+', string)
    string = ''.join(string)
    return(string)

def sumAllnumbers(string):
    string = re.findall('\d+', string)
    string = [int(x) for x in string]
    string = sum(string)
    return(string)


def today():
    return datetime.date.today().strftime('%d/%m/%Y')

#String =  texto de linha retornado
#Deli = delimitador
#Offset = a partir do delimitador quantos números irá para qual lado ?
#Posicao = Qual posição do array criado você quer ?
#Space = Espaço

def splitInLine(string,deli,offset=0,posicao=0,space=' '):
    var = []
    length = ''
    for x in range(0,len(string)):
        if string[x] == deli:
            var.append(x + offset)
    y = 0
    for x in range(0,len(string)):
        length = "".join((length,string[x]))
        try:
            if x == var[y]:
                length = "".join((length,space))
                y = y+1
        except:
            pass

    zoro = length.split(space)
    if posicao == -1:
        posicao = len(zoro)-1
        return zoro[posicao].strip()
    return zoro[posicao].strip()

  #Pega todo o texto entre textA e textb
def gettext(text, textA, textb): 

    textA = text.split(textA)

    textA = textA[1]
    textA = textA.split(textb)
    textA = textA[0]

    print(textA)
    return textA   

def charSelect(text, textA,split,less=0): 

    textA = text.split(textA)

    textA = textA[0]
    textA = textA.split(split)
    print(textA)
    
    length = (len(textA))
    textA = (textA[length - int(less)])
    print(textA)

    return textA
    
def capitalizeString(string,split):
    string = string.split(split)
    tamanho = len(string)
    y = 0
    element = []
    for y in range(0,tamanho):
        slice = string[y].capitalize()
        element.append(slice)
        nome = ' '.join(element) 
    print(nome)
    return nome 

def findNumber(text):
    string = ""
    for n in text:
        if n.isdigit():
            string = string + n
    print(string)
    return string

def convertMonthNameToNumber(string,alg=''):
    string = string.lower()
    if 'janeiro' in string:
        string = string.replace('janeiro',f'{alg}1')
    elif 'fevereiro' in string:
        string = string.replace('feveiro',f'{alg}2')
    elif 'março' in string:
        string = string.replace('março',f'{alg}3')
    elif 'abril' in string:
        string = string.replace('abril',f'{alg}4')
    elif 'maio' in string:
        string = string.replace('maio',f'{alg}5')
    elif 'junho' in string:
        string = string.replace('junho',f'{alg}6')
    elif 'julho' in string:
        string = string.replace('julho',f'{alg}7')
    elif 'agosto' in string:
        string = string.replace('agosto',f'{alg}8')
    elif 'setembro' in string:
        string = string.replace('setembro',f'{alg}9')
    elif 'outubro' in string:
        string = string.replace('outubro','10')
    elif 'novembro' in string:
        string = string.replace('novembro','11')
    else:
        string = string.replace('dezembro','12')
    print(string)
    return string

def findUP(text,deli,reduce=2):
    string = text.split(deli) 
    string = string[0]
    string = string.split('\n')
    string = string[- reduce] 
    print(string)
    return string

def calculateAge(born):



    today = date.today() 
    try:
        birthday = born.replace(year = today.year) 

    except ValueError:
        birthday = born.replace(year = today.year, 
                  month = born.month + 1, day = 1) 

    if birthday > today: 
        return today.year - born.year - 1
    else: 
        return today.year - born.year

def calculaIdade(data):


    data = data.split('/')

    dia = int(data[0])
    mes = int(data[1])
    ano = int(data[2])

    idade = calculateAge(date(ano,mes,dia))
    return idade

def sprint(text,deli):
    text = text.split(deli)
    print(text)
    return text

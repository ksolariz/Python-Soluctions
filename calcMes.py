from datetime import datetime, date
from dateutil.relativedelta import relativedelta
import calendar

def busca_mes_atual():
    dataAtual = date.today()
    valida = dataAtual.strftime("%d/%m/%Y")
    valida = valida.split('/')
    ultimoDia = calendar._monthlen(int(valida[2]), int(valida[1]))
    d = dataAtual.strftime(str(ultimoDia)+"/%m/%Y")
    t = dataAtual.strftime("01/%m/%Y")
    return ([t,d])

def busca_mes_anterior():
    dataAtual = date.today()
    t = dataAtual + relativedelta(months=-1)
    d = dataAtual + relativedelta(months=-1)
    valida = d.strftime("%d/%m/%Y")
    valida = valida.split('/')
    ultimoDia = calendar._monthlen(int(valida[2]), int(valida[1]))
    d = d.strftime(str(ultimoDia)+"/%m/%Y")
    t = t.strftime("01/%m/%Y")
    return([t,d])


def broke_date(date):
    brokenDate = date.split('/')
    return(brokenDate)

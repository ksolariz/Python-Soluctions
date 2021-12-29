import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email.mime.image import MIMEImage
from email.mime.audio import MIMEAudio
from email import encoders


def enviarEmail():
    host = "smtp.gmail.com"
    port = "587"
    login = "login de quem envia o email"
    senha = "senha do email"
    server = smtplib.SMTP(host,port)
    server.ehlo()
    server.starttls()
    server.login(login,senha)

    corpo = f'''
    <p>CORPO DO EMAIL EM HTML<p>
    '''
    

    email_msg = MIMEMultipart()
    email_msg['From'] = login
    email_msg['Subject'] = "ASSUNTO DO EMAIL"
    email_msg.attach(MIMEText(corpo,'html'))

    #Email da pessoa que está configurada pra enviar
    from_email = 'email de quem envia'

    #Email de quem irá ser posto em cópia
    copy = ['exemplo1@gmail.com', 'exemplo1@gmail.com']

    email_msg['From'] = from_email
    email_msg['To'] = ", ".join(copy)

    
    
    #Põem esse primeiro arquivo em anexo
    file = "caminho do arquivo que irá ser posto em anexo"
    filename = 'nome do arquivo que irá ser posto em anexo'
    attachment = open(file,'rb')
    att = MIMEBase('application','octet-stream')
    att.set_payload(attachment.read())
    encoders.encode_base64(att)
    att.add_header('Content-Disposition', f'attachment; filename={filename}')
    email_msg.attach(att)
    #OBS: SE QUISER POR MAIS DE UM ARQUIVO APENAS REPITA ESTE PROCESSO.
   
    server.sendmail(from_email, copy, email_msg.as_string())

    print('Email enviado')
    server.quit()

enviarEmail()

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import streamlit as st

def enviar_email(email_dest, assunto, corpo):
    smtp_server = "smtp.gmail.com"
    smtp_port = 587
    remetente = st.secrets["email"]["sender"]
    senha = st.secrets["email"]["password"]

    msg = MIMEMultipart()
    msg['From'] = remetente
    msg['To'] = email_dest
    msg['Subject'] = assunto
    msg.attach(MIMEText(corpo, 'plain'))

    with smtplib.SMTP(smtp_server, smtp_port) as server:
        server.starttls()
        server.login(remetente, senha)
        server.send_message(msg)
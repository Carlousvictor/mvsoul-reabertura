import gspread
import pandas as pd
from oauth2client.service_account import ServiceAccountCredentials
from datetime import datetime
import streamlit as st

def _abrir_planilha():
    scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
    creds_dict = st.secrets["google"]
    creds = ServiceAccountCredentials.from_json_keyfile_dict(creds_dict, scope)
    client = gspread.authorize(creds)
    sheet = client.open("Solicitações_Reabertura_MVSoul").sheet1
    return sheet

def gravar_solicitacao(nome, email, unidade, setor, data, periodo, justificativa, anexo):
    sheet = _abrir_planilha()
    linha = [datetime.now().strftime("%d/%m/%Y %H:%M:%S"), nome, email, unidade, setor, str(data),
             periodo, justificativa, anexo, "Pendente", "", ""]
    sheet.append_row(linha)

def atualizar_status(index, status):
    sheet = _abrir_planilha()
    cell = f"J{index + 2}"  # Coluna J = Status
    sheet.update_acell(cell, status)

def carregar_solicitacoes():
    sheet = _abrir_planilha()
    data = sheet.get_all_records()
    return pd.DataFrame(data)
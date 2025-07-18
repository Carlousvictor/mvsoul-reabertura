import streamlit as st
from utils_email import enviar_email
from utils_google import gravar_solicitacao, atualizar_status, carregar_solicitacoes
from datetime import datetime

st.set_page_config(page_title="Solicitação de Reabertura - MV Soul", layout="centered")

menu = st.sidebar.selectbox("Menu", ["Nova Solicitação", "Painel da Contabilidade", "Confirmação de Correção"])

if menu == "Nova Solicitação":
    st.title("📄 Solicitação de Reabertura de Mês no MV Soul")
    with st.form("formulario_solicitacao"):
        nome = st.text_input("Solicitante")
        email = st.text_input("E-mail do Solicitante")
        unidade = st.text_input("Unidade Solicitante")
        setor = st.text_input("Setor Responsável")
        data_solicitacao = st.date_input("Data da Solicitação", value=datetime.today())
        periodo = st.text_input("Período a ser Reaberto (ex: 06/2025)")
        justificativa = st.text_area("Justificativa Detalhada")
        doc = st.file_uploader("Anexo de Documento (opcional)", type=["pdf", "jpg", "png", "docx"])
        submitted = st.form_submit_button("Enviar Solicitação")

        if submitted:
            link_anexo = ""  # Ex: poderia fazer upload externo aqui
            gravar_solicitacao(nome, email, unidade, setor, data_solicitacao, periodo, justificativa, link_anexo)
            enviar_email(email_dest="gestao_mxm@grupohospitalcasa.com.br",
                         assunto="Nova Solicitação de Reabertura",
                         corpo=f"Solicitação enviada por {nome} ({email}) referente ao período {periodo}.")
            st.success("Solicitação enviada com sucesso!")

elif menu == "Painel da Contabilidade":
    st.title("✅ Painel da Contabilidade")
    dados = carregar_solicitacoes()
    for idx, row in dados.iterrows():
        with st.expander(f"{row['Solicitante']} | {row['Período']} | Status: {row['Status']}"):
            st.write("Justificativa:", row['Justificativa'])
            col1, col2 = st.columns(2)
            if col1.button("✅ Aprovar", key=f"ap{idx}"):
                atualizar_status(idx, "Aprovado")
                enviar_email(row['E-mail'], "Solicitação Aprovada",
                             f"Sua solicitação do período {row['Período']} foi aprovada. Finalize a correção e confirme no link abaixo.")
                st.success("Aprovado.")
            if col2.button("❌ Reprovar", key=f"rp{idx}"):
                atualizar_status(idx, "Reprovado")
                enviar_email(row['E-mail'], "Solicitação Reprovada",
                             f"Sua solicitação do período {row['Período']} foi reprovada.")
                st.warning("Reprovado.")

elif menu == "Confirmação de Correção":
    st.title("📌 Confirmação de Correção Realizada")
    email = st.text_input("Seu e-mail usado na solicitação")
    periodo = st.text_input("Período corrigido (ex: 06/2025)")
    confirmar = st.button("Confirmar correção")
    if confirmar:
        enviar_email("gestao_mxm@grupohospitalcasa.com.br",
                     "Correção Finalizada",
                     f"{email} confirmou que a correção do período {periodo} foi realizada.")
        st.success("Correção confirmada e notificação enviada!")
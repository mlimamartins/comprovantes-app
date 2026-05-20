import streamlit as st
import os
from datetime import date


# Configurações da página

st.set_page_config(
    page_title="Sistema de Comprovantes",
    page_icon="📄",
    layout="centered"
)

# Criação da pasta uploads

PASTA_UPLOADS = "Uploads"

os.makedirs(PASTA_UPLOADS, exist_ok=True)

# Título

st.title("📄 Sistema de Comprovantes")

st.write("Envie e organize seus comprovantes aqui")


# Formulário

with st.form("form_comprovante"):

    arquivo = st.file_uploader(
        "Escolha um comprovante", 
        type=["pdf", "jpg", "jpeg", "png"]
    )

    descricao = st.text_input(
        "Descrição do comprovante",
        max_chars=100
    )

    data_vencimento = st.date_input(
        "Data de vencimento"
    )

    data_pagamento = st.date_input(
        "Data de pagamento"
    )

    botao_salvar = st.form_submit_button(
        "Salvar comprovante"
    )

    # Salvar o arquivo e as informações

    if botao_salvar:

        if arquivo is not None:

            caminho_arquivo = os.path.join(
                PASTA_UPLOADS,
                arquivo.name
            )

            with open (caminho_arquivo, "wb") as f:

                f.write(arquivo.getbuffer())

            st.sucess="Comprovante salvo com sucesso!" 

            st.write(f"Desccrição: {descricao}")

            st.write(f"Data de vencimento: {data_vencimento}")

            st.write(f"Data de pagamento: {data_pagamento}")

        else: 

            st.error("Por favor, selecione um arquivo para upload")


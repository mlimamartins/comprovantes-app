import streamlit as st
import sqlite3
import os
from datetime import date
import pandas as pd


# Configurações da página


st.set_page_config(
    page_title="Comprovantes",
    page_icon="📄"
)

PASTA_UPLOADS = "uploads"

os.makedirs(PASTA_UPLOADS, exist_ok=True)

# Banco de dados


conn = sqlite3.connect("banco.db")

cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS comprovantes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    descricao TEXT,
    data TEXT,
    arquivo TEXT
)
""")

conn.commit()


# Título da aplicação


st.title("📄 Sistema de Comprovantes")

# Formulário de upload

with st.form("formulario"):

    arquivo = st.file_uploader(
        "Comprovante",
        type=["png", "jpg", "jpeg", "pdf"]
    )

    descricao = st.text_input(
        "Descrição"
    )

    data_pagamento = st.date_input(
        "Data",
        value=date.today()
    )

    salvar = st.form_submit_button(
        "Salvar"
    )

# Salvar o comprovante

if salvar:

    if arquivo is not None:

        caminho = os.path.join(
            PASTA_UPLOADS,
            arquivo.name
        )

        with open(caminho, "wb") as f:

            f.write(arquivo.getbuffer())

        cursor.execute("""
        INSERT INTO comprovantes
        (descricao, data, arquivo)
        VALUES (?, ?, ?)
        """, (
            descricao,
            str(data_pagamento),
            arquivo.name
        ))

        conn.commit()

        st.success("Comprovante salvo!")

    else:

        st.error("Envie um arquivo")

# Listar os comprovantes

st.divider()

st.subheader("📋 Comprovantes Salvos")

dados = pd.read_sql_query(
    "SELECT * FROM comprovantes",
    conn
)

st.dataframe(dados)
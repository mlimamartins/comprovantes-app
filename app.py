import streamlit as st
import sqlite3
import pandas as pd
import os
from datetime import date
from PIL import Image
import pytesseract
from pdf2image import convert_from_path
import re
import pytesseract

pytesseract.pytesseract.tesseract_cmd = (
    r"C:\Program Files\Tesseract-OCR\tesseract.exe"
)

# Configurações Iniciais

st.set_page_config(
    page_title="Sistema de Comprovantes",
    page_icon="📄",
    layout="wide"
)

# Pasta para uploads


PASTA_UPLOADS = "uploads"

os.makedirs(PASTA_UPLOADS, exist_ok=True)

# Banco de Dados

conn = sqlite3.connect(
    "banco.db",
    check_same_thread=False
)

cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS comprovantes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    descricao TEXT,
    categoria TEXT,
    data TEXT,
    arquivo TEXT
)
""")

conn.commit()

# Título


st.title("📄 Sistema de Comprovantes")

st.caption(
    "Organize pagamentos, PIX, boletos e recibos"
)
st.sidebar.title("⚙️ Menu")

st.sidebar.info(
    "Sistema de gerenciamento de comprovantes"
)


# Métricas

cursor.execute("""
SELECT COUNT(*) FROM comprovantes
""")

total = cursor.fetchone()[0]

col1, col2 = st.columns(2)

with col1:

    st.metric(
        "Total de comprovantes",
        total
    )

with col2:

    st.metric(
        "Pasta uploads",
        PASTA_UPLOADS
    )

# Função para extrair texto (OCR)

def extrair_texto(caminho_arquivo):

    texto = ""

    extensao = caminho_arquivo.lower()

    try:

    
        # Imagens

        if extensao.endswith(
            (".png", ".jpg", ".jpeg")
        ):

            imagem = Image.open(caminho_arquivo)

            texto = pytesseract.image_to_string(
                imagem,
                lang="por"
            )

        # PDFs

        elif extensao.endswith(".pdf"):

            paginas = convert_from_path(
                caminho_arquivo
            )

            for pagina in paginas:

                texto += pytesseract.image_to_string(
                    pagina,
                    lang="por"
                )

    except Exception as erro:

        texto = f"Erro OCR: {erro}"

    return texto

# =========================
# EXTRAIR VALORES
# =========================

def extrair_valor(texto):

    padrao = r"R\$\s?\d+[.,]\d+"

    resultado = re.findall(
        padrao,
        texto
    )

    if resultado:

        return resultado[0]

    return "Não encontrado"

# Formulário de Upload


with st.form("formulario"):

    arquivo = st.file_uploader(
        "Comprovante",
        type=["png", "jpg", "jpeg", "pdf"]
    )

    descricao = st.text_input(
        "Descrição"
    )

    categoria = st.selectbox(
        "Categoria",
        [
            "Casa",
            "Mercado",
            "Trabalho",
            "Impostos",
            "PIX",
            "Cartão",
            "Outros"
        ]
    )

    data_pagamento = st.date_input(
        "Data",
        value=date.today()
    )

    salvar = st.form_submit_button(
        "Salvar"
    )

# Salvar


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
        (descricao, categoria, data, arquivo)
        VALUES (?, ?, ?, ?)
        """, (
            descricao,
            categoria,
            str(data_pagamento),
            arquivo.name
        ))

        conn.commit()

        st.success("Comprovante salvo!")

        # OCR
        texto_extraido = extrair_texto(
            caminho
        )

        st.subheader("🧠 Texto extraído")

        st.text_area(
            "OCR",
            texto_extraido,
            height=300
        )

        valor_detectado = extrair_valor(
            texto_extraido
        )

        st.success(
            f"💰 Valor detectado: {valor_detectado}"
        )

    else:

        st.error("Envie um arquivo")

# Buscar

st.divider()

st.subheader("🔎 Buscar comprovantes")

col1, col2 = st.columns(2)

with col1:

    busca = st.text_input(
        "🔎 Buscar descrição"
    )

with col2:

    filtro_categoria = st.selectbox(
        "📂 Categoria",
        [
            "Todas",
            "Casa",
            "Mercado",
            "Trabalho",
            "Impostos",
            "PIX",
            "Cartão",
            "Outros"
        ]
    )

# Consultar banco

query = "SELECT * FROM comprovantes WHERE 1=1"

if busca:

    query += f"""
    AND descricao LIKE '%{busca}%'
    """

if filtro_categoria != "Todas":

    query += f"""
    AND categoria = '{filtro_categoria}'
    """

dados = pd.read_sql_query(
    query,
    conn
)


# Listar

st.subheader("📋 Comprovantes")

st.dataframe(
    dados,
    use_container_width=True
)

# Excluir

st.divider()

st.subheader("🗑️ Excluir comprovante")

if not dados.empty:

    id_excluir = st.number_input(
        "Digite o ID",
        min_value=1,
        step=1
    )

    excluir = st.button(
        "Excluir"
    )

    if excluir:

        # Buscar arquivo
        cursor.execute("""
        SELECT arquivo
        FROM comprovantes
        WHERE id = ?
        """, (id_excluir,))

        resultado = cursor.fetchone()

        if resultado:

            nome_arquivo = resultado[0]

            caminho_arquivo = os.path.join(
                PASTA_UPLOADS,
                nome_arquivo
            )

            # Excluir arquivo físico
            if os.path.exists(caminho_arquivo):

                os.remove(caminho_arquivo)

            # Excluir banco
            cursor.execute("""
            DELETE FROM comprovantes
            WHERE id = ?
            """, (id_excluir,))

            conn.commit()

            st.success("Comprovante excluído!")

            st.rerun()

        else:

            st.error("ID não encontrado")

# Visualizar Comprovante

st.divider()

st.subheader("👁️ Visualizar comprovante")

if not dados.empty:

    id_visualizar = st.number_input(
        "Digite o ID do comprovante",
        min_value=1,
        step=1,
        key="visualizar"
    )

    visualizar = st.button(
        "Visualizar"
    )

    if visualizar:

        cursor.execute("""
        SELECT arquivo
        FROM comprovantes
        WHERE id = ?
        """, (id_visualizar,))

        resultado = cursor.fetchone()

        if resultado:

            nome_arquivo = resultado[0]

            caminho = os.path.join(
                PASTA_UPLOADS,
                nome_arquivo
            )

            extensao = nome_arquivo.lower()

            # Imagem
            if extensao.endswith(
                (".png", ".jpg", ".jpeg")
            ):

                imagem = Image.open(caminho)

                st.image(
                    imagem,
                    caption=nome_arquivo,
                    use_container_width=True
                )

            # PDF
            elif extensao.endswith(".pdf"):

                with open(caminho, "rb") as pdf:

                    st.download_button(
                        label="📥 Baixar PDF",
                        data=pdf,
                        file_name=nome_arquivo,
                        mime="application/pdf"
                    )

        else:

            st.error("ID não encontrado")
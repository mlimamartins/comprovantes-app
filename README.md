# 📄 Sistema de Comprovantes

Sistema web desenvolvido com Python + Streamlit para organizar comprovantes de pagamentos, PIX, boletos e recibos.

O projeto permite:

- Upload de comprovantes
- Organização por categoria
- Busca de comprovantes
- Visualização de arquivos
- Exclusão de comprovantes
- Banco de dados SQLite
- Interface web responsiva
- Deploy online com Streamlit Cloud

---

# 🚀 Tecnologias utilizadas

- Python
- Streamlit
- SQLite
- Pandas
- Pillow
- Git & GitHub

---

# 📸 Funcionalidades

## ✅ Upload de comprovantes

Envio de:
- PNG
- JPG
- JPEG
- PDF

---

## ✅ Organização

Os comprovantes podem ser categorizados em:

- Casa
- Mercado
- Trabalho
- Impostos
- PIX
- Cartão
- Outros

---

## ✅ Banco de dados

O sistema utiliza SQLite para armazenar:

- descrição
- categoria
- data
- nome do arquivo

---

## ✅ Busca inteligente

Filtro por:
- descrição
- categoria

---

## ✅ Visualização

- Preview de imagens
- Download de PDFs

---

## ✅ Exclusão

Exclusão completa:
- banco de dados
- arquivo físico

---

# 🗂️ Estrutura do projeto

```bash
comprovantes-app/
│
├── app.py
├── banco.db
├── requirements.txt
├── uploads/
├── .gitignore
└── README.md

import streamlit as st
import pandas as pd
import datetime

PLANILHA_URL = "https://docs.google.com/spreadsheets/d/1OyyByD4qQ6vDupvh4vS3ZMif7qPyBjH_we_ow8LXyG0/gviz/tq?tqx=out:csv"

st.set_page_config(page_title="Sistema Bufunfa", layout="wide")

st.title("💰 Gestão de Reciclagem Bufunfa")
st.subheader("Associação Comunitária São Luiz (ASCOMSL)")

# carregar dados da planilha
try:
    historico = pd.read_csv(PLANILHA_URL)
except:
    historico = pd.DataFrame(columns=["Nome","Aluminio","Oleo","Plastico","Total","Data"])

# barra lateral
with st.sidebar:
    st.header("⚙️ Ajuste de Preços")

    preco_alu = st.number_input("Preço Alumínio (kg)", value=8.0)
    preco_ole = st.number_input("Preço Óleo (litro)", value=2.5)
    preco_pla = st.number_input("Preço Plástico (kg)", value=1.5)

# entrada
st.header("📥 Registrar Coleta")

nome = st.text_input("Nome da Mãe/Doadora")
alu = st.number_input("Alumínio (kg)", min_value=0.0)
oleo = st.number_input("Óleo (litros)", min_value=0.0)
pla = st.number_input("Plástico (kg)", min_value=0.0)

if st.button("Calcular"):

    if nome == "":
        st.error("Digite o nome")

    else:

        total = alu*preco_alu + oleo*preco_ole + pla*preco_pla

        nova_linha = pd.DataFrame([{
            "Nome":nome,
            "Aluminio":alu,
            "Oleo":oleo,
            "Plastico":pla,
            "Total":total,
            "Data":datetime.datetime.now().strftime("%d/%m/%Y %H:%M")
        }])

        historico = pd.concat([historico,nova_linha],ignore_index=True)

        st.success(f"Total a pagar: R$ {total:.2f}")

# mostrar histórico
st.divider()

st.subheader("📊 Histórico de Coletas")

st.dataframe(historico)


import streamlit as st
import pandas as pd
import datetime

# --- CONFIGURAÇÃO ESTRATÉGICA ---
# Substitua pelo link que você copiou da sua planilha (entre as aspas)
LINK_PLANILHA = "https://docs.google.com/spreadsheets/d/1OyyByD4qQ6vDupvh4vS3ZMif7qPyBjH_we_ow8LXyG0/edit?gid=0#gid=0"

st.set_page_config(page_title="Sistema Bufunfa - ASCOMSL", layout="wide")
if "historico" not in st.session_state:
    st.session_state.historico = pd.DataFrame(
        columns=["Nome", "Aluminio", "Oleo", "Plastico", "Total", "Data"]
    )

st.title("💰 Gestão de Reciclagem Bufunfa")
st.subheader("Associação Comunitária São Luiz (ASCOMSL)")

# --- BARRA LATERAL: AJUSTE DE PREÇOS ---
with st.sidebar:
    st.header("⚙️ Ajuste de Preços (R$)")
    preco_alu = st.number_input("Preço Alumínio (kg)", value=8.0, step=0.1)
    preco_ole = st.number_input("Preço Óleo (Litro)", value=2.5, step=0.1)
    preco_pla = st.number_input("Preço Plástico (kg)", value=1.5, step=0.1)
    st.divider()
    st.info("O link da planilha já está configurado internamente por segurança.")

# --- ENTRADA DE DADOS ---
col1, col2 = st.columns(2)

with col1:
    st.header("📥 Registrar Coleta")
    nome_mae = st.text_input("Nome da Mãe/Doadora")
    peso_alu = st.number_input("Peso Alumínio (kg)", min_value=0.0)
    litros_ole = st.number_input("Litros de Óleo", min_value=0.0)
    peso_pla = st.number_input("Peso Plástico (kg)", min_value=0.0)
    
    if st.button("Calcular e Salvar"):

        total = (
        peso_alu * preco_alu +
        litros_ole * preco_ole +
        peso_pla * preco_pla
    )

    nova_linha = {
        "Nome": nome_mae,
        "Aluminio": peso_alu,
        "Oleo": litros_ole,
        "Plastico": peso_pla,
        "Total": total,
        "Data": datetime.datetime.now().strftime("%d/%m/%Y %H:%M")
    }

    st.session_state.historico = pd.concat(
        [st.session_state.historico, pd.DataFrame([nova_linha])],
        ignore_index=True
    )

    st.success(f"Total a pagar: R$ {total:.2f}")
    
st.divider()
st.subheader("📊 Histórico de Coletas")
st.dataframe(st.session_state.historico)

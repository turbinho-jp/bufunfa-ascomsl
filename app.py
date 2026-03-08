import streamlit as st
import pandas as pd
from datetime import datetime

# --- CONFIGURAÇÃO ESTRATÉGICA ---
# Substitua pelo link que você copiou da sua planilha (entre as aspas)
LINK_PLANILHA = "COLE_AQUI_O_LINK_DA_SUA_PLANILHA"

st.set_page_config(page_title="Sistema Bufunfa - ASCOMSL", layout="wide")

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
        if nome_mae:
            # Cálculos
            valor_total = (peso_alu * preco_alu) + (litros_ole * preco_ole) + (peso_pla * preco_pla)
            total_kg = peso_alu + peso_pla + (litros_ole * 0.9)
            arvores = total_kg * 0.05
            data_hoje = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
            
            # Resultado na Tela
            with col2:
                st.header("📊 Recibo Digital")
                st.success(f"Doadora: {nome_mae}")
                st.metric("Total em Bufunfas", f"฿ {valor_total:.2f}")
                st.info(f"🌳 Impacto: {arvores:.3f} árvores salvas.")
                st.balloons()
                
                # Instrução de salvamento (Link direto para facilitar o CSV)
                st.warning("Dados prontos para envio. Clique no link abaixo para abrir a planilha e conferir.")
                st.markdown(f"[Abrir Planilha de Registros]({LINK_PLANILHA})")
        else:
            st.error("Por favor, insira o nome da doadora.")

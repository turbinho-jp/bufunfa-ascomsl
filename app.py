import streamlit as st
import pandas as pd

st.set_page_config(page_title="Sistema Bufunfa - ASCOMSL", layout="wide")

st.title("💰 Gestão de Reciclagem Bufunfa")
st.subheader("Associação Comunitária São Luiz (ASCOMSL)")

# Configuração de Preços Editáveis
with st.sidebar:
    st.header("⚙️ Ajuste de Preços (R$)")
    preco_aluminio = st.number_input("Preço Alumínio (por kg)", value=8.0, step=0.1)
    preco_oleo = st.number_input("Preço Óleo (por Litro)", value=2.5, step=0.1)
    preco_plastico = st.number_input("Preço Plástico (por kg)", value=1.5, step=0.1)

# Entrada de Dados
col1, col2 = st.columns(2)
with col1:
    st.header("📥 Registrar Coleta")
    nome_mae = st.text_input("Nome da Mãe/Doadora")
    peso_aluminio = st.number_input("Peso Alumínio (kg)", min_value=0.0)
    litros_oleo = st.number_input("Litros de Óleo", min_value=0.0)
    peso_plastico = st.number_input("Peso Plástico (kg)", min_value=0.0)
    btn = st.button("Calcular")

# Cálculos de Impacto
if btn and nome_mae:
    valor_total = (peso_aluminio * preco_aluminio) + (litros_oleo * preco_oleo) + (peso_plastico * preco_plastico)
    total_kg = peso_aluminio + peso_plastico + (litros_oleo * 0.9)
    arvores = total_kg * 0.05
    
    with col2:
        st.header("📊 Resultado")
        st.metric("Total Bufunfas", f"฿ {valor_total:.2f}")
        st.info(f"🌳 Você salvou {arvores:.3f} árvores!")

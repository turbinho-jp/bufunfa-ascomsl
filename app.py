import streamlit as st
import pandas as pd
import datetime
import gspread
from google.oauth2.service_account import Credentials

# ========================= CONFIGURAÇÃO =========================
st.set_page_config(page_title="Sistema Bufunfa - ASCOMSL", layout="wide")

LINK_PLANILHA = "https://docs.google.com/spreadsheets/d/1OyyByD4qQ6vDupvh4vS3ZMif7qPyBjH_we_ow8LXyG0/edit?gid=0#gid=0"

# ========================= CONEXÃO COM A PLANILHA (STREAMLIT CLOUD) =========================
@st.cache_resource
def conectar_planilha():
    scope = [
        "https://www.googleapis.com/auth/spreadsheets",
        "https://www.googleapis.com/auth/drive"
    ]
    creds = Credentials.from_service_account_info(
        st.secrets["gspread"], scopes=scope
    )
    client = gspread.authorize(creds)
    return client.open_by_url(LINK_PLANILHA).sheet1

ws = conectar_planilha()

# Carregar histórico da planilha
if "historico" not in st.session_state:
    dados = ws.get_all_records()
    st.session_state.historico = pd.DataFrame(dados)

# ========================= TÍTULO =========================
st.title("💰 Gestão de Reciclagem Bufunfa")
st.subheader("Associação Comunitária São Luiz (ASCOMSL)")

# ========================= BARRA LATERAL =========================
with st.sidebar:
    st.header("⚙️ Ajuste de Preços (R$)")
    preco_alu = st.number_input("Preço Alumínio (kg)", value=8.0, step=0.1)
    preco_ole = st.number_input("Preço Óleo (Litro)", value=2.5, step=0.1)
    preco_pla = st.number_input("Preço Plástico (kg)", value=1.5, step=0.1)
    st.divider()
    if st.button("🔄 Atualizar dados da planilha"):
        dados = ws.get_all_records()
        st.session_state.historico = pd.DataFrame(dados)
        st.success("✅ Dados atualizados!")

# ========================= REGISTRO =========================
col1, col2 = st.columns([2, 1])

with col1:
    st.header("📥 Registrar Coleta")
    nome_mae = st.text_input("Nome da Mãe/Doadora")
    peso_alu = st.number_input("Peso Alumínio (kg)", min_value=0.0)
    litros_ole = st.number_input("Litros de Óleo", min_value=0.0)
    peso_pla = st.number_input("Peso Plástico (kg)", min_value=0.0)

    if st.button("💰 Calcular e Salvar na Planilha", type="primary"):
        if not nome_mae.strip():
            st.error("Por favor, insira o nome da doadora.")
        else:
            total = peso_alu * preco_alu + litros_ole * preco_ole + peso_pla * preco_pla

            # Salva na planilha
            nova_linha = [
                nome_mae,
                peso_alu,
                litros_ole,
                peso_pla,
                total,
                datetime.datetime.now().strftime("%d/%m/%Y %H:%M")
            ]
            ws.append_row(nova_linha)

            # Atualiza o dataframe
            nova_df = pd.DataFrame([{
                "Nome": nome_mae,
                "Aluminio": peso_alu,
                "Oleo": litros_ole,
                "Plastico": peso_pla,
                "Total": total,
                "Data": nova_linha[5]
            }])
            st.session_state.historico = pd.concat([st.session_state.historico, nova_df], ignore_index=True)

            st.success(f"✅ Salvo com sucesso! Total a pagar: **R$ {total:,.2f}**")

with col2:
    st.header("📊 Resumo Geral")
    if not st.session_state.historico.empty:
        total_pago = st.session_state.historico["Total"].sum()
        alu_total = st.session_state.historico["Aluminio"].sum()
        ole_total = st.session_state.historico["Oleo"].sum()
        pla_total = st.session_state.historico["Plastico"].sum()

        st.metric("💰 Total já pago", f"R$ {total_pago:,.2f}")
        st.metric("♻️ Alumínio coletado", f"{alu_total:,.1f} kg")
        st.metric("🛢️ Óleo coletado", f"{ole_total:,.1f} L")
        st.metric("🧴 Plástico coletado", f"{pla_total:,.1f} kg")

# ========================= HISTÓRICO =========================
st.divider()
st.subheader("📋 Histórico de Coletas")

busca = st.text_input("🔍 Buscar por nome da mãe", "")
df_filtrado = st.session_state.historico
if busca:
    df_filtrado = df_filtrado[df_filtrado["Nome"].str.contains(busca, case=False)]

st.dataframe(
    df_filtrado.style.format({
        "Aluminio": "{:.2f} kg",
        "Oleo": "{:.2f} L",
        "Plastico": "{:.2f} kg",
        "Total": "R$ {:.2f}"
    }),
    use_container_width=True,
    hide_index=True
)

if df_filtrado.empty and busca:
    st.info("Nenhum registro encontrado.")

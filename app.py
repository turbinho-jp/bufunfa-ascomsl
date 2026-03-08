import streamlit as st
import pandas as pd
import datetime

st.set_page_config(page_title="Sistema Bufunfa", layout="wide")

st.title("💰 Gestão de Reciclagem Bufunfa")
st.subheader("Associação Comunitária São Luiz (ASCOMSL)")

# ---------------------------
# HISTÓRICO NA MEMÓRIA
# ---------------------------

if "historico" not in st.session_state:
    st.session_state.historico = pd.DataFrame(
        columns=["Nome","Aluminio","Oleo","Plastico","Total","Data"]
    )

# ---------------------------
# BARRA LATERAL (PREÇOS)
# ---------------------------

with st.sidebar:

    st.header("⚙️ Ajuste de Preços")

    preco_alu = st.number_input(
        "Preço Alumínio (kg)",
        min_value=0.0,
        value=8.0
    )

    preco_ole = st.number_input(
        "Preço Óleo (litro)",
        min_value=0.0,
        value=2.5
    )

    preco_pla = st.number_input(
        "Preço Plástico (kg)",
        min_value=0.0,
        value=1.5
    )

# ---------------------------
# REGISTRO DE COLETA
# ---------------------------

st.header("📥 Registrar Coleta")

nome = st.text_input("Nome da Mãe/Doadora")

col1,col2,col3 = st.columns(3)

with col1:
    alu = st.number_input("Alumínio (kg)", min_value=0.0)

with col2:
    oleo = st.number_input("Óleo (litros)", min_value=0.0)

with col3:
    pla = st.number_input("Plástico (kg)", min_value=0.0)

# ---------------------------
# BOTÃO CALCULAR
# ---------------------------

if st.button("💰 Calcular e Registrar"):

    if nome == "":
        st.error("Digite o nome da doadora")

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

        st.session_state.historico = pd.concat(
            [st.session_state.historico, nova_linha],
            ignore_index=True
        )

        st.success(f"Total a pagar: R$ {total:.2f}")

# ---------------------------
# HISTÓRICO
# ---------------------------

st.divider()

st.subheader("📊 Histórico de Coletas")

st.dataframe(
    st.session_state.historico,
    use_container_width=True
)

# ---------------------------
# INDICADORES
# ---------------------------

st.divider()
st.subheader("📊 Indicadores de Reciclagem")

historico = st.session_state.historico

if not historico.empty:

    total_alu = historico["Aluminio"].sum()
    total_oleo = historico["Oleo"].sum()
    total_pla = historico["Plastico"].sum()
    total_pago = historico["Total"].sum()

    col1,col2,col3,col4 = st.columns(4)

    col1.metric("♻️ Alumínio coletado (kg)", round(total_alu,2))
    col2.metric("🛢 Óleo coletado (L)", round(total_oleo,2))
    col3.metric("🧴 Plástico coletado (kg)", round(total_pla,2))
    col4.metric("💰 Total pago (R$)", round(total_pago,2))

    # ---------------------------
    # GRÁFICO
    # ---------------------------

    st.subheader("📈 Materiais Coletados")

    dados = pd.DataFrame({
        "Material":["Alumínio","Óleo","Plástico"],
        "Quantidade":[total_alu,total_oleo,total_pla]
    })

    st.bar_chart(
        dados.set_index("Material"),
        use_container_width=True
    )

else:

    st.info("Nenhuma coleta registrada ainda.")

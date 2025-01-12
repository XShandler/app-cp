import pandas as pd
import altair as alt
import streamlit as st

# ==============================
# Configuração do Streamlit
# ==============================
st.set_page_config(page_title="Dashboard Interativo", layout="wide")

# ==============================
# Carregar Dados
# ==============================
@st.cache_data
def load_data():
    try:
        url = 'https://docs.google.com/spreadsheets/d/1RNg8r47qq1SjgpRXlReeR0Vp4U9lE_urklVIh8upzOo/export?format=csv'
        df = pd.read_csv(url)
        df = df[["Descrição", "Adquiridos", "Valor Unitario", "Valor total", "Reservadas", "Distribuidos", "Restantes"]]
        df1 = df.iloc[:-1]
        return df, df1
    except Exception as e:
        st.error(f"Erro ao carregar os dados: {e}")
        return pd.DataFrame(), pd.DataFrame()

# Carrega os dados
df, df1 = load_data()

# ==============================
# Título e Interatividade
# ==============================
st.title("📊 Biênio 2023-2025 - Equipamentos")

# Botão para atualizar dados
if st.button("🔄 Atualizar Base"):
    df, df1 = load_data()
    st.success("Dados atualizados com sucesso!")

# ==============================
# Gráficos com Altair
# ==============================

# Gráfico de Pizza (adaptado para gráfico de setores no Altair)
totals = {
    'Adquiridos': df1['Adquiridos'].sum(),
    'Distribuidos': df1['Distribuidos'].sum(),
    'Reservadas': df1['Reservadas'].sum(),
    'Restantes': df1['Restantes'].sum()
}
data_totals = pd.DataFrame({
    'Categoria': list(totals.keys()),
    'Quantidade': list(totals.values())
})

pie_chart = alt.Chart(data_totals).mark_arc(innerRadius=50).encode(
    theta=alt.Theta(field="Quantidade", type="quantitative"),
    color=alt.Color(field="Categoria", type="nominal"),
    tooltip=["Categoria", "Quantidade"]
).properties(title="Proporção Geral dos Equipamentos")

# Card de Investimento
try:
    investimento = df.tail(1)
    campo = investimento["Valor total"].values[0]
    simbolo, valor = campo.split(' ', 1)
    valor = valor.replace('.', '').replace(',', '.')
    valor = float(valor)
except:
    valor = 0

# Gráfico de Barras: Exibir "Adquiridos" por "Descrição"
bar_chart = alt.Chart(df1).mark_bar().encode(
    x=alt.X("Adquiridos:Q", title="Quantidade Adquirida"),
    y=alt.Y("Descrição:N", sort="-x", title="Descrição"),
    tooltip=["Descrição", "Adquiridos"]
).properties(
    title="Adquiridos por Descrição",
    height=300
)

# Estilo para borda
# borda_css = """
# <style>
# .borda-container {
#     border: 2px solid #4F81BD;  /* Cor da borda */
#     border-radius: 10px;       /* Bordas arredondadas */
#     padding: 10px;             /* Espaçamento interno */
#     margin-bottom: 20px;       /* Espaçamento entre os gráficos */
#     background-color: #f9f9f9; /* Cor de fundo */
#     box-shadow: 2px 2px 5px rgba(0, 0, 0, 0.1); /* Sombra opcional */
# }
# </style>
# """

# # Insere o CSS
# st.markdown(borda_css, unsafe_allow_html=True)


# ==============================
# Layout no Streamlit
# ==============================
col1, col2, col3 = st.columns([1.5,1,1.5])

with col1:
    st.altair_chart(pie_chart, use_container_width=True)

with col2:
    #st.markdown('<div class="borda-container">', unsafe_allow_html=True)
    st.metric(label="Investimento Total (R$)", value=f"R$ {valor:,.2f}")
    #st.markdown('</div>', unsafe_allow_html=True)

#st.markdown('<div class="borda-container">', unsafe_allow_html=True)
with col3:
    st.subheader("📊 Quantidade Adquirida por Item")
    st.altair_chart(bar_chart, use_container_width=True)
#st.markdown('</div>', unsafe_allow_html=True)

# Exibe tabela
st.subheader("📊 Tabela Resumo dos Dados")
st.dataframe(df, use_container_width=True)

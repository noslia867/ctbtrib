# ctbtrib
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

sns.set_style("whitegrid")

data = {
    'Ano': [2025, 2026, 2027, 2028, 2029]*3,
    'Crescimento': ['5%']*5 + ['8%']*5 + ['12%']*5,
    'Total_Projetado': [
        2935815, 3082606, 3236736, 3398573, 3568502,
        3019696, 3261272, 3522173, 3803947, 4108263,
        3104409, 3476937, 3894178, 4361499, 4874473
    ],
    'Desconto (%)': [45, 55, 50, 60, 65]*3,
    'Total_com_Transacao': [
        2264045, 2220501, 2413817, 2361695, 2389053,
        2328732, 2349199, 2626684, 2643393, 2750414,
        2392765, 2500832, 2896075, 3020323, 3246702
    ]
}

projecoes = pd.DataFrame(data)

st.set_page_config(page_title="Painel PGFN", layout="centered")
st.title("📊 Painel de Projeções PGFN e Simulações Tributárias")

crescimento = st.selectbox("Selecione o cenário de crescimento:", sorted(projecoes['Crescimento'].unique()))

df_filtrado = projecoes[projecoes['Crescimento'] == crescimento]

st.subheader("Evolução do Débito: Projeção x Transação")
fig, ax = plt.subplots(figsize=(10, 5))
ax.plot(df_filtrado['Ano'], df_filtrado['Total_Projetado'], label='Total Projetado', marker='o', linewidth=2)
ax.plot(df_filtrado['Ano'], df_filtrado['Total_com_Transacao'], label='Com Transação', marker='o', linewidth=2)
ax.set_ylabel("Valor (R$)")
ax.set_xlabel("Ano")
ax.set_title("Comparativo Anual")
ax.legend()
ax.grid(True)
st.pyplot(fig)

st.subheader("Tabela de Projeções Detalhada")
st.dataframe(df_filtrado.reset_index(drop=True))
with st.expander("📄 Exibir código-fonte do painel"):
    with open(__file__, "r", encoding="utf-8") as f:
        st.code(f.read(), language="python")


import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter

# =====================
# CONFIG
# =====================
st.set_page_config(
    page_title="Simulador de Variância",
    layout="wide"
)

st.title("Simulador de Variância – Value Betting")
st.subheader("EV x Resultado Real por Volume (Monte Carlo)")

# =====================
# INPUTS
# =====================
col1, col2, col3, col4 = st.columns(4)

with col1:
    n_apostas = st.number_input(
        "Número de apostas",
        min_value=100,
        max_value=50000,
        value=10000,
        step=500
    )

with col2:
    stake = st.number_input(
        "Stake por aposta (R$)",
        min_value=100,
        max_value=5000,
        value=1000,
        step=100
    )

with col3:
    odd_media = st.number_input(
        "Odd média",
        min_value=1.5,
        max_value=20.0,
        value=9.0,
        step=0.1
    )

with col4:
    ev = st.number_input(
        "EV (%)",
        min_value=1.0,
        max_value=20.0,
        value=7.0,
        step=0.5
    ) / 100

simulacoes = st.slider(
    "Número de simulações (cenários)",
    min_value=5,
    max_value=20,
    value=20
)

# =====================
# SIMULAÇÃO
# =====================
p_win = (1 + ev) / odd_media
ganho = stake * (odd_media - 1)
perda = -stake

volume = np.arange(1, n_apostas + 1)
ev_linha = volume * stake * ev

# Configuração visual (forçando padrão tipo Colab)
plt.rcParams.update({
    "font.size": 9,
    "axes.titlesize": 11,
    "axes.labelsize": 9,
    "legend.fontsize": 9
})

fig, ax = plt.subplots(figsize=(8, 4.5), dpi=100)

todas_simulacoes = []

for _ in range(simulacoes):
    resultados = np.where(
        np.random.rand(n_apostas) < p_win,
        ganho,
        perda
    )
    acumulado = np.cumsum(resultados)
    todas_simulacoes.append(acumulado)
    ax.plot(volume, acumulado, alpha=0.35, linewidth=1)

# Linha de EV esperado
ax.plot(
    volume,
    ev_linha,
    linestyle="--",
    color="black",
    linewidth=2,
    label="EV Esperado"
)

ax.set_xlabel("Volume (número de apostas)")
ax.set_ylabel("Resultado (R$)")
ax.set_title("Cenários de Variância vs EV")
ax.legend()

# Formatação monetária
def formato_real(x, pos):
    return f"R$ {x:,.0f}".replace(",", ".")

ax.yaxis.set_major_formatter(FuncFormatter(formato_real))
plt.tight_layout()

# =====================
# MÉTRICAS
# =====================
resultados_finais = np.array([sim[-1] for sim in todas_simulacoes])

ev_esperado_final = n_apostas * stake * ev
resultado_medio = resultados_finais.mean()
p5 = np.percentile(resultados_finais, 5)
p95 = np.percentile(resultados_finais, 95)
prob_prejuizo = np.mean(resultados_finais < 0)

# =====================
# LAYOUT FINAL
# =====================
col_graf, col_stats = st.columns([2.2, 1])

with col_graf:
    st.pyplot(fig, use_container_width=False)

with col_stats:
    st.markdown("### 📊 Resumo da Simulação")

    st.metric(
        "EV Esperado",
        f"R$ {ev_esperado_final:,.0f}".replace(",", ".")
    )

    st.metric(
        "Resultado Médio",
        f"R$ {resultado_medio:,.0f}".replace(",", ".")
    )

    st.metric(
        "Pior cenário plausível (P5)",
        f"R$ {p5:,.0f}".replace(",", ".")
    )

    st.metric(
        "Melhor cenário plausível (P95)",
        f"R$ {p95:,.0f}".replace(",", ".")
    )

    st.markdown("---")

    st.metric(
        "Probabilidade de prejuízo",
        f"{prob_prejuizo * 100:.1f}%"
    )

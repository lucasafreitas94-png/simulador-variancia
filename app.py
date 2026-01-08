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
    n_apostas = st.number_input("Número de apostas", 100, 50000, 10000, step=500)

with col2:
    stake = st.number_input("Stake por aposta (R$)", 100, 5000, 1000, step=100)

with col3:
    odd_media = st.number_input("Odd média", 1.5, 20.0, 9.0, step=0.1)

with col4:
    ev = st.number_input("EV (%)", 1.0, 20.0, 7.0, step=0.5) / 100

simulacoes = st.slider("Número de simulações", 5, 100, 30)

# =====================
# SIMULAÇÃO
# =====================
p_win = (1 + ev) / odd_media
ganho = stake * (odd_media - 1)
perda = -stake

volume = np.arange(1, n_apostas + 1)
ev_linha = volume * stake * ev

fig, ax = plt.subplots(figsize=(7.5, 4))

todas_simulacoes = []

for _ in range(simulacoes):
    resultados = np.where(
        np.random.rand(n_apostas) < p_win,
        ganho,
        perda
    )
    acumulado = np.cumsum(resultados)
    todas_simulacoes.append(acumulado)
    ax.plot(volume, acumulado, alpha=0.25)


ax.plot(volume, ev_linha, "k--", linewidth=2, label="EV Esperado")

ax.set_xlabel("Volume (número de apostas)")
ax.set_ylabel("Resultado (R$)")
ax.set_title("Cenários de Variância vs EV")
ax.legend()

def formato_real(x, pos):
    return f'R$ {x:,.0f}'.replace(',', '.')

plt.gca().yaxis.set_major_formatter(FuncFormatter(formato_real))

plt.tight_layout()
st.pyplot(fig, use_container_width=False)


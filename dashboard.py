import os
import time
from datetime import datetime
from html import escape

import pandas as pd
import streamlit as st

# =====================================================================
# CONFIGURAÇÕES GLOBAIS
# =====================================================================
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ARQUIVO_BANCO_DADOS = os.path.join(BASE_DIR, "banco_leads_sdr_enterprise.csv")
ARQUIVO_LOGS = os.path.join(BASE_DIR, "sdr_system_audit.log")

st.set_page_config(
    page_title="Olli Hub Enterprise v2.0 | SDR Intelligence & AI Matrix",
    page_icon="🔮",
    layout="wide",
    initial_sidebar_state="expanded",
)

# =====================================================================
# CSS
# =====================================================================
st.markdown(
    """
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&family=Space+Grotesk:wght@500;700&display=swap');

        html, body, [data-testid="stAppViewContainer"], .main {
            background: linear-gradient(180deg, #0B071E 0%, #120B2D 100%);
            color: #E2E8F0 !important;
            font-family: 'Inter', sans-serif;
        }

        [data-testid="stSidebar"] {
            background: #070414 !important;
            border-right: 1px solid rgba(124, 58, 237, 0.2);
        }

        h1, h2, h3, h4 {
            font-family: 'Space Grotesk', sans-serif !important;
            font-weight: 700 !important;
            letter-spacing: -0.02em;
        }

        .cyber-title {
            background: linear-gradient(135deg, #A855F7 0%, #7C3AED 50%, #06B6D4 100%);
            -webkit-background-clip: text;
            background-clip: text;
            color: transparent;
            font-size: 2.5rem;
            font-weight: 800;
            margin-bottom: 0.35rem;
            text-shadow: 0 0 30px rgba(124, 58, 237, 0.3);
        }

        .subtitle {
            color: #94A3B8;
            font-size: 1.08rem;
            margin-top: -8px;
            margin-bottom: 1.5rem;
        }

        div[data-testid="stTextInput"] input {
            background-color: rgba(15, 10, 36, 0.6) !important;
            color: #E2E8F0 !important;
            border: 1px solid rgba(168, 85, 247, 0.4) !important;
            border-radius: 12px !important;
            padding: 0.8rem 1rem !important;
            font-family: 'Space Grotesk', sans-serif !important;
            box-shadow: 0 0 15px rgba(124, 58, 237, 0.1) !important;
            transition: all 0.3s ease;
        }

        div[data-testid="stTextInput"] input:focus {
            border-color: #06B6D4 !important;
            box-shadow: 0 0 25px rgba(6, 182, 212, 0.35), inset 0 0 10px rgba(6, 182, 212, 0.1) !important;
        }

        div.stButton > button {
            width: 100%;
            background: linear-gradient(135deg, #7C3AED 0%, #A855F7 100%) !important;
            color: #ffffff !important;
            border: 1px solid rgba(255, 255, 255, 0.1) !important;
            border-radius: 12px !important;
            font-family: 'Space Grotesk', sans-serif !important;
            font-weight: 600 !important;
            padding: 0.75rem 1.2rem !important;
            box-shadow: 0 6px 20px rgba(124, 58, 237, 0.35) !important;
            transition: all 0.25s ease !important;
        }

        div.stButton > button:hover {
            transform: translateY(-2px);
            box-shadow: 0 10px 30px rgba(168, 85, 247, 0.55) !important;
            border-color: rgba(6, 182, 212, 0.7) !important;
        }

        div.stButton > button:active {
            transform: scale(0.98);
            background: #06B6D4 !important;
        }

        .kpi-container {
            background: linear-gradient(145deg, rgba(26, 18, 70, 0.5), rgba(11, 7, 30, 0.85));
            border-left: 4px solid #7C3AED;
            border-radius: 16px;
            padding: 20px;
            box-shadow: inset 0 0 12px rgba(124, 58, 237, 0.05);
            min-height: 120px;
        }

        .kpi-title {
            color: #94A3B8;
            font-size: 11px;
            font-weight: 700;
            text-transform: uppercase;
            letter-spacing: 0.15em;
        }

        .kpi-value {
            color: #ffffff;
            font-size: 2rem;
            font-family: 'Space Grotesk', sans-serif;
            font-weight: 700;
            margin-top: 8px;
        }

        .hologram-card {
            background: rgba(20, 14, 56, 0.45);
            border: 1px solid rgba(168, 85, 247, 0.18);
            border-radius: 20px;
            padding: 22px;
            margin-bottom: 1.5rem;
            box-shadow: 0 12px 40px rgba(124, 58, 237, 0.08);
            backdrop-filter: blur(12px);
            -webkit-backdrop-filter: blur(12px);
        }

        .hologram-card:hover {
            border-color: rgba(6, 182, 212, 0.6);
            transform: translateY(-4px);
            transition: all 0.25s ease;
        }

        .ai-response {
            background: rgba(6, 182, 212, 0.06);
            border: 1px dashed rgba(6, 182, 212, 0.35);
            border-radius: 14px;
            padding: 18px;
            color: #7DD3FC;
            font-family: 'Space Grotesk', sans-serif;
            margin-top: 14px;
            line-height: 1.7;
        }

        .latency-bar-bg {
            background: rgba(255,255,255,0.05);
            border-radius: 8px;
            height: 10px;
            width: 100%;
            margin-top: 8px;
            overflow: hidden;
        }

        .latency-bar-fill {
            background: linear-gradient(90deg, #7C3AED, #06B6D4);
            height: 100%;
            border-radius: 8px;
        }
    </style>
    """,
    unsafe_allow_html=True,
)

# =====================================================================
# LOGS
# =====================================================================
def registrar_log(mensagem: str, usuario: str = "Sistema") -> None:
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    linha = f"[{timestamp}] [{usuario}] {mensagem}\n"
    try:
        with open(ARQUIVO_LOGS, "a", encoding="utf-8") as arquivo:
            arquivo.write(linha)
    except OSError:
        pass


# =====================================================================
# DADOS
# =====================================================================
DADOS_INICIAIS_MOCK = [
    {
        "ID": "ISP-701",
        "Status Contato": "Qualificado",
        "Provedor": "Alpha Fibra Telecom",
        "Responsáveis": "Carlos Silva",
        "Cargo": "Diretor de Operações",
        "Localidade": "Chapecó - SC",
        "Telefone": "(49) 3321-1000",
        "Email": "diretoria@alphafibra.com.br",
        "Situação de Mercado": "Guerra de preço agressiva / Perda de margem na região",
        "Produto Olli": "Olli Smart Home",
        "CNPJ": "31.862.534/0001-30",
        "Clientes Estimados": 12000,
        "Ticket Médio (R$)": 89.90,
        "Data Cadastro": "2026-01-10",
        "Score Conectividade": 88,
        "Origem Lead": "Outbound LinkedIn",
    },
    {
        "ID": "ISP-702",
        "Status Contato": "Não Chamado",
        "Provedor": "Beta Net Telecom",
        "Responsáveis": "Rodrigo Ramos",
        "Cargo": "CEO",
        "Localidade": "Blumenau - SC",
        "Telefone": "(47) 3211-5500",
        "Email": "rodrigo@betanet.net.br",
        "Situação de Mercado": "Churn alto detectado em relatórios ANATEL",
        "Produto Olli": "Olli Habita",
        "CNPJ": "14.552.112/0001-99",
        "Clientes Estimados": 7500,
        "Ticket Médio (R$)": 79.90,
        "Data Cadastro": "2026-02-15",
        "Score Conectividade": 45,
        "Origem Lead": "Mapeamento ANATEL",
    },
    {
        "ID": "ISP-703",
        "Status Contato": "Agendado (Reunião)",
        "Provedor": "Wave Conectividade",
        "Responsáveis": "Juliana Mendes",
        "Cargo": "Gerente de Marketing",
        "Localidade": "Maringá - PR",](#)


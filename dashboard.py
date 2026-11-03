import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import random
import os
import time
from datetime import datetime

# =====================================================================
# CONFIGURAÇÕES GLOBAIS E ESTILIZAÇÃO ULTRA-FUTURISTA (HUD & CYBER-LUXURY)
# =====================================================================
ARQUIVO_BANCO_DADOS = "banco_leads_sdr_enterprise.csv"
ARQUIVO_LOGS = "sdr_system_audit.log"

st.set_page_config(
    page_title="Olli Hub Enterprise v2.0 | SDR Intelligence & AI Matrix",
    page_icon="🔮",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Injeção de CSS de Última Geração (Estilo Awwwards / Vercel Premium)
st.markdown("""
<style>
    /* Importando fonte tecnológica */
    @import url('https://googleapis.com');
    
    /* Configuração Global do Dark Mode Absoluto */
    html, body, [data-testid="stAppViewContainer"], .main {
        background-color: #0B071E !important;
        color: #E2E8F0 !important;
        font-family: 'Plus Jakarta Sans', sans-serif;
    }
    
    /* Customização da Sidebar Futurista */
    [data-testid="stSidebar"] {
        background-color: #070414 !important;
        border-right: 1px solid rgba(124, 58, 237, 0.2);
    }
    
    /* Títulos em Fonte Geométrica */
    h1, h2, h3 {
        font-family: 'Space Grotesk', sans-serif !important;
        font-weight: 700 !important;
        letter-spacing: -0.02em;
    }
    
    /* Cabeçalho Principal Neon */
    .cyber-title {
        background: linear-gradient(135deg, #A855F7 0%, #7C3AED 50%, #06B6D4 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-size: 2.5rem;
        font-weight: 800;
        margin-bottom: 0.5rem;
        text-shadow: 0 0 40px rgba(124, 58, 237, 0.3);
    }
    
    /* Barra de Busca com Efeito HUD de Escaneamento */
    div[data-testid="stTextInput"] input {
        background-color: rgba(15, 10, 36, 0.6) !important;
        color: #06B6D4 !important;
        border: 1px solid rgba(168, 85, 247, 0.4) !important;
        border-radius: 12px !important;
        padding: 0.75rem 1.2rem !important;
        font-family: 'Space Grotesk', sans-serif !important;
        box-shadow: 0 0 15px rgba(124, 58, 237, 0.1) !important;
        transition: all 0.4s cubic-bezier(0.25, 1, 0.5, 1) !important;
    }
    div[data-testid="stTextInput"] input:focus {
        border-color: #06B6D4 !important;
        box-shadow: 0 0 25px rgba(6, 182, 212, 0.4), inset 0 0 10px rgba(6, 182, 212, 0.1) !important;
        transform: scale(1.01);
    }

    /* Botões Premium com Animação de Onda Magnética e Ripple Elétrico no Clique */
    div.stButton > button {
        background: linear-gradient(135deg, #7C3AED 0%, #A855F7 100%) !important;
        color: #ffffff !important;
        border: 1px solid rgba(255, 255, 255, 0.1) !important;
        border-radius: 12px !important;
        font-family: 'Space Grotesk', sans-serif !important;
        font-weight: 600 !important;
        padding: 0.75rem 1.5rem !important;
        box-shadow: 0 4px 20px rgba(124, 58, 237, 0.3) !important;
        transition: all 0.3s cubic-bezier(0.25, 1, 0.5, 1) !important;
        position: relative;
        overflow: hidden;
        width: 100%;
    }
    div.stButton > button:hover {
        transform: translateY(-3px);
        box-shadow: 0 8px 30px rgba(168, 85, 247, 0.6) !important;
        border-color: #06B6D4 !important;
    }
    div.stButton > button:active {
        transform: scale(0.97) !important;
        background: #06B6D4 !important;
        box-shadow: 0 0 40px #06B6D4 !important;
        animation: electricPulse 0.4s ease-out;
    }

    @keyframes electricPulse {
        0% { box-shadow: 0 0 0px rgba(6, 182, 212, 0.7); }
        100% { box-shadow: 0 0 50px rgba(6, 182, 212, 0); }
    }

    /* Cards Holográficos de Provedores (Glassmorphism de Alto Padrão) */
    .hologram-card {
        background: rgba(20, 14, 56, 0.4) !important;
        backdrop-filter: blur(16px) saturate(180%);
        -webkit-backdrop-filter: blur(16px) saturate(180%);
        border: 1px solid rgba(168, 85, 247, 0.15);
        border-radius: 20px;
        padding: 24px;
        margin-bottom: 1.5rem;
        transition: all 0.4s cubic-bezier(0.25, 1, 0.5, 1);
        position: relative;
        overflow: hidden;
    }
    .hologram-card:hover {
        transform: translateY(-6px) scale(1.01);
        border-color: rgba(6, 182, 212, 0.6);
        box-shadow: 0 20px 40px rgba(124, 58, 237, 0.15), 0 0 30px rgba(6, 182, 212, 0.1);
    }
    
    /* Decoração de Canto estilo HUD */
    .hologram-card::before {
        content: '';
        position: absolute;
        top: 0; right: 0;
        width: 12px; height: 12px;
        border-top: 2px solid #06B6D4;
        border-right: 2px solid #06B6D4;
        opacity: 0;
        transition: opacity 0.3s ease;
    }
    .hologram-card:hover::before { opacity: 1; }

    /* Indicadores de Métricas (KPIs Corporativos de Alta Performance) */
    .kpi-container-futuristic {
        background: linear-gradient(145deg, rgba(26, 18, 70, 0.5) 0%, rgba(11, 7, 30, 0.8) 100%);
        border-left: 4px solid #7C3AED;
        border-radius: 14px;
        padding: 20px;
        box-shadow: inset 0 0 20px rgba(124, 58, 237, 0.05);
    }
    .kpi-title-futuristic {
        color: #94A3B8;
        font-size: 11px;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 0.15em;
    }
    .kpi-value-futuristic {
        color: #ffffff;
        font-size: 2rem;
        font-family: 'Space Grotesk', sans-serif;
        font-weight: 700;
        margin-top: 5px;
        text-shadow: 0 0 20px rgba(255,255,255,0.1);
    }

    /* Gráfico de Latência de última geração */
    .latency-bar-bg {
        background: rgba(255,255,255,0.05);
        border-radius: 6px;
        height: 8px;
        width: 100%;
        margin-top: 8px;
        overflow: hidden;
    }
    .latency-bar-fill {
        background: linear-gradient(90deg, #7C3AED, #06B6D4);
        height: 100%;
        border-radius: 6px;
        animation: networkScan 2s infinite linear;
    }

    /* Animação Laser de Varredura para Itens em Carregamento */
    @keyframes networkScan {
        0% { opacity: 0.7; }
        50% { opacity: 1; }
        100% { opacity: 0.7; }
    }
</style>
""", unsafe_allow_html=True)

# =====================================================================
# MÓDULO DE AUDITORIA, TELEMETRIA E LOGS
# =====================================================================
def registrar_log(mensagem: str, usuario: str = "Sistema"):
    """Registra eventos críticos em um arquivo local para governança de dados."""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_linha = f"[{timestamp}] [{usuario}] {mensagem}\n"
    try:
        with open(ARQUIVO_LOGS, "a", encoding="utf-8") as f:
            f.write(log_linha)
    except IOError:
        pass

# =====================================================================
# CAMADA DE PERSISTÊNCIA DE DADOS (CRUD ENGINE)
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
        "Origem Lead": "Outbound LinkedIn"
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
        "Situação de Mercado": "Churn Alto detectado em relatórios ANATEL",
        "Produto Olli": "Olli Habita",
        "CNPJ": "14.552.112/0001-99",
        "Clientes Estimados": 7500,
        "Ticket Médio (R$)": 79.90,
        "Data Cadastro": "2026-02-15",
        "Score Conectividade": 45,
        "Origem Lead": "Mapeamento ANATEL"
    },
    {
        "ID": "ISP-703",
        "Status Contato": "Agendado (Reunião)",
        "Provedor": "Wave Conectividade",
        "Responsáveis": "Juliana Mendes",
        "Cargo": "Gerente de Marketing",
        "Localidade": "Maringá - PR",
        "Telefone": "(44) 99881-2233",
        "Email": "juliana@waveconect.com.br",
        "Situação de Mercado": "Estagnação de vendas / Sem Serviços de Valor Adicionado (SVA)",
        "Produto Olli": "Olli Smart Home",
        "CNPJ": "45.123.789/0001-02",
        "Clientes Estimados": 24000,
        "Ticket Médio (R$)": 110.00,
        "Data Cadastro": "2026-03-22",
        "Score Conectividade": 92,
        "Origem Lead": "Inbound - Evento IXC"
    }
]

def inicializar_e_carregar_dados() -> pd.DataFrame:
    """Garante a existência do banco de dados local com tratamento de integridade schema-level."""
    if not os.path.exists(ARQUIVO_BANCO_DADOS):
        df = pd.DataFrame(DADOS_INICIAIS_MOCK)
        df.to_csv(ARQUIVO_BANCO_DADOS, index=False, encoding="utf-8")
        registrar_log("Base de dados corporativa inicializada com sucesso.")
        return df
    try:
        df = pd.read_csv(ARQUIVO_BANCO_DADOS, encoding="utf-8")

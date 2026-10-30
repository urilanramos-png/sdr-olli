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
# CONFIGURAÇÕES GLOBAIS E ESTILIZAÇÃO DA INTERFACE
# =====================================================================
ARQUIVO_BANCO_DADOS = "banco_leads_sdr_enterprise.csv"
ARQUIVO_LOGS = "sdr_system_audit.log"

st.set_page_config(
    page_title="Olli Hub Enterprise v2.0 | SDR Intelligence & AI Matrix",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Injeção de CSS Customizado para uma interface corporativa moderna
st.markdown("""
<style>
    .main .block-container { padding-top: 1.5rem; padding-bottom: 1.5rem; }
    div.stButton > button:first-child {
        background-color: #4F46E5;
        color: white;
        border-radius: 6px;
        font-weight: 600;
        border: none;
        padding: 0.5rem 1rem;
        transition: all 0.3s ease;
    }
    div.stButton > button:first-child:hover {
        background-color: #4338CA;
        transform: translateY(-1px);
    }
    .kpi-card {
        background-color: #ffffff;
        padding: 22px;
        border-radius: 10px;
        box-shadow: 0 4px 6px -1px rgba(0,0,0,0.07);
        border-left: 5px solid #4F46E5;
        margin-bottom: 1rem;
    }
    .kpi-title { color: #6B7280; font-size: 13px; font-weight: 700; letter-spacing: 0.05em; margin: 0; }
    .kpi-value { margin: 8px 0 0 0; color: #1F2937; font-size: 28px; font-weight: 700; }
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
        colunas_obrigatorias = ["ID", "Status Contato", "Provedor", "Responsáveis", "Cargo", "Localidade", 
                                "Telefone", "Email", "Situação de Mercado", "Produto Olli", "CNPJ", 
                                "Clientes Estimados", "Ticket Médio (R$)", "Data Cadastro", "Score Conectividade", "Origem Lead"]
        mudou = False
        for col in colunas_obrigatorias:
            if col not in df.columns:
                df[col] = 0 if "Estimados" in col or "Score" in col else "Não Informado"
                mudou = True
        if mudou:
            df.to_csv(ARQUIVO_BANCO_DADOS, index=False, encoding="utf-8")
        return df
    except Exception as e:
        registrar_log(f"Falha ao carregar banco de dados: {str(e)}", "ERRO")
        return pd.DataFrame(DADOS_INICIAIS_MOCK)

def salvar_dados_locais(df: pd.DataFrame):
    """Grava as modificações no arquivo CSV local de forma permanente."""
    try:
        df.to_csv(ARQUIVO_BANCO_DADOS, index=False, encoding="utf-8")
    except Exception as e:
        st.error(f"Erro ao salvar alterações no disco: {e}")

# =====================================================================
# MOTOR COGNITIVO E ENGENHARIA DE PROMPTS PARA SDR
# =====================================================================
class MotorInteligenciaSDR:
    @staticmethod
    def obter_matriz_contextual(situacao_mercado: str) -> dict:
        """Mapeia dores operacionais de provedores para gatilhos de abordagem comercial."""
        matrizes = {
            "Guerra de preço agressiva / Perda de margem na região": {
                "Gancho Principal": "Diferenciação competitiva e blindagem de margem agregando valor perceptual.",
                "Estratégia": "Posicionar a Olli como acelerador de receita marginal, eliminando a necessidade de dar descontos em conexões puras.",
                "Framework": "PAS (Problema, Agitação, Solução)"
            },
            "Churn Alto detectado em relatórios ANATEL": {
                "Gancho Principal": "Criação de ecossistema residencial integrado para aumento drástico de LTV.",
                "Estratégia": "Mostrar que agregar segurança e smart home vincula o cliente ao provedor, reduzindo quebra de contratos em até 30%.",
                "Framework": "AIDA (Atenção, Interesse, Desejo, Ação)"
            },
            "Estagnação de vendas / Sem Serviços de Valor Adicionado (SVA)": {
                "Gancho Principal": "Monetização da base de clientes existente através de cross-selling estruturado.",
                "Estratégia": "Introduzir a Olli como novo portfólio de faturamento imediato para contornar o teto de vendas de banda larga.",
                "Framework": "Venda Consultiva Baseada em Valor"
            },
            "Picos de queixas recentes no Reclame Aqui (Queda/Suporte)": {
                "Gancho Principal": "Melhoria da percepção de estabilidade dentro do lar do consumidor final.",
                "Estratégia": "Mudar a conversa de infraestrutura física caída para uma experiência de automação residencial de alta fidelidade.",
                "Framework": "Inversão de Risco e Restauração de Confiança"
            }
        }
        return matrizes.get(situacao_mercado, {
            "Gancho Principal": "Parceria estratégica de tecnologia e valor agregado para ISPs corporativos.",
            "Estratégia": "Apresentar as vantagens integradas nativas do ecossistema IXC Soft para controle operacional.",
            "Framework": "Abordagem Linear B2B"
        })

    @staticmethod
    def construir_script_venda(linha_lead, matriz: dict) -> str:
        """Gera um roteiro hiper-personalizado usando formatação direta por chaves."""
        script_modelo = (
            "### 📞 SCRIPT DE ABORDAGEM PERSONALIZADO (ALTA CONVERSÃO)\n"
            "* **Alvo:** {responsavel} ({cargo}) | **ISP:** {provedor}\n"
            "* **Canal Sugerido:** Mensagem Direta LinkedIn InMail ou Cold Call\n\n"
            "#### 🎯 Abertura Estratégica\n"
            "\"Olá, {responsavel}. Tudo bem? Acompanho o crescimento da {provedor} na região de {localidade} "
            "e notei o quão competitiva a praça tem se tornado. Para operações robustas como a sua, gerenciar "
            "a rentabilidade média virou o grande divisor de águas.\"\n\n"
            "#### 🔥 Diagnóstico e Agitação da Dor\n"
            "\"Analisando indicadores macro, fica nítido que enfrentar a conjuntura de [{dor_mercado}] "
            "exige saídas que fujam da guerra tarifária convencional. Quem vende apenas pacotes de megas " 
            "está sacrificando margem líquida toda semana.\"\n\n"
            "#### 🚀 Proposta de Valor Conectada (Olli + IXC Soft)\n"
            "\"É por isso que estruturamos uma solução de Smart Home e Automação via Olli, totalmente integrada "
            "ao ecossistema IXC Soft. Para sua operação, que já conta com cerca de {clientes:,} assinantes, " )

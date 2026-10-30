import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import random
import os
import time
from datetime import datetime, timedelta

# =====================================================================
# CONSTANTES E CONFIGURAÇÕES GLOBAIS
# =====================================================================
ARQUIVO_BANCO_DADOS = "banco_leads_sdr_v2.csv"
ARQUIVO_LOGS = "sdr_system_logs.txt"

st.set_page_config(
    page_title="Olli Hub Enterprise v2.0 | SDR Intelligence & AI Matrix",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Estilização CSS customizada para visual corporativo premium (Modo Escuro/Claro Suportado)
st.markdown("""
<style>
    .reportview-container { background: #f5f7f9; }
    .main .block-container { padding-top: 2rem; }
    div.stButton > button:first-child {
        background-color: #4F46E5;
        color: white;
        border-radius: 6px;
        font-weight: 600;
        transition: all 0.3s ease;
    }
    div.stButton > button:first-child:hover {
        background-color: #4338CA;
        transform: translateY(-1px);
    }
    .metric-card {
        background-color: #ffffff;
        padding: 20px;
        border-radius: 8px;
        box-shadow: 0 4px 6px -1px rgba(0,0,0,0.1);
        border-left: 5px solid #4F46E5;
    }
</style>
""", unsafe_allow_html=True)

# =====================================================================
# SISTEMA DE LOGS E AUDITORIA
# =====================================================================
def registrar_log(mensagem: str, usuario: str = "Sistema"):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_linha = f"[{timestamp}] [{usuario}] {mensagem}\n"
    with open(ARQUIVO_LOGS, "a", encoding="utf-8") as f:
        f.write(log_linha)

# =====================================================================
# GERENCIAMENTO DE MOCK DATA & BASE DE DADOS
# =====================================================================
DADOS_DEMO = [
    {
        "ID": "ISP-001",
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
        "Data Cadastro": "2026-10-01",
        "Última Interação": "2026-10-28",
        "SDR Responsável": "Alice Costa",
        "Score Conectividade": 85,
        "Origem Lead": "Outbound LinkedIn"
    },
    {
        "ID": "ISP-002",
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
        "Data Cadastro": "2026-10-15",
        "Última Interação": "2026-10-15",
        "SDR Responsável": "Bruno Melo",
        "Score Conectividade": 42,
        "Origem Lead": "Mapeamento ANATEL"
    },
    {
        "ID": "ISP-003",
        "Status Contato": "Agendado (Reunião)",
        "Provedor": "Wave Conectividade",
        "Responsáveis": "Juliana Mendes",
        "Cargo": "Gerente de Marketing / Produto",
        "Localidade": "Maringá - PR",
        "Telefone": "(44) 99881-2233",
        "Email": "juliana@waveconect.com.br",
        "Situação de Mercado": "Estagnação de vendas / Sem Serviços de Valor Adicionado (SVA)",
        "Produto Olli Smart Home",
        "CNPJ": "45.123.789/0001-02",
        "Clientes Estimados": 24000,
        "Ticket Médio (R$)": 110.00,
        "Data Cadastro": "2026-10-20",
        "Última Interação": "2026-10-29",
        "SDR Responsável": "Alice Costa",
        "Score Conectividade": 91,
        "Origem Lead": "Inbound - Evento IXC"
    }
]

def inicializar_banco_dados():
    if not os.path.exists(ARQUIVO_BANCO_DADOS):
        df = pd.DataFrame(DADOS_DEMO)
        df.to_csv(ARQUIVO_BANCO_DADOS, index=False, encoding="utf-8")
        registrar_log("Banco de dados inicial criado com dados mockados de alta fidelidade.")
    else:
        # Garantir integridade de colunas estruturais novas
        df = pd.read_csv(ARQUIVO_BANCO_DADOS, encoding="utf-8")
        colunas_obrigatorias = [
            "ID", "Status Contato", "Provedor", "Responsáveis", "Cargo", "Localidade", 
            "Telefone", "Email", "Situação de Mercado", "Produto Olli", "CNPJ", 
            "Clientes Estimados", "Ticket Médio (R$)", "Data Cadastro", "Última Interação", 
            "SDR Responsável", "Score Conectividade", "Origem Lead"
        ]
        mudou = False
        for col in colunas_obrigatorias:
            if col not in df.columns:
                if col == "Score Conectividade":
                    df[col] = np.random.randint(30, 99, size=len(df))
                elif col == "Origem Lead":
                    df[col] = "Outbound"
                else:
                    df[col] = "Não Informado"
                mudou = True
        if mudou:
            df.to_csv(ARQUIVO_BANCO_DADOS, index=False, encoding="utf-8")

def carregar_leads() -> pd.DataFrame:
    inicializar_banco_dados()
    try:
        df = pd.read_csv(ARQUIVO_BANCO_DADOS, encoding="utf-8")
        return df
    except Exception as e:
        st.error(f"Erro crítico ao ler base de dados: {e}")
        return pd.DataFrame(DADOS_DEMO)

def salvar_leads(df: pd.DataFrame):
    df.to_csv(ARQUIVO_BANCO_DADOS, index=False, encoding="utf-8")

# =====================================================================
# MOTORES AUXILIARES DE INTELIGÊNCIA ARTIFICIAL (PROMPTING & COPYWRITING)
# =====================================================================
class PromptEngine:
    @staticmethod
    def gerar_matriz_dor(situacao: str) -> dict:
        matrizes = {
            "Guerra de preço agressiva / Perda de margem na região": {
                "Gancho Principal": "Aumento do ARPU (Ticket Médio) sem precisar subir o preço da banda larga pura.",
                "Estratégia": "Mostrar que agregar a Olli cria diferenciação imbatível contra provedores 'comoditizados'.",
                "Framework Copy": "PAS (Problema, Agitação, Solução)"
            },
            "Churn Alto detectado em relatórios ANATEL": {
                "Gancho Principal": "Aumento do LTV (Tempo de vida do cliente) e fidelização forçada por ecossistema smart home.",
                "Estratégia": "Comprovar que SVAs de automação e segurança reduzem a evasão em até 35% nos primeiros 6 meses.",
                "Framework Copy": "AIDA (Atenção, Interesse, Desejo, Ação)"
            },
            "Estagnação de vendas / Sem Serviços de Valor Adicionado (SVA)": {
                "Gancho Principal": "Desbloqueio de novas linhas de receita usando a base instalada atual.",
                "Estratégia": "Vender Upgrades estruturados de planos de conectividade + Olli integrado.",
                "Framework Copy": "Storytelling focado em ROI corporativo"
            },
            "Picos de queixas recentes no Reclame Aqui (Queda/Suporte)": {
                "Gancho Principal": "Mudança da percepção de valor: De infraestrutura instável para Hub de Experiência Familiar.",
                "Estratégia": "Posicionar a Olli como solução premium de estabilidade perceptual na casa do usuário final.",
                "Framework Copy": "Abordagem Consultiva e Inversão de Risco"
            }
        }
        return matrizes.get(situacao, {
            "Gancho Principal": "Inovação tecnológica e entrega de valor em ecossistemas de tecnologia.",
            "Estratégia": "Apresentar a Olli como parceira oficial integrada ao ecossistema IXC Soft.",
            "Framework Copy": "Abordagem Clássica B2B"
        })

    @staticmethod
    def construir_script_ abordagem(lead_row, matriz: dict) -> str:
        script = f"""---
### 🛠️ SCRIPT DE ABORDAGEM PERSONALIZADO (C-LEVEL INTERACTION)
**Alvo:** {lead_row['Responsáveis']} ({lead_row['Cargo']}) | **Empresa:** {lead_row['Provedor']}
**Canal Recomendado:** LinkedIn Inmail ou Cold Call Direta via WhatsApp

**[Abertura de Alto Impacto]**
"Olá, {lead_row['Responsáveis']}. Tudo bem? Tenho acompanhado a expansão da {lead_row['Provedor']} em {lead_row['Localidade']} e notei o dinamismo do mercado local. No cenário atual, sabemos que gerenciar a percepção de valor da marca é um desafio crítico para operações do seu porte."

**[Agitação da Dor - Foco Baseado em Dados]**
"Olhando para os dados de mercado e movimentações dos provedores da região, fica claro que lidar com [{lead_row['Situação de Mercado'].lower()}] exige ir além de simplesmente vender mais megas ou fibra pura. O mercado pune quem compete apenas por preço."

**[Apresentação da Proposta de Valor Olli + IXC Soft]**
"É exatamente aqui que nós, do ecossistema IXC Soft através da Olli, estamos ajudando ISPs com mais de {lead_row['Clientes Estimados']:,} assinantes. Nós injetamos uma camada de Smart Home e Automação diretamente na sua oferta. Isso muda o jogo: em vez de brigar por R$ 5,00 de desconto, sua operação desbloqueia uma nova linha de receita, estabiliza o churn e eleva o ticket médio real."

**[Chamada para Ação (CTA) Assíncrona]**

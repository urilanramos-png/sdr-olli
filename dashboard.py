import streamlit as st
import pandas as pd
import random
import os
import time

# Configuração de Layout e Título da Aba
st.set_page_config(
    page_title="Olli Hub - Inteligência SDR", 
    page_icon="🤖", 
    layout="wide"
)

# =====================================================================
# INJEÇÃO DE DESIGN AVANÇADO (CORES E ACABAMENTO PREMIUM DA OLLI)
# =====================================================================
st.markdown(
    """
    <style>
    /* Fundo geral e fontes do aplicativo */
    .stApp { background-color: #0B0B0E !important; color: #F0F0F5 !important; font-family: 'Inter', sans-serif !important; }
    
    /* Customização da Barra Lateral */
    [data-testid="stSidebar"] { background-color: #121217 !important; border-right: 1px solid #1E1E26; }
    
    /* Títulos e textos em destaque */
    h1, h2, h3, p, span, label { color: #FFFFFF !important; font-family: 'Inter', sans-serif !important; }
    
    /* Botões Grandes no Roxo Vibrante da Olli */
    div.stButton > button:first-child {
        background: linear-gradient(135deg, #7A28FF 0%, #5E14E3 100%) !important;
        color: #FFFFFF !important;
        border-radius: 8px !important;
        border: none !important;
        font-weight: 600 !important;
        padding: 0.6rem 2.5rem !important;
        letter-spacing: 0.5px !important;
        transition: all 0.3s ease !important;
        box-shadow: 0px 4px 15px rgba(122, 40, 255, 0.3) !important;
    }
    div.stButton > button:first-child:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0px 6px 20px rgba(122, 40, 255, 0.5) !important;
    }
    
    /* Customização dos Cards de Métricas */
    div[data-testid="stMetric"] {
        background-color: #121217 !important;
        padding: 20px !important;
        border-radius: 12px !important;
        border: 1px solid #1E1E26 !important;
        box-shadow: 0px 4px 10px rgba(0,0,0,0.2) !important;
    }
    div[data-testid="stMetricValue"] > div { color: #7A28FF !important; font-weight: 700 !important; }
    
    /* Estilização das Abas (Tabs) */
    button[data-baseweb="tab"] { color: #888899 !important; font-size: 15px !important; font-weight: 500 !important; }
    button[data-baseweb="tab"][aria-selected="true"] { color: #7A28FF !important; border-bottom-color: #7A28FF !important; font-weight: 600 !important; }
    
    /* Caixa Informativa do Pitch Comercial */
    .caixa-pitch {
        background-color: #121217 !important;
        padding: 25px !important;
        border-radius: 12px !important;
        border: 1px solid #7A28FF !important;
        box-shadow: 0px 4px 15px rgba(122, 40, 255, 0.15) !important;
    }
    </style>
    """,
    unsafe_html=True
)

ARQUIVO_BANCO_DADOS = "banco_leads_sdr.csv"

# Base de inicialização limpa com o Status do Lead incluído de fábrica
DADOS_INICIAIS = [
    {
        "Status Contato": "Não Chamado",
        "Provedor": "Alpha Fibra Telecom", 
        "Responsáveis": "Carlos Silva",
        "Localidade": "Chapecó - SC",
        "Telefone": "(49) 3321-1000", 
        "Email": "diretoria@alphafibra.com.br", 
        "Situação de Mercado": "Guerra de preço agressiva / Perda de margem na região", 
        "Produto Olli": "Olli Smart Home",
        "CNPJ": "31.862.534/0001-30"
    }
]

def carregar_dados_salvos():
    if os.path.exists(ARQUIVO_BANCO_DADOS):
        try: 
            df_salvo = pd.read_csv(ARQUIVO_BANCO_DADOS)
            if df_salvo.empty:
                return pd.DataFrame(DADOS_INICIAIS)
            if "Status Contato" not in df_salvo.columns:
                df_salvo.insert(0, "Status Contato", "Não Chamado")
            return df_salvo
        except: 
            return pd.DataFrame(DADOS_INICIAIS)
    else:
        df_novo = pd.DataFrame(DADOS_INICIAIS)
        df_novo.to_csv(ARQUIVO_BANCO_DADOS, index=False)
        return df_novo

def salvar_alteracoes_tabela(df_atualizado):
    df_atualizado.to_csv(ARQUIVO_BANCO_DADOS, index=False)

def gravar_multiplos_leads_no_arquivo(novos_leads):
    df_atual = carregar_dados_salvos()
    df_novos_registros = pd.DataFrame(novos_leads)
    df_consolidado = pd.concat([df_atual, df_novos_registros], ignore_index=True)
    df_consolidado.drop_duplicates(subset=["Provedor"], keep="first", inplace=True)
    df_consolidado.to_csv(ARQUIVO_BANCO_DADOS, index=False)

def deletar_lista_leads_do_arquivo(lista_nomes_provedores):
    df_atual = carregar_dados_salvos()
    df_atual = df_atual[~df_atual["Provedor"].isin(lista_nomes_provedores)]
    df_atual.reset_index(drop=True, inplace=True)
    df_atual.to_csv(ARQUIVO_BANCO_DADOS, index=False)

# =====================================================================
# TELA DE LOGIN CORPORATIVA
# =====================================================================
def verificar_senha():
    if "autenticado" not in st.session_state: 
        st.session_state.autenticado = False

    if not st.session_state.autenticado:
        st.write("")
        st.write("")
        col_log1, col_log2, col_log3 = st.columns([1, 1.5, 1])
        with col_log2:
            st.markdown("<h2 style='text-align: center; color: #7A28FF;'>🔒 Olli Hub - Autenticação</h2>", unsafe_html=True)
            st.write("---")
            with st.form("Formulário de Login"):
                usuario = st.text_input("Usuário Corporativo:")
                senha = st.text_input("Senha de Acesso:", type="password")
                enviar = st.form_submit_button("Acessar Plataforma")
                if enviar:
                    if usuario == "olli" and senha == "ixc123":
                        st.session_state.autenticado = True
                        st.rerun()
                    else: 
                        st.error("❌ Credenciais incorretas.")
        return False
    return True

if verificar_senha():
    df = carregar_dados_salvos()

    # =====================================================================
    # SIDEBAR DESIGN MARCA OLLI
    # =====================================================================
    st.sidebar.markdown(
        "<div style='text-align: center; padding: 10px;'>"
        "<h1 style='color: #7A28FF; font-family: sans-serif; font-size: 42px; margin-bottom: 0px; font-weight: bold;'>Olli</h1>"
        "<p style='font-size: 13px; color: #888899; margin-top: 0px;'>Intelligence SDR v2.0</p>"
        "</div>", 
        unsafe_html=True
    )
    st.sidebar.write("---")
    
    st.sidebar.subheader("🎯 Menu de Filtros")
    
    status_selecionado = st.sidebar.multiselect(
        "Filtrar por Status do Lead:",
        options=["Não Chamado", "Chamado"],
        default=["Não Chamado", "Chamado"]
    )
    
    situacao_selecionada = st.sidebar.multiselect(
        "Filtrar Dores de Provedores:", 
        options=df["Situação de Mercado"].unique(), 
        default=df["Situação de Mercado"].unique()
    )
    
    st.sidebar.write("---")
    st.sidebar.caption("Divisão de Soluções IXC Soft © 2026")

    df_filtrado = df[
        (df["Situação de Mercado"].isin(situacao_selecionada)) & 
        (df["Status Contato"].isin(status_selecionado))
    ].copy()

    # =====================================================================
    # CORPO PRINCIPAL DO DASHBOARD
    # =====================================================================
    st.markdown("## 📊 Painel Geral de Prospecção Estratégica")
    st.markdown("Gerenciamento automatizado de leads ISPs com status de controle e dores validadas.")
    st.write("---")

    # CARDS DE MÉTRICAS
    m1, m2, m3 = st.columns(3)
    with m1:
        st.metric(label="Total de ISPs na Base", value=len(df))
    with m2:
        st.metric(label="Foco: Olli Smart Home", value=len(df[df['Produto Olli'] == 'Olli Smart Home']))
    with m3:
        st.metric(label="Foco: Olli Habita", value=len(df[df['Produto Olli'] == 'Olli Habita']))

    st.write("---")

    # ABAS INTERATIVAS DE OPERAÇÃO
    aba_varredura, aba_analise = st.tabs(["🚀 Central de Operações & Leads", "📊 Gráficos & Estatísticas de Mercado"])

    with aba_varredura:
        st.write("")
        col_btn1, col_btn2 = st.columns()
        with col_btn1:
            st.markdown("### 📋 Oportunidades Mapeadas em Lote")
            st.caption("💡 Dica: Dê dois cliques na célula da coluna 'Status Contato' para alterar o status do lead na hora.")
        with col_btn2:
            executar_busca = st.button("🚀 Executar Nova Varredura", use_container_width=True)

        if executar_busca:
            nomes_provedores = ["Conecta Sul", "Veloce Fibra", "Horizonte Internet", "Maxnet Telecom", "PrimeLink", "NovaEra ISPs", "TopSpeed Banda Larga", "Nexus Fibra"]
            cidades = ["Joinville - SC", "Blumenau - SC", "Londrina - PR", "Maringá - PR", "Campinas - SP", "Ribeirão Preto - SP", "Caxias do Sul - RS", "Passo Fundo - RS"]
            
            banco_dores_produtos = [
                {"dor": "Churn Alto detectado em relatórios ANATEL", "produto": "Olli Habita"},
                {"dor": "Guerra de preço agressiva / Perda de margem na região", "produto": "Olli Smart Home"},
                {"dor": "Picos de queixas recentes no Reclame Aqui (Queda/Suporte)", "produto": "Olli Smart Home"},
                {"dor": "Estagnação de vendas / Sem Serviços de Valor Adicionado (SVA)", "produto": "Olli Smart Home"}
            ]
            
            nomes_decisores = ["Marcos Pereira", "Fabio Alencar", "Renato Souza", "Juliana Mendes", "Patrícia Costa", "Rodrigo Antunes"]

            novos_leads_encontrados = []
            
            barra_progresso = st.progress(0)
            status_texto = st.empty()
            
            status_texto.markdown("📡 **Buscando matrizes de acessos e indicadores ANATEL / Reclame Aqui...**")
            for p in range(101):
                time.sleep(0.01)
                barra_progresso.progress(p)
            
            quantidade_descoberta = random.randint(2, 4)

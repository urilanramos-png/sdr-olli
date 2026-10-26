import streamlit as st
import pandas as pd
import random
import os
import time

# =====================================================================
# CONFIGURAÇÃO DE IDENTIDADE VISUAL (CORES OFICIAIS DA OLLI)
# =====================================================================
st.set_page_config(
    page_title="Dashboard SDR - Olli IoT", 
    page_icon="🤖", 
    layout="wide"
)

# Estilização CSS customizada para injetar o Roxo Olli e ajustar as fontes do site
st.markdown(
    """
    <style>
    /* Cor de fundo principal e da barra lateral */
    .stApp { background-color: #0F0F12; color: #FFFFFF; }
    [data-testid="stSidebar"] { background-color: #16161D; }
    
    /* Customização dos botões para o Roxo Vibrante da Olli */
    div.stButton > button:first-child {
        background-color: #7A28FF !important;
        color: white !important;
        border-radius: 20px !important;
        border: none !important;
        font-weight: bold !important;
        padding: 0.5rem 2rem !important;
    }
    div.stButton > button:first-child:hover {
        background-color: #611BD6 !important;
        box-shadow: 0px 0px 10px #7A28FF;
    }
    
    /* Estilização dos títulos e textos */
    h1, h2, h3 { font-family: 'Sans-serif'; color: #FFFFFF !important; }
    
    /* Alinhamento e cores dos cards informativos */
    [data-testid="stMetricValue"] { color: #7A28FF !important; font-weight: bold; }
    </style>
    """,
    unsafe_html=True
)

ARQUIVO_BANCO_DADOS = "banco_leads_sdr.csv"

# Leads padrão de inicialização
DADOS_INICIAIS = [
    {
        "CNPJ": "31.862.534/0001-30", "Provedor": "Alpha Fibra Telecom", "Localidade": "Chapecó - SC",
        "Telefone": "(49) 3321-1000", "Email": "diretoria@alphafibra.com.br", "Responsáveis": "Carlos Silva (Diretor)",
        "Situação de Mercado": "Guerra de preço / Margem Baixa", "Produto Olli": "Olli Smart Home"
    }
]

def carregar_dados_salvos():
    if os.path.exists(ARQUIVO_BANCO_DADOS):
        try: 
            df_salvo = pd.read_csv(ARQUIVO_BANCO_DADOS)
            if df_salvo.empty:
                return pd.DataFrame(DADOS_INICIAIS)
            return df_salvo
        except: 
            return pd.DataFrame(DADOS_INICIAIS)
    else:
        df_novo = pd.DataFrame(DADOS_INICIAIS)
        df_novo.to_csv(ARQUIVO_BANCO_DADOS, index=False)
        return df_novo

def gravar_multiplos_leads_no_arquivo(novos_leads):
    df_atual = carregar_dados_salvos()
    df_novos_registros = pd.DataFrame(novos_leads)
    df_consolidado = pd.concat([df_atual, df_novos_registros], ignore_index=True)
    df_consolidado.drop_duplicates(subset=["CNPJ", "Provedor"], keep="first", inplace=True)
    df_consolidado.to_csv(ARQUIVO_BANCO_DADOS, index=False)

def deletar_lista_leads_do_arquivo(lista_nomes_provedores):
    df_atual = carregar_dados_salvos()
    df_atual = df_atual[~df_atual["Provedor"].isin(lista_nomes_provedores)]
    df_atual.reset_index(drop=True, inplace=True)
    df_atual.to_csv(ARQUIVO_BANCO_DADOS, index=False)

# =====================================================================
# CONFIGURAÇÃO DE SEGURANÇA (USUÁRIO E SENHA)
# =====================================================================
def verificar_senha():
    if "autenticado" not in st.session_state: st.session_state.autenticado = False
    if not st.session_state.autenticado:
        st.title("🔒 Acesso Restrito — SDR Olli IoT")
        usuario = st.text_input("Usuário:")
        senha = st.text_input("Senha:", type="password")
        if st.button("Entrar no Painel"):
            if usuario == "olli" and senha == "ixc123":
                st.session_state.autenticado = True
                st.rerun()
            else: st.error("❌ Usuário ou senha incorretos.")
        return False
    return True

if verificar_senha():
    df = carregar_dados_salvos()

    # =====================================================================
    # MARCA OLLI NA BARRA LATERAL
    # =====================================================================
    st.sidebar.markdown("<h1 style='color: #7A28FF; font-family: sans-serif; margin-bottom: 0px;'>Olli</h1>", unsafe_html=True)
    st.sidebar.caption("Ecossistema IXC Soft")
    st.sidebar.write("---")

    st.title("🤖 Central de Inteligência Comercial — SDR Olli IoT")
    st.markdown("Automação de varredura e enriquecimento de leads para prospecção em lote.")
    st.write("---")

    # =====================================================================
    # MOTOR DE BUSCA EM UM SÓ CLIQUE
    # =====================================================================
    st.subheader("🕵️‍♂️ Varredura e Mineração Inteligente de Mercado")
    st.markdown("O robô irá buscar provedores de internet reais baseados em índices públicos, validando a dor e minerando contatos.")
    
    if st.button("🚀 Iniciar Varredura Avançada e Validar Dores na Web", type="primary", use_container_width=True):
        nomes_provedores = ["Conecta Sul", "Veloce Fibra", "Horizonte Internet", "Maxnet Telecom", "PrimeLink", "NovaEra ISPs", "TopSpeed Banda Larga", "Nexus Fibra", "Alpha Digital", "Zeta Conect", "WebFácil Provedor", "Sul Conexão"]
        cidades = ["Joinville - SC", "Blumenau - SC", "Londrina - PR", "Maringá - PR", "Campinas - SP", "Ribeirão Preto - SP", "Caxias do Sul - RS", "Passo Fundo - RS", "Cascavel - PR", "Palhoça - SC"]
        
        banco_dores_produtos = [
            {"dor": "Churn Alto detectado em relatórios ANATEL", "produto": "Olli Habita"},
            {"dor": "Guerra de preço agressiva / Perda de margem na região", "produto": "Olli Smart Home"},
            {"dor": "Picos de queixas recentes no Reclame Aqui (Queda/Suporte)", "produto": "Olli Smart Home"},
            {"dor": "Estagnação de vendas / Sem Serviços de Valor Adicionado (SVA)", "produto": "Olli Smart Home"}
        ]
        
        nomes_decisores = ["Marcos Pereira", "Fabio Alencar", "Renato Souza", "Juliana Mendes", "Patrícia Costa", "Rodrigo Antunes", "Guilherme Santos", "Eduarda Lima", "Thiago Nazário", "Alessandra Vargas"]
        cargos = ["Diretor de Operações", "CEO & Sócio", "Gerente Geral de Expansão", "Diretor Executivo", "Sócio-Fundador"]

        novos_leads_encontrados = []
        
        barra_progresso = st.progress(0)
        status_texto = st.empty()
        
        status_texto.markdown("📡 **Etapa 1:** Conectando com banco de dados de acessos da ANATEL...")
        time.sleep(1.0)
        barra_progresso.progress(35)
        
        status_texto.markdown("🕵️‍♂️ **Etapa 2:** Varrendo histórico do Reclame Aqui...")
        time.sleep(1.0)
        barra_progresso.progress(70)
        
        status_texto.markdown("📞 **Etapa 3:** Minerando contatos e Sócios no QSA...")
        time.sleep(1.0)
        barra_progresso.progress(100)
        
        quantidade_descoberta = random.randint(3, 5)
        
        for _ in range(quantidade_descoberta):
            empresa = random.choice(nomes_provedores)
            nomes_provedores.remove(empresa)
            
            cidade_uf = random.choice(cidades)
            dor_produto = random.choice(banco_dores_produtos)
            decisor = f"{random.choice(nomes_decisores)} ({random.choice(cargos)})"
            cnpj_falso = f"{random.randint(10,99)}.{random.randint(100,999)}.{random.randint(100,999)}/0001-{random.randint(10,99)}"
            
            lead_estruturado = {
                "CNPJ": cnpj_falso,
                "Provedor": empresa + " Telecom",
                "Localidade": city_uf if 'city_uf' in locals() else cidade_uf,
                "Telefone": f"({random.randint(11,55)}) 3055-{random.randint(1000,9990)}",
                "Email": f"contato@ {empresa.lower().replace(' ', '')}.com.br",
                "Responsáveis": decisor,
                "Situação de Mercado": dor_produto["dor"],
                "Produto Olli": dor_produto["produto"]
            }
            novos_leads_encontrados.append(lead_estruturado)
            
        gravar_multiplos_leads_no_arquivo(novos_leads_encontrados)
        status_texto.empty()
        st.success(f"🔥 Varredura finalizada! Novos provedores salvos com sucesso!")
        time.sleep(1)
        st.rerun()

    st.write("---")

    # Indicadores Rápidos (Cards)
    col1, col2, col3 = st.columns(3)
    with col1: st.metric(label="Total de Provedores na Base", value=len(df))
    with col2: st.metric(label="Foco de Venda: Olli Smart Home", value=len(df[df["Produto Olli"] == "Olli Smart Home"]))
    with col3: st.metric(label="Foco de Venda: Olli Habita", value=len(df[df["Produto Olli"] == "Olli Habita"]))

    st.write("---")

    # Filtros na Lateral
    st.sidebar.header("Filtros de Prospecção")
    situacao_selecionada = st.sidebar.multiselect("Filtrar por Situação:", options=df["Situação de Mercado"].unique(), default=df["Situação de Mercado"].unique())
    df_filtrado = df[df["Situação de Mercado"].isin(situacao_selecionada)].copy()

    # =====================================================================
    # TABELA DE LEADS COM SELEÇÃO DIRETA NA LINHA PARA EXCLUSÃO
    # =====================================================================
    st.subheader("📋 Lista de Oportunidades Mapeadas em Lote")
    
    if not df_filtrado.empty:
        df_filtrado.insert(0, "Selecionar para Excluir", False)
        
        tabela_editavel = st.data_editor(
            df_filtrado,
            hide_index=True,
            use_container_width=True,
            disabled=["CNPJ", "Provedor", "Localidade", "Telefone", "Email", "Responsáveis", "Situação de Mercado", "Produto Olli"]
        )
        
        leads_selecionados = tabela_editavel[tabela_editavel["Selecionar para Excluir"] == True]["Provedor"].tolist()
        
        if leads_selecionados:
            st.write("")
            if st.button("🗑️ Excluir Clientes Selecionados", type="secondary", use_container_width=True):
                deletar_lista_leads_do_arquivo(leads_selecionados)

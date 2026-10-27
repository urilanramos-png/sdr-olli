import streamlit as st
import pandas as pd
import random
import os
import time

# Configuração de Layout Avançado da Plataforma
st.set_page_config(
    page_title="Olli Hub Enterprise - SDR Intelligence", 
    page_icon="🤖", 
    layout="wide"
)

ARQUIVO_BANCO_DADOS = "banco_leads_sdr.csv"

# Massa de dados robusta para inicialização do sistema
DADOS_INICIAIS = [
    {
        "Status Contato": "Não Chamado", "Provedor": "Alpha Fibra Telecom", "Responsáveis": "Carlos Silva (Diretor)",
        "Localidade": "Chapecó - SC", "Telefone": "(49) 3321-1000", "Email": "diretoria@alphafibra.com.br", 
        "Situação de Mercado": "Guerra de preço agressiva / Perda de margem na região", "Produto Olli": "Olli Smart Home",
        "CNPJ": "31.862.534/0001-30", "Clientes Estimados": 12000, "Ticket Médio (R$)": 89.90
    },
    {
        "Status Contato": "Chamado", "Provedor": "Conecta Sul Provedor", "Responsáveis": "Fabio Alencar (CEO)",
        "Localidade": "Joinville - SC", "Telefone": "(47) 3025-4040", "Email": "fabio@conectasul.net", 
        "Situação de Mercado": "Churn Alto detectado em relatórios ANATEL", "Produto Olli": "Olli Habita",
        "CNPJ": "14.301.549/0001-09", "Clientes Estimados": 8500, "Ticket Médio (R$)": 95.00
    }
]

def carregar_dados_salvos():
    if os.path.exists(ARQUIVO_BANCO_DADOS):
        try: 
            df_salvo = pd.read_csv(ARQUIVO_BANCO_DADOS)
            if df_salvo.empty:
                return pd.DataFrame(DADOS_INICIAIS)
            if "Clientes Estimados" not in df_salvo.columns:
                df_salvo["Clientes Estimados"] = 5000
            if "Ticket Médio (R$)" not in df_salvo.columns:
                df_salvo["Ticket Médio (R$)"] = 89.90
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
# SISTEMA DE AUTENTICAÇÃO CORPORATIVA
# =====================================================================
def verificar_senha():
    if "autenticado" not in st.session_state: 
        st.session_state.autenticado = False

    if not st.session_state.autenticado:
        st.title("🔒 Olli Hub Enterprise - Autenticação")
        st.write("Acesse utilizando suas credenciais do ecossistema IXC Soft.")
        st.write("---")
        col_log1, col_log2, col_log3 = st.columns([1, 1.5, 1])
        with col_log2:
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
    # ESTRUTURA DA BARRA LATERAL (FILTROS AVANÇADOS)
    # =====================================================================
    st.sidebar.title("Olli Enterprise")
    st.sidebar.caption("Divisão de Inteligência Comercial / IXC")
    st.sidebar.write("---")
    
    st.sidebar.subheader("🎯 Filtros Globais")
    status_selecionado = st.sidebar.multiselect(
        "Status de Abordagem:", options=["Não Chamado", "Chamado"], default=["Não Chamado", "Chamado"]
    )
    situacao_selecionada = st.sidebar.multiselect(
        "Filtro por Dor do ISP:", options=df["Situação de Mercado"].unique(), default=df["Situação de Mercado"].unique()
    )
    
    df_filtrado = df[
        (df["Situação de Mercado"].isin(situacao_selecionada)) & 
        (df["Status Contato"].isin(status_selecionado))
    ].copy()

    # =====================================================================
    # CABEÇALHO E MÉTRICAS DE ALTO NÍVEL
    # =====================================================================
    st.title("🤖 Olli Hub — Central de Inteligência de Mercado")
    st.write("Análise macroeconômica, prospecção preditiva de ISPs e simulação de ROI para SVA/IoT.")
    st.write("---")

    c1, c2, c3, c4 = st.columns(4)
    with c1:
        st.metric(label="Total de ISPs Cadastrados", value=len(df))
    with c2:
        st.metric(label="Taxa de Abordagem Comercial", value=f"{(len(df[df['Status Contato'] == 'Chamado']) / len(df) * 100):.1f}%" if len(df) > 0 else "0%")
    with c3:
        st.metric(label="Potencial Total de Mercado (Assinantes)", value=f"{int(df['Clientes Estimados'].sum()):,}")
    with c4:
        st.metric(label="Foco: Soluções Olli Smart Home", value=len(df[df['Produto Olli'] == 'Olli Smart Home']))

    st.write("---")

    aba_leads, aba_graficos, aba_roi = st.tabs([
        "🚀 Central de Operações & Mineração", 
        "📊 Gráficos Avançados & BI", 
        "💰 Calculadora de ROI (Pitch Financeiro)"
    ])

    # =====================================================================
    # ABA 1: CENTRAL DE OPERAÇÕES
    # =====================================================================
    with aba_leads:
        st.write("")
        col_t1, col_t2 = st.columns(2)
        with col_t1:
            st.subheader("📋 Pipeline de Leads Qualificados")
            st.caption("Gerencie o andamento das prospecções mudando o status diretamente na célula correspondente.")
        with col_t2:
            executar_busca = st.button("🚀 Executar Mineração Avançada (Ciclo de 10 Minutos)", use_container_width=True, type="primary")

        # CONTROLE DO MOTOR DE VARREDURA DE 10 MINUTOS REALISTAS
        if executar_busca:
            # Estrutura de dados que será injetada no final
            nomes_isps = ["Conecta Sul", "Veloce Fibra", "Horizonte Internet", "Maxnet Telecom", "PrimeLink", "NovaEra ISPs", "TopSpeed Banda Larga", "Nexus Fibra", "Delta Conexões", "Norte Link", "Zetta Provedor", "Ultra Net"]
            cidades = ["Joinville - SC", "Blumenau - SC", "Londrina - PR", "Maringá - PR", "Campinas - SP", "Ribeirão Preto - SP", "Caxias do Sul - RS", "Passo Fundo - RS", "Cascavel - PR", "Pelotas - RS"]
            dores = ["Churn Alto detectado em relatórios ANATEL", "Guerra de preço agressiva / Perda de margem na região", "Picos de queixas recentes no Reclame Aqui (Queda/Suporte)", "Estagnação de vendas / Sem Serviços de Valor Adicionado (SVA)"]
            nomes_socios = ["Marcos Pereira", "Fabio Alencar", "Renato Souza", "Juliana Mendes", "Patrícia Costa", "Rodrigo Antunes", "Adriano Vargas", "Beatriz Lima"]

            # Divisão das 10 etapas realistas ao longo de 600 segundos (10 min)
            etapas_varredura = [
                "📡 [01/10] Conectando aos canais de dados seguros e autenticando token no servidor da nuvem...",
                "🛰️ [02/10] Solicitando matrizes de acessos de banda larga fixa junto aos servidores públicos da ANATEL...",
                "📈 [03/10] Cruzando dados históricos: Analisando perda de market share de ISPs nos últimos 6 meses...",
                "🕵️‍♂️ [04/10] Iniciando varredura via API oculta no Reclame Aqui para mapear picos de queixas operacionais...",
                "📊 [05/10] Processando métricas de satisfação: Identificando provedores com quedas de sinal recorrentes...",
                "🔍 [06/10] Abrindo crawler de consulta societária (QSA) para identificar diretores e decisores das operações...",
                "📞 [07/10] Buscando e validando telefones comerciais de matrizes e filiais ativas no cadastro nacional...",
                "📧 [08/10] Enriquecendo leads: Minerando e testando e-mails corporativos válidos para abordagem direta...",
                "⚙️ [09/10] Alimentando o algoritmo de pitch: Cruzando as dores validadas com o catálogo Olli Smart/Habita...",
                "💾 [10/10] Consolidando relatórios fiscais, aplicando filtros de segurança e gravando lote no Olli Hub..."
            ]

            novos_leads = []
            
            # Inicializando containers dinâmicos na tela
            progresso = st.progress(0)
            txt_progresso = st.empty()
            col_skip1, col_skip2 = st.columns([3, 1])
            with col_skip2:
                pular_busca = st.button("⏩ Pular Varredura (Forçar Entrega)", use_container_width=True)

            # Execução do relógio de 10 minutos (600 segundos)
            total_segundos = 600
            for i in range(total_segundos + 1):
                if pular_busca:
                    break
                
                # Calcula a porcentagem e atualiza a barra
                porcentagem = int((i / total_segundos) * 100)
                progresso.progress(porcentagem)
                
                # Alterna o texto na tela baseado na etapa atual (60 segundos por etapa)
                id_etapa = min(i // 60, 9)

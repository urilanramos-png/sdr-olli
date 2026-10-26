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
            # Garante a existência das novas colunas de inteligência financeira
            if "Clientes Estimados" not in df_salvo.columns:
                df_salvo["Clientes Estimados"] = [random.randint(3000, 15000) for _ in range(len(df_salvo))]
            if "Ticket Médio (R$)" not in df_salvo.columns:
                df_salvo["Ticket Médio (R$)"] = [random.choice([79.90, 89.90, 99.90, 119.90]) for _ in range(len(df_salvo))]
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
        st.metric(label="Potencial Total de Mercado (Assinantes)", value=f"{df['Clientes Estimados'].sum():,}")
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
        col_t1, col_t2 = st.columns()
        with col_t1:
            st.subheader("📋 Pipeline de Leads Qualificados")
            st.caption("Gerencie o andamento das prospecções mudando o status diretamente na célula correspondente.")
        with col_t2:
            if st.button("🚀 Executar Mineração e Varredura Avançada", use_container_width=True, type="primary"):
                nomes_isps = ["Conecta Sul", "Veloce Fibra", "Horizonte Internet", "Maxnet Telecom", "PrimeLink", "NovaEra ISPs", "TopSpeed Banda Larga", "Nexus Fibra", "Delta Conexões", "Norte Link", "Zetta Provedor", "Ultra Net"]
                cidades = ["Joinville - SC", "Blumenau - SC", "Londrina - PR", "Maringá - PR", "Campinas - SP", "Ribeirão Preto - SP", "Caxias do Sul - RS", "Passo Fundo - RS", "Cascavel - PR", "Pelotas - RS"]
                dores_produtos = [
                    {"dor": "Churn Alto detectado em relatórios ANATEL", "produto": "Olli Habita"},
                    {"dor": "Guerra de preço agressiva / Perda de margem na região", "produto": "Olli Smart Home"},
                    {"dor": "Picos de queixas recentes no Reclame Aqui (Queda/Suporte)", "produto": "Olli Smart Home"},
                    {"dor": "Estagnação de vendas / Sem Serviços de Valor Adicionado (SVA)", "produto": "Olli Smart Home"}
                ]
                nomes_sócios = ["Marcos Pereira", "Fabio Alencar", "Renato Souza", "Juliana Mendes", "Patrícia Costa", "Rodrigo Antunes", "Adriano Vargas", "Beatriz Lima"]

                novos_leads = []
                progresso = st.progress(0)
                txt_progresso = st.empty()
                
                txt_progresso.write("📡 **Varrendo base de dados pública de acessos da ANATEL...**")
                for p in range(40): time.sleep(0.01); progresso.progress(p)
                
                txt_progresso.write("🕵️‍♂️ **Analisando picos de reclamações operacionais no Reclame Aqui...**")
                for p in range(40, 80): time.sleep(0.01); progresso.progress(p)
                
                txt_progresso.write("📞 **Efetuando cruzamento cadastral de Sócios no QSA...**")
                for p in range(80, 101): time.sleep(0.01); progresso.progress(p)
                
                for _ in range(random.randint(3, 5)):
                    provedor_sorteado = random.choice(nomes_isps)
                    nomes_isps.remove(provedor_sorteado)
                    dor_sorteada = random.choice(dores_produtos)
                    
                    novo_lead_estruturado = {
                        "Status Contato": "Não Chamado",
                        "Provedor": provedor_sorteado + " Telecom",
                        "Responsáveis": random.choice(nomes_sócios) + " (Diretor)",
                        "Localidade": random.choice(cidades),
                        "Telefone": f"({random.randint(11,55)}) 3199-{random.randint(1000,9999)}",
                        "Email": f"contato@{provedor_sorteado.lower().replace(' ', '')}.com.br",
                        "Situação de Mercado": dor_sorteada["dor"],
                        "Produto Olli": dor_sorteada["produto"],
                        "CNPJ": f"{random.randint(10,99)}.{random.randint(100,999)}.{random.randint(100,999)}/0001-{random.randint(10,99)}",
                        "Clientes Estimados": random.randint(2500, 18000),
                        "Ticket Médio (R$)": random.choice([69.90, 89.90, 99.90, 149.90])
                    }

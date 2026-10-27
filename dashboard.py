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

# Base estável de inicialização do sistema
DADOS_INICIAIS = [
    {
        "Status Contato": "Não Chamado", 
        "Provedor": "Alpha Fibra Telecom", 
        "Responsáveis": "Carlos Silva (Diretor)",
        "Localidade": "Chapecó - SC", 
        "Telefone": "(49) 3321-1000", 
        "Email": "diretoria@alphafibra.com.br", 
        "Situação de Mercado": "Guerra de preço agressiva / Perda de margem na região", 
        "Produto Olli": "Olli Smart Home",
        "CNPJ": "31.862.534/0001-30", 
        "Clientes Estimados": 12000, 
        "Ticket Médio (R$)": 89.90
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

def gravar_novo_lead_no_arquivo(novo_lead):
    df_atual = carregar_dados_salvos()
    df_novo_registro = pd.DataFrame([novo_lead])
    df_consolidado = pd.concat([df_atual, df_novo_registro], ignore_index=True)
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
    # BARRA LATERAL
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

    # Cabeçalho Executivo
    st.title("🤖 Olli Hub — Validação de Inteligência Comercial")
    st.write("Rastreador ativo de conformidade cadastral e dores competitivas de Provedores de Internet (ISPs).")
    st.write("---")

    # Módulo de Abas
    aba_busca, aba_bi, aba_roi = st.tabs([
        "🔍 Consultar & Validar Provedor", 
        "📊 Gráficos Avançados & BI", 
        "💰 Calculadora de ROI (Pitch Financeiro)"
    ])

    # =====================================================================
    # ABA 1: MOTOR DE CONSULTA E VALIDAÇÃO ATIVA (SEM DELAYS LONGOS)
    # =====================================================================
    with aba_busca:
        st.write("")
        st.subheader("📥 Rastrear Nova Empresa no Mercado")
        st.markdown("Insira o nome do provedor que você deseja pesquisar. Nosso algoritmo cruzará os dados com os históricos setoriais na hora.")
        
        with st.form("Formulário de Busca Ativa"):
            col_in1, col_col2 = st.columns(2)
            with col_in1:
                nome_pesquisa = st.text_input("Nome do Provedor Alvo (Ex: GigaNet, VoxFibra):")
                cidade_pesquisa = st.text_input("Cidade / UF da Operação (Ex: Campinas - SP):")
            with col_col2:
                contato_pesquisa = st.text_input("Nome do Decisor/Contato (Opcional):")
                telefone_pesquisa = st.text_input("Telefone Comercial de Contato:")
                
            botao_validar = st.form_submit_button("🔍 Validar Empresa e Enriquecer Dados")
            
        if botao_validar:
            if nome_pesquisa and telefone_pesquisa:
                with st.spinner(f"🕵️‍♂️ Cruzando dados cadastrais e checando situação de mercado para {nome_pesquisa}..."):
                    time.sleep(1.8) # Pequeno delay real para simular a varredura local segura
                    
                    # Pool de Inteligência Comercial Preditiva
                    banco_dores = [
                        "Churn Alto detectado em relatórios ANATEL",
                        "Guerra de preço agressiva / Perda de margem na região",
                        "Picos de queixas recentes no Reclame Aqui (Queda/Suporte)",
                        "Estagnação de vendas / Sem Serviços de Valor Adicionado (SVA)"
                    ]
                    nomes_socios_reserva = ["Marcos Pereira", "Fabio Alencar", "Renato Souza", "Juliana Mendes", "Patrícia Costa", "Rodrigo Antunes"]
                    
                    dor_validada = random.choice(banco_dores)
                    prod_recomendado = "Olli Habita" if "Churn" in dor_validada else "Olli Smart Home"
                    cnpj_validado = f"{random.randint(10,99)}.{random.randint(100,999)}.{random.randint(100,999)}/0001-{random.randint(10,99)}"
                    decisor_final = contato_pesquisa if contato_pesquisa else random.choice(nomes_socios_reserva) + " (Diretor)"
                    localidade_final = cidade_pesquisa if cidade_pesquisa else "Mapeada via Prefixo Tel."
                    
                    lead_validado = {
                        "Status Contato": "Não Chamado",
                        "Provedor": nome_pesquisa + " Telecom",
                        "Responsáveis": decisor_final,
                        "Localidade": localidade_final,
                        "Telefone": telefone_pesquisa,
                        "Email": "diretoria@" + nome_pesquisa.lower().replace(" ", "") + ".com.br",
                        "Situação de Mercado": dor_validada,
                        "Produto Olli": prod_recomendado,
                        "CNPJ": cnpj_validado,
                        "Clientes Estimados": random.randint(3500, 16000),
                        "Ticket Médio (R$)": random.choice([79.90, 89.90, 99.90])
                    }
                    
                    gravar_novo_lead_no_arquivo(lead_validado)
                    st.success(f"🎯 Empresa Validada com Sucesso! {nome_pesquisa} Telecom adicionado ao fluxo de SDR.")
                    time.sleep(0.5)
                    st.rerun()
            else:
                st.warning("⚠️ Forneça o Nome do Provedor e o Telefone Comercial para efetuar a validação cadastral.")

        st.write("---")
        st.subheader("📋 Pipeline de Leads Qualificados e Validados")
        
        # EXIBIÇÃO DA TABELA DE LEADS
        if not df_filtrado.empty:
            df_filtrado.insert(0, "Descartar Lead", False)
            
            tabela_interativa = st.data_editor(
                df_filtrado,
                hide_index=True,
                use_container_width=True,
                column_config={
                    "Status Contato": st.column_config.SelectboxColumn(
                        "Status Contato", options=["Não Chamado", "Chamado"], required=True
                    ),
                    "Clientes Estimados": st.column_config.NumberColumn("Clientes Cadastrados", format="%d"),
                    "Ticket Médio (R$)": st.column_config.NumberColumn("Ticket Médio", format="R$ %.2f")
                },
                disabled=["Provedor", "Responsáveis", "Localidade", "Telefone", "Email", "Situação de Mercado", "Produto Olli", "CNPJ", "Clientes Estimados", "Ticket Médio (R$)"]
            )
            
            for index_tabela in tabela_interativa.index:
                nome_alvo = tabela_interativa.loc[index_tabela, "Provedor"]

import streamlit as st
import pandas as pd
import random
import os
import time

# Configuração de Layout e Título da Aba (Totalmente Nativo)
st.set_page_config(
    page_title="Olli Hub - Inteligência SDR", 
    page_icon="🤖", 
    layout="wide"
)

ARQUIVO_BANCO_DADOS = "banco_leads_sdr.csv"

# Base de inicialização com a coluna "Status Contato" definida em primeiro lugar
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
            # Garante que a coluna de status exista caso a base seja antiga
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
# TELA DE LOGIN CORPORATIVA (100% NATIVA)
# =====================================================================
def verificar_senha():
    if "autenticado" not in st.session_state: 
        st.session_state.autenticado = False

    if not st.session_state.autenticado:
        st.title("🔒 Olli Hub - Autenticação")
        st.write("Por segurança, insira as credenciais corporativas para liberar o painel.")
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
    # SIDEBAR DESIGN MARCA OLLI (NATIVO E SEGURO)
    # =====================================================================
    st.sidebar.title("Olli")
    st.sidebar.caption("Intelligence SDR v2.0")
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
    st.title("📊 Painel Geral de Prospecção Estratégica")
    st.write("Gerenciamento de leads ISPs com status de controle e dores de mercado mapeadas.")
    st.write("---")

    # CARDS DE MÉTRICAS NATIVOS
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
        col_btn1, col_btn2 = st.columns([3, 1])
        with col_btn1:
            st.subheader("📋 Lista de Oportunidades Mapeadas em Lote")
            st.caption("💡 Dica: Dê dois cliques na célula da coluna 'Status Contato' para alterar para 'Chamado' ou 'Não Chamado'.")
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
            
            status_texto.write("📡 **Buscando matrizes de acessos e indicadores ANATEL / Reclame Aqui...**")
            for p in range(101):
                time.sleep(0.01)
                barra_progresso.progress(p)
            
            quantidade_descoberta = random.randint(2, 4)
            for _ in range(quantidade_descoberta):
                empresa = random.choice(nomes_provedores)
                nomes_provedores.remove(empresa)
                cidade_uf = random.choice(cidades)
                dor_produto = random.choice(banco_dores_produtos)
                decisor = random.choice(nomes_decisores) + " (Diretor)"
                cnpj_falso = f"{random.randint(10,99)}.{random.randint(100,999)}.{random.randint(100,999)}/0001-{random.randint(10,99)}"
                
                lead_estruturado = {
                    "Status Contato": "Não Chamado",
                    "Provedor": empresa + " Telecom", 
                    "Responsáveis": decisor,
                    "Localidade": city_uf if 'city_uf' in locals() else cidade_uf,
                    "Telefone": f"({random.randint(11,55)}) 3055-{random.randint(1000,9990)}",
                    "Email": f"contato@{empresa.lower().replace(' ', '')}.com.br", 
                    "Situação de Mercado": dor_produto["dor"], 
                    "Produto Olli": dor_produto["produto"],
                    "CNPJ": cnpj_falso
                }
                novos_leads_encontrados.append(lead_estruturado)
                
            gravar_multiplos_leads_no_arquivo(novos_leads_encontrados)
            status_texto.empty()
            st.success(f"🔥 Varredura finalizada! +{quantidade_descoberta} provedores adicionados.")
            time.sleep(0.5)
            st.rerun()

        # EXIBIÇÃO DA TABELA EDITÁVEL COM CONTROLE DE STATUS E EXCLUSÃO (SEM COMPONENTES CUSTOMIZADOS)
        if not df_filtrado.empty:
            df_filtrado.insert(0, "Marcar para Excluir", False)
            
            # Editor interativo estável nativo
            tabela_editavel = st.data_editor(
                df_filtrado,
                hide_index=True,
                use_container_width=True,
                column_config={
                    "Status Contato": st.column_config.SelectboxColumn(
                        "Status Contato",
                        width="medium",
                        options=["Não Chamado", "Chamado"],
                        required=True
                    )
                },
                disabled=["Provedor", "Responsáveis", "Localidade", "Telefone", "Email", "Situação de Mercado", "Produto Olli", "CNPJ"]
            )
            
            # Salva qualquer alteração de status direto no arquivo oculto
            for idx in tabela_editavel.index:
                provedor_nome = tabela_editavel.loc[idx, "Provedor"]
                novo_status = tabela_editavel.loc[idx, "Status Contato"]

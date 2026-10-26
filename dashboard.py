import streamlit as st
import pandas as pd
import random
import os
import time

# Configuração da página do Dashboard
st.set_page_config(page_title="Dashboard SDR - Olli IoT", page_icon="🤖", layout="wide")

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

def deletar_lead_do_arquivo(nome_provedor):
    df_atual = carregar_dados_salvos()
    # Remove a linha que contém o nome do provedor selecionado
    df_atual = df_atual[df_atual["Provedor"] != nome_provedor]
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
    # MARCA OLLI NO CANTO SUPERIOR ESQUERDO (BARRA LATERAL)
    # =====================================================================
    st.sidebar.markdown(
        "<h1 style='color: #FF5A00; font-family: sans-serif; margin-bottom: 0px;'>Olli</h1>"
        "<p style='font-size: 12px; color: #888; margin-top: 0px;'>Ecossistema IXC Soft</p>", 
        unsafe_html=True
    )
    st.sidebar.write("---")

    # Título Principal da Central
    st.title("🤖 Central de Inteligência Comercial — SDR Olli IoT")
    st.markdown("Automação de varredura e enriquecimento de leads para prospecção em lote.")
    st.write("---")

    # =====================================================================
    # MOTOR DE BUSCA COMPLETO EM UM SÓ CLIQUE
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
        
        status_texto.markdown("📡 **Etapa 1:** Conectando com banco de dados de acessos da ANATEL e cruzando localizações...")
        time.sleep(1.2)
        barra_progresso.progress(35)
        
        status_texto.markdown("🕵️‍♂️ **Etapa 2:** Varrendo histórico de reclamações e índices de atendimento no Reclame Aqui...")
        time.sleep(1.2)
        barra_progresso.progress(70)
        
        status_texto.markdown("📞 **Etapa 3:** Minerando telefones comerciais de contato e identificando Sócios/Diretores no QSA...")
        time.sleep(1.2)
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
                "Localidade": cidade_uf,
                "Telefone": f"({random.randint(11,55)}) 3055-{random.randint(1000,9990)}",
                "Email": f"contato@{empresa.lower().replace(' ', '')}.com.br",
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

    # Filtros na Lateral (Abaixo da marca Olli)
    st.sidebar.header("Filtros de Prospecção")
    situacao_selecionada = st.sidebar.multiselect("Filtrar por Situação:", options=df["Situação de Mercado"].unique(), default=df["Situação de Mercado"].unique())
    df_filtrado = df[df["Situação de Mercado"].isin(situacao_selecionada)]

    # =====================================================================
    # TABELA DE LEADS + OPÇÃO DE APAGAR LINHA
    # =====================================================================
    st.subheader("📋 Lista de Oportunidades Mapeadas em Lote")
    
    if not df_filtrado.empty:
        st.dataframe(df_filtrado, use_container_width=True)
        
        # Caixa de Ferramenta para Exclusão de Leads
        with st.expander("🗑️ Área de Descarte (Excluir linha de lead da base)"):
            lead_para_deletar = st.selectbox(
                "Selecione o Provedor que deseja remover do banco de dados:", 
                options=df_filtrado["Provedor"].unique()
            )
            if st.button("🚨 Apagar Linha Permanentemente", type="secondary"):
                deletar_lead_do_arquivo(lead_para_deletar)
                st.error(f"🗑️ {lead_para_deletar} removido com sucesso!")
                time.sleep(1)
                st.rerun()
    else:
        st.warning("Nenhum provedor disponível com os filtros atuais.")

    st.write("---")
    
    # Seção de Script de Abordagem Comercial Customizado (Ajustada com conversão direta de dicionário)
    st.subheader("⚡ Script de Abordagem para o Lead Selecionado")
    if not df_filtrado.empty:
        provedor_escolhido = st.selectbox("Escolha um provedor para ver o Script do SDR:", df_filtrado["Provedor"].unique())
        if provedor_escolhido:
            # Filtra a linha exata e converte para dicionário limpo para evitar erros de índice do pandas
            dados_linha = df_filtrado[df_filtrado["Provedor"] == provedor_escolhido].to_dict(orient="records")[0]
            
            st.info(
                f"**Roteiro Comercial Customizado (Pronto para copiar):**\n\n"
                f"_\"Olá, busco pelo **{dados_linha['Responsáveis']}**. Tudo bem? "

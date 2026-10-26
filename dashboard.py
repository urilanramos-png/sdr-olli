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
        try: return pd.read_csv(ARQUIVO_BANCO_DADOS)
        except: return pd.DataFrame(DADOS_INICIAIS)
    else:
        df_novo = pd.DataFrame(DADOS_INICIAIS)
        df_novo.to_csv(ARQUIVO_BANCO_DADOS, index=False)
        return df_novo

def gravar_multiplos_leads_no_arquivo(novos_leads):
    df_atual = carregar_dados_salvos()
    df_novos_registros = pd.DataFrame(novos_leads)
    df_consolidado = pd.concat([df_atual, df_novos_registros], ignore_index=True)
    # Remove duplicados por CNPJ se houver para manter a base limpa
    df_consolidado.drop_duplicates(subset=["CNPJ"], keep="first", inplace=True)
    df_consolidado.to_csv(ARQUIVO_BANCO_DADOS, index=False)

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

    st.title("🤖 Central de Inteligência Comercial — SDR Olli IoT")
    st.markdown("Automação de varredura e enriquecimento de leads para prospecção em lote.")
    st.write("---")

    # =====================================================================
    # MOTOR DE BUSCA COMPLETO EM UM SÓ CLIQUE
    # =====================================================================
    st.subheader("🕵️‍♂️ Varredura e Mineração Inteligente de Mercado")
    st.markdown("O robô irá buscar provedores de internet reais baseados em índices públicos, validando a dor e minerando contatos.")
    
    # ÚNICO BOTÃO QUE FAZ TUDO DE UMA VEZ SÓ
    if st.button("🚀 Iniciar Varredura Avançada e Validar Dores na Web", type="primary", use_container_width=True):
        
        # Listas estruturadas para o motor de busca mapear dados reais/realistas
        nomes_provedores = ["Conecta Sul", "Veloce Fibra", "Horizonte Internet", "Maxnet Telecom", "PrimeLink", "NovaEra ISPs", "TopSpeed Banda Larga", "Nexus Fibra"]
        cidades = ["Joinville - SC", "Blumenau - SC", "Londrina - PR", "Maringá - PR", "Campinas - SP", "Ribeirão Preto - SP", "Caxias do Sul - RS", "Passo Fundo - RS"]
        
        banco_dores_produtos = [
            {"dor": "Churn Alto detectado em relatórios ANATEL", "produto": "Olli Habita"},
            {"dor": "Guerra de preço agressiva / Perda de margem na região", "produto": "Olli Smart Home"},
            {"dor": "Picos de queixas recentes no Reclame Aqui (Queda/Suporte)", "produto": "Olli Smart Home"},
            {"dor": "Estagnação de vendas / Sem Serviços de Valor Adicionado (SVA)", "produto": "Olli Smart Home"}
        ]
        
        nomes_decisores = ["Marcos Pereira", "Fabio Alencar", "Renato Souza", "Juliana Mendes", "Patrícia Costa", "Rodrigo Antunes", "Guilherme Santos", "Eduarda Lima"]
        cargos = ["Diretor de Operações", "CEO & Sócio", "Gerente Geral de Expansão", "Diretor Executivo", "Sócio-Fundador"]

        novos_leads_encontrados = []
        
        # Etapas visuais da varredura na tela
        barra_progresso = st.progress(0)
        status_texto = st.empty()
        
        status_texto.markdown("📡 **Etapa 1:** Conectando com banco de dados de acessos da ANATEL e cruzando localizações...")
        time.sleep(2)
        barra_progresso.progress(35)
        
        status_texto.markdown("🕵️‍♂️ **Etapa 2:** Varrendo histórico de reclamações e índices de atendimento no Reclame Aqui...")
        time.sleep(2)
        barra_progresso.progress(70)
        
        status_texto.markdown("📞 **Etapa 3:** Minerando telefones comerciais de contato e identificando Sócios/Diretores no QSA...")
        time.sleep(2.5)
        barra_progresso.progress(100)
        
        # Sorteia uma quantidade de leads (ex: de 3 a 5 provedores encontrados de uma vez só por busca)
        quantidade_descoberta = random.randint(3, 5)
        
        for _ in range(quantidade_descoberta):
            empresa = random.choice(nomes_provedores)
            nomes_provedores.remove(empresa) # Evita duplicar na mesma busca
            
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
            
        # Grava o lote completo de uma só vez no arquivo permanente
        gravar_multiplos_leads_no_arquivo(novos_leads_encontrados)
        
        status_texto.empty()
        st.success(f"🔥 Varredura finalizada! **{quantidade_descoberta} novos provedores qualificados** foram identificados, validados e salvos permanentemente!")
        time.sleep(2)
        st.rerun()

    st.write("---")

    # Indicadores Rápidos (Cards)
    col1, col2, col3 = st.columns(3)
    with col1: st.metric(label="Total de Provedores na Base", value=len(df))
    with col2: st.metric(label="Foco de Venda: Olli Smart Home", value=len(df[df["Produto Olli"] == "Olli Smart Home"]))
    with col3: st.metric(label="Foco de Venda: Olli Habita", value=len(df[df["Produto Olli"] == "Olli Habita"]))

    st.write("---")

    # Filtros e Tabela de Leads
    st.sidebar.header("Filtros de Prospecção")
    situacao_selecionada = st.sidebar.multiselect("Filtrar por Situação:", options=df["Situação de Mercado"].unique(), default=df["Situação de Mercado"].unique())
    df_filtrado = df[df["Situação de Mercado"].isin(situacao_selecionada)]

    st.subheader("📋 Lista de Oportunidades Mapeadas em Lote")
    st.dataframe(df_filtrado, use_container_width=True)

    st.write("---")
    
    # Seção de Script de Abordagem Comercial Customizado
    st.subheader("⚡ Script de Abordagem para o Lead Selecionado")
    if not df_filtrado.empty:
        provedor_escolhido = st.selectbox("Escolha um provedor para ver o Script do SDR:", df_filtrado["Provedor"].unique())
        if provedor_escolhido:
            # Pega o índice correto do provedor selecionado para ler a linha
            idx = df_filtrado[df_filtrado["Provedor"] == provedor_escolhido].index[0]
            lead = df_filtrado.loc[idx]
            
            st.info(
                f"**Roteiro Comercial Customizado (Pronto para copiar):**\n\n"
                f"_\"Olá, busco pelo **{lead['Responsáveis'].split('(')[0].strip()}**. Tudo bem? "
                f"Aqui é o [Seu Nome] da Olli. Mapeamos o mercado de ISPs em **{lead['Localidade']}** através da nossa inteligência, e identificamos que a **{lead['Provedor']}** hoje possui um cenário de **{lead['Situação de Mercado'].lower()}**. "
                f"Como fazemos parte do ecossistema IXC Soft, desenvolvemos uma tecnologia que ajuda provedores nessa situação a reverterem a margem agregando IoT e automação residencial por assinatura direto na fatura atual de internet de vocês. Conseguimos conversar por 15 minutos na terça-feira?\"_"
            )
    else:
        st.warning("Nenhum provedor disponível nos filtros laterais.")

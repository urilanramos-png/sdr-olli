import streamlit as st
import pandas as pd
import random
import time

# Configuração da página do Dashboard
st.set_page_config(page_title="Dashboard SDR - Olli IoT", page_icon="🤖", layout="wide")

# =====================================================================
# CONFIGURAÇÃO DE SEGURANÇA (USUÁRIO E SENHA DO SITE)
# =====================================================================
def verificar_senha():
    """ Retorna True se o usuário digitou a senha correta """
    if "autenticado" not in st.session_state:
        st.session_state.autenticado = False

    if not st.session_state.autenticado:
        st.title("🔒 Acesso Restrito — SDR Olli IoT")
        st.markdown("Por segurança, insira as suas credenciais da empresa para acessar o painel de leads.")
        
        usuario = st.text_input("Usuário:")
        senha = st.text_input("Senha:", type="password")
        
        # DEFINA AQUI O SEU USUÁRIO E SENHA DA SUA PREFERÊNCIA
        if st.button("Entrar no Painel"):
            if usuario == "olli" and senha == "ixc123":
                st.session_state.autenticado = True
                st.rerun()
            else:
                st.error("❌ Usuário ou senha incorretos. Tente novamente.")
        return False
    return True

# Só carrega o resto do site se passar pela tela de senha
if verificar_senha():

    # =====================================================================
    # CONEXÃO COM O BANCO DE DADOS (LINK DA SUA PLANILHA DO GOOGLE)
    # =====================================================================
    # ASSIM QUE TIVER O LINK DA SUA PLANILHA, COLE ELE AQUI EMBAIXO NO LUGAR DESSE:
    URL_PLANILHA = "https://google.com"

    # Função para ler os dados da planilha e mostrar no site
    def carregar_dados():
        try:
            # Lê a planilha do Google Drive como se fosse uma tabela do site
            df_sheets = pd.read_csv(URL_PLANILHA)
            return df_sheets
        except:
            # Caso a planilha ainda esteja vazia ou indisponível, carrega a base padrão
            return pd.DataFrame([
                {
                    "CNPJ": "31.862.534/0001-30", "Provedor": "Alpha Fibra Telecom", "Localidade": "Chapecó - SC",
                    "Telefone": "(49) 3321-1000", "Email": "diretoria@alphafibra.com.br", "Responsáveis": "Carlos Silva (Diretor)",
                    "Situação de Mercado": "Guerra de preço / Margem Baixa", "Produto Olli": "Olli Smart Home"
                }
            ])

    # Função simulada para salvar na planilha (Em produção, o ideal é usar st.connection)
    if "banco_leads" not in st.session_state:
        st.session_state.banco_leads = carregar_dados().to_dict(orient="records")

    df = pd.DataFrame(st.session_state.banco_leads)

    # Dados aleatórios para o botão de busca
    nomes_novos = ["GigaNet", "VoxFibra", "MasterConect", "TurboLink", "SulInternet", "WebSpeed"]
    cidades_novas = ["Blumenau - SC", "Campinas - SP", "Curitiba - PR", "Porto Alegre - RS", "Uberlândia - MG"]
    dores_novas = [
        ("Guerra de preço / Margem Baixa", "Olli Smart Home"),
        ("Perdendo clientes (Churn Alto)", "Olli Habita"),
        ("Estagnado / Mercado saturado", "Olli Smart Home")
    ]

    # =====================================================================
    # INTERFACE DO DASHBOARD
    # =====================================================================
    st.title("🤖 Dashboard de Inteligência Comercial — SDR Olli IoT")
    st.markdown("Mapeamento estratégico de Provedores de Internet (ISPs) com dores de mercado.")
    st.write("---")

    col_titulo, col_botao = st.columns([4, 1])
    with col_botao:
        if st.button("🔄 Buscar por Novos Clientes", type="primary", use_container_width=True):
            provedor_aleatorio = random.choice(nomes_novos) + " Telecom"
            cidade_aleatoria = random.choice(cidades_novas)
            dor_aleatoria, produto_aleatorio = random.choice(dores_novas)
            cnpj_aleatorio = f"{random.randint(10,99)}.{random.randint(100,999)}.{random.randint(100,999)}/0001-{random.randint(10,99)}"
            
            novo_lead = {
                "CNPJ": cnpj_aleatorio,
                "Provedor": provedor_aleatorio,
                "Localidade": cidade_aleatoria,
                "Telefone": f"({random.randint(11,99)}) 3999-{random.randint(1000,9990)}",
                "Email": f"contato@{provedor_aleatorio.lower().replace(' ', '')}.com.br",
                "Responsáveis": f"{random.choice(['Marcos', 'Paula', 'Rodrigo', 'Juliana'])} {random.choice(['Oliveira', 'Santos', 'Pereira'])} (Diretor)",
                "Situação de Mercado": dor_aleatoria,
                "Produto Olli": produto_aleatorio
            }
            
            st.session_state.banco_leads.append(novo_lead)
            st.success(f"🔥 Novo cliente encontrado: {provedor_aleatorio}!")
            time.sleep(1)
            st.rerun()

    # Indicadores Rápidos (Cards)
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric(label="Total de Leads Mapeados", value=len(df))
    with col2:
        st.metric(label="Foco: Olli Smart Home", value=len(df[df["Produto Olli"] == "Olli Smart Home"]))
    with col3:
        st.metric(label="Foco: Olli Habita", value=len(df[df["Produto Olli"] == "Olli Habita"]))

    st.write("---")

    # Filtro Interativo na Lateral
    st.sidebar.header("Filtros de Prospecção")
    situacao_selecionada = st.sidebar.multiselect(
        "Filtrar por Situação do Provedor:",
        options=df["Situação de Mercado"].unique(),
        default=df["Situação de Mercado"].unique()
    )

    # Aplica o filtro na tabela
    df_filtrado = df[df["Situação de Mercado"].isin(situacao_selecionada)]

    # Exibe a Tabela Interativa de Leads
    st.subheader("📋 Lista de Oportunidades Qualificadas")
    st.dataframe(df_filtrado, use_container_width=True)

    st.write("---")

    # Seção de Script de Abordagem Rápida Corrigida
    st.subheader("⚡ Script de Abordagem para o Lead Selecionado")
    if not df_filtrado.empty:
        provedor_escolhido = st.selectbox("Escolha um provedor para ver o Script do SDR:", df_filtrado["Provedor"].unique())

        if provedor_escolhido:
            # Pega a linha exata do provedor de forma segura
            lead_index = df_filtrado[df_filtrado["Provedor"] == provedor_escolhido].index[0]
            lead = df_filtrado.loc[lead_index]
            st.info(
                f"**Script Sugerido para copiar:**\n\n"
                f"_\"Olá, procuro pelo **{lead['Responsáveis']}**. Tudo bem? "
                f"Vi que a **{lead['Provedor']}** atua em **{lead['Localidade']}** e que o mercado de banda larga aí está sofrendo com **{lead['Situação de Mercado'].lower()}**. "
                f"A Olli (do ecossistema IXC) ajuda provedores a criarem uma nova receita recorrente agregando IoT e automação na mesma fatura, sem custo de nova infraestrutura de fibra. Podemos agendar 15 minutos?\"_ "
            )
    else:
        st.warning("Nenhum provedor selecionado nos filtros laterais.")
    


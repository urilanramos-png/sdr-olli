import streamlit as st
import pandas as pd
import random

# Configuração da página do Dashboard
st.set_page_config(page_title="Dashboard SDR - Olli IoT", page_icon="🤖", layout="wide")

# =====================================================================
# GERENCIAMENTO DE BANCO DE DADOS (Armazenado na memória do navegador)
# =====================================================================
if "banco_leads" not in st.session_state:
    st.session_state.banco_leads = [
        {
            "CNPJ": "31.862.534/0001-30",
            "Provedor": "Alpha Fibra Telecom",
            "Localidade": "Chapecó - SC",
            "Telefone": "(49) 3321-1000",
            "Email": "diretoria@alphafibra.com.br",
            "Responsáveis": "Carlos Silva (Diretor)",
            "Situação de Mercado": "Guerra de preço / Margem Baixa",
            "Produto Olli": "Olli Smart Home"
        },
        {
            "CNPJ": "14.301.549/0001-09",
            "Provedor": "Litoral Byte Internet",
            "Localidade": "Santos - SP",
            "Telefone": "(13) 3255-4040",
            "Email": "contato@litoralbyte.net",
            "Responsáveis": "Roberto Mendes (CEO)",
            "Situação de Mercado": "Perdendo clientes (Churn Alto)",
            "Produto Olli": "Olli Habita"
        }
    ]

# Lista de dados aleatórios para simular a busca de novos clientes
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

# Seção do Botão de Busca na parte de cima
col_titulo, col_botao = st.columns([4, 1])
with col_botao:
    # O BOTÃO DE BUSCA
    if st.button("🔄 Buscar por Novos Clientes", type="primary", use_container_width=True):
        # Gera dados de um novo provedor fictício para a simulação
        provedor_aleatorio = random.choice(nomes_novos) + " Telecom"
        cidade_aleatoria = random.choice(cidades_novas)
        dor_aleatoria, produto_aleatorio = random.choice(dores_novas)
        cnpj_aleatorio = f"{random.randint(10,99)}.{random.randint(100,999)}.{random.randint(100,999)}/0001-{random.randint(10,99)}"
        
        novo_lead = {
            "CNPJ": cnpj_aleatorio,
            "Provedor": provedor_aleatorio,
            "Localidade": city_aleatoria if 'city_aleatoria' in locals() else cidade_aleatoria,
            "Telefone": f"({random.randint(11,99)}) 3999-{random.randint(1000,9990)}",
            "Email": f"contato@ {provedor_aleatorio.lower().replace(' ', '')}.com.br",
            "Responsáveis": f"{random.choice(['Marcos', 'Paula', 'Rodrigo', 'Juliana'])} {random.choice(['Oliveira', 'Santos', 'Pereira'])} (Diretor)",
            "Situação de Mercado": dor_aleatoria,
            "Produto Olli": produto_aleatorio
        }
        
        # Salva o novo cliente na lista atual do Dashboard
        st.session_state.banco_leads.append(novo_lead)
        st.success(f"🔥 Novo cliente encontrado: {provedor_aleatorio}!")

# Transforma a lista atual em tabela do Pandas
df = pd.DataFrame(st.session_state.banco_leads)

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
        # Pega a linha exata do provedor selecionado de forma segura
        lead = df_filtrado[df_filtrado["Provedor"] == provedor_escolhido].iloc[0]
        st.info(
            f"**Script Sugerido para copiar:**\n\n"
            f"_\"Olá, procuro pelo **{lead['Responsáveis']}**. Tudo bem? "
            f"Vi que a **{lead['Provedor']}** atua em **{lead['Localidade']}** e que o mercado de banda larga aí está sofrendo com **{lead['Situação de Mercado'].lower()}**. "
            f"A Olli (do ecossistema IXC) ajuda provedores a criarem uma nova receita recorrente agregando IoT e automação na mesma fatura, sem custo de nova infraestrutura de fibra. Podemos agendar 15 minutos?\"_"
        )
else:
    st.warning("Nenhum provedor selecionado nos filtros laterais.")


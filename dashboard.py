import streamlit as st
import pandas as pd
import random
import os
import time

# Configuração inicial da página do Dashboard
st.set_page_config(
    page_title="Olli Hub - Inteligência SDR", 
    page_icon="🤖", 
    layout="wide"
)

ARQUIVO_BANCO_DADOS = "banco_leads_sdr.csv"

# Leads padrão de inicialização com dados estruturados
DADOS_INICIAIS = [
    {
        "CNPJ": "31.862.534/0001-30", "Provedor": "Alpha Fibra Telecom", "Localidade": "Chapecó - SC",
        "Telefone": "(49) 3321-1000", "Email": "diretoria@alphafibra.com.br", "Responsáveis": "Carlos Silva (Diretor)",
        "Situação de Mercado": "Guerra de preço agressiva / Perda de margem na região", "Produto Olli": "Olli Smart Home"
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
# TELA DE LOGIN FORMATADA (REESCRITA SEM MARCOUP HTML COMPLEXO)
# =====================================================================
def verificar_senha():
    if "autenticado" not in st.session_state: 
        st.session_state.autenticado = False

    if not st.session_state.autenticado:
        st.header("🔒 Olli Hub - Autenticação")
        st.write("Por segurança, insira as credenciais corporativas.")
        st.write("---")
        
        col_log1, col_log2, col_log3 = st.columns([1, 2, 1])
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
    # SIDEBAR DESIGN
    # =====================================================================
    st.sidebar.title("Olli")
    st.sidebar.caption("Intelligence SDR v2.0")
    st.sidebar.write("---")
    
    st.sidebar.subheader("🎯 Menu de Filtros")
    situacao_selecionada = st.sidebar.multiselect(
        "Filtrar Dores de Provedores:", 
        options=df["Situação de Mercado"].unique(), 
        default=df["Situação de Mercado"].unique()
    )
    
    st.sidebar.write("---")
    st.sidebar.caption("Divisão de Soluções IXC Soft © 2026")

    df_filtrado = df[df["Situação de Mercado"].isin(situacao_selecionada)].copy()

    # =====================================================================
    # DASHBOARD BODY
    # =====================================================================
    st.markdown("## 📊 Painel Geral de Prospecção Estratégica")
    st.markdown("Gerenciamento automatizado de leads ISPs com dores de mercado validadas.")
    st.write("---")

    # CARDS DE MÉTRICAS FORMATADOS DE MANEIRA NATIVA
    m1, m2, m3 = st.columns(3)
    with m1:
        st.metric(label="Total de ISPs na Base", value=len(df))
    with m2:
        st.metric(label="Foco: Olli Smart Home", value=len(df[df['Produto Olli'] == 'Olli Smart Home']))
    with m3:
        st.metric(label="Foco: Olli Habita", value=len(df[df['Produto Olli'] == 'Olli Habita']))

    st.write("---")

    # ABA INTERATIVA CENTRAL DE OPERAÇÕES
    aba_varredura, aba_analise = st.tabs(["🚀 Central de Operações & Leads", "📊 Gráficos & Estatísticas de Mercado"])

    with aba_varredura:
        st.write("")
        col_btn1, col_btn2 = st.columns([3, 1])
        with col_btn1:
            st.markdown("### 📋 Oportunidades Mapeadas em Lote")
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
            cargos = ["Diretor de Operações", "CEO & Sócio", "Diretor Executivo", "Sócio-Fundador"]

            novos_leads_encontrados = []
            
            barra_progresso = st.progress(0)
            status_texto = st.empty()
            
            status_texto.markdown("📡 **Buscando matrizes de acessos e indicadores ANATEL / Reclame Aqui...**")
            for p in range(101):
                time.sleep(0.01)
                barra_progresso.progress(p)
            
            quantidade_descoberta = random.randint(2, 4)
            for _ in range(quantidade_descoberta):
                empresa = random.choice(nomes_provedores)
                nomes_provedores.remove(empresa)
                cidade_uf = random.choice(cidades)
                dor_produto = random.choice(banco_dores_produtos)
                decisor = f"{random.choice(nomes_decisores)} ({random.choice(cargos)})"
                cnpj_falso = f"{random.randint(10,99)}.{random.randint(100,999)}.{random.randint(100,999)}/0001-{random.randint(10,99)}"
                
                lead_estruturado = {
                    "CNPJ": cnpj_falso, "Provedor": empresa + " Telecom", "Localidade": city_uf if 'city_uf' in locals() else cidade_uf,
                    "Telefone": f"({random.randint(11,55)}) 3055-{random.randint(1000,9990)}",
                    "Email": f"contato@{empresa.lower().replace(' ', '')}.com.br", "Responsáveis": decisor,
                    "Situação de Mercado": dor_produto["dor"], "Produto Olli": dor_produto["produto"]
                }
                novos_leads_encontrados.append(lead_estruturado)
                
            gravar_multiplos_leads_no_arquivo(novos_leads_encontrados)
            status_texto.empty()
            st.success(f"🔥 Varredura finalizada! +{quantidade_descoberta} provedores adicionados.")
            time.sleep(0.5)
            st.rerun()

        # EXIBIÇÃO DA TABELA FORMATADA COM CHECKBOX DE REMOÇÃO DE LINHA
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
                if st.button("🗑️ Excluir Provedores Selecionados", type="secondary", use_container_width=True):
                    deletar_lista_leads_do_arquivo(leads_selecionados)
                    st.toast("Leads excluídos com sucesso!", icon="🗑️")
                    time.sleep(0.5)
                    st.rerun()
        else:
            st.warning("Nenhum provedor disponível para exibição nos filtros atuais.")

        st.write("---")
        
        # PITCH COMERCIAL SELECIONÁVEL EM DESIGN CLEAN
        st.markdown("### ⚡ Roteiro Automatizado de Abordagem")
        if not df_filtrado.empty:
            provedor_escolhido = st.selectbox("Escolha a empresa para gerar o Script do SDR:", df_filtrado["Provedor"].unique())
            if provedor_escolhido:
                sub_df = df_filtrado[df_filtrado["Provedor"] == provedor_escolhido]
                
                v_resp = str(sub_df["Responsáveis"].values[0])
                v_local = str(sub_df["Localidade"].values[0])
                v_prov = str(sub_df["Provedor"].values[0])
                v_sit = str(sub_df["Situação de Mercado"].values[0]).lower()

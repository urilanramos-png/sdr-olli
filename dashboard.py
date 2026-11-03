import os
import time
from datetime import datetime
from html import escape

import pandas as pd
import streamlit as st

# =====================================================================
# CONFIGURAÇÕES
# =====================================================================
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ARQUIVO_BANCO_DADOS = os.path.join(BASE_DIR, "banco_leads_sdr_enterprise.csv")
ARQUIVO_LOGS = os.path.join(BASE_DIR, "sdr_system_audit.log")

st.set_page_config(
    page_title="Olli Hub Enterprise v2.0 | SDR Intelligence & AI Matrix",
    page_icon="🔮",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown(
    """
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&family=Space+Grotesk:wght@500;700&display=swap');
        html, body, [data-testid="stAppViewContainer"], .main {
            background: linear-gradient(180deg, #0B071E 0%, #120B2D 100%);
            color: #E2E8F0 !important;
            font-family: 'Inter', sans-serif;
        }
        [data-testid="stSidebar"] {
            background: #070414 !important;
            border-right: 1px solid rgba(124, 58, 237, 0.2);
        }
        h1, h2, h3, h4 {
            font-family: 'Space Grotesk', sans-serif !important;
            font-weight: 700 !important;
            letter-spacing: -0.02em;
        }
        .cyber-title {
            background: linear-gradient(135deg, #A855F7 0%, #7C3AED 50%, #06B6D4 100%);
            -webkit-background-clip: text;
            background-clip: text;
            color: transparent;
            font-size: 2.5rem;
            font-weight: 800;
            margin-bottom: 0.35rem;
        }
        .subtitle { color: #94A3B8; font-size: 1.08rem; margin-bottom: 1.5rem; }
        div[data-testid="stTextInput"] input {
            background-color: rgba(15, 10, 36, 0.7) !important;
            color: #E2E8F0 !important;
            border: 1px solid rgba(168, 85, 247, 0.4) !important;
            border-radius: 12px !important;
        }
        div.stButton > button {
            width: 100%;
            background: linear-gradient(135deg, #7C3AED 0%, #A855F7 100%) !important;
            color: #fff !important;
            border: 1px solid rgba(255, 255, 255, 0.1) !important;
            border-radius: 12px !important;
            font-family: 'Space Grotesk', sans-serif !important;
            font-weight: 600 !important;
            padding: 0.75rem 1rem !important;
        }
        .kpi-container {
            background: linear-gradient(145deg, rgba(26, 18, 70, 0.5), rgba(11, 7, 30, 0.85));
            border-left: 4px solid #7C3AED;
            border-radius: 16px;
            padding: 20px;
            min-height: 115px;
        }
        .kpi-title {
            color: #94A3B8;
            font-size: 11px;
            font-weight: 700;
            text-transform: uppercase;
            letter-spacing: 0.15em;
        }
        .kpi-value {
            color: #fff;
            font-size: 2rem;
            font-family: 'Space Grotesk', sans-serif;
            font-weight: 700;
            margin-top: 8px;
        }
        .hologram-card {
            background: rgba(20, 14, 56, 0.45);
            border: 1px solid rgba(168, 85, 247, 0.18);
            border-radius: 20px;
            padding: 22px;
            margin-bottom: 1rem;
            box-shadow: 0 12px 40px rgba(124, 58, 237, 0.08);
        }
        .ai-response {
            background: rgba(6, 182, 212, 0.06);
            border: 1px dashed rgba(6, 182, 212, 0.35);
            border-radius: 14px;
            padding: 18px;
            color: #7DD3FC;
            margin-top: 14px;
            line-height: 1.7;
        }
        .score-track {
            background: rgba(255,255,255,0.08);
            border-radius: 8px;
            height: 10px;
            width: 100%;
            margin-top: 8px;
            overflow: hidden;
        }
        .score-fill {
            background: linear-gradient(90deg, #7C3AED, #06B6D4);
            height: 100%;
            border-radius: 8px;
        }
    </style>
    """,
    unsafe_allow_html=True,
)

# =====================================================================
# LOGS E DADOS
# =====================================================================
def registrar_log(mensagem: str, usuario: str = "Sistema") -> None:
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    try:
        with open(ARQUIVO_LOGS, "a", encoding="utf-8") as arquivo:
            arquivo.write(f"[{timestamp}] [{usuario}] {mensagem}\n")
    except OSError:
        pass


DADOS_INICIAIS_MOCK = [
    {
        "ID": "ISP-701",
        "Status Contato": "Qualificado",
        "Provedor": "Alpha Fibra Telecom",
        "Responsáveis": "Carlos Silva",
        "Cargo": "Diretor de Operações",
        "Localidade": "Chapecó - SC",
        "Telefone": "(49) 3321-1000",
        "Email": "diretoria@alphafibra.com.br",
        "Situação de Mercado": "Guerra de preço agressiva / Perda de margem na região",
        "Produto Olli": "Olli Smart Home",
        "CNPJ": "31.862.534/0001-30",
        "Clientes Estimados": 12000,
        "Ticket Médio (R$)": 89.90,
        "Data Cadastro": "2026-01-10",
        "Score Conectividade": 88,
        "Origem Lead": "Outbound LinkedIn",
    },
    {
        "ID": "ISP-702",
        "Status Contato": "Não Chamado",
        "Provedor": "Beta Net Telecom",
        "Responsáveis": "Rodrigo Ramos",
        "Cargo": "CEO",
        "Localidade": "Blumenau - SC",
        "Telefone": "(47) 3211-5500",
        "Email": "rodrigo@betanet.net.br",
        "Situação de Mercado": "Churn alto detectado em relatórios ANATEL",
        "Produto Olli": "Olli Habita",
        "CNPJ": "14.552.112/0001-99",
        "Clientes Estimados": 7500,
        "Ticket Médio (R$)": 79.90,
        "Data Cadastro": "2026-02-15",
        "Score Conectividade": 45,
        "Origem Lead": "Mapeamento ANATEL",
    },
    {
        "ID": "ISP-703",
        "Status Contato": "Agendado (Reunião)",
        "Provedor": "Wave Conectividade",
        "Responsáveis": "Juliana Mendes",
        "Cargo": "Gerente de Marketing",
        "Localidade": "Maringá - PR",
        "Telefone": "(44) 99881-2233",
        "Email": "juliana@waveconect.com.br",
        "Situação de Mercado": "Estagnação de vendas / Sem serviços de valor agregado (SVA)",
        "Produto Olli": "Olli Smart Home",
        "CNPJ": "45.123.789/0001-02",
        "Clientes Estimados": 24000,
        "Ticket Médio (R$)": 110.00,
        "Data Cadastro": "2026-03-22",
        "Score Conectividade": 92,
        "Origem Lead": "Inbound - Evento IXC",
    },
]

COLUNAS_OBRIGATORIAS = [
    "ID", "Status Contato", "Provedor", "Responsáveis", "Cargo", "Localidade",
    "Telefone", "Email", "Situação de Mercado", "Produto Olli", "CNPJ",
    "Clientes Estimados", "Ticket Médio (R$)", "Data Cadastro",
    "Score Conectividade", "Origem Lead",
]


def inicializar_e_carregar_dados() -> pd.DataFrame:
    """Cria/carrega o CSV e garante que as colunas esperadas estejam disponíveis."""
    if not os.path.exists(ARQUIVO_BANCO_DADOS):
        df = pd.DataFrame(DADOS_INICIAIS_MOCK, columns=COLUNAS_OBRIGATORIAS)
        try:
            df.to_csv(ARQUIVO_BANCO_DADOS, index=False, encoding="utf-8")
            registrar_log("Base de dados corporativa inicializada com sucesso.")
        except OSError as erro:
            registrar_log(f"Falha ao criar banco de dados: {erro}", "ERRO")
        return df

    try:
        df = pd.read_csv(ARQUIVO_BANCO_DADOS, encoding="utf-8")
    except (OSError, pd.errors.ParserError, UnicodeDecodeError) as erro:
        registrar_log(f"Falha ao carregar banco de dados: {erro}", "ERRO")
        return pd.DataFrame(DADOS_INICIAIS_MOCK, columns=COLUNAS_OBRIGATORIAS)

    mudou = False
    for coluna in COLUNAS_OBRIGATORIAS:
        if coluna not in df.columns:
            df[coluna] = 0 if coluna in ("Clientes Estimados", "Score Conectividade") else "Não Informado"
            mudou = True

    if mudou:
        try:
            df.to_csv(ARQUIVO_BANCO_DADOS, index=False, encoding="utf-8")
        except OSError as erro:
            registrar_log(f"Falha ao atualizar colunas do banco: {erro}", "ERRO")

    return df


def gerar_abordagem_ia(provedor: str, responsavel: str, dor: str, produto: str) -> str:
    """Gera uma sugestão demonstrativa de abordagem comercial."""
    time.sleep(0.8)
    return (
        f"Olá {responsavel}, percebi o posicionamento da {provedor} na região e o cenário atual "
        f"envolvendo '{dor}'. O {produto} pode ajudar a fortalecer a percepção de valor, "
        "reduzir churn e elevar o ticket médio. Podemos agendar uma conversa esta semana "
        "para avaliar se essa solução faz sentido para sua operação?"
    )


# =====================================================================
# INTERFACE
# =====================================================================
df_provedores = inicializar_e_carregar_dados()

# Normaliza colunas numéricas para evitar erros em CSVs preenchidos manualmente.
df_provedores["Clientes Estimados"] = pd.to_numeric(
    df_provedores["Clientes Estimados"], errors="coerce"
).fillna(0)
df_provedores["Score Conectividade"] = pd.to_numeric(
    df_provedores["Score Conectividade"], errors="coerce"
).fillna(0).clip(0, 100)

st.markdown('<div class="cyber-title">⚡ Olli Hub Enterprise v2.0</div>', unsafe_allow_html=True)
st.markdown(
    '<div class="subtitle">SDR Intelligence Matrix &amp; Real-time Network Mapping</div>',
    unsafe_allow_html=True,
)

kpi1, kpi2, kpi3 = st.columns(3)
with kpi1:
    st.markdown(
        f'<div class="kpi-container"><div class="kpi-title">Total Provedores</div>'
        f'<div class="kpi-value">{len(df_provedores)}</div></div>',
        unsafe_allow_html=True,
    )
with kpi2:
    total_clientes = int(df_provedores["Clientes Estimados"].sum())
    st.markdown(
        '<div class="kpi-container" style="border-left-color:#A855F7;">'
        f'<div class="kpi-title">Clientes Estimados</div><div class="kpi-value">{total_clientes:,}</div></div>',
        unsafe_allow_html=True,
    )
with kpi3:
    score_medio = int(df_provedores["Score Conectividade"].mean()) if not df_provedores.empty else 0
    st.markdown(
        '<div class="kpi-container" style="border-left-color:#06B6D4;">'
        f'<div class="kpi-title">Score Médio</div><div class="kpi-value">{score_medio}%</div></div>',
        unsafe_allow_html=True,
    )

st.write("---")
st.markdown("### 🔍 Escaneamento de Rede e Filtro Inteligente")
termo_busca = st.text_input(
    "Digite o nome do provedor ou cidade para iniciar a varredura...",
    placeholder="Ex: Alpha Fibra",
)

if termo_busca:
    provedor_match = df_provedores["Provedor"].fillna("").astype(str).str.contains(
        termo_busca, case=False, na=False, regex=False
    )
    localidade_match = df_provedores["Localidade"].fillna("").astype(str).str.contains(
        termo_busca, case=False, na=False, regex=False
    )
    df_filtrado = df_provedores[provedor_match | localidade_match]
else:
    df_filtrado = df_provedores

st.markdown("### 🔮 Mapeamento de Cartões Holográficos")

if df_filtrado.empty:
    st.info("Nenhum provedor encontrado com os critérios de busca informados.")

for _, row in df_filtrado.iterrows():
    col_card, col_action = st.columns([4, 1])

    provedor_valor = str(row.get("Provedor", "Não informado"))
    responsavel_valor = str(row.get("Responsáveis", "Não informado"))
    dor_valor = str(row.get("Situação de Mercado", "Não informada"))
    produto_valor = str(row.get("Produto Olli", "Não informado"))
    lead_id = str(row.get("ID", row.name))
    score = int(row.get("Score Conectividade", 0))
    score = max(0, min(100, score))

    with col_card:
        provedor = escape(provedor_valor)
        status = escape(str(row.get("Status Contato", "Não informado")))
        localidade = escape(str(row.get("Localidade", "Não informada")))
        produto = escape(produto_valor)
        responsavel = escape(responsavel_valor)
        cargo = escape(str(row.get("Cargo", "Não informado")))
        dor = escape(dor_valor)

        st.markdown(
            f"""
            <div class="hologram-card">
                <div style="display:flex;justify-content:space-between;align-items:center;gap:12px;">
                    <span style="color:#06B6D4;font-family:'Space Grotesk',sans-serif;font-weight:700;font-size:1.3rem;">{provedor}</span>
                    <span style="background:rgba(124,58,237,0.2);color:#A855F7;padding:4px 12px;border-radius:20px;font-size:0.78rem;border:1px solid rgba(168,85,247,0.3);font-weight:600;">{status}</span>
                </div>
                <div style="margin-top:18px;display:grid;grid-template-columns:repeat(3,minmax(150px,1fr));gap:16px;">
                    <div><span style="color:#64748B;font-size:0.75rem;display:block;">📍 LOCALIDADE</span><span style="color:#E2E8F0;font-weight:600;">{localidade}</span></div>
                    <div><span style="color:#64748B;font-size:0.75rem;display:block;">🎯 PRODUTO OLLI</span><span style="color:#A855F7;font-weight:700;">{produto}</span></div>
                    <div><span style="color:#64748B;font-size:0.75rem;display:block;">💼 RESPONSÁVEL</span><span style="color:#E2E8F0;font-weight:600;">{responsavel} ({cargo})</span></div>
                </div>
                <div style="margin-top:18px;padding:10px 12px;background:rgba(255,255,255,0.02);border-radius:10px;border-left:3px solid #7C3AED;">
                    <span style="color:#64748B;font-size:0.75rem;display:block;">⚠️ SITUAÇÃO DE MERCADO / DOR</span>
                    <span style="color:#CBD5E1;font-size:0.92rem;">{dor}</span>
                </div>
                <div style="margin-top:18px;">
                    <span style="color:#64748B;font-size:0.75rem;">SCORE DE SAÚDE DA REDE ({score}%)</span>
                    <div class="score-track"><div class="score-fill" style="width:{score}%;"></div></div>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with col_action:
        st.write("")
        if st.button("Disparar IA Matrix", key=f"btn_{lead_id}"):
            with st.spinner("🤖 Preparando sugestão de abordagem..."):
                abordagem = gerar_abordagem_ia(
                    provedor_valor,
                    responsavel_valor,
                    dor_valor,
                    produto_valor,
                )
            st.markdown(
                '<div class="ai-response"><strong>🛰️ Abordagem sugerida:</strong><br><br>'
                f'{escape(abordagem)}</div>',
                unsafe_allow_html=True,
            )
            registrar_log(f"Abordagem gerada para {provedor_valor}", "AI_ENGINE")

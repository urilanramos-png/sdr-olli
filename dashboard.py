import os
from datetime import datetime
from html import escape

import pandas as pd
import streamlit as st
import streamlit.components.v1 as components

# =====================================================================
# CONFIGURAÇÃO
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
        :root { color-scheme: dark; }
        html, body, [data-testid="stAppViewContainer"], .main {
            background: linear-gradient(180deg, #0B071E 0%, #120B2D 100%);
            color: #E2E8F0 !important;
            font-family: Inter, system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
        }
        [data-testid="stSidebar"] { background: #070414 !important; }
        h1, h2, h3, h4 { letter-spacing: -0.02em; }
        .cyber-title {
            background: linear-gradient(135deg, #C084FC 0%, #7C3AED 52%, #22D3EE 100%);
            -webkit-background-clip: text; background-clip: text; color: transparent;
            font-size: clamp(2rem, 4vw, 2.7rem); font-weight: 800; margin-bottom: .3rem;
        }
        .subtitle { color: #94A3B8; font-size: 1.05rem; margin-bottom: 1.2rem; }
        div[data-testid="stTextInput"] input {
            background: rgba(15, 10, 36, .8) !important; color: #E2E8F0 !important;
            border: 1px solid rgba(168, 85, 247, .45) !important; border-radius: 12px !important;
            min-height: 44px;
        }
        div.stButton > button, div[data-testid="stFormSubmitButton"] button {
            width: 100%; color: #fff !important; border: 1px solid rgba(255,255,255,.12) !important;
            border-radius: 12px !important; font-weight: 650 !important;
            background: linear-gradient(135deg, #6D28D9, #A855F7) !important;
            transition: transform .18s ease, box-shadow .18s ease !important;
        }
        div.stButton > button:hover, div[data-testid="stFormSubmitButton"] button:hover {
            transform: translateY(-2px); box-shadow: 0 0 20px rgba(168,85,247,.4) !important;
        }
        .kpi-container {
            background: linear-gradient(145deg, rgba(26,18,70,.55), rgba(11,7,30,.88));
            border-left: 4px solid #7C3AED; border-radius: 15px; padding: 18px; min-height: 105px;
        }
        .kpi-title { color:#94A3B8; font-size:11px; font-weight:700; text-transform:uppercase; letter-spacing:.14em; }
        .kpi-value { color:#fff; font-size:1.9rem; font-weight:750; margin-top:7px; }
        .hologram-card {
            background: rgba(20,14,56,.48); border: 1px solid rgba(168,85,247,.2);
            border-radius: 18px; padding: 20px; margin-bottom: 12px;
            box-shadow: 0 10px 30px rgba(124,58,237,.07);
            animation: card-enter .35s ease both;
        }
        @keyframes card-enter { from { opacity:0; transform:translateY(12px); } to { opacity:1; transform:translateY(0); } }
        .score-track { background:rgba(255,255,255,.08); border-radius:8px; height:9px; margin-top:7px; overflow:hidden; }
        .score-fill { height:100%; border-radius:8px; background:linear-gradient(90deg,#7C3AED,#22D3EE); }
        .ai-response {
            background:rgba(6,182,212,.06); border:1px dashed rgba(6,182,212,.35);
            border-radius:13px; padding:16px; color:#A5F3FC; margin:10px 0 16px; line-height:1.65;
        }
        .empty-state {
            position:relative; overflow:hidden; text-align:center; padding:30px 18px 22px;
            margin:18px 0; border:1px solid rgba(168,85,247,.2); border-radius:20px;
            background:radial-gradient(ellipse at 50% 100%,rgba(124,58,237,.18),transparent 65%),rgba(18,11,45,.55);
        }
        .empty-title { color:#E9D5FF; font-size:1.3rem; font-weight:750; margin:8px 0 4px; }
        .empty-copy { color:#A1A1AA; font-size:.95rem; }
        .walker { transform-origin:center; animation: walk-across 8s ease-in-out infinite alternate; }
        @keyframes walk-across { from { transform:translateX(-105px); } to { transform:translateX(105px); } }
        @media (prefers-reduced-motion: reduce) {
            *, *::before, *::after { animation-duration:.01ms !important; transition-duration:.01ms !important; }
        }
    </style>
    """,
    unsafe_allow_html=True,
)

components.html(
    """
    <script>
    (() => {
      try {
        const doc = window.parent.document;
        if (doc.getElementById('olli-effects')) return;

        const style = doc.createElement('style');
        style.textContent = `
          #olli-pointer-light {
            position: fixed; z-index: 2147483645; width: 150px; height: 150px; left: 0; top: 0;
            pointer-events: none; opacity: 0; transform: translate(-50%, -50%);
            border-radius: 50%;
            background: radial-gradient(circle, rgba(255,255,255,.2) 0%, rgba(216,180,254,.18) 18%, rgba(168,85,247,.16) 38%, rgba(124,58,237,.08) 58%, transparent 72%);
            filter: blur(3px); transition: opacity .2s ease;
          }
          #olli-walker {
            position: fixed; z-index: 2147483644; left: 50%; bottom: 12px; width: 110px; height: 125px;
            pointer-events: none; opacity: .72; transform: translateX(-50%);
            animation: olli-walk 10s ease-in-out infinite alternate;
          }
          #olli-walker svg { width: 100%; height: 100%; overflow: visible; }
          #olli-walker .beam { transform-origin: 58px 66px; animation: olli-beam 2.6s ease-in-out infinite alternate; }
          @keyframes olli-walk { from { margin-left: -34vw; } to { margin-left: 34vw; } }
          @keyframes olli-beam { from { transform: rotate(-12deg); opacity: .45; } to { transform: rotate(12deg); opacity: .8; } }
          @media (prefers-reduced-motion: reduce) { #olli-walker, #olli-walker .beam { animation: none !important; } }
        `;
        doc.head.appendChild(style);

        const wrap = doc.createElement('div');
        wrap.id = 'olli-effects';
        wrap.innerHTML = `
          <div id="olli-pointer-light"></div>
          <div id="olli-walker" aria-hidden="true">
            <svg viewBox="0 0 110 125" xmlns="http://www.w3.org/2000/svg">
              <defs>
                <radialGradient id="lanternGlow">
                  <stop stop-color="#FDE68A" stop-opacity=".85"/>
                  <stop offset="1" stop-color="#A855F7" stop-opacity="0"/>
                </radialGradient>
              </defs>
              <path class="beam" d="M58 66 L101 36 Q108 63 91 89 Z" fill="url(#lanternGlow)"/>
              <circle cx="49" cy="30" r="10" fill="#DDD6FE"/>
              <path d="M39 42 Q49 37 59 43 L64 69 L38 69 Z" fill="#8B5CF6"/>
              <path d="M42 67 L39 94 M59 67 L64 93" stroke="#C4B5FD" stroke-width="6" stroke-linecap="round"/>
              <path d="M42 47 L31 62 M58 47 L69 59" stroke="#C4B5FD" stroke-width="5" stroke-linecap="round"/>
              <g class="beam"><path d="M70 58 L78 54 L82 64 L73 68 Z" fill="#FDE68A" stroke="#F5D17A" stroke-width="2"/><circle cx="78" cy="61" r="10" fill="url(#lanternGlow)"/></g>
              <path d="M34 97 H47 M60 97 H73" stroke="#E9D5FF" stroke-width="5" stroke-linecap="round"/>
            </svg>
          </div>
        `;
        doc.body.appendChild(wrap);

        const light = doc.getElementById('olli-pointer-light');
        doc.addEventListener('pointermove', (event) => {
          if (event.pointerType === 'touch' || window.parent.matchMedia('(prefers-reduced-motion: reduce)').matches) return;
          light.style.left = event.clientX + 'px';
          light.style.top = event.clientY + 'px';
          light.style.opacity = '1';
        }, { passive: true });
        doc.addEventListener('pointerleave', () => { light.style.opacity = '0'; }, { passive: true });
      } catch (_) { /* ignore */ }
    })();
    </script>
    """,
    height=0,
    scrolling=False,
)

# =====================================================================
# DADOS / FUNÇÕES
# =====================================================================
COLUNAS = [
    "ID", "Status Contato", "Provedor", "Responsáveis", "Cargo", "Localidade", "Telefone", "Email",
    "Situação de Mercado", "Produto Olli", "CNPJ", "Clientes Estimados", "Ticket Médio (R$)",
    "Data Cadastro", "Score Conectividade", "Origem Lead",
]

DADOS_INICIAIS = [
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


def registrar_log(mensagem: str, usuario: str = "Sistema") -> None:
    try:
        with open(ARQUIVO_LOGS, "a", encoding="utf-8") as arquivo:
            arquivo.write(f"[{datetime.now():%Y-%m-%d %H:%M:%S}] [{usuario}] {mensagem}\n")
    except OSError:
        pass


@st.cache_data(ttl=60, show_spinner=False)
def carregar_dados() -> pd.DataFrame:
    if not os.path.exists(ARQUIVO_BANCO_DADOS):
        df = pd.DataFrame(DADOS_INICIAIS, columns=COLUNAS)
        df.to_csv(ARQUIVO_BANCO_DADOS, index=False, encoding="utf-8")
        registrar_log("Base de dados inicializada.")
        return df

    try:
        df = pd.read_csv(ARQUIVO_BANCO_DADOS, encoding="utf-8")
    except (OSError, pd.errors.ParserError, UnicodeDecodeError) as erro:
        registrar_log(f"Falha ao carregar banco de dados: {erro}", "ERRO")
        return pd.DataFrame(DADOS_INICIAIS, columns=COLUNAS)

    for coluna in COLUNAS:
        if coluna not in df.columns:
            df[coluna] = 0 if coluna in ("Clientes Estimados", "Score Conectividade") else "Não Informado"

    return df


def salvar_dados(df: pd.DataFrame) -> bool:
    try:
        df.to_csv(ARQUIVO_BANCO_DADOS, index=False, encoding="utf-8")
        carregar_dados.clear()
        return True
    except OSError as erro:
        st.error(f"Não foi possível salvar as alterações: {erro}")
        return False


def gerar_abordagem_ia(provedor: str, responsavel: str, dor: str, produto: str) -> str:
    return (
        f"Olá {responsavel}, percebi o posicionamento da {provedor} na região e o cenário atual "
        f"envolvendo '{dor}'. O {produto} pode ajudar a fortalecer a percepção de valor, reduzir churn "
        "e elevar o ticket médio. Podemos agendar uma conversa esta semana para avaliar se essa solução "
        "faz sentido para sua operação?"
    )


def mostrar_estado_vazio() -> None:
    st.markdown(
        """
        <div class="empty-state">
          <svg width="190" height="125" viewBox="0 0 190 125" role="img" aria-label="Pessoa caminhando com uma lanterna">
            <defs>
              <radialGradient id="emptyGlow">
                <stop stop-color="#FDE68A" stop-opacity=".65"/>
                <stop offset="1" stop-color="#A855F7" stop-opacity="0"/>
              </radialGradient>
            </defs>
            <ellipse cx="96" cy="111" rx="72" ry="8" fill="#7C3AED" opacity=".15"/>
            <g class="walker">
              <path d="M101 68 L154 42 Q165 62 151 82 Z" fill="url(#emptyGlow)"/>
              <circle cx="86" cy="37" r="10" fill="#DDD6FE"/>
              <path d="M77 50 Q87 46 96 51 L100 78 L75 78 Z" fill="#8B5CF6"/>
              <path d="M79 76 L75 101 M96 76 L102 100" stroke="#C4B5FD" stroke-width="6" stroke-linecap="round"/>
              <path d="M79 54 L69 70 M94 54 L106 65" stroke="#C4B5FD" stroke-width="5" stroke-linecap="round"/>
              <path d="M105 61 L113 57 L117 67 L108 71 Z" fill="#FDE68A" stroke="#F5D17A" stroke-width="2"/>
              <path d="M70 103 H82 M98 103 H111" stroke="#E9D5FF" stroke-width="5" stroke-linecap="round"/>
            </g>
          </svg>
          <div class="empty-title">Que tal procurar novos leads?</div>
          <div class="empty-copy">Sua busca não encontrou provedores. Experimente outro nome ou localidade.</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


# =====================================================================
# DASHBOARD
# =====================================================================
if "termo_busca_provedor" not in st.session_state:
    st.session_state.termo_busca_provedor = ""
if "confirmar_exclusao" not in st.session_state:
    st.session_state.confirmar_exclusao = None
if "scroll_resultados" not in st.session_state:
    st.session_state.scroll_resultados = False

# Carrega e padroniza dados
try:
    df = carregar_dados().copy()
except Exception:
    df = pd.DataFrame(DADOS_INICIAIS, columns=COLUNAS)

df["Clientes Estimados"] = pd.to_numeric(df["Clientes Estimados"], errors="coerce").fillna(0)
df["Score Conectividade"] = pd.to_numeric(df["Score Conectividade"], errors="coerce").fillna(0).clip(0, 100)

st.markdown('<div class="cyber-title">⚡ Olli Hub Enterprise v2.0</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">SDR Intelligence Matrix &amp; Real-time Network Mapping</div>', unsafe_allow_html=True)

k1, k2, k3 = st.columns(3)
with k1:
    st.markdown(
        f'<div class="kpi-container"><div class="kpi-title">Total Provedores</div><div class="kpi-value">{len(df)}</div></div>',
        unsafe_allow_html=True,
    )
with k2:
    st.markdown(
        f'<div class="kpi-container" style="border-left-color:#A855F7"><div class="kpi-title">Clientes Estimados</div><div class="kpi-value">{int(df["Clientes Estimados"].sum()):,}</div></div>',
        unsafe_allow_html=True,
    )
with k3:
    media = int(df["Score Conectividade"].mean()) if not df.empty else 0
    st.markdown(
        f'<div class="kpi-container" style="border-left-color:#22D3EE"><div class="kpi-title">Score Médio</div><div class="kpi-value">{media}%</div></div>',
        unsafe_allow_html=True,
    )

st.write("---")
st.markdown("### 🔎 Busca de provedores")
with st.form("form_busca_provedor", clear_on_submit=False):
    campo_busca, botao_busca = st.columns([5, 1])
    with campo_busca:
        termo_digitado = st.text_input(
            "Busca", placeholder="Nome do provedor ou cidade...", label_visibility="collapsed",
            key="campo_busca_provedor",
        )
    with botao_busca:
        buscar = st.form_submit_button("🔍 Procurar")

if buscar:
    st.session_state.termo_busca_provedor = termo_digitado.strip()
    st.session_state.scroll_resultados = True

barra_busca, barra_limpar = st.columns([5, 1])
with barra_busca:
    if st.session_state.termo_busca_provedor:
        st.caption(f"Busca ativa: {st.session_state.termo_busca_provedor}")
with barra_limpar:
    if st.button("Limpar", key="limpar_busca"):
        st.session_state.termo_busca_provedor = ""
        st.session_state.campo_busca_provedor = ""
        st.session_state.scroll_resultados = False
        st.rerun()

termo = st.session_state.termo_busca_provedor
if termo:
    prov_match = df["Provedor"].fillna("").astype(str).str.contains(termo, case=False, regex=False)
    local_match = df["Localidade"].fillna("").astype(str).str.contains(termo, case=False, regex=False)
    resultados = df[prov_match | local_match].copy()
else:
    resultados = df.copy()

st.markdown('<div id="scroll-resultados"></div>', unsafe_allow_html=True)
if st.session_state.scroll_resultados:
    components.html(
        """
        <script>
          setTimeout(() => {
            const el = window.parent.document.getElementById('scroll-resultados');
            if (el) el.scrollIntoView({ behavior: 'smooth', block: 'start' });
          }, 120);
        </script>
        """,
        height=0,
    )
    st.session_state.scroll_resultados = False

st.markdown("### 🔮 Provedores")
if resultados.empty:
    mostrar_estado_vazio()
else:
    for _, row in resultados.iterrows():
        lead_id = str(row.get("ID", row.name))
        provedor_raw = str(row.get("Provedor", "Não informado"))
        responsavel_raw = str(row.get("Responsáveis", "Não informado"))
        dor_raw = str(row.get("Situação de Mercado", "Não informada"))
        produto_raw = str(row.get("Produto Olli", "Não informado"))
        score = max(0, min(100, int(row.get("Score Conectividade", 0))))

        card_col, action_col = st.columns([4, 1])

        with card_col:
            provedor = escape(provedor_raw)
            status = escape(str(row.get("Status Contato", "Não informado")))
            local = escape(str(row.get("Localidade", "Não informada")))
            responsavel = escape(responsavel_raw)
            cargo = escape(str(row.get("Cargo", "Não informado")))
            produto = escape(produto_raw)
            dor = escape(dor_raw)
            st.markdown(
                f"""
                <div class="hologram-card">
                  <div style="display:flex;justify-content:space-between;align-items:center;gap:12px">
                    <span style="color:#22D3EE;font-size:1.25rem;font-weight:750">{provedor}</span>
                    <span style="background:rgba(124,58,237,.2);color:#D8B4FE;padding:4px 11px;border-radius:20px;font-size:.78rem">{status}</span>
                  </div>
                  <div style="margin-top:16px;display:grid;grid-template-columns:repeat(3,minmax(130px,1fr));gap:14px">
                    <div><small style="color:#64748B">📍 LOCALIDADE</small><br><b>{local}</b></div>
                    <div><small style="color:#64748B">🎯 PRODUTO OLLI</small><br><b style="color:#C084FC">{produto}</b></div>
                    <div><small style="color:#64748B">💼 RESPONSÁVEL</small><br><b>{responsavel} ({cargo})</b></div>
                  </div>
                  <div style="margin-top:15px;padding:10px 12px;background:rgba(255,255,255,.025);border-left:3px solid #7C3AED;border-radius:8px">
                    <small style="color:#64748B">⚠️ SITUAÇÃO DE MERCADO / DOR</small><br><span style="color:#CBD5E1">{dor}</span>
                  </div>
                  <div style="margin-top:14px"><small style="color:#94A3B8">SCORE DE SAÚDE DA REDE ({score}%)</small>
                    <div class="score-track"><div class="score-fill" style="width:{score}%"></div></div>
                  </div>
                </div>
                """,
                unsafe_allow_html=True,
            )

        with action_col:
            st.write("")
            if st.button("✨ Gerar abordagem", key=f"ia_{lead_id}"):
                sugestao = gerar_abordagem_ia(provedor_raw, responsavel_raw, dor_raw, produto_raw)
                st.markdown(
                    f'<div class="ai-response"><b>Abordagem sugerida</b><br><br>{escape(sugestao)}</div>',
                    unsafe_allow_html=True,
                )
                registrar_log(f"Abordagem gerada para {provedor_raw}", "AI_ENGINE")

            if st.button("🗑️ Excluir lead", key=f"excluir_{lead_id}"):
                st.session_state.confirmar_exclusao = lead_id
                st.rerun()

            if st.session_state.confirmar_exclusao == lead_id:
                st.warning(f"Excluir {provedor_raw} permanentemente?")
                confirmar_col, cancelar_col = st.columns(2)
                with confirmar_col:
                    if st.button("Confirmar", key=f"confirmar_{lead_id}"):
                        novos = df[df["ID"].astype(str) != lead_id].copy()
                        if salvar_dados(novos):
                            registrar_log(f"Lead {provedor_raw} ({lead_id}) excluído", "USUARIO")
                            st.session_state.confirmar_exclusao = None
                            st.success("Lead excluído.")
                            st.rerun()
                with cancelar_col:
                    if st.button("Cancelar", key=f"cancelar_{lead_id}"):
                        st.session_state.confirmar_exclusao = None
                        st.rerun()

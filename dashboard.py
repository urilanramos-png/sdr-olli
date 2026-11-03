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
            box-shadow: 0 10px 30px rgba(124,58,237,.07); animation: card-enter .35s ease both;
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

# Mascote pequeno em SVG sombreado: segue o cursor por toda a página com atraso
# suave, caminha enquanto se desloca e aponta a lanterna quando para. O cursor
# deixa um rastro de luz roxa semelhante a uma estrela cadente.
components.html(
    """
    <script>
    (() => {
      try {
        const win = window.parent;
        const doc = win.document;
        if (doc.getElementById('olli-effects')) return;

        const style = doc.createElement('style');
        style.textContent = `
          #olli-effects { position: fixed; inset: 0; z-index: 2147483644; pointer-events: none; overflow: visible; }
          #olli-pointer-glow {
            position: fixed; width: 32px; height: 32px; left: 0; top: 0; opacity: 0;
            transform: translate(-50%, -50%); border-radius: 50%;
            background: radial-gradient(circle, rgba(255,255,255,.95) 0%, rgba(216,180,254,.9) 12%, rgba(168,85,247,.62) 34%, rgba(124,58,237,.25) 58%, transparent 76%);
            filter: blur(2px); pointer-events: none; will-change: left, top, opacity;
            transition: opacity .16s ease;
          }
          #olli-pointer-trail {
            position: fixed; left: 0; top: 0; width: 125px; height: 10px; opacity: 0;
            transform-origin: 100% 50%; border-radius: 100%; pointer-events: none;
            background: linear-gradient(90deg, transparent 0%, rgba(124,58,237,.03) 24%, rgba(168,85,247,.36) 70%, rgba(233,213,255,.95) 100%);
            filter: blur(2px) drop-shadow(0 0 7px rgba(168,85,247,.95));
            will-change: left, top, transform, opacity; transition: opacity .12s ease;
          }
          #olli-pointer-trail::after {
            content: ''; position: absolute; right: -2px; top: 3px; width: 7px; height: 4px;
            border-radius: 50%; background: #fff; box-shadow: 0 0 8px 3px #C084FC, 0 0 18px 6px rgba(124,58,237,.8);
          }
          #olli-walker {
            position: fixed; left: 40px; top: 40px; width: 64px; height: 76px;
            opacity: .97; pointer-events: none; will-change: left, top;
            filter: drop-shadow(0 5px 7px rgba(124,58,237,.38));
          }
          #olli-walker svg { display: block; width: 100%; height: 100%; overflow: visible; }
          #olli-sprite { transform-box: view-box; transform-origin: 60px 75px; }
          #olli-sprite.walking #olli-leg-a { animation: olli-step-a .25s ease-in-out infinite alternate; transform-box: view-box; transform-origin: 50px 108px; }
          #olli-sprite.walking #olli-leg-b { animation: olli-step-b .25s ease-in-out infinite alternate; transform-box: view-box; transform-origin: 71px 108px; }
          #olli-sprite.walking #olli-arm-free { animation: olli-arm-swing .25s ease-in-out infinite alternate; transform-box: view-box; transform-origin: 48px 67px; }
          #olli-lantern { transform-box: view-box; transition: transform .16s ease-out; }
          #olli-lantern-beam { filter: drop-shadow(0 0 5px rgba(192,132,252,.95)); opacity: .75; }
          @keyframes olli-step-a { from { transform: rotate(-18deg); } to { transform: rotate(18deg); } }
          @keyframes olli-step-b { from { transform: rotate(18deg); } to { transform: rotate(-18deg); } }
          @keyframes olli-arm-swing { from { transform: rotate(11deg); } to { transform: rotate(-11deg); } }
          @media (prefers-reduced-motion: reduce) {
            #olli-sprite.walking *, #olli-sprite.walking *::before { animation: none !important; }
            #olli-lantern { transition: none !important; }
          }
        `;
        doc.head.appendChild(style);

        const wrap = doc.createElement('div');
        wrap.id = 'olli-effects';
        wrap.innerHTML = `
          <div id="olli-pointer-trail" aria-hidden="true"></div>
          <div id="olli-pointer-glow" aria-hidden="true"></div>
          <div id="olli-walker" aria-hidden="true">
            <svg viewBox="0 0 120 140" xmlns="http://www.w3.org/2000/svg" role="presentation">
              <defs>
                <radialGradient id="olli-face" cx="32%" cy="24%" r="78%">
                  <stop stop-color="#FFFDF8"/><stop offset=".62" stop-color="#E9D5FF"/><stop offset="1" stop-color="#A78BFA"/>
                </radialGradient>
                <linearGradient id="olli-coat" x1="0" y1="0" x2="1" y2="1">
                  <stop stop-color="#DDD6FE"/><stop offset=".42" stop-color="#8B5CF6"/><stop offset="1" stop-color="#3B1A72"/>
                </linearGradient>
                <linearGradient id="olli-sleeve" x1="0" y1="0" x2="1" y2="1">
                  <stop stop-color="#E9D5FF"/><stop offset="1" stop-color="#7C3AED"/>
                </linearGradient>
                <linearGradient id="olli-boot" x1="0" y1="0" x2="0" y2="1">
                  <stop stop-color="#C4B5FD"/><stop offset="1" stop-color="#4C1D95"/>
                </linearGradient>
                <radialGradient id="olli-lamp-glow">
                  <stop stop-color="#FFF7CC" stop-opacity=".95"/><stop offset=".42" stop-color="#FDE68A" stop-opacity=".55"/><stop offset="1" stop-color="#A855F7" stop-opacity="0"/>
                </radialGradient>
              </defs>
              <ellipse cx="60" cy="132" rx="25" ry="4" fill="#8B5CF6" opacity=".22"/>
              <g id="olli-sprite">
                <!-- legs with articulated joints and boots -->
                <path id="olli-leg-a" d="M49 103 L45 119" stroke="#BBA6F5" stroke-width="7" stroke-linecap="round"/>
                <path id="olli-leg-b" d="M69 103 L74 119" stroke="#D8CCFA" stroke-width="7" stroke-linecap="round"/>
                <path d="M45 117 Q39 120 38 126 Q46 129 55 126 L53 120 Z" fill="url(#olli-boot)" stroke="#D8B4FE" stroke-width=".8"/>
                <path d="M73 117 Q71 123 75 127 Q84 129 90 125 L84 120 Z" fill="url(#olli-boot)" stroke="#D8B4FE" stroke-width=".8"/>
                <path d="M39 126 Q46 128 55 126 M75 127 Q82 129 90 125" stroke="#F5D0FE" stroke-opacity=".8" stroke-width="1.2"/>
                <!-- layered coat, seams and light/shadow for volume -->
                <path d="M42 57 Q59 48 76 57 L81 103 Q61 111 39 103 Z" fill="url(#olli-coat)" stroke="#DDD6FE" stroke-width="1.3"/>
                <path d="M43 59 Q49 55 54 55 L52 106 L39 103 Z" fill="#F5D0FE" opacity=".22"/>
                <path d="M57 57 L61 103 M69 58 L74 101" stroke="#E9D5FF" stroke-opacity=".35" stroke-width="1"/>
                <path d="M54 68 L68 68 L67 87 Q61 91 55 87 Z" fill="#4C1D95" opacity=".48"/>
                <circle cx="61" cy="76" r="2.2" fill="#67E8F9"/>
                <path d="M55 97 Q61 100 68 97" stroke="#F5D0FE" stroke-opacity=".72" stroke-width="1" fill="none"/>
                <!-- head, hair, face highlights and features -->
                <path d="M46 35 Q47 20 60 19 Q76 19 78 35 L75 52 Q71 61 60 61 Q48 59 45 49 Z" fill="url(#olli-face)" stroke="#F5D0FE" stroke-width="1.3"/>
                <path d="M46 38 Q44 22 58 17 Q73 15 79 31 Q70 27 64 30 Q55 30 47 42 Z" fill="#5B2A9D"/>
                <path d="M49 34 Q54 23 64 22" stroke="#E9D5FF" stroke-opacity=".85" stroke-width="2" fill="none" stroke-linecap="round"/>
                <ellipse cx="54" cy="41" rx="1.7" ry="2.4" fill="#30204F"/>
                <ellipse cx="68" cy="40" rx="1.7" ry="2.4" fill="#30204F"/>
                <circle cx="54.5" cy="40.5" r=".55" fill="#FFF"/><circle cx="68.5" cy="39.5" r=".55" fill="#FFF"/>
                <path d="M57 49 Q61 52 66 48" stroke="#A855F7" stroke-width="1.4" fill="none" stroke-linecap="round"/>
                <!-- free arm -->
                <path id="olli-arm-free" d="M43 65 L34 82 L41 86 L51 72" fill="none" stroke="url(#olli-sleeve)" stroke-width="8" stroke-linecap="round" stroke-linejoin="round"/>
                <path d="M34 81 L31 86" stroke="#F1EAFE" stroke-width="5" stroke-linecap="round"/>
                <!-- lantern arm and articulated hand -->
                <path d="M75 64 Q83 69 88 77" fill="none" stroke="url(#olli-sleeve)" stroke-width="8" stroke-linecap="round"/>
                <circle cx="89" cy="78" r="3.4" fill="#F1EAFE" stroke="#C4B5FD" stroke-width=".8"/>
                <g id="olli-lantern" transform="rotate(0 91 78)">
                  <path id="olli-lantern-beam" d="M93 75 L119 58 Q121 79 108 98 Z" fill="url(#olli-lamp-glow)"/>
                  <path d="M88 74 Q89 69 94 71 L99 78 L95 84 L89 81 Z" fill="#FBBF24" stroke="#FFF0B3" stroke-width="1.3"/>
                  <path d="M89 73 L94 70 L98 74" fill="none" stroke="#FFF9DB" stroke-width="1.2" stroke-linecap="round"/>
                  <circle cx="95" cy="78" r="2.5" fill="#FFFBEA"/>
                  <path d="M89 82 L95 85" stroke="#B45309" stroke-width="1"/>
                </g>
                <!-- soft rim light -->
                <path d="M43 61 Q40 80 42 98" fill="none" stroke="#F5D0FE" stroke-opacity=".38" stroke-width="1.2"/>
              </g>
            </svg>
          </div>
        `;
        doc.body.appendChild(wrap);

        const walker = doc.getElementById('olli-walker');
        const sprite = doc.getElementById('olli-sprite');
        const lantern = doc.getElementById('olli-lantern');
        const glow = doc.getElementById('olli-pointer-glow');
        const trail = doc.getElementById('olli-pointer-trail');
        const reduceMotion = win.matchMedia('(prefers-reduced-motion: reduce)');
        const size = { width: 64, height: 76 };
        let pointer = { x: win.innerWidth * .5, y: win.innerHeight * .65 };
        let position = { x: Math.max(12, pointer.x - 78), y: Math.max(12, pointer.y - 90) };
        let previousPointer = null;
        let lastDirection = 1;
        let stopWalkTimer = 0;
        let lastFrame = 0;

        walker.style.left = `${position.x}px`;
        walker.style.top = `${position.y}px`;

        doc.addEventListener('pointermove', (event) => {
          if (event.pointerType === 'touch') return;
          pointer = { x: event.clientX, y: event.clientY };
          glow.style.left = `${pointer.x}px`;
          glow.style.top = `${pointer.y}px`;
          glow.style.opacity = '1';

          if (previousPointer) {
            const dx = pointer.x - previousPointer.x;
            const dy = pointer.y - previousPointer.y;
            const distance = Math.hypot(dx, dy);
            if (distance > 1) {
              if (Math.abs(dx) > 1.5) lastDirection = dx > 0 ? 1 : -1;
              const angle = Math.atan2(dy, dx) * 180 / Math.PI;
              trail.style.left = `${pointer.x}px`;
              trail.style.top = `${pointer.y}px`;
              trail.style.transform = `translate(-100%, -50%) rotate(${angle}deg)`;
              trail.style.opacity = '1';
              win.clearTimeout(trail._fadeTimer);
              trail._fadeTimer = win.setTimeout(() => { trail.style.opacity = '0'; }, 170);
              sprite.classList.add('walking');
              win.clearTimeout(stopWalkTimer);
              stopWalkTimer = win.setTimeout(() => sprite.classList.remove('walking'), 280);
            }
          }
          previousPointer = { x: pointer.x, y: pointer.y };
        }, { passive: true, capture: true });

        doc.addEventListener('pointerleave', () => {
          glow.style.opacity = '0';
          trail.style.opacity = '0';
        }, { passive: true });

        const animate = (time) => {
          const elapsed = lastFrame ? Math.min(time - lastFrame, 32) : 16;
          lastFrame = time;
          // Mascote persegue o cursor com suavização e fica próximo quando o mouse para.
          const targetX = pointer.x + (lastDirection > 0 ? -72 : 8);
          const targetY = pointer.y - 88;
          const maxX = Math.max(8, win.innerWidth - size.width - 8);
          const maxY = Math.max(8, win.innerHeight - size.height - 8);
          const clampedX = Math.max(8, Math.min(maxX, targetX));
          const clampedY = Math.max(8, Math.min(maxY, targetY));
          const follow = reduceMotion.matches ? .28 : Math.min(.13, elapsed * .0052);
          position.x += (clampedX - position.x) * follow;
          position.y += (clampedY - position.y) * follow;
          walker.style.left = `${position.x}px`;
          walker.style.top = `${position.y}px`;

          // Vira o corpo para o sentido do deslocamento; parado, mira a luz no cursor.
          const moveX = clampedX - position.x;
          const facing = Math.abs(moveX) > 2 ? (moveX > 0 ? 1 : -1) : lastDirection;
          sprite.setAttribute('transform', facing > 0 ? '' : 'translate(120 0) scale(-1 1)');
          const scale = size.width / 120;
          const handX = position.x + (facing > 0 ? 91 : 29) * scale;
          const handY = position.y + 78 * (size.height / 140);
          const localTargetX = facing > 0 ? pointer.x : 120 * scale - (pointer.x - position.x);
          const angle = Math.atan2(pointer.y - handY, localTargetX - (facing > 0 ? 91 : 29) * scale) * 180 / Math.PI;
          lantern.setAttribute('transform', `rotate(${Math.max(-75, Math.min(75, angle))} 91 78)`);

          win.requestAnimationFrame(animate);
        };
        win.requestAnimationFrame(animate);

        win.addEventListener('resize', () => {
          position.x = Math.min(position.x, Math.max(8, win.innerWidth - size.width - 8));
          position.y = Math.min(position.y, Math.max(8, win.innerHeight - size.height - 8));
        }, { passive: true });
      } catch (_) { /* Ignore browser restrictions for embedded components. */ }
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
        "ID": "ISP-701", "Status Contato": "Qualificado", "Provedor": "Alpha Fibra Telecom",
        "Responsáveis": "Carlos Silva", "Cargo": "Diretor de Operações", "Localidade": "Chapecó - SC",
        "Telefone": "(49) 3321-1000", "Email": "diretoria@alphafibra.com.br",
        "Situação de Mercado": "Guerra de preço agressiva / Perda de margem na região",
        "Produto Olli": "Olli Smart Home", "CNPJ": "31.862.534/0001-30",
        "Clientes Estimados": 12000, "Ticket Médio (R$)": 89.90, "Data Cadastro": "2026-01-10",
        "Score Conectividade": 88, "Origem Lead": "Outbound LinkedIn",
    },
    {
        "ID": "ISP-702", "Status Contato": "Não Chamado", "Provedor": "Beta Net Telecom",
        "Responsáveis": "Rodrigo Ramos", "Cargo": "CEO", "Localidade": "Blumenau - SC",
        "Telefone": "(47) 3211-5500", "Email": "rodrigo@betanet.net.br",
        "Situação de Mercado": "Churn alto detectado em relatórios ANATEL", "Produto Olli": "Olli Habita",
        "CNPJ": "14.552.112/0001-99", "Clientes Estimados": 7500, "Ticket Médio (R$)": 79.90,
        "Data Cadastro": "2026-02-15", "Score Conectividade": 45, "Origem Lead": "Mapeamento ANATEL",
    },
    {
        "ID": "ISP-703", "Status Contato": "Agendado (Reunião)", "Provedor": "Wave Conectividade",
        "Responsáveis": "Juliana Mendes", "Cargo": "Gerente de Marketing", "Localidade": "Maringá - PR",
        "Telefone": "(44) 99881-2233", "Email": "juliana@waveconect.com.br",
        "Situação de Mercado": "Estagnação de vendas / Sem serviços de valor agregado (SVA)",
        "Produto Olli": "Olli Smart Home", "CNPJ": "45.123.789/0001-02",
        "Clientes Estimados": 24000, "Ticket Médio (R$)": 110.00, "Data Cadastro": "2026-03-22",
        "Score Conectividade": 92, "Origem Lead": "Inbound - Evento IXC",
    },
]


def registrar_log(mensagem: str, usuario: str = "Sistema") -> None:
    try:
        with open(ARQUIVO_LOGS, "a", encoding="utf-8") as arquivo:
            arquivo.write(f"[{datetime.now():%Y-%m-%d %H:%M:%S}] [{usuario}] {mensagem}\n")
    except OSError:
        pass


def normalizar_df(df: pd.DataFrame) -> pd.DataFrame:
    if df is None:
        return pd.DataFrame(DADOS_INICIAIS, columns=COLUNAS)
    df = df.copy()
    for coluna in COLUNAS:
        if coluna not in df.columns:
            df[coluna] = 0 if coluna in ("Clientes Estimados", "Score Conectividade") else "Não Informado"
    df["Clientes Estimados"] = pd.to_numeric(df["Clientes Estimados"], errors="coerce").fillna(0)
    df["Score Conectividade"] = pd.to_numeric(df["Score Conectividade"], errors="coerce").fillna(0).clip(0, 100)
    return df


@st.cache_data(ttl=60, show_spinner=False)
def carregar_dados() -> pd.DataFrame:
    if not os.path.exists(ARQUIVO_BANCO_DADOS):
        df = pd.DataFrame(DADOS_INICIAIS, columns=COLUNAS)
        try:
            df.to_csv(ARQUIVO_BANCO_DADOS, index=False, encoding="utf-8")
        except OSError:
            pass
        registrar_log("Base de dados inicializada.")
        return normalizar_df(df)
    try:
        df = pd.read_csv(ARQUIVO_BANCO_DADOS, encoding="utf-8")
    except (OSError, pd.errors.ParserError, UnicodeDecodeError) as erro:
        registrar_log(f"Falha ao carregar banco de dados: {erro}", "ERRO")
        return normalizar_df(pd.DataFrame(DADOS_INICIAIS, columns=COLUNAS))
    return normalizar_df(df)


def salvar_dados(df: pd.DataFrame) -> bool:
    try:
        normalizar_df(df).to_csv(ARQUIVO_BANCO_DADOS, index=False, encoding="utf-8")
        carregar_dados.clear()
        return True
    except OSError as erro:
        st.error(f"Não foi possível salvar as alterações: {erro}")
        return False


def gerar_abordagem_ia(provedor: str, responsavel: str, dor: str, produto: str) -> str:
    provedor = provedor or "o provedor"
    responsavel = responsavel or "o responsável"
    dor = dor or "a dor atual do mercado"
    produto = produto or "a solução Olli"
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
              <radialGradient id="emptyGlow"><stop stop-color="#FDE68A" stop-opacity=".65"/><stop offset="1" stop-color="#A855F7" stop-opacity="0"/></radialGradient>
              <linearGradient id="emptyBody" x1="0" y1="0" x2="1" y2="1"><stop stop-color="#F5D0FE"/><stop offset="1" stop-color="#7C3AED"/></linearGradient>
            </defs>
            <ellipse cx="96" cy="111" rx="72" ry="8" fill="#7C3AED" opacity=".15"/>
            <g class="walker" style="filter:drop-shadow(0 8px 8px rgba(168,85,247,.35))">
              <path d="M101 68 L154 42 Q165 62 151 82 Z" fill="url(#emptyGlow)"/>
              <circle cx="86" cy="37" r="10" fill="#F5D0FE" stroke="#FFF" stroke-opacity=".5"/>
              <path d="M77 50 Q87 46 96 51 L100 78 L75 78 Z" fill="url(#emptyBody)" stroke="#DDD6FE" stroke-width="1.2"/>
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
st.session_state.setdefault("termo_busca_provedor", "")
st.session_state.setdefault("confirmar_exclusao", None)
st.session_state.setdefault("scroll_resultados", False)

try:
    df = normalizar_df(carregar_dados().copy())
except Exception:
    df = normalizar_df(pd.DataFrame(DADOS_INICIAIS, columns=COLUNAS))

st.markdown('<div class="cyber-title">⚡ Olli Hub Enterprise v2.0</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">SDR Intelligence Matrix &amp; Real-time Network Mapping</div>', unsafe_allow_html=True)

k1, k2, k3 = st.columns(3)
with k1:
    st.markdown(f'<div class="kpi-container"><div class="kpi-title">Total Provedores</div><div class="kpi-value">{len(df)}</div></div>', unsafe_allow_html=True)
with k2:
    st.markdown(f'<div class="kpi-container" style="border-left-color:#A855F7"><div class="kpi-title">Clientes Estimados</div><div class="kpi-value">{int(df["Clientes Estimados"].sum()):,}</div></div>', unsafe_allow_html=True)
with k3:
    media = int(df["Score Conectividade"].mean()) if not df.empty else 0
    st.markdown(f'<div class="kpi-container" style="border-left-color:#22D3EE"><div class="kpi-title">Score Médio</div><div class="kpi-value">{media}%</div></div>', unsafe_allow_html=True)

st.write("---")
st.markdown("### 🔎 Busca de provedores")
with st.form("form_busca_provedor", clear_on_submit=False):
    campo_busca, botao_busca = st.columns([5, 1])
    with campo_busca:
        termo_digitado = st.text_input("Busca", placeholder="Nome do provedor ou cidade...", label_visibility="collapsed", key="campo_busca_provedor")
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
        st.session_state["campo_busca_provedor"] = ""
        st.session_state.scroll_resultados = False
        st.rerun()

termo = st.session_state.termo_busca_provedor.strip()
if termo:
    prov_match = df["Provedor"].fillna("").astype(str).str.contains(termo, case=False, regex=False)
    local_match = df["Localidade"].fillna("").astype(str).str.contains(termo, case=False, regex=False)
    resultados = df[prov_match | local_match].copy()
else:
    resultados = df.copy()

st.markdown('<div id="scroll-resultados"></div>', unsafe_allow_html=True)
if st.session_state.scroll_resultados:
    components.html("""
        <script>
          setTimeout(() => {
            const el = window.parent.document.getElementById('scroll-resultados');
            if (el) el.scrollIntoView({ behavior: 'smooth', block: 'start' });
          }, 120);
        </script>
        """, height=0)
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
        score_val = pd.to_numeric(row.get("Score Conectividade", 0), errors="coerce")
        score = max(0, min(100, int(score_val))) if pd.notna(score_val) else 0

        card_col, action_col = st.columns([4, 1])
        with card_col:
            provedor = escape(provedor_raw)
            status = escape(str(row.get("Status Contato", "Não informado")))
            local = escape(str(row.get("Localidade", "Não informada")))
            responsavel = escape(responsavel_raw)
            cargo = escape(str(row.get("Cargo", "Não informado")))
            produto = escape(produto_raw)
            dor = escape(dor_raw)
            st.markdown(f"""
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
                """, unsafe_allow_html=True)

        with action_col:
            st.write("")
            if st.button("✨ Gerar abordagem", key=f"ia_{lead_id}"):
                sugestao = gerar_abordagem_ia(provedor_raw, responsavel_raw, dor_raw, produto_raw)
                st.markdown(f'<div class="ai-response"><b>Abordagem sugerida</b><br><br>{escape(sugestao)}</div>', unsafe_allow_html=True)
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

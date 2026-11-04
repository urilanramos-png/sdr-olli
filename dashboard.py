# Dica: crie .streamlit/config.toml com [theme] base = "dark" e primaryColor = "#A855F7"
# para que os widgets nativos do Streamlit acompanhem a paleta do Olli Hub.
from __future__ import annotations

import hashlib
import json
import os
import re
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime
from html import escape, unescape

import pandas as pd
import requests
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

CSS_GLOBAL = """
@import url('https://fonts.googleapis.com/css2?family=Chakra+Petch:wght@500;600;700&family=Inter:wght@400;500;600&display=swap');
:root {
  color-scheme: dark;
  --bg-1: #0B071E; --bg-2: #120B2D;
  --violet: #7C3AED; --violet-2: #A855F7; --violet-3: #C084FC;
  --cyan: #22D3EE; --green: #34D399;
  --text: #E2E8F0; --muted: #94A3B8; --faint: #8B98B2;
  --glass: rgba(22, 15, 60, .55); --line: rgba(168, 85, 247, .28);
  --display: "Chakra Petch", Inter, system-ui, sans-serif;
}
html, body, [data-testid="stAppViewContainer"], .main {
  background:
    linear-gradient(rgba(168,85,247,.045) 1px, transparent 1px) 0 0 / 56px 56px,
    linear-gradient(90deg, rgba(34,211,238,.035) 1px, transparent 1px) 0 0 / 56px 56px,
    radial-gradient(1000px 520px at 8% -6%, rgba(124,58,237,.32), transparent 60%),
    radial-gradient(820px 460px at 100% 0%, rgba(34,211,238,.13), transparent 58%),
    linear-gradient(180deg, var(--bg-1) 0%, var(--bg-2) 100%);
  background-attachment: fixed;
  color: var(--text) !important;
  font-family: Inter, system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
}
header[data-testid="stHeader"] { background: transparent; }
footer { visibility: hidden; }
hr { border-color: var(--line) !important; }
::selection { background: rgba(168, 85, 247, .45); }
::-webkit-scrollbar { width: 10px; height: 10px; }
::-webkit-scrollbar-track { background: #07041A; }
::-webkit-scrollbar-thumb { background: linear-gradient(180deg, var(--violet), var(--cyan)); border-radius: 8px; }
h1, h2, h3, h4 { font-family: var(--display); letter-spacing: -.01em; color: #F5F3FF !important; }
h3 { text-shadow: 0 0 18px rgba(168, 85, 247, .35); }
[data-testid="stWidgetLabel"] p, [data-testid="stCaptionContainer"], label { color: var(--muted) !important; }
[data-testid="stSidebar"] { background: linear-gradient(180deg, #070414 0%, #0D0826 100%) !important; border-right: 1px solid var(--line); }
.sidebar-brand { font-family: var(--display); font-size: 1.2rem; font-weight: 700; color: #F5F3FF; text-shadow: 0 0 16px rgba(168,85,247,.8); margin: 4px 0 2px; }
.sidebar-brand span { color: var(--cyan); text-shadow: 0 0 16px rgba(34,211,238,.7); }
.cyber-title {
  font-family: var(--display); font-size: clamp(2rem, 4vw, 2.9rem); font-weight: 700; line-height: 1.1; margin-bottom: .35rem;
  background: linear-gradient(110deg, #C084FC 0%, #7C3AED 30%, #22D3EE 62%, #C084FC 100%); background-size: 220% 100%;
  -webkit-background-clip: text; background-clip: text; color: transparent;
  filter: drop-shadow(0 0 18px rgba(168,85,247,.45)); animation: title-flow 10s linear infinite;
}
@keyframes title-flow { to { background-position: -220% 0; } }
.subtitle { color: var(--muted); font-size: 1.02rem; margin-bottom: 1.3rem; display: flex; align-items: center; gap: 12px; flex-wrap: wrap; }
.live { display: inline-flex; align-items: center; gap: 8px; padding: 3px 11px; border: 1px solid rgba(52,211,153,.38); border-radius: 999px; background: rgba(52,211,153,.08); color: #6EE7B7; font-size: .78rem; font-weight: 600; }
.live::before { content: ""; width: 7px; height: 7px; border-radius: 50%; background: var(--green); box-shadow: 0 0 10px var(--green); animation: pulse 1.8s ease-in-out infinite; }
@keyframes pulse { 50% { opacity: .35; transform: scale(.7); } }
div[data-testid="stTextInput"] input, div[data-baseweb="select"] > div {
  background: rgba(15, 10, 36, .8) !important; color: var(--text) !important;
  border: 1px solid rgba(168, 85, 247, .45) !important; border-radius: 12px !important; min-height: 44px;
  transition: border-color .2s ease, box-shadow .2s ease;
}
div[data-testid="stTextInput"] input:focus, div[data-baseweb="select"] > div:focus-within {
  border-color: var(--cyan) !important; box-shadow: 0 0 0 3px rgba(34,211,238,.16), 0 0 18px rgba(34,211,238,.25) !important;
}
div[data-baseweb="popover"] ul, ul[role="listbox"] { background: #120B2D !important; color: var(--text) !important; border: 1px solid var(--line); }
li[role="option"]:hover { background: rgba(124, 58, 237, .32) !important; }
span[data-baseweb="tag"] { background: rgba(124, 58, 237, .38) !important; color: #F5F3FF !important; border-radius: 8px !important; }
:is(div.stButton, div[data-testid="stFormSubmitButton"], div[data-testid="stDownloadButton"]) button {
  position: relative; overflow: hidden; width: 100%; min-height: 44px; color: #fff !important;
  border: 1px solid rgba(255,255,255,.14) !important; border-radius: 12px !important; font-weight: 650 !important;
  background: linear-gradient(135deg, #6D28D9, #A855F7) !important;
  transition: transform .18s ease, box-shadow .18s ease, filter .18s ease !important;
}
:is(div.stButton, div[data-testid="stFormSubmitButton"], div[data-testid="stDownloadButton"]) button::after {
  content: ""; position: absolute; inset: 0; pointer-events: none;
  background: linear-gradient(105deg, transparent 35%, rgba(255,255,255,.28) 50%, transparent 65%);
  transform: translateX(-120%); transition: transform .6s ease;
}
:is(div.stButton, div[data-testid="stFormSubmitButton"], div[data-testid="stDownloadButton"]) button:hover {
  transform: translateY(-2px); box-shadow: 0 0 24px rgba(168,85,247,.5), 0 0 0 1px rgba(34,211,238,.45) !important;
}
:is(div.stButton, div[data-testid="stFormSubmitButton"], div[data-testid="stDownloadButton"]) button:hover::after { transform: translateX(120%); }
button:disabled { opacity: .45 !important; filter: saturate(.4); }
button:focus-visible, a:focus-visible, input:focus-visible { outline: 2px solid var(--cyan) !important; outline-offset: 2px; }
[class*="st-key-ia_"] button { background: linear-gradient(135deg, #0891B2, #7C3AED) !important; }
[class*="st-key-excluir_"] button { background: linear-gradient(135deg, #9F1239, #E11D48) !important; }
[class*="st-key-limpar_busca"] button { background: transparent !important; border: 1px solid var(--line) !important; }
.kpi-container {
  position: relative; overflow: hidden; min-height: 108px; padding: 18px; border: 1px solid var(--line); border-radius: 16px;
  background: var(--glass); backdrop-filter: blur(14px) saturate(140%);
  box-shadow: inset 0 1px 0 rgba(255,255,255,.06), 0 10px 30px rgba(0,0,0,.25); animation: card-enter .45s ease both;
}
.kpi-container::before { content: ""; position: absolute; inset: 0 0 auto 0; height: 2px; background: linear-gradient(90deg, var(--accent, #7C3AED), transparent); box-shadow: 0 0 14px var(--accent, #7C3AED); }
.kpi-title { color: var(--muted); font-size: .82rem; font-weight: 600; letter-spacing: .06em; }
.kpi-value { margin-top: 6px; color: #fff; font-family: var(--display); font-size: 2rem; font-weight: 700; font-variant-numeric: tabular-nums; text-shadow: 0 0 22px var(--accent, #7C3AED); }
.hologram-card {
  position: relative; margin-bottom: 12px; padding: 20px; border: 1px solid var(--line); border-radius: 18px;
  background: linear-gradient(160deg, rgba(30,20,78,.55), rgba(12,8,34,.72)); backdrop-filter: blur(14px) saturate(140%);
  box-shadow: inset 0 1px 0 rgba(255,255,255,.06), 0 14px 36px rgba(0,0,0,.3);
  animation: card-enter .45s ease both; transition: transform .25s ease, border-color .25s ease, box-shadow .25s ease;
}
.hologram-card:hover { transform: translateY(-3px); border-color: rgba(34,211,238,.55); box-shadow: 0 0 0 1px rgba(34,211,238,.22), 0 18px 44px rgba(124,58,237,.28), 0 0 34px rgba(34,211,238,.12); }
.hologram-card::before, .hologram-card::after { content: ""; position: absolute; width: 14px; height: 14px; pointer-events: none; transition: width .25s ease, height .25s ease; }
.hologram-card::before { top: -1px; left: -1px; border-top: 2px solid var(--cyan); border-left: 2px solid var(--cyan); border-top-left-radius: 18px; }
.hologram-card::after { right: -1px; bottom: -1px; border-right: 2px solid var(--violet-2); border-bottom: 2px solid var(--violet-2); border-bottom-right-radius: 18px; }
.hologram-card:hover::before, .hologram-card:hover::after { width: 28px; height: 28px; }
@keyframes card-enter { from { opacity: 0; transform: translateY(12px); } to { opacity: 1; transform: translateY(0); } }
.card-head { display: flex; justify-content: space-between; align-items: center; gap: 12px; flex-wrap: wrap; }
.card-title { color: var(--cyan); font-family: var(--display); font-size: 1.3rem; font-weight: 700; text-shadow: 0 0 18px rgba(34,211,238,.4); }
.pill { padding: 4px 12px; border: 1px solid currentColor; border-radius: 999px; font-size: .78rem; font-weight: 600; }
.card-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(170px, 1fr)); gap: 14px; margin-top: 16px; }
.meta-label { display: block; margin-bottom: 2px; color: var(--faint); font-size: .74rem; letter-spacing: .04em; }
b.accent { color: var(--violet-3); }
.pain { margin-top: 15px; padding: 10px 12px; border-left: 3px solid var(--violet); border-radius: 8px; background: rgba(255,255,255,.03); color: #CBD5E1; }
.chips { display: flex; flex-wrap: wrap; gap: 8px; margin-top: 14px; }
.chip { padding: 4px 11px; border: 1px solid rgba(168,85,247,.28); border-radius: 999px; background: rgba(124,58,237,.14); color: #DDD6FE; font-size: .78rem; text-decoration: none !important; transition: border-color .2s ease, box-shadow .2s ease; }
a.chip:hover { border-color: var(--cyan); color: #fff; box-shadow: 0 0 14px rgba(34,211,238,.35); }
.score-label { margin-top: 14px; color: var(--muted); font-size: .78rem; }
.score-track { height: 9px; margin-top: 7px; overflow: hidden; border-radius: 8px; background: rgba(255,255,255,.08); }
.score-fill { height: 100%; border-radius: 8px; transform-origin: left; background: linear-gradient(90deg, var(--c1, #7C3AED), var(--c2, #22D3EE)); box-shadow: 0 0 12px var(--c2, #22D3EE); animation: fill-in 1s cubic-bezier(.2,.8,.2,1) both; }
@keyframes fill-in { from { transform: scaleX(0); } }
.ai-response { margin: 2px 0 16px; padding: 16px; border: 1px dashed rgba(6,182,212,.4); border-radius: 14px; background: linear-gradient(135deg, rgba(6,182,212,.09), rgba(124,58,237,.08)); color: #A5F3FC; line-height: 1.65; animation: card-enter .4s ease both; }
.ai-tag { display: inline-block; margin-bottom: 8px; padding: 2px 9px; border-radius: 6px; background: linear-gradient(90deg, var(--cyan), var(--violet-3)); color: #0B071E; font-size: .72rem; font-weight: 800; }
.empty-state {
  position: relative; overflow: hidden; text-align: center; padding: 30px 18px 22px; margin: 18px 0;
  border: 1px solid var(--line); border-radius: 20px;
  background: radial-gradient(ellipse at 50% 100%, rgba(124,58,237,.18), transparent 65%), rgba(18,11,45,.55);
}
.empty-title { color: #E9D5FF; font-family: var(--display); font-size: 1.3rem; font-weight: 700; margin: 8px 0 4px; }
.empty-copy { color: #A1A1AA; font-size: .95rem; }
.walker { transform-origin: center; animation: walk-across 8s ease-in-out infinite alternate; }
@keyframes walk-across { from { transform: translateX(-105px); } to { transform: translateX(105px); } }
@media (max-width: 640px) { .hologram-card { padding: 16px; } .kpi-value { font-size: 1.6rem; } }
@media (prefers-reduced-motion: reduce) {
  *, *::before, *::after { animation-duration: .01ms !important; animation-iteration-count: 1 !important; transition-duration: .01ms !important; }
}
"""
st.markdown("<style>" + CSS_GLOBAL + "</style>", unsafe_allow_html=True)

# Mascote em SVG sombreado: segue o cursor com atraso e velocidade limitados,
# anima os passos apenas enquanto caminha e mira com a lanterna quando alcança.
# Um rastro roxo com cintilação acompanha movimentos rápidos do mouse.
JS_EFEITOS_OLLI = """
<script>
(() => {
  try {
    const win = window.parent;
    const doc = win.document;
    if (win.__olliEffectsCleanup) win.__olliEffectsCleanup();
    doc.getElementById('olli-effects')?.remove();
    doc.getElementById('olli-effects-style')?.remove();

    const style = doc.createElement('style');
    style.id = 'olli-effects-style';
    style.textContent = `
      #olli-effects { position: fixed; inset: 0; z-index: 2147483644; pointer-events: none; overflow: visible; }
      #olli-star-canvas { position: fixed; inset: 0; width: 100%; height: 100%; pointer-events: none; }
      #olli-pointer-glow {
        position: fixed; width: 34px; height: 34px; left: 0; top: 0; opacity: 0;
        transform: translate(-50%, -50%); border-radius: 50%; pointer-events: none;
        background: radial-gradient(circle, rgba(255,255,255,.96) 0%, rgba(216,180,254,.9) 15%, rgba(168,85,247,.62) 38%, rgba(124,58,237,.22) 63%, transparent 80%);
        filter: blur(2px) drop-shadow(0 0 9px rgba(168,85,247,.9));
        transition: opacity .16s ease; will-change: left, top, opacity;
      }
      #olli-walker {
        position: fixed; left: 40px; top: 40px; width: 66px; height: 82px;
        opacity: .98; pointer-events: none; will-change: left, top;
        filter: drop-shadow(0 5px 8px rgba(91,33,182,.42));
      }
      #olli-walker svg { display: block; width: 100%; height: 100%; overflow: visible; }
      #olli-sprite { transform-box: view-box; transform-origin: 60px 75px; }
      #olli-sprite.walking #olli-leg-a { animation: olli-step-a .42s ease-in-out infinite alternate; transform-box: view-box; transform-origin: 49px 103px; }
      #olli-sprite.walking #olli-leg-b { animation: olli-step-b .42s ease-in-out infinite alternate; transform-box: view-box; transform-origin: 69px 103px; }
      #olli-sprite.walking #olli-arm-free { animation: olli-arm-swing .42s ease-in-out infinite alternate; transform-box: view-box; transform-origin: 43px 65px; }
      #olli-sprite.walking { animation: olli-body-bob .42s ease-in-out infinite alternate; }
      #olli-lantern { transform-box: view-box; transition: transform .18s ease-out; }
      #olli-lantern-beam { opacity: .84; filter: drop-shadow(0 0 6px rgba(192,132,252,.95)); }
      @keyframes olli-step-a { from { transform: rotate(-20deg); } to { transform: rotate(20deg); } }
      @keyframes olli-step-b { from { transform: rotate(18deg); } to { transform: rotate(-20deg); } }
      @keyframes olli-arm-swing { from { transform: rotate(12deg); } to { transform: rotate(-12deg); } }
      @keyframes olli-body-bob { from { translate: 0 0; } to { translate: 0 -1.5px; } }
      @media (prefers-reduced-motion: reduce) {
        #olli-sprite.walking, #olli-sprite.walking * { animation: none !important; }
        #olli-lantern { transition: none !important; }
      }
      @media (hover: none) { #olli-walker, #olli-pointer-glow { display: none; } }
    `;
    doc.head.appendChild(style);

    const wrap = doc.createElement('div');
    wrap.id = 'olli-effects';
    wrap.innerHTML = `
      <canvas id="olli-star-canvas" aria-hidden="true"></canvas>
      <div id="olli-pointer-glow" aria-hidden="true"></div>
      <div id="olli-walker" aria-hidden="true">
        <svg viewBox="0 0 120 140" xmlns="http://www.w3.org/2000/svg" role="presentation">
          <defs>
            <radialGradient id="olli-face" cx="32%" cy="24%" r="78%">
              <stop stop-color="#FFFDF8"/><stop offset=".62" stop-color="#E9D5FF"/><stop offset="1" stop-color="#A78BFA"/>
            </radialGradient>
            <linearGradient id="olli-coat" x1="0" y1="0" x2="1" y2="1">
              <stop stop-color="#E9D5FF"/><stop offset=".42" stop-color="#8B5CF6"/><stop offset="1" stop-color="#32145F"/>
            </linearGradient>
            <linearGradient id="olli-sleeve" x1="0" y1="0" x2="1" y2="1">
              <stop stop-color="#E9D5FF"/><stop offset="1" stop-color="#6D28D9"/>
            </linearGradient>
            <linearGradient id="olli-boot" x1="0" y1="0" x2="0" y2="1">
              <stop stop-color="#C4B5FD"/><stop offset="1" stop-color="#3B1A72"/>
            </linearGradient>
            <radialGradient id="olli-lamp-glow">
              <stop stop-color="#FFF7CC" stop-opacity=".98"/><stop offset=".42" stop-color="#FDE68A" stop-opacity=".6"/><stop offset="1" stop-color="#A855F7" stop-opacity="0"/>
            </radialGradient>
          </defs>
          <ellipse cx="60" cy="132" rx="25" ry="4" fill="#8B5CF6" opacity=".22"/>
          <g id="olli-sprite">
            <!-- legs, articulated boots and coat -->
            <path id="olli-leg-a" d="M49 103 L45 119" stroke="#BBA6F5" stroke-width="7" stroke-linecap="round"/>
            <path id="olli-leg-b" d="M69 103 L74 119" stroke="#D8CCFA" stroke-width="7" stroke-linecap="round"/>
            <path d="M45 117 Q39 120 38 126 Q46 129 55 126 L53 120 Z" fill="url(#olli-boot)" stroke="#D8B4FE" stroke-width=".8"/>
            <path d="M73 117 Q71 123 75 127 Q84 129 90 125 L84 120 Z" fill="url(#olli-boot)" stroke="#D8B4FE" stroke-width=".8"/>
            <path d="M42 57 Q59 48 76 57 L81 103 Q61 111 39 103 Z" fill="url(#olli-coat)" stroke="#DDD6FE" stroke-width="1.3"/>
            <path d="M43 59 Q49 55 54 55 L52 106 L39 103 Z" fill="#F5D0FE" opacity=".2"/>
            <path d="M57 57 L61 103 M69 58 L74 101" stroke="#E9D5FF" stroke-opacity=".34" stroke-width="1"/>
            <path d="M54 68 L68 68 L67 87 Q61 91 55 87 Z" fill="#32145F" opacity=".48"/>
            <circle cx="61" cy="76" r="2.2" fill="#67E8F9"/>
            <path d="M55 97 Q61 100 68 97" stroke="#F5D0FE" stroke-opacity=".7" stroke-width="1" fill="none"/>
            <!-- face, hair, subtle highlights and eyes -->
            <path d="M46 35 Q47 20 60 19 Q76 19 78 35 L75 52 Q71 61 60 61 Q48 59 45 49 Z" fill="url(#olli-face)" stroke="#F5D0FE" stroke-width="1.3"/>
            <path d="M46 38 Q44 22 58 17 Q73 15 79 31 Q70 27 64 30 Q55 30 47 42 Z" fill="#512583"/>
            <path d="M49 34 Q54 23 64 22" stroke="#E9D5FF" stroke-opacity=".8" stroke-width="2" fill="none" stroke-linecap="round"/>
            <ellipse cx="54" cy="41" rx="1.7" ry="2.4" fill="#30204F"/>
            <ellipse cx="68" cy="40" rx="1.7" ry="2.4" fill="#30204F"/>
            <circle cx="54.5" cy="40.5" r=".55" fill="#FFF"/><circle cx="68.5" cy="39.5" r=".55" fill="#FFF"/>
            <path d="M57 49 Q61 52 66 48" stroke="#A855F7" stroke-width="1.4" fill="none" stroke-linecap="round"/>
            <!-- free arm swings against the walking legs -->
            <path id="olli-arm-free" d="M43 65 L34 82 L41 86 L51 72" fill="none" stroke="url(#olli-sleeve)" stroke-width="8" stroke-linecap="round" stroke-linejoin="round"/>
            <path d="M34 81 L31 86" stroke="#F1EAFE" stroke-width="5" stroke-linecap="round"/>
            <!-- lantern arm and glowing lantern -->
            <path d="M75 64 Q83 69 88 77" fill="none" stroke="url(#olli-sleeve)" stroke-width="8" stroke-linecap="round"/>
            <circle cx="89" cy="78" r="3.4" fill="#F1EAFE" stroke="#C4B5FD" stroke-width=".8"/>
            <g id="olli-lantern" transform="rotate(0 91 78)">
              <path id="olli-lantern-beam" d="M93 75 L119 58 Q121 79 108 98 Z" fill="url(#olli-lamp-glow)"/>
              <path d="M88 74 Q89 69 94 71 L99 78 L95 84 L89 81 Z" fill="#FBBF24" stroke="#FFF0B3" stroke-width="1.3"/>
              <path d="M89 73 L94 70 L98 74" fill="none" stroke="#FFF9DB" stroke-width="1.2" stroke-linecap="round"/>
              <circle cx="95" cy="78" r="2.5" fill="#FFFBEA"/>
              <path d="M89 82 L95 85" stroke="#B45309" stroke-width="1"/>
            </g>
          </g>
        </svg>
      </div>
    `;
    doc.body.appendChild(wrap);

    const walker = doc.getElementById('olli-walker');
    const sprite = doc.getElementById('olli-sprite');
    const lantern = doc.getElementById('olli-lantern');
    const glow = doc.getElementById('olli-pointer-glow');
    const canvas = doc.getElementById('olli-star-canvas');
    const ctx = canvas.getContext('2d');
    const reduceMotion = win.matchMedia('(prefers-reduced-motion: reduce)');
    const width = 66;
    const height = 82;
    const cursor = { x: win.innerWidth * .55, y: win.innerHeight * .55 };
    const position = { x: cursor.x - 125, y: cursor.y - 75 };
    const velocity = { x: 0, y: 0 };
    const trail = [];
    let lastPointer = null;
    let lastDirection = 1;
    let lastTime = 0;
    let visible = false;
    let cleanup = () => {};
    // frameId/disposed garantem que o loop antigo pare quando o Streamlit reexecuta o script.
    let frameId = 0;
    let disposed = false;

    const clamp = (value, min, max) => Math.min(Math.max(value, min), max);

    function resizeCanvas() {
      const dpr = Math.min(win.devicePixelRatio || 1, 2);
      canvas.width = Math.round(win.innerWidth * dpr);
      canvas.height = Math.round(win.innerHeight * dpr);
      canvas.style.width = `${win.innerWidth}px`;
      canvas.style.height = `${win.innerHeight}px`;
      ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
    }
    resizeCanvas();

    function onPointerMove(event) {
      if (event.pointerType === 'touch') return;
      const now = performance.now();
      const point = { x: event.clientX, y: event.clientY, t: now };
      cursor.x = point.x;
      cursor.y = point.y;
      visible = true;
      glow.style.left = `${point.x}px`;
      glow.style.top = `${point.y}px`;
      glow.style.opacity = '1';

      if (lastPointer) {
        const dx = point.x - lastPointer.x;
        const dy = point.y - lastPointer.y;
        const distance = Math.hypot(dx, dy);
        const dt = Math.max(8, now - lastPointer.t);
        if (Math.abs(dx) > 1) lastDirection = dx > 0 ? 1 : -1;
        if (distance > 1) {
          // Keep cursor samples to paint a fading, intermittently twinkling comet tail.
          const steps = Math.min(7, Math.max(1, Math.ceil(distance / 24)));
          for (let i = 1; i <= steps; i++) {
            const ratio = i / steps;
            trail.push({
              x: lastPointer.x + dx * ratio,
              y: lastPointer.y + dy * ratio,
              t: now,
              life: 360 + Math.random() * 260,
              size: 1.2 + Math.random() * 2.5,
              phase: Math.random() * Math.PI * 2,
            });
          }
          // Limite de partículas: evita queda de FPS com movimentos muito rápidos.
          if (trail.length > 240) trail.splice(0, trail.length - 240);
          if (distance / dt > .18) sprite.classList.add('walking');
        }
      }
      lastPointer = point;
    }

    function onPointerLeave() {
      visible = false;
      glow.style.opacity = '0';
    }

    function drawTrail(now) {
      ctx.clearRect(0, 0, win.innerWidth, win.innerHeight);
      for (let i = trail.length - 1; i >= 0; i--) {
        const particle = trail[i];
        const age = now - particle.t;
        const progress = age / particle.life;
        if (progress >= 1) {
          trail.splice(i, 1);
          continue;
        }
        const flicker = .48 + .52 * Math.abs(Math.sin(now * .025 + particle.phase));
        const alpha = (1 - progress) * flicker;
        const radius = particle.size * (1 - progress * .45);
        const gradient = ctx.createRadialGradient(particle.x, particle.y, 0, particle.x, particle.y, radius * 5);
        gradient.addColorStop(0, `rgba(255,255,255,${alpha})`);
        gradient.addColorStop(.24, `rgba(216,180,254,${alpha * .95})`);
        gradient.addColorStop(.58, `rgba(168,85,247,${alpha * .7})`);
        gradient.addColorStop(1, 'rgba(124,58,237,0)');
        ctx.fillStyle = gradient;
        ctx.beginPath();
        ctx.arc(particle.x, particle.y, radius * 5, 0, Math.PI * 2);
        ctx.fill();
      }
      if (visible && lastPointer && trail.length) {
        const newest = trail[trail.length - 1];
        const dx = cursor.x - newest.x;
        const dy = cursor.y - newest.y;
        const length = Math.hypot(dx, dy);
        if (length > 2) {
          const tail = ctx.createLinearGradient(cursor.x, cursor.y, cursor.x - dx * 3, cursor.y - dy * 3);
          tail.addColorStop(0, 'rgba(255,255,255,.88)');
          tail.addColorStop(.25, 'rgba(192,132,252,.68)');
          tail.addColorStop(1, 'rgba(124,58,237,0)');
          ctx.strokeStyle = tail;
          ctx.lineWidth = 3;
          ctx.lineCap = 'round';
          ctx.shadowColor = '#A855F7';
          ctx.shadowBlur = 12;
          ctx.beginPath();
          ctx.moveTo(cursor.x, cursor.y);
          ctx.lineTo(cursor.x - dx * 3, cursor.y - dy * 3);
          ctx.stroke();
          ctx.shadowBlur = 0;
        }
      }
    }

    function animate(now) {
      if (disposed) return;
      const dt = lastTime ? Math.min((now - lastTime) / 1000, .04) : 1 / 60;
      lastTime = now;
      drawTrail(now);

      // A moving target stays well ahead of the explorer; when it stops,
      // the target settles nearby so Olli can approach and aim the lantern.
      const cursorSpeed = lastPointer && now - lastPointer.t < 90
        ? Math.hypot(cursor.x - (lastPointer.x || cursor.x), cursor.y - (lastPointer.y || cursor.y)) / Math.max(dt, .016)
        : 0;
      const moving = sprite.classList.contains('walking') || cursorSpeed > 35;
      let targetX;
      let targetY;
      if (moving && lastPointer) {
        const lookAhead = Math.min(110, cursorSpeed * .12);
        targetX = cursor.x - lastDirection * (88 + lookAhead);
        targetY = cursor.y + 24;
      } else {
        targetX = cursor.x - lastDirection * 62;
        targetY = cursor.y + 8;
      }
      targetX = clamp(targetX, 10, win.innerWidth - width - 10);
      targetY = clamp(targetY, 10, win.innerHeight - height - 10);

      const dx = targetX - position.x;
      const dy = targetY - position.y;
      const distance = Math.hypot(dx, dy);
      const maxSpeed = reduceMotion.matches ? 115 : (moving ? 105 : 72);
      const desiredVX = distance > 2 ? (dx / distance) * Math.min(maxSpeed, distance * 1.45) : 0;
      const desiredVY = distance > 2 ? (dy / distance) * Math.min(maxSpeed, distance * 1.45) : 0;
      const acceleration = reduceMotion.matches ? 7 : 2.6;
      velocity.x += (desiredVX - velocity.x) * Math.min(1, acceleration * dt);
      velocity.y += (desiredVY - velocity.y) * Math.min(1, acceleration * dt);
      position.x = clamp(position.x + velocity.x * dt, 4, win.innerWidth - width - 4);
      position.y = clamp(position.y + velocity.y * dt, 4, win.innerHeight - height - 4);
      walker.style.left = `${position.x}px`;
      walker.style.top = `${position.y}px`;

      const movingBody = Math.hypot(velocity.x, velocity.y) > 13;
      sprite.classList.toggle('walking', movingBody && !reduceMotion.matches);
      const facing = Math.abs(velocity.x) > 5 ? (velocity.x > 0 ? 1 : -1) : lastDirection;
      sprite.setAttribute('transform', facing > 0 ? '' : 'translate(120 0) scale(-1 1)');

      const handX = position.x + (facing > 0 ? 91 : 29);
      const handY = position.y + 46;
      const aimX = cursor.x - handX;
      const aimY = cursor.y - handY;
      // SVG lantern points right at zero degrees; flip angle for left-facing sprite.
      let angle = Math.atan2(aimY, Math.abs(aimX)) * 180 / Math.PI;
      if (aimX < 0) angle = -angle;
      lantern.setAttribute('transform', `rotate(${clamp(angle, -78, 78)} 91 78)`);

      frameId = win.requestAnimationFrame(animate);
    }

    const onResize = () => {
      resizeCanvas();
      position.x = clamp(position.x, 4, win.innerWidth - width - 4);
      position.y = clamp(position.y, 4, win.innerHeight - height - 4);
    };
    win.addEventListener('resize', onResize, { passive: true });
    doc.addEventListener('pointermove', onPointerMove, { passive: true, capture: true });
    doc.addEventListener('pointerleave', onPointerLeave, { passive: true });
    frameId = win.requestAnimationFrame(animate);

    cleanup = () => {
      disposed = true;
      win.cancelAnimationFrame(frameId);
      win.removeEventListener('resize', onResize);
      doc.removeEventListener('pointermove', onPointerMove, true);
      doc.removeEventListener('pointerleave', onPointerLeave);
      style.remove();
      wrap.remove();
      delete win.__olliEffectsCleanup;
    };
    win.__olliEffectsCleanup = cleanup;
  } catch (_) {
    // Ignore browser restrictions for embedded components.
  }
})();
</script>
"""
components.html(JS_EFEITOS_OLLI, height=0, scrolling=False)

# =====================================================================
# DADOS / FUNÇÕES
# =====================================================================
COLUNAS = [
    "ID", "Status Contato", "Provedor", "Responsáveis", "Cargo", "Localidade", "Telefone", "Email",
    "Situação de Mercado", "Produto Olli", "CNPJ", "Clientes Estimados", "Ticket Médio (R$)",
    "Data Cadastro", "Score Conectividade", "Origem Lead",
    "Site", "Stack Detectada", "Motivo do Encaixe", "Fontes",
]
COLUNAS_NUMERICAS = ("Clientes Estimados", "Ticket Médio (R$)", "Score Conectividade")

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


def normalizar_df(df: pd.DataFrame | None) -> pd.DataFrame:
    if df is None:
        return pd.DataFrame(DADOS_INICIAIS, columns=COLUNAS)
    df = df.copy()
    for coluna in COLUNAS:
        if coluna not in df.columns:
            df[coluna] = 0 if coluna in COLUNAS_NUMERICAS else "Não Informado"
        elif coluna in COLUNAS_NUMERICAS:
            df[coluna] = pd.to_numeric(df[coluna], errors="coerce").fillna(0)
        else:
            df[coluna] = df[coluna].fillna("Não Informado").astype(str)
    df["Score Conectividade"] = df["Score Conectividade"].clip(0, 100)
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
    # Grava em arquivo temporário e troca no final: uma falha no meio não corrompe o CSV.
    caminho_tmp = f"{ARQUIVO_BANCO_DADOS}.tmp"
    try:
        normalizar_df(df).to_csv(caminho_tmp, index=False, encoding="utf-8")
        os.replace(caminho_tmp, ARQUIVO_BANCO_DADOS)
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
          <div class="empty-copy">Sua busca não encontrou provedores. Experimente outro nome, localidade ou filtro.</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


# =====================================================================
# HELPERS DE UI
# =====================================================================
ORDENACOES = {
    "Maior score": ("Score Conectividade", False),
    "Mais clientes": ("Clientes Estimados", False),
    "Cadastro recente": ("Data Cadastro", False),
    "Provedor (A–Z)": ("Provedor", True),
}
STATUS_ESTILOS = {  # status -> (cor do texto, fundo)
    "Qualificado": ("#6EE7B7", "rgba(52,211,153,.14)"),
    "Agendado (Reunião)": ("#67E8F9", "rgba(34,211,238,.14)"),
    "Não Chamado": ("#D8B4FE", "rgba(124,58,237,.22)"),
}
STATUS_PADRAO = ("#CBD5E1", "rgba(148,163,184,.16)")


def formatar_numero(valor: float, casas: int = 0) -> str:
    """Formata no padrão brasileiro: 12.000 / 89,90."""
    return f"{valor:,.{casas}f}".replace(",", "_").replace(".", ",").replace("_", ".")


def formatar_moeda(valor: float) -> str:
    return f"R$ {formatar_numero(valor, 2)}"


def formatar_compacto(valor: float) -> str:
    for limite, sufixo in ((1e9, " bi"), (1e6, " mi"), (1e3, " mil")):
        if abs(valor) >= limite:
            return formatar_numero(valor / limite, 2) + sufixo
    return formatar_numero(valor)


def cor_score(score: int) -> tuple[str, str]:
    if score >= 75:
        return "#22D3EE", "#34D399"
    if score >= 50:
        return "#7C3AED", "#22D3EE"
    return "#F472B6", "#A855F7"


def limpar_html(html: str) -> str:
    """Remove quebras e indentação para o Markdown não tratar o HTML como bloco de código."""
    return "".join(linha.strip() for linha in html.splitlines())


def html_kpi(titulo: str, valor: str, cor: str = "#7C3AED") -> str:
    return limpar_html(f"""
        <div class="kpi-container" style="--accent:{cor}">
          <div class="kpi-title">{escape(titulo)}</div>
          <div class="kpi-value">{escape(valor)}</div>
        </div>
    """)


def html_ia(texto: str) -> str:
    return f'<div class="ai-response"><span class="ai-tag">✦ IA</span><br>{escape(texto)}</div>'


def html_card(lead: dict, indice: int = 0) -> str:
    def campo(chave: str) -> str:
        return escape(str(lead.get(chave, "Não informado")))

    provedor, status, local = campo("Provedor"), campo("Status Contato"), campo("Localidade")
    produto, responsavel, cargo = campo("Produto Olli"), campo("Responsáveis"), campo("Cargo")
    dor = campo("Situação de Mercado")
    score = int(lead["Score Conectividade"])
    cor_a, cor_b = cor_score(score)
    cor_status, fundo_status = STATUS_ESTILOS.get(str(lead.get("Status Contato")), STATUS_PADRAO)

    email = str(lead.get("Email", ""))
    telefone = "".join(c for c in str(lead.get("Telefone", "")) if c.isdigit() or c == "+")
    chips = [
        f'<span class="chip">👥 {formatar_numero(lead["Clientes Estimados"])} clientes</span>',
        f'<span class="chip">💳 Ticket {formatar_moeda(lead["Ticket Médio (R$)"])}</span>',
        f'<span class="chip">🛰️ {campo("Origem Lead")}</span>',
    ]
    if "@" in email:
        chips.append(f'<a class="chip" href="mailto:{escape(email)}">✉️ {escape(email)}</a>')
    if telefone:
        chips.append(f'<a class="chip" href="tel:{telefone}">📞 {campo("Telefone")}</a>')
    chips_html = "".join(chips)

    return limpar_html(f"""
        <div class="hologram-card" style="animation-delay:{min(indice, 8) * 60}ms">
          <div class="card-head">
            <span class="card-title">{provedor}</span>
            <span class="pill" style="color:{cor_status};background:{fundo_status}">{status}</span>
          </div>
          <div class="card-grid">
            <div><span class="meta-label">📍 Localidade</span><b>{local}</b></div>
            <div><span class="meta-label">🎯 Produto Olli</span><b class="accent">{produto}</b></div>
            <div><span class="meta-label">💼 Responsável</span><b>{responsavel} ({cargo})</b></div>
          </div>
          <div class="pain"><span class="meta-label">⚠️ Situação de mercado / dor</span>{dor}</div>
          <div class="chips">{chips_html}</div>
          <div class="score-label">Score de saúde da rede ({score}%)</div>
          <div class="score-track"><div class="score-fill" style="width:{score}%;--c1:{cor_a};--c2:{cor_b}"></div></div>
        </div>
    """)


def filtrar_leads(
    df: pd.DataFrame, termo: str, status: list[str], produtos: list[str], score_min: int, ordem: str
) -> pd.DataFrame:
    mascara = df["Score Conectividade"] >= score_min
    if termo:
        mascara &= (
            df["Provedor"].str.contains(termo, case=False, regex=False)
            | df["Localidade"].str.contains(termo, case=False, regex=False)
        )
    if status:
        mascara &= df["Status Contato"].isin(status)
    if produtos:
        mascara &= df["Produto Olli"].isin(produtos)
    coluna, crescente = ORDENACOES[ordem]
    return df[mascara].sort_values(
        coluna,
        ascending=crescente,
        kind="stable",
        key=lambda serie: serie if pd.api.types.is_numeric_dtype(serie) else serie.str.lower(),
    )


def limpar_busca() -> None:
    # Callback: roda antes dos widgets serem criados, então pode alterar o estado do campo.
    st.session_state.termo_busca_provedor = ""
    st.session_state["campo_busca_provedor"] = ""
    st.session_state.ids_radar = []
    st.session_state.scroll_resultados = False


def pedir_exclusao(lead_id: str | None) -> None:
    st.session_state.confirmar_exclusao = lead_id


# =====================================================================
# RADAR DE PROVEDORES (WEB)
# =====================================================================
ANTHROPIC_URL = "https://api.anthropic.com/v1/messages"
MODELO = os.getenv("OLLI_MODELO", "claude-sonnet-5-5")
CABECALHO_HTTP = {"User-Agent": "OlliHubRadar/2.0 (pesquisa comercial B2B)"}
TIMEOUT = 15
MAX_CANDIDATOS = 5

# ----- Perfil de cliente (ICP): ajuste aqui ----------------------------------
# CNAEs de telecomunicações (Receita Federal). Fora dessa lista, o encaixe é limitado.
CNAES_TELECOM = {"6110801", "6110802", "6120500", "6130200", "6141800", "6190601", "6190699"}
PRODUTOS_OLLI = {
    # TODO: descreva o benefício de cada produto. O Claude usa isso para medir o encaixe.
    "Olli Smart Home": "a preencher",
    "Olli Habita": "a preencher",
}
# Padrões no HTML do site que indicam ferramentas usadas pelo provedor.
ASSINATURAS_STACK = {
    "WordPress": [r"wp-content", r"wp-includes"],
    "WhatsApp": [r"wa\.me/", r"api\.whatsapp\.com"],
    "Google Analytics/GTM": [r"googletagmanager\.com", r"gtag\("],
    "Meta Pixel": [r"connect\.facebook\.net"],
    "RD Station": [r"rdstation"],
    "HubSpot": [r"hs-scripts\.com", r"hubspot"],
    "Zendesk": [r"zdassets", r"zendesk"],
    "Tawk.to": [r"tawk\.to"],
    "Asaas": [r"asaas\.com"],
    "Efí/Gerencianet": [r"efi\.com\.br", r"gerencianet"],
    "Mercado Pago": [r"mercadopago"],
    "IXC Soft": [r"ixcsoft"],
    "MK-Auth": [r"mk-auth"],
    "Hubsoft": [r"hubsoft"],
    "Voalle": [r"voalle"],
    "UISP": [r"uisp"],
}


def _so_digitos(texto) -> str:
    return re.sub(r"\D", "", str(texto or ""))


def _formatar_cnpj(d: str) -> str:
    return f"{d[:2]}.{d[2:5]}.{d[5:8]}/{d[8:12]}-{d[12:]}"


def _json(texto: str):
    """Extrai o primeiro array ou objeto JSON de uma resposta do modelo."""
    m = re.search(r"(\[.*\]|\{.*\})", texto or "", re.S)
    try:
        return json.loads(m.group(1)) if m else None
    except json.JSONDecodeError:
        return None


def _chamar_claude(prompt: str, usos_busca: int = 4) -> str:
    chave = os.getenv("ANTHROPIC_API_KEY")
    if not chave:
        raise RuntimeError("defina a variável de ambiente ANTHROPIC_API_KEY")
    cabecalhos = {"x-api-key": chave, "anthropic-version": "2023-06-01", "content-type": "application/json"}
    ferramenta = {
        "type": "web_search_20250305",
        "name": "web_search",
        "max_uses": usos_busca,
        "user_location": {"type": "approximate", "country": "BR"},
    }
    mensagens = [{"role": "user", "content": prompt}]
    for _ in range(3):  # stop_reason "pause_turn": reenvia a mesma conversa para continuar a busca
        r = requests.post(
            ANTHROPIC_URL,
            headers=cabecalhos,
            timeout=180,
            json={"model": MODELO, "max_tokens": 4096, "tools": [ferramenta], "messages": mensagens},
        )
        r.raise_for_status()
        corpo = r.json()
        if corpo.get("stop_reason") != "pause_turn":
            return "\n".join(b.get("text", "") for b in corpo.get("content", []) if b.get("type") == "text")
        mensagens = [{"role": "user", "content": prompt}, {"role": "assistant", "content": corpo["content"]}]
    return ""


def consultar_cnpj(cnpj) -> dict:
    digitos = _so_digitos(cnpj)
    if len(digitos) != 14:
        return {}
    try:
        r = requests.get(f"https://brasilapi.com.br/api/cnpj/v1/{digitos}", headers=CABECALHO_HTTP, timeout=TIMEOUT)
        return r.json() if r.status_code == 200 else {}
    except (requests.RequestException, ValueError):
        return {}


def consultar_peeringdb(nome: str) -> dict:
    try:
        r = requests.get(
            "https://www.peeringdb.com/api/net",
            params={"name__contains": nome},
            headers=CABECALHO_HTTP,
            timeout=TIMEOUT,
        )
        redes = r.json().get("data", []) if r.status_code == 200 else []
    except (requests.RequestException, ValueError):
        return {}
    if not redes:
        return {}
    rede = redes[0]
    try:
        ix = requests.get(
            "https://www.peeringdb.com/api/netixlan",
            params={"net_id": rede["id"]},
            headers=CABECALHO_HTTP,
            timeout=TIMEOUT,
        )
        pontos_ix = len(ix.json().get("data", []))
    except (requests.RequestException, ValueError, KeyError):
        pontos_ix = None
    return {
        "asn": rede.get("asn"),
        "tipo": rede.get("info_type"),
        "trafego": rede.get("info_traffic"),
        "pontos_ix": pontos_ix,
    }


def ler_site(site) -> tuple[list[str], str]:
    """Lê só a página inicial, uma vez por provedor. Devolve (stack detectada, texto)."""
    if not site or str(site).lower() in ("null", "não informado"):
        return [], ""
    url = site if str(site).startswith("http") else f"https://{site}"
    try:
        r = requests.get(url, headers=CABECALHO_HTTP, timeout=TIMEOUT)
    except requests.RequestException:
        return [], ""
    html = r.text or ""
    baixo = html.lower()
    stack = [nome for nome, padroes in ASSINATURAS_STACK.items() if any(re.search(p, baixo) for p in padroes)]
    if "cf-ray" in r.headers:
        stack.append("Cloudflare")
    sem_tags = re.sub(r"<script.*?</script>|<style.*?</style>|<[^>]+>", " ", html, flags=re.S | re.I)
    return stack, re.sub(r"\s+", " ", unescape(sem_tags)).strip()


def descobrir_provedores(termo: str) -> list[dict]:
    prompt = f"""Encontre provedores de internet (ISPs) brasileiros relacionados a: "{termo}".
Pesquise na web: sites oficiais, Anatel, notícias, Google Maps e redes sociais.
Responda APENAS com um array JSON de até {MAX_CANDIDATOS} itens, no formato:
[{{"nome": "...", "site": "dominio.com.br ou null", "cnpj": "14 dígitos ou null", "cidade": "...", "uf": "XX"}}]
Não invente CNPJ, site ou cidade: use null quando não confirmar."""
    dados = _json(_chamar_claude(prompt, usos_busca=5))
    return dados[:MAX_CANDIDATOS] if isinstance(dados, list) else []


def analisar_provedor(candidato: dict, cnpj: dict, pdb: dict, stack: list[str], texto_site: str) -> dict:
    produtos = "\n".join(f"- {nome}: {desc}" for nome, desc in PRODUTOS_OLLI.items())
    campos_receita = ("razao_social", "nome_fantasia", "descricao_situacao_cadastral", "cnae_fiscal_descricao",
                      "capital_social", "porte", "municipio", "uf")
    receita = {k: cnpj.get(k) for k in campos_receita}
    prompt = f"""Você analisa provedores de internet (ISPs) para o time de SDR do Olli.
Produtos Olli:
{produtos}

Dados coletados de fontes públicas:
- Candidato: {json.dumps(candidato, ensure_ascii=False)}
- Receita Federal (BrasilAPI): {json.dumps(receita, ensure_ascii=False)}
- PeeringDB: {json.dumps(pdb, ensure_ascii=False)}
- Stack detectada no site: {", ".join(stack) or "nada identificado"}
- Trecho da página inicial: {texto_site[:2000]}

Pesquise na web reclamações, notícias, relatórios e vagas recentes para descobrir POR QUE esse
provedor precisaria de algum produto Olli (churn, guerra de preço, falta de serviços de valor
agregado, retrabalho no suporte etc.).
Responda APENAS com JSON:
{{"dores": [{{"dor": "...", "evidencia": "...", "fonte": "url"}}], "produto_recomendado": "nome ou null", "encaixe": 0-100, "motivo": "1 a 2 frases", "confianca": "alta|media|baixa"}}
Regras: use só o que encontrou e cite a fonte. Sem evidência, dores = [] e encaixe baixo."""
    dados = _json(_chamar_claude(prompt, usos_busca=4))
    return dados if isinstance(dados, dict) else {}


def _pontuar(analise: dict, cnpj: dict) -> int:
    try:
        encaixe = int(float(analise.get("encaixe") or 0))
    except (TypeError, ValueError):
        encaixe = 0
    if cnpj and str(cnpj.get("cnae_fiscal")) not in CNAES_TELECOM:
        encaixe = min(encaixe, 40)
    situacao = cnpj.get("descricao_situacao_cadastral") or cnpj.get("situacao_cadastral")
    if isinstance(situacao, str) and situacao and "ATIV" not in situacao.upper():
        encaixe = min(encaixe, 20)
    return max(0, min(100, encaixe))


def _montar_lead(candidato: dict, cnpj: dict, pdb: dict, stack: list[str], analise: dict) -> dict:
    nome = candidato.get("nome") or cnpj.get("razao_social") or "Provedor sem nome"
    dores = analise.get("dores") or []
    dor_resumo = "; ".join(d.get("dor", "") for d in dores if d.get("dor")) or "Nenhuma dor confirmada nas fontes"
    fontes = " | ".join(sorted({d.get("fonte", "") for d in dores if d.get("fonte")}))
    digitos = _so_digitos(candidato.get("cnpj") or cnpj.get("cnpj"))
    chave = digitos or hashlib.sha1(nome.lower().encode()).hexdigest()[:8].upper()
    cidade = candidato.get("cidade") or cnpj.get("municipio") or ""
    uf = candidato.get("uf") or cnpj.get("uf") or ""
    return {
        "ID": f"WEB-{chave}",
        "Status Contato": "Novo (Radar Web)",
        "Provedor": nome,
        "Responsáveis": "Não Informado",
        "Cargo": "Não Informado",
        "Localidade": f"{cidade} - {uf}".strip(" -") or "Não Informada",
        "Telefone": cnpj.get("ddd_telefone_1") or "Não Informado",
        "Email": cnpj.get("email") or "Não Informado",
        "Situação de Mercado": dor_resumo,
        "Produto Olli": analise.get("produto_recomendado") or "Não definido",
        "CNPJ": _formatar_cnpj(digitos) if len(digitos) == 14 else "Não Informado",
        "Clientes Estimados": 0,
        "Ticket Médio (R$)": 0,
        "Data Cadastro": datetime.now().strftime("%Y-%m-%d"),
        "Score Conectividade": _pontuar(analise, cnpj),
        "Origem Lead": "Radar Web",
        "Site": candidato.get("site") or "Não Informado",
        "Stack Detectada": ", ".join(stack) or "Não identificada",
        "Motivo do Encaixe": analise.get("motivo") or "Não avaliado",
        "Fontes": fontes or "Não encontradas",
    }


def _processar(candidato: dict) -> dict:
    cnpj = consultar_cnpj(candidato.get("cnpj"))
    nome_busca = candidato.get("nome") or cnpj.get("razao_social") or ""
    pdb = consultar_peeringdb(nome_busca) if nome_busca else {}
    stack, texto_site = ler_site(candidato.get("site"))
    analise = analisar_provedor(candidato, cnpj, pdb, stack, texto_site)
    return _montar_lead(candidato, cnpj, pdb, stack, analise)


def _seguro(candidato: dict):
    try:
        return _processar(candidato)
    except Exception:  # um provedor com falha não derruba a busca inteira
        return None


@st.cache_data(ttl=3600, show_spinner=False)
def buscar_provedores_web(termo: str) -> list[dict]:
    """Cache de 1 hora por termo: cada busca gasta chamadas da API Claude."""
    candidatos = descobrir_provedores(termo)
    with ThreadPoolExecutor(max_workers=4) as pool:
        leads = list(pool.map(_seguro, candidatos))
    return [lead for lead in leads if lead]


# =====================================================================
# DASHBOARD
# =====================================================================
st.session_state.setdefault("termo_busca_provedor", "")
st.session_state.setdefault("confirmar_exclusao", None)
st.session_state.setdefault("scroll_resultados", False)
st.session_state.setdefault("abordagens", {})

try:
    df = normalizar_df(carregar_dados().copy())
except Exception:
    df = normalizar_df(pd.DataFrame(DADOS_INICIAIS, columns=COLUNAS))

st.markdown('<div class="cyber-title">⚡ Olli Hub Enterprise v2.0</div>', unsafe_allow_html=True)
st.markdown(
    '<div class="subtitle">SDR Intelligence Matrix &amp; Real-time Network Mapping<span class="live">Sistema online</span></div>',
    unsafe_allow_html=True,
)

media = int(df["Score Conectividade"].mean()) if not df.empty else 0
mrr = float((df["Clientes Estimados"] * df["Ticket Médio (R$)"]).sum())
kpis = [
    ("Total Provedores", formatar_numero(len(df)), "#7C3AED"),
    ("Clientes Estimados", formatar_numero(df["Clientes Estimados"].sum()), "#A855F7"),
    ("Score Médio", f"{media}%", "#22D3EE"),
    ("MRR Estimado", f"R$ {formatar_compacto(mrr)}", "#34D399"),
]
for coluna_kpi, (titulo_kpi, valor_kpi, cor_kpi) in zip(st.columns(len(kpis)), kpis):
    coluna_kpi.markdown(html_kpi(titulo_kpi, valor_kpi, cor_kpi), unsafe_allow_html=True)

with st.sidebar:
    st.markdown('<div class="sidebar-brand">🔮 OLLI <span>HUB</span></div>', unsafe_allow_html=True)
    st.caption("Filtros de inteligência")
    filtro_status = st.multiselect("Status do contato", sorted(df["Status Contato"].unique()))
    filtro_produto = st.multiselect("Produto Olli", sorted(df["Produto Olli"].unique()))
    score_minimo = st.selectbox(
        "Score mínimo", [0, 50, 75, 90], format_func=lambda v: "Todos" if v == 0 else f"{v}% ou mais"
    )
    ordem = st.selectbox("Ordenar por", list(ORDENACOES))

st.write("---")
st.markdown("### 🔎 Busca de provedores")
with st.form("form_busca_provedor", clear_on_submit=False):
    campo_busca, botao_busca = st.columns([5, 1])
    with campo_busca:
        termo_digitado = st.text_input(
            "Busca", placeholder="Nome do provedor ou cidade...", label_visibility="collapsed", key="campo_busca_provedor"
        )
    with botao_busca:
        buscar = st.form_submit_button("🔍 Procurar")

if buscar:
    st.session_state.termo_busca_provedor = termo_digitado.strip()
    st.session_state.scroll_resultados = True
    st.session_state.ids_radar = []
    if st.session_state.termo_busca_provedor:
        with st.spinner("Varrendo a web: fontes, CNPJ, PeeringDB e stack..."):
            try:
                novos = pd.DataFrame(buscar_provedores_web(st.session_state.termo_busca_provedor), columns=COLUNAS)
            except Exception as erro:
                novos = pd.DataFrame(columns=COLUNAS)
                st.error(f"Radar indisponível: {erro}")
        if not novos.empty:
            df = normalizar_df(pd.concat([df, novos], ignore_index=True).drop_duplicates("ID", keep="last"))
            salvar_dados(df)
            st.session_state.ids_radar = novos["ID"].tolist()
            st.toast(f"{len(novos)} provedor(es) encontrado(s) na web", icon="🛰️")

barra_busca, barra_limpar = st.columns([5, 1])
with barra_busca:
    if st.session_state.termo_busca_provedor:
        st.caption(f"Busca ativa: {st.session_state.termo_busca_provedor}")
with barra_limpar:
    st.button("Limpar", key="limpar_busca", on_click=limpar_busca)

termo = st.session_state.termo_busca_provedor.strip()
resultados = filtrar_leads(df, termo, filtro_status, filtro_produto, score_minimo, ordem)
ids_radar = st.session_state.get("ids_radar", [])
if ids_radar and termo:
    resultados = pd.concat([df[df["ID"].isin(ids_radar)], resultados]).drop_duplicates("ID")

with st.sidebar:
    st.download_button(
        "⬇️ Exportar CSV",
        data=resultados.to_csv(index=False).encode("utf-8-sig"),
        file_name=f"leads_olli_{datetime.now():%Y%m%d_%H%M}.csv",
        mime="text/csv",
        disabled=resultados.empty,
        on_click=registrar_log,
        args=("Exportação de leads em CSV", "USUARIO"),
    )

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
st.caption(f"Exibindo {len(resultados)} de {len(df)} provedores")
if resultados.empty:
    mostrar_estado_vazio()
else:
    for indice, lead in enumerate(resultados.to_dict("records")):
        lead_id = str(lead["ID"])
        chave = f"{lead_id}_{indice}"
        provedor = lead["Provedor"]

        card_col, action_col = st.columns([4, 1])
        with card_col:
            st.markdown(html_card(lead, indice), unsafe_allow_html=True)
            slot_ia = st.empty()

        with action_col:
            st.write("")
            if st.button("✨ Gerar abordagem", key=f"ia_{chave}"):
                st.session_state.abordagens[lead_id] = gerar_abordagem_ia(
                    provedor, lead["Responsáveis"], lead["Situação de Mercado"], lead["Produto Olli"]
                )
                registrar_log(f"Abordagem gerada para {provedor}", "AI_ENGINE")
                st.toast("Abordagem gerada", icon="✨")

            st.button("🗑️ Excluir lead", key=f"excluir_{chave}", on_click=pedir_exclusao, args=(lead_id,))

            if st.session_state.confirmar_exclusao == lead_id:
                st.warning(f"Excluir {provedor} permanentemente?")
                confirmar_col, cancelar_col = st.columns(2)
                with confirmar_col:
                    if st.button("Confirmar", key=f"confirmar_{chave}"):
                        novos = df[df["ID"].astype(str) != lead_id].copy()
                        if salvar_dados(novos):
                            registrar_log(f"Lead {provedor} ({lead_id}) excluído", "USUARIO")
                            st.session_state.abordagens.pop(lead_id, None)
                            st.session_state.confirmar_exclusao = None
                            st.toast("Lead excluído", icon="🗑️")
                            st.rerun()
                with cancelar_col:
                    st.button("Cancelar", key=f"cancelar_{chave}", on_click=pedir_exclusao, args=(None,))

        abordagem = st.session_state.abordagens.get(lead_id)
        if abordagem:
            slot_ia.markdown(html_ia(abordagem), unsafe_allow_html=True)

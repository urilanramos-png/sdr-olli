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
        const win = window.parent;
        if (doc.getElementById('olli-effects')) return;

        const style = doc.createElement('style');
        style.textContent = `
          #olli-effects, #olli-beam-overlay, #olli-trail-canvas {
            position: fixed; inset: 0; pointer-events: none;
          }
          #olli-beam-overlay { z-index: 2147483642; overflow: visible; }
          #olli-trail-canvas { z-index: 2147483643; width: 100%; height: 100%; }
          #olli-effects { z-index: 2147483644; overflow: visible; }
          #olli-pointer-light {
            position: fixed; z-index: 2147483645; width: 190px; height: 190px;
            left: 0; top: 0; opacity: 0; transform: translate(-50%, -50%);
            border-radius: 50%; pointer-events: none; mix-blend-mode: screen;
            background: radial-gradient(circle, rgba(255,255,255,.24) 0%, rgba(216,180,254,.3) 12%, rgba(168,85,247,.24) 30%, rgba(124,58,237,.12) 52%, transparent 72%);
            filter: blur(5px); will-change: left, top, opacity;
          }
          #olli-walker {
            position: fixed; left: 50%; bottom: 13px; width: 176px; height: 220px;
            pointer-events: none; opacity: .98; transform: translateX(-50%);
            transform-style: preserve-3d; perspective: 700px; filter: drop-shadow(0 13px 15px rgba(5,2,20,.62));
            will-change: transform;
          }
          #olli-walker svg { width: 100%; height: 100%; overflow: visible; }
          #olli-walker .body-shell { transform-origin: 90px 138px; }
          #olli-walker .leg-left, #olli-walker .leg-right { transform-box: view-box; transform-origin: 78px 168px; }
          #olli-walker .leg-right { transform-origin: 103px 168px; }
          #olli-walker .arm-pivot { transform-box: view-box; }
          #olli-walker .face { transform-box: view-box; transform-origin: 91px 64px; }
          @media (prefers-reduced-motion: reduce) {
            #olli-walker { filter: drop-shadow(0 8px 10px rgba(5,2,20,.5)); }
          }
          @media (max-width: 640px) { #olli-walker { width: 132px; height: 170px; bottom: 8px; } }
        `;
        doc.head.appendChild(style);

        const beam = doc.createElementNS('http://www.w3.org/2000/svg', 'svg');
        beam.id = 'olli-beam-overlay';
        beam.setAttribute('aria-hidden', 'true');
        beam.innerHTML = `
          <defs>
            <linearGradient id="olliBeamGradient" gradientUnits="userSpaceOnUse">
              <stop offset="0" stop-color="#FDE68A" stop-opacity=".30"/>
              <stop offset=".35" stop-color="#C084FC" stop-opacity=".14"/>
              <stop offset="1" stop-color="#A855F7" stop-opacity=".015"/>
            </linearGradient>
            <radialGradient id="olliBeamTarget">
              <stop stop-color="#FFF7CC" stop-opacity=".5"/>
              <stop offset=".22" stop-color="#D8B4FE" stop-opacity=".24"/>
              <stop offset="1" stop-color="#A855F7" stop-opacity="0"/>
            </radialGradient>
            <filter id="olliBeamBlur"><feGaussianBlur stdDeviation="8"/></filter>
          </defs>
          <path id="olli-beam-haze" fill="#A855F7" opacity=".1" filter="url(#olliBeamBlur)"/>
          <path id="olli-beam" fill="url(#olliBeamGradient)" opacity="0"/>
          <circle id="olli-beam-target" r="70" fill="url(#olliBeamTarget)" opacity="0"/>
        `;
        doc.body.appendChild(beam);

        const canvas = doc.createElement('canvas');
        canvas.id = 'olli-trail-canvas';
        canvas.setAttribute('aria-hidden', 'true');
        doc.body.appendChild(canvas);

        const wrap = doc.createElement('div');
        wrap.id = 'olli-effects';
        wrap.innerHTML = `
          <div id="olli-pointer-light"></div>
          <div id="olli-walker" aria-hidden="true">
            <svg viewBox="0 0 180 220" xmlns="http://www.w3.org/2000/svg">
              <defs>
                <linearGradient id="olliSkin" x1="0" y1="0" x2="1" y2="1">
                  <stop stop-color="#FFE0BD"/><stop offset=".48" stop-color="#D9A47E"/><stop offset="1" stop-color="#8F5A4B"/>
                </linearGradient>
                <linearGradient id="olliCoat" x1="0" y1="0" x2="1" y2="0">
                  <stop stop-color="#211344"/><stop offset=".3" stop-color="#7250B8"/><stop offset=".56" stop-color="#39256D"/><stop offset="1" stop-color="#160F32"/>
                </linearGradient>
                <linearGradient id="olliCoatLight" x1="0" y1="0" x2="1" y2="1">
                  <stop stop-color="#E9D5FF" stop-opacity=".75"/><stop offset="1" stop-color="#A78BFA" stop-opacity="0"/>
                </linearGradient>
                <linearGradient id="olliBoot" x1="0" y1="0" x2="0" y2="1">
                  <stop stop-color="#A78BFA"/><stop offset="1" stop-color="#25164D"/>
                </linearGradient>
                <radialGradient id="olliLanternGlow">
                  <stop stop-color="#FFF7CC" stop-opacity=".95"/><stop offset=".3" stop-color="#FDE68A" stop-opacity=".6"/><stop offset="1" stop-color="#A855F7" stop-opacity="0"/>
                </radialGradient>
                <filter id="olliSoftShadow" x="-50%" y="-50%" width="200%" height="200%">
                  <feGaussianBlur stdDeviation="4"/>
                </filter>
              </defs>
              <ellipse cx="91" cy="207" rx="48" ry="8" fill="#6D28D9" opacity=".34" filter="url(#olliSoftShadow)"/>
              <g id="olli-character">
                <g id="olli-legs">
                  <g class="leg-left">
                    <path d="M76 157 Q72 176 73 193 L87 194 L94 166Z" fill="url(#olliCoat)" stroke="#BCA4F8" stroke-opacity=".35" stroke-width="2"/>
                    <path d="M73 190 Q82 194 94 190 L96 199 Q88 204 70 200Z" fill="url(#olliBoot)"/>
                  </g>
                  <g class="leg-right">
                    <path d="M98 158 L111 160 Q114 178 107 194 L94 194 L91 168Z" fill="url(#olliCoat)" stroke="#BCA4F8" stroke-opacity=".3" stroke-width="2"/>
                    <path d="M94 190 Q103 194 109 190 L115 198 Q108 205 91 200Z" fill="url(#olliBoot)"/>
                  </g>
                </g>
                <g class="body-shell">
                  <path d="M74 88 Q90 79 107 89 Q119 103 116 158 Q96 171 68 158 Q67 117 74 88Z" fill="url(#olliCoat)" stroke="#C4B5FD" stroke-opacity=".44" stroke-width="2"/>
                  <path d="M82 89 L92 105 L103 88 L108 155 L80 155Z" fill="url(#olliCoatLight)" opacity=".7"/>
                  <path d="M91 104 L92 153" stroke="#E9D5FF" stroke-opacity=".35" stroke-width="2"/>
                  <circle cx="98" cy="117" r="2" fill="#FDE68A"/><circle cx="98" cy="129" r="2" fill="#FDE68A"/>
                  <path d="M75 100 Q66 111 68 131 L78 137 L85 112Z" fill="url(#olliCoat)" stroke="#C4B5FD" stroke-opacity=".4" stroke-width="2"/>
                  <path d="M110 101 Q119 114 116 133 L107 137 L101 113Z" fill="#251744" stroke="#C4B5FD" stroke-opacity=".35" stroke-width="2"/>
                  <path d="M89 87 L96 99 L103 87" fill="none" stroke="#F5EFFF" stroke-opacity=".8" stroke-width="3"/>
                </g>
                <g class="face">
                  <path d="M77 46 Q78 27 94 27 Q110 29 109 49 L106 69 Q101 81 91 81 Q79 77 77 63Z" fill="url(#olliSkin)" stroke="#FFE6CF" stroke-opacity=".55" stroke-width="1.5"/>
                  <path d="M76 49 Q72 34 82 24 Q91 15 105 24 Q114 30 110 46 L104 39 Q92 42 82 36 L80 51Z" fill="#19132C"/>
                  <path d="M81 53 Q85 50 89 53 M98 52 Q102 49 106 52" fill="none" stroke="#38213F" stroke-width="2" stroke-linecap="round"/>
                  <ellipse cx="86" cy="57" rx="1.8" ry="2.3" fill="#1F1630"/><ellipse cx="102" cy="56" rx="1.8" ry="2.3" fill="#1F1630"/>
                  <path d="M91 57 L89 65 L94 66" fill="none" stroke="#9B6558" stroke-width="1.5" stroke-linecap="round"/>
                  <path d="M89 71 Q95 74 100 70" fill="none" stroke="#8A4F50" stroke-width="1.5" stroke-linecap="round"/>
                  <path d="M78 46 Q83 42 88 42" fill="none" stroke="#F7D5B6" stroke-opacity=".65" stroke-width="2"/>
                </g>
                <g id="olli-arm" class="arm-pivot">
                  <path d="M106 111 Q120 110 135 126 L151 137 L144 147 Q128 141 113 134 L102 126Z" fill="url(#olliCoat)" stroke="#C4B5FD" stroke-opacity=".52" stroke-width="2"/>
                  <path d="M140 137 Q148 132 154 139 L158 146 Q152 153 145 148Z" fill="url(#olliSkin)"/>
                  <g id="olli-lantern">
                    <path d="M151 137 L165 132 L173 145 L158 151Z" fill="#5B3B76" stroke="#E9D5FF" stroke-width="2"/>
                    <path d="M163 134 L174 131 L178 138 L168 142Z" fill="#FDE68A" stroke="#FFF7CC" stroke-width="1.5"/>
                    <circle cx="175" cy="137" r="17" fill="url(#olliLanternGlow)"/>
                    <path d="M154 137 L164 134" stroke="#FFF7CC" stroke-width="2" opacity=".8"/>
                  </g>
                </g>
                <path d="M75 119 Q67 127 72 139" fill="none" stroke="#C4B5FD" stroke-opacity=".5" stroke-width="2"/>
              </g>
            </svg>
          </div>
        `;
        doc.body.appendChild(wrap);

        const light = doc.getElementById('olli-pointer-light');
        const walker = doc.getElementById('olli-walker');
        const character = doc.getElementById('olli-character');
        const arm = doc.getElementById('olli-arm');
        const face = doc.querySelector('#olli-walker .face');
        const legs = doc.getElementById('olli-legs');
        const beamPath = doc.getElementById('olli-beam');
        const hazePath = doc.getElementById('olli-beam-haze');
        const beamTarget = doc.getElementById('olli-beam-target');
        const canvasContext = canvas.getContext('2d');
        const reducedMotion = win.matchMedia('(prefers-reduced-motion: reduce)').matches;
        const dpr = Math.min(win.devicePixelRatio || 1, 2);
        let width = win.innerWidth;
        let height = win.innerHeight;
        canvas.width = width * dpr;
        canvas.height = height * dpr;
        canvasContext.scale(dpr, dpr);

        let pointerX = width * .5;
        let pointerY = height * .45;
        let smoothX = pointerX;
        let smoothY = pointerY;
        let lastX = pointerX;
        let lastY = pointerY;
        let velocityX = 0;
        let velocityY = 0;
        let armAngle = 0;
        let armVelocity = 0;
        let headAngle = 0;
        let headVelocity = 0;
        let lastTime = 0;
        let lastParticle = 0;
        let isActive = false;
        const particles = [];

        const resize = () => {
          width = win.innerWidth;
          height = win.innerHeight;
          canvas.width = width * dpr;
          canvas.height = height * dpr;
          canvasContext.setTransform(dpr, 0, 0, dpr, 0, 0);
        };
        win.addEventListener('resize', resize, { passive: true });

        doc.addEventListener('pointermove', (event) => {
          if (event.pointerType === 'touch') return;
          pointerX = event.clientX;
          pointerY = event.clientY;
          isActive = true;
          light.style.opacity = '1';
          if (!reducedMotion && performance.now() - lastParticle > 20) {
            const dx = pointerX - lastX;
            const dy = pointerY - lastY;
            if (dx * dx + dy * dy > 20) {
              particles.push({ x: pointerX, y: pointerY, life: 1, radius: 5 + Math.random() * 8 });
              if (particles.length > 38) particles.shift();
              lastParticle = performance.now();
            }
          }
          lastX = pointerX;
          lastY = pointerY;
        }, { passive: true });
        doc.addEventListener('pointerleave', () => {
          isActive = false;
          light.style.opacity = '0';
          beamPath.style.opacity = '0';
          hazePath.style.opacity = '0';
          beamTarget.style.opacity = '0';
        }, { passive: true });

        const shortestAngle = (from, to) => ((to - from + 540) % 360) - 180;
        const frame = (time) => {
          const dt = Math.min((time - (lastTime || time)) / 1000, .032);
          lastTime = time;
          const walkerRect = walker.getBoundingClientRect();
          const shoulderX = walkerRect.left + walkerRect.width * (108 / 180);
          const shoulderY = walkerRect.top + walkerRect.height * (122 / 220);
          const targetAngle = Math.atan2(pointerY - shoulderY, pointerX - shoulderX) * 180 / Math.PI;
          const angleDelta = shortestAngle(armAngle, targetAngle);
          if (!reducedMotion) {
            armVelocity += (angleDelta * 34 - armVelocity * 10) * dt;
            armAngle += armVelocity * dt;
            const desiredHead = Math.max(-22, Math.min(22, (pointerX - (walkerRect.left + walkerRect.width / 2)) / walkerRect.width * 22));
            headVelocity += ((desiredHead - headAngle) * 30 - headVelocity * 9) * dt;
            headAngle += headVelocity * dt;
            velocityX += ((pointerX - smoothX) * 18 - velocityX * 8) * dt;
            velocityY += ((pointerY - smoothY) * 18 - velocityY * 8) * dt;
            smoothX += velocityX * dt;
            smoothY += velocityY * dt;
            light.style.left = `${smoothX}px`;
            light.style.top = `${smoothY}px`;
            character.style.transform = `translate3d(${Math.max(-7, Math.min(7, velocityX * .09))}px, ${Math.sin(time / 180) * .8}px, 0) rotateY(${Math.max(-7, Math.min(7, velocityX * .12))}deg)`;
            legs.style.transform = `translateY(${Math.sin(time / 210) * .7}px)`;
          } else {
            armAngle = targetAngle;
            smoothX = pointerX;
            smoothY = pointerY;
            light.style.left = `${pointerX}px`;
            light.style.top = `${pointerY}px`;
          }
          arm.setAttribute('transform', `rotate(${armAngle} 108 122)`);
          face.setAttribute('transform', `rotate(${headAngle} 91 64)`);

          const lampX = shoulderX + Math.cos(armAngle * Math.PI / 180) * walkerRect.width * .39;
          const lampY = shoulderY + Math.sin(armAngle * Math.PI / 180) * walkerRect.height * .25;
          const dx = pointerX - lampX;
          const dy = pointerY - lampY;
          const distance = Math.max(1, Math.hypot(dx, dy));
          const nx = -dy / distance;
          const ny = dx / distance;
          const spread = Math.min(86, Math.max(18, distance * .12));
          const endX = lampX + dx * Math.min(distance, 1150) / distance;
          const endY = lampY + dy * Math.min(distance, 1150) / distance;
          const tipX = endX + nx * spread;
          const tipY = endY + ny * spread;
          const otherX = endX - nx * spread;
          const otherY = endY - ny * spread;
          const path = `M ${lampX} ${lampY} Q ${(lampX + tipX) / 2} ${(lampY + tipY) / 2} ${tipX} ${tipY} Q ${endX} ${endY} ${otherX} ${otherY} Q ${(lampX + otherX) / 2} ${(lampY + otherY) / 2} ${lampX} ${lampY} Z`;
          beamPath.setAttribute('d', path);
          hazePath.setAttribute('d', path);
          const gradient = doc.getElementById('olliBeamGradient');
          gradient.setAttribute('x1', lampX);
          gradient.setAttribute('y1', lampY);
          gradient.setAttribute('x2', endX);
          gradient.setAttribute('y2', endY);
          beamPath.style.opacity = isActive ? '.95' : '.25';
          hazePath.style.opacity = isActive ? '.65' : '.16';
          beamTarget.setAttribute('cx', pointerX);
          beamTarget.setAttribute('cy', pointerY);
          beamTarget.style.opacity = isActive ? '.9' : '.2';

          canvasContext.clearRect(0, 0, width, height);
          if (!reducedMotion) {
            for (let i = particles.length - 1; i >= 0; i--) {
              const particle = particles[i];
              particle.life -= dt * 1.05;
              particle.radius *= .994;
              if (particle.life <= 0) {
                particles.splice(i, 1);
                continue;
              }
              const glow = canvasContext.createRadialGradient(particle.x, particle.y, 0, particle.x, particle.y, particle.radius * 2.5);
              glow.addColorStop(0, `rgba(216,180,254,${particle.life * .48})`);
              glow.addColorStop(.35, `rgba(168,85,247,${particle.life * .24})`);
              glow.addColorStop(1, 'rgba(124,58,237,0)');
              canvasContext.fillStyle = glow;
              canvasContext.beginPath();
              canvasContext.arc(particle.x, particle.y, particle.radius * 2.5, 0, Math.PI * 2);
              canvasContext.fill();
            }
          }
          win.requestAnimationFrame(frame);
        };
        win.requestAnimationFrame(frame);
      } catch (_) { /* ignore rendering issues in restricted browser contexts */ }
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

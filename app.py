"""
Polisomnografía Pediátrica — Calculadora Clínica con Impresión Integrada
Salud Es Vivir IPS | Laboratorio de Función Pulmonar
Jefferson — Neumólogo Pediatra
Criterios: AASM Pediatric Scoring Manual 2020 | ICSD-3
"""

import streamlit as st
from datetime import date, datetime
import math

# ─────────────────────────────────────────────
# Configuración de página
# ─────────────────────────────────────────────
st.set_page_config(
    page_title="PSG Pediátrica",
    page_icon="🫁",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─────────────────────────────────────────────
# CSS global — estética clínica
# ─────────────────────────────────────────────
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700&display=swap');

    html, body, [class*="css"] { font-family: 'Inter', sans-serif; }

    .main-header {
        background: linear-gradient(135deg, #1a3a5c 0%, #2563a0 100%);
        padding: 22px 28px; border-radius: 12px; margin-bottom: 24px; color: white;
    }
    .main-header h1 { margin:0; font-size:1.8rem; font-weight:700; }
    .main-header p  { margin:4px 0 0; font-size:0.85rem; opacity:.8; }

    .section-card {
        background:#f8fafc; border:1px solid #e2e8f0;
        border-radius:10px; padding:18px 20px; margin-bottom:16px;
    }
    .section-card h3 { color:#1e3a5c; font-size:1rem; font-weight:700;
        border-bottom:2px solid #2563a0; padding-bottom:6px; margin-bottom:14px; }

    .metric-badge {
        display:inline-block; padding:3px 10px; border-radius:20px;
        font-size:0.78rem; font-weight:600; margin:2px;
    }
    .badge-normal  { background:#d1fae5; color:#065f46; }
    .badge-mild    { background:#fef3c7; color:#92400e; }
    .badge-mod     { background:#fed7aa; color:#9a3412; }
    .badge-severe  { background:#fee2e2; color:#991b1b; }

    .report-box {
        background:#fff; border:1px solid #cbd5e1; border-radius:10px;
        padding:28px 32px; font-family:'Inter',sans-serif; font-size:0.88rem;
        line-height:1.7; color:#1e293b;
    }
    .report-header {
        border-bottom:3px solid #1e3a5c; padding-bottom:12px; margin-bottom:20px;
    }
    .report-section-title {
        font-size:0.82rem; font-weight:700; color:#1e3a5c;
        text-transform:uppercase; letter-spacing:.05em;
        margin:18px 0 6px; border-bottom:1px solid #e2e8f0; padding-bottom:4px;
    }
    .report-conclusion {
        background:#f0f4ff; border-left:4px solid #2563a0;
        padding:12px 16px; border-radius:0 8px 8px 0; margin-top:12px;
    }
    .print-btn {
        background:#2563a0; color:white; border:none;
        padding:10px 24px; border-radius:8px; cursor:pointer; font-size:0.9rem;
        font-weight:600; width:100%; margin-top:10px;
    }
    @media print {
        .stSidebar, .stButton, [data-testid="stHeader"], .stTabs { display:none !important; }
        .report-box { border:none; box-shadow:none; }
    }
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
# Encabezado
# ─────────────────────────────────────────────
st.markdown("""
<div class="main-header">
  <h1>🫁 Polisomnografía Pediátrica</h1>
  <p>Calculadora Clínica con Impresión Integrada · Salud Es Vivir IPS · AASM Pediatric Scoring Manual 2020 · ICSD-3</p>
</div>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
# Tabs de entrada
# ─────────────────────────────────────────────
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "👤 Paciente y Estudio",
    "💤 Arquitectura del Sueño",
    "🌬️ Parámetros Respiratorios",
    "❤️ Cardíaco & Movimientos",
    "📄 Impresión Clínica"
])

# ──────────────────────────────────
# TAB 1 — Identificación
# ──────────────────────────────────
with tab1:
    col1, col2 = st.columns(2)
    with col1:
        st.markdown('<div class="section-card"><h3>🧒 Datos del Paciente</h3>', unsafe_allow_html=True)
        paciente_nombre = st.text_input("Nombre completo")
        paciente_id     = st.text_input("N° Historia Clínica / ID")
        fecha_nac       = st.date_input("Fecha de nacimiento",
                                        value=date(2015, 1, 1),
                                        min_value=date(1990, 1, 1))
        sexo            = st.selectbox("Sexo biológico", ["Masculino", "Femenino"])
        peso_kg         = st.number_input("Peso (kg)", 0.0, 150.0, 20.0, 0.1)
        talla_cm        = st.number_input("Talla (cm)", 40.0, 200.0, 110.0, 0.5)
        st.markdown('</div>', unsafe_allow_html=True)

    with col2:
        st.markdown('<div class="section-card"><h3>📋 Datos del Estudio</h3>', unsafe_allow_html=True)
        fecha_estudio   = st.date_input("Fecha del estudio", value=date.today())
        medico_ref      = st.text_input("Médico remitente")
        diagnostico_pre = st.text_input("Diagnóstico presuntivo / motivo")
        indicacion      = st.selectbox("Indicación principal", [
            "Sospecha de SAHOS",
            "Roncador habitual",
            "Apneas observadas",
            "Hipertrofia adenoamigdalina",
            "Titulación CPAP/BPAP",
            "Control post-quirúrgico",
            "Hipoventilación central",
            "Movimientos periódicos de extremidades",
            "Parasomnias",
            "Otra"
        ])
        tipo_estudio    = st.selectbox("Tipo de estudio", [
            "PSG diagnóstica completa",
            "PSG de titulación CPAP",
            "PSG de titulación BPAP",
            "PSG split-night"
        ])
        tecnico         = st.text_input("Técnico responsable")
        equipo          = st.text_input("Equipo / software", value="")
        st.markdown('</div>', unsafe_allow_html=True)

    # Calcular edad
    hoy = date.today()
    edad_anos = (hoy - fecha_nac).days // 365
    edad_meses_total = (hoy - fecha_nac).days // 30
    meses_resto = edad_meses_total % 12

    if edad_anos < 2:
        edad_str = f"{edad_meses_total} meses"
        grupo_edad = "lactante"
    elif edad_anos < 13:
        edad_str = f"{edad_anos} años {meses_resto} meses"
        grupo_edad = "preescolar_escolar"
    else:
        edad_str = f"{edad_anos} años {meses_resto} meses"
        grupo_edad = "adolescente"

    imc = peso_kg / ((talla_cm / 100) ** 2) if talla_cm > 0 else 0
    st.info(f"**Edad calculada:** {edad_str}  |  **IMC:** {imc:.1f} kg/m²")


# ──────────────────────────────────
# TAB 2 — Arquitectura del Sueño
# ──────────────────────────────────
with tab2:
    col1, col2 = st.columns(2)
    with col1:
        st.markdown('<div class="section-card"><h3>⏱️ Tiempos Globales</h3>', unsafe_allow_html=True)
        TRT  = st.number_input("Tiempo Total de Registro — TRT (min)", 0.0, 600.0, 480.0, 1.0)
        TST  = st.number_input("Tiempo Total de Sueño — TST (min)",    0.0, 600.0, 420.0, 1.0)
        SOL  = st.number_input("Latencia al Sueño — SOL (min)",        0.0, 120.0, 15.0, 0.5)
        RLAT = st.number_input("Latencia REM (min)",                   0.0, 300.0, 90.0, 1.0)
        WASO = st.number_input("Vigilia intrasueño — WASO (min)",      0.0, 300.0, 20.0, 1.0)
        st.markdown('</div>', unsafe_allow_html=True)

    with col2:
        st.markdown('<div class="section-card"><h3>📊 Estadios del Sueño (% del TST)</h3>', unsafe_allow_html=True)
        N1_pct  = st.number_input("N1 (%)", 0.0, 100.0, 5.0, 0.5)
        N2_pct  = st.number_input("N2 (%)", 0.0, 100.0, 45.0, 0.5)
        N3_pct  = st.number_input("N3 — Sueño de ondas lentas (%)", 0.0, 100.0, 25.0, 0.5)
        REM_pct = st.number_input("REM (%)", 0.0, 100.0, 25.0, 0.5)
        total_stages = N1_pct + N2_pct + N3_pct + REM_pct
        if abs(total_stages - 100) > 1:
            st.warning(f"⚠️ Los porcentajes suman {total_stages:.1f}% (debe ser ≈100%)")
        st.markdown('</div>', unsafe_allow_html=True)

    # Derivados
    SE = (TST / TRT * 100) if TRT > 0 else 0

    with st.expander("📐 Valores calculados automáticamente"):
        colA, colB, colC = st.columns(3)
        colA.metric("Eficiencia del sueño (SE%)", f"{SE:.1f}%",
                    "Normal ≥85%" if SE >= 85 else "⚠️ Reducida")
        colB.metric("N3 + REM (sueño restaurador)", f"{N3_pct + REM_pct:.1f}%",
                    "Normal >35%" if (N3_pct + REM_pct) >= 35 else "⚠️ Bajo")
        colC.metric("SOL", f"{SOL:.0f} min", "Normal <20 min" if SOL < 20 else "⚠️ Prolongada")


# ──────────────────────────────────
# TAB 3 — Respiratorio
# ──────────────────────────────────
with tab3:
    col1, col2 = st.columns(2)
    with col1:
        st.markdown('<div class="section-card"><h3>🌬️ Índices Respiratorios (/h TST)</h3>', unsafe_allow_html=True)
        IAO  = st.number_input("Índice de Apnea Obstructiva — IAO (/h)", 0.0, 200.0, 0.0, 0.1,
                               help="Normal pediátrico: <1/h (AASM 2020)")
        IAC  = st.number_input("Índice de Apnea Central — IAC (/h)",     0.0, 100.0, 0.0, 0.1,
                               help="Normal: <1/h; en neonatos <0-3/h aisladas se toleran")
        IAM  = st.number_input("Índice de Apnea Mixta — IAM (/h)",       0.0, 100.0, 0.0, 0.1)
        IH   = st.number_input("Índice de Hipopnea — IH (/h)",           0.0, 200.0, 0.0, 0.1,
                               help="Hipopnea: caída flujo ≥30% + 3% desat o arousal")
        IDR  = st.number_input("Índice de Disturbio Respiratorio — IDR (/h)", 0.0, 200.0, 0.0, 0.1,
                               help="IDR = IAH + RERA (esfuerzos respiratorios relacionados con arousal)")
        st.markdown('</div>', unsafe_allow_html=True)

    with col2:
        st.markdown('<div class="section-card"><h3>🩸 Oximetría y Capnografía</h3>', unsafe_allow_html=True)
        SpO2_basal = st.number_input("SpO₂ basal en vigilia (%)", 80.0, 100.0, 98.0, 0.5)
        SpO2_media = st.number_input("SpO₂ media durante el sueño (%)", 60.0, 100.0, 96.0, 0.5)
        SpO2_nadir = st.number_input("SpO₂ nadir (mínima) (%)", 50.0, 100.0, 92.0, 0.5)
        T90 = st.number_input("Tiempo con SpO₂ <90% — T90 (min)", 0.0, 600.0, 0.0, 0.5,
                              help="T90 >1 min es clínicamente significativo en niños")
        T95 = st.number_input("Tiempo con SpO₂ <95% — T95 (min)", 0.0, 600.0, 0.0, 1.0)

        st.markdown("**Capnografía (si disponible)**")
        capno = st.checkbox("Capnografía realizada")
        if capno:
            ETCO2_pico  = st.number_input("EtCO₂ pico (mmHg)", 20.0, 80.0, 45.0, 0.5)
            ETCO2_media = st.number_input("EtCO₂ media (mmHg)", 20.0, 80.0, 40.0, 0.5)
            T_hipov     = st.number_input("Tiempo EtCO₂ >50 mmHg (min)", 0.0, 600.0, 0.0, 1.0,
                                          help="Hipoventilación: EtCO₂ >50 mmHg por >25% del TST")
        else:
            ETCO2_pico = ETCO2_media = T_hipov = None
        st.markdown('</div>', unsafe_allow_html=True)

    # IAH calculado
    IAH = IAO + IAC + IAM + IH
    st.markdown(f"""
    <div class="section-card">
      <h3>📌 IAH Calculado</h3>
      <p style="font-size:1.4rem; font-weight:700; color:#1e3a5c;">
        IAH = IAO + IAC + IAM + IH = <span style="color:#2563a0;">{IAH:.1f} /h</span>
      </p>
      <p style="font-size:0.8rem; color:#64748b;">Referencia pediátrica AASM 2020:
        Normal &lt;1/h | Leve 1–5/h | Moderado 5–10/h | Grave &gt;10/h</p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<div class="section-card"><h3>⚙️ Parámetros de Titulación (si aplica)</h3>', unsafe_allow_html=True)
    tit_col1, tit_col2 = st.columns(2)
    with tit_col1:
        tit_realizada = st.checkbox("Titulación realizada en esta PSG")
        if tit_realizada:
            dispositivo  = st.selectbox("Dispositivo", ["CPAP", "BPAP-S", "BPAP-ST", "AVAPS"])
            presion_opt  = st.number_input("Presión óptima / EPAP (cmH₂O)", 4.0, 25.0, 8.0, 0.5)
            presion_ipap = st.number_input("IPAP (cmH₂O, si BPAP)", 0.0, 30.0, 0.0, 0.5)
    with tit_col2:
        if tit_realizada:
            IAH_tit = st.number_input("IAH residual bajo titulación (/h)", 0.0, 50.0, 0.5, 0.1)
            leak_tit = st.number_input("Fuga media (L/min)", 0.0, 60.0, 5.0, 0.5)
    st.markdown('</div>', unsafe_allow_html=True)


# ──────────────────────────────────
# TAB 4 — Cardíaco y Movimientos
# ──────────────────────────────────
with tab4:
    col1, col2 = st.columns(2)
    with col1:
        st.markdown('<div class="section-card"><h3>❤️ Parámetros Cardíacos</h3>', unsafe_allow_html=True)
        FC_media = st.number_input("FC media durante sueño (lpm)", 20.0, 200.0, 75.0, 1.0)
        FC_min   = st.number_input("FC mínima (lpm)",              20.0, 200.0, 55.0, 1.0)
        FC_max   = st.number_input("FC máxima (lpm)",              20.0, 250.0, 120.0, 1.0)
        arritmia = st.multiselect("Arritmias detectadas", [
            "Ninguna",
            "Bradicardia sinusal",
            "Taquicardia sinusal",
            "Bloqueo AV",
            "Extrasístoles supraventriculares",
            "Extrasístoles ventriculares",
            "Fibrilación auricular",
            "Otra"
        ], default=["Ninguna"])
        if "Otra" in arritmia:
            arritmia_otra = st.text_input("Especifique arritmia")
        else:
            arritmia_otra = ""
        st.markdown('</div>', unsafe_allow_html=True)

    with col2:
        st.markdown('<div class="section-card"><h3>🦵 Movimientos Periódicos (MPE)</h3>', unsafe_allow_html=True)
        IMPE       = st.number_input("Índice de MPE — IMPE (/h TST)", 0.0, 100.0, 0.0, 0.1,
                                    help="Normal: <5/h en niños (AASM 2020)")
        IMPE_arousal = st.number_input("IMPE con arousal asociado (/h)", 0.0, 100.0, 0.0, 0.1)
        mpe_sintomas = st.checkbox("Síntomas clínicos de piernas inquietas")
        st.markdown('</div>', unsafe_allow_html=True)

        st.markdown('<div class="section-card"><h3>🔄 Índices de Arousal</h3>', unsafe_allow_html=True)
        AI_total = st.number_input("Índice de Arousal total — IA (/h)", 0.0, 100.0, 12.0, 0.5,
                                   help="Normal escolar: 7–15/h (varía por edad)")
        AI_resp  = st.number_input("IA respiratorio (/h)", 0.0, 100.0, 0.0, 0.5)
        AI_espon = st.number_input("IA espontáneo (/h)", 0.0, 100.0, 0.0, 0.5)
        st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div class="section-card"><h3>📝 Hallazgos adicionales / Parasomnias</h3>', unsafe_allow_html=True)
    parasomnias = st.multiselect("Parasomnias documentadas", [
        "Ninguna",
        "Sonambulismo",
        "Terrores nocturnos",
        "Pesadillas (trastorno por pesadillas)",
        "Bruxismo",
        "Enuresis nocturna",
        "Parálisis del sueño",
        "Somniloquio",
        "Otro"
    ], default=["Ninguna"])
    observaciones_tec = st.text_area("Observaciones técnicas (calidad de señal, artefactos, etc.)", height=80)
    st.markdown('</div>', unsafe_allow_html=True)


# ──────────────────────────────────
# TAB 5 — Impresión Clínica
# ──────────────────────────────────
with tab5:

    # ─── Clasificaciones ───────────────────────────────────────────────
    def clasificar_IAH(iah, edad_a):
        """AASM Pediatric Scoring Manual 2020"""
        if iah < 1:
            return "normal", "Normal"
        elif iah < 5:
            return "mild", "SAHOS leve"
        elif iah < 10:
            return "mod", "SAHOS moderado"
        else:
            return "severe", "SAHOS grave"

    def clasificar_SE(se):
        if se >= 85:  return "normal", "Normal (≥85%)"
        elif se >= 75: return "mild",  "Levemente reducida (75–84%)"
        elif se >= 65: return "mod",   "Moderadamente reducida (65–74%)"
        else:          return "severe", "Severamente reducida (<65%)"

    def clasificar_IMPE(impe):
        if impe < 5:   return "normal", "Normal (<5/h)"
        elif impe < 25: return "mild",  "Leve (5–24/h)"
        elif impe < 50: return "mod",   "Moderado (25–49/h)"
        else:           return "severe", "Grave (≥50/h)"

    def badge(nivel, texto):
        cls = {"normal":"badge-normal","mild":"badge-mild","mod":"badge-mod","severe":"badge-severe"}.get(nivel,"badge-normal")
        return f'<span class="metric-badge {cls}">{texto}</span>'

    # Clasificaciones
    iah_nivel, iah_texto = clasificar_IAH(IAH, edad_anos)
    se_nivel,  se_texto  = clasificar_SE(SE)
    mpe_nivel, mpe_texto = clasificar_IMPE(IMPE)

    # ─── Lógica narrativa ──────────────────────────────────────────────
    def generar_impresion():
        lineas = []
        fecha_hoy = datetime.now().strftime("%d/%m/%Y")

        # ── Encabezado ──
        lineas.append("═" * 72)
        lineas.append("INFORME DE POLISOMNOGRAFÍA PEDIÁTRICA")
        lineas.append("Salud Es Vivir IPS | Laboratorio de Función Pulmonar")
        lineas.append("═" * 72)
        lineas.append(f"Paciente : {paciente_nombre or '—'}  |  HC: {paciente_id or '—'}")
        lineas.append(f"Edad     : {edad_str}  |  Sexo: {sexo}  |  Peso: {peso_kg} kg  |  Talla: {talla_cm} cm  |  IMC: {imc:.1f} kg/m²")
        lineas.append(f"Estudio  : {fecha_estudio.strftime('%d/%m/%Y')}  |  {tipo_estudio}")
        lineas.append(f"Indicación: {indicacion}  |  Dx. presuntivo: {diagnostico_pre or '—'}")
        lineas.append(f"Médico remitente: {medico_ref or '—'}  |  Técnico: {tecnico or '—'}")
        lineas.append(f"Criterios: AASM Pediatric Scoring Manual 2020 | ICSD-3")
        lineas.append("")

        # ── I. Parámetros técnicos ──
        lineas.append("I. PARÁMETROS TÉCNICOS DEL REGISTRO")
        lineas.append("─" * 50)
        lineas.append(f"  Tiempo Total de Registro (TRT): {TRT:.0f} min")
        lineas.append(f"  Tiempo Total de Sueño (TST)   : {TST:.0f} min ({TST/60:.1f} h)")
        lineas.append(f"  Eficiencia del sueño (SE%)    : {SE:.1f}%  → {se_texto}")
        if observaciones_tec.strip():
            lineas.append(f"  Observaciones técnicas: {observaciones_tec.strip()}")
        lineas.append("")

        # ── II. Arquitectura ──
        lineas.append("II. ARQUITECTURA DEL SUEÑO")
        lineas.append("─" * 50)
        lineas.append(f"  Latencia al sueño (SOL)       : {SOL:.0f} min")
        lineas.append(f"  Latencia REM                  : {RLAT:.0f} min")
        lineas.append(f"  Vigilia intrasueño (WASO)     : {WASO:.0f} min")
        lineas.append(f"  N1: {N1_pct:.1f}%  |  N2: {N2_pct:.1f}%  |  N3 (SOL): {N3_pct:.1f}%  |  REM: {REM_pct:.1f}%")
        lineas.append(f"  Sueño restaurador (N3+REM)    : {N3_pct+REM_pct:.1f}%")

        # Comentario arquitectura
        arch_obs = []
        if SE < 85:
            arch_obs.append(f"eficiencia del sueño reducida ({SE:.1f}%)")
        if SOL > 20:
            arch_obs.append(f"latencia al sueño prolongada ({SOL:.0f} min)")
        if RLAT > 120:
            arch_obs.append(f"latencia REM prolongada ({RLAT:.0f} min)")
        if REM_pct < 18:
            arch_obs.append(f"porcentaje de sueño REM reducido ({REM_pct:.1f}%)")
        if N3_pct < 15:
            arch_obs.append(f"porcentaje de sueño N3 reducido ({N3_pct:.1f}%)")
        if arch_obs:
            lineas.append(f"  ► Hallazgos: Se documentó " + ", ".join(arch_obs) + ".")
        else:
            lineas.append("  ► Arquitectura del sueño dentro de parámetros normales para la edad.")
        lineas.append("")

        # ── III. Respiratorio ──
        lineas.append("III. PARÁMETROS RESPIRATORIOS")
        lineas.append("─" * 50)
        lineas.append(f"  IAO (obstructivo)             : {IAO:.1f} /h  (normal <1/h)")
        lineas.append(f"  IAC (central)                 : {IAC:.1f} /h  (normal <1/h)")
        lineas.append(f"  IAM (mixto)                   : {IAM:.1f} /h")
        lineas.append(f"  IH  (hipopneas)               : {IH:.1f}  /h")
        lineas.append(f"  ─────────────────────────────────")
        lineas.append(f"  IAH TOTAL                     : {IAH:.1f} /h  → {iah_texto.upper()}")
        lineas.append(f"  IDR                           : {IDR:.1f} /h")
        lineas.append("")
        lineas.append(f"  SpO₂ basal                    : {SpO2_basal:.1f}%")
        lineas.append(f"  SpO₂ media (sueño)            : {SpO2_media:.1f}%")
        lineas.append(f"  SpO₂ nadir                    : {SpO2_nadir:.1f}%")
        lineas.append(f"  Tiempo SpO₂ <90% (T90)        : {T90:.1f} min")
        lineas.append(f"  Tiempo SpO₂ <95% (T95)        : {T95:.1f} min")

        if capno:
            lineas.append(f"  EtCO₂ pico                    : {ETCO2_pico:.1f} mmHg")
            lineas.append(f"  EtCO₂ media                   : {ETCO2_media:.1f} mmHg")
            t_hipov_pct = (T_hipov / TST * 100) if TST > 0 else 0
            lineas.append(f"  Tiempo EtCO₂ >50 mmHg        : {T_hipov:.1f} min ({t_hipov_pct:.1f}% del TST)")

        # Comentario respiratorio
        resp_obs = []
        if IAO >= 1:
            resp_obs.append(f"eventos obstructivos con IAO de {IAO:.1f}/h")
        if IAC >= 1:
            resp_obs.append(f"apneas centrales con IAC de {IAC:.1f}/h")
        if SpO2_nadir < 90:
            resp_obs.append(f"desaturación significativa con SpO₂ nadir de {SpO2_nadir:.1f}%")
        elif SpO2_nadir < 95:
            resp_obs.append(f"desaturaciones leves con SpO₂ nadir de {SpO2_nadir:.1f}%")
        if T90 > 1:
            resp_obs.append(f"tiempo con SpO₂ <90% de {T90:.1f} min")
        if capno and T_hipov is not None:
            t_hipov_pct = (T_hipov / TST * 100) if TST > 0 else 0
            if t_hipov_pct > 25:
                resp_obs.append(f"hipoventilación nocturna (EtCO₂ >50 mmHg por {t_hipov_pct:.1f}% del TST)")
        lineas.append("")

        # ── IV. Cardíaco ──
        lineas.append("IV. PARÁMETROS CARDÍACOS")
        lineas.append("─" * 50)
        lineas.append(f"  FC media: {FC_media:.0f} lpm  |  FC mín: {FC_min:.0f} lpm  |  FC máx: {FC_max:.0f} lpm")
        arr_txt = ", ".join([a for a in arritmia if a != "Ninguna"]) or "No detectadas"
        if arritmia_otra:
            arr_txt += f", {arritmia_otra}"
        lineas.append(f"  Arritmias: {arr_txt}")
        lineas.append("")

        # ── V. Movimientos periódicos ──
        lineas.append("V. MOVIMIENTOS PERIÓDICOS DE EXTREMIDADES")
        lineas.append("─" * 50)
        lineas.append(f"  IMPE total                    : {IMPE:.1f} /h  → {mpe_texto}")
        lineas.append(f"  IMPE con arousal asociado     : {IMPE_arousal:.1f} /h")
        lineas.append(f"  Síntomas de piernas inquietas : {'Sí' if mpe_sintomas else 'No referidos'}")
        lineas.append("")

        # ── VI. Arousals ──
        lineas.append("VI. ÍNDICES DE AROUSAL")
        lineas.append("─" * 50)
        lineas.append(f"  IA total                      : {AI_total:.1f} /h  (referencia escolar: 7–15/h)")
        lineas.append(f"  IA respiratorio               : {AI_resp:.1f} /h")
        lineas.append(f"  IA espontáneo                 : {AI_espon:.1f} /h")
        lineas.append("")

        # ── VII. Parasomnias ──
        par_txt = ", ".join([p for p in parasomnias if p != "Ninguna"]) or "No documentadas"
        lineas.append("VII. PARASOMNIAS")
        lineas.append("─" * 50)
        lineas.append(f"  {par_txt}")
        lineas.append("")

        # ── VIII. Titulación ──
        if tit_realizada:
            lineas.append("VIII. PARÁMETROS DE TITULACIÓN")
            lineas.append("─" * 50)
            lineas.append(f"  Dispositivo                   : {dispositivo}")
            lineas.append(f"  Presión óptima / EPAP         : {presion_opt:.1f} cmH₂O")
            if presion_ipap > 0:
                lineas.append(f"  IPAP                          : {presion_ipap:.1f} cmH₂O")
            lineas.append(f"  IAH residual bajo titulación  : {IAH_tit:.1f} /h")
            lineas.append(f"  Fuga media                    : {leak_tit:.1f} L/min")
            lineas.append("")

        # ── IX. IMPRESIÓN CLÍNICA INTEGRADA ──
        lineas.append("═" * 72)
        lineas.append("RESULTADO FORMAL — IMPRESIÓN CLÍNICA INTEGRADA")
        lineas.append("═" * 72)

        # Párrafo integrador
        sexo_pron = "el paciente" if sexo == "Masculino" else "la paciente"

        p1 = (
            f"Estudio de polisomnografía pediátrica realizado en {sexo_pron} "
            f"{paciente_nombre or '[nombre]'}, de {edad_str}, con indicación de "
            f"{indicacion.lower()}. "
        )

        # Sueño
        if SE >= 85 and not arch_obs:
            p1 += f"La arquitectura del sueño es normal, con eficiencia de {SE:.1f}%. "
        else:
            p1 += f"Se documenta {', '.join(arch_obs) if arch_obs else f'eficiencia del sueño de {SE:.1f}%'}. "

        # Respiratorio
        if IAH < 1:
            p1 += (
                f"El índice apnea-hipopnea (IAH) es de {IAH:.1f}/h, dentro del rango "
                f"normal para la edad según criterios AASM 2020 (<1/h), sin evidencia de "
                f"síndrome de apnea-hipopnea obstructiva del sueño (SAHOS). "
            )
        else:
            p1 += (
                f"Se documenta {iah_texto} con IAH de {IAH:.1f}/h "
                f"(normal pediátrico <1/h, AASM Pediatric Scoring Manual 2020). "
            )
            if IAO >= 1:
                p1 += f"El componente obstructivo predomina con IAO de {IAO:.1f}/h. "
            if IAC >= 1:
                p1 += f"Se asocian apneas centrales con IAC de {IAC:.1f}/h. "

        # Oximetría
        if SpO2_nadir >= 95 and T90 == 0:
            p1 += f"La oximetría nocturna es normal con SpO₂ nadir de {SpO2_nadir:.1f}% y sin desaturaciones significativas. "
        elif SpO2_nadir < 90:
            p1 += (
                f"Se documenta hipoxemia nocturna con SpO₂ nadir de {SpO2_nadir:.1f}% "
                f"y T90 de {T90:.1f} min. "
            )
        else:
            p1 += f"Desaturaciones leves con SpO₂ nadir de {SpO2_nadir:.1f}%. "

        # Capnografía
        if capno:
            t_hipov_pct = (T_hipov / TST * 100) if TST > 0 else 0
            if t_hipov_pct > 25:
                p1 += (
                    f"La capnografía documenta hipoventilación nocturna con EtCO₂ pico de "
                    f"{ETCO2_pico:.1f} mmHg y EtCO₂ >50 mmHg durante {t_hipov_pct:.1f}% del TST. "
                )
            else:
                p1 += f"La capnografía no evidencia hipoventilación nocturna significativa (EtCO₂ pico {ETCO2_pico:.1f} mmHg). "

        # MPE
        if IMPE >= 5:
            p1 += (
                f"Se documenta índice de movimientos periódicos de extremidades de "
                f"{IMPE:.1f}/h, compatible con trastorno de movimientos periódicos de "
                f"extremidades {'con síntomas de síndrome de piernas inquietas' if mpe_sintomas else ''}. "
            )
        else:
            p1 += f"El índice de movimientos periódicos de extremidades es normal ({IMPE:.1f}/h). "

        # Arritmias
        arr_no_ninguna = [a for a in arritmia if a != "Ninguna"]
        if arr_no_ninguna:
            p1 += f"Desde el punto de vista cardiológico se registraron: {', '.join(arr_no_ninguna)}. "

        # Parasomnias
        par_no_ninguna = [p for p in parasomnias if p != "Ninguna"]
        if par_no_ninguna:
            p1 += f"Se documentaron las siguientes parasomnias: {', '.join(par_no_ninguna)}. "

        # Titulación
        if tit_realizada:
            p1 += (
                f"La titulación con {dispositivo} fue efectiva, alcanzando control "
                f"adecuado de eventos respiratorios con presión óptima de {presion_opt:.1f} cmH₂O "
                f"(IAH residual {IAH_tit:.1f}/h). "
            )

        lineas.append("")
        lineas.append(p1)
        lineas.append("")

        # Conclusión diagnóstica principal
        lineas.append("Conclusión diagnóstica principal:")
        if IAH < 1:
            lineas.append("  • Polisomnografía sin evidencia de SAHOS (IAH dentro de límites normales para la edad).")
        elif iah_nivel == "mild":
            lineas.append(f"  • SAHOS LEVE (IAH {IAH:.1f}/h; AASM Pediatric 2020).")
        elif iah_nivel == "mod":
            lineas.append(f"  • SAHOS MODERADO (IAH {IAH:.1f}/h; AASM Pediatric 2020).")
        else:
            lineas.append(f"  • SAHOS GRAVE (IAH {IAH:.1f}/h; AASM Pediatric 2020).")

        if IAC >= 5:
            lineas.append(f"  • Síndrome de apnea central del sueño (IAC {IAC:.1f}/h).")
        if IMPE >= 5:
            lineas.append(f"  • Trastorno de movimientos periódicos de extremidades (IMPE {IMPE:.1f}/h).")
        if par_no_ninguna:
            lineas.append(f"  • Parasomnia documentada: {', '.join(par_no_ninguna)}.")
        if capno and T_hipov is not None:
            t_hipov_pct = (T_hipov / TST * 100) if TST > 0 else 0
            if t_hipov_pct > 25:
                lineas.append(f"  • Hipoventilación nocturna (EtCO₂ >50 mmHg durante {t_hipov_pct:.1f}% del TST).")

        lineas.append("")
        lineas.append("NOTA: La interpretación clínica, el diagnóstico definitivo y las decisiones")
        lineas.append("terapéuticas son responsabilidad exclusiva del médico tratante.")
        lineas.append("")
        lineas.append(f"Fecha de informe: {fecha_hoy}")
        lineas.append("Elaborado por: Laboratorio de Función Pulmonar — Salud Es Vivir IPS")
        lineas.append("═" * 72)

        return "\n".join(lineas)

    # ─── Render ──────────────────────────────────────────────────────
    st.markdown("### 📊 Resumen de Clasificaciones")
    col_b1, col_b2, col_b3, col_b4 = st.columns(4)
    col_b1.markdown(f"**IAH:** {badge(iah_nivel, f'{IAH:.1f}/h · {iah_texto}')}", unsafe_allow_html=True)
    col_b2.markdown(f"**SE%:** {badge(se_nivel, f'{SE:.1f}% · {se_texto}')}", unsafe_allow_html=True)
    col_b3.markdown(f"**IMPE:** {badge(mpe_nivel, f'{IMPE:.1f}/h · {mpe_texto}')}", unsafe_allow_html=True)
    nadir_nivel = "normal" if SpO2_nadir >= 95 else ("mild" if SpO2_nadir >= 90 else "severe")
    col_b4.markdown(f"**SpO₂ nadir:** {badge(nadir_nivel, f'{SpO2_nadir:.1f}%')}", unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("### 📄 Impresión Clínica Integrada")

    reporte_texto = generar_impresion()

    # Mostrar reporte
    st.markdown(
        f'<div class="report-box"><pre style="white-space:pre-wrap; font-family:Courier New,monospace; font-size:0.82rem;">'
        f'{reporte_texto}</pre></div>',
        unsafe_allow_html=True
    )

    # Botones de acción
    st.markdown("---")
    col_dl1, col_dl2 = st.columns(2)
    with col_dl1:
        st.download_button(
            label="⬇️ Descargar reporte (.txt)",
            data=reporte_texto,
            file_name=f"PSG_{paciente_id or 'paciente'}_{fecha_estudio.strftime('%Y%m%d')}.txt",
            mime="text/plain",
            use_container_width=True
        )
    with col_dl2:
        st.button(
            "🖨️ Imprimir (Ctrl+P)",
            help="Use Ctrl+P o Cmd+P para imprimir o exportar a PDF desde el navegador",
            use_container_width=True
        )

    # Nota metodológica
    with st.expander("📚 Referencias y criterios diagnósticos"):
        st.markdown("""
        **Criterios AASM Pediatric Scoring Manual 2020:**
        - **IAH normal pediátrico:** <1 evento/hora de TST
        - **SAHOS Leve:** IAH 1–5/h | **Moderado:** 5–10/h | **Grave:** >10/h
        - **Apnea obstructiva:** cese flujo ≥2 ciclos respiratorios con esfuerzo persistente
        - **Apnea central:** cese flujo ≥20 s o ≥2 ciclos + arousal/bradicardia/desat ≥3%
        - **Hipopnea:** caída de flujo ≥30% × ≥2 ciclos + desat ≥3% o arousal
        - **RERA:** esfuerzo respiratorio ≥2 ciclos con limitación flujo + arousal (sin apnea/hipopnea)
        - **MPE normales:** <5/h en niños
        - **Hipoventilación:** EtCO₂ >50 mmHg por >25% del TST
        - **Eficiencia del sueño normal:** ≥85%

        **Referencias principales:**
        - AASM Pediatric Scoring Manual, 3rd ed. (2020)
        - ICSD-3 — International Classification of Sleep Disorders (2014/2023)
        - Marcus CL et al. *Diagnosis and Management of Childhood OSA Syndrome.* Pediatrics 2012
        """)

# ─────────────────────────────────────────────
# Footer
# ─────────────────────────────────────────────
st.markdown("---")
st.markdown(
    "<div style='text-align:center; color:#94a3b8; font-size:0.75rem;'>"
    "Salud Es Vivir IPS · Laboratorio de Función Pulmonar · "
    "AASM Pediatric Scoring Manual 2020 · ICSD-3 · "
    "La interpretación clínica es responsabilidad exclusiva del médico tratante."
    "</div>",
    unsafe_allow_html=True
)

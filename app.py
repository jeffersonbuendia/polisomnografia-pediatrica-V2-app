"""
Polisomnografía Pediátrica — Calculadora Clínica con Impresión Integrada
Jefferson — Médico Neumólogo Pediatra
Criterios: AASM Pediatric Scoring Manual 2020 | ICSD-3
"""

import streamlit as st
from datetime import date, datetime
import base64

st.set_page_config(
    page_title="PSG Pediátrica",
    page_icon="🫁",
    layout="wide",
    initial_sidebar_state="expanded",
)

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
.metric-badge { display:inline-block; padding:3px 10px; border-radius:20px;
    font-size:0.78rem; font-weight:600; margin:2px; }
.badge-normal { background:#d1fae5; color:#065f46; }
.badge-mild   { background:#fef3c7; color:#92400e; }
.badge-mod    { background:#fed7aa; color:#9a3412; }
.badge-severe { background:#fee2e2; color:#991b1b; }
.report-box { background:#fff; border:1px solid #cbd5e1; border-radius:10px;
    padding:28px 32px; font-family:'Courier New',monospace; font-size:0.84rem;
    line-height:1.7; color:#1e293b; }
.dl-link { display:block; text-align:center; padding:9px; color:white;
    border-radius:8px; text-decoration:none; font-weight:600; font-size:0.9rem; }
</style>
""", unsafe_allow_html=True)

st.markdown("""
<div class="main-header">
  <h1>🫁 Polisomnografía Pediátrica</h1>
  <p>Calculadora Clínica con Impresión Integrada · AASM Pediatric Scoring Manual 2020 · ICSD-3</p>
</div>
""", unsafe_allow_html=True)

tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "👤 Paciente y Estudio",
    "💤 Arquitectura del Sueño",
    "🌬️ Parámetros Respiratorios",
    "❤️ Cardíaco & Movimientos",
    "📄 Impresión Clínica"
])

# ── TAB 1 ──────────────────────────────────────────────────────────────
with tab1:
    c1, c2 = st.columns(2)
    with c1:
        st.markdown('<div class="section-card"><h3>🧒 Datos del Paciente</h3>', unsafe_allow_html=True)
        paciente_nombre = st.text_input("Nombre completo")
        paciente_id     = st.text_input("N° Historia Clínica / ID")
        fecha_nac       = st.date_input("Fecha de nacimiento", value=date(2015, 1, 1), min_value=date(1990, 1, 1))
        sexo            = st.selectbox("Sexo biológico", ["Masculino", "Femenino"])
        peso_kg         = st.number_input("Peso (kg)", 0.0, 150.0, 20.0, 0.1)
        talla_cm        = st.number_input("Talla (cm)", 40.0, 200.0, 110.0, 0.5)
        st.markdown('</div>', unsafe_allow_html=True)
    with c2:
        st.markdown('<div class="section-card"><h3>📋 Datos del Estudio</h3>', unsafe_allow_html=True)
        fecha_estudio   = st.date_input("Fecha del estudio", value=date.today())
        medico_ref      = st.text_input("Médico remitente")
        diagnostico_pre = st.text_input("Diagnóstico presuntivo / motivo")
        indicacion      = st.selectbox("Indicación principal", [
            "Sospecha de SAHOS", "Roncador habitual", "Apneas observadas",
            "Hipertrofia adenoamigdalina", "Titulación CPAP/BPAP",
            "Control post-quirúrgico", "Hipoventilación central",
            "Movimientos periódicos de extremidades", "Parasomnias", "Otra"])
        tipo_estudio    = st.selectbox("Tipo de estudio", [
            "PSG diagnóstica completa", "PSG de titulación CPAP",
            "PSG de titulación BPAP", "PSG split-night"])
        tecnico         = st.text_input("Técnico responsable")
        equipo          = st.text_input("Equipo / software")
        st.markdown('</div>', unsafe_allow_html=True)

    hoy = date.today()
    edad_anos        = (hoy - fecha_nac).days // 365
    edad_meses_total = (hoy - fecha_nac).days // 30
    meses_resto      = edad_meses_total % 12
    edad_str  = f"{edad_meses_total} meses" if edad_anos < 2 else f"{edad_anos} años {meses_resto} meses"
    imc       = peso_kg / ((talla_cm / 100) ** 2) if talla_cm > 0 else 0
    st.info(f"**Edad calculada:** {edad_str}  |  **IMC:** {imc:.1f} kg/m²")

# ── TAB 2 ──────────────────────────────────────────────────────────────
with tab2:
    c1, c2 = st.columns(2)
    with c1:
        st.markdown('<div class="section-card"><h3>⏱️ Tiempos Globales</h3>', unsafe_allow_html=True)
        TRT  = st.number_input("TRT — Tiempo Total de Registro (min)", 0.0, 600.0, 480.0, 1.0)
        TST  = st.number_input("TST — Tiempo Total de Sueño (min)",    0.0, 600.0, 420.0, 1.0)
        SOL  = st.number_input("SOL — Latencia al Sueño (min)",        0.0, 120.0, 15.0, 0.5)
        RLAT = st.number_input("Latencia REM (min)",                   0.0, 300.0, 90.0, 1.0)
        WASO = st.number_input("WASO — Vigilia intrasueño (min)",      0.0, 300.0, 20.0, 1.0)
        st.markdown('</div>', unsafe_allow_html=True)
    with c2:
        st.markdown('<div class="section-card"><h3>📊 Estadios del Sueño (% del TST)</h3>', unsafe_allow_html=True)
        N1_pct  = st.number_input("N1 (%)", 0.0, 100.0, 5.0, 0.5)
        N2_pct  = st.number_input("N2 (%)", 0.0, 100.0, 45.0, 0.5)
        N3_pct  = st.number_input("N3 — Sueño de ondas lentas (%)", 0.0, 100.0, 25.0, 0.5)
        REM_pct = st.number_input("REM (%)", 0.0, 100.0, 25.0, 0.5)
        total_s = N1_pct + N2_pct + N3_pct + REM_pct
        if abs(total_s - 100) > 1:
            st.warning(f"⚠️ Los porcentajes suman {total_s:.1f}% (debe ser ≈100%)")
        st.markdown('</div>', unsafe_allow_html=True)

    SE = (TST / TRT * 100) if TRT > 0 else 0
    with st.expander("📐 Valores calculados automáticamente"):
        ca, cb, cc = st.columns(3)
        ca.metric("SE%", f"{SE:.1f}%", "Normal ≥85%" if SE >= 85 else "⚠️ Reducida")
        cb.metric("N3+REM", f"{N3_pct+REM_pct:.1f}%", "Normal >35%" if N3_pct+REM_pct >= 35 else "⚠️ Bajo")
        cc.metric("SOL", f"{SOL:.0f} min", "Normal <20 min" if SOL < 20 else "⚠️ Prolongada")

# ── TAB 3 ──────────────────────────────────────────────────────────────
with tab3:
    c1, c2 = st.columns(2)
    with c1:
        st.markdown('<div class="section-card"><h3>🌬️ Índices Respiratorios (/h TST)</h3>', unsafe_allow_html=True)
        IAO = st.number_input("IAO — Índice de Apnea Obstructiva (/h)", 0.0, 200.0, 0.0, 0.1, help="Normal <1/h")
        IAC = st.number_input("IAC — Índice de Apnea Central (/h)",     0.0, 100.0, 0.0, 0.1)
        IAM = st.number_input("IAM — Índice de Apnea Mixta (/h)",       0.0, 100.0, 0.0, 0.1)
        IH  = st.number_input("IH — Índice de Hipopnea (/h)",           0.0, 200.0, 0.0, 0.1)
        IDR = st.number_input("IDR — Índice de Disturbio Respiratorio (/h)", 0.0, 200.0, 0.0, 0.1)
        st.markdown('</div>', unsafe_allow_html=True)
    with c2:
        st.markdown('<div class="section-card"><h3>🩸 Oximetría y Capnografía</h3>', unsafe_allow_html=True)
        SpO2_basal = st.number_input("SpO₂ basal en vigilia (%)", 80.0, 100.0, 98.0, 0.5)
        SpO2_media = st.number_input("SpO₂ media durante el sueño (%)", 60.0, 100.0, 96.0, 0.5)
        SpO2_nadir = st.number_input("SpO₂ nadir — mínima (%)", 50.0, 100.0, 92.0, 0.5)
        T90        = st.number_input("T90 — tiempo SpO₂ <90% (min)", 0.0, 600.0, 0.0, 0.5)
        T95        = st.number_input("T95 — tiempo SpO₂ <95% (min)", 0.0, 600.0, 0.0, 1.0)
        st.markdown("**Capnografía (si disponible)**")
        capno = st.checkbox("Capnografía realizada")
        if capno:
            ETCO2_pico  = st.number_input("EtCO₂ pico (mmHg)", 20.0, 80.0, 45.0, 0.5)
            ETCO2_media = st.number_input("EtCO₂ media (mmHg)", 20.0, 80.0, 40.0, 0.5)
            T_hipov     = st.number_input("Tiempo EtCO₂ >50 mmHg (min)", 0.0, 600.0, 0.0, 1.0,
                                          help="Hipoventilación: EtCO₂ >50 mmHg por >25% TST")
        else:
            ETCO2_pico = ETCO2_media = T_hipov = None
        st.markdown('</div>', unsafe_allow_html=True)

    IAH = IAO + IAC + IAM + IH
    st.markdown(f"""
    <div class="section-card">
      <h3>📌 IAH Calculado</h3>
      <p style="font-size:1.4rem;font-weight:700;color:#1e3a5c;">
        IAH = IAO + IAC + IAM + IH = <span style="color:#2563a0;">{IAH:.1f} /h</span>
      </p>
      <p style="font-size:0.8rem;color:#64748b;">
        Normal &lt;1/h | Leve 1–5/h | Moderado 5–10/h | Grave &gt;10/h (AASM Pediatric 2020)</p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<div class="section-card"><h3>⚙️ Parámetros de Titulación (si aplica)</h3>', unsafe_allow_html=True)
    tc1, tc2 = st.columns(2)
    with tc1:
        tit_realizada = st.checkbox("Titulación realizada en esta PSG")
        if tit_realizada:
            dispositivo  = st.selectbox("Dispositivo", ["CPAP", "BPAP-S", "BPAP-ST", "AVAPS"])
            presion_opt  = st.number_input("Presión óptima / EPAP (cmH₂O)", 4.0, 25.0, 8.0, 0.5)
            presion_ipap = st.number_input("IPAP (cmH₂O, si BPAP)", 0.0, 30.0, 0.0, 0.5)
    with tc2:
        if tit_realizada:
            IAH_tit  = st.number_input("IAH residual bajo titulación (/h)", 0.0, 50.0, 0.5, 0.1)
            leak_tit = st.number_input("Fuga media (L/min)", 0.0, 60.0, 5.0, 0.5)
    st.markdown('</div>', unsafe_allow_html=True)

# ── TAB 4 ──────────────────────────────────────────────────────────────
with tab4:
    c1, c2 = st.columns(2)
    with c1:
        st.markdown('<div class="section-card"><h3>❤️ Parámetros Cardíacos</h3>', unsafe_allow_html=True)
        FC_media = st.number_input("FC media sueño (lpm)", 20.0, 200.0, 75.0, 1.0)
        FC_min   = st.number_input("FC mínima (lpm)",      20.0, 200.0, 55.0, 1.0)
        FC_max   = st.number_input("FC máxima (lpm)",      20.0, 250.0, 120.0, 1.0)
        arritmia = st.multiselect("Arritmias detectadas", [
            "Ninguna", "Bradicardia sinusal", "Taquicardia sinusal", "Bloqueo AV",
            "Extrasístoles supraventriculares", "Extrasístoles ventriculares",
            "Fibrilación auricular", "Otra"], default=["Ninguna"])
        arritmia_otra = st.text_input("Especifique arritmia") if "Otra" in arritmia else ""
        st.markdown('</div>', unsafe_allow_html=True)
    with c2:
        st.markdown('<div class="section-card"><h3>🦵 Movimientos Periódicos (MPE)</h3>', unsafe_allow_html=True)
        IMPE         = st.number_input("IMPE — Índice de MPE (/h TST)", 0.0, 100.0, 0.0, 0.1, help="Normal <5/h")
        IMPE_arousal = st.number_input("IMPE con arousal asociado (/h)", 0.0, 100.0, 0.0, 0.1)
        mpe_sintomas = st.checkbox("Síntomas clínicos de piernas inquietas")
        st.markdown('</div>', unsafe_allow_html=True)
        st.markdown('<div class="section-card"><h3>🔄 Índices de Arousal</h3>', unsafe_allow_html=True)
        AI_total = st.number_input("IA total (/h)", 0.0, 100.0, 12.0, 0.5, help="Referencia escolar: 7–15/h")
        AI_resp  = st.number_input("IA respiratorio (/h)", 0.0, 100.0, 0.0, 0.5)
        AI_espon = st.number_input("IA espontáneo (/h)", 0.0, 100.0, 0.0, 0.5)
        st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div class="section-card"><h3>📝 Parasomnias y Observaciones</h3>', unsafe_allow_html=True)
    parasomnias = st.multiselect("Parasomnias documentadas", [
        "Ninguna", "Sonambulismo", "Terrores nocturnos", "Pesadillas",
        "Bruxismo", "Enuresis nocturna", "Parálisis del sueño", "Somniloquio", "Otro"],
        default=["Ninguna"])
    observaciones_tec = st.text_area("Observaciones técnicas (calidad de señal, artefactos, etc.)", height=70)
    st.markdown('</div>', unsafe_allow_html=True)

# ── TAB 5 ──────────────────────────────────────────────────────────────
with tab5:

    def badge(nivel, texto):
        cls = {"normal":"badge-normal","mild":"badge-mild","mod":"badge-mod","severe":"badge-severe"}.get(nivel,"badge-normal")
        return f'<span class="metric-badge {cls}">{texto}</span>'

    IAH_nivel = "normal" if IAH < 1 else "mild" if IAH < 5 else "mod" if IAH < 10 else "severe"
    IAH_texto = "Normal" if IAH < 1 else "SAHOS leve" if IAH < 5 else "SAHOS moderado" if IAH < 10 else "SAHOS grave"
    SE_nivel  = "normal" if SE >= 85 else "mild" if SE >= 75 else "mod" if SE >= 65 else "severe"
    SE_texto  = ("Normal (≥85%)" if SE >= 85 else "Levemente reducida (75–84%)"
                 if SE >= 75 else "Moderadamente reducida (65–74%)" if SE >= 65
                 else "Severamente reducida (<65%)")
    MPE_nivel = "normal" if IMPE < 5 else "mild" if IMPE < 25 else "mod" if IMPE < 50 else "severe"
    MPE_texto = ("Normal (<5/h)" if IMPE < 5 else "Leve (5–24/h)"
                 if IMPE < 25 else "Moderado (25–49/h)" if IMPE < 50 else "Grave (≥50/h)")

    def generar_reporte():
        fecha_hoy = datetime.now().strftime("%d/%m/%Y")
        pron = "el paciente" if sexo == "Masculino" else "la paciente"
        L = 72

        R = []
        R.append("═" * L)
        R.append("INFORME DE POLISOMNOGRAFÍA PEDIÁTRICA")
        R.append("Criterios: AASM Pediatric Scoring Manual 2020 · ICSD-3")
        R.append("═" * L)
        R.append(f"Paciente  : {paciente_nombre or '—'}  |  HC: {paciente_id or '—'}")
        R.append(f"Edad      : {edad_str}  |  Sexo: {sexo}  |  Peso: {peso_kg} kg  |  Talla: {talla_cm} cm  |  IMC: {imc:.1f} kg/m²")
        R.append(f"Estudio   : {fecha_estudio.strftime('%d/%m/%Y')}  |  {tipo_estudio}")
        R.append(f"Indicación: {indicacion}  |  Dx. presuntivo: {diagnostico_pre or '—'}")
        R.append(f"Remitente : {medico_ref or '—'}  |  Técnico: {tecnico or '—'}")
        R.append("")

        R.append("I. PARÁMETROS TÉCNICOS DEL REGISTRO")
        R.append("─" * 50)
        R.append(f"  TRT: {TRT:.0f} min  |  TST: {TST:.0f} min ({TST/60:.1f} h)  |  SE: {SE:.1f}%  →  {SE_texto}")
        if observaciones_tec.strip():
            R.append(f"  Observaciones: {observaciones_tec.strip()}")
        R.append("")

        R.append("II. ARQUITECTURA DEL SUEÑO")
        R.append("─" * 50)
        R.append(f"  SOL: {SOL:.0f} min  |  Latencia REM: {RLAT:.0f} min  |  WASO: {WASO:.0f} min")
        R.append(f"  N1: {N1_pct:.1f}%  |  N2: {N2_pct:.1f}%  |  N3: {N3_pct:.1f}%  |  REM: {REM_pct:.1f}%")
        R.append(f"  Sueño restaurador (N3+REM): {N3_pct+REM_pct:.1f}%")
        arch = []
        if SE < 85:      arch.append(f"eficiencia del sueño reducida ({SE:.1f}%)")
        if SOL > 20:     arch.append(f"latencia al sueño prolongada ({SOL:.0f} min)")
        if RLAT > 120:   arch.append(f"latencia REM prolongada ({RLAT:.0f} min)")
        if REM_pct < 18: arch.append(f"REM reducido ({REM_pct:.1f}%)")
        if N3_pct < 15:  arch.append(f"N3 reducido ({N3_pct:.1f}%)")
        R.append(f"  ► {', '.join(arch)}." if arch
                 else "  ► Arquitectura del sueño dentro de parámetros normales para la edad.")
        R.append("")

        R.append("III. PARÁMETROS RESPIRATORIOS")
        R.append("─" * 50)
        R.append(f"  IAO: {IAO:.1f} /h  |  IAC: {IAC:.1f} /h  |  IAM: {IAM:.1f} /h  |  IH: {IH:.1f} /h")
        R.append(f"  ─────────────────────────────────")
        R.append(f"  IAH TOTAL: {IAH:.1f} /h  →  {IAH_texto.upper()}")
        R.append(f"  IDR: {IDR:.1f} /h")
        R.append(f"  SpO₂ basal: {SpO2_basal:.1f}%  |  media: {SpO2_media:.1f}%  |  nadir: {SpO2_nadir:.1f}%")
        R.append(f"  T90: {T90:.1f} min  |  T95: {T95:.1f} min")
        if capno:
            thp = (T_hipov / TST * 100) if TST > 0 else 0
            R.append(f"  EtCO₂ pico: {ETCO2_pico:.1f} mmHg  |  media: {ETCO2_media:.1f} mmHg  |  T>50 mmHg: {T_hipov:.1f} min ({thp:.1f}% TST)")
        R.append("")

        R.append("IV. PARÁMETROS CARDÍACOS")
        R.append("─" * 50)
        R.append(f"  FC media: {FC_media:.0f} lpm  |  FC mín: {FC_min:.0f} lpm  |  FC máx: {FC_max:.0f} lpm")
        arr_txt = ", ".join([a for a in arritmia if a != "Ninguna"]) or "No detectadas"
        if arritmia_otra: arr_txt += f", {arritmia_otra}"
        R.append(f"  Arritmias: {arr_txt}")
        R.append("")

        R.append("V. MOVIMIENTOS PERIÓDICOS DE EXTREMIDADES")
        R.append("─" * 50)
        R.append(f"  IMPE: {IMPE:.1f} /h  →  {MPE_texto}")
        R.append(f"  IMPE con arousal: {IMPE_arousal:.1f} /h  |  Piernas inquietas: {'Sí' if mpe_sintomas else 'No referidos'}")
        R.append("")

        R.append("VI. ÍNDICES DE AROUSAL")
        R.append("─" * 50)
        R.append(f"  IA total: {AI_total:.1f} /h  |  IA respiratorio: {AI_resp:.1f} /h  |  IA espontáneo: {AI_espon:.1f} /h")
        R.append("")

        par_txt = ", ".join([p for p in parasomnias if p != "Ninguna"]) or "No documentadas"
        R.append("VII. PARASOMNIAS")
        R.append("─" * 50)
        R.append(f"  {par_txt}")
        R.append("")

        if tit_realizada:
            R.append("VIII. PARÁMETROS DE TITULACIÓN")
            R.append("─" * 50)
            R.append(f"  Dispositivo: {dispositivo}  |  Presión óptima / EPAP: {presion_opt:.1f} cmH₂O")
            if presion_ipap > 0:
                R.append(f"  IPAP: {presion_ipap:.1f} cmH₂O")
            R.append(f"  IAH residual: {IAH_tit:.1f} /h  |  Fuga media: {leak_tit:.1f} L/min")
            R.append("")

        R.append("═" * L)
        R.append("RESULTADO FORMAL — IMPRESIÓN CLÍNICA INTEGRADA")
        R.append("═" * L)
        R.append("")

        p = (f"Estudio de polisomnografía pediátrica realizado en {pron} "
             f"{paciente_nombre or '[nombre]'}, de {edad_str}, con indicación de "
             f"{indicacion.lower()}. ")
        if arch:
            p += f"Se documenta {', '.join(arch)}. "
        else:
            p += f"La arquitectura del sueño es normal con eficiencia de {SE:.1f}%. "

        if IAH < 1:
            p += (f"El índice apnea-hipopnea (IAH) es de {IAH:.1f}/h, dentro del rango "
                  f"normal para la edad según criterios AASM 2020 (<1/h), sin evidencia de "
                  f"síndrome de apnea-hipopnea obstructiva del sueño (SAHOS). ")
        else:
            p += (f"Se documenta {IAH_texto} con IAH de {IAH:.1f}/h "
                  f"(normal pediátrico <1/h, AASM Pediatric Scoring Manual 2020). ")
            if IAO >= 1: p += f"El componente obstructivo predomina con IAO de {IAO:.1f}/h. "
            if IAC >= 1: p += f"Se asocian apneas centrales con IAC de {IAC:.1f}/h. "

        if SpO2_nadir >= 95 and T90 == 0:
            p += f"La oximetría nocturna es normal con SpO₂ nadir de {SpO2_nadir:.1f}% sin desaturaciones significativas. "
        elif SpO2_nadir < 90:
            p += f"Se documenta hipoxemia nocturna con SpO₂ nadir de {SpO2_nadir:.1f}% y T90 de {T90:.1f} min. "
        else:
            p += f"Desaturaciones leves con SpO₂ nadir de {SpO2_nadir:.1f}%. "

        if capno:
            thp = (T_hipov / TST * 100) if TST > 0 else 0
            if thp > 25:
                p += (f"La capnografía documenta hipoventilación nocturna con EtCO₂ pico de "
                      f"{ETCO2_pico:.1f} mmHg (EtCO₂ >50 mmHg durante {thp:.1f}% del TST). ")
            else:
                p += f"La capnografía no evidencia hipoventilación nocturna significativa (EtCO₂ pico {ETCO2_pico:.1f} mmHg). "

        if IMPE >= 5:
            p += (f"Se documenta índice de MPE de {IMPE:.1f}/h compatible con trastorno de "
                  f"movimientos periódicos de extremidades"
                  f"{' con síntomas de síndrome de piernas inquietas' if mpe_sintomas else ''}. ")
        else:
            p += f"El índice de MPE es normal ({IMPE:.1f}/h). "

        arr_no = [a for a in arritmia if a != "Ninguna"]
        if arr_no:
            p += f"Desde el punto de vista cardiológico se registraron: {', '.join(arr_no)}. "
        par_no = [x for x in parasomnias if x != "Ninguna"]
        if par_no:
            p += f"Parasomnias documentadas: {', '.join(par_no)}. "
        if tit_realizada:
            p += (f"La titulación con {dispositivo} fue efectiva con presión óptima de "
                  f"{presion_opt:.1f} cmH₂O (IAH residual {IAH_tit:.1f}/h). ")

        R.append(p)
        R.append("")
        R.append("Conclusión diagnóstica principal:")

        if IAH < 1:
            R.append("  • Polisomnografía sin evidencia de SAHOS (IAH dentro de límites normales para la edad).")
        elif IAH_nivel == "mild":
            R.append(f"  • SAHOS LEVE (IAH {IAH:.1f}/h — AASM Pediatric Scoring Manual 2020).")
        elif IAH_nivel == "mod":
            R.append(f"  • SAHOS MODERADO (IAH {IAH:.1f}/h — AASM Pediatric Scoring Manual 2020).")
        else:
            R.append(f"  • SAHOS GRAVE (IAH {IAH:.1f}/h — AASM Pediatric Scoring Manual 2020).")
        if IAC >= 5:
            R.append(f"  • Síndrome de apnea central del sueño (IAC {IAC:.1f}/h).")
        if IMPE >= 5:
            R.append(f"  • Trastorno de movimientos periódicos de extremidades (IMPE {IMPE:.1f}/h).")
        if capno and T_hipov is not None:
            thp = (T_hipov / TST * 100) if TST > 0 else 0
            if thp > 25:
                R.append(f"  • Hipoventilación nocturna (EtCO₂ >50 mmHg durante {thp:.1f}% del TST).")
        if par_no:
            R.append(f"  • Parasomnia: {', '.join(par_no)}.")

        R.append("")
        R.append(f"Fecha de informe: {fecha_hoy}")
        R.append("═" * L)
        return "\n".join(R)

    # Sumario de clasificaciones
    st.markdown("### 📊 Resumen de Clasificaciones")
    cb1, cb2, cb3, cb4 = st.columns(4)
    cb1.markdown(f"**IAH:** {badge(IAH_nivel, f'{IAH:.1f}/h · {IAH_texto}')}", unsafe_allow_html=True)
    cb2.markdown(f"**SE%:** {badge(SE_nivel, f'{SE:.1f}% · {SE_texto}')}", unsafe_allow_html=True)
    cb3.markdown(f"**IMPE:** {badge(MPE_nivel, f'{IMPE:.1f}/h · {MPE_texto}')}", unsafe_allow_html=True)
    niv_n = "normal" if SpO2_nadir >= 95 else ("mild" if SpO2_nadir >= 90 else "severe")
    cb4.markdown(f"**SpO₂ nadir:** {badge(niv_n, f'{SpO2_nadir:.1f}%')}", unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("### 📄 Impresión Clínica Integrada")

    reporte_texto = generar_reporte()

    st.markdown(
        f'<div class="report-box"><pre style="white-space:pre-wrap;margin:0;">'
        f'{reporte_texto}</pre></div>',
        unsafe_allow_html=True
    )

    # Descarga
    def build_html(texto):
        nombre_p = paciente_nombre or "Paciente"
        hc_p     = paciente_id or "—"
        fecha_p  = fecha_estudio.strftime("%d/%m/%Y")
        return f"""<!DOCTYPE html>
<html lang="es"><head><meta charset="UTF-8">
<title>PSG Pediátrica — {nombre_p}</title>
<style>
@page{{size:letter;margin:2cm 2.2cm}}
body{{font-family:'Courier New',monospace;font-size:10.5pt;line-height:1.65;color:#111;background:#fff}}
pre{{white-space:pre-wrap;word-break:break-word;margin:0}}
h1{{font-family:Arial,sans-serif;font-size:13pt;font-weight:700;color:#1a3a5c;
    border-bottom:2px solid #1a3a5c;padding-bottom:6px;margin-bottom:14px}}
.meta{{font-family:Arial,sans-serif;font-size:9pt;color:#666;margin-bottom:16px}}
</style></head><body>
<h1>Informe de Polisomnografía Pediátrica</h1>
<div class="meta">AASM Pediatric Scoring Manual 2020 · ICSD-3 · Fecha: {fecha_p} · HC: {hc_p}</div>
<pre>{texto}</pre>
</body></html>"""

    html_out   = build_html(reporte_texto)
    nombre_arch = f"PSG_{paciente_id or 'paciente'}_{fecha_estudio.strftime('%Y%m%d')}"
    b64        = base64.b64encode(html_out.encode()).decode()

    st.markdown("---")
    dl1, dl2 = st.columns(2)
    with dl1:
        st.markdown(
            f'<a href="data:text/html;base64,{b64}" download="{nombre_arch}.html" '
            f'class="dl-link" style="background:#1e3a5c;">'
            f'⬇️ Descargar para PDF</a>',
            unsafe_allow_html=True)
        st.caption("Ctrl+P → Guardar como PDF desde el navegador")
    with dl2:
        st.markdown(
            f'<a href="data:application/msword;base64,{b64}" download="{nombre_arch}.doc" '
            f'class="dl-link" style="background:#2563a0;">'
            f'⬇️ Descargar como .DOC</a>',
            unsafe_allow_html=True)
        st.caption("Abre directamente en Microsoft Word")

    with st.expander("📚 Referencias y criterios diagnósticos"):
        st.markdown("""
**Criterios AASM Pediatric Scoring Manual 2020:**
- IAH normal pediátrico: <1 /h · Leve 1–5/h · Moderado 5–10/h · Grave >10/h
- Apnea obstructiva: cese flujo ≥2 ciclos con esfuerzo persistente
- Apnea central: cese flujo ≥20 s o ≥2 ciclos + arousal/bradicardia/desat ≥3%
- Hipopnea: caída flujo ≥30% × ≥2 ciclos + desat ≥3% o arousal
- Hipoventilación: EtCO₂ >50 mmHg por >25% del TST
- MPE normales: <5/h en niños · Eficiencia del sueño normal: ≥85%

**Referencias:**
- AASM Pediatric Scoring Manual, 3rd ed. (2020) · ICSD-3 (2014/2023)
- Marcus CL et al. CHAT. NEJM 2013 · Marcus CL et al. Pediatrics 2012
- Daftary AS et al. PSG Reference Values in Healthy Newborns. JCSM 2019
        """)

st.markdown("---")
st.markdown(
    "<div style='text-align:center;color:#94a3b8;font-size:0.75rem;'>"
    "AASM Pediatric Scoring Manual 2020 · ICSD-3</div>",
    unsafe_allow_html=True)

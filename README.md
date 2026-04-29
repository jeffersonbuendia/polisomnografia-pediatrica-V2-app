# 🫁 Polisomnografía Pediátrica — Calculadora Clínica

Calculadora clínica con impresión integrada para informes de polisomnografía pediátrica.

---

## Características

- Ingreso estructurado de todos los parámetros PSG pediátricos
- Cálculo automático de IAH, eficiencia del sueño y derivados
- Clasificación automática de severidad (AASM Pediatric Scoring Manual 2020)
- Generación automática de **impresión clínica integrada** en texto formal
- Descarga del reporte como `.html` (imprimible como PDF desde el navegador) y `.doc` (Word)
- Soporte para titulación CPAP/BPAP, capnografía y movimientos periódicos

## Secciones del reporte

| Sección | Contenido |
|---|---|
| I. Técnica | TRT, TST, SE% |
| II. Arquitectura | SOL, RLAT, WASO, estadios N1–N3–REM |
| III. Respiratorio | IAO, IAC, IAM, IH, **IAH**, IDR, SpO₂, capnografía |
| IV. Cardíaco | FC, arritmias |
| V. MPE | IMPE total y con arousal, piernas inquietas |
| VI. Arousal | IA total, respiratorio, espontáneo |
| VII. Parasomnias | Documentación de eventos |
| VIII. Titulación | CPAP/BPAP, presiones, IAH residual |
| **Resultado Formal** | **Impresión clínica integrada generada automáticamente** |

## Criterios diagnósticos

| Parámetro | Referencia |
|---|---|
| IAH normal pediátrico | < 1 /h |
| SAHOS Leve | IAH 1–5 /h |
| SAHOS Moderado | IAH 5–10 /h |
| SAHOS Grave | IAH > 10 /h |
| Eficiencia del sueño normal | ≥ 85% |
| MPE normales | < 5 /h |
| Hipoventilación | EtCO₂ > 50 mmHg por > 25% del TST |

> **Fuente:** AASM Pediatric Scoring Manual 2020 · ICSD-3 · Marcus et al. NEJM 2013

## Validación externa

Validada contra 6 casos de literatura indexada (Marcus 1992, CHAT Trial NEJM 2013, Frontiers Sleep 2023, Toma Pediatr Pulmonol 2025, Daftary JCSM 2019). Concordancia 5/6 (83%). La única discordancia corresponde a neonatos <6 meses, para quienes los umbrales AASM 2020 no aplican por diseño.

## Instalación local

```bash
git clone https://github.com/TU_USUARIO/psg-pediatrica.git
cd psg-pediatrica
pip install -r requirements.txt
streamlit run app.py
```

## Despliegue en Streamlit Cloud

1. Sube este repositorio a GitHub
2. Ve a [share.streamlit.io](https://share.streamlit.io)
3. Conecta tu cuenta de GitHub → selecciona el repositorio → `app.py`
4. Haz clic en **Deploy**

## Estructura

```
psg-pediatrica/
├── app.py
├── requirements.txt
├── README.md
└── .streamlit/
    └── config.toml
```

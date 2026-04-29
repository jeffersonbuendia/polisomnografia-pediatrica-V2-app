# 🫁 Polisomnografía Pediátrica — Calculadora Clínica

**Calculadora clínica con impresión integrada para informes de polisomnografía pediátrica.**

Desarrollado para el Laboratorio de Función Pulmonar — **Salud Es Vivir IPS**

---

## Características

- ✅ Ingreso estructurado de todos los parámetros PSG pediátricos
- ✅ Cálculo automático de IAH, eficiencia del sueño y derivados
- ✅ Clasificación automática de severidad (AASM Pediatric Scoring Manual 2020)
- ✅ Generación automática de **impresión clínica integrada** en texto formal
- ✅ Descarga del reporte en `.txt` listo para imprimir o copiar a historia clínica
- ✅ Soporte para titulación CPAP/BPAP, capnografía y movimientos periódicos
- ✅ Sin dependencias externas complejas — solo Streamlit

## Secciones del reporte

| Sección | Contenido |
|---------|-----------|
| I. Técnica | TRT, TST, SE%, observaciones |
| II. Arquitectura | SOL, RLAT, WASO, estadios N1-N2-N3-REM |
| III. Respiratorio | IAO, IAC, IAM, IH, IAH, IDR, SpO₂, capnografía |
| IV. Cardíaco | FC media/mín/máx, arritmias |
| V. MPE | IMPE total y con arousal, piernas inquietas |
| VI. Arousal | IA total, respiratorio, espontáneo |
| VII. Parasomnias | Documentación de eventos |
| VIII. Titulación | CPAP/BPAP presiones óptimas, IAH residual |
| **RESULTADO FORMAL** | **Impresión clínica integrada generada automáticamente** |

## Criterios diagnósticos

| Parámetro | Valor de referencia |
|-----------|-------------------|
| IAH normal pediátrico | < 1 /h |
| SAHOS Leve | IAH 1–5 /h |
| SAHOS Moderado | IAH 5–10 /h |
| SAHOS Grave | IAH > 10 /h |
| Eficiencia del sueño | ≥ 85% |
| MPE normales | < 5 /h |
| Hipoventilación | EtCO₂ > 50 mmHg por > 25% del TST |

> **Fuente:** AASM Pediatric Scoring Manual 2020 · ICSD-3 · Marcus et al. Pediatrics 2012

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
3. Conecta tu cuenta de GitHub
4. Selecciona este repositorio → `app.py` como archivo principal
5. Haz clic en **Deploy**

## Estructura del repositorio

```
psg-pediatrica/
├── app.py                  ← Aplicación principal
├── requirements.txt        ← Dependencias (solo streamlit)
├── README.md               ← Este archivo
└── .streamlit/
    └── config.toml         ← Tema visual (azul clínico)
```

## Nota clínica

> La interpretación clínica, el diagnóstico definitivo y las decisiones terapéuticas son responsabilidad **exclusiva del médico tratante**. Esta herramienta genera texto de soporte basado en los parámetros ingresados y no reemplaza el juicio clínico.

---

**Autor:** Laboratorio de Función Pulmonar — Salud Es Vivir IPS  
**Especialidad:** Neumología Pediátrica  
**Licencia:** Uso clínico institucional

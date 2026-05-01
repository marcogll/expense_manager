# PRD — Talia & C.A.R.O.L.
### Ecosistema Contable AI en Telegram · *Second Brain*

> **C.A.R.O.L.** = **C**lasificadora **A**utónoma de **R**egistros y **O**peraciones de **L**ibros

---

## 1. Resumen del Proyecto

**Visión:** Convertir un grupo de Telegram (Second Brain) en un ecosistema contable automatizado e inteligente. El sistema permite al usuario enviar tickets, facturas, audios o textos. La IA extrae, clasifica y almacena la información financiera — ingresos y gastos — tanto a nivel personal como de negocio, eliminando la fricción de la contabilidad manual.

### Personajes del Sistema

| Personaje | Rol | Responsabilidad |
|-----------|-----|-----------------|
| **Talia** | Bot Principal / Contadora Oficial | Interfaz de Telegram: comunicación directa, reportes, recordatorios y respuestas financieras. |
| **C.A.R.O.L.** | Módulo Asistente de Registro | Motor interno. Procesa archivos, ejecuta OCR, estructura el JSON, clasifica transacciones y dispara los webhooks hacia n8n. |

---

## 2. Objetivos del Producto

- **Automatización de Captura** — Reducir a cero el tiempo de captura manual de tickets y facturas.
- **Clasificación Inteligente** — Categorizar automáticamente entre gastos *Personales* y de *Negocio*, asignando subcategorías detalladas por ítem.
- **Aprendizaje Continuo** — Mejorar la precisión de clasificación a partir de correcciones del usuario.
- **Visibilidad Financiera** — Proveer reportes semanales claros y proactivos sobre el estado financiero.

---

## 3. Casos de Uso y Flujo de Usuario

### 3.1 Captura de Gastos / Ingresos

```
Usuario  ──►  Topic #4 de Telegram  ──►  Talia  ──►  C.A.R.O.L.  ──►  n8n / Sheets
                 (foto, PDF, audio,           "Recibido,    (OCR + JSON)
                  texto libre)                procesando…")
```

1. **Actor:** Usuario.
2. **Acción:** Envía al Topic #4 un mensaje, foto de ticket, PDF de factura o nota de voz.
3. **Talia responde:** *"Recibido. C.A.R.O.L. está procesando el documento…"*
4. **C.A.R.O.L. procesa:** OCR → extracción → estructurado del JSON → webhook a n8n.
5. **Confirmación de Talia:** *"He registrado un gasto de $850 en Ferretería El Norte bajo Negocio › Refacciones. ¿Todo correcto?"*
6. **Ajuste (si aplica):** El usuario corrige; C.A.R.O.L. actualiza la BD, envía el ajuste a n8n y guarda la excepción para aprendizaje futuro.

### 3.2 Recordatorios Diarios

- **Actora:** Talia.
- **Horario:** 09:00 AM y 05:00 PM (hora local, vía CRON).
- **Ejemplo:** *"¡Hola! Son las 5:00 PM. ¿Tienes algún ticket, factura o compra del día que C.A.R.O.L. deba registrar?"*

### 3.3 Reportes Semanales

- **Actoras:** Talia + C.A.R.O.L.
- **Cuándo:** Domingos por la noche o Lunes por la mañana.
- **Contenido:**
  - Total de gastos e ingresos del período.
  - División macro: Personal vs. Negocio.
  - Desglose por subcategorías (Gasolina, Comida, Refacciones, etc.).

---

## 4. Requerimientos Funcionales

### 4.1 Ingreso de Datos — Telegram Bot API

| Formato | Tipo MIME / Descripción |
|---------|------------------------|
| Imágenes | JPG, PNG |
| Documentos | PDF |
| Texto plano | Mensajes de chat |
| Audio | Notas de voz (OGG/MP3) |

> **Nota:** Soporte completo para foros de Telegram (`message_thread_id` configurable; default `4`).

### 4.2 Extracción de Datos — C.A.R.O.L. + OpenAI Vision/NLP

C.A.R.O.L. extraerá los siguientes campos cuando estén disponibles:

- Nombre del local / Tienda
- RFC del emisor
- Razón Social
- Dirección completa
- Fecha y hora de la transacción
- Monto total + desglose de impuestos (IVA, IEPS, etc.)
- **Matriz de ítems:** descripción, cantidad, precio unitario

### 4.3 Motor de Clasificación — C.A.R.O.L.

La clasificación opera **a nivel de factura general** y **a nivel de cada ítem**.

**Tipo Macro**

| Categoría | Subcategorías |
|-----------|--------------|
| **Personal** | Alimentos · Transporte · Vivienda · Salud · Entretenimiento · Educación · Impuestos · Servicios |
| **Negocio** | Gasolina · Refacciones · Publicidad/Marketing · Papelería · Vestimenta · Renta · Software · Viajes · Servicios Profesionales |

### 4.4 Estructura de Salida — JSON hacia Webhook

```json
{
  "system": {
    "interface": "Talia",
    "processor": "C.A.R.O.L.",
    "timestamp": "2026-05-01T17:22:00Z"
  },
  "transaction": {
    "type": "expense",
    "store_name": "Ferretería El Norte",
    "rfc": "XAXX010101000",
    "legal_name": "Ferretería El Norte SA de CV",
    "address": "Calle Falsa 123, Saltillo, Coah.",
    "date": "2026-05-01",
    "total_amount": 850.00,
    "classification": {
      "macro": "Negocio",
      "confidence_score": 0.95
    },
    "items": [
      {
        "description": "Martillo de acero",
        "qty": 1,
        "unit_price": 350.00,
        "subcategory": "Refacciones"
      }
    ]
  }
}
```

### 4.5 Integración con n8n

- C.A.R.O.L. realiza peticiones `POST` autenticadas a la URL del webhook de n8n.
- n8n mapea el JSON e inserta las filas correspondientes en **Google Sheets** o la base de datos configurada.
- El secreto del webhook se gestiona como variable de entorno (`N8N_WEBHOOK_SECRET`).

### 4.6 Lógica de Recordatorios y Reportes — CRON Jobs

- Recordatorios diarios (09:00 y 17:00 hrs) implementados con **APScheduler**.
- Reporte semanal: C.A.R.O.L. consulta la BD local (o la API de Sheets vía n8n) y genera el resumen que Talia envía al Topic.

---

## 5. Arquitectura Técnica

```
┌─────────────────────────────────────────────────────┐
│                  Telegram (Topic #4)                │
│          Talia Bot  ←──────────────────►  Usuario   │
└─────────────────────────────┬───────────────────────┘
                              │
                    ┌─────────▼──────────┐
                    │    C.A.R.O.L.      │
                    │  (Python Backend)  │
                    │                   │
                    │  OpenAI GPT-4o    │
                    │  OCR · NLP · JSON │
                    │  APScheduler      │
                    │  SQLite / SQLAlch │
                    └─────────┬──────────┘
                              │  POST (JSON)
                    ┌─────────▼──────────┐
                    │        n8n         │
                    │  (Orquestador)     │
                    └─────────┬──────────┘
                              │
                    ┌─────────▼──────────┐
                    │   Google Sheets /  │
                    │   Base de Datos    │
                    └────────────────────┘
```

### Stack Principal

| Capa | Tecnología |
|------|-----------|
| Lenguaje | Python 3.10+ |
| Telegram | `python-telegram-bot` |
| IA / Visión | `openai` (GPT-4o) |
| Webhooks | `requests` |
| CRON | `apscheduler` |
| Base de datos local | `sqlite3` / `SQLAlchemy` |
| Orquestador de datos | n8n |
| Destino final | Google Sheets / Excel |
| Despliegue | VPS (DigitalOcean / AWS EC2 / Railway) |

---

## 6. Flujo de Aprendizaje — C.A.R.O.L. Learning Mode

C.A.R.O.L. implementa un aprendizaje basado en reglas guardadas en la BD local, sin necesidad de reentrenamiento del LLM.

```
1. REGISTRO INICIAL
   └─ Talia procesa "Starbucks" → C.A.R.O.L. guarda:
      { tienda: "Starbucks", macro: "Personal", sub: "Alimentos" }

2. NUEVA INGESTA
   └─ Llega ticket de Starbucks → C.A.R.O.L. busca en la BD.

3. PREDICCIÓN AUTOMÁTICA
   └─ Coincidencia encontrada → asigna "Personal / Alimentos"
      sin consultar al LLM (ahorra tokens y tiempo).

4. EXCEPCIÓN DEL USUARIO
   └─ "Esta vez Starbucks es Negocio (reunión de clientes)"
      → C.A.R.O.L. registra excepción puntual y la aplica
        solo a esa transacción, preservando la regla general.
```

---

## 7. Variables de Entorno Requeridas

```env
TELEGRAM_BOT_TOKEN=...
OPENAI_API_KEY=...
N8N_WEBHOOK_URL=https://tu-n8n.com/webhook/carol
N8N_WEBHOOK_SECRET=...
TOPIC_ID=4
TZ=America/Monterrey
```

---

## 8. Roadmap Sugerido

| Fase | Entregable | Estado |
|------|-----------|--------|
| **v0.1** | Bot básico de Telegram + respuesta de Talia | ⬜ Pendiente |
| **v0.2** | Integración OCR con GPT-4o + JSON estructurado | ⬜ Pendiente |
| **v0.3** | Webhook hacia n8n + escritura en Sheets | ⬜ Pendiente |
| **v0.4** | CRONs de recordatorios (09:00 / 17:00) | ⬜ Pendiente |
| **v0.5** | Motor de aprendizaje (BD local de reglas) | ⬜ Pendiente |
| **v1.0** | Reporte semanal automático + ajustes del usuario | ⬜ Pendiente |

---

*Documento generado para el repositorio `expense_manager` · [github.com/marcogll/expense_manager](https://github.com/marcogll/expense_manager)*

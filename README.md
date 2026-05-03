<div align="center">

<img src="https://soul23.mx/logo/soul23_logo.svg" width="90" alt="Soul23">

# Expense Manager

Expense management system with AI receipt processing and Telegram integration 💰

<p>
  <img src="https://img.shields.io/badge/Python-111111?style=flat-square&logo=python&logoColor=white" alt="Python">
  <img src="https://img.shields.io/badge/OpenAI-111111?style=flat-square&logo=openai&logoColor=white" alt="OpenAI">
</p>

</div>

---

### Ecosistema Contable AI · Telegram Second Brain

> **C.A.R.O.L.** = **C**aptura y **A**nálisis de **R**ecibos con **O**rganización de **L**ibros

Convierte tu grupo de Telegram en una contadora personal automatizada. Envía una foto de tu ticket, una nota de voz o un PDF — Talia confirma, C.A.R.O.L. procesa, n8n registra.

```
Usuario → [foto / audio / PDF / texto] → Talia → C.A.R.O.L. → n8n → Google Sheets
```

---

## ✨ ¿Qué hace cada quién?

| | Talia | C.A.R.O.L. |
|---|---|---|
| **Rol** | Contadora oficial · interfaz de Telegram | Motor interno · procesadora de documentos |
| **Hace** | Recibe mensajes, confirma registros, envía reportes y recordatorios | OCR, extracción, clasificación, webhook a n8n |
| **Habla con** | El usuario | n8n / Google Sheets / BD local |

---

## ⚙️ Variables de Entorno

```env
# .env.example
TELEGRAM_BOT_TOKEN=
TELEGRAM_CHAT_ID=
TELEGRAM_USER_ID=
LLM_PROVIDER=openai
OPENAI_API_KEY=
OPENROUTER_API_KEY=
OPENROUTER_BASE_URL=https://openrouter.ai/api/v1
OPENROUTER_MODEL=openai/gpt-4o
N8N_WEBHOOK_URL=https://tu-n8n.com/webhook/carol
N8N_WEBHOOK_SECRET=
TOPIC_ID=4
TZ=America/Monterrey
DATABASE_URL=sqlite:///carol.db
CLASSIFICATION_CONFIDENCE_THRESHOLD=0.85
```

---

## 🗂️ Estructura del Proyecto

```
expense_manager/
├── main.py                  # Entry point · inicializa Talia + scheduler
├── talia/
│   ├── bot.py               # Handlers de Telegram
│   └── messages.py          # Plantillas de respuesta
├── carol/
│   ├── processor.py         # Orquesta el flujo de C.A.R.O.L.
│   ├── ocr.py               # Extracción via GPT-4o Vision
│   ├── classifier.py        # Motor Personal / Negocio
│   ├── learner.py           # Reglas y excepciones
│   └── schemas.py           # Modelos Pydantic del JSON estándar
├── integrations/
│   └── n8n.py               # Cliente webhook
├── db/
│   ├── models.py            # SQLAlchemy models
│   └── session.py           # Configuración de BD
├── scheduler/
│   └── jobs.py              # CRONs de recordatorios y reporte semanal
├── .env.example
├── requirements.txt
└── README.md
```

---

## 📦 Dependencias

```txt
python-telegram-bot>=21.0
openai>=1.0
requests
apscheduler
sqlalchemy
pypdf
pydantic
loguru
python-dotenv
```

---

## 🚀 Inicio Rápido

```bash
git clone https://github.com/marcogll/expense_manager.git
cd expense_manager
cp .env.example .env        # Llena tus credenciales
pip install -r requirements.txt
python main.py
```

---

*Talia habla. C.A.R.O.L. trabaja. Tú solo envías el ticket.*

# 📋 TASKS — Implementación en 24 Horas
### `expense_manager` · Talia & C.A.R.O.L.

---

## Bloque 1 · Horas 0–4 · Fundación
> El bot vive, escucha y responde.

- [ ] Crear bot en @BotFather y guardar `TELEGRAM_BOT_TOKEN`
- [ ] Configurar repo, `.env` y `requirements.txt`
- [ ] Instalar dependencias base (`python-telegram-bot`, `openai`, `python-dotenv`, `loguru`)
- [ ] Handler básico: bot escucha mensajes en Topic #4 (`message_thread_id`)
- [ ] Talia responde: *"Recibido. C.A.R.O.L. está procesando…"*
- [ ] Deploy en VPS — bot corriendo 24/7

**✅ Checkpoint:** Talia responde en Telegram al recibir cualquier mensaje.

---

## Bloque 2 · Horas 4–10 · Motor C.A.R.O.L.
> C.A.R.O.L. lee, entiende y estructura.

- [ ] Handler para imágenes (JPG / PNG) → descarga y codifica en base64
- [ ] Handler para PDFs → extracción de texto con `pypdf`
- [ ] Handler para notas de voz → transcripción con `openai.audio.transcriptions`
- [ ] Prompt de sistema para GPT-4o Vision: extrae tienda, RFC, fecha, total, ítems
- [ ] Parsear respuesta del LLM al JSON estándar de C.A.R.O.L.
- [ ] Motor de clasificación: Personal vs. Negocio + subcategoría por ítem
- [ ] Campo `confidence_score` (umbral configurable, default `0.85`)

**✅ Checkpoint:** Foto de ticket → JSON correcto impreso en consola.

---

## Bloque 3 · Horas 10–14 · Base de Datos y Aprendizaje
> C.A.R.O.L. recuerda y mejora.

- [ ] Inicializar SQLite con SQLAlchemy (tablas: `transactions`, `store_rules`, `exceptions`)
- [ ] Antes de llamar al LLM: buscar tienda en `store_rules`
- [ ] Si hay match → usar regla guardada (sin gastar tokens)
- [ ] Si no hay match → usar LLM y guardar resultado como nueva regla
- [ ] Handler de corrección del usuario: *"No, es Personal"* → C.A.R.O.L. actualiza la BD
- [ ] Guardar excepciones puntuales sin borrar la regla general

**✅ Checkpoint:** Segunda foto del mismo comercio se clasifica sin llamar al LLM.

---

## Bloque 4 · Horas 14–18 · Integración n8n → Google Sheets
> Los datos llegan a la hoja de cálculo.

- [ ] Crear workflow en n8n con trigger `Webhook POST /carol`
- [ ] Mapear JSON → columnas en hoja `Gastos` (fecha, tienda, total, macro, subcategoría, confianza)
- [ ] Mapear ítems → hoja `Ítems` (desglose por producto)
- [ ] Implementar `send_to_n8n()` en Python con header de autenticación
- [ ] Reintentos automáticos (3 intentos, backoff exponencial) si n8n no responde
- [ ] Talia confirma al usuario tras éxito: *"✅ $850 · Ferretería El Norte · Negocio › Refacciones"*

**✅ Checkpoint:** Ticket enviado por Telegram aparece como fila nueva en Google Sheets.

---

## Bloque 5 · Horas 18–21 · Recordatorios y Reporte Semanal
> Talia trabaja sola aunque el usuario no pregunte.

- [ ] Configurar APScheduler con zona horaria `America/Monterrey`
- [ ] CRON 09:00 AM → recordatorio matutino en Topic #4
- [ ] CRON 05:00 PM → recordatorio vespertino en Topic #4
- [ ] CRON Domingo 08:00 PM → C.A.R.O.L. consolida la semana:
  - [ ] Total gastos e ingresos
  - [ ] División Personal vs. Negocio
  - [ ] Top 3 subcategorías
- [ ] Validar que el scheduler no dispara duplicados al reiniciar el bot

**✅ Checkpoint:** Recordatorio llega a Telegram a la hora exacta sin intervención.

---

## Bloque 6 · Horas 21–24 · QA y Hardening
> Listo para producción real.

- [ ] Prueba end-to-end: imagen JPG · PDF · nota de voz · texto libre
- [ ] Prueba de corrección y verificación de aprendizaje en BD
- [ ] Logging estructurado con `loguru` — errores visibles desde VPS
- [ ] `.env.example` con todas las variables documentadas
- [ ] Configurar `systemd` service o `pm2` para auto-restart en VPS
- [ ] Primer ticket real registrado y verificado en Google Sheets

**✅ Checkpoint:** Sistema estable en producción. Sprint cerrado.

---

> Referencia de arquitectura y especificaciones completas en [`PRD_Talia_Carol.md`](./PRD_Talia_Carol.md)

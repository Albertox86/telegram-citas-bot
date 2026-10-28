# Telegram Citas Bot (Python)

Bot de Telegram en Python para responder en **español** sobre citas médicas.

## Objetivo
Cuando un usuario pide una cita por chat, el bot responde que:
- la cita se agenda **solo por teléfono**,
- muestra el número de contacto,
- opcionalmente muestra horario de atención.

## Arquitectura extensible
El proyecto está organizado para permitir agregar nuevos tipos de preguntas fácilmente:

- `bot/intents.py`
  - Motor de intents (`IntentEngine`)
  - Reglas de detección (`IntentRule`, `KeywordIntentRule`)
  - Hoy incluye `appointment_request`
- `bot/handlers.py`
  - Router de respuestas por intent
  - Para agregar una nueva pregunta: crear intent + respuesta y registrarla
- `bot/main.py`
  - Wiring del bot, comandos y polling

## Requisitos
- Python 3.11+
- Token de Telegram creado con `@BotFather`

## Configuración
1. Copia variables de entorno:

```bash
cp .env.example .env
```

2. Edita `.env` con tus datos reales:
- `BOT_TOKEN`
- `CLINIC_PHONE`
- `CLINIC_HOURS` (opcional)
- `EMERGENCY_TEXT` (opcional)

## Ejecución local
```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\\Scripts\\activate
pip install -r requirements.txt
python -m bot.main
```

## Tests
```bash
python -m unittest discover -s tests -p "test_*.py"
```

## Cómo agregar soporte para nuevas preguntas
1. En `bot/intents.py`, agrega una nueva regla con otro `intent_name`.
2. En `bot/handlers.py`, crea una función de respuesta para ese intent.
3. Registra ese intent en el diccionario `intent_responses`.
4. Agrega tests en `tests/`.

---
Si luego quieres, puedo agregar:
- despliegue con Docker,
- webhooks en lugar de polling,
- métricas de intents no reconocidos,
- soporte multi-idioma.

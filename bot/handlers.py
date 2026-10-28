from __future__ import annotations

from dataclasses import dataclass
from typing import Callable, Dict

from telegram import Update
from telegram.ext import ContextTypes

from .config import Settings
from .intents import IntentEngine


@dataclass(frozen=True)
class BotContext:
    settings: Settings
    intent_engine: IntentEngine


def build_router(ctx: BotContext) -> Callable[[Update, ContextTypes.DEFAULT_TYPE], str]:
    """Returns a pure routing function so behavior is easy to extend and test.

    Architecture note:
    - Add a new intent in `intents.py`
    - Add its responder function here
    - Register it in `intent_responses`
    """

    def appointment_response() -> str:
        phone = ctx.settings.clinic_phone
        hours = ctx.settings.clinic_hours
        emergency = ctx.settings.emergency_text

        lines = [
            "Para agendar una cita médica, solo atendemos por teléfono.",
            f"📞 Por favor llama al: {phone}",
        ]

        if hours:
            lines.append(f"🕒 Horario: {hours}")
        if emergency:
            lines.append(emergency)

        return "\n".join(lines)

    def fallback_response() -> str:
        return (
            "Gracias por tu mensaje. "
            "Si deseas agendar una cita, la gestión se realiza únicamente por teléfono.\n"
            f"📞 {ctx.settings.clinic_phone}"
        )

    intent_responses: Dict[str, Callable[[], str]] = {
        "appointment_request": appointment_response,
        "fallback": fallback_response,
    }

    def route(update: Update, _: ContextTypes.DEFAULT_TYPE) -> str:
        text = (update.message.text if update.message else "") or ""
        intent = ctx.intent_engine.detect(text)
        responder = intent_responses.get(intent.intent_name, fallback_response)
        return responder()

    return route


def start_message(ctx: BotContext) -> str:
    return (
        "Hola 👋 Soy el asistente de citas.\n"
        "Si quieres agendar una cita médica, te indicaré el número telefónico para hacerlo.\n\n"
        f"📞 Número de atención: {ctx.settings.clinic_phone}"
    )


def help_message(ctx: BotContext) -> str:
    hours_line = f"\n🕒 Horario: {ctx.settings.clinic_hours}" if ctx.settings.clinic_hours else ""
    return (
        "Puedo ayudarte con información para agendar citas.\n"
        "La agenda se realiza solo por teléfono.\n"
        f"📞 {ctx.settings.clinic_phone}{hours_line}"
    )

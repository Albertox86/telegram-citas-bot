from dataclasses import dataclass
import os


@dataclass(frozen=True)
class Settings:
    bot_token: str
    clinic_phone: str
    clinic_hours: str
    emergency_text: str


def load_settings() -> Settings:
    bot_token = os.getenv("BOT_TOKEN", "")
    clinic_phone = os.getenv("CLINIC_PHONE", "")
    clinic_hours = os.getenv("CLINIC_HOURS", "")
    emergency_text = os.getenv("EMERGENCY_TEXT", "")

    if not bot_token:
        raise ValueError("Missing BOT_TOKEN environment variable")
    if not clinic_phone:
        raise ValueError("Missing CLINIC_PHONE environment variable")

    return Settings(
        bot_token=bot_token,
        clinic_phone=clinic_phone,
        clinic_hours=clinic_hours,
        emergency_text=emergency_text,
    )

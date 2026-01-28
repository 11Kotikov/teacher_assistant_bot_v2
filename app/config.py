import os
from pathlib import Path
from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent.parent
ENV_PATH = BASE_DIR / ".env"

load_dotenv(dotenv_path=ENV_PATH)


class Config:
    BOT_TOKEN: str | None = os.getenv("BOT_TOKEN")
    LOG_LEVEL: str = os.getenv("LOG_LEVEL", "INFO")

    _teacher_id = os.getenv("TEACHER_TELEGRAM_ID")
    TEACHER_TELEGRAM_ID: int | None = (
        int(_teacher_id) if _teacher_id and _teacher_id.isdigit() else None
    )


def validate_config() -> None:
    if not Config.BOT_TOKEN:
        raise RuntimeError("❌ BOT_TOKEN not found in .env file")

    if Config.TEACHER_TELEGRAM_ID is None:
        raise RuntimeError("❌ TEACHER_TELEGRAM_ID not found or invalid in .env file")


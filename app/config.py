import os
from pathlib import Path
from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent.parent
ENV_PATH = BASE_DIR / ".env"

load_dotenv(dotenv_path=ENV_PATH)


class Config:
    BOT_TOKEN: str | None = os.getenv("BOT_TOKEN")
    LOG_LEVEL: str = os.getenv("LOG_LEVEL", "INFO")


def validate_config() -> None:
    if not Config.BOT_TOKEN:
        raise RuntimeError("BOT_TOKEN not found in .env file")

from __future__ import annotations
import os
from dataclasses import dataclass
from dotenv import load_dotenv

load_dotenv()

@dataclass(frozen=True)
class Settings:
    api_key: str
    api_secret: str
    base_url: str = "https://live.trading212.com"

def get_settings() -> Settings:
    api_key = os.getenv("API_KEY", "").strip()
    api_secret = os.getenv("API_SECRET", "").strip()
    missing = [name for name, value in (("API_KEY", api_key), ("API_SECRET", api_secret)) if not value]
    if missing:
        raise RuntimeError(f"Variáveis de ambiente obrigatórias em falta: {', '.join(missing)}")
    return Settings(api_key=api_key, api_secret=api_secret)

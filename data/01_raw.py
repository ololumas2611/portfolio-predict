"""Extract dividend history from Trading 212 into a CSV file."""
from __future__ import annotations
import time
from pathlib import Path
from typing import Any
import requests
from requests.auth import HTTPBasicAuth
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
from core.settings import Settings, get_settings
from service.csv_service import write_csv

DIVIDENDS_PATH = "/api/v0/equity/history/dividends"
FIELDS = ("currency", "amountInEuro", "paidOn", "type", "grossAmountPerShare", "reference", "quantity", "ticker", "name", "isin", "amount")

def extract_header(items: list[dict[str, Any]]) -> list[str]:

    instrument_fields: list[str] = []

    for item in items:
        for key in (item.get("instrument") or {}):
            if key not in instrument_fields:
                instrument_fields.append(key)
                
    return instrument_fields + [field for field in FIELDS if field not in instrument_fields]

def get_values(items: list[dict[str, Any]], header: list[str]) -> list[list[Any]]:
    return [[(item.get("instrument") or {}).get(field, item.get(field)) for field in header] for item in items]

def get_data(output: str | Path = "output/dividends.csv", settings: Settings | None = None, session: requests.Session | None = None, pause_seconds: float = 1.0) -> list[dict[str, Any]]:

    settings = settings or get_settings()
    client = session or requests.Session()

    if session is None:
        retry = Retry(total=3, backoff_factor=1, status_forcelist=(429, 500, 502, 503, 504), allowed_methods=("GET",))
        client.mount("https://", HTTPAdapter(max_retries=retry))

    auth = HTTPBasicAuth(settings.api_key, settings.api_secret)
    items: list[dict[str, Any]] = []
    next_path: str | None = DIVIDENDS_PATH

    while next_path:
        response = client.get(f"{settings.base_url}{next_path}", auth=auth, timeout=(5, 30))
        response.raise_for_status()
        payload = response.json()
        page = payload.get("items", [])

        if not isinstance(page, list):
            raise ValueError("Resposta inválida da API: 'items' deve ser uma lista")
        items.extend(page)
        next_path = payload.get("nextPagePath")

        if next_path:
            time.sleep(pause_seconds)

    header = extract_header(items)
    write_csv(header, get_values(items, header), output)
    print(f"{len(items)} dividendos extraídos com sucesso para {output}")
    return items

if __name__ == "__main__":
    get_data()

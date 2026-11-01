

from __future__ import annotations
import csv
from pathlib import Path
from typing import Iterable, Sequence


def write_csv(header: Sequence[object], rows: Iterable[Sequence[object]], filename: str | Path) -> None:
    path = Path(filename)
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(path.suffix + ".tmp")
    try:
        with temporary.open("w", newline="", encoding="utf-8") as file:
            writer = csv.writer(file)
            writer.writerow(header)
            writer.writerows(rows)
        temporary.replace(path)
    except Exception:
        temporary.unlink(missing_ok=True)
        raise

def append_csv(rows: Iterable[Sequence[object]], filename: str | Path) -> None:
    path = Path(filename)
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", newline="", encoding="utf-8") as file:
        csv.writer(file).writerows(rows)

def to_csv(fields: Iterable[Sequence[object]], filename: str | Path) -> None:
    append_csv(fields, filename)

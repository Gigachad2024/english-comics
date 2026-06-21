"""Load canonical dialogues from data/canonical-dialogues.json."""

from __future__ import annotations

import json
from functools import lru_cache
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent
CANONICAL_PATH = ROOT / "data" / "canonical-dialogues.json"


@lru_cache(maxsize=1)
def load_canonical_map() -> dict[str, list[dict]]:
    if not CANONICAL_PATH.exists():
        return {}
    data = json.loads(CANONICAL_PATH.read_text(encoding="utf-8"))
    out: dict[str, list[dict]] = {}
    for key, ep in (data.get("episodes") or {}).items():
        lines = ep.get("lines") or []
        if lines:
            out[key] = lines
    return out


def get_canonical_lines(series_id: str, ep_num: int) -> list[dict] | None:
    return load_canonical_map().get(f"{series_id}/{ep_num}")

#!/usr/bin/env python3
"""Merge phrasal verbs expansion (119–210) into core.json and canonical-overrides.json."""

from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))

from phrasal_verbs_expansion import (  # noqa: E402
    EPISODE_COUNT,
    PHRASAL_DIALOGUES,
    PHRASAL_PACKS,
    PHRASAL_SERIES,
)


def merge_core(path: Path) -> None:
    data = json.loads(path.read_text(encoding="utf-8"))
    existing_ids = {p["id"] for p in data["packs"]}
    added = 0
    for pack in PHRASAL_PACKS:
        if pack["id"] not in existing_ids:
            data["packs"].append(pack)
            added += 1

    arc_entries = []
    for s in PHRASAL_SERIES:
        nums = [n for n, _, _ in s["episodes"]]
        arc_entries.append({
            "id": s["id"].replace("-", "_") + "_arc",
            "title": s["title"],
            "focus": [s["desc"].split("—")[0].strip() if "—" in s["desc"] else s["desc"]],
            "episodeRange": f"{min(nums)}-{max(nums)}",
        })

    existing_arc_ids = {a["id"] for a in data["arcs"]}
    arcs_added = 0
    for arc in arc_entries:
        if arc["id"] not in existing_arc_ids:
            data["arcs"].append(arc)
            arcs_added += 1

    path.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"{path.name}: +{added} packs, +{arcs_added} arcs")


def merge_overrides() -> None:
    path = ROOT / "data" / "canonical-overrides.json"
    data = json.loads(path.read_text(encoding="utf-8"))
    overrides = data.get("overrides", data)
    added = 0
    for key, lines in PHRASAL_DIALOGUES.items():
        if key not in overrides:
            overrides[key] = lines
            added += 1
    data["overrides"] = overrides
    path.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"canonical-overrides.json: +{added} episodes ({EPISODE_COUNT} total in expansion)")


def main() -> None:
    merge_core(ROOT / "data" / "core.json")
    merge_core(ROOT / "english_vault_website_core.json")
    merge_overrides()


if __name__ == "__main__":
    main()

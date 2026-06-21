#!/usr/bin/env python3
"""Build data/canonical-dialogues.json from comic PNGs (OCR) + script hints."""

from __future__ import annotations

import json
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))

from comic_dialogue.ocr_extract import pick_best_dialogue  # noqa: E402
from comic_dialogue.schema import validate_episode_dialogue  # noqa: E402
from comic_dialogue.sources import load_all_script_hints, load_comics  # noqa: E402

OUT = ROOT / "data" / "canonical-dialogues.json"
OVERRIDES = ROOT / "data" / "canonical-overrides.json"


def load_overrides() -> dict[str, list[dict]]:
    if OVERRIDES.exists():
        data = json.loads(OVERRIDES.read_text(encoding="utf-8"))
        return data.get("overrides") or data
    return {}


def merge_ocr_and_hint(ocr_lines: list[dict], hint_lines: list[dict]) -> list[dict]:
    """Prefer OCR text; use hint for speaker when OCR lacks prefix."""
    if not ocr_lines and hint_lines:
        return hint_lines[:6]
    if not hint_lines:
        return ocr_lines[:6]

    merged: list[dict] = []
    for i in range(6):
        panel = i + 1
        ocr = next((x for x in ocr_lines if x.get("panel") == panel), None)
        hint = next((x for x in hint_lines if x.get("panel") == panel), None)
        if not hint and i < len(hint_lines):
            hint = hint_lines[i]
        if not ocr and not hint:
            continue
        if ocr and hint:
            merged.append({
                "panel": panel,
                "speaker": ocr.get("speaker") or hint.get("speaker") or "Nam",
                "text": ocr.get("text") or hint.get("text", ""),
            })
        elif ocr:
            merged.append({**ocr, "panel": panel})
        elif hint:
            merged.append({**hint, "panel": panel})
    return merged[:6]


def main() -> None:
    comics = load_comics()
    hints = load_all_script_hints(comics)
    overrides = load_overrides()

    episodes: dict[str, dict] = {}
    stats = {"ocr_ok": 0, "override": 0, "weak": 0, "errors": 0}

    for series in comics["series"]:
        sid = series["id"]
        for ep in series["episodes"]:
            key = f"{sid}/{ep['num']}"
            img_rel = ep.get("image", "")
            img_path = ROOT / img_rel if img_rel else None
            hint = hints.get(key, [])

            if key in overrides:
                lines = overrides[key]
                source = "override"
                verify_score = 1.0
                stats["override"] += 1
            elif img_path and img_path.exists():
                lines, source, verify_score = pick_best_dialogue(img_path, hint)
                verify_score = round(verify_score, 3)
                if source == "script+verified" and len(lines) >= 6:
                    stats["ocr_ok"] += 1
                elif verify_score >= 0.55 and len(lines) >= 6:
                    stats["ocr_ok"] += 1
                else:
                    stats["weak"] += 1
            else:
                lines = hint[:6]
                source = "script-only"
                verify_score = None
                stats["weak"] += 1

            errs = validate_episode_dialogue(lines)
            if errs:
                stats["errors"] += 1

            episodes[key] = {
                "seriesId": sid,
                "num": ep["num"],
                "slug": ep.get("slug", ""),
                "title": ep.get("title", ""),
                "image": img_rel,
                "source": source,
                "verifyScore": verify_score if img_path and img_path.exists() else None,
                "errors": errs,
                "lines": lines,
            }

    payload = {
        "version": 1,
        "generatedAt": datetime.now(timezone.utc).isoformat(),
        "count": len(episodes),
        "stats": stats,
        "episodes": episodes,
    }
    OUT.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"Wrote {OUT} — {len(episodes)} episodes")
    print(f"  OCR verified: {stats['ocr_ok']}, overrides: {stats['override']}, weak: {stats['weak']}, errors: {stats['errors']}")


if __name__ == "__main__":
    main()

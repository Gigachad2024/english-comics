#!/usr/bin/env python3
"""Validate dialogue sync: canonical ↔ prompts ↔ guides ↔ images."""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))

from comic_dialogue.ocr_extract import verify_image_matches_dialogue  # noqa: E402
from comic_dialogue.schema import normalize_text  # noqa: E402
from comic_dialogue.sources import parse_prompt_md  # noqa: E402

CANONICAL = ROOT / "data" / "canonical-dialogues.json"
GUIDES = ROOT / "data" / "episode-guides.json"
PROMPTS = ROOT / "prompts"


def main() -> int:
    canonical = json.loads(CANONICAL.read_text(encoding="utf-8"))
    guides = json.loads(GUIDES.read_text(encoding="utf-8"))["guides"]
    errors: list[str] = []

    for key, ep in canonical["episodes"].items():
        lines = ep.get("lines") or []
        if ep.get("errors"):
            errors.append(f"{key}: canonical validation {ep['errors']}")

        img = ROOT / ep.get("image", "")
        if img.exists() and lines:
            ok, score = verify_image_matches_dialogue(img, lines, threshold=0.5)
            if not ok:
                errors.append(f"{key}: image verify failed score={score:.2f}")

        sid, num = key.split("/")
        prompt_path = PROMPTS / f"{sid}-t{int(num):02d}-comic.md"
        prompt_lines = parse_prompt_md(prompt_path)
        canon_norm = [normalize_text(x["text"]) for x in lines]
        prompt_lines = parse_prompt_md(prompt_path)
        prompt_norm = [normalize_text(x["text"]) for x in prompt_lines[: len(canon_norm)]]
        if canon_norm and prompt_norm != canon_norm[: len(canon_norm)]:
            errors.append(f"{key}: prompt mismatch")

        guide = guides.get(key, {})
        guide_norm = [normalize_text(x.get("en", "")) for x in guide.get("dialogueLines") or []]
        if canon_norm and guide_norm[: len(canon_norm)] != canon_norm:
            errors.append(f"{key}: guide mismatch")

    print(f"Checked {len(canonical['episodes'])} episodes")
    if errors:
        print(f"FAILED: {len(errors)} issues")
        for e in errors[:40]:
            print(f"  - {e}")
        if len(errors) > 40:
            print(f"  ... +{len(errors)-40} more")
        return 1
    print("OK — canonical, prompts, guides, and images aligned")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

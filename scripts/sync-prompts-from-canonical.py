#!/usr/bin/env python3
"""Rewrite prompt markdown dialogue from data/canonical-dialogues.json."""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))

CANONICAL = ROOT / "data" / "canonical-dialogues.json"
PROMPTS = ROOT / "prompts"


def update_prompt_file(path: Path, lines: list[dict], title: str) -> None:
    if not path.exists():
        return
    content = path.read_text(encoding="utf-8")

    panels_md = "\n".join(
        f'- **Panel {ln["panel"]}:** Scene. Dialogue: {ln["speaker"]}: "{ln["text"]}"'
        for ln in lines
    )
    panels_prompt = "\n".join(
        f'Panel {ln["panel"]}: Story beat. Speech: {ln["speaker"]}: "{ln["text"]}"'
        for ln in lines
    )

    if "## Story beats" in content:
        content = re.sub(
            r"## Story beats\n\n.*?\n\n---",
            f"## Story beats\n\n{panels_md}\n\n---",
            content,
            count=1,
            flags=re.S,
        )

    if "PANEL STORY:" in content:
        content = re.sub(
            r"PANEL STORY:\n.*?(?=\nENGLISH FOCUS box must list:)",
            f"PANEL STORY:\n{panels_prompt}\n",
            content,
            count=1,
            flags=re.S,
        )

    # Canonical block for tooling
    canon_block = (
        "## Canonical dialogue (synced from image — do not edit by hand)\n\n"
        "```json\n"
        + json.dumps(lines, indent=2, ensure_ascii=False)
        + "\n```\n\n---\n\n"
    )
    if "## Canonical dialogue" in content:
        content = re.sub(
            r"## Canonical dialogue \(synced from image — do not edit by hand\)\n\n```json\n.*?\n```",
            "## Canonical dialogue (synced from image — do not edit by hand)\n\n```json\n"
            + json.dumps(lines, indent=2, ensure_ascii=False)
            + "\n```",
            content,
            count=1,
            flags=re.S,
        )
    elif "## Canonical dialogue" not in content:
        content = content.replace("---\n\n## ENGLISH FOCUS", f"---\n\n{canon_block}## ENGLISH FOCUS", 1)

    path.write_text(content, encoding="utf-8")


def main() -> None:
    data = json.loads(CANONICAL.read_text(encoding="utf-8"))
    updated = 0
    for key, ep in data["episodes"].items():
        sid, num = key.split("/")
        path = PROMPTS / f"{sid}-t{int(num):02d}-comic.md"
        lines = ep.get("lines") or []
        if path.exists() and lines:
            update_prompt_file(path, lines, ep.get("title", ""))
            updated += 1
    print(f"Synced {updated} prompt files from canonical-dialogues.json")


if __name__ == "__main__":
    main()

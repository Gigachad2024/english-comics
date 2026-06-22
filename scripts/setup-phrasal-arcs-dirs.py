#!/usr/bin/env python3
"""Create image directories for Phrasal Verb expansion arcs (episodes 119–210)."""

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))

from phrasal_verbs_expansion import EPISODE_DIRS  # noqa: E402


def main() -> None:
    for arc, num, slug in EPISODE_DIRS:
        tap = f"tập-{num:02d}"
        name = f"{arc}-tap{num:02d}-{slug}.png"
        d = ROOT / "images" / "comics" / arc / tap
        d.mkdir(parents=True, exist_ok=True)
        placeholder = d / ".gitkeep"
        if not placeholder.exists():
            placeholder.write_text("", encoding="utf-8")
        print(f"OK  {d.relative_to(ROOT)}/{name}")
    print(f"\nCreated {len(EPISODE_DIRS)} episode folders under images/comics/")


if __name__ == "__main__":
    main()

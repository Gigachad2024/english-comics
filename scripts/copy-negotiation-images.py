#!/usr/bin/env python3
"""Copy generated negotiation-boundaries images into images/comics/."""

import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
ASSETS = Path("/Users/kevin/.cursor/projects/Users-kevin-Documents-English-Comics/assets")

COPIES = [
    ("negotiation-boundaries-tap85.png", "negotiation-boundaries/tập-85/negotiation-boundaries-tap85-the-tight-deadline.png"),
    ("negotiation-boundaries-tap86.png", "negotiation-boundaries/tập-86/negotiation-boundaries-tap86-would-it-be-possible-to.png"),
    ("negotiation-boundaries-tap87.png", "negotiation-boundaries/tập-87/negotiation-boundaries-tap87-thats-outside-the-scope.png"),
    ("negotiation-boundaries-tap88.png", "negotiation-boundaries/tập-88/negotiation-boundaries-tap88-push-back-on-scope-creep.png"),
    ("negotiation-boundaries-tap89.png", "negotiation-boundaries/tập-89/negotiation-boundaries-tap89-negotiation-boundaries-finale.png"),
]


def main() -> None:
    for src_name, rel_dst in COPIES:
        src = ASSETS / src_name
        dst = ROOT / "images" / "comics" / rel_dst
        if not src.exists():
            print(f"MISSING {src}")
            continue
        dst.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(src, dst)
        print(f"OK  {rel_dst} ({dst.stat().st_size} bytes)")


if __name__ == "__main__":
    main()

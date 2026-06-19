#!/usr/bin/env python3
"""Copy generated giving-feedback images into images/comics/."""

import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
ASSETS = Path("/Users/kevin/.cursor/projects/Users-kevin-Documents-English-Comics/assets")

COPIES = [
    ("giving-feedback-tap90.png", "giving-feedback/tập-90/giving-feedback-tap90-preparing-for-the-1-on-1.png"),
    ("giving-feedback-tap91.png", "giving-feedback/tập-91/giving-feedback-tap91-one-thing-that-went-well-was.png"),
    ("giving-feedback-tap92.png", "giving-feedback/tập-92/giving-feedback-tap92-id-suggest-trying.png"),
    ("giving-feedback-tap93.png", "giving-feedback/tập-93/giving-feedback-tap93-how-can-i-support-you.png"),
    ("giving-feedback-tap94.png", "giving-feedback/tập-94/giving-feedback-tap94-feedback-1-on-1-finale.png"),
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

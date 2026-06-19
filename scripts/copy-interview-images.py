#!/usr/bin/env python3
"""Copy generated interview-career images into images/comics/."""

import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

# Primary: Cursor assets from generate session
ASSETS = Path("/Users/kevin/.cursor/projects/Users-kevin-Documents-English-Comics/assets")
# Fallback: sibling copy if assets missing
FALLBACK = Path("/Users/kevin/Documents/English-Comics/images/comics")

COPIES = [
    ("interview-career-tap79-v2.png", "interview-career/tập-79/interview-career-tap79-the-first-phone-screen.png"),
    ("interview-career-tap80.png", "interview-career/tập-80/interview-career-tap80-tell-me-about-a-time-when.png"),
    ("interview-career-tap81.png", "interview-career/tập-81/interview-career-tap81-why-do-you-want-this-role.png"),
    ("interview-career-tap82.png", "interview-career/tập-82/interview-career-tap82-the-salary-question.png"),
    ("interview-career-tap83.png", "interview-career/tập-83/interview-career-tap83-questions-for-the-interviewer.png"),
    ("interview-career-tap84.png", "interview-career/tập-84/interview-career-tap84-interview-career-finale.png"),
]


def resolve_src(name: str, rel_dst: str):
    for base in (ASSETS, FALLBACK / Path(rel_dst).parent):
        # assets use flat names; fallback uses final filename in tập folder
        if base == ASSETS:
            p = base / name
        else:
            p = base / Path(rel_dst).name
        if p.exists():
            return p
    return None


def main() -> None:
    for src_name, rel_dst in COPIES:
        src = resolve_src(src_name, rel_dst)
        dst = ROOT / "images" / "comics" / rel_dst
        if not src:
            print(f"MISSING {src_name}")
            continue
        dst.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(src, dst)
        print(f"OK  {rel_dst} ({dst.stat().st_size} bytes) <- {src}")


if __name__ == "__main__":
    main()

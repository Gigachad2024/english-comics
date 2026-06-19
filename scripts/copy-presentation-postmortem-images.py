#!/usr/bin/env python3
"""Copy generated presentation-pitch and incident-postmortem images."""

import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
ASSETS = Path("/Users/kevin/.cursor/projects/Users-kevin-Documents-English-Comics/assets")

COPIES = [
    ("presentation-pitch-tap95.png", "presentation-pitch/tập-95/presentation-pitch-tap95-structuring-the-demo.png"),
    ("presentation-pitch-tap96.png", "presentation-pitch/tập-96/presentation-pitch-tap96-walk-through-the-demo.png"),
    ("presentation-pitch-tap97.png", "presentation-pitch/tập-97/presentation-pitch-tap97-the-key-takeaway-is.png"),
    ("presentation-pitch-tap98.png", "presentation-pitch/tập-98/presentation-pitch-tap98-handling-tough-questions.png"),
    ("presentation-pitch-tap99.png", "presentation-pitch/tập-99/presentation-pitch-tap99-presentation-pitch-finale.png"),
    ("incident-postmortem-tap100.png", "incident-postmortem/tập-100/incident-postmortem-tap100-the-war-room.png"),
    ("incident-postmortem-tap101.png", "incident-postmortem/tập-101/incident-postmortem-tap101-what-we-know-so-far-is.png"),
    ("incident-postmortem-tap102.png", "incident-postmortem/tập-102/incident-postmortem-tap102-root-cause-analysis.png"),
    ("incident-postmortem-tap103.png", "incident-postmortem/tập-103/incident-postmortem-tap103-action-items-going-forward.png"),
    ("incident-postmortem-tap104.png", "incident-postmortem/tập-104/incident-postmortem-tap104-postmortem-finale.png"),
]


def main() -> None:
    ok = 0
    for src_name, rel_dst in COPIES:
        src = ASSETS / src_name
        dst = ROOT / "images" / "comics" / rel_dst
        if not src.exists():
            print(f"MISSING {src_name}")
            continue
        dst.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(src, dst)
        print(f"OK  {rel_dst} ({dst.stat().st_size} bytes)")
        ok += 1
    print(f"\nCopied {ok}/{len(COPIES)} images")


if __name__ == "__main__":
    main()

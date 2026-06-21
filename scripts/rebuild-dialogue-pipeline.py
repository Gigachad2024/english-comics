#!/usr/bin/env python3
"""Full dialogue pipeline: canonical → prompts → guides → validate."""

import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PY = sys.executable

STEPS = [
    ("Build canonical from images", [PY, str(ROOT / "scripts/build-canonical-dialogues.py")]),
    ("Sync prompts", [PY, str(ROOT / "scripts/sync-prompts-from-canonical.py")]),
    ("Build learning guides", [PY, str(ROOT / "scripts/build-learning-data.py")]),
    ("Validate sync", [PY, str(ROOT / "scripts/validate-dialogue-sync.py")]),
]


def main() -> int:
    for name, cmd in STEPS:
        print(f"\n=== {name} ===")
        r = subprocess.run(cmd, cwd=ROOT)
        if r.returncode != 0:
            print(f"FAILED at: {name}")
            return r.returncode
    print("\nAll dialogue pipeline steps passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

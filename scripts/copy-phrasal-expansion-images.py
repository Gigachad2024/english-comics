#!/usr/bin/env python3
"""Copy generated phrasal expansion images from Cursor assets into images/comics/."""

import re
import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
ASSETS = Path("/Users/kevin/.cursor/projects/Users-kevin-Documents-Learn-English-Comics/assets")


def output_path(ep: int) -> Path:
    matches = list((ROOT / "prompts").glob(f"*-t{ep}-comic.md"))
    if not matches:
        raise FileNotFoundError(f"No prompt for episode {ep}")
    text = matches[0].read_text()
    rel = re.search(r"\*\*Output:\*\* `([^`]+)`", text).group(1)
    return ROOT / rel


def resolve_src(dst: Path, extra_names=None):
    names = [dst.name]
    if extra_names:
        names = extra_names + names
    for name in names:
        p = ASSETS / name
        if p.exists():
            return p
    return None


def copy_episode(ep: int, extra_names=None) -> bool:
    dst = output_path(ep)
    src = resolve_src(dst, extra_names)
    if not src:
        print(f"T{ep} MISSING {dst.name}")
        return False
    dst.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(src, dst)
    print(f"T{ep} OK {dst.stat().st_size} bytes -> {dst.relative_to(ROOT)}")
    return True


def main() -> None:
    if len(sys.argv) > 1:
        episodes = [int(x) for x in sys.argv[1:]]
    else:
        episodes = list(range(133, 211))
    ok = sum(copy_episode(ep) for ep in episodes)
    print(f"Copied {ok}/{len(episodes)} episodes")


if __name__ == "__main__":
    main()

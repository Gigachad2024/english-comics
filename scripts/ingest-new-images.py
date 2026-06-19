#!/usr/bin/env python3
"""Copy newly provided images into images/comics/ with standard names."""

import json
import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / "untitled folder"

NEW_EPISODES = [
    ("ChatGPT Image Jun 14, 2026, 09_30_41 PM.png", 41, "first-code-review-in-english"),
    ("ChatGPT Image Jun 14, 2026, 09_30_19 PM.png", 42, "the-performance-problem"),
    ("ChatGPT Image Jun 14, 2026, 09_30_15 PM.png", 43, "i-have-a-different-take"),
    ("ChatGPT Image Jun 14, 2026, 09_30_29 PM.png", 44, "walk-me-through-the-architecture"),
    ("ChatGPT Image Jun 14, 2026, 09_30_02 PM.png", 45, "quick-patch-or-full-refactor"),
    ("ChatGPT Image Jun 14, 2026, 09_29_58 PM.png", 46, "demo-day-pressure"),
    ("ChatGPT Image Jun 14, 2026, 09_29_53 PM.png", 47, "the-junior-asks-for-help"),
    ("ChatGPT Image Jun 14, 2026, 09_29_48 PM.png", 48, "incident-recap-meeting"),
    ("ChatGPT Image Jun 14, 2026, 09_29_35 PM.png", 49, "speaking-up"),
    ("ChatGPT Image Jun 14, 2026, 09_29_29 PM.png", 50, "nam-becomes-the-bridge"),
]

ARC = "career-growth"

# ── Template: System Design 51–60 ──
# ARC = "system-design"
# NEW_EPISODES = [
#     ("ChatGPT Image ....png", 51, "the-system-design-question"),
#     ("ChatGPT Image ....png", 52, "monolith-or-microservices"),
#     ...
# ]

# ── Template: Career Advanced 79–104 ──
# Chạy từng arc — đổi ARC và NEW_EPISODES, thả PNG vào untitled folder/
#
# ARC = "interview-career"
# NEW_EPISODES = [
#     ("ChatGPT Image ....png", 79, "the-first-phone-screen"),
#     ("ChatGPT Image ....png", 80, "tell-me-about-a-time-when"),
#     ...
# ]
#
# ARC = "negotiation-boundaries"  # 85-89
# ARC = "giving-feedback"         # 90-94
# ARC = "presentation-pitch"      # 95-99
# ARC = "incident-postmortem"     # 100-104
#
# python3 scripts/setup-career-advanced-dirs.py  # tạo thư mục trước


def target(num: int, slug: str) -> Path:
    tap = f"tập-{num:02d}"
    name = f"{ARC}-tap{num:02d}-{slug}.png"
    return ROOT / "images" / "comics" / ARC / tap / name


def main() -> None:
    manifest = []
    for filename, num, slug in NEW_EPISODES:
        src = SRC / filename
        dst = target(num, slug)
        if not src.exists():
            raise FileNotFoundError(f"Missing source: {src}")
        dst.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(src, dst)
        rel = str(dst.relative_to(ROOT)).replace("\\", "/")
        manifest.append({"arc": ARC, "episode_num": num, "slug": slug, "image": rel, "source": filename})
        print(f"OK  {rel}")

    out = ROOT / "data" / "new-images-manifest.json"
    out.write_text(json.dumps(manifest, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"\nWrote {out} ({len(manifest)} episodes)")


if __name__ == "__main__":
    main()

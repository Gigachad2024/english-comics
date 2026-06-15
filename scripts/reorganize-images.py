#!/usr/bin/env python3
"""Reorganize English Vault comic images to web-friendly paths."""

import json
import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

CATALOG = [
    {"old_path": "ChatGPT Image Jun 14, 2026, 02_23_52 PM.png", "arc": "series-bible", "episode_num": 0, "slug": "series-bible-master-style"},
    {"old_path": "Bug/Phần 1/ChatGPT Image Jun 14, 2026, 02_24_13 PM (1).png", "arc": "bug-arc-1", "episode_num": 1, "slug": "quick-patch-or-full-refactor"},
    {"old_path": "Bug/Phần 1/ChatGPT Image Jun 14, 2026, 02_24_13 PM (2).png", "arc": "bug-arc-1", "episode_num": 2, "slug": "deploy-today-or-wait-for-qa"},
    {"old_path": "Bug/Phần 1/ChatGPT Image Jun 14, 2026, 02_24_13 PM (3).png", "arc": "bug-arc-1", "episode_num": 3, "slug": "redis-or-database-only"},
    {"old_path": "Bug/Phần 1/ChatGPT Image Jun 14, 2026, 02_24_13 PM (4).png", "arc": "bug-arc-1", "episode_num": 4, "slug": "rollback-or-hotfix"},
    {"old_path": "Bug/Phần 1/ChatGPT Image Jun 14, 2026, 02_24_13 PM (5).png", "arc": "bug-arc-1", "episode_num": 5, "slug": "go-or-frontend"},
    {"old_path": "Bug/Phần 1/ChatGPT Image Jun 14, 2026, 02_24_13 PM (6).png", "arc": "bug-arc-1", "episode_num": 6, "slug": "tokyo-cafe-late-thoughts"},
    {"old_path": "Bug/Phần 1/ChatGPT Image Jun 14, 2026, 02_24_13 PM (7).png", "arc": "bug-arc-1", "episode_num": 7, "slug": "settling-on-a-plan"},
    {"old_path": "Bug/Phần 1/ChatGPT Image Jun 14, 2026, 02_24_13 PM (8).png", "arc": "bug-arc-1", "episode_num": 8, "slug": "team-dinner-in-tokyo"},
    {"old_path": "Bug/Phần 1/ChatGPT Image Jun 14, 2026, 02_24_13 PM (9).png", "arc": "bug-arc-1", "episode_num": 9, "slug": "tokyo-or-osaka"},
    {"old_path": "Bug/Phần 1/ChatGPT Image Jun 14, 2026, 02_24_13 PM (10).png", "arc": "bug-arc-1", "episode_num": 10, "slug": "the-safer-choice"},
    {"old_path": "Bug/Phần 2/ChatGPT Image Jun 14, 2026, 02_28_00 PM (1).png", "arc": "bug-arc-2", "episode_num": 1, "slug": "payment-page-panic"},
    {"old_path": "Bug/Phần 2/ChatGPT Image Jun 14, 2026, 02_28_00 PM (2).png", "arc": "bug-arc-2", "episode_num": 2, "slug": "frontend-relies-on-the-api"},
    {"old_path": "Bug/Phần 2/ChatGPT Image Jun 14, 2026, 02_28_00 PM (3).png", "arc": "bug-arc-2", "episode_num": 3, "slug": "go-through-the-logs"},
    {"old_path": "Bug/Phần 2/ChatGPT Image Jun 14, 2026, 02_28_00 PM (4).png", "arc": "bug-arc-2", "episode_num": 4, "slug": "qa-checklist-showdown"},
    {"old_path": "Bug/Phần 2/ChatGPT Image Jun 14, 2026, 02_28_01 PM (5).png", "arc": "bug-arc-2", "episode_num": 5, "slug": "demo-flow-drill"},
    {"old_path": "Bug/Phần 2/ChatGPT Image Jun 14, 2026, 02_28_01 PM (6).png", "arc": "bug-arc-2", "episode_num": 6, "slug": "when-plans-fall-through"},
    {"old_path": "Bug/Phần 2/ChatGPT Image Jun 14, 2026, 02_28_01 PM (7).png", "arc": "bug-arc-2", "episode_num": 7, "slug": "follow-through-the-fix"},
    {"old_path": "Bug/Phần 2/ChatGPT Image Jun 14, 2026, 02_28_03 PM (8).png", "arc": "bug-arc-2", "episode_num": 8, "slug": "cache-culprit"},
    {"old_path": "Bug/Phần 2/ChatGPT Image Jun 14, 2026, 02_28_04 PM (9).png", "arc": "bug-arc-2", "episode_num": 9, "slug": "final-risk-meeting"},
    {"old_path": "Bug/Phần 2/ChatGPT Image Jun 14, 2026, 02_28_06 PM (10).png", "arc": "bug-arc-2", "episode_num": 10, "slug": "safe-release-finale"},
    {"old_path": "Bug/Phần 3/ChatGPT Image Jun 14, 2026, 02_29_16 PM (1).png", "arc": "bug-arc-3", "episode_num": 1, "slug": "investor-demo-nightmare"},
    {"old_path": "Bug/Phần 3/ChatGPT Image Jun 14, 2026, 02_29_16 PM (2).png", "arc": "bug-arc-3", "episode_num": 2, "slug": "quick-patch-or-rollback"},
    # Episode 3 image added separately — see prompts/bug-arc-3-t03-comic.md
    {"old_path": "Bug/Phần 3/ChatGPT Image Jun 14, 2026, 02_29_17 PM (3).png", "arc": "bug-arc-3", "episode_num": 4, "slug": "cache-suspect"},
    {"old_path": "Bug/Phần 3/ChatGPT Image Jun 14, 2026, 02_29_19 PM (4).png", "arc": "bug-arc-3", "episode_num": 5, "slug": "qa-gate"},
    {"old_path": "Bug/Phần 3/ChatGPT Image Jun 14, 2026, 02_29_20 PM (5).png", "arc": "bug-arc-3", "episode_num": 6, "slug": "the-safer-choice"},
    {"old_path": "Bug/Phần 3/ChatGPT Image Jun 14, 2026, 02_29_21 PM (6).png", "arc": "bug-arc-3", "episode_num": 7, "slug": "demo-rehearsal"},
    {"old_path": "Bug/Phần 3/ChatGPT Image Jun 14, 2026, 02_29_23 PM (7).png", "arc": "bug-arc-3", "episode_num": 8, "slug": "release-plan-at-risk"},
    {"old_path": "Bug/Phần 3/ChatGPT Image Jun 14, 2026, 02_29_24 PM (8).png", "arc": "bug-arc-3", "episode_num": 9, "slug": "nam-levels-up"},
    {"old_path": "Traveling/ChatGPT Image Jun 14, 2026, 02_53_58 PM (1).png", "arc": "traveling", "episode_num": 11, "slug": "tokyo-or-osaka"},
    {"old_path": "Traveling/ChatGPT Image Jun 14, 2026, 02_53_58 PM (2).png", "arc": "traveling", "episode_num": 12, "slug": "train-or-taxi"},
    {"old_path": "Traveling/ChatGPT Image Jun 14, 2026, 02_53_58 PM (3).png", "arc": "traveling", "episode_num": 13, "slug": "the-hotel-problem"},
    {"old_path": "Traveling/ChatGPT Image Jun 14, 2026, 02_53_58 PM (4).png", "arc": "traveling", "episode_num": 14, "slug": "sleep-on-the-itinerary"},
    {"old_path": "Traveling/ChatGPT Image Jun 14, 2026, 02_53_58 PM (5).png", "arc": "traveling", "episode_num": 15, "slug": "settling-on-osaka"},
    {"old_path": "Traveling/ChatGPT Image Jun 14, 2026, 02_54_03 PM (1).png", "arc": "traveling", "episode_num": 16, "slug": "what-should-i-order"},
    {"old_path": "Traveling/ChatGPT Image Jun 14, 2026, 02_54_03 PM (2).png", "arc": "traveling", "episode_num": 17, "slug": "food-tour-or-shopping"},
    {"old_path": "Traveling/ChatGPT Image Jun 14, 2026, 02_54_03 PM (3).png", "arc": "traveling", "episode_num": 18, "slug": "lost-in-shinjuku-station"},
    {"old_path": "Traveling/ChatGPT Image Jun 14, 2026, 02_54_03 PM (4).png", "arc": "traveling", "episode_num": 19, "slug": "walk-me-through-the-route"},
    {"old_path": "Traveling/ChatGPT Image Jun 14, 2026, 02_54_03 PM (5).png", "arc": "traveling", "episode_num": 20, "slug": "kyoto-before-sunset"},
    {"old_path": "Traveling/ChatGPT Image Jun 14, 2026, 02_54_08 PM (1).png", "arc": "traveling", "episode_num": 21, "slug": "the-fuji-question"},
    {"old_path": "Traveling/ChatGPT Image Jun 14, 2026, 02_54_08 PM (2).png", "arc": "traveling", "episode_num": 22, "slug": "morning-train-to-fuji"},
    {"old_path": "Traveling/ChatGPT Image Jun 14, 2026, 02_54_08 PM (3).png", "arc": "traveling", "episode_num": 23, "slug": "rainy-day-backup-plan"},
    {"old_path": "Traveling/ChatGPT Image Jun 14, 2026, 02_54_08 PM (4).png", "arc": "traveling", "episode_num": 24, "slug": "fuji-clears-up"},
    {"old_path": "Traveling/ChatGPT Image Jun 14, 2026, 02_54_08 PM (5).png", "arc": "traveling", "episode_num": 25, "slug": "travel-finale"},
    {"old_path": "Living/ChatGPT Image Jun 14, 2026, 05_52_08 PM (1).png", "arc": "living", "episode_num": 26, "slug": "new-apartment-in-tokyo"},
    {"old_path": "Living/ChatGPT Image Jun 14, 2026, 05_52_13 PM (5).png", "arc": "living", "episode_num": 27, "slug": "can-you-walk-me-through-the-contract"},
    {"old_path": "Living/ChatGPT Image Jun 14, 2026, 05_52_10 PM (3).png", "arc": "living", "episode_num": 28, "slug": "does-saturday-work-for-you"},
    {"old_path": "Living/ChatGPT Image Jun 14, 2026, 05_52_11 PM (4).png", "arc": "living", "episode_num": 29, "slug": "running-late-at-shinjuku-station"},
    {"old_path": "Living/ChatGPT Image Jun 14, 2026, 05_52_08 PM (2).png", "arc": "living", "episode_num": 30, "slug": "fill-out-the-form"},
    {"old_path": "Living/ChatGPT Image Jun 14, 2026, 05_55_50 PM.png", "arc": "living", "episode_num": 31, "slug": "moving-day"},
    {"old_path": "Living/ChatGPT Image Jun 14, 2026, 05_55_56 PM.png", "arc": "living", "episode_num": 33, "slug": "opening-a-bank-account"},
    {"old_path": "Living/ChatGPT Image Jun 14, 2026, 05_55_59 PM.png", "arc": "living", "episode_num": 34, "slug": "bug-alert-after-work"},
    {"old_path": "Living/ChatGPT Image Jun 14, 2026, 05_56_05 PM.png", "arc": "living", "episode_num": 35, "slug": "first-remote-meeting-from-tokyo-apartment"},
    {"old_path": "Living/ChatGPT Image Jun 14, 2026, 05_56_10 PM (1).png", "arc": "living", "episode_num": 36, "slug": "follow-through-on-the-fix"},
    {"old_path": "Living/ChatGPT Image Jun 14, 2026, 05_56_12 PM (2).png", "arc": "living", "episode_num": 37, "slug": "clinic-appointment"},
    {"old_path": "Living/ChatGPT Image Jun 14, 2026, 05_56_12 PM (3).png", "arc": "living", "episode_num": 38, "slug": "getting-used-to-life-in-japan"},
    {"old_path": "Living/ChatGPT Image Jun 14, 2026, 05_56_13 PM (4).png", "arc": "living", "episode_num": 39, "slug": "team-dinner-after-release"},
    {"old_path": "Living/ChatGPT Image Jun 14, 2026, 05_56_14 PM (5).png", "arc": "living", "episode_num": 40, "slug": "english-for-real-life-finale"},
]


def target_path(item: dict) -> Path:
    arc = item["arc"]
    num = item["episode_num"]
    slug = item["slug"]
    if arc == "series-bible":
        return Path("images/comics/series-bible") / f"tokyo-debug-{slug}.png"
    tap = f"tập-{num:02d}"
    filename = f"{arc}-tap{num:02d}-{slug}.png"
    return Path("images/comics") / arc / tap / filename


def main() -> None:
    manifest = []
    for item in CATALOG:
        src = ROOT / item["old_path"]
        dst = ROOT / target_path(item)
        if not src.exists():
            raise FileNotFoundError(f"Missing: {src}")
        dst.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(src, dst)
        rel = str(target_path(item)).replace("\\", "/")
        manifest.append({**item, "image": rel})
        print(f"OK  {rel}")

    out = ROOT / "data" / "image-manifest.json"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(manifest, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"\nWrote {out} ({len(manifest)} entries)")


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""Create empty image directories for Get Phrasal Verb arcs (episodes 105–118)."""

from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

EPISODES = [
    ("silicon-valley-get", 105, "can-you-loop-me-in"),
    ("silicon-valley-get", 106, "we-need-buy-in"),
    ("silicon-valley-get", 107, "blocked-on-dependencies"),
    ("silicon-valley-get", 108, "ship-it-friday"),
    ("silicon-valley-get", 109, "pulled-into-the-war-room"),
    ("silicon-valley-get", 110, "the-acquisition-news"),
    ("switzerland-travel", 111, "landing-in-zurich"),
    ("switzerland-travel", 112, "the-glacier-express"),
    ("switzerland-travel", 113, "view-from-the-top"),
    ("switzerland-travel", 114, "snowed-in-at-zermatt"),
    ("switzerland-travel", 115, "lost-on-the-alpine-trail"),
    ("english-everyday-get", 116, "first-english-meetup"),
    ("english-everyday-get", 117, "when-you-finally-get-it"),
    ("english-everyday-get", 118, "everyday-get-finale"),
]


def main() -> None:
    for arc, num, slug in EPISODES:
        tap = f"tập-{num:02d}"
        name = f"{arc}-tap{num:02d}-{slug}.png"
        d = ROOT / "images" / "comics" / arc / tap
        d.mkdir(parents=True, exist_ok=True)
        placeholder = d / ".gitkeep"
        if not placeholder.exists():
            placeholder.write_text("", encoding="utf-8")
        print(f"OK  {d.relative_to(ROOT)}/{name}")

    print(f"\nCreated {len(EPISODES)} episode folders under images/comics/")


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""Create empty image directories for Career Advanced arcs (episodes 79–104)."""

from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

EPISODES = [
    ("interview-career", 79, "the-first-phone-screen"),
    ("interview-career", 80, "tell-me-about-a-time-when"),
    ("interview-career", 81, "why-do-you-want-this-role"),
    ("interview-career", 82, "the-salary-question"),
    ("interview-career", 83, "questions-for-the-interviewer"),
    ("interview-career", 84, "interview-career-finale"),
    ("negotiation-boundaries", 85, "the-tight-deadline"),
    ("negotiation-boundaries", 86, "would-it-be-possible-to"),
    ("negotiation-boundaries", 87, "thats-outside-the-scope"),
    ("negotiation-boundaries", 88, "push-back-on-scope-creep"),
    ("negotiation-boundaries", 89, "negotiation-boundaries-finale"),
    ("giving-feedback", 90, "preparing-for-the-1-on-1"),
    ("giving-feedback", 91, "one-thing-that-went-well-was"),
    ("giving-feedback", 92, "id-suggest-trying"),
    ("giving-feedback", 93, "how-can-i-support-you"),
    ("giving-feedback", 94, "feedback-1-on-1-finale"),
    ("presentation-pitch", 95, "structuring-the-demo"),
    ("presentation-pitch", 96, "walk-through-the-demo"),
    ("presentation-pitch", 97, "the-key-takeaway-is"),
    ("presentation-pitch", 98, "handling-tough-questions"),
    ("presentation-pitch", 99, "presentation-pitch-finale"),
    ("incident-postmortem", 100, "the-war-room"),
    ("incident-postmortem", 101, "what-we-know-so-far-is"),
    ("incident-postmortem", 102, "root-cause-analysis"),
    ("incident-postmortem", 103, "action-items-going-forward"),
    ("incident-postmortem", 104, "postmortem-finale"),
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

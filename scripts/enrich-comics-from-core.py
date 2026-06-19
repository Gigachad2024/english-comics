#!/usr/bin/env python3
"""Enrich comics.json episodes with patterns, packs, practice prompts from core.json."""

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

# Arc -> default pack IDs
ARC_PACKS = {
    "bug-arc-1": ["decision_hesitation", "preference_opinion", "bug_report_agreement_through"],
    "bug-arc-2": ["bug_report_agreement_through", "decision_hesitation"],
    "bug-arc-3": ["bug_report_agreement_through", "preference_opinion", "decision_hesitation"],
    "traveling": ["decision_hesitation", "preference_opinion"],
    "living": ["universal_communication_v2"],
    "career-growth": [
        "bug_report_agreement_through",
        "preference_opinion",
        "decision_hesitation",
        "universal_communication_v2",
    ],
    "system-design": [
        "bug_report_agreement_through",
        "preference_opinion",
        "decision_hesitation",
        "universal_communication_v2",
    ],
    "email-async": ["email_async", "universal_communication_v2"],
    "japan-culture": ["decision_hesitation", "preference_opinion", "universal_communication_v2"],
    "anime-manga": ["decision_hesitation", "preference_opinion", "universal_communication_v2"],
    "interview-career": ["interview_career", "universal_communication_v2"],
    "negotiation-boundaries": ["negotiation_boundaries", "preference_opinion", "decision_hesitation"],
    "giving-feedback": ["giving_feedback", "universal_communication_v2"],
    "presentation-pitch": ["presentation_pitch", "universal_communication_v2", "bug_report_agreement_through"],
    "incident-postmortem": ["incident_postmortem", "bug_report_agreement_through", "email_async"],
}

# Slug -> contexts tags
SLUG_CONTEXTS = {
    "quick-patch-or-full-refactor": ["software-engineering", "work-meeting", "decision"],
    "deploy-today-or-wait-for-qa": ["software-engineering", "QA", "decision"],
    "tokyo-or-osaka": ["travel", "decision"],
    "what-should-i-order": ["travel", "food", "decision"],
    "walk-me-through-shrine-etiquette": ["japan-culture", "travel", "asking-help"],
    "the-onsen-question": ["japan-culture", "japan-life", "clarification"],
    "cherry-blossom-dilemma": ["japan-culture", "travel", "decision"],
    "akihabara-or-nakano-broadway": ["anime-manga", "travel", "decision"],
    "anime-pilgrimage-day": ["anime-manga", "travel", "small-talk"],
    "anime-talk-at-team-lunch": ["anime-manga", "software-engineering", "small-talk"],
    "the-first-phone-screen": ["career", "interview", "software-engineering"],
    "tell-me-about-a-time-when": ["career", "interview", "software-engineering"],
    "the-tight-deadline": ["career", "work-meeting", "negotiation"],
    "thats-outside-the-scope": ["career", "work-meeting", "negotiation"],
    "one-thing-that-went-well-was": ["career", "work-meeting", "feedback"],
    "walk-through-the-demo": ["career", "work-meeting", "presentation"],
    "the-war-room": ["software-engineering", "production", "incident"],
    "root-cause-analysis": ["software-engineering", "QA", "incident"],
    "new-apartment-in-tokyo": ["japan-life", "decision"],
    "moving-day": ["japan-life", "feeling"],
    "first-code-review-in-english": ["software-engineering", "asking-help"],
    "speaking-up": ["software-engineering", "work-meeting", "opinion"],
    "nam-becomes-the-bridge": ["career-growth", "work-meeting"],
}

COMMON_MISTAKES = [
    {
        "wrong": "Could you help me this?",
        "correct": "Could you help me with this?",
        "why": "help me with + object",
        "patterns": ["Could you help me", "help me with"],
    },
    {
        "wrong": "I'm looking forward to visit Kyoto.",
        "correct": "I'm looking forward to visiting Kyoto.",
        "why": "look forward to + V-ing",
        "patterns": ["look forward to"],
    },
    {
        "wrong": "The API is return incorrect data.",
        "correct": "The API is returning incorrect data.",
        "why": "dùng present continuous cho lỗi đang xảy ra",
        "patterns": ["The API is returning", "is returning"],
    },
    {
        "wrong": "I'm torn between deploy or wait.",
        "correct": "I'm torn between deploying and waiting.",
        "why": "torn between A and B — A/B cùng dạng từ",
        "patterns": ["I'm torn between"],
    },
    {
        "wrong": "Tell me about a time when I fix a bug.",
        "correct": "Tell me about a time when I fixed a bug.",
        "why": "behavioral interview — dùng past tense cho sự kiện đã xảy ra",
        "patterns": ["Tell me about a time when", "One challenge I faced"],
    },
    {
        "wrong": "Root cause is the cache.",
        "correct": "Root cause appears to be the cache.",
        "why": "postmortem — dùng appears to be khi chưa chắc chắn 100%",
        "patterns": ["Root cause appears", "What we know so far"],
    },
    {
        "wrong": "One thing went well was the demo.",
        "correct": "One thing that went well was the demo.",
        "why": "feedback pattern — cần that sau thing",
        "patterns": ["One thing that went well"],
    },
]


def normalize(s: str) -> str:
    return re.sub(r"\s+", " ", s.lower().replace("'", "'").strip())


def collect_patterns(core: dict) -> list[str]:
    out = []
    for pack in core["packs"]:
        out.extend(pack.get("patterns", []))
        out.extend(pack.get("phrasalVerbs", []))
        out.extend(pack.get("phrases", []))
        for g in pack.get("groups", []):
            out.extend(g.get("patterns", []))
            out.extend(g.get("phrases", []))
    return out


def match_packs(ep, series_id: str, all_patterns: list[str]) -> list[str]:
    packs = set(ARC_PACKS.get(series_id, []))
    focus_text = " ".join(
        f.get("phrase", f) if isinstance(f, dict) else str(f)
        for f in ep.get("englishFocus", [])
    ).lower()
    title = ep.get("title", "").lower()
    blob = f"{focus_text} {title}"

    rules = [
        ("decision_hesitation", ["torn between", "debating", "can't decide", "don't know what", "should i"]),
        ("preference_opinion", ["leaning toward", "makes more sense", "go with", "opt for", "stick with", "rule out", "weigh up"]),
        ("bug_report_agreement_through", ["the issue is", "it seems like", "api is returning", "bug affects", "different take", "see your point", "walk through", "go through", "follow through"]),
        ("email_async", ["following up", "loop me in", "loop in", "get back to", "check in on", "keep me posted", "blocked on", "look into this", "async standup", "reach out"]),
        ("interview_career", ["tell me about a time", "what i learned from", "looking for a role", "interested in this role", "attracted me to"]),
        ("negotiation_boundaries", ["would it be possible", "outside the scope", "push back", "timeline is too tight", "need at least", "scope creep"]),
        ("giving_feedback", ["one thing that went well", "area to improve", "i'd suggest trying", "how can i support", "have you considered"]),
        ("presentation_pitch", ["let me walk you through", "key takeaway", "any questions on this", "main problem we're solving", "keep this brief"]),
        ("incident_postmortem", ["what we know so far", "root cause appears", "action items going forward", "mitigated the issue", "timeline of events"]),
    ]
    for pack_id, keys in rules:
        if any(k in blob for k in keys):
            packs.add(pack_id)
    if series_id in ("living", "traveling", "career-growth", "system-design", "email-async", "japan-culture", "anime-manga", "interview-career", "giving-feedback", "presentation-pitch"):
        packs.add("universal_communication_v2")
    return sorted(packs)


def practice_prompts(ep, packs: list[str], core: dict) -> list[str]:
    prompts = []
    title = ep.get("title", "this situation")
    for f in ep.get("englishFocus", [])[:3]:
        phrase = f.get("phrase", f) if isinstance(f, dict) else str(f)
        prompts.append(f"Dùng câu 「{phrase}」 để nói về tình huống: {title}.")
    if not prompts:
        prompts.append(f"Đọc truyện và viết 2–3 câu tiếng Anh mô tả tình huống: {title}.")
    for pack in core["packs"]:
        if pack["id"] in packs and pack.get("masterCombo"):
            prompts.append(f"Thử nói master combo của pack 「{pack['title']}」 cho tình huống này.")
            break
    return prompts[:4]


def related_mistakes(ep) -> list[dict]:
    blob = " ".join(
        (f.get("phrase", f) if isinstance(f, dict) else str(f)).lower()
        for f in ep.get("englishFocus", [])
    )
    return [m for m in COMMON_MISTAKES if any(p.lower() in blob for p in m["patterns"])]


def main() -> None:
    core = json.loads((ROOT / "data" / "core.json").read_text(encoding="utf-8"))
    comics_path = ROOT / "data" / "comics.json"
    comics = json.loads(comics_path.read_text(encoding="utf-8"))
    all_patterns = collect_patterns(core)

    for series in comics["series"]:
        sid = series["id"]
        eps = series["episodes"]
        for i, ep in enumerate(eps):
            packs = match_packs(ep, sid, all_patterns)
            ep["packs"] = packs
            ep["contexts"] = SLUG_CONTEXTS.get(ep.get("slug", ""), [])
            ep["patterns"] = [
                (f.get("phrase") if isinstance(f, dict) else str(f))
                for f in ep.get("englishFocus", [])
            ]
            ep["practicePrompts"] = practice_prompts(ep, packs, core)
            ep["commonMistakes"] = related_mistakes(ep)
            if i + 1 < len(eps):
                ep["hook"] = f"Next: {eps[i + 1]['title']}"
            else:
                ep["hook"] = ""

    comics["coreLoop"] = core["project"]["coreLoop"]
    comics_path.write_text(json.dumps(comics, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"Enriched {comics['count']} episodes with packs & practice prompts")


if __name__ == "__main__":
    main()

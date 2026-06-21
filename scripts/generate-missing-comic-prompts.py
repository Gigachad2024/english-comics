#!/usr/bin/env python3
"""Generate comic prompt .md files for episodes missing dialogue story beats."""

from __future__ import annotations

import importlib.util
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))

from dialogue_helpers import fill_pattern, title_options  # noqa: E402

OUT = ROOT / "prompts"

STYLE = """Modern anime manga educational webcomic, clean cel-shading, Tokyo office at night,
Tokyo Tower through window, cinematic blue-purple lighting, professional software team,
detailed UI monitors, high quality illustration, portrait comic page 1024x1536,
thin white panel borders, educational infographic style"""

ARC_META = {
    "bug-arc-1": {"title": "Debug & Release", "color": "#EF4444", "setting": "Tokyo dev office, monitors showing production alerts"},
    "bug-arc-2": {"title": "Payment & Demo Crisis", "color": "#F97316", "setting": "Tokyo office war room, payment dashboard on screens"},
    "bug-arc-3": {"title": "Investor Demo Nightmare", "color": "#A855F7", "setting": "Tokyo office at night, investor demo countdown on screen"},
    "traveling": {"title": "English on the Road", "color": "#06B6D4", "setting": "Tokyo streets, train stations, travel maps and konbini"},
    "living": {"title": "English for Real Life", "color": "#10B981", "setting": "Tokyo apartment, station, clinic, bank — daily life in Japan"},
    "career-growth": {"title": "Career Growth Arc", "color": "#6366F1", "setting": "Tokyo office meeting rooms, code review on monitors"},
}


def load_focus() -> dict:
    spec = importlib.util.spec_from_file_location("bcd", ROOT / "scripts" / "build-comics-data.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod.FOCUS


def load_parse_prompts():
    spec = importlib.util.spec_from_file_location("bld", ROOT / "scripts" / "build-learning-data.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod.parse_prompts


def focus_items(ep: dict, focus_dict: dict) -> list[dict]:
    items = ep.get("englishFocus") or focus_dict.get(ep.get("slug", ""), [])
    return items


def filled_phrases(ep: dict, items: list[dict]) -> list[str]:
    title = ep["title"]
    out = []
    for f in items:
        p = f.get("phrase", "")
        if p:
            out.append(fill_pattern(p, title).rstrip("."))
    return out


def story_decision(ep: dict, items: list[dict]) -> list[tuple[str, str]]:
    title = ep["title"]
    a, b = title_options(title)
    phrases = filled_phrases(ep, items)
    p0 = phrases[0] if phrases else f"I'm torn between {a} and {b}"
    p1 = phrases[1] if len(phrases) > 1 else f"I'm leaning toward {a.split()[0] if a else 'this'}"
    p2 = phrases[2] if len(phrases) > 2 else f"I think I'll go with {a.split()[0] if a else 'this'}"
    return [
        (f"Team faces decision: {title.rstrip('?')}.", f'Kenji: "We need to choose — {a} or {b}?"'),
        (f"Nam shares hesitation.", f'Nam: "{p0}."'),
        (f"Aoi weighs trade-offs.", f'Aoi: "{b.capitalize()} is safer, but {a} has benefits too."'),
        (f"Linh adds perspective.", f'Linh: "{p1}."'),
        (f"Kenji seeks clarity.", f'Kenji: "What makes more sense to you?"'),
        (f"Nam decides.", f'Nam: "{p2}."'),
    ]


def story_bug(ep: dict, items: list[dict]) -> list[tuple[str, str]]:
    title = ep["title"]
    phrases = filled_phrases(ep, items)
    p0 = phrases[0] if phrases else "The issue is that the payment API is returning 500 errors"
    p1 = phrases[1] if len(phrases) > 1 else "The API is returning incorrect data for some users"
    p2 = phrases[2] if len(phrases) > 2 else "The bug affects the checkout flow at the confirm step"
    return [
        ("Alert on payment dashboard.", 'Linh: "Users are reporting checkout failures."'),
        ("Nam checks logs.", f'Nam: "{p0}."'),
        ("API response on screen.", f'Nam: "{p1}."'),
        ("Impact diagram.", f'Nam: "{p2}."'),
        ("Kenji asks next step.", 'Kenji: "I think we should go through the logs before deploying."'),
        ("Team aligned.", 'Aoi: "That makes sense — let\'s find the root cause first."'),
    ]


def story_walk_through(ep: dict, items: list[dict]) -> list[tuple[str, str]]:
    title = ep["title"]
    topic = title.replace("Walk Me Through the ", "").replace("Can You Walk Me Through the ", "").replace("?", "")
    topic = topic.replace("Walk Me Through ", "").strip() or "this"
    phrases = filled_phrases(ep, items)
    ask = phrases[0] if phrases else f"Can you walk me through the {topic.lower()}?"
    return [
        (f"Nam needs help with {topic}.", f'Nam: "{ask if ask.endswith("?") else ask + "?"}"'),
        ("Helper explains step by step.", f'Staff: "Let me walk you through it step by step."'),
        ("Whiteboard or document.", f'Staff: "First, here is the main flow you need to know."'),
        ("Nam asks clarifying question.", 'Nam: "What does this part mean?"'),
        ("Confirmation.", 'Nam: "Let me make sure I got this right."'),
        ("Nam thanks helper.", 'Nam: "That makes sense — thank you."'),
    ]


def story_travel(ep: dict, items: list[dict]) -> list[tuple[str, str]]:
    title = ep["title"]
    a, b = title_options(title)
    phrases = filled_phrases(ep, items)
    slug = ep.get("slug", "")
    if "order" in slug or "should i" in title.lower():
        p0 = phrases[0] if phrases else "I don't know what to order"
        p1 = phrases[1] if len(phrases) > 1 else "I can't decide what to try first"
        return [
            ("Team at restaurant in Japan.", 'Friend: "What should we order?"'),
            ("Menu in Japanese and English.", f'Nam: "{p0}."'),
            ("Friend suggests dishes.", 'Friend: "Do you have any dietary restrictions?"'),
            ("Nam narrows choices.", f'Nam: "{p1}."'),
            ("Decision.", 'Nam: "I think I\'ll go with the ramen."'),
            ("Food arrives.", 'Friend: "That sounds amazing — enjoy!"'),
        ]
    if "lost" in slug or "route" in slug:
        return [
            ("Shinjuku station — crowded.", 'Nam: "I\'m not sure I understand this map."'),
            ("Asks station staff.", 'Nam: "Could you show me how to get to the right platform?"'),
            ("Staff explains.", 'Staff: "Let me walk you through the route step by step."'),
            ("Nam follows signs.", 'Nam: "Just to clarify — I transfer at Shibuya, right?"'),
            ("Arrives at destination.", 'Nam: "I\'m glad that worked — thank you."'),
            ("Team meets up.", 'Friend: "You made it! That station is confusing."'),
        ]
    if "finale" in slug:
        return story_finale(ep, items, "travel")
    p0 = phrases[0] if phrases else f"I'm torn between {a} and {b}"
    p1 = phrases[1] if len(phrases) > 1 else f"I'm leaning toward {a.split()[0] if a else 'Tokyo'}"
    return [
        ("Travel planning at hotel lobby.", f'Friend: "Where should we go next — {a} or {b}?"'),
        ("Nam thinks.", f'Nam: "{p0}."'),
        ("Research on phone.", f'Nam: "{p1}."'),
        ("Friend agrees.", f'Friend: "{a.capitalize() if a else "This option"} makes more sense for our schedule."'),
        ("Tickets booked.", 'Nam: "I think we\'ll go with that plan."'),
        ("Excited for trip.", 'Nam: "I\'m excited about the trip tomorrow."'),
    ]


def story_living(ep: dict, items: list[dict]) -> list[tuple[str, str]]:
    title = ep["title"]
    slug = ep.get("slug", "")
    phrases = filled_phrases(ep, items)
    if "contract" in slug:
        return story_walk_through(ep, items)
    if "saturday" in slug or "appointment" in slug or "schedule" in slug.lower():
        return [
            ("Scheduling on phone.", 'Landlord: "When can you come to sign?"'),
            ("Nam checks calendar.", 'Nam: "Does Saturday work for you?"'),
            ("Time negotiation.", 'Landlord: "How about 2 PM?"'),
            ("Nam confirms.", 'Nam: "That works for me — I\'ll be there."'),
            ("Reminder note.", 'Nam: "I\'m running late if the train is delayed."'),
            ("Meeting confirmed.", 'Nam: "Thank you — see you Saturday."'),
        ]
    if "running late" in slug:
        return [
            ("Nam rushing at Shinjuku station.", 'Nam: "I\'m running late — sorry!"'),
            ("Texts landlord.", 'Nam: "I\'ll be there in twenty minutes."'),
            ("Train delay announcement.", 'Nam: "Can we push it back by thirty minutes?"'),
            ("Landlord replies OK.", 'Landlord: "No problem — see you soon."'),
            ("Nam arrives.", 'Nam: "Sorry, I missed that last transfer."'),
            ("Relief.", 'Landlord: "You made it — let\'s start."'),
        ]
    if "form" in slug or "bank" in slug:
        return [
            ("Bank counter in Tokyo.", 'Clerk: "How can I help you today?"'),
            ("Nam with documents.", 'Nam: "I\'d like to open a bank account."'),
            ("Form on desk.", 'Clerk: "You need to fill out this form first."'),
            ("Nam asks help.", 'Nam: "Could you help me with this section?"'),
            ("Clerk explains.", 'Clerk: "Can you show me how to fill out the address part?"'),
            ("Done.", 'Nam: "Thank you — I think I got it right."'),
        ]
    if "moving" in slug:
        p0 = phrases[0] if phrases else "I'm excited about the new apartment"
        p1 = phrases[1] if len(phrases) > 1 else "I'm nervous about moving day"
        return [
            ("Boxes everywhere.", f'Nam: "{p0}."'),
            ("Friend helps carry.", f'Nam: "{p1}."'),
            ("Landlord handover.", 'Landlord: "Let me walk you through the contract one more time."'),
            ("Keys handed over.", 'Nam: "I\'m getting used to the neighborhood already."'),
            ("First night.", 'Nam: "It was worth it — I\'m proud of myself."'),
            ("Settled in.", 'Friend: "Welcome to your new place in Tokyo!"'),
        ]
    if "finale" in slug:
        return story_finale(ep, items, "living")
    if "bug" in slug or "remote" in slug or "follow-through" in slug:
        return story_bug(ep, items)
    a, b = title_options(title)
    p0 = phrases[0] if phrases else f"I'm torn between {a} and {b}"
    return [
        ("Nam at apartment.", f'Friend: "How is life in Tokyo going?"'),
        ("Daily life challenge.", f'Nam: "{p0}."'),
        ("Asking for help.", 'Nam: "Could you help me with this?"'),
        ("Helper responds.", 'Friend: "Let me walk you through it."'),
        ("Progress.", 'Nam: "I\'m getting used to life in Japan."'),
        ("Confidence.", 'Nam: "That makes sense now — thank you."'),
    ]


def story_career(ep: dict, items: list[dict]) -> list[tuple[str, str]]:
    slug = ep.get("slug", "")
    phrases = filled_phrases(ep, items)
    if "code-review" in slug:
        return [
            ("PR review on screen.", 'Aoi: "Can you walk me through this logic?"'),
            ("Nam explains.", 'Nam: "I\'m not sure I understand this part — could you clarify?"'),
            ("Discussion.", 'Aoi: "I think we should add a test before merging."'),
            ("Nam learns.", 'Nam: "That makes sense — I\'ll update the PR."'),
            ("Approved.", 'Aoi: "Good improvement — clear structure."'),
            ("Nam confident.", 'Nam: "Thanks — first code review in English done!"'),
        ]
    if "different-take" in slug or "speaking-up" in slug:
        p0 = phrases[0] if phrases else "I have a different take"
        p1 = phrases[1] if len(phrases) > 1 else "I see your point, but we need to think through the risks"
        return [
            ("Architecture debate.", 'Engineer: "We should deploy tonight."'),
            ("Nam speaks up.", f'Nam: "{p0}."'),
            ("Polite disagreement.", f'Nam: "{p1}."'),
            ("Kenji listens.", 'Kenji: "That\'s a fair point — tell us more."'),
            ("Team discusses.", 'Nam: "It comes down to user impact vs speed."'),
            ("Respectful agreement.", 'Kenji: "Let\'s weigh up both options."'),
        ]
    if "architecture" in slug or "walk-me-through" in slug:
        return story_walk_through(ep, items)
    if "demo" in slug:
        return [
            ("Demo rehearsal.", 'Kenji: "Investors arrive in one hour."'),
            ("Nam nervous.", 'Nam: "I\'m nervous about the demo."'),
            ("Team drills flow.", 'Aoi: "Let\'s run through the main flow one more time."'),
            ("Nam presents.", 'Nam: "I\'m ready to present."'),
            ("Demo succeeds.", 'Kenji: "Strong demo — clear structure."'),
            ("Relief.", 'Nam: "We worked through the pressure together."'),
        ]
    if "junior" in slug or "help" in slug:
        return [
            ("Junior engineer stuck.", 'Junior: "Could you help me with this setup?"'),
            ("Nam mentors.", 'Nam: "I can walk you through it step by step."'),
            ("Pair debugging.", 'Nam: "Let\'s figure it out together."'),
            ("Junior learns.", 'Junior: "Oh — that makes sense now."'),
            ("Nam encourages.", 'Nam: "You\'ll get it — step by step."'),
            ("Team growth.", 'Kenji: "Good mentoring, Nam."'),
        ]
    if "incident-recap" in slug:
        return [
            ("Post-incident meeting.", 'Kenji: "Walk us through what happened."'),
            ("Nam presents timeline.", 'Nam: "Let me walk you through what happened."'),
            ("Root issue.", 'Nam: "The issue was that we skipped a cache check."'),
            ("Fix status.", 'Nam: "We followed through on the fix overnight."'),
            ("Lessons.", 'Aoi: "Good recap — clear structure."'),
            ("Close.", 'Kenji: "Let\'s add monitoring before the next release."'),
        ]
    if "bridge" in slug or "finale" in slug:
        return story_finale(ep, items, "career")
    return story_decision(ep, items) if " or " in ep["title"].lower() else story_bug(ep, items)


def story_bug_arc3(ep: dict, items: list[dict]) -> list[tuple[str, str]]:
    slug = ep.get("slug", "")
    if "investor" in slug:
        phrases = filled_phrases(ep, items)
        p0 = phrases[0] if phrases else "The issue is that the demo environment is unstable"
        p1 = phrases[1] if len(phrases) > 1 else "I'm torn between a quick patch and a rollback"
        return [
            ("Investor demo tomorrow — tension.", 'Kenji: "Investors arrive in twelve hours."'),
            ("Payment broken on staging.", f'Linh: "{p0}."'),
            ("High stakes decision.", f'Nam: "{p1}."'),
            ("Trade-offs.", 'Kenji: "We need to weigh up the trade-offs."'),
            ("War room mode.", 'Aoi: "Let\'s focus on the payment flow first."'),
            ("Hook.", 'Kenji: "No mistakes tomorrow — let\'s prepare."'),
        ]
    if "cache" in slug:
        return [
            ("Cache layer diagram.", 'Aoi: "It seems like the cache update caused this."'),
            ("Nam investigates.", 'Nam: "This might be caused by misconfigured TTL."'),
            ("Confirm step fails.", 'Nam: "The confirm call fails after the cache update."'),
            ("Linh tests.", 'Linh: "That\'s where the 500 errors are coming from."'),
            ("Fix plan.", 'Kenji: "I think we should roll back the cache change."'),
            ("Next step.", 'Kenji: "Good — now let\'s verify in QA."'),
        ]
    if "qa-gate" in slug:
        return [
            ("QA checklist on screen.", 'Linh: "We can\'t skip QA before the investor demo."'),
            ("PM pushes timeline.", 'PM: "Can we deploy today without full QA?"'),
            ("Nam pushback.", 'Nam: "I see your point, but the bug affects checkout."'),
            ("Risk discussion.", 'Kenji: "I think we should wait for QA sign-off."'),
            ("Agreement.", 'Linh: "That makes sense — safety first."'),
            ("Plan.", 'Kenji: "Let\'s run through the demo flow after QA passes."'),
        ]
    if "rehearsal" in slug or "demo" in slug:
        return [
            ("Empty conference room rehearsal.", 'Kenji: "Let\'s run through the demo one last time."'),
            ("Nam presents flow.", 'Nam: "Let me walk you through the payment flow."'),
            ("Linh catches bug.", 'Linh: "Wait — the confirm step still fails sometimes."'),
            ("Fix applied.", 'Aoi: "We mitigated the issue — try again."'),
            ("Success.", 'Kenji: "That looks ready for investors."'),
            ("Confidence.", 'Nam: "I\'m ready — we followed through on every fix."'),
        ]
    if "levels-up" in slug:
        return [
            ("After successful demo.", 'Investor: "Clear explanation — well done."'),
            ("Kenji proud.", 'Kenji: "You walked the team through the whole crisis."'),
            ("Nam reflects.", 'Nam: "I think we made the safer choice at every step."'),
            ("Team celebrates.", 'Aoi: "You\'ve become the bridge between QA and backend."'),
            ("Future.", 'Nam: "I\'m looking forward to leading the next release."'),
            ("Finale.", 'Kenji: "Nam levels up — great work under pressure."'),
        ]
    if " or " in ep["title"].lower():
        return story_decision(ep, items)
    return story_bug(ep, items)


def story_finale(ep: dict, items: list[dict], kind: str) -> list[tuple[str, str]]:
    phrases = filled_phrases(ep, items)
    recap = {
        "travel": "We used travel English from trains to food to Fuji.",
        "living": "From contracts to bank forms — real life English in Tokyo.",
        "career": "From code review to speaking up — Nam leads with English.",
    }
    text = recap.get(kind, "We practiced English patterns across this arc.")
    p0 = phrases[0] if phrases else "It was worth it"
    p1 = phrases[1] if len(phrases) > 1 else "I'm proud of myself"
    p2 = phrases[2] if len(phrases) > 2 else "I'm looking forward to using these patterns every day"
    return [
        ("Arc recap montage.", f'Nam: "{text}"'),
        ("Friend or team reflects.", f'Friend: "{p0}."'),
        ("Nam proud.", f'Nam: "{p1}."'),
        ("Patterns remembered.", f'Nam: "{p2}."'),
        ("Future plans.", 'Nam: "I\'ll keep practicing in real situations."'),
        ("Finale title card.", f'Nam: "{ep["title"]} — we did it!"'),
    ]


def story_bug_arc2(ep: dict, items: list[dict]) -> list[tuple[str, str]]:
    slug = ep.get("slug", "")
    title = ep["title"].lower()
    if "panic" in slug or ep.get("num") == 1:
        return story_bug(ep, items)
    if "fall through" in slug or "plans-fall" in slug:
        return [
            ("QA discovery.", 'Linh: "A new QA discovery just came in."'),
            ("Release at risk.", 'Kenji: "The release plan might fall through if this bug stays open."'),
            ("Nam disagrees.", 'Nam: "I have a different take."'),
            ("Kenji responds.", 'Kenji: "I see your point, but we need more testing."'),
            ("Bug scope.", 'Linh: "The bug affects mobile checkout only."'),
            ("Nam plan.", 'Nam: "We can isolate the impact, ship a scoped fix, and protect the release."'),
        ]
    if "logs" in slug:
        return [
            ("Log dashboard open.", 'Kenji: "Let\'s go through the logs together."'),
            ("Nam scrolls.", 'Nam: "It seems like the error starts at the confirm endpoint."'),
            ("Pattern found.", 'Aoi: "This might be caused by the new cache layer."'),
            ("Timeline.", 'Nam: "The API is returning 500 after the cache update."'),
            ("Next step.", 'Linh: "Can you walk me through the sequence diagram?"'),
            ("Aligned.", 'Kenji: "Good — let\'s follow through on this lead."'),
        ]
    if "qa" in slug or "checklist" in slug:
        return [
            ("QA checklist on whiteboard.", 'Linh: "We need full regression before the demo."'),
            ("Dev pushback.", 'Aoi: "Can we deploy with a known low-risk bug?"'),
            ("Nam mediates.", 'Nam: "I see your point, but I think we should wait for QA."'),
            ("Agreement.", 'Linh: "That makes sense — checkout must pass."'),
            ("Sign-off.", 'Linh: "I\'ll run through the payment flow tests tonight."'),
            ("Plan.", 'Kenji: "Demo flow drill tomorrow morning."'),
        ]
    if "fall through" in slug:
        return [
            ("Calendar change.", 'PM: "The demo slot might fall through — investor delayed."'),
            ("Team reacts.", 'Nam: "Should we still deploy the fix today?"'),
            ("Replan.", 'Kenji: "Let\'s follow through on the fix anyway."'),
            ("Priority.", 'Aoi: "The issue is that checkout is still broken."'),
            ("New date.", 'PM: "Demo moved to Friday — we have more time."'),
            ("Relief.", 'Nam: "We can wait for QA now."'),
        ]
    if "finale" in slug or "safe release" in slug:
        return [
            ("Release checklist green.", 'Kenji: "All QA tests passed — safe to release."'),
            ("Nam summary.", 'Nam: "We followed through on every action item."'),
            ("Deploy success.", 'Aoi: "The bug is fixed — checkout works."'),
            ("Demo ready.", 'Linh: "Demo flow drill completed successfully."'),
            ("Celebration.", 'Kenji: "Safe release — great teamwork."'),
            ("Hook.", 'Nam: "Next arc: investor demo nightmare awaits..."'),
        ]
    if "cache" in slug:
        return story_bug_arc3(ep, items)
    return story_bug(ep, items)


def pick_story(series_id: str, ep: dict, items: list[dict]) -> list[tuple[str, str]]:
    slug = ep.get("slug", "")
    title = ep["title"].lower()
    if series_id.startswith("bug-arc-3"):
        return story_bug_arc3(ep, items)
    if series_id == "bug-arc-2":
        return story_bug_arc2(ep, items)
    if series_id == "bug-arc-1":
        if " or " in title:
            return story_decision(ep, items)
        if "cafe" in slug or "dinner" in slug:
            return [
                ("Tokyo café at night.", 'Nam: "I\'m still thinking about the deploy decision."'),
                ("Friend joins.", 'Friend: "Sleep on it — don\'t decide when tired."'),
                ("Reflection.", 'Nam: "A full refactor makes more sense long term."'),
                ("Team dinner.", 'Kenji: "Let\'s settle on a plan tomorrow morning."'),
                ("Small talk.", 'Nam: "I\'m torn between speed and quality."'),
                ("Calm.", 'Nam: "I think I\'ll go with the safer choice."'),
            ]
        if "settling" in slug or "safer" in slug:
            return story_decision(ep, items)
        return story_bug(ep, items) if "redis" in slug or "rollback" in slug else story_decision(ep, items)
    if series_id == "traveling":
        return story_travel(ep, items)
    if series_id == "living":
        return story_living(ep, items)
    if series_id == "career-growth":
        return story_career(ep, items)
    if "walk" in title and "through" in title:
        return story_walk_through(ep, items)
    if " or " in title:
        return story_decision(ep, items)
    if any(w in title for w in ("bug", "panic", "api", "payment", "incident", "cache")):
        return story_bug(ep, items)
    if "finale" in slug:
        return story_finale(ep, items, series_id)
    return story_decision(ep, items)


def render_md(series: dict, ep: dict, story: list[tuple[str, str]], items: list[dict]) -> str:
    sid = series["id"]
    meta = ARC_META.get(sid, {"title": series["title"], "color": series.get("color", "#06B6D4"), "setting": "Tokyo"})
    num = ep["num"]
    slug = ep["slug"]
    title = ep["title"]
    hook = ep.get("hook") or (story[-1][1] if story else "")
    if hook and not hook.startswith("Next"):
        hook = f"Next: {hook.replace('Next: ', '')}"

    focus_lines = "\n".join(
        f'  {i}. "{f["phrase"]}" = {f["meaning"]}' for i, f in enumerate(items, 1)
    ) if items else "  (patterns from episode dialogue)"
    focus_prompt = "\n".join(
        f'- "{f["phrase"]}" = {f["meaning"]}' for f in items
    ) if items else "- key phrases from dialogue"

    panels_md = "\n".join(
        f"- **Panel {i}:** {scene} Dialogue: {dialogue}" for i, (scene, dialogue) in enumerate(story, 1)
    )
    panels_prompt = "\n".join(
        f"Panel {i}: {scene}. Speech: {dialogue}" for i, (scene, dialogue) in enumerate(story, 1)
    )

    fname = f"{sid}-t{num:02d}-comic.md"
    return fname, f"""# {meta['title']} — Episode {num}: {title}

> **File:** `{fname}` · **Arc ID:** `{sid}` · **Màu:** `{meta['color']}`
> **Output:** `images/comics/{sid}/tập-{num:02d}/{sid}-tap{num:02d}-{slug}.png`
> **Attach:** `prompts/00-character-bible.md` + `prompts/00-layout-guide.md`

**Slug:** `{slug}`

---

## Story beats

{panels_md}

---

## ENGLISH FOCUS (phải có trong ảnh)

```
ENGLISH FOCUS
{focus_lines}
Tip: Patterns from episode dialogue — read each line in the comic.
```

**Next hook:** {hook}

---

## PROMPT FULL PAGE (copy-paste)

```
Draw ONE complete educational manga comic page — English Vault: Tokyo Debug Chronicles.

ARC: {meta['title']}
EPISODE {num}: {title}
Accent color: {meta['color']}

STYLE: {STYLE}

CHARACTERS (consistent):
- Nam: young Vietnamese man, blue hoodie #2563EB, Junior Engineer badge
- Kenji: Tech Lead, dark shirt/suit, glasses
- Aoi: Senior Engineer, navy blazer, long black hair
- Linh: QA Engineer, gray hoodie
Setting: {meta['setting']}

LAYOUT: Header once at top → 6 numbered panels (2x3 grid) → ENGLISH FOCUS box → NEXT hook box

PANEL STORY:
{panels_prompt}

ENGLISH FOCUS box must list:
{focus_prompt}

All dialogue in ENGLISH. Vietnamese ONLY inside ENGLISH FOCUS meanings.
Portrait 1024x1536. NO watermark.
```
"""


def main() -> None:
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("--force", action="store_true", help="Overwrite even if canonical exists")
    args = parser.parse_args()

    focus_dict = load_focus()
    parse_prompts = load_parse_prompts()
    existing = parse_prompts()
    comics = json.loads((ROOT / "data" / "comics.json").read_text(encoding="utf-8"))

    canonical_path = ROOT / "data" / "canonical-dialogues.json"
    canonical = {}
    if canonical_path.exists():
        canonical = json.loads(canonical_path.read_text(encoding="utf-8")).get("episodes", {})

    written = 0
    skipped = 0
    for series in comics["series"]:
        sid = series["id"]
        for ep in series["episodes"]:
            key = f"{sid}/{ep['num']}"
            fname = f"{sid}-t{ep['num']:02d}-comic.md"
            path = OUT / fname

            if key in canonical and not args.force:
                skipped += 1
                continue

            pd = existing.get(key) or existing.get(ep.get("slug", ""), {})
            n = len(pd.get("dialogueLines") or [])
            if path.exists() and n >= 6 and not args.force:
                skipped += 1
                continue

            items = focus_items(ep, focus_dict)
            story = pick_story(sid, ep, items)
            _, content = render_md(series, ep, story, items)
            path.write_text(content, encoding="utf-8")
            print(f"Wrote {fname} ({len(story)} panels, {len(items)} focus)")
            written += 1

    print(f"\nDone: {written} written, {skipped} skipped (canonical protected)")


if __name__ == "__main__":
    main()

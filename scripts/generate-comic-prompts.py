#!/usr/bin/env python3
"""Generate Cursor/ChatGPT image prompts for English Vault comic episodes."""

from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "prompts"


def load_focus_dict() -> dict:
    """Reuse Vietnamese meanings from build-comics-data.py."""
    import importlib.util
    path = ROOT / "scripts" / "build-comics-data.py"
    spec = importlib.util.spec_from_file_location("build_comics_data", path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod.FOCUS

STYLE = """Modern anime manga educational webcomic, clean cel-shading, Tokyo office at night,
Tokyo Tower through window, cinematic blue-purple lighting, professional software team,
detailed UI monitors, high quality illustration, portrait comic page 1024x1536,
thin white panel borders, educational infographic style"""

EPISODES = [
    # ── System Design Arc 51–60 ──
    {
        "file": "system-design-t51-comic.md",
        "arc": "System Design Arc — Thinking Bigger",
        "arc_id": "system-design",
        "num": 51,
        "title": "The System Design Question",
        "color": "#8B5CF6",
        "focus": ["I'm wondering if...", "Could we start by...", "walk me through"],
        "story": [
            ("Kenji asks Nam to explain a feature at scale in English.", "Kenji: \"Can you walk us through how this would work at 10x traffic?\""),
            ("Nam nervous but starts.", "Nam: \"I'm wondering if we should start with the current flow first.\""),
            ("Whiteboard: User → API → Service → DB.", "Aoi: \"Good — let's map the read path vs write path.\""),
            ("Team discusses bottlenecks.", "Linh: \"What happens when checkout spikes?\""),
            ("Nam gains confidence.", "Nam: \"Could we start by identifying the single biggest bottleneck?\""),
            ("Hook.", "Next: Monolith or Microservices?"),
        ],
    },
    {
        "file": "system-design-t52-comic.md",
        "arc": "System Design Arc — Thinking Bigger",
        "arc_id": "system-design",
        "num": 52,
        "title": "Monolith or Microservices?",
        "color": "#8B5CF6",
        "focus": ["I'm torn between A and B.", "I'm leaning toward A because...", "weigh up"],
        "story": [
            ("Whiteboard: MONOLITH vs MICROSERVICES pros/cons.", "Nam: \"I'm torn between keeping the monolith and splitting services.\""),
            ("Kenji asks why.", "Nam: \"I'm leaning toward the monolith because our team is still small.\""),
            ("Aoi adds trade-offs.", "Aoi: \"Microservices help scale teams, not always traffic.\""),
            ("Cost diagram on screen.", "Kenji: \"We need to weigh up complexity vs flexibility.\""),
            ("Decision checklist.", "Nam: \"A monolith makes more sense to me for the next two quarters.\""),
            ("Hook.", "Next: Cache or Database First?"),
        ],
    },
    {
        "file": "system-design-t53-comic.md",
        "arc": "System Design Arc — Thinking Bigger",
        "arc_id": "system-design",
        "num": 53,
        "title": "Cache or Database First?",
        "color": "#8B5CF6",
        "focus": ["The issue is that...", "It seems like...", "rely on"],
        "story": [
            ("Slow reads on dashboard.", "Nam: \"The issue is that every request hits the database.\""),
            ("Redis diagram on monitor.", "Aoi: \"Redis can act as a cache layer here.\""),
            ("Cache hit/miss flow.", "Nam: \"It seems like we're not caching user profile data.\""),
            ("Linh asks about stale data.", "Linh: \"What if the cache is stale?\""),
            ("TTL strategy whiteboard.", "Nam: \"We could rely on Redis for reads and keep DB as source of truth.\""),
            ("Hook.", "Next: Queue Saves the Day"),
        ],
    },
    {
        "file": "system-design-t54-comic.md",
        "arc": "System Design Arc — Thinking Bigger",
        "arc_id": "system-design",
        "num": 54,
        "title": "Queue Saves the Day",
        "color": "#8B5CF6",
        "focus": ["This might be caused by...", "I think we should...", "follow through"],
        "story": [
            ("Payment timeout alert.", "Nam: \"This might be caused by synchronous email sending.\""),
            ("Architecture: add message queue.", "Aoi: \"Put heavy work on a queue — respond fast to users.\""),
            ("SQS/Kafka style diagram.", "Nam: \"I think we should move notifications to async processing.\""),
            ("Before/after latency chart.", "Kenji: \"Show the latency before and after.\""),
            ("Deploy checklist.", "Nam: \"Let's follow through on monitoring the queue depth.\""),
            ("Hook.", "Next: API Gateway at Night"),
        ],
    },
    {
        "file": "system-design-t55-comic.md",
        "arc": "System Design Arc — Thinking Bigger",
        "arc_id": "system-design",
        "num": 55,
        "title": "API Gateway at Night",
        "color": "#8B5CF6",
        "focus": ["walk me through", "act as", "make sure"],
        "story": [
            ("Late night architecture review.", "Aoi: \"Can you walk me through the API Gateway setup?\""),
            ("Gateway routes diagram.", "Nam: \"It acts as a single entry point for all clients.\""),
            ("Auth + rate limit boxes.", "Nam: \"We need to make sure rate limiting is per API key.\""),
            ("Kenji asks about failure.", "Kenji: \"What happens if the gateway goes down?\""),
            ("Health check monitor.", "Nam: \"Let me make sure I got this right — gateway → services → cache → DB.\""),
            ("Hook.", "Next: Scale Under Pressure"),
        ],
    },
    {
        "file": "system-design-t56-comic.md",
        "arc": "System Design Arc — Thinking Bigger",
        "arc_id": "system-design",
        "num": 56,
        "title": "Scale Under Pressure",
        "color": "#8B5CF6",
        "focus": ["It comes down to...", "We need to weigh up...", "I'd opt for..."],
        "story": [
            ("Traffic spike graph on screen.", "Kenji: \"Black Friday scale — we're 5x normal traffic.\""),
            ("Options: scale up vs scale out.", "Nam: \"It comes down to cost vs response time.\""),
            ("Auto-scaling diagram.", "Aoi: \"Horizontal scaling buys time if stateless.\""),
            ("Nam presents recommendation.", "Nam: \"I'd opt for scaling out the API tier first.\""),
            ("Team agrees.", "Kenji: \"We need to weigh up DB connection limits too.\""),
            ("Hook.", "Next: The Cost of Overengineering"),
        ],
    },
    {
        "file": "system-design-t57-comic.md",
        "arc": "System Design Arc — Thinking Bigger",
        "arc_id": "system-design",
        "num": 57,
        "title": "The Cost of Overengineering",
        "color": "#8B5CF6",
        "focus": ["I have a different take.", "I see your point, but...", "rule out"],
        "story": [
            ("Proposal: 12 microservices for MVP.", "Engineer: \"Let's split everything now.\""),
            ("Nam speaks up.", "Nam: \"I have a different take — that's overengineering for our stage.\""),
            ("Simple vs complex diagram.", "Nam: \"I see your point, but we can rule out k8s for now.\""),
            ("Kenji nods.", "Kenji: \"YAGNI — you aren't gonna need it yet.\""),
            ("Simpler architecture approved.", "Aoi: \"Start simple. Measure. Then split.\""),
            ("Hook.", "Next: Explain It to Product"),
        ],
    },
    {
        "file": "system-design-t58-comic.md",
        "arc": "System Design Arc — Thinking Bigger",
        "arc_id": "system-design",
        "num": 58,
        "title": "Explain It to Product",
        "color": "#8B5CF6",
        "focus": ["Let me walk you through...", "In simple terms...", "The main idea is..."],
        "story": [
            ("Meeting with PM (non-technical).", "PM: \"Why does this feature take 3 sprints?\""),
            ("Nam uses simple diagram.", "Nam: \"Let me walk you through the flow in simple terms.\""),
            ("No jargon — user journey.", "Nam: \"The main idea is: fast checkout beats perfect architecture.\""),
            ("PM understands trade-off.", "PM: \"So we ship phase 1 without real-time sync?\""),
            ("Alignment.", "Nam: \"Exactly — we can add that in phase 2.\""),
            ("Hook.", "Next: Design Review Showdown"),
        ],
    },
    {
        "file": "system-design-t59-comic.md",
        "arc": "System Design Arc — Thinking Bigger",
        "arc_id": "system-design",
        "num": 59,
        "title": "Design Review Showdown",
        "color": "#8B5CF6",
        "focus": ["I'm debating whether...", "That makes sense.", "stick with"],
        "story": [
            ("Design review room, big screen.", "Nam presents architecture v2."),
            ("Senior asks hard question.", "Senior: \"What fails first under load?\""),
            ("Nam answers clearly.", "Nam: \"I'm debating whether to add a read replica now or later.\""),
            ("Discussion.", "Aoi: \"That makes sense — stick with one source of truth first.\""),
            ("Approved with actions.", "Kenji: \"Good review. Ship with monitoring.\""),
            ("Hook.", "Next: Thinking Bigger Finale"),
        ],
    },
    {
        "file": "system-design-t60-comic.md",
        "arc": "System Design Arc — Thinking Bigger",
        "arc_id": "system-design",
        "num": 60,
        "title": "Thinking Bigger Finale",
        "color": "#8B5CF6",
        "focus": ["look forward to", "be the bridge", "explain problems clearly"],
        "story": [
            ("Nam at whiteboard — full system map.", "Nam: \"Here's how all the pieces connect now.\""),
            ("Team applauds growth.", "Kenji: \"You think in systems now, not just tickets.\""),
            ("Reflection panel — Tokyo night.", "Nam: \"I'm looking forward to tackling bigger problems.\""),
            ("Bridge between dev/QA/product.", "Nam: \"I can be the bridge between teams on design decisions.\""),
            ("English Focus summary montage.", "Patterns from arc 51–59 recap."),
            ("Next arc teaser.", "Next Arc: Email & Async — Just Following Up"),
        ],
    },
    # ── Email & Async Arc 61–65 (Pack 5) ──
    {
        "file": "email-async-t61-comic.md",
        "arc": "Email & Async Arc — Write Like a Pro",
        "arc_id": "email-async",
        "num": 61,
        "title": "Just Following Up on the PR",
        "color": "#3B82F6",
        "focus": ["Just following up on...", "I wanted to check in on...", "get back to"],
        "story": [
            ("Nam writing Slack/email at desk.", "Subject: Following up on PR #512"),
            ("Draft email on screen.", "Nam: \"Just following up on the PR I sent yesterday.\""),
            ("Linh reviews tone.", "Linh: \"Friendly but clear — add what you need from them.\""),
            ("Improved version.", "Nam: \"I wanted to check in on the review timeline.\""),
            ("Reply received.", "Kenji: \"I'll get back to you by EOD.\""),
            ("Hook.", "Next: Loop Me In on the Decision"),
        ],
    },
    {
        "file": "email-async-t62-comic.md",
        "arc": "Email & Async Arc — Write Like a Pro",
        "arc_id": "email-async",
        "num": 62,
        "title": "Loop Me In on the Decision",
        "color": "#3B82F6",
        "focus": ["Could you loop me in on...?", "keep me posted on...", "reach out to"],
        "story": [
            ("Nam missed a meeting.", "Slack: \"Decision made on cache strategy\""),
            ("Nam messages Kenji.", "Nam: \"Could you loop me in on what was decided?\""),
            ("Kenji adds Nam to thread.", "Kenji: \"I'll add you to the channel thread.\""),
            ("Nam asks to stay updated.", "Nam: \"Please keep me posted on any changes.\""),
            ("Team norm.", "Aoi: \"Always reach out if you're unsure after a meeting.\""),
            ("Hook.", "Next: I'll Get Back to You by EOD"),
        ],
    },
    {
        "file": "email-async-t63-comic.md",
        "arc": "Email & Async Arc — Write Like a Pro",
        "arc_id": "email-async",
        "num": 63,
        "title": "I'll Get Back to You by EOD",
        "color": "#3B82F6",
        "focus": ["I'll get back to you by...", "Let me look into this.", "follow up on"],
        "story": [
            ("PM asks urgent question via Slack.", "PM: \"Can we ship Friday?\""),
            ("Nam doesn't know yet.", "Nam: \"Let me look into this and I'll get back to you by EOD.\""),
            ("Nam checks with Linh + Kenji.", "Quick huddle at desk."),
            ("Nam replies professionally.", "Nam: \"Following up — we can ship Friday if QA passes tonight.\""),
            ("PM thanks.", "PM: \"Thanks for the quick follow-up!\""),
            ("Hook.", "Next: Async Standup in English"),
        ],
    },
    {
        "file": "email-async-t64-comic.md",
        "arc": "Email & Async Arc — Write Like a Pro",
        "arc_id": "email-async",
        "num": 64,
        "title": "Async Standup in English",
        "color": "#3B82F6",
        "focus": ["Here's what I worked on...", "I'm blocked on...", "I'll follow up with..."],
        "story": [
            ("Team uses async standup in Slack.", "Template: Yesterday / Today / Blockers"),
            ("Nam writes update.", "Nam: \"Here's what I worked on: cache invalidation fix.\""),
            ("Blocker.", "Nam: \"I'm blocked on staging access — I'll follow up with DevOps.\""),
            ("Kenji replies.", "Kenji: \"I'll loop in the platform team.\""),
            ("Clean async standup done.", "Linh: \"Clear updates — no meeting needed!\""),
            ("Hook.", "Next: Email & Async Finale"),
        ],
    },
    {
        "file": "email-async-t65-comic.md",
        "arc": "Email & Async Arc — Write Like a Pro",
        "arc_id": "email-async",
        "num": 65,
        "title": "Email & Async Finale",
        "color": "#3B82F6",
        "focus": ["follow up on", "loop in", "get back to", "reach out to"],
        "story": [
            ("Montage: Nam handles email/Slack confidently.", "Multiple screens: sent, replied, resolved"),
            ("Master combo email on screen.", "Full professional async message example."),
            ("Team dinner casual.", "Kenji: \"Your async communication is clear now.\""),
            ("Nam reflects.", "Nam: \"Clear writing saves meetings.\""),
            ("English Focus recap all Pack 5 phrases.", "Summary box."),
            ("Celebrate.", "Next: Nam's English journey continues…"),
        ],
    },
]


def render_episode(ep: dict, slug: str, focus_dict: dict) -> str:
    vi_entries = focus_dict.get(slug, [])
    if vi_entries:
        focus_lines = "\n".join(
            f'  {i}. "{e["phrase"]}" = {e["meaning"]}'
            for i, e in enumerate(vi_entries, 1)
        )
        focus_prompt = "\n".join(
            f'- "{e["phrase"]}" = {e["meaning"]}' for e in vi_entries
        )
    else:
        focus_lines = "\n".join(
            f'  {i}. "{p}" = [Vietnamese meaning]' for i, p in enumerate(ep["focus"], 1)
        )
        focus_prompt = "\n".join(
            f'- "{p}" with Vietnamese translation' for p in ep["focus"]
        )
    hook = ep["story"][-1][1] if ep["story"] else ""
    panels = "\n".join(
        f"- **Panel {i}:** {scene} Dialogue: {dialogue}"
        for i, (scene, dialogue) in enumerate(ep["story"], 1)
    )

    return f"""# {ep['arc']} — Episode {ep['num']}: {ep['title']}

> **File:** `{ep['file']}` · **Arc ID:** `{ep['arc_id']}` · **Màu:** `{ep['color']}`
> **Output:** `images/comics/{ep['arc_id']}/tập-{ep['num']:02d}/{ep['arc_id']}-tap{ep['num']:02d}-{slug}.png`
> **Attach:** `prompts/00-character-bible.md` + `prompts/00-layout-guide.md` + style ref image
> **Cách tạo:** Copy **PROMPT FULL PAGE** → Cursor Generate Image (hoặc ChatGPT)

**Slug gợi ý:** `{slug}`

---

## Story beats

{panels}

---

## ENGLISH FOCUS (phải có trong ảnh)

```
ENGLISH FOCUS
{focus_lines}
Tip: Use these patterns for {ep['arc_id'].replace('-', ' ')} communication.
```

**Next hook:** {hook}

---

## PROMPT FULL PAGE (copy-paste)

```
Draw ONE complete educational manga comic page — English Vault: Tokyo Debug Chronicles.

ARC: {ep['arc']}
EPISODE {ep['num']}: {ep['title']}
Accent color: {ep['color']}

STYLE: {STYLE}

CHARACTERS (consistent):
- Nam: young Vietnamese man, blue hoodie #2563EB, Junior Engineer badge
- Kenji: Tech Lead, dark shirt/suit, glasses
- Aoi: Senior Engineer, navy blazer, long black hair
- Linh: QA Engineer, gray hoodie
Setting: Modern Tokyo office at night, Tokyo Tower visible through window

LAYOUT: Header once at top → 6 numbered panels (2x3 grid) → ENGLISH FOCUS box (beige, full width) → NEXT hook box bottom-right

PANEL STORY:
{chr(10).join(f"Panel {i}: {s}. Speech: {d}" for i, (s, d) in enumerate(ep['story'], 1))}

ENGLISH FOCUS box must list:
{focus_prompt}

Highlight key phrases in BLUE BOLD inside speech bubbles.
All dialogue in ENGLISH. Vietnamese ONLY inside ENGLISH FOCUS meanings.

Footer next episode: {hook}

Portrait 1024x1536, high detail, same visual style as English Vault Tokyo Debug Chronicles series bible.
NO watermark. NO real company logos.
```
"""


def slugify(title: str) -> str:
    import re
    s = title.lower().replace("?", "").replace("'", "")
    s = re.sub(r"[^a-z0-9]+", "-", s).strip("-")
    return s


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    focus_dict = load_focus_dict()
    index = []
    for ep in EPISODES:
        slug = slugify(ep["title"])
        content = render_episode(ep, slug, focus_dict)
        path = OUT / ep["file"]
        path.write_text(content, encoding="utf-8")
        index.append({
            "file": ep["file"],
            "arc_id": ep["arc_id"],
            "num": ep["num"],
            "title": ep["title"],
            "slug": slug,
            "focus": ep["focus"],
        })
        print(f"Wrote {path.name}")

    (OUT / "episode-queue.json").write_text(
        json.dumps(index, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
    )
    print(f"\nWrote episode-queue.json ({len(index)} episodes)")


if __name__ == "__main__":
    main()

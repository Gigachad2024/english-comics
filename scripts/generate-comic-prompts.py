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
    # ── Japan Culture Arc 66–72 ──
    {
        "file": "japan-culture-t66-comic.md",
        "arc": "Japan Culture Arc — Explore Beyond the Guidebook",
        "arc_id": "japan-culture",
        "num": 66,
        "title": "Walk Me Through Shrine Etiquette",
        "color": "#DC2626",
        "setting": "Meiji Shrine or Fushimi Inari torii gates, stone path, warm afternoon light, traditional Japanese atmosphere",
        "focus": ["Can you walk me through how to pray at a shrine?", "Let me make sure I got this right.", "I'm not sure I understand this part."],
        "story": [
            ("Nam and Linh arrive at a shrine.", "Nam: \"It's my first time at a real shrine.\""),
            ("Torii gate and purification fountain.", "Linh: \"Can you walk me through how to pray at a shrine?\""),
            ("Kenji demonstrates bow and clap.", "Kenji: \"Two bows, two claps, one bow — like this.\""),
            ("Nam tries and checks understanding.", "Nam: \"Let me make sure I got this right.\""),
            ("Small mistake on order.", "Nam: \"I'm not sure I understand this part — the clap timing?\""),
            ("Hook.", "Next: The Onsen Question"),
        ],
    },
    {
        "file": "japan-culture-t67-comic.md",
        "arc": "Japan Culture Arc — Explore Beyond the Guidebook",
        "arc_id": "japan-culture",
        "num": 67,
        "title": "The Onsen Question",
        "color": "#DC2626",
        "setting": "Traditional ryokan onsen entrance, wooden signs, steam, tatami changing room, calm hot-spring atmosphere",
        "focus": ["I'm not sure if I should...", "What do you mean by...?", "Could you explain this part again?"],
        "story": [
            ("Team weekend trip to onsen town.", "Signs: wash before bath, no tattoos rule"),
            ("Nam reads rules nervously.", "Nam: \"I'm not sure if I should enter before or after dinner.\""),
            ("Aoi explains konyoku vs gender-separated.", "Aoi: \"What do you mean by 'family bath' here?\""),
            ("Staff explains towel etiquette.", "Staff: \"Small towel stays out of the water.\""),
            ("Nam asks again politely.", "Nam: \"Could you explain this part again?\""),
            ("Hook.", "Next: Izakaya After Work"),
        ],
    },
    {
        "file": "japan-culture-t68-comic.md",
        "arc": "Japan Culture Arc — Explore Beyond the Guidebook",
        "arc_id": "japan-culture",
        "num": 68,
        "title": "Izakaya After Work",
        "color": "#DC2626",
        "setting": "Cozy Tokyo izakaya at night, red lanterns, wooden counter, yakitori and beer, warm after-work atmosphere",
        "focus": ["I'm excited about trying real izakaya food.", "That sounds amazing.", "I'm not really into raw fish, but..."],
        "story": [
            ("Friday after release — team heads to izakaya.", "Kenji: \"Celebration izakaya night!\""),
            ("Menu with unfamiliar dishes.", "Nam: \"I'm excited about trying real izakaya food.\""),
            ("Linh recommends yakitori set.", "Linh: \"Grilled chicken and edamame — that sounds amazing.\""),
            ("Nam sets food preference.", "Nam: \"I'm not really into raw fish, but I'll try the grilled stuff.\""),
            ("Kanpai toast.", "Team: \"Kanpai! Great release week!\""),
            ("Hook.", "Next: Cherry Blossom Dilemma"),
        ],
    },
    {
        "file": "japan-culture-t69-comic.md",
        "arc": "Japan Culture Arc — Explore Beyond the Guidebook",
        "arc_id": "japan-culture",
        "num": 69,
        "title": "Cherry Blossom Dilemma",
        "color": "#DC2626",
        "setting": "Tokyo cherry blossom season, Meguro River and Ueno Park photos on phone, pink petals, hanami picnic scene",
        "focus": ["I'm torn between A and B.", "I'm leaning toward A because...", "I think I'll go with A."],
        "story": [
            ("Spring hanami planning on Slack.", "Linh: \"Where should we do hanami this weekend?\""),
            ("Two options on screen.", "Nam: \"I'm torn between Ueno Park and Meguro River.\""),
            ("Crowd vs scenery debate.", "Aoi: \"Meguro is prettier at night.\""),
            ("Nam decides.", "Nam: \"I'm leaning toward Meguro because the lights look better.\""),
            ("Final choice.", "Nam: \"I think I'll go with Meguro River.\""),
            ("Hook.", "Next: What Is Omotenashi?"),
        ],
    },
    {
        "file": "japan-culture-t70-comic.md",
        "arc": "Japan Culture Arc — Explore Beyond the Guidebook",
        "arc_id": "japan-culture",
        "num": 70,
        "title": "What Is Omotenashi?",
        "color": "#DC2626",
        "setting": "Traditional Japanese inn lobby, staff bowing deeply, tea service, elegant hospitality details",
        "focus": ["I'm surprised that...", "That was worth it.", "I'm glad that we learned the custom first."],
        "story": [
            ("Ryokan check-in — staff bows deeply.", "Nam: \"I'm surprised that they bowed so low.\""),
            ("Kenji explains omotenashi.", "Kenji: \"It's thoughtful hospitality — no tip expected.\""),
            ("Tea and slippers detail.", "Linh: \"Every small detail feels intentional.\""),
            ("Nam reflects.", "Nam: \"I'm glad that we learned the custom first.\""),
            ("Evening kaiseki dinner.", "Nam: \"That was worth it — best meal of the trip.\""),
            ("Hook.", "Next: Summer Festival Night"),
        ],
    },
    {
        "file": "japan-culture-t71-comic.md",
        "arc": "Japan Culture Arc — Explore Beyond the Guidebook",
        "arc_id": "japan-culture",
        "num": 71,
        "title": "Summer Festival Night",
        "color": "#DC2626",
        "setting": "Asakusa summer matsuri at night, food stalls, yukata, paper lanterns, festival crowd energy",
        "focus": ["I'm looking for...", "How long does it take to get to...?", "That sounds amazing."],
        "story": [
            ("Team in yukata at festival.", "Nam: \"I'm looking for the takoyaki stall.\""),
            ("Checking train route on phone.", "Riku: \"How long does it take to get to Asakusa from here?\""),
            ("Goldfish scooping and drums.", "Linh: \"The taiko performance — that sounds amazing.\""),
            ("Fireworks in distance.", "Team watches together."),
            ("Nam buys festival snack.", "Nam: \"This is exactly the Japan experience I wanted.\""),
            ("Hook.", "Next: Japan Culture Finale"),
        ],
    },
    {
        "file": "japan-culture-t72-comic.md",
        "arc": "Japan Culture Arc — Explore Beyond the Guidebook",
        "arc_id": "japan-culture",
        "num": 72,
        "title": "Japan Culture Finale",
        "color": "#DC2626",
        "setting": "Montage: shrine, onsen, izakaya, hanami, matsuri — golden sunset over Tokyo skyline",
        "focus": ["It was worth it.", "I'm proud of myself.", "look forward to"],
        "story": [
            ("Montage of culture episodes.", "Shrine, onsen, izakaya, hanami, festival"),
            ("Team café debrief.", "Kenji: \"You handled every custom situation well.\""),
            ("Nam reflects.", "Nam: \"It was worth it — I feel more confident in Japan now.\""),
            ("Pride moment.", "Nam: \"I'm proud of myself for asking when I wasn't sure.\""),
            ("Future plans.", "Nam: \"I look forward to exploring more regions next season.\""),
            ("Celebrate.", "Next: Akihabara or Nakano Broadway?"),
        ],
    },
    # ── Anime & Manga Arc 73–78 ──
    {
        "file": "anime-manga-t73-comic.md",
        "arc": "Anime & Manga Arc — Dive Into Otaku Japan",
        "arc_id": "anime-manga",
        "num": 73,
        "title": "Akihabara or Nakano Broadway?",
        "color": "#EC4899",
        "setting": "Split scene: Akihabara neon electric town vs Nakano Broadway Sun Mall, colorful anime billboards",
        "focus": ["I'm torn between A and B.", "I'm more interested in A.", "A makes more sense to me."],
        "story": [
            ("Saturday otaku trip planning.", "Nam: \"Where should we go first?\""),
            ("Two districts on map.", "Nam: \"I'm torn between Akihabara and Nakano Broadway.\""),
            ("Linh wants rare manga.", "Linh: \"I'm more interested in Nakano for vintage manga.\""),
            ("Nam decides for figures.", "Nam: \"Akihabara makes more sense to me for my first visit.\""),
            ("Train to Akihabara.", "Team: \"Let's do Nakano tomorrow!\""),
            ("Hook.", "Next: My First Manga Cafe"),
        ],
    },
    {
        "file": "anime-manga-t74-comic.md",
        "arc": "Anime & Manga Arc — Dive Into Otaku Japan",
        "arc_id": "anime-manga",
        "num": 74,
        "title": "My First Manga Cafe",
        "color": "#EC4899",
        "setting": "Japanese manga cafe interior, cubicle booths, manga shelves, drink bar, locker area",
        "focus": ["Can you walk me through how a manga cafe works?", "Could you show me how to use the locker?", "I'm not sure I understand the time system."],
        "story": [
            ("Nam enters manga cafe nervously.", "Sign: pay by time, free drink bar"),
            ("Asks staff for help.", "Nam: \"Can you walk me through how a manga cafe works?\""),
            ("Locker and shoes.", "Staff: \"Shoes off, locker key here.\""),
            ("Nam asks about locker.", "Nam: \"Could you show me how to use the locker?\""),
            ("Hourly billing confusion.", "Nam: \"I'm not sure I understand the time system.\""),
            ("Hook.", "Next: Anime Pilgrimage Day"),
        ],
    },
    {
        "file": "anime-manga-t75-comic.md",
        "arc": "Anime & Manga Arc — Dive Into Otaku Japan",
        "arc_id": "anime-manga",
        "num": 75,
        "title": "Anime Pilgrimage Day",
        "color": "#EC4899",
        "setting": "Real-life anime location in Tokyo suburb, recognizable café staircase, fans taking photos",
        "focus": ["I'm really into this anime.", "I'm excited about finding the café from the scene.", "That sounds amazing."],
        "story": [
            ("Nam shows anime screenshot on phone.", "Nam: \"I'm really into this anime — I want the real location.\""),
            ("Train to pilgrimage spot.", "Linh: \"Fans call this a 'seichi junrei' spot.\""),
            ("Finding the famous staircase.", "Nam: \"I'm excited about finding the café from the scene.\""),
            ("Photo moment.", "Riku: \"Recreating the scene — that sounds amazing.\""),
            ("Other fans chatting in English.", "Fan: \"Which episode is this from?\""),
            ("Hook.", "Next: Figure Store Dilemma"),
        ],
    },
    {
        "file": "anime-manga-t76-comic.md",
        "arc": "Anime & Manga Arc — Dive Into Otaku Japan",
        "arc_id": "anime-manga",
        "num": 76,
        "title": "Figure Store Dilemma",
        "color": "#EC4899",
        "setting": "Akihabara figure shop, glass display cases, limited edition boxes, price tags in yen",
        "focus": ["I can't decide what to buy.", "I'd rather A than B.", "I think I'll go with A."],
        "story": [
            ("Wall of anime figures.", "Nam: \"I can't decide what to buy — everything looks good.\""),
            ("Budget reality.", "Linh: \"Quality over quantity.\""),
            ("Nam compares two figures.", "Nam: \"I'd rather get one good figure than three cheap ones.\""),
            ("Limited edition spotted.", "Nam: \"I think I'll go with this limited edition.\""),
            ("Happy purchase.", "Cashier: \"Careful — box art is part of the value.\""),
            ("Hook.", "Next: Anime Talk at Team Lunch"),
        ],
    },
    {
        "file": "anime-manga-t77-comic.md",
        "arc": "Anime & Manga Arc — Dive Into Otaku Japan",
        "arc_id": "anime-manga",
        "num": 77,
        "title": "Anime Talk at Team Lunch",
        "color": "#EC4899",
        "setting": "Office lunch room, bento boxes, casual conversation, anime poster on Nam's phone wallpaper",
        "focus": ["I'm not really into A, but I love B.", "That sounds amazing.", "We should hang out at... sometime."],
        "story": [
            ("Lunch with colleagues.", "Kenji: \"Anyone watch anime lately?\""),
            ("Nam shares taste.", "Nam: \"I'm not really into sports anime, but I love slice-of-life.\""),
            ("Aoi recommends series.", "Aoi: \"Try this one — the Tokyo locations are real.\""),
            ("Nam reacts.", "Nam: \"Set in Shimokitazawa? That sounds amazing.\""),
            ("Plan weekend.", "Nam: \"We should hang out at Akihabara sometime.\""),
            ("Hook.", "Next: Anime & Manga Finale"),
        ],
    },
    {
        "file": "anime-manga-t78-comic.md",
        "arc": "Anime & Manga Arc — Dive Into Otaku Japan",
        "arc_id": "anime-manga",
        "num": 78,
        "title": "Anime & Manga Finale",
        "color": "#EC4899",
        "setting": "Akihabara night montage, manga cafe, figure bag, pilgrimage photo — neon otaku paradise",
        "focus": ["It was worth it.", "I'm glad that we shared our favorites.", "look forward to"],
        "story": [
            ("Montage: Akihabara, manga cafe, pilgrimage, figures.", "Nam's otaku weekend highlights"),
            ("Team shares favorite series.", "Everyone names their top anime"),
            ("Nam reflects.", "Nam: \"I'm glad that we shared our favorites — I learned new shows.\""),
            ("Worth it moment.", "Nam: \"It was worth it — Japan is anime heaven.\""),
            ("Future plan.", "Nam: \"I look forward to Comiket season next time.\""),
            ("Celebrate.", "Next: Nam's English journey continues…"),
        ],
    },
    # ── Japan Culture Arc 66–72 ──
    {
        "file": "japan-culture-t66-comic.md",
        "arc": "Japan Culture Arc — Explore Beyond the Guidebook",
        "arc_id": "japan-culture",
        "num": 66,
        "title": "Walk Me Through Shrine Etiquette",
        "color": "#DC2626",
        "setting": "Meiji Shrine or Fushimi Inari torii gates, stone path, warm afternoon light, traditional Japanese atmosphere",
        "focus": ["Can you walk me through how to pray at a shrine?", "Let me make sure I got this right.", "I'm not sure I understand this part."],
        "story": [
            ("Nam and Linh arrive at a shrine.", "Nam: \"It's my first time at a real shrine.\""),
            ("Torii gate and purification fountain.", "Linh: \"Can you walk me through how to pray at a shrine?\""),
            ("Kenji demonstrates bow and clap.", "Kenji: \"Two bows, two claps, one bow — like this.\""),
            ("Nam tries and checks understanding.", "Nam: \"Let me make sure I got this right.\""),
            ("Small mistake on order.", "Nam: \"I'm not sure I understand this part — the clap timing?\""),
            ("Hook.", "Next: The Onsen Question"),
        ],
    },
    {
        "file": "japan-culture-t67-comic.md",
        "arc": "Japan Culture Arc — Explore Beyond the Guidebook",
        "arc_id": "japan-culture",
        "num": 67,
        "title": "The Onsen Question",
        "color": "#DC2626",
        "setting": "Traditional ryokan onsen entrance, wooden signs, steam, tatami changing room, calm hot-spring atmosphere",
        "focus": ["I'm not sure if I should...", "What do you mean by...?", "Could you explain this part again?"],
        "story": [
            ("Team weekend trip to onsen town.", "Signs: wash before bath, no tattoos rule"),
            ("Nam reads rules nervously.", "Nam: \"I'm not sure if I should enter before or after dinner.\""),
            ("Aoi explains konyoku vs gender-separated.", "Aoi: \"What do you mean by 'family bath' here?\""),
            ("Staff explains towel etiquette.", "Staff: \"Small towel stays out of the water.\""),
            ("Nam asks again politely.", "Nam: \"Could you explain this part again?\""),
            ("Hook.", "Next: Izakaya After Work"),
        ],
    },
    {
        "file": "japan-culture-t68-comic.md",
        "arc": "Japan Culture Arc — Explore Beyond the Guidebook",
        "arc_id": "japan-culture",
        "num": 68,
        "title": "Izakaya After Work",
        "color": "#DC2626",
        "setting": "Cozy Tokyo izakaya at night, red lanterns, wooden counter, yakitori and beer, warm after-work atmosphere",
        "focus": ["I'm excited about trying real izakaya food.", "That sounds amazing.", "I'm not really into raw fish, but..."],
        "story": [
            ("Friday after release — team heads to izakaya.", "Kenji: \"Celebration izakaya night!\""),
            ("Menu with unfamiliar dishes.", "Nam: \"I'm excited about trying real izakaya food.\""),
            ("Linh recommends yakitori set.", "Linh: \"Grilled chicken and edamame — that sounds amazing.\""),
            ("Nam sets food preference.", "Nam: \"I'm not really into raw fish, but I'll try the grilled stuff.\""),
            ("Kanpai toast.", "Team: \"Kanpai! Great release week!\""),
            ("Hook.", "Next: Cherry Blossom Dilemma"),
        ],
    },
    {
        "file": "japan-culture-t69-comic.md",
        "arc": "Japan Culture Arc — Explore Beyond the Guidebook",
        "arc_id": "japan-culture",
        "num": 69,
        "title": "Cherry Blossom Dilemma",
        "color": "#DC2626",
        "setting": "Tokyo cherry blossom season, Meguro River and Ueno Park photos on phone, pink petals, hanami picnic scene",
        "focus": ["I'm torn between A and B.", "I'm leaning toward A because...", "I think I'll go with A."],
        "story": [
            ("Spring hanami planning on Slack.", "Linh: \"Where should we do hanami this weekend?\""),
            ("Two options on screen.", "Nam: \"I'm torn between Ueno Park and Meguro River.\""),
            ("Crowd vs scenery debate.", "Aoi: \"Meguro is prettier at night.\""),
            ("Nam decides.", "Nam: \"I'm leaning toward Meguro because the lights look better.\""),
            ("Final choice.", "Nam: \"I think I'll go with Meguro River.\""),
            ("Hook.", "Next: What Is Omotenashi?"),
        ],
    },
    {
        "file": "japan-culture-t70-comic.md",
        "arc": "Japan Culture Arc — Explore Beyond the Guidebook",
        "arc_id": "japan-culture",
        "num": 70,
        "title": "What Is Omotenashi?",
        "color": "#DC2626",
        "setting": "Traditional Japanese inn lobby, staff bowing deeply, tea service, elegant hospitality details",
        "focus": ["I'm surprised that...", "That was worth it.", "I'm glad that we learned the custom first."],
        "story": [
            ("Ryokan check-in — staff bows deeply.", "Nam: \"I'm surprised that they bowed so low.\""),
            ("Kenji explains omotenashi.", "Kenji: \"It's thoughtful hospitality — no tip expected.\""),
            ("Tea and slippers detail.", "Linh: \"Every small detail feels intentional.\""),
            ("Nam reflects.", "Nam: \"I'm glad that we learned the custom first.\""),
            ("Evening kaiseki dinner.", "Nam: \"That was worth it — best meal of the trip.\""),
            ("Hook.", "Next: Summer Festival Night"),
        ],
    },
    {
        "file": "japan-culture-t71-comic.md",
        "arc": "Japan Culture Arc — Explore Beyond the Guidebook",
        "arc_id": "japan-culture",
        "num": 71,
        "title": "Summer Festival Night",
        "color": "#DC2626",
        "setting": "Asakusa summer matsuri at night, food stalls, yukata, paper lanterns, festival crowd energy",
        "focus": ["I'm looking for...", "How long does it take to get to...?", "That sounds amazing."],
        "story": [
            ("Team in yukata at festival.", "Nam: \"I'm looking for the takoyaki stall.\""),
            ("Checking train route on phone.", "Riku: \"How long does it take to get to Asakusa from here?\""),
            ("Goldfish scooping and drums.", "Linh: \"The taiko performance — that sounds amazing.\""),
            ("Fireworks in distance.", "Team watches together."),
            ("Nam buys festival snack.", "Nam: \"This is exactly the Japan experience I wanted.\""),
            ("Hook.", "Next: Japan Culture Finale"),
        ],
    },
    {
        "file": "japan-culture-t72-comic.md",
        "arc": "Japan Culture Arc — Explore Beyond the Guidebook",
        "arc_id": "japan-culture",
        "num": 72,
        "title": "Japan Culture Finale",
        "color": "#DC2626",
        "setting": "Montage: shrine, onsen, izakaya, hanami, matsuri — golden sunset over Tokyo skyline",
        "focus": ["It was worth it.", "I'm proud of myself.", "look forward to"],
        "story": [
            ("Montage of culture episodes.", "Shrine, onsen, izakaya, hanami, festival"),
            ("Team café debrief.", "Kenji: \"You handled every custom situation well.\""),
            ("Nam reflects.", "Nam: \"It was worth it — I feel more confident in Japan now.\""),
            ("Pride moment.", "Nam: \"I'm proud of myself for asking when I wasn't sure.\""),
            ("Future plans.", "Nam: \"I look forward to exploring more regions next season.\""),
            ("Celebrate.", "Next: Akihabara or Nakano Broadway?"),
        ],
    },
    # ── Anime & Manga Arc 73–78 ──
    {
        "file": "anime-manga-t73-comic.md",
        "arc": "Anime & Manga Arc — Dive Into Otaku Japan",
        "arc_id": "anime-manga",
        "num": 73,
        "title": "Akihabara or Nakano Broadway?",
        "color": "#EC4899",
        "setting": "Split scene: Akihabara neon electric town vs Nakano Broadway Sun Mall, colorful anime billboards",
        "focus": ["I'm torn between A and B.", "I'm more interested in A.", "A makes more sense to me."],
        "story": [
            ("Saturday otaku trip planning.", "Nam: \"Where should we go first?\""),
            ("Two districts on map.", "Nam: \"I'm torn between Akihabara and Nakano Broadway.\""),
            ("Linh wants rare manga.", "Linh: \"I'm more interested in Nakano for vintage manga.\""),
            ("Nam decides for figures.", "Nam: \"Akihabara makes more sense to me for my first visit.\""),
            ("Train to Akihabara.", "Team: \"Let's do Nakano tomorrow!\""),
            ("Hook.", "Next: My First Manga Cafe"),
        ],
    },
    {
        "file": "anime-manga-t74-comic.md",
        "arc": "Anime & Manga Arc — Dive Into Otaku Japan",
        "arc_id": "anime-manga",
        "num": 74,
        "title": "My First Manga Cafe",
        "color": "#EC4899",
        "setting": "Japanese manga cafe interior, cubicle booths, manga shelves, drink bar, locker area",
        "focus": ["Can you walk me through how a manga cafe works?", "Could you show me how to use the locker?", "I'm not sure I understand the time system."],
        "story": [
            ("Nam enters manga cafe nervously.", "Sign: pay by time, free drink bar"),
            ("Asks staff for help.", "Nam: \"Can you walk me through how a manga cafe works?\""),
            ("Locker and shoes.", "Staff: \"Shoes off, locker key here.\""),
            ("Nam asks about locker.", "Nam: \"Could you show me how to use the locker?\""),
            ("Hourly billing confusion.", "Nam: \"I'm not sure I understand the time system.\""),
            ("Hook.", "Next: Anime Pilgrimage Day"),
        ],
    },
    {
        "file": "anime-manga-t75-comic.md",
        "arc": "Anime & Manga Arc — Dive Into Otaku Japan",
        "arc_id": "anime-manga",
        "num": 75,
        "title": "Anime Pilgrimage Day",
        "color": "#EC4899",
        "setting": "Real-life anime location in Tokyo suburb, recognizable café staircase, fans taking photos",
        "focus": ["I'm really into this anime.", "I'm excited about finding the café from the scene.", "That sounds amazing."],
        "story": [
            ("Nam shows anime screenshot on phone.", "Nam: \"I'm really into this anime — I want the real location.\""),
            ("Train to pilgrimage spot.", "Linh: \"Fans call this a 'seichi junrei' spot.\""),
            ("Finding the famous staircase.", "Nam: \"I'm excited about finding the café from the scene.\""),
            ("Photo moment.", "Riku: \"Recreating the scene — that sounds amazing.\""),
            ("Other fans chatting in English.", "Fan: \"Which episode is this from?\""),
            ("Hook.", "Next: Figure Store Dilemma"),
        ],
    },
    {
        "file": "anime-manga-t76-comic.md",
        "arc": "Anime & Manga Arc — Dive Into Otaku Japan",
        "arc_id": "anime-manga",
        "num": 76,
        "title": "Figure Store Dilemma",
        "color": "#EC4899",
        "setting": "Akihabara figure shop, glass display cases, limited edition boxes, price tags in yen",
        "focus": ["I can't decide what to buy.", "I'd rather A than B.", "I think I'll go with A."],
        "story": [
            ("Wall of anime figures.", "Nam: \"I can't decide what to buy — everything looks good.\""),
            ("Budget reality.", "Linh: \"Quality over quantity.\""),
            ("Nam compares two figures.", "Nam: \"I'd rather get one good figure than three cheap ones.\""),
            ("Limited edition spotted.", "Nam: \"I think I'll go with this limited edition.\""),
            ("Happy purchase.", "Cashier: \"Careful — box art is part of the value.\""),
            ("Hook.", "Next: Anime Talk at Team Lunch"),
        ],
    },
    {
        "file": "anime-manga-t77-comic.md",
        "arc": "Anime & Manga Arc — Dive Into Otaku Japan",
        "arc_id": "anime-manga",
        "num": 77,
        "title": "Anime Talk at Team Lunch",
        "color": "#EC4899",
        "setting": "Office lunch room, bento boxes, casual conversation, anime poster on Nam's phone wallpaper",
        "focus": ["I'm not really into A, but I love B.", "That sounds amazing.", "We should hang out at... sometime."],
        "story": [
            ("Lunch with colleagues.", "Kenji: \"Anyone watch anime lately?\""),
            ("Nam shares taste.", "Nam: \"I'm not really into sports anime, but I love slice-of-life.\""),
            ("Aoi recommends series.", "Aoi: \"Try this one — the Tokyo locations are real.\""),
            ("Nam reacts.", "Nam: \"Set in Shimokitazawa? That sounds amazing.\""),
            ("Plan weekend.", "Nam: \"We should hang out at Akihabara sometime.\""),
            ("Hook.", "Next: Anime & Manga Finale"),
        ],
    },
    {
        "file": "anime-manga-t78-comic.md",
        "arc": "Anime & Manga Arc — Dive Into Otaku Japan",
        "arc_id": "anime-manga",
        "num": 78,
        "title": "Anime & Manga Finale",
        "color": "#EC4899",
        "setting": "Akihabara night montage, manga cafe, figure bag, pilgrimage photo — neon otaku paradise",
        "focus": ["It was worth it.", "I'm glad that we shared our favorites.", "look forward to"],
        "story": [
            ("Montage: Akihabara, manga cafe, pilgrimage, figures.", "Nam's otaku weekend highlights"),
            ("Team shares favorite series.", "Everyone names their top anime"),
            ("Nam reflects.", "Nam: \"I'm glad that we shared our favorites — I learned new shows.\""),
            ("Worth it moment.", "Nam: \"It was worth it — Japan is anime heaven.\""),
            ("Future plan.", "Nam: \"I look forward to Comiket season next time.\""),
            ("Celebrate.", "Next: Nam's English journey continues…"),
        ],
    },
    # ── Interview & Career Arc 79–84 ──
    {
        "file": "interview-career-t79-comic.md",
        "arc": "Interview & Career Arc — Land Your Next Role",
        "arc_id": "interview-career",
        "num": 79,
        "title": "The First Phone Screen",
        "color": "#F59E0B",
        "focus": ["I'm looking for a role where...", "I see myself growing in...", "What attracted me to this company is..."],
        "setting": "Quiet Tokyo apartment, laptop video call, professional but warm lighting",
        "story": [
            ("Nam prepares for recruiter call.", "Recruiter: \"Tell me a bit about yourself and what you're looking for.\""),
            ("Nam answers confidently.", "Nam: \"I'm looking for a role where I can grow as a full-stack engineer.\""),
            ("Recruiter asks about goals.", "Nam: \"I see myself growing in system design and cross-team communication.\""),
            ("Company culture question.", "Recruiter: \"Why our company?\""),
            ("Nam explains motivation.", "Nam: \"What attracted me to this company is the global product impact.\""),
            ("Positive close.", "Recruiter: \"Great — let's schedule the technical round.\""),
            ("Hook.", "Next: Tell Me About a Time When..."),
        ],
    },
    {
        "file": "interview-career-t80-comic.md",
        "arc": "Interview & Career Arc — Land Your Next Role",
        "arc_id": "interview-career",
        "num": 80,
        "title": "Tell Me About a Time When...",
        "color": "#F59E0B",
        "focus": ["Tell me about a time when...", "One challenge I faced was...", "What I learned from that was..."],
        "setting": "Video interview, whiteboard notes visible, STAR method sticky notes",
        "story": [
            ("Interviewer asks behavioral question.", "Interviewer: \"Tell me about a time when you handled a production incident.\""),
            ("Nam sets the scene.", "Nam: \"One challenge I faced was a payment outage before a demo.\""),
            ("Nam explains actions.", "Nam: \"I walked the team through the logs and we rolled back safely.\""),
            ("Result.", "Nam: \"The result was that we saved the demo and added better monitoring.\""),
            ("Lesson learned.", "Nam: \"What I learned from that was to always run through the main flow early.\""),
            ("Interviewer nods.", "Interviewer: \"Strong example — clear structure.\""),
            ("Hook.", "Next: Why Do You Want This Role?"),
        ],
    },
    {
        "file": "interview-career-t81-comic.md",
        "arc": "Interview & Career Arc — Land Your Next Role",
        "arc_id": "interview-career",
        "num": 81,
        "title": "Why Do You Want This Role?",
        "color": "#F59E0B",
        "focus": ["Why I'm interested in this role is...", "I'm looking for a role where...", "work closely with"],
        "setting": "Office interview room, Tokyo skyline, hiring manager and Nam",
        "story": [
            ("Classic interview question.", "Manager: \"Why do you want this role?\""),
            ("Nam connects motivation to role.", "Nam: \"Why I'm interested in this role is the chance to own backend services at scale.\""),
            ("Team fit.", "Nam: \"I'm looking for a role where I can work closely with product and QA.\""),
            ("Manager asks about growth.", "Manager: \"Where do you see yourself in two years?\""),
            ("Nam answers.", "Nam: \"I see myself growing into a tech lead who bridges teams.\""),
            ("Positive signal.", "Manager: \"That's exactly what we need on this team.\""),
            ("Hook.", "Next: The Salary Question"),
        ],
    },
    {
        "file": "interview-career-t82-comic.md",
        "arc": "Interview & Career Arc — Land Your Next Role",
        "arc_id": "interview-career",
        "num": 82,
        "title": "The Salary Question",
        "color": "#F59E0B",
        "focus": ["I'd need at least...", "Would it be possible to...?", "I'm looking for a range of..."],
        "setting": "Calm negotiation call, notebook with salary research, professional tone",
        "story": [
            ("Recruiter brings up compensation.", "Recruiter: \"What are your salary expectations?\""),
            ("Nam answers professionally.", "Nam: \"I'm looking for a range of ¥8–9M based on my experience.\""),
            ("Recruiter pushes back slightly.", "Recruiter: \"Our initial offer might be lower.\""),
            ("Nam negotiates politely.", "Nam: \"Would it be possible to include a signing bonus?\""),
            ("Nam sets minimum.", "Nam: \"I'd need at least ¥7.5M to make the move worthwhile.\""),
            ("Agreement in principle.", "Recruiter: \"Let me check with HR and get back to you.\""),
            ("Hook.", "Next: Questions for the Interviewer"),
        ],
    },
    {
        "file": "interview-career-t83-comic.md",
        "arc": "Interview & Career Arc — Land Your Next Role",
        "arc_id": "interview-career",
        "num": 83,
        "title": "Questions for the Interviewer",
        "color": "#F59E0B",
        "focus": ["Do you have any questions for us?", "What does success look like in this role?", "How does the team collaborate?"],
        "setting": "Final interview round, friendly panel of two engineers",
        "story": [
            ("Panel opens floor.", "Panel: \"Do you have any questions for us?\""),
            ("Nam asks about success.", "Nam: \"What does success look like in this role in the first six months?\""),
            ("Panel answers.", "Engineer: \"Shipping two features independently and mentoring juniors.\""),
            ("Nam asks about collaboration.", "Nam: \"How does the team collaborate across time zones?\""),
            ("Culture insight.", "Engineer: \"We rely on async updates and weekly design reviews.\""),
            ("Nam shows interest.", "Nam: \"That aligns with how I work — thank you for sharing.\""),
            ("Hook.", "Next: Interview & Career Finale"),
        ],
    },
    {
        "file": "interview-career-t84-comic.md",
        "arc": "Interview & Career Arc — Land Your Next Role",
        "arc_id": "interview-career",
        "num": 84,
        "title": "Interview & Career Finale",
        "color": "#F59E0B",
        "focus": ["Tell me about a time when...", "What I learned from that was...", "I'm looking for a role where...", "look forward to"],
        "setting": "Nam receives offer email, team celebrates at café",
        "story": [
            ("Offer email on phone.", "Nam: \"I got the offer — they liked my STAR stories.\""),
            ("Kenji congratulates.", "Kenji: \"Your Tell me about a time when answers were clear and structured.\""),
            ("Nam reflects.", "Nam: \"What I learned from that was to prepare three strong stories.\""),
            ("Future vision.", "Nam: \"I'm looking for a role where I can keep growing as a bridge engineer.\""),
            ("Celebration.", "Linh: \"You earned it — your English in interviews leveled up.\""),
            ("Forward look.", "Nam: \"I look forward to starting next month.\""),
            ("Hook.", "Next: The Tight Deadline"),
        ],
    },
    # ── Negotiation & Boundaries Arc 85–89 ──
    {
        "file": "negotiation-boundaries-t85-comic.md",
        "arc": "Negotiation & Boundaries Arc — Push Back Like a Pro",
        "arc_id": "negotiation-boundaries",
        "num": 85,
        "title": "The Tight Deadline",
        "color": "#14B8A6",
        "focus": ["I'm concerned that the timeline is too tight.", "Could we push the deadline back by...?", "weigh up"],
        "story": [
            ("PM sets aggressive deadline.", "PM: \"We need the full feature by Friday.\""),
            ("Nam raises concern.", "Nam: \"I'm concerned that the timeline is too tight for proper QA.\""),
            ("Whiteboard trade-offs.", "Aoi: \"We need to weigh up speed vs stability.\""),
            ("Nam proposes alternative.", "Nam: \"Could we push the deadline back by three days?\""),
            ("PM considers.", "PM: \"What if we ship MVP Friday and polish next week?\""),
            ("Agreement.", "Nam: \"That makes more sense — let's scope down the MVP.\""),
            ("Hook.", "Next: Would It Be Possible To...?"),
        ],
    },
    {
        "file": "negotiation-boundaries-t86-comic.md",
        "arc": "Negotiation & Boundaries Arc — Push Back Like a Pro",
        "arc_id": "negotiation-boundaries",
        "num": 86,
        "title": "Would It Be Possible To...?",
        "color": "#14B8A6",
        "focus": ["Would it be possible to...?", "I'd be more comfortable if we...", "What would it take to...?"],
        "story": [
            ("Stakeholder request.", "PM: \"Can you also add admin dashboard this sprint?\""),
            ("Nam negotiates politely.", "Nam: \"Would it be possible to move that to next sprint?\""),
            ("Nam sets comfort boundary.", "Nam: \"I'd be more comfortable if we finish payment first.\""),
            ("PM asks what's needed.", "PM: \"What would it take to do both?\""),
            ("Nam explains resources.", "Nam: \"We'd need at least one more engineer or cut scope.\""),
            ("Compromise.", "PM: \"Fair — let's prioritize payment and plan admin for Q2.\""),
            ("Hook.", "Next: That's Outside the Scope"),
        ],
    },
    {
        "file": "negotiation-boundaries-t87-comic.md",
        "arc": "Negotiation & Boundaries Arc — Push Back Like a Pro",
        "arc_id": "negotiation-boundaries",
        "num": 87,
        "title": "That's Outside the Scope",
        "color": "#14B8A6",
        "focus": ["That's outside the original scope.", "I'd need at least...", "scope creep"],
        "story": [
            ("New request in meeting.", "PM: \"While you're at it, add multi-currency support too.\""),
            ("Nam flags scope.", "Nam: \"That's outside the original scope for this release.\""),
            ("Kenji supports.", "Kenji: \"Classic scope creep — let's document the change.\""),
            ("Nam estimates.", "Nam: \"I'd need at least two extra weeks for multi-currency.\""),
            ("PM rethinks.", "PM: \"Okay — let's create a separate ticket and timeline.\""),
            ("Clear boundary.", "Nam: \"Happy to help, but we'll need a new sprint plan.\""),
            ("Hook.", "Next: Push Back on Scope Creep"),
        ],
    },
    {
        "file": "negotiation-boundaries-t88-comic.md",
        "arc": "Negotiation & Boundaries Arc — Push Back Like a Pro",
        "arc_id": "negotiation-boundaries",
        "num": 88,
        "title": "Push Back on Scope Creep",
        "color": "#14B8A6",
        "focus": ["Let me push back on that.", "I'm happy to help, but we'll need to...", "push back"],
        "story": [
            ("Slack message with extra asks.", "PM in Slack: \"Also refactor the whole module please.\""),
            ("Nam responds professionally.", "Nam: \"Let me push back on that for this week.\""),
            ("Nam offers alternative.", "Nam: \"I'm happy to help, but we'll need to split it into phases.\""),
            ("Kenji coaches.", "Kenji: \"Good push back — always tie it to timeline and risk.\""),
            ("PM accepts.", "PM: \"You're right. Phase 1 this sprint, refactor later.\""),
            ("Nam relieved.", "Nam: \"Setting boundaries saved us from another crunch week.\""),
            ("Hook.", "Next: Negotiation & Boundaries Finale"),
        ],
    },
    {
        "file": "negotiation-boundaries-t89-comic.md",
        "arc": "Negotiation & Boundaries Arc — Push Back Like a Pro",
        "arc_id": "negotiation-boundaries",
        "num": 89,
        "title": "Negotiation & Boundaries Finale",
        "color": "#14B8A6",
        "focus": ["Would it be possible to...?", "That's outside the original scope.", "set a boundary", "compromise on"],
        "story": [
            ("Retrospective on negotiation week.", "Kenji: \"You handled scope requests much better this sprint.\""),
            ("Nam summarizes skills.", "Nam: \"Would it be possible to... is my go-to opener now.\""),
            ("Boundary lesson.", "Aoi: \"Saying that's outside the original scope protects the team.\""),
            ("Compromise example.", "Nam: \"We compromised on MVP scope instead of crunching.\""),
            ("Team respect.", "Linh: \"Clear boundaries make QA planning easier too.\""),
            ("Confidence.", "Nam: \"I can push back without burning bridges.\""),
            ("Hook.", "Next: Preparing for the 1-on-1"),
        ],
    },
    # ── Feedback & 1-on-1 Arc 90–94 ──
    {
        "file": "giving-feedback-t90-comic.md",
        "arc": "Feedback & 1-on-1 Arc — Lead Through Conversations",
        "arc_id": "giving-feedback",
        "num": 90,
        "title": "Preparing for the 1-on-1",
        "color": "#A855F7",
        "focus": ["What would help you most right now?", "Let's set a goal for next week.", "check in with"],
        "setting": "Small meeting room, coffee cups, 1-on-1 agenda on laptop",
        "story": [
            ("Kenji opens 1-on-1.", "Kenji: \"What's on your mind this week?\""),
            ("Nam asks supportive question.", "Nam: \"What would help you most right now on the payment project?\""),
            ("Goal setting.", "Kenji: \"Let's set a goal for next week — ship the cache fix.\""),
            ("Nam commits to check in.", "Nam: \"I'll check in with QA before we deploy.\""),
            ("Mutual support.", "Kenji: \"And I'll check in with you on the design doc.\""),
            ("Productive close.", "Both: \"Good 1-on-1 — clear next steps.\""),
            ("Hook.", "Next: One Thing That Went Well Was..."),
        ],
    },
    {
        "file": "giving-feedback-t91-comic.md",
        "arc": "Feedback & 1-on-1 Arc — Lead Through Conversations",
        "arc_id": "giving-feedback",
        "num": 91,
        "title": "One Thing That Went Well Was...",
        "color": "#A855F7",
        "focus": ["One thing that went well was...", "I appreciate how you handled...", "One area to improve would be..."],
        "story": [
            ("Nam reviews junior's PR.", "Nam: \"One thing that went well was your test coverage.\""),
            ("Positive reinforcement.", "Nam: \"I appreciate how you handled the review comments quickly.\""),
            ("Constructive note.", "Nam: \"One area to improve would be the PR description summary.\""),
            ("Junior listens.", "Junior: \"Thanks — I'll add a summary section next time.\""),
            ("Balanced feedback.", "Aoi: \"Good sandwich — positive, improve, support.\""),
            ("Junior motivated.", "Junior: \"That feedback felt clear, not harsh.\""),
            ("Hook.", "Next: I'd Suggest Trying..."),
        ],
    },
    {
        "file": "giving-feedback-t92-comic.md",
        "arc": "Feedback & 1-on-1 Arc — Lead Through Conversations",
        "arc_id": "giving-feedback",
        "num": 92,
        "title": "I'd Suggest Trying...",
        "color": "#A855F7",
        "focus": ["I'd suggest trying...", "Have you considered...?", "step up"],
        "story": [
            ("Junior stuck on bug.", "Junior: \"I've been debugging this API issue for hours.\""),
            ("Nam offers suggestion.", "Nam: \"I'd suggest trying to reproduce it with a smaller payload first.\""),
            ("Alternative idea.", "Nam: \"Have you considered checking the cache headers?\""),
            ("Junior tries.", "Junior: \"Oh — that fixed it. Thanks!\""),
            ("Growth moment.", "Kenji: \"Good mentoring — you helped them step up independently.\""),
            ("Nam smiles.", "Nam: \"Suggesting beats solving it for them.\""),
            ("Hook.", "Next: How Can I Support You?"),
        ],
    },
    {
        "file": "giving-feedback-t93-comic.md",
        "arc": "Feedback & 1-on-1 Arc — Lead Through Conversations",
        "arc_id": "giving-feedback",
        "num": 93,
        "title": "How Can I Support You?",
        "color": "#A855F7",
        "focus": ["How can I support you?", "What would help you most right now?", "grow into"],
        "story": [
            ("Junior looks stressed.", "Junior: \"I'm worried about the upcoming demo.\""),
            ("Nam asks support question.", "Nam: \"How can I support you before demo day?\""),
            ("Specific help.", "Junior: \"A mock run-through would help most.\""),
            ("Nam offers time.", "Nam: \"Let's do a dry run tomorrow at 3pm.\""),
            ("Kenji observes.", "Kenji: \"That question opens space for real support.\""),
            ("Growth talk.", "Nam: \"You're growing into a confident presenter.\""),
            ("Hook.", "Next: Feedback & 1-on-1 Finale"),
        ],
    },
    {
        "file": "giving-feedback-t94-comic.md",
        "arc": "Feedback & 1-on-1 Arc — Lead Through Conversations",
        "arc_id": "giving-feedback",
        "num": 94,
        "title": "Feedback & 1-on-1 Finale",
        "color": "#A855F7",
        "focus": ["One thing that went well was...", "I'd suggest trying...", "How can I support you?", "follow up on"],
        "story": [
            ("Team retro on feedback culture.", "Kenji: \"1-on-1s feel more useful lately.\""),
            ("Nam shares pattern.", "Nam: \"One thing that went well was asking How can I support you?\""),
            ("Junior thanks Nam.", "Junior: \"I'd suggest trying mock demos — that changed everything for me.\""),
            ("Follow up.", "Nam: \"I'll follow up on your growth plan next month.\""),
            ("Leadership growth.", "Aoi: \"You're leading through conversations, not commands.\""),
            ("Nam proud.", "Nam: \"Feedback English is a skill — and I'm getting better.\""),
            ("Hook.", "Next: Structuring the Demo"),
        ],
    },
    # ── Presentation & Pitch Arc 95–99 ──
    {
        "file": "presentation-pitch-t95-comic.md",
        "arc": "Presentation & Pitch Arc — Demo Like a Pro",
        "arc_id": "presentation-pitch",
        "num": 95,
        "title": "Structuring the Demo",
        "color": "#F97316",
        "focus": ["I'll keep this brief.", "The main problem we're solving is...", "To summarize..."],
        "setting": "Conference room, projector, demo slides on screen",
        "story": [
            ("Nam prepares slide outline.", "Aoi: \"Start with the problem, not the code.\""),
            ("Opening line.", "Nam: \"I'll keep this brief — three parts: problem, solution, results.\""),
            ("Problem slide.", "Nam: \"The main problem we're solving is failed checkouts at peak traffic.\""),
            ("Solution slide.", "Nam: \"We added caching and a retry queue.\""),
            ("Summary.", "Nam: \"To summarize — 40% faster and 99.9% success rate.\""),
            ("Kenji approves.", "Kenji: \"Clear structure — ready for stakeholders.\""),
            ("Hook.", "Next: Let Me Walk You Through the Demo"),
        ],
    },
    {
        "file": "presentation-pitch-t96-comic.md",
        "arc": "Presentation & Pitch Arc — Demo Like a Pro",
        "arc_id": "presentation-pitch",
        "num": 96,
        "title": "Let Me Walk You Through the Demo",
        "color": "#F97316",
        "focus": ["Let me walk you through...", "As you can see on this slide...", "run through"],
        "story": [
            ("Stakeholder demo begins.", "PM: \"Show us the new checkout flow.\""),
            ("Nam opens demo.", "Nam: \"Let me walk you through the happy path first.\""),
            ("Screen share.", "Nam: \"As you can see on this slide, latency dropped after caching.\""),
            ("Live demo.", "Nam: \"I'll run through a test purchase now.\""),
            ("Success.", "Checkout completes — team claps"),
            ("PM impressed.", "PM: \"Clean demo — very easy to follow.\""),
            ("Hook.", "Next: The Key Takeaway Is..."),
        ],
    },
    {
        "file": "presentation-pitch-t97-comic.md",
        "arc": "Presentation & Pitch Arc — Demo Like a Pro",
        "arc_id": "presentation-pitch",
        "num": 97,
        "title": "The Key Takeaway Is...",
        "color": "#F97316",
        "focus": ["The key takeaway is...", "Here's what changed since last time.", "break down"],
        "story": [
            ("Investor asks for summary.", "Investor: \"What's the one thing we should remember?\""),
            ("Nam delivers takeaway.", "Nam: \"The key takeaway is reliability under traffic spikes.\""),
            ("Progress update.", "Nam: \"Here's what changed since last time — we cut errors by half.\""),
            ("Break down metrics.", "Nam: \"Let me break down the numbers on this chart.\""),
            ("Investor satisfied.", "Investor: \"Clear takeaway — I get the business impact.\""),
            ("Kenji proud.", "Kenji: \"Strong close — always land the takeaway.\""),
            ("Hook.", "Next: Handling Tough Questions"),
        ],
    },
    {
        "file": "presentation-pitch-t98-comic.md",
        "arc": "Presentation & Pitch Arc — Demo Like a Pro",
        "arc_id": "presentation-pitch",
        "num": 98,
        "title": "Handling Tough Questions",
        "color": "#F97316",
        "focus": ["Any questions on this part?", "That's a great question — let me...", "circle back"],
        "story": [
            ("Nam opens Q&A.", "Nam: \"Any questions on this part before we wrap up?\""),
            ("Tough question.", "Investor: \"What if traffic grows 10x next month?\""),
            ("Nam pauses calmly.", "Nam: \"That's a great question — let me show our scaling plan.\""),
            ("Partial answer.", "Nam: \"We can handle 3x today; for 10x we need the queue migration.\""),
            ("Circle back.", "Nam: \"I'll circle back with a detailed capacity doc by Friday.\""),
            ("Respect earned.", "Investor: \"Honest answer — I appreciate the transparency.\""),
            ("Hook.", "Next: Presentation & Pitch Finale"),
        ],
    },
    {
        "file": "presentation-pitch-t99-comic.md",
        "arc": "Presentation & Pitch Arc — Demo Like a Pro",
        "arc_id": "presentation-pitch",
        "num": 99,
        "title": "Presentation & Pitch Finale",
        "color": "#F97316",
        "focus": ["Let me walk you through...", "The key takeaway is...", "Any questions on this part?", "look forward to"],
        "story": [
            ("Demo success celebration.", "Team high-five after investor meeting"),
            ("Kenji debrief.", "Kenji: \"Your Let me walk you through flow was smooth.\""),
            ("Takeaway praise.", "PM: \"The key takeaway is line landed perfectly.\""),
            ("Q&A growth.", "Nam: \"I handled tough questions without panicking.\""),
            ("Future pitch.", "Nam: \"I look forward to the product launch demo next month.\""),
            ("Confidence.", "Nam: \"Presentation English — unlocked.\""),
            ("Hook.", "Next: The War Room"),
        ],
    },
    # ── Incident & Postmortem Arc 100–104 ──
    {
        "file": "incident-postmortem-t100-comic.md",
        "arc": "Incident & Postmortem Arc — Blameless Communication",
        "arc_id": "incident-postmortem",
        "num": 100,
        "title": "The War Room",
        "color": "#DC2626",
        "focus": ["What we know so far is...", "Let's focus on the facts, not blame.", "dig into"],
        "setting": "Dim war room, multiple monitors, incident channel on Slack, urgent but calm",
        "story": [
            ("Alert fires at night.", "PagerDuty: \"Checkout error rate > 15%\""),
            ("Kenji opens war room.", "Kenji: \"Let's focus on the facts, not blame — status first.\""),
            ("Nam gives update.", "Nam: \"What we know so far is API timeouts on payment service.\""),
            ("Team assigns roles.", "Aoi: \"I'll dig into the database metrics.\""),
            ("Linh checks QA.", "Linh: \"Last deploy was 2 hours ago — possible correlation.\""),
            ("Calm coordination.", "Kenji: \"Good — keep updates every 15 minutes.\""),
            ("Hook.", "Next: What We Know So Far Is..."),
        ],
    },
    {
        "file": "incident-postmortem-t101-comic.md",
        "arc": "Incident & Postmortem Arc — Blameless Communication",
        "arc_id": "incident-postmortem",
        "num": 101,
        "title": "What We Know So Far Is...",
        "color": "#DC2626",
        "focus": ["What we know so far is...", "The impact was that...", "The timeline of events was..."],
        "story": [
            ("Stakeholder joins call.", "PM: \"What's the customer impact?\""),
            ("Nam status update.", "Nam: \"What we know so far is 12% of checkouts are failing.\""),
            ("Impact statement.", "Nam: \"The impact was that EU users couldn't complete purchases.\""),
            ("Timeline.", "Nam: \"The timeline of events was: deploy at 8pm, errors at 8:45pm.\""),
            ("Mitigation.", "Kenji: \"We rolled back at 9:10pm — errors dropping now.\""),
            ("PM relieved.", "PM: \"Clear update — thanks for the timeline.\""),
            ("Hook.", "Next: Root Cause Analysis"),
        ],
    },
    {
        "file": "incident-postmortem-t102-comic.md",
        "arc": "Incident & Postmortem Arc — Blameless Communication",
        "arc_id": "incident-postmortem",
        "num": 102,
        "title": "Root Cause Analysis",
        "color": "#DC2626",
        "focus": ["Root cause appears to be...", "It seems like...", "This might be caused by..."],
        "story": [
            ("Post-rollback analysis.", "Aoi: \"Logs show cache invalidation errors.\""),
            ("Nam hypothesis.", "Nam: \"Root cause appears to be stale cache keys after deploy.\""),
            ("Supporting evidence.", "Nam: \"It seems like the new TTL config wasn't applied.\""),
            ("Linh adds.", "Linh: \"This might be caused by a missing env variable in staging.\""),
            ("Kenji confirms.", "Kenji: \"Let's verify before we finalize the postmortem.\""),
            ("No blame.", "Kenji: \"Process gap, not person fault.\""),
            ("Hook.", "Next: Action Items Going Forward"),
        ],
    },
    {
        "file": "incident-postmortem-t103-comic.md",
        "arc": "Incident & Postmortem Arc — Blameless Communication",
        "arc_id": "incident-postmortem",
        "num": 103,
        "title": "Action Items Going Forward",
        "color": "#DC2626",
        "focus": ["Action items going forward...", "We mitigated the issue by...", "To prevent this from happening again..."],
        "story": [
            ("Postmortem doc on screen.", "Title: Checkout Incident — Action Items"),
            ("Mitigation recap.", "Nam: \"We mitigated the issue by rolling back within 25 minutes.\""),
            ("Prevention.", "Nam: \"To prevent this from happening again, we'll add a cache integration test.\""),
            ("Action list.", "Nam: \"Action items going forward: update runbook, fix env check, schedule game day.\""),
            ("Owner assignments.", "Aoi: \"I'll own the runbook update by Friday.\""),
            ("Team alignment.", "Kenji: \"Clear actions — no blame, just improvement.\""),
            ("Hook.", "Next: Postmortem Finale"),
        ],
    },
    {
        "file": "incident-postmortem-t104-comic.md",
        "arc": "Incident & Postmortem Arc — Blameless Communication",
        "arc_id": "incident-postmortem",
        "num": 104,
        "title": "Postmortem Finale",
        "color": "#DC2626",
        "focus": ["What we know so far is...", "Root cause appears to be...", "Action items going forward...", "follow up on"],
        "story": [
            ("Postmortem meeting with leadership.", "Leadership: \"Walk us through the incident briefly.\""),
            ("Nam summary.", "Nam: \"What we know so far is covered in the doc — 12% impact, 25-min recovery.\""),
            ("Root cause.", "Nam: \"Root cause appears to be cache config — fixed and tested.\""),
            ("Actions.", "Nam: \"Action items going forward are assigned with owners and dates.\""),
            ("Follow up.", "Kenji: \"I'll follow up on the game day drill next sprint.\""),
            ("Leadership praise.", "Leadership: \"Blameless, clear, actionable — well done.\""),
            ("Nam reflects.", "Nam: \"Incident English — I can handle the war room now.\""),
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
    setting = ep.get("setting", "Modern Tokyo office at night, Tokyo Tower visible through window")

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
Setting: {setting}

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

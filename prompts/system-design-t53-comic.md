# System Design Arc — Thinking Bigger — Episode 53: Cache or Database First?

> **File:** `system-design-t53-comic.md` · **Arc ID:** `system-design` · **Màu:** `#8B5CF6`
> **Output:** `images/comics/system-design/tập-53/system-design-tap53-cache-or-database-first.png`
> **Attach:** `prompts/00-character-bible.md` + `prompts/00-layout-guide.md` + style ref image
> **Cách tạo:** Copy **PROMPT FULL PAGE** → Cursor Generate Image (hoặc ChatGPT)

**Slug gợi ý:** `cache-or-database-first`

---

## Story beats

- **Panel 1:** Scene. Dialogue: Nam: "The issue is that every request hits the database."
- **Panel 2:** Scene. Dialogue: Aoi: "Redis can act as a cache layer here."
- **Panel 3:** Scene. Dialogue: Nam: "It seems like we're not caching user profile data."
- **Panel 4:** Scene. Dialogue: Linh: "What if the cache is stale?"
- **Panel 5:** Scene. Dialogue: Nam: "We could rely on Redis for reads and keep DB as source of truth."
- **Panel 6:** Scene. Dialogue: Hook: "Next: Queue Saves the Day"

---

## Canonical dialogue (synced from image — do not edit by hand)

```json
[
  {
    "panel": 1,
    "speaker": "Nam",
    "text": "The issue is that every request hits the database."
  },
  {
    "panel": 2,
    "speaker": "Aoi",
    "text": "Redis can act as a cache layer here."
  },
  {
    "panel": 3,
    "speaker": "Nam",
    "text": "It seems like we're not caching user profile data."
  },
  {
    "panel": 4,
    "speaker": "Linh",
    "text": "What if the cache is stale?"
  },
  {
    "panel": 5,
    "speaker": "Nam",
    "text": "We could rely on Redis for reads and keep DB as source of truth."
  },
  {
    "panel": 6,
    "speaker": "Hook",
    "text": "Next: Queue Saves the Day"
  }
]
```

---

## ENGLISH FOCUS (phải có trong ảnh)

```
ENGLISH FOCUS
  1. "The issue is that..." = Vấn đề là...
  2. "It seems like..." = Có vẻ như...
  3. "rely on" = phụ thuộc vào / dựa vào
Tip: Use these patterns for system design communication.
```

**Next hook:** Next: Queue Saves the Day

---

## PROMPT FULL PAGE (copy-paste)

```
Draw ONE complete educational manga comic page — English Vault: Tokyo Debug Chronicles.

ARC: System Design Arc — Thinking Bigger
EPISODE 53: Cache or Database First?
Accent color: #8B5CF6

STYLE: Modern anime manga educational webcomic, clean cel-shading, Tokyo office at night,
Tokyo Tower through window, cinematic blue-purple lighting, professional software team,
detailed UI monitors, high quality illustration, portrait comic page 1024x1536,
thin white panel borders, educational infographic style

CHARACTERS (consistent):
- Nam: young Vietnamese man, blue hoodie #2563EB, Junior Engineer badge
- Kenji: Tech Lead, dark shirt/suit, glasses
- Aoi: Senior Engineer, navy blazer, long black hair
- Linh: QA Engineer, gray hoodie
Setting: Modern Tokyo office at night, Tokyo Tower visible through window

LAYOUT: Header once at top → 6 numbered panels (2x3 grid) → ENGLISH FOCUS box (beige, full width) → NEXT hook box bottom-right

PANEL STORY:
Panel 1: Story beat. Speech: Nam: "The issue is that every request hits the database."
Panel 2: Story beat. Speech: Aoi: "Redis can act as a cache layer here."
Panel 3: Story beat. Speech: Nam: "It seems like we're not caching user profile data."
Panel 4: Story beat. Speech: Linh: "What if the cache is stale?"
Panel 5: Story beat. Speech: Nam: "We could rely on Redis for reads and keep DB as source of truth."
Panel 6: Story beat. Speech: Hook: "Next: Queue Saves the Day"

ENGLISH FOCUS box must list:
- "The issue is that..." = Vấn đề là...
- "It seems like..." = Có vẻ như...
- "rely on" = phụ thuộc vào / dựa vào

Highlight key phrases in BLUE BOLD inside speech bubbles.
All dialogue in ENGLISH. Vietnamese ONLY inside ENGLISH FOCUS meanings.

Footer next episode: Next: Queue Saves the Day

Portrait 1024x1536, high detail, same visual style as English Vault Tokyo Debug Chronicles series bible.
NO watermark. NO real company logos.
```

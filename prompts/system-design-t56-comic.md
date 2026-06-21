# System Design Arc — Thinking Bigger — Episode 56: Scale Under Pressure

> **File:** `system-design-t56-comic.md` · **Arc ID:** `system-design` · **Màu:** `#8B5CF6`
> **Output:** `images/comics/system-design/tập-56/system-design-tap56-scale-under-pressure.png`
> **Attach:** `prompts/00-character-bible.md` + `prompts/00-layout-guide.md` + style ref image
> **Cách tạo:** Copy **PROMPT FULL PAGE** → Cursor Generate Image (hoặc ChatGPT)

**Slug gợi ý:** `scale-under-pressure`

---

## Story beats

- **Panel 1:** Scene. Dialogue: Kenji: "Black Friday scale — we're 5x normal traffic."
- **Panel 2:** Scene. Dialogue: Nam: "It comes down to cost vs response time."
- **Panel 3:** Scene. Dialogue: Aoi: "Horizontal scaling buys time if stateless."
- **Panel 4:** Scene. Dialogue: Nam: "I'd opt for scaling out the API tier first."
- **Panel 5:** Scene. Dialogue: Kenji: "We need to weigh up DB connection limits too."
- **Panel 6:** Scene. Dialogue: Hook: "Next: The Cost of Overengineering"

---

## Canonical dialogue (synced from image — do not edit by hand)

```json
[
  {
    "panel": 1,
    "speaker": "Kenji",
    "text": "Black Friday scale — we're 5x normal traffic."
  },
  {
    "panel": 2,
    "speaker": "Nam",
    "text": "It comes down to cost vs response time."
  },
  {
    "panel": 3,
    "speaker": "Aoi",
    "text": "Horizontal scaling buys time if stateless."
  },
  {
    "panel": 4,
    "speaker": "Nam",
    "text": "I'd opt for scaling out the API tier first."
  },
  {
    "panel": 5,
    "speaker": "Kenji",
    "text": "We need to weigh up DB connection limits too."
  },
  {
    "panel": 6,
    "speaker": "Hook",
    "text": "Next: The Cost of Overengineering"
  }
]
```

---

## ENGLISH FOCUS (phải có trong ảnh)

```
ENGLISH FOCUS
  1. "It comes down to..." = Vấn đề cốt lõi là...
  2. "We need to weigh up..." = Chúng ta cần cân nhắc...
  3. "I'd opt for..." = Tôi sẽ chọn...
Tip: Use these patterns for system design communication.
```

**Next hook:** Next: The Cost of Overengineering

---

## PROMPT FULL PAGE (copy-paste)

```
Draw ONE complete educational manga comic page — English Vault: Tokyo Debug Chronicles.

ARC: System Design Arc — Thinking Bigger
EPISODE 56: Scale Under Pressure
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
Panel 1: Story beat. Speech: Kenji: "Black Friday scale — we're 5x normal traffic."
Panel 2: Story beat. Speech: Nam: "It comes down to cost vs response time."
Panel 3: Story beat. Speech: Aoi: "Horizontal scaling buys time if stateless."
Panel 4: Story beat. Speech: Nam: "I'd opt for scaling out the API tier first."
Panel 5: Story beat. Speech: Kenji: "We need to weigh up DB connection limits too."
Panel 6: Story beat. Speech: Hook: "Next: The Cost of Overengineering"

ENGLISH FOCUS box must list:
- "It comes down to..." = Vấn đề cốt lõi là...
- "We need to weigh up..." = Chúng ta cần cân nhắc...
- "I'd opt for..." = Tôi sẽ chọn...

Highlight key phrases in BLUE BOLD inside speech bubbles.
All dialogue in ENGLISH. Vietnamese ONLY inside ENGLISH FOCUS meanings.

Footer next episode: Next: The Cost of Overengineering

Portrait 1024x1536, high detail, same visual style as English Vault Tokyo Debug Chronicles series bible.
NO watermark. NO real company logos.
```

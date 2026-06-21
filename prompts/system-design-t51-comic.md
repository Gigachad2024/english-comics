# System Design Arc — Thinking Bigger — Episode 51: The System Design Question

> **File:** `system-design-t51-comic.md` · **Arc ID:** `system-design` · **Màu:** `#8B5CF6`
> **Output:** `images/comics/system-design/tập-51/system-design-tap51-the-system-design-question.png`
> **Attach:** `prompts/00-character-bible.md` + `prompts/00-layout-guide.md` + style ref image
> **Cách tạo:** Copy **PROMPT FULL PAGE** → Cursor Generate Image (hoặc ChatGPT)

**Slug gợi ý:** `the-system-design-question`

---

## Story beats

- **Panel 1:** Scene. Dialogue: Kenji: "Can you walk us through how this would work at 10x traffic?"
- **Panel 2:** Scene. Dialogue: Nam: "I'm wondering if we should start with the current flow first."
- **Panel 3:** Scene. Dialogue: Aoi: "Good — let's map the read path vs write path."
- **Panel 4:** Scene. Dialogue: Linh: "What happens when checkout spikes?"
- **Panel 5:** Scene. Dialogue: Nam: "Could we start by identifying the single biggest bottleneck?"
- **Panel 6:** Scene. Dialogue: Hook: "Next: Monolith or Microservices?"

---

## Canonical dialogue (synced from image — do not edit by hand)

```json
[
  {
    "panel": 1,
    "speaker": "Kenji",
    "text": "Can you walk us through how this would work at 10x traffic?"
  },
  {
    "panel": 2,
    "speaker": "Nam",
    "text": "I'm wondering if we should start with the current flow first."
  },
  {
    "panel": 3,
    "speaker": "Aoi",
    "text": "Good — let's map the read path vs write path."
  },
  {
    "panel": 4,
    "speaker": "Linh",
    "text": "What happens when checkout spikes?"
  },
  {
    "panel": 5,
    "speaker": "Nam",
    "text": "Could we start by identifying the single biggest bottleneck?"
  },
  {
    "panel": 6,
    "speaker": "Hook",
    "text": "Next: Monolith or Microservices?"
  }
]
```

---

## ENGLISH FOCUS (phải có trong ảnh)

```
ENGLISH FOCUS
  1. "I'm wondering if..." = Tôi đang tự hỏi liệu...
  2. "Could we start by..." = Chúng ta có thể bắt đầu bằng...?
  3. "walk me through" = giải thích từng bước cho tôi
Tip: Use these patterns for system design communication.
```

**Next hook:** Next: Monolith or Microservices?

---

## PROMPT FULL PAGE (copy-paste)

```
Draw ONE complete educational manga comic page — English Vault: Tokyo Debug Chronicles.

ARC: System Design Arc — Thinking Bigger
EPISODE 51: The System Design Question
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
Panel 1: Story beat. Speech: Kenji: "Can you walk us through how this would work at 10x traffic?"
Panel 2: Story beat. Speech: Nam: "I'm wondering if we should start with the current flow first."
Panel 3: Story beat. Speech: Aoi: "Good — let's map the read path vs write path."
Panel 4: Story beat. Speech: Linh: "What happens when checkout spikes?"
Panel 5: Story beat. Speech: Nam: "Could we start by identifying the single biggest bottleneck?"
Panel 6: Story beat. Speech: Hook: "Next: Monolith or Microservices?"

ENGLISH FOCUS box must list:
- "I'm wondering if..." = Tôi đang tự hỏi liệu...
- "Could we start by..." = Chúng ta có thể bắt đầu bằng...?
- "walk me through" = giải thích từng bước cho tôi

Highlight key phrases in BLUE BOLD inside speech bubbles.
All dialogue in ENGLISH. Vietnamese ONLY inside ENGLISH FOCUS meanings.

Footer next episode: Next: Monolith or Microservices?

Portrait 1024x1536, high detail, same visual style as English Vault Tokyo Debug Chronicles series bible.
NO watermark. NO real company logos.
```

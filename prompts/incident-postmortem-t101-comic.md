# Incident & Postmortem Arc — Blameless Communication — Episode 101: What We Know So Far Is...

> **File:** `incident-postmortem-t101-comic.md` · **Arc ID:** `incident-postmortem` · **Màu:** `#DC2626`
> **Output:** `images/comics/incident-postmortem/tập-101/incident-postmortem-tap101-what-we-know-so-far-is.png`
> **Attach:** `prompts/00-character-bible.md` + `prompts/00-layout-guide.md` + style ref image
> **Cách tạo:** Copy **PROMPT FULL PAGE** → Cursor Generate Image (hoặc ChatGPT)

**Slug gợi ý:** `what-we-know-so-far-is`

---

## Story beats

- **Panel 1:** Scene. Dialogue: PM: "What's the customer impact?"
- **Panel 2:** Scene. Dialogue: Nam: "What we know so far is 12% of checkouts are failing."
- **Panel 3:** Scene. Dialogue: Nam: "The impact was that EU users couldn't complete purchases."
- **Panel 4:** Scene. Dialogue: Nam: "The timeline of events was: deploy at 8pm, errors at 8:45pm."
- **Panel 5:** Scene. Dialogue: Kenji: "We rolled back at 9:10pm — errors dropping now."
- **Panel 6:** Scene. Dialogue: PM: "Clear update — thanks for the timeline."

---

## Canonical dialogue (synced from image — do not edit by hand)

```json
[
  {
    "panel": 1,
    "speaker": "PM",
    "text": "What's the customer impact?"
  },
  {
    "panel": 2,
    "speaker": "Nam",
    "text": "What we know so far is 12% of checkouts are failing."
  },
  {
    "panel": 3,
    "speaker": "Nam",
    "text": "The impact was that EU users couldn't complete purchases."
  },
  {
    "panel": 4,
    "speaker": "Nam",
    "text": "The timeline of events was: deploy at 8pm, errors at 8:45pm."
  },
  {
    "panel": 5,
    "speaker": "Kenji",
    "text": "We rolled back at 9:10pm — errors dropping now."
  },
  {
    "panel": 6,
    "speaker": "PM",
    "text": "Clear update — thanks for the timeline."
  }
]
```

---

## ENGLISH FOCUS (phải có trong ảnh)

```
ENGLISH FOCUS
  1. "What we know so far is..." = Những gì chúng ta biết đến giờ là...
  2. "The impact was that..." = Tác động là...
  3. "The timeline of events was..." = Diễn biến theo thời gian là...
Tip: Use these patterns for incident postmortem communication.
```

**Next hook:** Next: Root Cause Analysis

---

## PROMPT FULL PAGE (copy-paste)

```
Draw ONE complete educational manga comic page — English Vault: Tokyo Debug Chronicles.

ARC: Incident & Postmortem Arc — Blameless Communication
EPISODE 101: What We Know So Far Is...
Accent color: #DC2626

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
Panel 1: Story beat. Speech: PM: "What's the customer impact?"
Panel 2: Story beat. Speech: Nam: "What we know so far is 12% of checkouts are failing."
Panel 3: Story beat. Speech: Nam: "The impact was that EU users couldn't complete purchases."
Panel 4: Story beat. Speech: Nam: "The timeline of events was: deploy at 8pm, errors at 8:45pm."
Panel 5: Story beat. Speech: Kenji: "We rolled back at 9:10pm — errors dropping now."
Panel 6: Story beat. Speech: PM: "Clear update — thanks for the timeline."

ENGLISH FOCUS box must list:
- "What we know so far is..." = Những gì chúng ta biết đến giờ là...
- "The impact was that..." = Tác động là...
- "The timeline of events was..." = Diễn biến theo thời gian là...

Highlight key phrases in BLUE BOLD inside speech bubbles.
All dialogue in ENGLISH. Vietnamese ONLY inside ENGLISH FOCUS meanings.

Footer next episode: Next: Root Cause Analysis

Portrait 1024x1536, high detail, same visual style as English Vault Tokyo Debug Chronicles series bible.
NO watermark. NO real company logos.
```

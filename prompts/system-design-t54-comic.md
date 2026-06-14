# System Design Arc — Thinking Bigger — Episode 54: Queue Saves the Day

> **File:** `system-design-t54-comic.md` · **Arc ID:** `system-design` · **Màu:** `#8B5CF6`
> **Output:** `images/comics/system-design/tập-54/system-design-tap54-queue-saves-the-day.png`
> **Attach:** `prompts/00-character-bible.md` + `prompts/00-layout-guide.md` + style ref image
> **Cách tạo:** Copy **PROMPT FULL PAGE** → Cursor Generate Image (hoặc ChatGPT)

**Slug gợi ý:** `queue-saves-the-day`

---

## Story beats

- **Panel 1:** Payment timeout alert. Dialogue: Nam: "This might be caused by synchronous email sending."
- **Panel 2:** Architecture: add message queue. Dialogue: Aoi: "Put heavy work on a queue — respond fast to users."
- **Panel 3:** SQS/Kafka style diagram. Dialogue: Nam: "I think we should move notifications to async processing."
- **Panel 4:** Before/after latency chart. Dialogue: Kenji: "Show the latency before and after."
- **Panel 5:** Deploy checklist. Dialogue: Nam: "Let's follow through on monitoring the queue depth."
- **Panel 6:** Hook. Dialogue: Next: API Gateway at Night

---

## ENGLISH FOCUS (phải có trong ảnh)

```
ENGLISH FOCUS
  1. "This might be caused by..." = Có thể do...
  2. "I think we should..." = Tôi nghĩ chúng ta nên...
  3. "follow through" = theo sát đến khi hoàn thành
Tip: Use these patterns for system design communication.
```

**Next hook:** Next: API Gateway at Night

---

## PROMPT FULL PAGE (copy-paste)

```
Draw ONE complete educational manga comic page — English Vault: Tokyo Debug Chronicles.

ARC: System Design Arc — Thinking Bigger
EPISODE 54: Queue Saves the Day
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
Panel 1: Payment timeout alert.. Speech: Nam: "This might be caused by synchronous email sending."
Panel 2: Architecture: add message queue.. Speech: Aoi: "Put heavy work on a queue — respond fast to users."
Panel 3: SQS/Kafka style diagram.. Speech: Nam: "I think we should move notifications to async processing."
Panel 4: Before/after latency chart.. Speech: Kenji: "Show the latency before and after."
Panel 5: Deploy checklist.. Speech: Nam: "Let's follow through on monitoring the queue depth."
Panel 6: Hook.. Speech: Next: API Gateway at Night

ENGLISH FOCUS box must list:
- "This might be caused by..." = Có thể do...
- "I think we should..." = Tôi nghĩ chúng ta nên...
- "follow through" = theo sát đến khi hoàn thành

Highlight key phrases in BLUE BOLD inside speech bubbles.
All dialogue in ENGLISH. Vietnamese ONLY inside ENGLISH FOCUS meanings.

Footer next episode: Next: API Gateway at Night

Portrait 1024x1536, high detail, same visual style as English Vault Tokyo Debug Chronicles series bible.
NO watermark. NO real company logos.
```

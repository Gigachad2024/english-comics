# System Design Arc — Thinking Bigger — Episode 55: API Gateway at Night

> **File:** `system-design-t55-comic.md` · **Arc ID:** `system-design` · **Màu:** `#8B5CF6`
> **Output:** `images/comics/system-design/tập-55/system-design-tap55-api-gateway-at-night.png`
> **Attach:** `prompts/00-character-bible.md` + `prompts/00-layout-guide.md` + style ref image
> **Cách tạo:** Copy **PROMPT FULL PAGE** → Cursor Generate Image (hoặc ChatGPT)

**Slug gợi ý:** `api-gateway-at-night`

---

## Story beats

- **Panel 1:** Late night architecture review. Dialogue: Aoi: "Can you walk me through the API Gateway setup?"
- **Panel 2:** Gateway routes diagram. Dialogue: Nam: "It acts as a single entry point for all clients."
- **Panel 3:** Auth + rate limit boxes. Dialogue: Nam: "We need to make sure rate limiting is per API key."
- **Panel 4:** Kenji asks about failure. Dialogue: Kenji: "What happens if the gateway goes down?"
- **Panel 5:** Health check monitor. Dialogue: Nam: "Let me make sure I got this right — gateway → services → cache → DB."
- **Panel 6:** Hook. Dialogue: Next: Scale Under Pressure

---

## ENGLISH FOCUS (phải có trong ảnh)

```
ENGLISH FOCUS
  1. "walk me through" = giải thích từng bước cho tôi
  2. "act as" = đóng vai trò / hoạt động như
  3. "make sure" = đảm bảo / chắc chắn rằng
Tip: Use these patterns for system design communication.
```

**Next hook:** Next: Scale Under Pressure

---

## PROMPT FULL PAGE (copy-paste)

```
Draw ONE complete educational manga comic page — English Vault: Tokyo Debug Chronicles.

ARC: System Design Arc — Thinking Bigger
EPISODE 55: API Gateway at Night
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
Panel 1: Late night architecture review.. Speech: Aoi: "Can you walk me through the API Gateway setup?"
Panel 2: Gateway routes diagram.. Speech: Nam: "It acts as a single entry point for all clients."
Panel 3: Auth + rate limit boxes.. Speech: Nam: "We need to make sure rate limiting is per API key."
Panel 4: Kenji asks about failure.. Speech: Kenji: "What happens if the gateway goes down?"
Panel 5: Health check monitor.. Speech: Nam: "Let me make sure I got this right — gateway → services → cache → DB."
Panel 6: Hook.. Speech: Next: Scale Under Pressure

ENGLISH FOCUS box must list:
- "walk me through" = giải thích từng bước cho tôi
- "act as" = đóng vai trò / hoạt động như
- "make sure" = đảm bảo / chắc chắn rằng

Highlight key phrases in BLUE BOLD inside speech bubbles.
All dialogue in ENGLISH. Vietnamese ONLY inside ENGLISH FOCUS meanings.

Footer next episode: Next: Scale Under Pressure

Portrait 1024x1536, high detail, same visual style as English Vault Tokyo Debug Chronicles series bible.
NO watermark. NO real company logos.
```

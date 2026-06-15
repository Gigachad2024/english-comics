# Investor Demo Arc — Final Boss — Episode 3: Walk Me Through the Payment Flow

> **File:** `prompts/bug-arc-3-t03-comic.md` · **Arc ID:** `bug-arc-3` · **Màu:** `#A855F7`
> **Output:** `images/comics/bug-arc-3/tập-03/bug-arc-3-tap03-walk-me-through-the-payment-flow.png`
> **Attach:** `prompts/00-character-bible.md` + `prompts/00-layout-guide.md` + `bug-arc-3-tap02-quick-patch-or-rollback.png`

**Slug:** `walk-me-through-the-payment-flow`

---

## Story beats

- **Panel 1:** Team regroups after rollback debate. Dialogue: Kenji: "Can you walk me through the payment flow?"
- **Panel 2:** Aoi draws architecture on whiteboard: Client → API Gateway → Payment Service → DB. Dialogue: Aoi: "Let me walk you through it step by step."
- **Panel 3:** Flow diagram: checkout → confirm → charge → receipt. Dialogue: Nam: "The bug affects the payment flow at the confirm step."
- **Panel 4:** API endpoint `/api/payments/confirm` highlighted red. Dialogue: Linh: "That's where the 500 errors are coming from."
- **Panel 5:** Sequence diagram on monitor. Dialogue: Nam: "It seems like the confirm call fails after the cache update."
- **Panel 6:** Team aligned. Dialogue: Kenji: "Good. Now let's find the root cause." Hook: Next: Cache Suspect

---

## ENGLISH FOCUS (phải có trong ảnh)

```
ENGLISH FOCUS
  1. "Can you walk me through the payment flow?" = Bạn giải thích flow thanh toán cho tôi được không?
  2. "The bug affects the payment flow." = Lỗi ảnh hưởng đến luồng thanh toán.
  3. "Walk me through..." = Giải thích từng bước cho tôi...
Tip: Use "walk me through" when you need a step-by-step explanation.
```

**Next hook:** Next: Cache Suspect

---

## PROMPT FULL PAGE (copy-paste)

```
Draw ONE complete educational manga comic page — English Vault: Tokyo Debug Chronicles.

ARC: Final Boss Arc — Investor Demo Nightmare
EPISODE 3: Walk Me Through the Payment Flow
Accent color: #A855F7

STYLE: Modern anime manga educational webcomic, clean cel-shading, Tokyo office at night,
Tokyo Tower through window, cinematic blue-purple lighting, professional software team,
detailed UI monitors and architecture diagrams, high quality illustration, portrait comic page 1024x1536,
thin white panel borders, educational infographic style

CHARACTERS (consistent):
- Nam: young Vietnamese man, blue hoodie #2563EB, Junior Engineer badge
- Kenji: Tech Lead, dark shirt/suit, glasses
- Aoi: Senior Engineer, navy blazer, long black hair
- Linh: QA Engineer, gray hoodie
Setting: Modern Tokyo office at night, Tokyo Tower visible through window

LAYOUT: Header once at top → 6 numbered panels (2x3 grid) → ENGLISH FOCUS box (beige, full width) → NEXT hook box bottom-right

PANEL STORY:
Panel 1: Team regroups after rollback debate.. Speech: Kenji: "Can you walk me through the payment flow?"
Panel 2: Aoi draws architecture on whiteboard: Client → API Gateway → Payment Service → DB.. Speech: Aoi: "Let me walk you through it step by step."
Panel 3: Flow diagram: checkout → confirm → charge → receipt.. Speech: Nam: "The bug affects the payment flow at the confirm step."
Panel 4: API endpoint /api/payments/confirm highlighted red.. Speech: Linh: "That's where the 500 errors are coming from."
Panel 5: Sequence diagram on monitor.. Speech: Nam: "It seems like the confirm call fails after the cache update."
Panel 6: Team aligned.. Speech: Kenji: "Good. Now let's find the root cause."

ENGLISH FOCUS box must list:
- "Can you walk me through the payment flow?" = Bạn giải thích flow thanh toán cho tôi được không?
- "The bug affects the payment flow." = Lỗi ảnh hưởng đến luồng thanh toán.
- "Walk me through..." = Giải thích từng bước cho tôi...

Highlight key phrases in BLUE BOLD inside speech bubbles.
All dialogue in ENGLISH. Vietnamese ONLY inside ENGLISH FOCUS meanings.

Footer next episode: Next: Cache Suspect

Portrait 1024x1536, high detail, same visual style as English Vault Tokyo Debug Chronicles series bible.
NO watermark. NO real company logos.
```

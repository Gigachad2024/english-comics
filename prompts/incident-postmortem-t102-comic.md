# Incident & Postmortem Arc — Blameless Communication — Episode 102: Root Cause Analysis

> **File:** `incident-postmortem-t102-comic.md` · **Arc ID:** `incident-postmortem` · **Màu:** `#DC2626`
> **Output:** `images/comics/incident-postmortem/tập-102/incident-postmortem-tap102-root-cause-analysis.png`
> **Attach:** `prompts/00-character-bible.md` + `prompts/00-layout-guide.md` + style ref image
> **Cách tạo:** Copy **PROMPT FULL PAGE** → Cursor Generate Image (hoặc ChatGPT)

**Slug gợi ý:** `root-cause-analysis`

---

## Story beats

- **Panel 1:** Post-rollback analysis. Dialogue: Aoi: "Logs show cache invalidation errors."
- **Panel 2:** Nam hypothesis. Dialogue: Nam: "Root cause appears to be stale cache keys after deploy."
- **Panel 3:** Supporting evidence. Dialogue: Nam: "It seems like the new TTL config wasn't applied."
- **Panel 4:** Linh adds. Dialogue: Linh: "This might be caused by a missing env variable in staging."
- **Panel 5:** Kenji confirms. Dialogue: Kenji: "Let's verify before we finalize the postmortem."
- **Panel 6:** No blame. Dialogue: Kenji: "Process gap, not person fault."
- **Panel 7:** Hook. Dialogue: Next: Action Items Going Forward

---

## ENGLISH FOCUS (phải có trong ảnh)

```
ENGLISH FOCUS
  1. "Root cause appears to be..." = Nguyên nhân gốc có vẻ là...
  2. "It seems like..." = Có vẻ như...
  3. "This might be caused by..." = Có thể do...
Tip: Use these patterns for incident postmortem communication.
```

**Next hook:** Next: Action Items Going Forward

---

## PROMPT FULL PAGE (copy-paste)

```
Draw ONE complete educational manga comic page — English Vault: Tokyo Debug Chronicles.

ARC: Incident & Postmortem Arc — Blameless Communication
EPISODE 102: Root Cause Analysis
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
Panel 1: Post-rollback analysis.. Speech: Aoi: "Logs show cache invalidation errors."
Panel 2: Nam hypothesis.. Speech: Nam: "Root cause appears to be stale cache keys after deploy."
Panel 3: Supporting evidence.. Speech: Nam: "It seems like the new TTL config wasn't applied."
Panel 4: Linh adds.. Speech: Linh: "This might be caused by a missing env variable in staging."
Panel 5: Kenji confirms.. Speech: Kenji: "Let's verify before we finalize the postmortem."
Panel 6: No blame.. Speech: Kenji: "Process gap, not person fault."
Panel 7: Hook.. Speech: Next: Action Items Going Forward

ENGLISH FOCUS box must list:
- "Root cause appears to be..." = Nguyên nhân gốc có vẻ là...
- "It seems like..." = Có vẻ như...
- "This might be caused by..." = Có thể do...

Highlight key phrases in BLUE BOLD inside speech bubbles.
All dialogue in ENGLISH. Vietnamese ONLY inside ENGLISH FOCUS meanings.

Footer next episode: Next: Action Items Going Forward

Portrait 1024x1536, high detail, same visual style as English Vault Tokyo Debug Chronicles series bible.
NO watermark. NO real company logos.
```

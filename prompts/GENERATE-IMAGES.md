# Tạo ảnh comic bằng Cursor — English Vault

Hướng dẫn tạo comic theo đúng style Tokyo Debug Chronicles.

**Kịch bản arc chi tiết:** `prompts/arcs/00-career-advanced-overview.md` (+ 01–05 arc scripts)

---

## Career Advanced — 26 tập mới (79–104) ⭐ Ưu tiên

| Arc | Tập | File kịch bản | Prompt files |
|-----|-----|---------------|--------------|
| Interview & Career | 79–84 | `arcs/01-interview-career-arc-script.md` | `interview-career-t79-comic.md` … `t84` |
| Negotiation | 85–89 | `arcs/02-negotiation-boundaries-arc-script.md` | `negotiation-boundaries-t85-comic.md` … |
| Feedback | 90–94 | `arcs/03-giving-feedback-arc-script.md` | `giving-feedback-t90-comic.md` … |
| Presentation | 95–99 | `arcs/04-presentation-pitch-arc-script.md` | `presentation-pitch-t95-comic.md` … |
| Postmortem | 100–104 | `arcs/05-incident-postmortem-arc-script.md` | `incident-postmortem-t100-comic.md` … |

**Style ref gợi ý:**
- Tập 79–84: `career-growth/tập-50/nam-becomes-the-bridge.png`
- Tập 85+: tập finale arc trước hoặc `system-design/tập-58`

**Thứ tự vẽ:** 79 → 84 → 85 → … → 104 (tập trước = ref tập sau)

**Sau khi có ảnh** — xem template trong `scripts/ingest-new-images.py` (Career Advanced 79–104).

```bash
python3 scripts/setup-career-advanced-dirs.py   # tạo thư mục trống
python3 scripts/ingest-new-images.py            # sau khi thả ảnh vào untitled folder/
python3 scripts/build-comics-data.py
```

---

## Arc cũ — System Design + Email (51–65)

## Chuẩn bị (1 lần)

1. Mở thư mục `prompts/`
2. Đọc:
   - `00-character-bible.md` — nhân vật, màu, setting
   - `00-layout-guide.md` — bố cục 6 panel + ENGLISH FOCUS
3. Chuẩn bị **ảnh tham chiếu** (attach khi generate):
   - `images/comics/series-bible/tokyo-debug-series-bible-master-style.png`
   - Tập gần nhất cùng tone: `images/comics/career-growth/tập-45/career-growth-tap45-quick-patch-or-full-refactor.png`

## Cách tạo từng tập trong Cursor

### Bước 1 — Mở file prompt

Ví dụ tập 51:

```
prompts/system-design-t51-comic.md
```

Danh sách đầy đủ trong `prompts/episode-queue.json`.

### Bước 2 — Generate Image

1. Trong Cursor Chat, gõ **Generate Image** (hoặc dùng công cụ tạo ảnh)
2. **Attach** 2 file bible + 1 ảnh ref career-growth tap45
3. Copy toàn bộ khối **PROMPT FULL PAGE** (giữa ``` … ```) từ file `.md`
4. Generate portrait **1024×1536**
5. Kiểm tra:
   - 6 panel có số thứ tự
   - Hội thoại **tiếng Anh**
   - Box **ENGLISH FOCUS** có nghĩa **tiếng Việt**
   - Footer **NEXT:** hook tập sau
   - Không watermark, không logo công ty thật

### Bước 3 — Lưu file đúng tên

Lưu PNG vào đúng path ghi ở đầu mỗi file prompt, ví dụ:

```
images/comics/system-design/tập-51/system-design-tap51-the-system-design-question.png
```

Quy tắc: `images/comics/{arc}/tập-{NN}/{arc}-tap{NN}-{slug}.png`

## Thứ tự đề xuất

| # | File prompt | Tập |
|---|-------------|-----|
| 1 | `system-design-t51-comic.md` | 51 |
| 2 | `system-design-t52-comic.md` | 52 |
| … | … | … |
| 10 | `system-design-t60-comic.md` | 60 |
| 11 | `email-async-t61-comic.md` | 61 |
| … | … | … |
| 15 | `email-async-t65-comic.md` | 65 |

Generate **theo thứ tự** để giữ style nhất quán — tập trước làm ref cho tập sau.

## Sau khi có ảnh — đưa lên website

1. Sửa `scripts/ingest-new-images.py`:
   - `ARC = "system-design"` (hoặc `"email-async"`)
   - `NEW_EPISODES = [("tên-file-gốc.png", 51, "the-system-design-question"), ...]`
   - Đặt file PNG gốc vào `untitled folder/` (hoặc sửa `SRC`)

2. Chạy pipeline:

```bash
python3 scripts/ingest-new-images.py
python3 scripts/build-comics-data.py
```

3. Refresh site: `python3 -m http.server 8080` → `http://localhost:8080`

## Tạo lại prompt (nếu sửa story)

```bash
python3 scripts/generate-comic-prompts.py
```

Script đọc nghĩa tiếng Việt từ `FOCUS` trong `build-comics-data.py`.

## Pack 5 — Email & Async English

Đã thêm vào `english_vault_website_core.json` / `data/core.json`:

- **ID:** `email_async`
- **Patterns:** Just following up on…, loop me in, get back to you by…, async standup
- **Arc:** Email & Async 61–65

Sau khi build, Pattern Library (`#/patterns`) sẽ hiện pack thứ 5.

## Mẹo khi ảnh không đúng style

- Nhắc lại: *"Same style as attached English Vault series bible reference"*
- Nhắc: *"ONE episode only, 6 panels, no collage"*
- Nếu thiếu ENGLISH FOCUS box → regenerate chỉ panel footer + focus box
- Nếu nhân vật sai màu → paste lại mô tả Nam/Kenji/Aoi/Linh từ `00-character-bible.md`

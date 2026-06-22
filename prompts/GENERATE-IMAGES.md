# Tạo ảnh comic bằng Cursor — English Vault

Hướng dẫn tạo comic theo đúng style Tokyo Debug Chronicles.

**136 tập · 18 series** · Kịch bản arc: `prompts/arcs/00-career-advanced-overview.md` (+ 01–05) · **Get phrasal verbs:** [`prompts/arcs/06-get-phrasal-overview.md`](prompts/arcs/06-get-phrasal-overview.md) (+ 07–09 arc scripts)

---

## Phrasal Verbs Expansion — 92 tập mới (119–210) ⭐ Mới

| Phase | Tập | Arc script | Prompt files | View |
|-------|-----|------------|--------------|------|
| LOOK — Big Tech | 119–124 | `arcs/11-look-bigtech-script.md` | `silicon-valley-look-t119-comic.md` … `t124` | [localhost:8080#/read/silicon-valley-look/119](http://localhost:8080#/read/silicon-valley-look/119) |
| LOOK — Wall Street | 125–129 | `arcs/12-look-wallstreet-script.md` | `wall-street-look-t125-comic.md` … `t129` | [localhost:8080#/read/wall-street-look/125](http://localhost:8080#/read/wall-street-look/125) |
| LOOK — Everyday | 130–132 | `arcs/13-look-everyday-script.md` | `english-everyday-look-t130-comic.md` … `t132` | [localhost:8080#/read/english-everyday-look/130](http://localhost:8080#/read/english-everyday-look/130) |
| TAKE/PUT/COME/GO | 133–188 | `arcs/14-take-phrasal-overview.md`, `15-put-come-go-overview.md` | `*-take/put/come/go-t*.md` | see README roadmap |
| Topic arcs | 189–210 | `arcs/16-topic-arcs-overview.md` | `customer-support-t189-comic.md` … `phrasal-review-t210` | [localhost:8080#/read/customer-support/189](http://localhost:8080#/read/customer-support/189) |

**Packs:** `look_phrasal_*` · `take_phrasal_*` · `put_phrasal_*` · `come_phrasal_*` · `go_phrasal_*` · `customer_support` · `health_clinic` · `side_project` · `remote_async` · `phrasal_review`

**Setup:** `python3 scripts/setup-phrasal-arcs-dirs.py` · **Sync:** `python3 scripts/sync-phrasal-expansion.py`

---

## Get Phrasal Verbs — 14 tập mới (105–118) ⭐ Mới

**Grammar (5 pattern types):** xem [`prompts/arcs/06-get-phrasal-overview.md`](prompts/arcs/06-get-phrasal-overview.md) — get + V3 · get + adj · get + prep + noun · get + noun · get + through/up to/used to/by/it

| Arc | Tập | File kịch bản | Prompt files | Xem trên local |
|-----|-----|---------------|--------------|----------------|
| Silicon Valley Get | 105–110 | `arcs/07-silicon-valley-get-arc-script.md` | `silicon-valley-get-t105-comic.md` … `t110` | [localhost:8080#/read/silicon-valley-get/105](http://localhost:8080#/read/silicon-valley-get/105) |
| Switzerland Travel | 111–115 | `arcs/08-switzerland-travel-arc-script.md` | `switzerland-travel-t111-comic.md` … `t115` | [localhost:8080#/read/switzerland-travel/111](http://localhost:8080#/read/switzerland-travel/111) |
| Everyday Get | 116–118 | `arcs/09-everyday-get-arc-script.md` | `english-everyday-get-t116-comic.md` … `t118` | [localhost:8080#/read/english-everyday-get/116](http://localhost:8080#/read/english-everyday-get/116) |

**Packs:** `get_phrasal_startup` · `get_phrasal_travel` · `get_phrasal_everyday`

**Style ref gợi ý:**
- Silicon Valley: `career-growth/tập-50/` + SF open office
- Switzerland: `traveling/tập-16/` + alpine scenery
- Everyday: warm meetup / cafe study session

```bash
python3 scripts/setup-get-arcs-dirs.py
python3 scripts/generate-comic-prompts.py
python3 scripts/build-comics-data.py
```

---

## Career Advanced — 26 tập (79–104)

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

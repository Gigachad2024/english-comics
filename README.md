# English Vault: Tokyo Debug Chronicles

Hướng dẫn A→Z — từ chạy website, thêm truyện, mở rộng pattern/phrasal verbs, đến cách học hiệu quả.

---

## Mục lục

1. [Dự án này là gì?](#1-dự-án-này-là-gì)
2. [Cấu trúc thư mục](#2-cấu-trúc-thư-mục)
3. [Chạy website lần đầu](#3-chạy-website-lần-đầu)
4. [Cách học trên website](#4-cách-học-trên-website)
5. [Quy ước đặt tên ảnh](#5-quy-ước-đặt-tên-ảnh)
6. [Thêm ảnh / tập truyện mới](#6-thêm-ảnh--tập-truyện-mới)
7. [Thêm arc (bộ truyện) mới](#7-thêm-arc-bộ-truyện-mới)
8. [Thêm pattern & phrasal verbs](#8-thêm-pattern--phrasal-verbs)
9. [Các file dữ liệu quan trọng](#9-các-file-dữ-liệu-quan-trọng)
10. [Scripts & lệnh build](#10-scripts--lệnh-build)
11. [Deploy lên internet](#11-deploy-lên-internet)
12. [Checklist nhanh](#12-checklist-nhanh)
13. [Xử lý lỗi thường gặp](#13-xử-lý-lỗi-thường-gặp)
14. [Arc tiếp theo gợi ý](#14-arc-tiếp-theo-gợi-ý)

---

## 1. Dự án này là gì?

**English Vault** là website học tiếng Anh qua truyện tranh (manga/webcomic), tập trung vào **pattern** — cụm câu dùng được trong đời thật:

- Công việc dev (debug, deploy, code review…)
- Du lịch Nhật
- Sống ở Tokyo
- Career growth (mentor, speaking up…)

### Triết lý học (Core Loop)

```text
Speak → Fix → Reuse → Review
```

### Luồng trên website

```text
Comic episode → English Focus → Pattern card → Practice prompt → Review Mode
```

### Tài liệu gốc (nên đọc)

| File | Mục đích |
|------|----------|
| `English_Vault_Website_Core.md` | Giải thích packs, patterns, UX, review mode |
| `english_vault_website_core.json` | Bản JSON của core — **sửa file này rồi sync sang `data/`** |
| `data/core.json` | Bản website đang dùng (copy từ file trên) |

---

## 2. Cấu trúc thư mục

```text
English-Comics/
├── README.md                          ← File này
├── English_Vault_Website_Core.md        ← Triết lý & pack patterns
├── english_vault_website_core.json    ← Core JSON (nguồn chỉnh sửa)
├── index.html                         ← Trang web chính
├── css/style.css                      ← Giao diện
├── js/
│   ├── app.js                         ← App: đọc truyện, lộ trình, tìm kiếm
│   └── learn.js                       ← Pattern Library & Review Mode
├── data/
│   ├── core.json                      ← Packs, patterns, review template
│   ├── comics.json                    ← Metadata 67 tập (auto-generated)
│   ├── roadmap.json                   ← Lộ trình học
│   ├── image-manifest.json            ← Map ảnh cũ → tên mới
│   └── new-images-manifest.json       ← Ảnh mới ingest gần nhất
├── images/comics/                     ← Ảnh đã đặt tên chuẩn (website dùng)
│   ├── bug-arc-1/tập-01/...
│   ├── traveling/tập-11/...
│   ├── living/tập-26/...
│   ├── career-growth/tập-41/...
│   └── series-bible/...
├── scripts/
│   ├── build-comics-data.py           ← Tạo comics.json + roadmap.json
│   ├── enrich-comics-from-core.py     ← Gắn packs, practice prompts
│   ├── ingest-new-images.py           ← Copy ảnh mới vào images/comics/
│   └── reorganize-images.py           ← Script đổi tên ảnh ban đầu (1 lần)
├── Bug/, Traveling/, Living/           ← Ảnh gốc ChatGPT (backup, có thể xóa)
└── untitled folder/                   ← Thả ảnh mới vào đây trước khi ingest
```

### Hiện có bao nhiêu nội dung?

| Arc | ID | Tập | Số episode |
|-----|-----|-----|------------|
| Debug & Release | `bug-arc-1` | 1–10 | 10 |
| Payment & Demo | `bug-arc-2` | 1–10 | 10 |
| Investor Demo | `bug-arc-3` | 1–9 | 9 (thiếu Ep 3) |
| English on the Road | `traveling` | 11–25 | 15 |
| English for Real Life | `living` | 26–40 | 13 (thiếu Ep 32) |
| Career Growth | `career-growth` | 41–50 | 10 |
| **Tổng** | | | **67 tập** |

---

## 3. Chạy website lần đầu

### Yêu cầu

- macOS / Linux / Windows
- Python 3 (đã có sẵn trên Mac)
- Trình duyệt (Chrome, Safari, Firefox…)

### Bước 1 — Mở terminal

```bash
cd ~/Documents/English-Comics
```

### Bước 2 — Chạy server local

```bash
python3 -m http.server 8080
```

Nếu port 8080 bận, dùng port khác:

```bash
python3 -m http.server 9000
```

### Bước 3 — Mở trình duyệt

```text
http://localhost:8080
```

> **Quan trọng:** Không mở trực tiếp file `index.html` bằng double-click. Website cần server để load file JSON.

### Bước 4 — Dừng server

Trong terminal: `Ctrl + C`

---

## 4. Cách học trên website

### Trang & chức năng

| Trang | URL | Dùng để |
|-------|-----|---------|
| Trang chủ | `#/` | Xem tất cả arc, filter theo tag |
| Lộ trình | `#/roadmap` | Học theo thứ tự Work → Travel → Life → Growth |
| Patterns | `#/patterns` | Xem 4 knowledge packs, master combo |
| Đọc truyện | `#/read/{arc-id}/{số-tập}` | Vd: `#/read/career-growth/45` |
| Đã lưu | `#/bookmarks` | Tập bookmark + lịch sử đọc |

### Phím tắt khi đọc truyện

| Phím | Chức năng |
|------|-----------|
| `←` `→` | Tập trước / sau |
| `Z` | Phóng to ảnh |
| `F` | Toàn màn hình |
| `S` | Chia sẻ link |
| `/` | Tìm kiếm |
| `?` | Xem phím tắt |
| `Esc` | Đóng / về danh sách |

### Quy trình học 1 tập (khuyến nghị)

1. **Đọc truyện** — chú ý hội thoại trong ảnh
2. **English Focus** — panel dưới ảnh (cụm từ + nghĩa tiếng Việt)
3. **Pattern packs** — bấm link pack để xem thêm câu mẫu
4. **Try it yourself** — viết 2–3 câu tiếng Anh theo prompt
5. **Review Mode** — copy prompt → dán vào ChatGPT/Claude → luyện nói
6. **Tập tiếp theo** — nút "Tiếp" hoặc lộ trình

### Review Mode (luyện với AI)

1. Trong trang đọc truyện → bấm **"Luyện với Review Mode"**
2. Hoặc vào **Patterns** → **Mở Review Mode**
3. Bấm **Copy prompt**
4. Dán vào ChatGPT / Claude / Cursor
5. AI hỏi tình huống tiếng Việt → bạn trả lời tiếng Anh → AI sửa ngay

---

## 5. Quy ước đặt tên ảnh

### Nguyên tắc (bắt buộc)

```text
1 ảnh = 1 tập = 1 tiêu đề
Không dùng collage nhiều tập trên 1 ảnh (trừ poster/banner)
```

### Cấu trúc thư mục

```text
images/comics/{arc-id}/tập-{num}/{arc-id}-tap{num}-{slug}.png
```

### Ví dụ

```text
images/comics/career-growth/tập-45/career-growth-tap45-quick-patch-or-full-refactor.png
images/comics/traveling/tập-16/traveling-tap16-what-should-i-order.png
```

### Quy tắc `slug`

- Chữ thường, nối bằng dấu `-`
- Lấy từ tiêu đề tiếng Anh trên ảnh
- Vd: `"Quick Patch or Full Refactor?"` → `quick-patch-or-full-refactor`

### Số tập (`num`)

| Arc | Cách đánh số |
|-----|--------------|
| `bug-arc-1`, `bug-arc-2`, `bug-arc-3` | 1, 2, 3… (reset mỗi arc) |
| `traveling`, `living`, `career-growth` | Số global: 11–25, 26–40, 41–50… |

---

## 6. Thêm ảnh / tập truyện mới

### Tình huống A — Thêm vài tập vào arc có sẵn

#### Bước 1: Tạo ảnh comic

Dùng ChatGPT / tool AI, đảm bảo mỗi ảnh có:
- Số tập (Episode XX)
- Tiêu đề tiếng Anh
- Khung **ENGLISH FOCUS** ở cuối ảnh

#### Bước 2: Thả ảnh vào folder

```text
untitled folder/
  ChatGPT Image ....png
  ChatGPT Image ....png
```

#### Bước 3: Mở ảnh, ghi lại metadata

Với mỗi ảnh, note:

| Trường | Ví dụ |
|--------|-------|
| Số tập | `51` |
| Tiêu đề | `The System Design Question` |
| Slug | `the-system-design-question` |
| Arc ID | `system-design` |
| English Focus | `I'm weighing up A and B.` = `Tôi đang cân nhắc…` |

#### Bước 4: Sửa `scripts/ingest-new-images.py`

Thêm dòng vào mảng `NEW_EPISODES`:

```python
NEW_EPISODES = [
    ("ChatGPT Image Jun 14, 2026, 10_00_00 PM.png", 51, "the-system-design-question"),
    # ...
]
ARC = "system-design"   # hoặc arc hiện có
```

#### Bước 5: Sửa `scripts/build-comics-data.py`

**a) Thêm tập vào `SERIES[].episodes`:**

```python
(51, "the-system-design-question", "The System Design Question"),
```

**b) Thêm English Focus vào dict `FOCUS` (tuỳ chọn nhưng nên có):**

```python
"the-system-design-question": [
    {"phrase": "I'm weighing up A and B.", "meaning": "Tôi đang cân nhắc A và B."},
    {"phrase": "trade-off", "meaning": "sự đánh đổi"},
],
```

#### Bước 6: Chạy build

```bash
cd ~/Documents/English-Comics
python3 scripts/ingest-new-images.py
python3 scripts/build-comics-data.py
```

#### Bước 7: Kiểm tra

1. Refresh browser (`Cmd+Shift+R`)
2. Vào arc → tìm tập mới
3. Mở ảnh xem load đúng không

---

### Tình huống B — Chỉ cập nhật English Focus (không thêm ảnh)

Sửa dict `FOCUS` trong `scripts/build-comics-data.py`, rồi:

```bash
python3 scripts/build-comics-data.py
```

---

## 7. Thêm arc (bộ truyện) mới

Ví dụ: **System Design Arc** (Ep 51–60)

### Bước 1: Thêm block series trong `build-comics-data.py`

```python
{
    "id": "system-design",
    "title": "System Design Arc",
    "desc": "Architecture, scalability, trade-offs — tiếng Anh khi thiết kế hệ thống",
    "color": "#8B5CF6",
    "icon": "🏗️",
    "tag": "Công việc",
    "arc": "system-design",
    "global_num": True,
    "episodes": [
        (51, "the-system-design-question", "The System Design Question"),
        (52, "monolith-or-microservices", "Monolith or Microservices?"),
        # ... thêm đến 60
    ],
},
```

### Bước 2: Thêm vào roadmap (`build-comics-data.py` → `build_roadmap()`)

Trong path `full-journey`, thêm phase:

```python
{
    "title": "Giai đoạn 5 — System Design",
    "desc": "Thinking bigger — architecture & trade-offs",
    "steps": [
        {"seriesId": "system-design", "tip": "Scale, cache, microservices…"}
    ],
},
```

### Bước 3: Gắn pack mặc định trong `enrich-comics-from-core.py`

```python
ARC_PACKS = {
    # ...
    "system-design": ["bug_report_agreement_through", "preference_opinion", "decision_hesitation"],
}
```

### Bước 4: Ingest ảnh + build (như mục 6)

### Bước 5: Cập nhật `index.html` (tuỳ chọn)

Số thống kê hero tự tính từ JSON — không cần sửa nếu dùng `app.js` dynamic.

Bump version cache nếu ảnh không đổi mà JS/CSS đổi:

Trong `js/app.js`:

```javascript
const ASSET_VERSION = "20250615-english-vault-v4";
```

Trong `index.html`:

```html
<link rel="stylesheet" href="css/style.css?v=20250615-v4">
<script src="js/learn.js?v=20250615-v4"></script>
<script src="js/app.js?v=20250615-v4"></script>
```

---

## 8. Thêm pattern & phrasal verbs

Đây là cách mở rộng **sau khi học xong** nội dung hiện tại.

### File cần sửa

```text
english_vault_website_core.json   ← Sửa ở đây (bản master)
         ↓ copy
data/core.json                    ← Website đọc file này
         ↓
scripts/enrich-comics-from-core.py  ← Auto-gắn pack vào tập
         ↓
python3 scripts/build-comics-data.py
```

### Cách 1 — Thêm pattern vào pack có sẵn

Mở `english_vault_website_core.json`, tìm pack (vd. `preference_opinion`):

```json
"phrasalVerbs": [
  "go with",
  "rule out",
  "back out of",
  "talk over"
]
```

Sync & build:

```bash
cp english_vault_website_core.json data/core.json
python3 scripts/build-comics-data.py
```

→ Vào `#/patterns` xem pack đã cập nhật.

### Cách 2 — Tạo pack mới hoàn toàn

Thêm object vào mảng `"packs"`:

```json
{
  "id": "email_async",
  "title": "Email & Async Communication",
  "purpose": "Dùng khi viết email, Slack, follow-up công việc.",
  "contexts": ["work", "software-engineering"],
  "patterns": [
    "Just following up on...",
    "Could you loop me in on...?",
    "I'll get back to you by + time."
  ],
  "phrasalVerbs": [
    "follow up on",
    "loop in",
    "get back to",
    "reach out to"
  ],
  "masterCombo": "Hi Kenji, just following up on the deployment timeline. Could you loop me in on the QA results? I'll get back to you by EOD."
}
```

Thêm rule auto-match trong `enrich-comics-from-core.py`:

```python
("email_async", ["following up", "loop me in", "get back to you"]),
```

### Cách 3 — Thêm common mistakes

Sửa mảng `COMMON_MISTAKES` trong `enrich-comics-from-core.py`:

```python
{
    "wrong": "I'll follow up you tomorrow.",
    "correct": "I'll follow up with you tomorrow.",
    "why": "follow up with + person",
    "patterns": ["follow up"],
},
```

### Cách 4 — Học pattern mới qua truyện (khuyến nghị)

Pattern trong `core.json` **+** comic mới **+** English Focus trên ảnh = học sâu nhất.

Thứ tự làm:

1. Viết pattern vào `core.json`
2. Tạo ảnh comic có ENGLISH FOCUS
3. Ingest ảnh + thêm tập (mục 6)
4. Build

---

## 9. Các file dữ liệu quan trọng

### `data/comics.json`

Metadata toàn bộ truyện. **Auto-generated** — không sửa tay trừ khi biết rõ cấu trúc.

Mỗi tập có:

```json
{
  "num": 45,
  "title": "Quick Patch or Full Refactor?",
  "slug": "quick-patch-or-full-refactor",
  "image": "images/comics/career-growth/tập-45/...",
  "englishFocus": [
    {"phrase": "I'm torn between A and B.", "meaning": "Tôi phân vân giữa A và B."}
  ],
  "packs": ["decision_hesitation", "preference_opinion"],
  "practicePrompts": ["Dùng câu ..."],
  "commonMistakes": [],
  "hook": "Next: Demo Day Pressure"
}
```

### `data/core.json`

4 knowledge packs + review mode template. **Nguồn sự thật** cho Pattern Library.

### `data/roadmap.json`

Lộ trình học — auto-generated từ `build-comics-data.py`.

### `English_Vault_Website_Core.md`

Tài liệu triết lý, tag system, episode schema, arc roadmap gốc.

---

## 10. Scripts & lệnh build

| Script | Khi nào chạy |
|--------|--------------|
| `ingest-new-images.py` | Có ảnh mới trong `untitled folder/` |
| `build-comics-data.py` | Sau khi sửa episodes, FOCUS, roadmap, hoặc core |
| `enrich-comics-from-core.py` | Tự chạy cuối `build-comics-data.py` |
| `reorganize-images.py` | Chỉ dùng 1 lần đầu (đổi tên ảnh ChatGPT cũ) |

### Lệnh build đầy đủ (dùng thường xuyên)

```bash
cd ~/Documents/English-Comics

# Nếu sửa core patterns
cp english_vault_website_core.json data/core.json

# Nếu có ảnh mới
python3 scripts/ingest-new-images.py

# Luôn chạy sau mọi thay đổi metadata
python3 scripts/build-comics-data.py
```

### Thứ tự pipeline

```text
Ảnh mới → ingest-new-images.py
                ↓
Sửa build-comics-data.py (episodes, FOCUS, series, roadmap)
                ↓
        build-comics-data.py
                ↓
        enrich-comics-from-core.py (tự động)
                ↓
        data/comics.json + data/roadmap.json
                ↓
        Refresh browser
```

---

## 11. Deploy lên internet

Website này là **static site** (HTML + JSON + ảnh) — deploy miễn phí được.

### GitHub Pages

```bash
cd ~/Documents/English-Comics
git init
git add .
git commit -m "English Vault website"
# Push lên GitHub repo
# Settings → Pages → Source: main branch
```

### Netlify / Vercel

Kéo thả folder `English-Comics` lên [netlify.com](https://netlify.com) hoặc [vercel.com](https://vercel.com).

> **Lưu ý:** Repo có thể nặng vì nhiều ảnh PNG (~2MB/ảnh). Cân nhắc Git LFS hoặc nén WebP sau.

---

## 12. Checklist nhanh

### Thêm 1 tập truyện mới

- [ ] Tạo ảnh (1 tập = 1 ảnh, có ENGLISH FOCUS)
- [ ] Thả vào `untitled folder/`
- [ ] Ghi: số tập, title, slug, arc id
- [ ] Sửa `ingest-new-images.py` → `NEW_EPISODES`
- [ ] Sửa `build-comics-data.py` → `SERIES[].episodes` + `FOCUS`
- [ ] `python3 scripts/ingest-new-images.py`
- [ ] `python3 scripts/build-comics-data.py`
- [ ] Refresh browser & test

### Thêm pattern / phrasal verb

- [ ] Sửa `english_vault_website_core.json`
- [ ] `cp english_vault_website_core.json data/core.json`
- [ ] (Tuỳ chọn) Sửa rules trong `enrich-comics-from-core.py`
- [ ] `python3 scripts/build-comics-data.py`
- [ ] Kiểm tra `#/patterns`

### Sau khi học xong toàn bộ

- [ ] Tạo pack mới trong core (email, interview, negotiation…)
- [ ] Plan arc truyện mới (System Design 51–60)
- [ ] Dùng Review Mode ôn pattern cũ
- [ ] Tạo comic mới cho pattern mới

---

## 13. Xử lý lỗi thường gặp

### Website trắng / "Không tải được dữ liệu"

**Nguyên nhân:** Mở file trực tiếp, không qua server.

**Fix:** Chạy `python3 -m http.server 8080` rồi mở `http://localhost:8080`

### Ảnh không hiện

**Nguyên nhân:** Đường dẫn sai hoặc chưa ingest.

**Fix:**
1. Kiểm tra file tồn tại trong `images/comics/...`
2. So sánh path trong `data/comics.json`
3. Hard refresh: `Cmd+Shift+R`

### Port đã bị chiếm

```bash
python3 -m http.server 9000
# hoặc
lsof -i :8080
```

### Sửa JSON xong website không đổi

1. Chạy lại `python3 scripts/build-comics-data.py`
2. Hard refresh browser
3. Bump `ASSET_VERSION` trong `js/app.js` nếu cần

### Tập mới không có English Focus

Thêm vào dict `FOCUS` trong `build-comics-data.py`, rồi build lại.

---

## 14. Arc tiếp theo gợi ý

Theo `English_Vault_Website_Core.md`, arc kế tiếp:

### System Design Arc — Ep 51–60

| Tập | Chủ đề gợi ý |
|-----|--------------|
| 51 | The System Design Question |
| 52 | Monolith or Microservices? |
| 53 | Cache or Database First? |
| 54 | Queue Saves the Day |
| 55 | API Gateway at Night |
| 56 | Scale Under Pressure |
| 57 | The Cost of Overengineering |
| 58 | Explain It to Product |
| 59 | Design Review Showdown |
| 60 | Thinking Bigger Finale |

### Pack mới có thể thêm

- **Email & Async** — follow up, loop in, get back to
- **Interview English** — tell me about a time when…
- **Negotiation** — would it be possible to…, push back
- **Customer Support** — I understand your concern…

---

## Tóm tắt 1 dòng

```text
Sửa core/patterns → sửa build-comics-data.py → ingest ảnh → build → refresh browser
```

---

*English Vault — Learn patterns through stories. Reuse them in real life.*

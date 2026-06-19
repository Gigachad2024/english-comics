# Career Advanced — Tổng quan 5 Arc (Tập 79–104)

> **Tiền đề:** Học xong 96 tập đầu (Debug → Anime). Nam đã là bridge engineer ở Tokyo.
> **Mục tiêu arc block này:** Tiếng Anh cấp senior — phỏng vấn, thương lượng, feedback, pitch, postmortem.

---

## Cung chuyện Nam (story spine)

```text
Ep 78  Nam vui với anime trip, nhưng nhận email recruiter...
  ↓
Ep 79–84  Phỏng vấn công ty mới — học STAR, salary, questions
  ↓
Ep 85–89  Ở team hiện tại: deadline gấp, scope creep — Nam push back
  ↓
Ep 90–94  Kenji giao Nam lead junior Riku — 1-on-1 & feedback
  ↓
Ep 95–99  Investor demo lần 2 — Nam trình bày, Q&A
  ↓
Ep 100–104  Production incident đêm — war room → postmortem blameless
  ↓
Finale  Nam = engineer biết nói, thương lượng, lead, và handle incident
```

---

## 5 Arc — Bảng nhanh

| # | Arc ID | Tập | Tập | Pack | Màu | Icon |
|---|--------|-----|-----|------|-----|------|
| 1 | `interview-career` | 79–84 | 6 | `interview_career` | `#F59E0B` | 💼 |
| 2 | `negotiation-boundaries` | 85–89 | 5 | `negotiation_boundaries` | `#14B8A6` | 🤝 |
| 3 | `giving-feedback` | 90–94 | 5 | `giving_feedback` | `#A855F7` | 💬 |
| 4 | `presentation-pitch` | 95–99 | 5 | `presentation_pitch` | `#F97316` | 📊 |
| 5 | `incident-postmortem` | 100–104 | 5 | `incident_postmortem` | `#DC2626` | 🚨 |

**Tổng:** 26 tập · 5 pack mới · ~4–5 tuần học

---

## Nhân vật chính theo arc

| Arc | Nam | Kenji | Aoi | Linh | Riku | Khách |
|-----|-----|-------|-----|------|------|-------|
| Interview | ứng viên | coach qua Slack | — | mock interviewer | — | Recruiter, Hiring Manager |
| Negotiation | engineer | Tech Lead | Senior | QA | — | PM (Product) |
| Feedback | mentor | manager 1-on-1 | observer | — | mentee | — |
| Presentation | presenter | supporter | co-presenter | QA check | — | PM, Investor |
| Postmortem | on-call | incident commander | metrics | QA verify | — | PM, Leadership |

---

## Quy trình sản xuất 1 tập

```text
1. Đọc kịch bản arc → prompts/arcs/0X-*.md
2. Mở prompts/{arc}-t{NN}-comic.md
3. Attach: 00-character-bible + 00-layout-guide + style ref
4. Generate portrait 1024×1536
5. Lưu: images/comics/{arc}/tập-{NN}/{arc}-tap{NN}-{slug}.png
6. Refresh website — metadata đã có sẵn trong comics.json
```

**Style ref gợi ý:**
- Arc 1: `career-growth/tập-50` (Nam confident)
- Arc 2–5: tập finale arc trước hoặc `system-design/tập-58` (explain to PM)

---

## Thứ tự vẽ đề xuất

```text
Tuần 1: Interview 79 → 84 (6 tập)
Tuần 2: Negotiation 85 → 89 + Feedback 90 → 91 (7 tập)
Tuần 3: Feedback 92 → 94 + Presentation 95 → 97 (6 tập)
Tuần 4: Presentation 98 → 99 + Postmortem 100 → 104 (7 tập)
```

---

## File kịch bản chi tiết

| File | Nội dung |
|------|----------|
| `01-interview-career-arc-script.md` | Tập 79–84 |
| `02-negotiation-boundaries-arc-script.md` | Tập 85–89 |
| `03-giving-feedback-arc-script.md` | Tập 90–94 |
| `04-presentation-pitch-arc-script.md` | Tập 95–99 |
| `05-incident-postmortem-arc-script.md` | Tập 100–104 |

Prompt ảnh: `prompts/interview-career-t79-comic.md` … `prompts/incident-postmortem-t104-comic.md`

Queue: `prompts/episode-queue.json` (filter `"num": 79` trở lên)

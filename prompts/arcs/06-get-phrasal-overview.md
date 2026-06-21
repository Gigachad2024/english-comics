# Get Phrasal Verbs — Arc Overview (Tập 105–118)

**3 arc mới** · Tách biệt khỏi danh sách get phrasal verbs trộn lẫn cũ  
**Pack mới:** `get_phrasal_startup` · `get_phrasal_travel` · `get_phrasal_everyday`

---

## Tổng quan

Nam học **get + prep/adj/V3** qua ba câu chuyện có chiều sâu cảm xúc:

| Arc | Tập | Bối cảnh | Cảm xúc chủ đạo |
|-----|-----|----------|-----------------|
| Silicon Valley Get | 105–110 | Bay Area rotation sau ship ở Tokyo | Overwhelmed → aligned → shipped → war room → bittersweet growth |
| Switzerland Travel | 111–115 | Phần thưởng du lịch Alps sau startup | Wonder → disorientation → adversity → joy in wrong turns |
| Everyday Get | 116–118 | Meetup & mentor Riku ở Tokyo | Nervous → aha moment → full circle |

---

## Ngữ pháp get — hướng dẫn chi tiết (tiếng Việt)

### 1. get + V3 (past participle) — trạng thái kết quả

Cấu trúc: **get + V3** — ai đó hoặc cái gì **đạt trạng thái mới** (thường bị động / do người khác).

| Cụm | Nghĩa | Ví dụ |
|-----|-------|-------|
| get looped in | được thêm vào luồng Slack/email | *I'll get you looped in on the launch channel.* |
| get shipped | được deploy lên production | *The feature got shipped on Friday.* |
| get promoted | được thăng chức | *You're getting promoted to senior.* |
| get acquired | (công ty) bị mua lại | *We're getting acquired by a global platform.* |
| get checked in | làm xong thủ tục nhận phòng | *I'll get you checked in.* |
| get snowed in | bị kẹt vì tuyết | *We might get snowed in tonight.* |

**Lỗi thường gặp:** *get loop in* → đúng: **get looped in** (cần -ed)

---

### 2. get + adj — trạng thái thay đổi

Cấu trúc: **get + tính từ** — chủ thể **trở nên** như vậy.

| Cụm | Nghĩa | Ví dụ |
|-----|-------|-------|
| get ready | sẵn sàng | *Let me get ready before the meetup.* |
| get stuck | bị kẹt / bí | *I'm stuck — the error only happens in prod.* |
| get lost | bị lạc | *It's easy to get lost up here.* |
| get aligned | thống nhất | *We need to get aligned on MVP scope.* |
| get unblocked | được gỡ kẹt | *You should be unblocked now.* |

---

### 3. get + prep + noun — di chuyển & quan hệ

| Cụm | Nghĩa | Ví dụ |
|-----|-------|-------|
| get to + place | đến nơi | *How do I get to the hotel?* |
| get on / get off | lên / xuống tàu xe | *We get on at platform 7.* |
| get around | đi lại quanh khu vực | *English gets you around Switzerland.* |
| get a view of | nhìn thấy cảnh | *You'll get a view of the whole Alps.* |
| get back to + person/topic | phản hồi / quay lại việc | *I'll get back to you in thirty minutes.* |
| get pulled into | bị kéo vào | *You're getting pulled into the war room.* |
| get swept up in | bị cuốn vào | *We got swept up in a village festival.* |

**Lỗi thường gặp:** *get the train* → đúng: **get on the train**

---

### 4. get + noun (không giới từ)

| Cụm | Nghĩa |
|-----|-------|
| get buy-in | được đồng thuận từ stakeholder |
| get sign-off | được phê duyệt chính thức |
| get face time | có thời gian trực tiếp với leadership |
| get a ticket / get a ride / get change | mua vé / được chở / đổi tiền lẻ |
| get altitude sickness | bị say độ cao |
| get pinged | bị tag/nhắn trên Slack |

---

### 5. get + through / up to / used to / by / it

| Cụm | Cấu trúc | Nghĩa |
|-----|----------|-------|
| get through | get + prep | vượt qua / hoàn thành (buổi học, review) |
| get up to speed | get + adv + prep | nắm bắt nhanh tình hình |
| get used to + V-ing | get + adj + to + V-ing | quen dần với |
| get by | get + adv | xoay xở được / tạm đủ dùng |
| get it | get + pronoun | hiểu rồi! (thân mật) |
| get the ball rolling | idiom | bắt đầu / khởi động |
| get your bearings | idiom | định hướng sau khi đến nơi mới |
| get held up | get + V3 | bị trì hoãn |

---

## Thứ tự vẽ / generate ảnh

```text
105 → 110 (Silicon Valley) → 111 → 115 (Switzerland) → 116 → 118 (Everyday)
```

**Style ref:**
- Silicon Valley: `career-growth/tập-50/nam-becomes-the-bridge.png` + SF office setting
- Switzerland: `traveling/tập-16/traveling-tap16-what-should-i-order.png` (travel tone)
- Everyday: `living/tập-26/` hoặc meetup warm lighting

---

## Scripts

```bash
python3 scripts/setup-get-arcs-dirs.py
python3 scripts/generate-comic-prompts.py   # nếu sửa story
# Sau khi có PNG trong images/comics/...:
python3 scripts/build-canonical-dialogues.py
python3 scripts/build-learning-data.py
python3 scripts/build-comics-data.py
```

"""Vocabulary, translations, and grammar hints for Phrasal Verb arcs (eps 119–210)."""

from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))

from phrasal_verbs_expansion import PHRASAL_DIALOGUES, PHRASAL_FOCUS  # noqa: E402


def _normalize_match(text: str) -> str:
    t = (text or "").lower().replace("\u2019", "'").replace("\u2018", "'")
    t = re.sub(r"\s+", " ", t.strip().rstrip(".!?"))
    t = re.sub(r"[^\w\s']", " ", t)
    return re.sub(r"\s+", " ", t).strip()


def _build_sentence_pairs() -> list[tuple[str, str]]:
    pairs: list[tuple[str, str]] = []
    for slug, focus_items in PHRASAL_FOCUS.items():
        for item in focus_items:
            phrase = item["phrase"]
            meaning = item["meaning"]
            pairs.append((f"Practice: {phrase} in context.", f"Luyện: {phrase} — {meaning}"))
    for lines in PHRASAL_DIALOGUES.values():
        for ln in lines:
            text = ln.get("text", "")
            if not text or text.startswith("Next:"):
                continue
            speaker = ln.get("speaker", "")
            if speaker == "Hook" or speaker == "Caption":
                pairs.append((text, f"Tiếp theo: {text.replace('Next: ', '')}"))
            else:
                pairs.append((text, f"({speaker}) {text}"))
    return pairs


_RAW_SENTENCE_PAIRS = _build_sentence_pairs()

PHRASAL_SENTENCE_VI: dict[str, str] = {
    _normalize_match(en): vi for en, vi in _RAW_SENTENCE_PAIRS
}

PHRASAL_PHRASE_NOTES: dict[str, str] = {}
for _slug, items in PHRASAL_FOCUS.items():
    for item in items:
        PHRASAL_PHRASE_NOTES[item["phrase"].lower()] = item["meaning"]

PHRASAL_GRAMMAR_PATTERNS: list[tuple[str, str]] = [
    (r"\blook into\b", "**look into + noun** = điều tra / tìm hiểu kỹ."),
    (r"\blook up\b", "**look up + noun** = tra cứu (docs, spec, số liệu)."),
    (r"\blook out for\b|\blook out\b", "**look out for + noun** = cẩn thận / để ý."),
    (r"\blook through\b", "**look through + noun** = xem xét từng phần (logs, file)."),
    (r"\blook over\b", "**look over + noun** = xem lại nhanh (PR, bản nháp)."),
    (r"\blook like\b|\blooks like\b", "**look like + clause** = có vẻ như / trông giống."),
    (r"\blook forward to\b", "**look forward to + V-ing/noun** = mong chờ."),
    (r"\blook up to\b", "**look up to + person** = ngưỡng mộ / noi theo."),
    (r"\blook for\b", "**look for + noun** = tìm kiếm."),
    (r"\blook back on\b|\blook back at\b", "**look back on + noun** = nhìn lại (quá khứ)."),
    (r"\blook ahead\b", "**look ahead** = nhìn về tương lai / lập kế hoạch."),
    (r"\blook around\b", "**look around** = nhìn quanh / khám phá."),
    (r"\blook after\b", "**look after + person/thing** = chăm sóc / trông coi."),
    (r"\btake over\b", "**take over + noun** = tiếp quản / đảm nhận."),
    (r"\btake on\b", "**take on + responsibility** = nhận thêm trách nhiệm."),
    (r"\btake apart\b", "**take apart + noun** = tháo rời / phân tích từng phần."),
    (r"\btake off\b", "**take off** = cất cánh / bùng nổ / rời đi nhanh."),
    (r"\btake ownership\b", "**take ownership of + noun** = chịu trách nhiệm hoàn toàn."),
    (r"\btake the heat\b|\btake heat\b", "**take the heat** = chịu áp lực / chỉ trích."),
    (r"\btake a position\b", "**take a position** = mở vị thế (tài chính) / lập trường."),
    (r"\btake out\b", "**take out + trash/food** = đổ rác / mang đi (ăn)."),
    (r"\btake your time\b", "**take your time** = cứ từ từ / không vội."),
    (r"\bput off\b", "**put off + noun/V-ing** = hoãn lại."),
    (r"\bput together\b", "**put together + noun** = lắp ráp / soạn thảo."),
    (r"\bput up with\b", "**put up with + noun** = chịu đựng."),
    (r"\bput forward\b", "**put forward + idea** = đề xuất."),
    (r"\bput aside\b", "**put aside + noun** = gác lại / dành riêng."),
    (r"\bput out\b", "**put out + fire/issue** = dập lửa / xử lý sự cố."),
    (r"\bput down\b", "**put down + deposit** = đặt cọc."),
    (r"\bput up\b", "**put up + shelves/rent** = lắp / cho thuê."),
    (r"\bput away\b", "**put away + things** = cất đi."),
    (r"\bput in an offer\b", "**put in an offer** = nộp đề nghị (thuê/mua)."),
    (r"\bcome across\b", "**come across + noun** = tình cờ gặp / phát hiện."),
    (r"\bcome up with\b", "**come up with + idea** = nghĩ ra."),
    (r"\bcome along\b", "**come along** = đi cùng / tiến triển."),
    (r"\bcome through\b", "**come through (for someone)** = làm được / không phụ lòng."),
    (r"\bcome down to\b", "**come down to + noun** = quy về / còn lại."),
    (r"\bcome up\b", "**come up** = nảy sinh (vấn đề) / đến (meeting)."),
    (r"\bcome over\b", "**come over** = ghé qua nhà/văn phòng."),
    (r"\bcome across as\b", "**come across as + adj** = tạo ấn tượng là."),
    (r"\bcome in handy\b", "**come in handy** = hữu ích khi cần."),
    (r"\bcome to terms with\b", "**come to terms with + noun** = chấp nhận / thỏa thuận."),
    (r"\bcome by\b", "**come by + place** = ghé qua."),
    (r"\bcome back to\b", "**come back to + topic** = quay lại chủ đề."),
    (r"\bcome full circle\b", "**come full circle** = tròn trịa / quay về điểm xuất phát."),
    (r"\bgo over\b", "**go over + checklist** = rà soát từng mục."),
    (r"\bgo through\b", "**go through + process** = trải qua / kiểm tra kỹ."),
    (r"\bgo ahead\b", "**go ahead** = cứ làm đi / được phép tiếp tục."),
    (r"\bgo down\b", "**go down** = sập (hệ thống) / giảm."),
    (r"\bgo with\b", "**go with + option** = chọn phương án."),
    (r"\bgo live\b", "**go live** = lên production / phát sóng."),
    (r"\bgo along with\b", "**go along with + plan** = đồng ý theo."),
    (r"\bgo out of your way\b", "**go out of your way** = bất chấp bất tiện để giúp."),
    (r"\bgo back\b", "**go back to + place/topic** = quay lại."),
    (r"\bgo for it\b", "**go for it** = cứ thử / làm luôn."),
    (r"\bfollow up\b", "**follow up on + topic** = theo dõi / nhắc lại."),
    (r"\bescalate\b", "**escalate to + team** = chuyển cấp xử lý."),
    (r"\bhand off\b", "**hand off to + person** = bàn giao cho."),
]

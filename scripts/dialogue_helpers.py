"""Helpers for episode dialogue parsing and beginner-friendly explanations."""

from __future__ import annotations

import re

from beginner_vocab import (
    GRAMMAR_PATTERNS,
    PHRASE_NOTES,
    SENTENCE_VI,
    WORD_NOTES,
)
from comic_dialogue.canonical import get_canonical_lines

SPEAKER_VI = {
    "nam": "Nam (kỹ sư junior)",
    "kenji": "Kenji (Tech Lead)",
    "aoi": "Aoi (Senior Engineer)",
    "linh": "Linh (QA)",
    "recruiter": "Recruiter (nhân viên tuyển dụng)",
    "interviewer": "Interviewer (người phỏng vấn)",
    "manager": "Manager (quản lý)",
    "pm": "PM (Product Manager)",
    "colleague": "Đồng nghiệp",
    "friend": "Bạn",
    "agent": "Nhân viên môi giới BĐS",
    "staff": "Nhân viên",
    "waiter": "Nhân viên quán",
    "landlord": "Chủ nhà",
    "doctor": "Bác sĩ",
}

# Legacy tech terms kept alongside beginner_vocab
WORD_NOTES.update({
    "role": "vị trí công việc",
    "full-stack": "làm cả frontend lẫn backend",
    "attracted": "thu hút, khiến bạn quan tâm",
    "whether": "liệu có… hay không (dùng khi chọn giữa 2 phương án)",
    "500 errors": "lỗi HTTP 500 — lỗi phía server",
    "coming from": "bắt nguồn từ / xuất phát từ",
    "stakeholder": "bên liên quan cần được cập nhật",
    "negotiate": "thương lượng",
})

SPEECH_RE = re.compile(
    r'(?:Dialogue|Speech):\s*([^:"]+?):\s*"([^"]+)"',
    re.IGNORECASE,
)
HOOK_RE = re.compile(
    r'(?:Dialogue|Speech):\s*(Next:\s*.+?)(?:\s*$|\.\.)',
    re.IGNORECASE,
)
PLAIN_SPEECH_RE = re.compile(
    r'(?:Dialogue|Speech):\s*([A-Za-z][^:"]+?):\s*([^"\n]+)',
    re.IGNORECASE,
)
ARC_SPEECH_RE = re.compile(
    r'([^:|*→\n]+?):\s*\*"([^"]+)"\*',
)
PANEL_NUM_RE = re.compile(r"Panel\s+(\d+)", re.IGNORECASE)


def normalize(text: str) -> str:
    t = (text or "").lower().replace("\u2019", "'").replace("\u2018", "'")
    return re.sub(r"\s+", " ", t.strip().rstrip(".!?"))


def normalize_match(text: str) -> str:
    """Looser normalize for sentence/phrase lookup (ignore punctuation)."""
    t = normalize(text)
    t = re.sub(r"[^\w\s']", " ", t)
    return re.sub(r"\s+", " ", t).strip()


def title_options(title: str) -> tuple[str, str]:
    """Split episode title into A/B options for pattern filling."""
    clean = (title or "").rstrip("?").strip()
    if " or " in clean.lower():
        parts = re.split(r"\s+or\s+", clean, maxsplit=1, flags=re.IGNORECASE)
        a, b = parts[0].strip(), parts[1].strip()
        return a.lower(), b.lower()
    if " vs " in clean.lower():
        parts = re.split(r"\s+vs\.?\s+", clean, maxsplit=1, flags=re.IGNORECASE)
        return parts[0].strip().lower(), parts[1].strip().lower()
    return "option A", "option B"


def fill_pattern(phrase: str, title: str) -> str:
    """Fill A/B placeholders using episode title."""
    a, b = title_options(title)
    a_short = a.split()[0] if a else "this"
    p = (phrase or "").strip()

    # Phrasal-only patterns → full sentence
    if normalize(p) in ("go with", "rule out", "stick with", "opt for", "sleep on it"):
        return f"I think I'll go with {a_short}."
    if p.lower().startswith("go with"):
        return f"I think I'll go with {a_short}."

    out = p
    replacements = [
        ("A and B.", f"{a} and {b}."),
        ("A and B", f"{a} and {b}"),
        ("A or B.", f"{a} or {b}."),
        ("A or B", f"{a} or {b}"),
        ("A to B.", f"{a} to {b}."),
        ("A to B", f"{a} to {b}"),
        ("A than B.", f"{a} than {b}."),
        ("A than B", f"{a} than {b}"),
        (" toward A.", f" toward {a_short}."),
        (" toward A,", f" toward {a_short},"),
        (" toward A", f" toward {a_short}"),
        (" go with A.", f" go with {a_short}."),
        ("I'll go with A.", f"I'll go with {a_short}."),
        ("A makes more sense", f"{a_short} makes more sense"),
        ("A is better", f"{a_short} is better"),
        ("interested in A.", f"interested in {a_short}."),
        (" to A.", f" to {a_short}."),
        (" to A,", f" to {a_short},"),
        ("A.", f"{a_short}."),
        ("A,", f"{a_short},"),
    ]
    for old, new in replacements:
        if old in out:
            out = out.replace(old, new)
    if out.endswith("..."):
        out = out.replace("...", f" {a}")
    if not out.endswith(("?", "!", ".")):
        out += "."
    return out


def parse_speech_from_line(line: str, default_panel: int | None = None) -> list[dict]:
    """Extract speaker + quote from a markdown line."""
    panel = default_panel
    pm = PANEL_NUM_RE.search(line)
    if pm:
        panel = int(pm.group(1))
    results = []
    for m in SPEECH_RE.finditer(line):
        speaker = m.group(1).strip()
        text = m.group(2).strip()
        if len(text) >= 4:
            results.append({"panel": panel, "speaker": speaker, "text": text})
    if results:
        return results
    hm = HOOK_RE.search(line)
    if hm:
        text = hm.group(1).strip().rstrip(".")
        if len(text) >= 4:
            return [{"panel": panel or 6, "speaker": "Hook", "text": text}]
    for chunk in re.split(r"\s*→\s*", line):
        for m in ARC_SPEECH_RE.finditer(chunk):
            speaker = m.group(1).strip()
            text = m.group(2).strip()
            if len(text) >= 4:
                results.append({"panel": panel, "speaker": speaker, "text": text})
    if results:
        return results
    for m in PLAIN_SPEECH_RE.finditer(line):
        speaker = m.group(1).strip()
        text = m.group(2).strip().rstrip(".")
        if speaker.lower().startswith("next"):
            continue
        if len(text) >= 4 and not text.lower().startswith("next:"):
            results.append({"panel": panel, "speaker": speaker, "text": text})
    return results


LINE_VI_HINTS = {
    "let me walk you through it step by step": "Để tôi giải thích cho bạn từng bước một.",
    "that's where the 500 errors are coming from": "Đó là nơi các lỗi 500 đang phát sinh.",
    "good. now let's find the root cause": "Tốt. Giờ chúng ta tìm nguyên nhân gốc nhé.",
    "it seems like the confirm call fails after the cache update": "Có vẻ như lệnh confirm thất bại sau khi cập nhật cache.",
    "i'm torn between": "Tôi phân vân giữa",
    "i'm leaning toward": "Tôi đang nghiêng về",
    "i think i'll go with": "Tôi nghĩ tôi sẽ chọn",
    "we need to choose": "Chúng ta cần chọn",
    "users are reporting": "User đang báo cáo",
}


def phrase_words(text: str) -> set[str]:
    return set(re.findall(r"[a-z']+", normalize(text)))


def phrase_is_in_line(phrase_norm: str, line_norm: str) -> bool:
    """True only when the focus phrase actually appears in the dialogue line."""
    if not phrase_norm or not line_norm:
        return False
    if phrase_norm == line_norm:
        return True
    if len(phrase_norm) >= 5 and phrase_norm in line_norm:
        return True
    pw = phrase_words(phrase_norm)
    lw = phrase_words(line_norm)
    if not pw:
        return False
    overlap = pw & lw
    if len(pw) <= 2:
        return len(overlap) == len(pw)
    return len(overlap) >= max(2, int(len(pw) * 0.55))


def build_fallback_vi(text: str) -> str:
    """Piece together a readable VI line from known phrases/words."""
    norm = normalize(text)
    parts: list[str] = []
    covered: set[str] = set()

    for key in sorted(PHRASE_NOTES.keys(), key=len, reverse=True):
        if key in norm and key not in covered:
            parts.append(f"«{key}» = {PHRASE_NOTES[key].split('—')[0].strip()}")
            covered.add(key)

    if not parts:
        for tok in re.findall(r"[a-z']+", norm):
            if tok in WORD_NOTES and tok not in covered:
                parts.append(f"«{tok}» = {WORD_NOTES[tok].split('—')[0].strip()}")
                covered.add(tok)
            if len(parts) >= 4:
                break

    if parts:
        return "Câu này có: " + "; ".join(parts[:5]) + "."
    return ""


def lookup_line_vi(text: str, focus_map: dict, ep: dict) -> str:
    """Find Vietnamese translation for a dialogue line."""
    norm = normalize_match(text)

    for sent_key, vi in sorted(SENTENCE_VI.items(), key=lambda x: -len(x[0])):
        sk = normalize_match(sent_key)
        if sk in norm or norm in sk:
            return vi

    for hint, vi in LINE_VI_HINTS.items():
        if hint in norm:
            if hint == "i'm torn between":
                a, b = title_options(ep.get("title", ""))
                return f"Tôi phân vân giữa {a} và {b}."
            if hint == "i'm leaning toward":
                a, _ = title_options(ep.get("title", ""))
                return f"Tôi đang nghiêng về {a.split()[0] if a else 'phương án này'}."
            if hint == "i think i'll go with":
                a, _ = title_options(ep.get("title", ""))
                return f"Tôi nghĩ tôi sẽ chọn {a.split()[0] if a else 'phương án này'}."
            if hint == "we need to choose":
                a, b = title_options(ep.get("title", ""))
                return f"Chúng ta cần chọn — {a} hay {b}?"
            return vi

    for key, vi in focus_map.items():
        kn = normalize(key)
        if kn == norm or phrase_is_in_line(kn, norm):
            return vi or ""

    for f in ep.get("englishFocus") or []:
        phrase = f.get("phrase", "")
        pn = normalize(phrase.replace("...", ""))
        filled = normalize(fill_pattern(phrase, ep.get("title", "")))
        if phrase_is_in_line(pn, norm) or phrase_is_in_line(filled, norm):
            return f.get("meaning", "")

    return build_fallback_vi(text)


def word_breakdown(text: str, max_items: int = 10) -> list[dict]:
    """Extract phrases and words with beginner-friendly notes."""
    low = text.lower()
    found: list[dict] = []
    seen: set[str] = set()

    def add(word: str, note: str) -> None:
        w = word.strip()
        if not w or w in seen:
            return
        seen.add(w)
        found.append({"word": w, "note": note})

    for key in sorted(PHRASE_NOTES.keys(), key=len, reverse=True):
        if key in low:
            add(key, PHRASE_NOTES[key])

    for m in re.finditer(r"\bmore (\w+)\b", low):
        adj = m.group(1)
        comp = f"more {adj}"
        base = WORD_NOTES.get(adj, adj)
        add(comp, f"... hơn — {base}")

    for m in re.finditer(r"\b(\w+)er\b", low):
        w = m.group(1)
        if len(w) >= 3:
            comp = f"{w}er"
            if comp in low and comp not in seen:
                base = WORD_NOTES.get(comp, WORD_NOTES.get(w, f"{w} + er = ... hơn"))
                add(comp, base)

    for key in sorted(WORD_NOTES.keys(), key=len, reverse=True):
        if key in low and not any(key in s for s in seen):
            add(key, WORD_NOTES[key])

    return found[:max_items]


def line_grammar_hint(text: str) -> str:
    low = text.lower()
    hints: list[str] = []
    for pattern, hint in GRAMMAR_PATTERNS:
        if re.search(pattern, low):
            hints.append(hint)
    if "walk me through" in low or "walk you through" in low:
        hints.append("Cấu trúc **walk + someone + through + something** = giải thích từng bước.")
    if "it seems like" in low:
        hints.append("**It seems like + câu** = suy đoán nhẹ, chưa khẳng định 100%.")
    if "that's where" in low or "that is where" in low:
        hints.append("**That's where + câu** = chỉ đúng chỗ/bước gây ra vấn đề.")
    if "looking for a role where" in low:
        hints.append("**a role where + mệnh đề** = mô tả điều kiện công việc bạn muốn.")
    if "see myself" in low:
        hints.append("**see myself + V-ing** = kế hoạch phát triển bản thân trong tương lai.")
    if "tell me about a time when" in low:
        hints.append("**Tell me about a time when + quá khứ** = câu behavioral interview (STAR).")
    if "would it be possible" in low:
        hints.append("**Would it be possible to + V?** = cách negotiate lịch sự.")
    if "the bug affects" in low or " affects " in low:
        hints.append("**affect** (V) = ảnh hưởng; **effect** (N) = tác dụng — đừng nhầm.")
    if "whether to " in low:
        hints.append("**whether to A or B** = không biết nên chọn A hay B.")
    if "following up" in low or "follow up" in low:
        hints.append("**follow up on + topic** = nhắc lại việc đang chờ phản hồi.")
    out: list[str] = []
    for h in hints:
        if h not in out:
            out.append(h)
    return " ".join(out[:4])


def line_story_context(text: str, ep: dict, series_tag: str) -> str:
    low = text.lower()
    title = ep.get("title", "")
    if "?" in text:
        return "dùng để hỏi hoặc đề xuất trong tình huống của tập"
    if any(w in low for w in ("bug", "deploy", "rollback", "api", "500", "cache", "root cause")):
        return "liên quan trực tiếp đến debug/release trong tập này"
    if any(w in low for w in ("role", "interview", "salary", "company")):
        return "liên quan phỏng vấn / career trong tập này"
    if any(w in low for w in ("apartment", "rent", "station", "commute", "landlord", "deposit")):
        return f"liên quan thuê nhà / đời sống Tokyo: {title}"
    if series_tag in ("Du lịch", "Văn hóa", "Anime"):
        return f"gắn với chủ đề du lịch/văn hóa: {title}"
    return f"phục vụ cốt truyện «{title}»"


def is_focus_line(text: str, ep: dict, focus_map: dict) -> bool:
    norm = normalize(text)
    title = ep.get("title", "")
    for f in ep.get("englishFocus") or []:
        phrase = f.get("phrase", "")
        pn = normalize(phrase.replace("...", ""))
        filled = normalize(fill_pattern(phrase, title))
        if phrase_is_in_line(pn, norm) or phrase_is_in_line(filled, norm):
            return True
    for key in focus_map:
        kn = normalize(key.replace("...", ""))
        if kn and phrase_is_in_line(kn, norm):
            return True
    return False


def explain_dialogue_line(line: dict, ep: dict, series: dict, focus_map: dict) -> dict:
    text = line["text"]
    speaker = line.get("speaker", "Nam")
    speaker_key = speaker.split("(")[0].strip().lower()
    speaker_vi = SPEAKER_VI.get(speaker_key, speaker)
    raw_vi = lookup_line_vi(text, focus_map, ep)
    words = word_breakdown(text)
    grammar = line_grammar_hint(text)
    tag = series.get("tag", "")

    vi = raw_vi
    if not vi or vi.startswith("Câu này có:"):
        norm = normalize_match(text)
        for sent_key, sent_vi in sorted(SENTENCE_VI.items(), key=lambda x: -len(x[0])):
            sk = normalize_match(sent_key)
            if sk in norm or norm in sk:
                vi = sent_vi
                break
        if not vi or vi.startswith("Câu này có:"):
            vi = raw_vi or "Xem giải thích từ & cụm bên dưới."

    explain_parts = [f"**{speaker_vi}** nói câu này trong truyện."]
    if vi and not vi.startswith("Câu này có:") and not vi.startswith("Xem giải thích"):
        explain_parts.append(f"**Dịch:** *{vi}*")
    if words:
        explain_parts.append(
            "**Từ & cụm cần biết:** "
            + " · ".join(f"*{w['word']}* — {w['note']}" for w in words)
        )
    if grammar:
        explain_parts.append(f"**Ngữ pháp:** {grammar}")
    explain_parts.append(f"**Ngữ cảnh:** {line_story_context(text, ep, tag)}.")

    return {
        "panel": line.get("panel"),
        "speaker": speaker,
        "en": text,
        "vi": vi,
        "words": words,
        "grammarHint": grammar,
        "explain": " ".join(explain_parts).strip(),
        "isFocus": is_focus_line(text, ep, focus_map),
    }


def get_dialogue_lines_for_episode(
    series_id: str, ep_num: int, prompt_data: dict | None, ep: dict, pack_patterns: dict
) -> list[dict]:
    """Prefer canonical dialogue, then prompt file, then synthesis."""
    key = f"{series_id}/{ep_num}"
    canonical = get_canonical_lines(series_id, ep_num)
    if canonical:
        return list(canonical)

    raw_lines = (prompt_data or {}).get("dialogueLines") or []
    if len(raw_lines) < 6:
        synth = synthesize_dialogue_lines(ep, pack_patterns)
        seen = {normalize(x.get("text", "")) for x in raw_lines}
        for ln in synth:
            t = ln.get("text", "")
            if normalize(t) not in seen and len(t) >= 4:
                raw_lines.append(ln)
                seen.add(normalize(t))
            if len(raw_lines) >= 6:
                break
    if not raw_lines:
        raw_lines = synthesize_dialogue_lines(ep, pack_patterns)
    return raw_lines


def synthesize_dialogue_lines(ep: dict, pack_patterns: dict) -> list[dict]:
    """Build plausible dialogue when no prompt file exists."""
    title = ep.get("title", "")
    focus = ep.get("englishFocus") or []
    lines = []
    question_speakers = ("Kenji", "Recruiter", "Interviewer", "Manager", "PM")

    if focus:
        for i, f in enumerate(focus):
            filled = fill_pattern(f["phrase"], title)
            is_question = "?" in filled or filled.lower().startswith(
                ("can ", "could ", "tell ", "why ", "what ", "where ", "should ")
            )
            if is_question:
                sp = question_speakers[i % len(question_speakers)]
            else:
                sp = "Nam"
            lines.append({"panel": i + 1, "speaker": sp, "text": filled})
        return lines

    # Try pack example
    for pid in ep.get("packs") or []:
        for phrase in pack_patterns.get(pid, []):
            if "A and B" in phrase or "whether to" in phrase or "torn between" in phrase:
                filled = fill_pattern(phrase, title)
                lines.append({"panel": 1, "speaker": "Nam", "text": filled})
                if len(lines) >= 3:
                    return lines
    if not lines:
        a, b = title_options(title)
        lines = [
            {"panel": 1, "speaker": "Kenji", "text": f"Should we go with {a} or {b}?"},
            {"panel": 2, "speaker": "Nam", "text": f"I'm not sure — I'm torn between {a} and {b}."},
            {"panel": 3, "speaker": "Nam", "text": f"I'm leaning toward {a.split()[0] if a else 'this'}."},
        ]
    return lines


def expand_grammar_beginner(rule: dict, episode_example: str = "") -> str:
    """Long-form Vietnamese grammar note for absolute beginners."""
    title = rule.get("title", "")
    rule_text = rule.get("rule", "")
    explain = rule.get("explain", "")
    good = rule.get("exampleGood", "")
    bad = rule.get("exampleBad", "")

    parts = [
        f"**{title}** — giải thích cho người mới:",
        rule_text,
        explain,
    ]
    if good:
        parts.append(f"Ví dụ đúng: *{good}*")
    if bad:
        parts.append(f"Ví dụ sai (tránh): *{bad}*")
    if episode_example:
        parts.append(f"Trong tập này bạn gặp: *{episode_example}*")
    parts.append(
        "Mẹo học: đọc to câu đúng 3 lần, viết lại 1 câu tương tự về công việc/đời sống của bạn."
    )
    return " ".join(p for p in parts if p)

"""Extract dialogue lines from comic PNG using macOS Vision (ocrmac)."""

from __future__ import annotations

import re
from pathlib import Path
from typing import Any

from comic_dialogue.schema import normalize_text

NOISE_PATTERNS = [
    r"^english vault",
    r"^english for real life",
    r"^learn\. live",
    r"^english focus",
    r"^episode \d",
    r"^panel \d$",
    r"^option [ab]$",
    r"^near the station$",
    r"^farther from station$",
    r"^let'?s compare",
    r"^\d+k\s*/",
    r"min walk",
    r"/ month",
    r"month$",
    r"^built:",
    r"^auto-lock",
    r"^delivery box",
    r"^bike parking",
    r"^meguro",
    r"^tokyo debug",
    r"^tip:",
    r"^next episode",
    r"^nam'?s note",
    r"^star$",
    r"^intro$",
    r"^¥",
    r"^•",
    r"^= ",
    r"can't choose between",
    r"more likely to choose",
    r"^what matters most",
    r"^think about your daily",
    r"^closer =",
    r"^time for what you love",
    r"^kenji$",
    r"^linh$",
    r"^aoi$",
    r"^nam$",
    r"^emerg",
    r"^mergem",
    r"^ur$",
    r"^\d{1,2}$",
    r"^debug & release$",
    r"^payment & demo",
    r"^investor demo",
    r"^ship it$",
    r"^no bugs$",
    r"^only features$",
    r"^next:$",
]

NOISE_RES = [re.compile(p, re.I) for p in NOISE_PATTERNS]

SPEAKER_PREFIX_RE = re.compile(
    r"^([A-Za-z][A-Za-z .'()-]{0,30}?):\s*(.+)$"
)

CODE_RE = re.compile(
    r"\b(async|await|const|let |function|\(\)|=>|\{\}|===|!==|getBalance|redis\.)\b",
    re.I,
)

# 6-panel grid (header ~10%, footer ~22%) — see prompts/00-layout-guide.md
PANEL_REGIONS: list[tuple[float, float, float, float]] = [
    (0.02, 0.11, 0.48, 0.34),  # 1 top-left
    (0.52, 0.11, 0.98, 0.34),  # 2 top-right
    (0.02, 0.34, 0.48, 0.55),  # 3 mid-left
    (0.52, 0.34, 0.98, 0.55),  # 4 mid-right
    (0.02, 0.55, 0.48, 0.76),  # 5 bottom-left
    (0.52, 0.55, 0.98, 0.76),  # 6 bottom-right
]

Y_MIN = 0.10
Y_MAX = 0.78


def _is_noise(text: str) -> bool:
    t = text.strip()
    if len(t) <= 1:
        return True
    if t.isdigit() and len(t) <= 2:
        return True
    for rx in NOISE_RES:
        if rx.search(t):
            return True
    letters = sum(c.isalpha() for c in t)
    if letters < 3:
        return True
    return False


def _bbox_center(bbox: list[float]) -> tuple[float, float]:
    x, y, w, h = bbox
    return x + w / 2, y + h / 2


def ocr_annotations(image_path: Path) -> list[tuple[str, float, list[float]]]:
    from ocrmac import ocrmac

    return ocrmac.OCR(str(image_path), language_preference=["en-US"]).recognize()


def _in_region(cx: float, cy: float, region: tuple[float, float, float, float]) -> bool:
    x0, y0, x1, y1 = region
    return x0 <= cx <= x1 and y0 <= cy <= y1


def _join_fragments(items: list[tuple[str, float, float]]) -> str:
    if not items:
        return ""
    items = sorted(items, key=lambda x: (round(x[2], 3), x[1]))
    parts: list[str] = []
    cur: list[str] = []
    last_y = None
    for text, _cx, cy in items:
        if last_y is not None and abs(cy - last_y) > 0.025:
            if cur:
                parts.append(" ".join(cur))
            cur = [text]
        else:
            cur.append(text)
        last_y = cy
    if cur:
        parts.append(" ".join(cur))
    return " ".join(parts)


def _line_quality(text: str) -> float:
    """0–1 score: higher = more like real speech bubble dialogue."""
    t = (text or "").strip()
    if not t or len(t) < 6:
        return 0.0
    score = 0.55
    words = t.split()
    n = len(words)
    if 4 <= n <= 22:
        score += 0.15
    elif n > 30:
        score -= 0.35
    elif n > 22:
        score -= 0.15
    if len(t) > 100:
        score -= 0.2
    if len(t) > 150:
        score -= 0.25
    if t.endswith((".", "!", "?")):
        score += 0.08
    upper = sum(1 for w in words if w.isupper() and len(w) > 2)
    if n and upper / n > 0.35:
        score -= 0.35
    if CODE_RE.search(t):
        score -= 0.45
    if t.count('"') >= 4 or t.count("'") >= 6:
        score -= 0.25
    if re.search(r"\b(NEXT|SHIP IT|NO BUGS|ONLY FEATURES|REPRO STEPS|NOT AFFECTED)\b", t, re.I):
        score -= 0.3
    if re.match(r"^[A-Za-z\"'(IWeLetTheWhatHowCan]", t):
        score += 0.05
    return max(0.0, min(1.0, score))


def dialogue_quality_score(lines: list[dict]) -> float:
    if not lines:
        return 0.0
    scores = [_line_quality(ln.get("text", "")) for ln in lines]
    avg = sum(scores) / len(scores)
    if len(lines) < 5:
        avg -= 0.15
    return max(0.0, avg)


def _panel_candidates(blob: str) -> list[str]:
    blob = re.sub(r"\s+", " ", blob).strip()
    if not blob:
        return []
    candidates: list[str] = []
    # Quoted speech fragments
    for m in re.finditer(r'"([^"]{8,120})"', blob):
        candidates.append(m.group(1).strip())
    # Sentence splits
    for part in re.split(r"(?<=[.!?])\s+", blob):
        part = part.strip().strip('"')
        if len(part) >= 8 and not _is_noise(part):
            candidates.append(part)
    # Whole blob if short enough
    if 8 <= len(blob) <= 90 and not _is_noise(blob):
        candidates.append(blob)
    # Deduplicate
    seen: set[str] = set()
    out: list[str] = []
    for c in candidates:
        k = normalize_text(c)
        if k in seen:
            continue
        seen.add(k)
        out.append(c)
    return out


def _pick_best_panel_text(candidates: list[str]) -> str:
    if not candidates:
        return ""
    return max(candidates, key=lambda c: (_line_quality(c), len(c)))


def _extract_panel_text(
    annotations: list[tuple[str, float, list[float]]],
    region: tuple[float, float, float, float],
) -> str:
    items: list[tuple[str, float, float]] = []
    for text, conf, bbox in annotations:
        if conf < 0.45:
            continue
        if _is_noise(text):
            continue
        cx, cy = _bbox_center(bbox)
        if not _in_region(cx, cy, region):
            continue
        items.append((text.strip(), cx, cy))
    if not items:
        return ""
    blob = _join_fragments(items)
    candidates = _panel_candidates(blob)
    return _pick_best_panel_text(candidates)


def extract_dialogue_from_image(
    image_path: Path,
    script_hint: list[dict] | None = None,
) -> list[dict[str, Any]]:
    if not image_path.exists():
        return []
    annotations = ocr_annotations(image_path)
    hint = script_hint or []
    lines: list[dict] = []
    for i, region in enumerate(PANEL_REGIONS, 1):
        text = _extract_panel_text(annotations, region)
        if not text:
            continue
        speaker = "Nam"
        m = SPEAKER_PREFIX_RE.match(text)
        if m:
            speaker = m.group(1).strip()
            text = m.group(2).strip().strip('"')
        else:
            matched = False
            for ln in hint:
                if ln.get("panel") == i:
                    speaker = ln.get("speaker") or "Nam"
                    matched = True
                    break
            if not matched and 0 <= i - 1 < len(hint):
                speaker = hint[i - 1].get("speaker") or "Nam"
        lines.append({"panel": i, "speaker": speaker, "text": text})
    return lines[:6]


def _panel_ocr_blob(
    annotations: list[tuple[str, float, list[float]]],
    panel: int,
) -> str:
    if panel < 1 or panel > 6:
        return ""
    region = PANEL_REGIONS[panel - 1]
    items: list[str] = []
    for text, conf, bbox in annotations:
        if conf < 0.4:
            continue
        cx, cy = _bbox_center(bbox)
        if _in_region(cx, cy, region):
            items.append(text)
    return normalize_text(" ".join(items))


def _word_hit_ratio(text: str, blob: str) -> float:
    words = [w for w in normalize_text(text).split() if len(w) > 2]
    if not words or not blob:
        return 0.0
    hit = sum(1 for w in words if w in blob)
    return hit / len(words)


def verify_image_matches_dialogue(
    image_path: Path,
    lines: list[dict],
    *,
    threshold: float = 0.55,
) -> tuple[bool, float]:
    if not image_path.exists() or not lines:
        return False, 0.0
    annotations = ocr_annotations(image_path)
    full_blob = normalize_text(" ".join(a[0] for a in annotations))
    scores: list[float] = []
    for ln in lines:
        panel = ln.get("panel") or (len(scores) + 1)
        panel_blob = _panel_ocr_blob(annotations, panel)
        panel_score = _word_hit_ratio(ln["text"], panel_blob)
        full_score = _word_hit_ratio(ln["text"], full_blob)
        scores.append(max(panel_score, full_score))
    if not scores:
        return False, 0.0
    avg = sum(scores) / len(scores)
    return avg >= threshold, avg


def pick_best_dialogue(
    image_path: Path,
    script_hint: list[dict] | None,
    *,
    threshold: float = 0.55,
) -> tuple[list[dict], str, float]:
    """Choose script or panel OCR by verification + dialogue quality."""
    hint = (script_hint or [])[:6]
    hint_score = 0.0
    hint_ok = False
    hint_quality = dialogue_quality_score(hint) if hint else 0.0
    if hint:
        hint_ok, hint_score = verify_image_matches_dialogue(image_path, hint, threshold=threshold)

    ocr_lines = extract_dialogue_from_image(image_path, hint)
    ocr_quality = dialogue_quality_score(ocr_lines)
    ocr_score = 0.0
    ocr_ok = False
    if ocr_lines:
        ocr_ok, ocr_score = verify_image_matches_dialogue(image_path, ocr_lines, threshold=threshold)
    ocr_min = min((_line_quality(ln["text"]) for ln in ocr_lines), default=0.0)
    ocr_usable = (
        ocr_lines
        and len(ocr_lines) >= 5
        and ocr_quality >= 0.62
        and ocr_min >= 0.4
    )

    if hint and len(hint) >= 5 and hint_ok and hint_quality >= 0.55:
        return hint, "script+verified", hint_score

    if ocr_usable and ocr_ok and ocr_quality >= hint_quality + 0.05:
        return ocr_lines, "ocr", ocr_score

    if hint and len(hint) >= 5 and hint_quality >= 0.55 and hint_score >= 0.48:
        return hint, "script+verified" if hint_ok else "script-unverified", hint_score

    if ocr_usable and ocr_ok:
        return ocr_lines, "ocr", ocr_score

    if hint and len(hint) >= 5:
        return hint, "script-unverified", hint_score
    return ocr_lines or hint, "ocr-weak", ocr_score

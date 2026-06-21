"""Dialogue record schema and validation."""

from __future__ import annotations

import re
from typing import Any

SPEECH_RE = re.compile(
    r'^([A-Za-z][A-Za-z .\'()-]{0,40}?):\s*["\']?(.+?)["\']?\s*$'
)
MULTI_SPEECH_RE = re.compile(
    r'([A-Za-z][A-Za-z .\'-]{0,30}?):\s*\*"([^"]+)"\*'
)
INLINE_SPEECH_RE = re.compile(
    r'([A-Za-z][A-Za-z .\'()-]{0,40}?):\s*"([^"]+)"'
)

KNOWN_SPEAKERS = {
    "nam", "kenji", "aoi", "linh", "agent", "recruiter", "interviewer",
    "manager", "pm", "landlord", "friend", "staff", "investor", "waiter",
    "doctor", "colleague", "customer", "receptionist", "hook", "next",
}


def parse_speech_field(raw: str) -> list[dict[str, Any]]:
    """Parse 'Speaker: \"text\"' or arc-style Speaker: *\"text\"*."""
    raw = (raw or "").strip()
    if not raw:
        return []
    if raw.lower().startswith("next:"):
        return [{"panel": None, "speaker": "Hook", "text": raw.rstrip(".")}]

    # Multiple quoted speakers on one line (common in comic panel beats)
    inline = list(INLINE_SPEECH_RE.finditer(raw))
    if len(inline) >= 1:
        out: list[dict[str, Any]] = []
        for m in inline:
            speaker, text = m.group(1).strip(), m.group(2).strip()
            if speaker.lower() == "next":
                speaker = "Hook"
                text = f"Next: {text}"
            out.append({"speaker": speaker, "text": text})
        return out

    parts = re.split(r"\s*→\s*", raw)
    out = []
    for part in parts:
        part = part.strip()
        m = SPEECH_RE.match(part)
        if not m:
            m2 = MULTI_SPEECH_RE.search(part)
            if m2:
                out.append({"speaker": m2.group(1).strip(), "text": m2.group(2).strip()})
                continue
            if part.startswith('"') and part.endswith('"'):
                out.append({"speaker": "Nam", "text": part.strip('"')})
            continue
        speaker, text = m.group(1).strip(), m.group(2).strip().strip('"\'')
        if speaker.lower() == "next":
            speaker = "Hook"
            text = f"Next: {text}"
        out.append({"speaker": speaker, "text": text})
    return out


def normalize_text(text: str) -> str:
    t = (text or "").lower().replace("\u2019", "'").replace("\u2018", "'")
    t = re.sub(r"[^\w\s']", " ", t)
    return re.sub(r"\s+", " ", t).strip()


def validate_episode_dialogue(lines: list[dict], *, min_panels: int = 5) -> list[str]:
    errors: list[str] = []
    if len(lines) < min_panels:
        errors.append(f"expected >={min_panels} dialogue lines, got {len(lines)}")
    for i, ln in enumerate(lines):
        if not (ln.get("text") or "").strip():
            errors.append(f"line {i+1}: empty text")
        if len((ln.get("text") or "")) < 4:
            errors.append(f"line {i+1}: text too short")
    return errors

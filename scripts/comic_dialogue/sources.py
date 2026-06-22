"""Import dialogue hints from prompts, arc scripts, generate-comic-prompts.py."""

from __future__ import annotations

import ast
import importlib.util
import json
import re
from pathlib import Path
from typing import Any

from comic_dialogue.schema import parse_speech_field

ROOT = Path(__file__).resolve().parent.parent.parent


def parse_prompt_md(path: Path) -> list[dict[str, Any]]:
    if not path.exists():
        return []
    content = path.read_text(encoding="utf-8")

    # Prefer synced canonical JSON block
    canon_m = re.search(
        r"## Canonical dialogue \(synced from image — do not edit by hand\)\n\n```json\n(.*?)\n```",
        content,
        re.S,
    )
    if canon_m:
        try:
            import json

            raw = json.loads(canon_m.group(1))
            if isinstance(raw, list) and raw:
                return raw[:6]
        except json.JSONDecodeError:
            pass

    lines: list[dict[str, Any]] = []
    panel = None
    for raw in content.splitlines():
        pm = re.search(r"Panel\s+(\d+)", raw, re.I)
        if pm:
            panel = int(pm.group(1))
        for m in re.finditer(
            r'(?:Dialogue|Speech):\s*([^:"]+?):\s*"([^"]+)"',
            raw,
            re.I,
        ):
            speaker = m.group(1).strip()
            text = m.group(2).strip()
            if speaker.lower().startswith("next"):
                continue
            lines.append({"panel": panel or len(lines) + 1, "speaker": speaker, "text": text})
        # Story beats: Dialogue: Nam: "..."
        dm = re.search(r"Dialogue:\s*([^:]+):\s*\"([^\"]+)\"", raw, re.I)
        if dm and not re.search(r"Speech:", raw, re.I):
            lines.append({
                "panel": panel or len(lines) + 1,
                "speaker": dm.group(1).strip(),
                "text": dm.group(2).strip(),
            })
    # dedupe by panel preserving order
    seen: set[int] = set()
    out: list[dict] = []
    for ln in lines:
        p = ln.get("panel") or len(out) + 1
        if p in seen:
            continue
        seen.add(p)
        ln["panel"] = p
        out.append(ln)
    return out[:6]


def load_generate_comic_prompts() -> dict[str, list[dict]]:
    """Load EPISODES from generate-comic-prompts.py (supports dynamic imports)."""
    path = ROOT / "scripts" / "generate-comic-prompts.py"
    spec = importlib.util.spec_from_file_location("generate_comic_prompts", path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    episodes = getattr(mod, "EPISODES", None)
    if not episodes:
        return {}
    out: dict[str, list[dict]] = {}
    for ep in episodes:
        key = f"{ep['arc_id']}/{ep['num']}"
        story = ep.get("story") or []
        lines: list[dict] = []
        for i, (_scene, dialogue) in enumerate(story[:6], 1):
            d = (dialogue or "").replace('\\"', '"').strip()
            if d.lower().startswith("next:"):
                lines.append({
                    "panel": i,
                    "speaker": "Hook",
                    "text": d.rstrip("."),
                })
                continue
            parsed = parse_speech_field(d)
            if parsed:
                ln = parsed[0]
                lines.append({"panel": i, "speaker": ln["speaker"], "text": ln["text"]})
            elif d:
                lines.append({"panel": i, "speaker": "Nam", "text": d})
        if lines:
            out[key] = lines
    return out


def parse_arc_scripts() -> dict[str, list[dict]]:
    """Parse prompts/arcs/*.md table dialogue into slug -> lines (ordered)."""
    slug_to_lines: dict[str, list[dict]] = {}
    current_slug = None
    current_lines: list[dict] = []

    def flush():
        nonlocal current_slug, current_lines
        if current_slug and current_lines:
            slug_to_lines[current_slug] = current_lines[:6]
        current_lines = []

    arc_dir = ROOT / "prompts" / "arcs"
    for path in sorted(arc_dir.glob("*.md")):
        content = path.read_text(encoding="utf-8")
        for line in content.splitlines():
            slug_m = re.search(r"\*\*Slug\*\*\s*\|\s*`([^`]+)`", line)
            if slug_m:
                flush()
                current_slug = slug_m.group(1)
                continue
            # | 1 | ... | Nam: *"..."* |
            row = re.match(
                r"^\|\s*(\d+)\s*\|(?:[^|]*\|)?\s*(.+?)\s*\|?\s*$",
                line,
            )
            if not row or not current_slug:
                continue
            panel = int(row.group(1))
            dialogue_cell = row.group(2)
            if panel < 1 or panel > 6:
                continue
            cell = dialogue_cell.replace("*", "").strip()
            parsed = parse_speech_field(cell)
            if not parsed:
                for m in re.finditer(r"([A-Za-z][A-Za-z ()]+):\s*\"([^\"]+)\"", cell):
                    parsed.append({"speaker": m.group(1).strip(), "text": m.group(2).strip()})
            for p in parsed:
                if p.get("speaker", "").lower() == "hook":
                    continue
                current_lines.append({"panel": panel, "speaker": p["speaker"], "text": p["text"]})
        flush()
        current_slug = None
    return slug_to_lines


def slug_to_key(comics: dict, slug: str) -> str | None:
    for series in comics["series"]:
        for ep in series["episodes"]:
            if ep.get("slug") == slug:
                return f"{series['id']}/{ep['num']}"
    return None


def load_missing_prompt_stories(comics: dict) -> dict[str, list[dict]]:
    """Fallback story templates from generate-missing-comic-prompts.py."""
    import importlib.util

    spec = importlib.util.spec_from_file_location(
        "gmp", ROOT / "scripts" / "generate-missing-comic-prompts.py"
    )
    if not spec or not spec.loader:
        return {}
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)

    focus_spec = importlib.util.spec_from_file_location(
        "bcd", ROOT / "scripts" / "build-comics-data.py"
    )
    focus_mod = importlib.util.module_from_spec(focus_spec)
    focus_spec.loader.exec_module(focus_mod)
    focus_dict = focus_mod.FOCUS

    out: dict[str, list[dict]] = {}
    for series in comics["series"]:
        sid = series["id"]
        for ep in series["episodes"]:
            key = f"{sid}/{ep['num']}"
            items = ep.get("englishFocus") or focus_dict.get(ep.get("slug", ""), [])
            story = mod.pick_story(sid, ep, items)
            lines: list[dict] = []
            for i, (_scene, dialogue) in enumerate(story[:6], 1):
                d = (dialogue or "").replace('\\"', '"').strip()
                if d.lower().startswith("next:"):
                    lines.append({"panel": i, "speaker": "Hook", "text": d.rstrip(".")})
                    continue
                parsed = parse_speech_field(d)
                if parsed:
                    ln = parsed[0]
                    lines.append({"panel": i, "speaker": ln["speaker"], "text": ln["text"]})
                elif d:
                    lines.append({"panel": i, "speaker": "Nam", "text": d})
            if len(lines) >= 5:
                out[key] = lines[:6]
    return out


def load_all_script_hints(comics: dict) -> dict[str, list[dict]]:
    """Priority: generate-comic-prompts > missing templates > arc scripts > prompt md."""
    hints: dict[str, list[dict]] = {}
    generated = load_generate_comic_prompts()
    hints.update(generated)

    for key, lines in load_missing_prompt_stories(comics).items():
        if key not in hints and len(lines) >= 5:
            hints[key] = lines

    arc_by_slug = parse_arc_scripts()
    for slug, lines in arc_by_slug.items():
        key = slug_to_key(comics, slug)
        if key and key not in hints and len(lines) >= 5:
            hints[key] = lines

    comic_re = re.compile(r"^([a-z0-9-]+)-t(\d+)-comic\.md$")
    for path in (ROOT / "prompts").glob("*-comic.md"):
        m = comic_re.match(path.name)
        if not m:
            continue
        key = f"{m.group(1)}/{int(m.group(2))}"
        prompt_lines = parse_prompt_md(path)
        if key not in hints:
            if len(prompt_lines) >= 5:
                hints[key] = prompt_lines
        elif len(hints.get(key, [])) < 5 and len(prompt_lines) >= 5:
            hints[key] = prompt_lines
    return hints


def load_comics() -> dict:
    return json.loads((ROOT / "data" / "comics.json").read_text(encoding="utf-8"))

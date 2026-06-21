#!/usr/bin/env python3
"""Audit episode guide dialogue quality — flag weak explanations."""

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
guides = json.loads((ROOT / "data" / "episode-guides.json").read_text(encoding="utf-8"))["guides"]

issues: list[tuple[str, str, int]] = []
stats = {"total": 0, "weak_words": 0, "bad_vi": 0, "no_grammar": 0}

for key, g in sorted(guides.items()):
    lines = g.get("dialogueLines") or []
    if not lines:
        issues.append((key, "no dialogue lines", 0))
        continue
    stats["total"] += 1
    empty_words = sum(1 for d in lines if len(d.get("words") or []) < 2)
    bad_vi = sum(
        1
        for d in lines
        if "cân nhắc (ưu/nhược)" in (d.get("vi") or "")
        and "weigh" not in (d.get("en") or "").lower()
    )
    no_grammar = sum(1 for d in lines if not (d.get("grammarHint") or "").strip())
    avg_words = sum(len(d.get("words") or []) for d in lines) / len(lines)

    if empty_words >= len(lines) // 2:
        stats["weak_words"] += 1
        issues.append((key, f"≥50% lines have <2 word notes (avg {avg_words:.1f})", empty_words))
    if bad_vi:
        stats["bad_vi"] += 1
        issues.append((key, f"wrong VI 'cân nhắc' on {bad_vi} lines", bad_vi))
    if no_grammar == len(lines):
        stats["no_grammar"] += 1
        issues.append((key, "no grammar hints on any line", no_grammar))

print(f"Audited {stats['total']} episodes")
print(f"  weak word coverage: {stats['weak_words']}")
print(f"  wrong VI (weigh leak): {stats['bad_vi']}")
print(f"  no grammar at all: {stats['no_grammar']}")
print()
if issues:
    print("Issues (first 30):")
    for key, msg, n in issues[:30]:
        print(f"  {key}: {msg}")
    if len(issues) > 30:
        print(f"  ... and {len(issues) - 30} more")
else:
    print("No major issues found.")

# Sample ep 26
ep26 = guides.get("living/26", {})
print("\n--- living/26 sample ---")
for d in ep26.get("dialogueLines") or []:
    w = ", ".join(x["word"] for x in (d.get("words") or [])[:5])
    print(f"  [{d.get('speaker')}] {d.get('en')[:60]}...")
    print(f"    VI: {d.get('vi')}")
    print(f"    Words: {w or '(none)'}")

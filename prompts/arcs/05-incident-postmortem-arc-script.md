# Arc Script 5 — Incident & Postmortem (Tập 100–104)

**Arc ID:** `incident-postmortem` · **Màu:** `#DC2626` · **Pack:** `incident_postmortem`
**Tagline arc:** *Blameless Communication — War Room to Postmortem*

---

## Tổng quan arc

Đêm sau demo thành công — checkout lại fail 12%. Arc dạy **status update**, **root cause**, **action items**, **blameless culture**.

**Nam's arc:** On-call panic → clear communicator → postmortem lead → leadership praise.

**Callback:** Ep 48 Incident Recap, Ep 100-104 = deep dive hơn với pattern chuyên biệt.

**Optional:** Bug Phantom silhouette ngoài cửa sổ (không bắt buộc).

---

## Tập 100 — The War Room

| | |
|---|---|
| **Slug** | `the-war-room` |
| **Setting** | War room tối, nhiều monitor, PagerDuty alert, Slack #incident |
| **Mục tiêu học** | Mở war room — facts not blame |

### Kịch bản 6 panel

| Panel | Dialogue |
|-------|----------|
| 1 | PagerDuty: CHECKOUT ERROR > 15% | |
| 2 | Kenji: *"Let's focus on the facts, not blame — status first."* |
| 3 | Nam: *"What we know so far is API timeouts on payment service."* |
| 4 | Aoi: *"I'll dig into the database metrics."* |
| 5 | Linh: *"Last deploy was 2 hours ago — possible correlation."* |
| 6 | Kenji: *"Good — keep updates every 15 minutes."* |

**ENGLISH FOCUS:** What we know so far is… / Let's focus on the facts, not blame. / dig into

**Hook:** Next: What We Know So Far Is...

---

## Tập 101 — What We Know So Far Is...

| | |
|---|---|
| **Slug** | `what-we-know-so-far-is` |
| **Setting** | Zoom call, PM joins, status doc |
| **Mục tiêu học** | Stakeholder update — impact + timeline |

### Kịch bản 6 panel

| Panel | Dialogue |
|-------|----------|
| 1 | PM: *"What's the customer impact?"* |
| 2 | Nam: *"What we know so far is 12% of checkouts are failing."* |
| 3 | Nam: *"The impact was that EU users couldn't complete purchases."* |
| 4 | Nam: *"The timeline of events was: deploy at 8pm, errors at 8:45pm."* |
| 5 | Kenji: *"We rolled back at 9:10pm — errors dropping now."* |
| 6 | PM: *"Clear update — thanks for the timeline."* |

**ENGLISH FOCUS:** What we know so far is… / The impact was that… / The timeline of events was…

**Hook:** Next: Root Cause Analysis

---

## Tập 102 — Root Cause Analysis

| | |
|---|---|
| **Slug** | `root-cause-analysis` |
| **Setting** | Logs terminal, cache diagram |
| **Mục tiêu học** | Hypothesis language — appears to be, might be caused by |

### Kịch bản 6 panel

| Panel | Dialogue |
|-------|----------|
| 1 | Aoi: *"Logs show cache invalidation errors."* |
| 2 | Nam: *"Root cause appears to be stale cache keys after deploy."* |
| 3 | Nam: *"It seems like the new TTL config wasn't applied."* |
| 4 | Linh: *"This might be caused by a missing env variable in staging."* |
| 5 | Kenji: *"Let's verify before we finalize the postmortem."* |
| 6 | Kenji: *"Process gap, not person fault."* |

**ENGLISH FOCUS:** Root cause appears to be… / It seems like… / This might be caused by…

**Hook:** Next: Action Items Going Forward

---

## Tập 103 — Action Items Going Forward

| | |
|---|---|
| **Slug** | `action-items-going-forward` |
| **Setting** | Postmortem doc Google Doc, action table |
| **Mục tiêu học** | Mitigation + prevention + owners |

### Kịch bản 6 panel

| Panel | Dialogue |
|-------|----------|
| 1 | Doc title: Checkout Incident — Action Items | |
| 2 | Nam: *"We mitigated the issue by rolling back within 25 minutes."* |
| 3 | Nam: *"To prevent this from happening again, we'll add a cache integration test."* |
| 4 | Nam: *"Action items going forward: update runbook, fix env check, schedule game day."* |
| 5 | Aoi: *"I'll own the runbook update by Friday."* |
| 6 | Kenji: *"Clear actions — no blame, just improvement."* |

**ENGLISH FOCUS:** Action items going forward… / We mitigated the issue by… / To prevent this from happening again…

**Hook:** Next: Postmortem Finale

---

## Tập 104 — Postmortem Finale

| | |
|---|---|
| **Slug** | `postmortem-finale` |
| **Setting** | Postmortem với leadership, sunrise qua cửa sổ |
| **Mục tiêu học** | Present postmortem + close Career Advanced block |

### Kịch bản 6 panel

| Panel | Dialogue |
|-------|----------|
| 1 | Leadership: *"Walk us through the incident briefly."* |
| 2 | Nam: *"What we know so far is covered in the doc — 12% impact, 25-min recovery."* |
| 3 | Nam: *"Root cause appears to be cache config — fixed and tested."* |
| 4 | Nam: *"Action items going forward are assigned with owners and dates."* |
| 5 | Kenji: *"I'll follow up on the game day drill next sprint."* |
| 6 | Leadership: *"Blameless, clear, actionable — well done."* Nam: *"Incident English — I can handle the war room now."* |

**ENGLISH FOCUS:** (review) What we know so far… / Root cause appears to be… / Action items going forward… / follow up on

**Finale note:** Có thể thêm banner nhỏ *"Career Advanced Arc Complete — 122 Episodes"* (optional poster).

---

## Visual notes

- Red accent `#DC2626` — urgent nhưng không horror
- Monitor: error graphs, Slack #incident channel
- Timeline whiteboard: 8:00 deploy → 8:45 errors → 9:10 rollback
- Blameless poster on wall (optional easter egg)

---

## Liên kết với arc trước

```text
Ep 99 Demo success → Ep 100 Same night incident (ironic twist)
Ep 48 Incident Recap (basic) → Ep 100-104 (professional incident comms)
Ep 84 Interview skills → Nam confident in Ep 104 leadership meeting
```

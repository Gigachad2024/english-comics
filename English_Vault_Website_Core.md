# English Vault Website Core

Use this file as the knowledge backbone for an English Comics / English Vault website.

## 1. Product idea

English Vault is a pattern-based English learning system built around manga/webcomic episodes. Each episode teaches one real-life or work situation through short English dialogue, then reinforces the learning with an **English Focus** box.

Core learning loop:

```text
Speak → Fix → Reuse → Review
```

Website goal:

```text
Comic episode → English Focus → Pattern card → Practice prompt → Review mode
```

The website should not only show images. It should help users understand what English pattern each episode is training.

---

## 2. Main knowledge packs

### Pack A — Decision / Hesitation

Used when the learner is unsure, choosing between options, or asking for advice.

Core patterns:

```text
I don’t know what to + verb.
Question word + to + verb.
I don’t know whether to A or B.
I don’t know if I should A or B.
Should I + verb?
I can’t decide what to + verb.
I can’t decide between A and B.
I’m not sure if / whether...
I have no idea what / which / how to...
I’m wondering if / whether...
I’m torn between A and B.
I’m debating whether to A or B.
```

Common contexts:

```text
food, travel, daily life, software engineering, career decisions, study plans
```

Example:

```text
I’m torn between a quick patch and a full refactor.
I’m debating whether to deploy today or wait for QA.
```

---

### Pack B — Preference / Opinion

Used when the learner needs to say what they prefer, what makes sense, or what option they choose.

Core patterns:

```text
I prefer A to B.
I like A more than B.
I’d rather A than B.
I’m leaning toward A.
A makes more sense to me.
I’m more interested in A.
I’m not really into A.
I think A is better because...
I think I’ll go with A.
```

Main combo:

```text
I’m torn between A and B,
but I’m leaning toward A
because A makes more sense to me.
I think I’ll go with A.
```

Useful phrasal verbs:

```text
go with
rule out
think over
sleep on it
settle on
opt for
narrow down
weigh up
come down to
stick with
pass on
be into
```

Example:

```text
I’m leaning toward a small patch because the deadline is tight.
A small patch makes more sense to me right now.
Let’s stick with the safer approach.
```

---

### Pack C — Bug Report + Agreement / Disagreement + Through Verbs

Used for software engineering communication: explaining bugs, disagreeing politely, and proposing safe next steps.

Core bug report patterns:

```text
The issue is that...
It seems like...
This might be caused by...
The API is returning...
The bug affects...
I think we should...
```

Agreement / disagreement patterns:

```text
That makes sense.
I agree with that.
I see your point, but...
I’m not sure I agree.
I have a different take.
```

Through / role dependency phrases:

```text
act as
rely on
go through
get through
work through
walk through
run through
think through
follow through
fall through
```

Master combo:

```text
I see your point, but the issue is that the API is returning incorrect data for some users.
It seems like this might be caused by the new caching logic.
The bug affects the payment flow, so I think we should wait for QA before deploying.
```

Example:

```text
Can you walk me through the payment flow?
Let’s run through the logs quickly.
We need to think through the risks before deploying.
```

---

### Pack D — Universal Communication Pack V2

Used across travel, software engineering, Japan life, daily life, work meetings, customer support, and self-improvement.

Groups:

```text
1. Asking for Help / Clarification
2. Scheduling / Appointment
3. Daily Life Survival
4. Feeling / Reaction / Small Talk
```

Core philosophy:

```text
Learn one pattern.
Use it in many contexts.
Repeat until it becomes automatic.
```

#### Asking for Help / Clarification

```text
Could you help me with this?
Can you show me how to + verb?
Could you explain this part again?
I’m not sure I understand.
What do you mean by...?
Just to clarify, do you mean A or B?
Let me make sure I got this right.
Could you say that again?
Could you speak a little more slowly?
Sorry, I missed that.
```

Useful phrases:

```text
ask for
look up
find out
figure out
check with
reach out to
get back to
follow up on
```

#### Scheduling / Appointment

```text
Are you available at + time?
Does + time + work for you?
What time works best for you?
Can we move it to tomorrow?
Can we push it back by 30 minutes?
Can we move it up?
I’m running late.
I’ll be there in + time.
I need to reschedule.
Let’s meet at + place.
```

Useful phrases:

```text
set up
push back
move up
put off
show up
run late
fit in
catch up
```

#### Daily Life Survival

```text
I’m looking for...
I’d like to...
Do you have...?
How much is this?
How long does it take?
Is this included?
Is there a cheaper option?
Can I pay by card?
Can I get a receipt?
I need to fill out this form.
I’m here to pick up...
```

Useful phrases:

```text
look for
pick up
drop off
fill out
sign up for
check in
check out
pay for
run out of
deal with
```

#### Feeling / Reaction / Small Talk

```text
I’m excited about...
I’m worried about...
I’m nervous about...
I’m surprised that...
I’m glad that...
That sounds amazing.
That sounds stressful.
I didn’t expect that.
It was worth it.
I’m proud of myself.
```

Useful phrases:

```text
look forward to
calm down
cheer up
stress out
open up
get used to
settle in
hang out
come across
bring back
```

---

### Pack E — Get Phrasal Verbs — Startup & Tech

Used in Silicon Valley / startup work: Slack, standups, ship day, war rooms, acquisition news.

Pack ID: `get_phrasal_startup` · Episodes **105–110** (`silicon-valley-get`)

Core phrases:

```text
get looped in
get up to speed
get buy-in
get aligned
get blocked / get unblocked
get shipped
get pulled into
get back to
get promoted / get acquired
get it
```

---

### Pack F — Get Phrasal Verbs — Travel & Movement

Used when traveling: trains, hotels, directions, weather delays, exploring Switzerland.

Pack ID: `get_phrasal_travel` · Episodes **111–115** (`switzerland-travel`)

Core phrases:

```text
get to
get checked in
get your bearings
get on / get off
get snowed in
get held up
get by / get around
get lost
get swept up in
```

---

### Pack G — Get Phrasal Verbs — Everyday English

Used when learning English daily: meetups, homework, building confidence.

Pack ID: `get_phrasal_everyday` · Episodes **116–118** (`english-everyday-get`)

Core phrases:

```text
get used to
get ready
get through
get it
get back to
get by
```

---

### Get grammar — 5 pattern types

Full guide (Vietnamese): [`prompts/arcs/06-get-phrasal-overview.md`](prompts/arcs/06-get-phrasal-overview.md)

```text
1. get + V3          — result state (get looped in, get shipped, get snowed in)
2. get + adj         — become (get ready, get stuck, get aligned)
3. get + prep + noun — movement & relations (get to, get on, get back to)
4. get + noun        — no preposition (get buy-in, get sign-off, get pinged)
5. get + through / up to / used to / by / it — idioms & fixed combos
```

---

## 3. Website information architecture

Recommended pages:

```text
/episodes
/patterns
/phrasal-verbs
/review-mode
/practice-bank
/arcs
/mistake-map
```

### Episode page

Each episode page should include:

```text
Episode image
Episode title
Arc name
Short story summary
Dialogue lines
English Focus
Patterns used
Phrasal verbs used
Common mistakes
Practice prompts
Next episode link
```

### Pattern card page

Each pattern card should include:

```text
Pattern name
Meaning in Vietnamese
Structure
When to use
Examples across contexts
Common mistakes
Related episodes
Practice prompt
```

### Phrasal verb card page

Each phrasal verb card should include:

```text
Phrase
Meaning in Vietnamese
Core feeling
Structure
Examples: travel / software / Japan life / daily life / work
Common mistakes
Related episodes
```

---

## 4. Comic episode data rules

Very important for the website:

```text
One episode = one separate image file.
Do not treat one image as multiple episodes.
Do not upload a collage as an arc unless it is specifically marked as a poster.
Each image should have one episode title only.
```

Recommended episode object:

```json
{
  "episodeNumber": 45,
  "title": "Quick Patch or Full Refactor?",
  "arc": "Career Growth Arc — Nam Speaks Up at Work",
  "image": "/images/episode-45.png",
  "contexts": ["software-engineering", "work-meeting", "decision"],
  "patterns": [
    "I’m torn between A and B.",
    "I’m leaning toward A because...",
    "A makes more sense to me.",
    "rule out",
    "stick with"
  ],
  "englishFocus": [
    "I’m torn between A and B.",
    "I’m leaning toward A because...",
    "A makes more sense to me.",
    "rule out",
    "stick with"
  ],
  "hook": "Next: Nam has to demo the feature under pressure."
}
```

---

## 5. Arc roadmap

### Traveling Japan Arc — English on the Road

Focus:

```text
travel choices, trains, hotels, food, stations, Kyoto, Fuji, confidence
```

Patterns:

```text
I’m torn between A and B.
I’m leaning toward A.
I prefer A to B.
I’d rather A than B.
go with
rule out
narrow down
weigh up
sleep on it
come down to
settle on
stick with
```

### Living in Japan Arc — English for Real Life

Focus:

```text
apartment, contract, appointment, station, forms, moving day, konbini, bank, clinic, daily confidence
```

Patterns:

```text
Could you help me with this?
Can you walk me through...?
Does Saturday work for you?
I’m running late.
I need to fill out this form.
I ran out of cash.
I’d like to open a bank account.
I’m getting used to life in Japan.
I’m proud of myself.
```

### Career Growth Arc — Nam Speaks Up at Work

Focus:

```text
code review, performance issue, disagreement, architecture, quick patch vs refactor, demo, mentoring, incident recap, speaking up
```

Patterns:

```text
I’m not sure I understand...
Can you walk me through...?
The issue is that...
It seems like...
I see your point, but...
I have a different take.
We need to weigh up...
I’d opt for...
It comes down to...
```

### System Design Arc — Thinking Bigger (Ep 51–60)

Focus:

```text
system design, scalability, trade-offs, architecture diagrams, product requirements, tech leadership
```

Patterns:

```text
I'm weighing up A and B.
It comes down to...
We need to scale under pressure.
Let's walk through the architecture.
The trade-off is...
```

### Email & Async Arc (Ep 61–65)

Focus:

```text
follow-up emails, loop in, async standup, stakeholder updates
```

### Japan Culture Arc (Ep 66–72) · Anime & Manga Arc (Ep 73–78)

Focus:

```text
shrine etiquette, onsen, izakaya, hanami, Akihabara, manga cafe
```

### Career Advanced Arcs (Ep 79–104)

Five arcs: interview, negotiation, feedback, presentation, postmortem — senior-level workplace English.

### Get Phrasal Verbs — 3 arcs (Ep 105–118)

Grammar overview: [`prompts/arcs/06-get-phrasal-overview.md`](prompts/arcs/06-get-phrasal-overview.md)

| Arc | Episodes | Pack | Focus |
|-----|----------|------|-------|
| Silicon Valley Get | 105–110 | `get_phrasal_startup` | Bay Area rotation: loop in, buy-in, ship day, war room, acquisition |
| Switzerland Travel | 111–115 | `get_phrasal_travel` | Alps reward trip: trains, peaks, snow, get around |
| Everyday Get | 116–118 | `get_phrasal_everyday` | Meetup & mentor: get it, get by, get used to |

Five get pattern types:

```text
1. get + V3
2. get + adj
3. get + prep + noun
4. get + noun
5. get + through / up to / used to / by / it
```

### Ideas for Next Arc (Ep 119+)

Focus:

```text
customer support, health & clinic visits, side-project launch, deeper async collaboration
```

---

## 6. Tag system

Use these tags to filter episodes and knowledge cards:

```text
#decision
#hesitation
#preference
#opinion
#bug-report
#agreement
#disagreement
#through-verbs
#asking-help
#clarification
#scheduling
#appointment
#daily-life
#small-talk
#feeling
#travel
#japan-life
#software-engineering
#work-meeting
#career-growth
#system-design
#phrasal-verbs
#mistake-map
```

---

## 7. Review Mode for website

The website can include a “Practice with AI” button using this template:

```text
Bật English Vault Review Mode.
Topic: [selected topic].
Use the patterns from this episode.
Ask me one Vietnamese situation at a time.
I will answer in English.
Correct grammar, word choice, tense, prepositions, articles, and natural phrasing immediately.
Explain mistakes in simple Vietnamese.
Give a natural/native version.
Make me reuse the corrected pattern in a new context.
After 10 questions, summarize my repeated mistakes and mini homework.
```

---

## 8. Common mistake system

Every pattern page should show mistake maps like this:

```text
Wrong: Could you help me this?
Correct: Could you help me with this?
Why: help me with + object
```

```text
Wrong: I’m looking forward to visit Kyoto.
Correct: I’m looking forward to visiting Kyoto.
Why: look forward to + V-ing
```

```text
Wrong: The API is return incorrect data.
Correct: The API is returning incorrect data.
Why: use present continuous for an issue happening now
```

---

## 9. Website UX recommendation

For each comic image, show learning content below the image:

```text
1. What happened in this episode?
2. Key English patterns
3. Pattern explanations in Vietnamese
4. Mistake warnings
5. Try it yourself
6. Related episodes
```

Best learner flow:

```text
Read comic → Notice phrase → Tap phrase → See pattern card → Do mini practice → Review later
```

---

## 10. Core identity of the project

English Vault is not a normal grammar website.

It is:

```text
Manga story + real communication patterns + mistake correction + repeated practice
```

The main promise:

```text
Learn English patterns through stories you actually want to read.
Use the same patterns in travel, software engineering, Japan life, daily life, and work.
```

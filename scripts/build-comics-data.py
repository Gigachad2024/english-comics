#!/usr/bin/env python3
"""Generate data/comics.json and data/roadmap.json for English Vault."""

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

SERIES = [
    {
        "id": "bug-arc-1",
        "title": "Debug & Release",
        "desc": "Patch vs refactor, deploy, Redis, rollback — học tiếng Anh khi debug production cùng team Tokyo",
        "color": "#EF4444",
        "icon": "🐛",
        "tag": "Công việc",
        "arc": "bug-arc-1",
        "episodes": [
            (1, "quick-patch-or-full-refactor", "Quick Patch or Full Refactor?"),
            (2, "deploy-today-or-wait-for-qa", "Deploy Today or Wait for QA?"),
            (3, "redis-or-database-only", "Redis or Database Only?"),
            (4, "rollback-or-hotfix", "Rollback or Hotfix?"),
            (5, "go-or-frontend", "Go or Frontend?"),
            (6, "tokyo-cafe-late-thoughts", "Tokyo Café, Late Thoughts"),
            (7, "settling-on-a-plan", "Settling on a Plan"),
            (8, "team-dinner-in-tokyo", "Team Dinner in Tokyo"),
            (9, "tokyo-or-osaka", "Tokyo or Osaka?"),
            (10, "the-safer-choice", "The Safer Choice"),
        ],
    },
    {
        "id": "bug-arc-2",
        "title": "Payment & Demo Crisis",
        "desc": "Payment page panic, API logs, QA gate, cache — tiếng Anh khi sửa lỗi trước demo",
        "color": "#F97316",
        "icon": "⚡",
        "tag": "Công việc",
        "arc": "bug-arc-2",
        "episodes": [
            (1, "payment-page-panic", "Payment Page Panic"),
            (2, "frontend-relies-on-the-api", "Frontend Relies on the API"),
            (3, "go-through-the-logs", "Go Through the Logs"),
            (4, "qa-checklist-showdown", "QA Checklist Showdown"),
            (5, "demo-flow-drill", "Demo Flow Drill"),
            (6, "when-plans-fall-through", "When Plans Fall Through"),
            (7, "follow-through-the-fix", "Follow Through the Fix"),
            (8, "cache-culprit", "Cache Culprit"),
            (9, "final-risk-meeting", "Final Risk Meeting"),
            (10, "safe-release-finale", "Safe Release Finale"),
        ],
    },
    {
        "id": "bug-arc-3",
        "title": "Investor Demo Nightmare",
        "desc": "Demo nhà đầu tư, rollback, QA gate — quyết định khó dưới áp lực thời gian",
        "color": "#A855F7",
        "icon": "👻",
        "tag": "Công việc",
        "arc": "bug-arc-3",
        "episodes": [
            (1, "investor-demo-nightmare", "Investor Demo Nightmare"),
            (2, "quick-patch-or-rollback", "Quick Patch or Rollback?"),
            (3, "walk-me-through-the-payment-flow", "Walk Me Through the Payment Flow"),
            (4, "cache-suspect", "Cache Suspect"),
            (5, "qa-gate", "QA Gate"),
            (6, "the-safer-choice", "The Safer Choice"),
            (7, "demo-rehearsal", "Demo Rehearsal"),
            (8, "release-plan-at-risk", "Release Plan at Risk"),
            (9, "nam-levels-up", "Nam Levels Up"),
        ],
    },
    {
        "id": "traveling",
        "title": "English on the Road",
        "desc": "Tokyo, Osaka, Kyoto, Fuji — học tiếng Anh khi du lịch Nhật cùng team",
        "color": "#06B6D4",
        "icon": "✈️",
        "tag": "Du lịch",
        "arc": "traveling",
        "global_num": True,
        "episodes": [
            (11, "tokyo-or-osaka", "Tokyo or Osaka?"),
            (12, "train-or-taxi", "Train or Taxi?"),
            (13, "the-hotel-problem", "The Hotel Problem"),
            (14, "sleep-on-the-itinerary", "Sleep on the Itinerary"),
            (15, "settling-on-osaka", "Settling on Osaka"),
            (16, "what-should-i-order", "What Should I Order?"),
            (17, "food-tour-or-shopping", "Food Tour or Shopping?"),
            (18, "lost-in-shinjuku-station", "Lost in Shinjuku Station"),
            (19, "walk-me-through-the-route", "Walk Me Through the Route"),
            (20, "kyoto-before-sunset", "Kyoto Before Sunset"),
            (21, "the-fuji-question", "The Fuji Question"),
            (22, "morning-train-to-fuji", "Morning Train to Fuji"),
            (23, "rainy-day-backup-plan", "Rainy Day Backup Plan"),
            (24, "fuji-clears-up", "Fuji Clears Up"),
            (25, "travel-finale", "Travel Finale"),
        ],
    },
    {
        "id": "living",
        "title": "English for Real Life",
        "desc": "Thuê nhà, hợp đồng, chuyển nhà, ngân hàng — tiếng Anh sống ở Tokyo",
        "color": "#10B981",
        "icon": "🏠",
        "tag": "Cuộc sống",
        "arc": "living",
        "global_num": True,
        "episodes": [
            (26, "new-apartment-in-tokyo", "New Apartment in Tokyo"),
            (27, "can-you-walk-me-through-the-contract", "Can You Walk Me Through the Contract?"),
            (28, "does-saturday-work-for-you", "Does Saturday Work for You?"),
            (29, "running-late-at-shinjuku-station", "Running Late at Shinjuku Station"),
            (30, "fill-out-the-form", "Fill Out the Form"),
            (31, "moving-day", "Moving Day"),
            (33, "opening-a-bank-account", "Opening a Bank Account"),
            (34, "bug-alert-after-work", "Bug Alert After Work"),
            (35, "first-remote-meeting-from-tokyo-apartment", "First Remote Meeting from Tokyo Apartment"),
            (36, "follow-through-on-the-fix", "Follow Through on the Fix"),
            (37, "clinic-appointment", "Clinic Appointment"),
            (38, "getting-used-to-life-in-japan", "Getting Used to Life in Japan"),
            (39, "team-dinner-after-release", "Team Dinner After Release"),
            (40, "english-for-real-life-finale", "English for Real Life Finale"),
        ],
    },
    {
        "id": "career-growth",
        "title": "Career Growth Arc",
        "desc": "Code review, performance, architecture, demo, mentor — Nam dùng tiếng Anh để lead và tạo impact",
        "color": "#6366F1",
        "icon": "🚀",
        "tag": "Công việc",
        "arc": "career-growth",
        "global_num": True,
        "episodes": [
            (41, "first-code-review-in-english", "First Code Review in English"),
            (42, "the-performance-problem", "The Performance Problem"),
            (43, "i-have-a-different-take", "I Have a Different Take"),
            (44, "walk-me-through-the-architecture", "Walk Me Through the Architecture"),
            (45, "quick-patch-or-full-refactor", "Quick Patch or Full Refactor?"),
            (46, "demo-day-pressure", "Demo Day Pressure"),
            (47, "the-junior-asks-for-help", "The Junior Asks for Help"),
            (48, "incident-recap-meeting", "Incident Recap Meeting"),
            (49, "speaking-up", "Speaking Up"),
            (50, "nam-becomes-the-bridge", "Nam Becomes the Bridge"),
        ],
    },
    {
        "id": "system-design",
        "title": "System Design Arc",
        "desc": "Architecture, cache, queue, scale, trade-offs — Nam học nói tiếng Anh khi thiết kế hệ thống",
        "color": "#8B5CF6",
        "icon": "🏗️",
        "tag": "Công việc",
        "arc": "system-design",
        "global_num": True,
        "episodes": [
            (51, "the-system-design-question", "The System Design Question"),
            (52, "monolith-or-microservices", "Monolith or Microservices?"),
            (53, "cache-or-database-first", "Cache or Database First?"),
            (54, "queue-saves-the-day", "Queue Saves the Day"),
            (55, "api-gateway-at-night", "API Gateway at Night"),
            (56, "scale-under-pressure", "Scale Under Pressure"),
            (57, "the-cost-of-overengineering", "The Cost of Overengineering"),
            (58, "explain-it-to-product", "Explain It to Product"),
            (59, "design-review-showdown", "Design Review Showdown"),
            (60, "thinking-bigger-finale", "Thinking Bigger Finale"),
        ],
    },
    {
        "id": "email-async",
        "title": "Email & Async Arc",
        "desc": "Follow-up, loop in, get back to you, async standup — viết email & Slack chuyên nghiệp",
        "color": "#3B82F6",
        "icon": "✉️",
        "tag": "Công việc",
        "arc": "email-async",
        "global_num": True,
        "episodes": [
            (61, "just-following-up-on-the-pr", "Just Following Up on the PR"),
            (62, "loop-me-in-on-the-decision", "Loop Me In on the Decision"),
            (63, "ill-get-back-to-you-by-eod", "I'll Get Back to You by EOD"),
            (64, "async-standup-in-english", "Async Standup in English"),
            (65, "email-async-finale", "Email & Async Finale"),
        ],
    },
    {
        "id": "japan-culture",
        "title": "Japan Culture Arc",
        "desc": "Đền chùa, onsen, izakaya, hanami, matsuri — tiếng Anh khi khám phá văn hóa Nhật sau giờ làm hoặc khi du lịch",
        "color": "#DC2626",
        "icon": "⛩️",
        "tag": "Văn hóa",
        "arc": "japan-culture",
        "global_num": True,
        "episodes": [
            (66, "walk-me-through-shrine-etiquette", "Walk Me Through Shrine Etiquette"),
            (67, "the-onsen-question", "The Onsen Question"),
            (68, "izakaya-after-work", "Izakaya After Work"),
            (69, "cherry-blossom-dilemma", "Cherry Blossom Dilemma"),
            (70, "what-is-omotenashi", "What Is Omotenashi?"),
            (71, "summer-festival-night", "Summer Festival Night"),
            (72, "japan-culture-finale", "Japan Culture Finale"),
        ],
    },
    {
        "id": "anime-manga",
        "title": "Anime & Manga Arc",
        "desc": "Akihabara, manga cafe, anime pilgrimage, figure shop — tiếng Anh khi khám phá thế giới anime manga ở Nhật",
        "color": "#EC4899",
        "icon": "🎌",
        "tag": "Anime",
        "arc": "anime-manga",
        "global_num": True,
        "episodes": [
            (73, "akihabara-or-nakano-broadway", "Akihabara or Nakano Broadway?"),
            (74, "my-first-manga-cafe", "My First Manga Cafe"),
            (75, "anime-pilgrimage-day", "Anime Pilgrimage Day"),
            (76, "figure-store-dilemma", "Figure Store Dilemma"),
            (77, "anime-talk-at-team-lunch", "Anime Talk at Team Lunch"),
            (78, "anime-manga-finale", "Anime & Manga Finale"),
        ],
    },
    {
        "id": "interview-career",
        "title": "Interview & Career Arc",
        "desc": "Phone screen, behavioral questions, salary talk — tiếng Anh phỏng vấn và định hướng sự nghiệp",
        "color": "#F59E0B",
        "icon": "💼",
        "tag": "Career",
        "arc": "interview-career",
        "global_num": True,
        "episodes": [
            (79, "the-first-phone-screen", "The First Phone Screen"),
            (80, "tell-me-about-a-time-when", "Tell Me About a Time When..."),
            (81, "why-do-you-want-this-role", "Why Do You Want This Role?"),
            (82, "the-salary-question", "The Salary Question"),
            (83, "questions-for-the-interviewer", "Questions for the Interviewer"),
            (84, "interview-career-finale", "Interview & Career Finale"),
        ],
    },
    {
        "id": "negotiation-boundaries",
        "title": "Negotiation & Boundaries Arc",
        "desc": "Deadline, scope creep, push back — thương lượng và đặt ranh giới chuyên nghiệp",
        "color": "#14B8A6",
        "icon": "🤝",
        "tag": "Career",
        "arc": "negotiation-boundaries",
        "global_num": True,
        "episodes": [
            (85, "the-tight-deadline", "The Tight Deadline"),
            (86, "would-it-be-possible-to", "Would It Be Possible To...?"),
            (87, "thats-outside-the-scope", "That's Outside the Scope"),
            (88, "push-back-on-scope-creep", "Push Back on Scope Creep"),
            (89, "negotiation-boundaries-finale", "Negotiation & Boundaries Finale"),
        ],
    },
    {
        "id": "giving-feedback",
        "title": "Feedback & 1-on-1 Arc",
        "desc": "1-on-1, constructive feedback, mentoring — tiếng Anh khi lead qua hội thoại",
        "color": "#A855F7",
        "icon": "💬",
        "tag": "Career",
        "arc": "giving-feedback",
        "global_num": True,
        "episodes": [
            (90, "preparing-for-the-1-on-1", "Preparing for the 1-on-1"),
            (91, "one-thing-that-went-well-was", "One Thing That Went Well Was..."),
            (92, "id-suggest-trying", "I'd Suggest Trying..."),
            (93, "how-can-i-support-you", "How Can I Support You?"),
            (94, "feedback-1-on-1-finale", "Feedback & 1-on-1 Finale"),
        ],
    },
    {
        "id": "presentation-pitch",
        "title": "Presentation & Pitch Arc",
        "desc": "Demo structure, key takeaway, Q&A — thuyết trình và pitch cho PM/investor",
        "color": "#F97316",
        "icon": "📊",
        "tag": "Career",
        "arc": "presentation-pitch",
        "global_num": True,
        "episodes": [
            (95, "structuring-the-demo", "Structuring the Demo"),
            (96, "walk-through-the-demo", "Let Me Walk You Through the Demo"),
            (97, "the-key-takeaway-is", "The Key Takeaway Is..."),
            (98, "handling-tough-questions", "Handling Tough Questions"),
            (99, "presentation-pitch-finale", "Presentation & Pitch Finale"),
        ],
    },
    {
        "id": "incident-postmortem",
        "title": "Incident & Postmortem Arc",
        "desc": "War room, root cause, action items — tiếng Anh sự cố và postmortem blameless",
        "color": "#DC2626",
        "icon": "🚨",
        "tag": "Công việc",
        "arc": "incident-postmortem",
        "global_num": True,
        "episodes": [
            (100, "the-war-room", "The War Room"),
            (101, "what-we-know-so-far-is", "What We Know So Far Is..."),
            (102, "root-cause-analysis", "Root Cause Analysis"),
            (103, "action-items-going-forward", "Action Items Going Forward"),
            (104, "postmortem-finale", "Postmortem Finale"),
        ],
    },
    {
        "id": "silicon-valley-get",
        "title": "Silicon Valley Get Arc",
        "desc": "Buy-in, ship day, war room — phrasal verbs get trong startup Bay Area (loop in, blocked, shipped, acquired)",
        "color": "#0EA5E9",
        "icon": "🌉",
        "tag": "Công việc",
        "arc": "silicon-valley-get",
        "global_num": True,
        "episodes": [
            (105, "can-you-loop-me-in", "Can You Loop Me In?"),
            (106, "we-need-buy-in", "We Need Buy-In"),
            (107, "blocked-on-dependencies", "Blocked on Dependencies"),
            (108, "ship-it-friday", "Ship It Friday"),
            (109, "pulled-into-the-war-room", "Pulled Into the War Room"),
            (110, "the-acquisition-news", "The Acquisition News"),
        ],
    },
    {
        "id": "switzerland-travel",
        "title": "Switzerland Travel Arc",
        "desc": "Zurich, Glacier Express, Zermatt — get around, get checked in, get snowed in trên đường khám phá Thụy Sĩ",
        "color": "#059669",
        "icon": "🏔️",
        "tag": "Du lịch",
        "arc": "switzerland-travel",
        "global_num": True,
        "episodes": [
            (111, "landing-in-zurich", "Landing in Zurich"),
            (112, "the-glacier-express", "The Glacier Express"),
            (113, "view-from-the-top", "View from the Top"),
            (114, "snowed-in-at-zermatt", "Snowed In at Zermatt"),
            (115, "lost-on-the-alpine-trail", "Lost on the Alpine Trail"),
        ],
    },
    {
        "id": "english-everyday-get",
        "title": "Everyday Get Arc",
        "desc": "Meetup, homework, daily confidence — get used to, get it, get by khi học và sống bằng tiếng Anh",
        "color": "#D946EF",
        "icon": "📚",
        "tag": "Học tập",
        "arc": "english-everyday-get",
        "global_num": True,
        "episodes": [
            (116, "first-english-meetup", "First English Meetup"),
            (117, "when-you-finally-get-it", "When You Finally Get It"),
            (118, "everyday-get-finale", "Everyday Get Finale"),
        ],
    },
]

FOCUS = {
    "quick-patch-or-full-refactor": [
        {"phrase": "I'm torn between A and B.", "meaning": "Tôi phân vân giữa A và B."},
        {"phrase": "I'm leaning toward A.", "meaning": "Tôi đang nghiêng về A."},
        {"phrase": "go with", "meaning": "chọn (một phương án)"},
    ],
    "payment-page-panic": [
        {"phrase": "The issue is that...", "meaning": "Vấn đề là..."},
        {"phrase": "The API is returning...", "meaning": "API đang trả về..."},
        {"phrase": "The bug affects...", "meaning": "Lỗi ảnh hưởng đến..."},
    ],
    "investor-demo-nightmare": [
        {"phrase": "The issue is that...", "meaning": "Vấn đề là..."},
        {"phrase": "I'm torn between A and B.", "meaning": "Tôi phân vân giữa A và B."},
        {"phrase": "We need to weigh up the trade-offs.", "meaning": "Chúng ta cần cân nhắc đánh đổi."},
    ],
    "walk-me-through-the-payment-flow": [
        {"phrase": "Can you walk me through the payment flow?", "meaning": "Bạn giải thích flow thanh toán cho tôi được không?"},
        {"phrase": "The bug affects the payment flow.", "meaning": "Lỗi ảnh hưởng đến luồng thanh toán."},
        {"phrase": "Walk me through...", "meaning": "Giải thích từng bước cho tôi..."},
    ],
    "tokyo-or-osaka": [
        {"phrase": "I'm torn between A and B.", "meaning": "Tôi phân vân giữa A và B."},
        {"phrase": "I'm leaning toward A.", "meaning": "Tôi đang nghiêng về A."},
        {"phrase": "A makes more sense to me.", "meaning": "A hợp lý hơn với tôi."},
    ],
    "what-should-i-order": [
        {"phrase": "I don't know what to + verb.", "meaning": "Tôi không biết phải + V."},
        {"phrase": "I can't decide what to + verb.", "meaning": "Tôi không thể quyết định phải + V."},
        {"phrase": "I'm not really into A.", "meaning": "Tôi không thực sự thích A."},
    ],
    "new-apartment-in-tokyo": [
        {"phrase": "I'm torn between A and B.", "meaning": "Tôi phân vân giữa A và B."},
        {"phrase": "A makes more sense to me.", "meaning": "A hợp lý hơn với tôi."},
        {"phrase": "weigh up", "meaning": "cân nhắc (ưu/nhược)"},
    ],
    "moving-day": [
        {"phrase": "I'm excited about...", "meaning": "Tôi hào hứng về..."},
        {"phrase": "I'm nervous about...", "meaning": "Tôi lo lắng về..."},
        {"phrase": "settle in", "meaning": "ổn định, làm quen nơi mới"},
    ],
    "walk-me-through-the-route": [
        {"phrase": "Walk me through...", "meaning": "Giải thích từng bước cho tôi..."},
        {"phrase": "Could you show me...?", "meaning": "Bạn có thể chỉ tôi...?"},
    ],
    "can-you-walk-me-through-the-contract": [
        {"phrase": "Walk me through the contract.", "meaning": "Giải thích hợp đồng cho tôi."},
        {"phrase": "What does this clause mean?", "meaning": "Điều khoản này nghĩa là gì?"},
    ],
    "first-code-review-in-english": [
        {"phrase": "I'm not sure I understand this part.", "meaning": "Tôi không chắc mình hiểu phần này."},
        {"phrase": "Can you walk me through this logic?", "meaning": "Bạn giải thích logic này cho tôi được không?"},
        {"phrase": "I think we should add a test before merging.", "meaning": "Tôi nghĩ nên thêm test trước khi merge."},
    ],
    "the-performance-problem": [
        {"phrase": "The issue is that...", "meaning": "Vấn đề là..."},
        {"phrase": "It seems like...", "meaning": "Có vẻ như..."},
        {"phrase": "This might be caused by...", "meaning": "Có thể do..."},
        {"phrase": "go through the logs", "meaning": "xem/xử lý log"},
    ],
    "i-have-a-different-take": [
        {"phrase": "I see your point, but...", "meaning": "Tôi hiểu ý bạn, nhưng..."},
        {"phrase": "I have a different take.", "meaning": "Tôi có góc nhìn khác."},
        {"phrase": "rely on", "meaning": "phụ thuộc vào"},
        {"phrase": "think through the risks", "meaning": "suy nghĩ kỹ về rủi ro"},
    ],
    "walk-me-through-the-architecture": [
        {"phrase": "walk me through", "meaning": "giải thích từng bước"},
        {"phrase": "act as a cache layer", "meaning": "đóng vai trò lớp cache"},
        {"phrase": "Let me make sure I got this right.", "meaning": "Để tôi xác nhận lại xem tôi hiểu đúng chưa."},
    ],
    "demo-day-pressure": [
        {"phrase": "I'm nervous about the demo.", "meaning": "Tôi lo về buổi demo."},
        {"phrase": "run through the main flow", "meaning": "đi lại flow chính"},
        {"phrase": "work through it", "meaning": "cùng giải quyết / vượt qua"},
        {"phrase": "I'm ready to present.", "meaning": "Tôi sẵn sàng trình bày."},
    ],
    "the-junior-asks-for-help": [
        {"phrase": "Could you help me with this setup?", "meaning": "Bạn giúp tôi setup cái này được không?"},
        {"phrase": "I can walk you through it.", "meaning": "Tôi có thể hướng dẫn bạn từng bước."},
        {"phrase": "figure it out step by step", "meaning": "giải quyết từng bước một"},
    ],
    "incident-recap-meeting": [
        {"phrase": "Let me walk you through what happened.", "meaning": "Để tôi trình bày diễn biến sự cố."},
        {"phrase": "The issue was that...", "meaning": "Vấn đề là..."},
        {"phrase": "follow through on the fix", "meaning": "theo sát đến khi fix xong"},
    ],
    "speaking-up": [
        {"phrase": "I'm debating whether to A or B.", "meaning": "Tôi đang cân nhắc giữa A và B."},
        {"phrase": "I have a different take.", "meaning": "Tôi có góc nhìn khác."},
        {"phrase": "I'd opt for...", "meaning": "Tôi sẽ chọn..."},
        {"phrase": "It comes down to...", "meaning": "Vấn đề cốt lõi là..."},
    ],
    "nam-becomes-the-bridge": [
        {"phrase": "be the bridge between A and B", "meaning": "là cầu nối giữa A và B"},
        {"phrase": "walk people through...", "meaning": "hướng dẫn mọi người từng bước"},
        {"phrase": "disagree respectfully", "meaning": "phản biện một cách tôn trọng"},
        {"phrase": "look forward to + V-ing", "meaning": "mong chờ / hướng tới việc..."},
    ],
    # System Design Arc 51–60
    "the-system-design-question": [
        {"phrase": "I'm wondering if...", "meaning": "Tôi đang tự hỏi liệu..."},
        {"phrase": "Could we start by...", "meaning": "Chúng ta có thể bắt đầu bằng...?"},
        {"phrase": "walk me through", "meaning": "giải thích từng bước cho tôi"},
    ],
    "monolith-or-microservices": [
        {"phrase": "I'm torn between A and B.", "meaning": "Tôi phân vân giữa A và B."},
        {"phrase": "I'm leaning toward A because...", "meaning": "Tôi đang nghiêng về A vì..."},
        {"phrase": "weigh up", "meaning": "cân nhắc (ưu/nhược)"},
    ],
    "cache-or-database-first": [
        {"phrase": "The issue is that...", "meaning": "Vấn đề là..."},
        {"phrase": "It seems like...", "meaning": "Có vẻ như..."},
        {"phrase": "rely on", "meaning": "phụ thuộc vào / dựa vào"},
    ],
    "queue-saves-the-day": [
        {"phrase": "This might be caused by...", "meaning": "Có thể do..."},
        {"phrase": "I think we should...", "meaning": "Tôi nghĩ chúng ta nên..."},
        {"phrase": "follow through", "meaning": "theo sát đến khi hoàn thành"},
    ],
    "api-gateway-at-night": [
        {"phrase": "walk me through", "meaning": "giải thích từng bước cho tôi"},
        {"phrase": "act as", "meaning": "đóng vai trò / hoạt động như"},
        {"phrase": "make sure", "meaning": "đảm bảo / chắc chắn rằng"},
    ],
    "scale-under-pressure": [
        {"phrase": "It comes down to...", "meaning": "Vấn đề cốt lõi là..."},
        {"phrase": "We need to weigh up...", "meaning": "Chúng ta cần cân nhắc..."},
        {"phrase": "I'd opt for...", "meaning": "Tôi sẽ chọn..."},
    ],
    "the-cost-of-overengineering": [
        {"phrase": "I have a different take.", "meaning": "Tôi có góc nhìn khác."},
        {"phrase": "I see your point, but...", "meaning": "Tôi hiểu ý bạn, nhưng..."},
        {"phrase": "rule out", "meaning": "loại trừ (một phương án)"},
    ],
    "explain-it-to-product": [
        {"phrase": "Let me walk you through...", "meaning": "Để tôi giải thích từng bước..."},
        {"phrase": "In simple terms...", "meaning": "Nói đơn giản thì..."},
        {"phrase": "The main idea is...", "meaning": "Ý chính là..."},
    ],
    "design-review-showdown": [
        {"phrase": "I'm debating whether...", "meaning": "Tôi đang cân nhắc liệu có nên..."},
        {"phrase": "That makes sense.", "meaning": "Điều đó hợp lý."},
        {"phrase": "stick with", "meaning": "giữ nguyên / theo phương án"},
    ],
    "thinking-bigger-finale": [
        {"phrase": "look forward to", "meaning": "mong chờ / hướng tới"},
        {"phrase": "be the bridge", "meaning": "là cầu nối (giữa các team)"},
        {"phrase": "explain problems clearly", "meaning": "giải thích vấn đề một cách rõ ràng"},
    ],
    # Email & Async Arc 61–65
    "just-following-up-on-the-pr": [
        {"phrase": "Just following up on...", "meaning": "Nhắc lại / theo dõi về..."},
        {"phrase": "I wanted to check in on...", "meaning": "Tôi muốn hỏi thăm / cập nhật về..."},
        {"phrase": "get back to", "meaning": "phản hồi lại / trả lời sau"},
    ],
    "loop-me-in-on-the-decision": [
        {"phrase": "Could you loop me in on...?", "meaning": "Bạn có thể cập nhật tôi về...?"},
        {"phrase": "keep me posted on...", "meaning": "nhắc tôi / cập nhật tôi về..."},
        {"phrase": "reach out to", "meaning": "liên hệ với ai đó"},
    ],
    "ill-get-back-to-you-by-eod": [
        {"phrase": "I'll get back to you by...", "meaning": "Tôi sẽ phản hồi bạn trước..."},
        {"phrase": "Let me look into this.", "meaning": "Để tôi tìm hiểu thêm."},
        {"phrase": "follow up on", "meaning": "theo dõi / nhắc lại về"},
    ],
    "async-standup-in-english": [
        {"phrase": "Here's what I worked on...", "meaning": "Đây là những gì tôi đã làm..."},
        {"phrase": "I'm blocked on...", "meaning": "Tôi đang bị kẹt ở / không tiến được vì..."},
        {"phrase": "I'll follow up with...", "meaning": "Tôi sẽ liên hệ với..."},
    ],
    "email-async-finale": [
        {"phrase": "follow up on", "meaning": "theo dõi / nhắc lại về"},
        {"phrase": "loop in", "meaning": "thêm ai vào cuộc trò chuyện / cập nhật"},
        {"phrase": "get back to", "meaning": "phản hồi lại"},
        {"phrase": "reach out to", "meaning": "chủ động liên hệ"},
    ],
    # Japan Culture Arc 66–72
    "walk-me-through-shrine-etiquette": [
        {"phrase": "Can you walk me through how to pray at a shrine?", "meaning": "Bạn hướng dẫn tôi cách cầu nguyện ở đền được không?"},
        {"phrase": "Let me make sure I got this right.", "meaning": "Để tôi xác nhận lại xem tôi hiểu đúng chưa."},
        {"phrase": "I'm not sure I understand this part.", "meaning": "Tôi không chắc mình hiểu phần này."},
    ],
    "the-onsen-question": [
        {"phrase": "I'm not sure if I should...", "meaning": "Tôi không chắc liệu mình có nên..."},
        {"phrase": "What do you mean by...?", "meaning": "... nghĩa là gì? / Ý bạn là gì khi nói...?"},
        {"phrase": "Could you explain this part again?", "meaning": "Bạn giải thích lại phần này được không?"},
    ],
    "izakaya-after-work": [
        {"phrase": "I'm excited about trying real izakaya food.", "meaning": "Tôi hào hứng được thử đồ ăn izakaya thật."},
        {"phrase": "That sounds amazing.", "meaning": "Nghe hay / tuyệt quá."},
        {"phrase": "I'm not really into raw fish, but...", "meaning": "Tôi không thích lắm món sống, nhưng..."},
    ],
    "cherry-blossom-dilemma": [
        {"phrase": "I'm torn between A and B.", "meaning": "Tôi phân vân giữa A và B."},
        {"phrase": "I'm leaning toward A because...", "meaning": "Tôi đang nghiêng về A vì..."},
        {"phrase": "I think I'll go with A.", "meaning": "Tôi nghĩ mình sẽ chọn A."},
    ],
    "what-is-omotenashi": [
        {"phrase": "I'm surprised that...", "meaning": "Tôi ngạc nhiên vì..."},
        {"phrase": "That was worth it.", "meaning": "Đáng giá / xứng đáng."},
        {"phrase": "I'm glad that we learned the custom first.", "meaning": "May mà chúng ta học phong tục trước."},
    ],
    "summer-festival-night": [
        {"phrase": "I'm looking for...", "meaning": "Tôi đang tìm..."},
        {"phrase": "How long does it take to get to...?", "meaning": "Mất bao lâu để đến...?"},
        {"phrase": "That sounds amazing.", "meaning": "Nghe hay / tuyệt quá."},
    ],
    "japan-culture-finale": [
        {"phrase": "It was worth it.", "meaning": "Đáng giá / xứng đáng."},
        {"phrase": "I'm proud of myself.", "meaning": "Tôi tự hào về bản thân."},
        {"phrase": "look forward to", "meaning": "mong chờ / hướng tới"},
    ],
    # Anime & Manga Arc 73–78
    "akihabara-or-nakano-broadway": [
        {"phrase": "I'm torn between A and B.", "meaning": "Tôi phân vân giữa A và B."},
        {"phrase": "I'm more interested in A.", "meaning": "Tôi quan tâm đến A hơn."},
        {"phrase": "A makes more sense to me.", "meaning": "A hợp lý hơn với tôi."},
    ],
    "my-first-manga-cafe": [
        {"phrase": "Can you walk me through how a manga cafe works?", "meaning": "Bạn giải thích manga cafe hoạt động thế nào được không?"},
        {"phrase": "Could you show me how to use the locker?", "meaning": "Bạn chỉ tôi cách dùng tủ khóa được không?"},
        {"phrase": "I'm not sure I understand the time system.", "meaning": "Tôi không chắc mình hiểu hệ thống tính giờ."},
    ],
    "anime-pilgrimage-day": [
        {"phrase": "I'm really into this anime.", "meaning": "Tôi rất mê anime này."},
        {"phrase": "I'm excited about finding the café from the scene.", "meaning": "Tôi hào hứng tìm quán cà phê trong phim."},
        {"phrase": "That sounds amazing.", "meaning": "Nghe hay / tuyệt quá."},
    ],
    "figure-store-dilemma": [
        {"phrase": "I can't decide what to buy.", "meaning": "Tôi không thể quyết định mua gì."},
        {"phrase": "I'd rather A than B.", "meaning": "Tôi thích A hơn B."},
        {"phrase": "I think I'll go with A.", "meaning": "Tôi nghĩ mình sẽ chọn A."},
    ],
    "anime-talk-at-team-lunch": [
        {"phrase": "I'm not really into A, but I love B.", "meaning": "Tôi không thích lắm A, nhưng rất thích B."},
        {"phrase": "That sounds amazing.", "meaning": "Nghe hay / tuyệt quá."},
        {"phrase": "We should hang out at... sometime.", "meaning": "Lần nào đi ... chơi cùng nhé."},
    ],
    "anime-manga-finale": [
        {"phrase": "It was worth it.", "meaning": "Đáng giá / xứng đáng."},
        {"phrase": "I'm glad that we shared our favorites.", "meaning": "May mà chúng ta chia sẻ anime yêu thích."},
        {"phrase": "look forward to", "meaning": "mong chờ / hướng tới"},
    ],
    # Interview & Career Arc 79–84
    "the-first-phone-screen": [
        {"phrase": "I'm looking for a role where...", "meaning": "Tôi đang tìm một vị trí mà..."},
        {"phrase": "I see myself growing in...", "meaning": "Tôi thấy mình phát triển trong..."},
        {"phrase": "What attracted me to this company is...", "meaning": "Điều thu hút tôi ở công ty này là..."},
    ],
    "tell-me-about-a-time-when": [
        {"phrase": "Tell me about a time when...", "meaning": "Hãy kể về một lần khi..."},
        {"phrase": "One challenge I faced was...", "meaning": "Một thử thách tôi gặp là..."},
        {"phrase": "What I learned from that was...", "meaning": "Bài học tôi rút ra là..."},
    ],
    "why-do-you-want-this-role": [
        {"phrase": "Why I'm interested in this role is...", "meaning": "Lý do tôi quan tâm vị trí này là..."},
        {"phrase": "I'm looking for a role where...", "meaning": "Tôi đang tìm một vị trí mà..."},
        {"phrase": "work closely with", "meaning": "làm việc sát sao với"},
    ],
    "the-salary-question": [
        {"phrase": "I'd need at least...", "meaning": "Tôi cần ít nhất..."},
        {"phrase": "Would it be possible to...?", "meaning": "Liệu có thể... không?"},
        {"phrase": "I'm looking for a range of...", "meaning": "Tôi đang tìm mức khoảng..."},
    ],
    "questions-for-the-interviewer": [
        {"phrase": "Do you have any questions for us?", "meaning": "Bạn có câu hỏi nào cho chúng tôi không?"},
        {"phrase": "What does success look like in this role?", "meaning": "Thành công ở vị trí này trông như thế nào?"},
        {"phrase": "How does the team collaborate?", "meaning": "Team cộng tác như thế nào?"},
    ],
    "interview-career-finale": [
        {"phrase": "Tell me about a time when...", "meaning": "Hãy kể về một lần khi..."},
        {"phrase": "What I learned from that was...", "meaning": "Bài học tôi rút ra là..."},
        {"phrase": "I'm looking for a role where...", "meaning": "Tôi đang tìm một vị trí mà..."},
        {"phrase": "look forward to", "meaning": "mong chờ / hướng tới"},
    ],
    # Negotiation & Boundaries Arc 85–89
    "the-tight-deadline": [
        {"phrase": "I'm concerned that the timeline is too tight.", "meaning": "Tôi lo deadline quá gấp."},
        {"phrase": "Could we push the deadline back by...?", "meaning": "Chúng ta có thể lùi deadline thêm... không?"},
        {"phrase": "weigh up", "meaning": "cân nhắc (ưu/nhược)"},
    ],
    "would-it-be-possible-to": [
        {"phrase": "Would it be possible to...?", "meaning": "Liệu có thể... không?"},
        {"phrase": "I'd be more comfortable if we...", "meaning": "Tôi sẽ thoải mái hơn nếu chúng ta..."},
        {"phrase": "What would it take to...?", "meaning": "Cần gì để...?"},
    ],
    "thats-outside-the-scope": [
        {"phrase": "That's outside the original scope.", "meaning": "Điều đó ngoài phạm vi ban đầu."},
        {"phrase": "I'd need at least...", "meaning": "Tôi cần ít nhất..."},
        {"phrase": "scope creep", "meaning": "phạm vi công việc bị phình to dần"},
    ],
    "push-back-on-scope-creep": [
        {"phrase": "Let me push back on that.", "meaning": "Để tôi phản hồi / không đồng ý với điều đó."},
        {"phrase": "I'm happy to help, but we'll need to...", "meaning": "Tôi sẵn sàng giúp, nhưng chúng ta cần..."},
        {"phrase": "push back", "meaning": "phản hồi / từ chối nhẹ nhàng"},
    ],
    "negotiation-boundaries-finale": [
        {"phrase": "Would it be possible to...?", "meaning": "Liệu có thể... không?"},
        {"phrase": "That's outside the original scope.", "meaning": "Điều đó ngoài phạm vi ban đầu."},
        {"phrase": "set a boundary", "meaning": "đặt ranh giới rõ ràng"},
        {"phrase": "compromise on", "meaning": "thỏa hiệp về"},
    ],
    # Feedback & 1-on-1 Arc 90–94
    "preparing-for-the-1-on-1": [
        {"phrase": "What would help you most right now?", "meaning": "Điều gì giúp bạn nhất lúc này?"},
        {"phrase": "Let's set a goal for next week.", "meaning": "Hãy đặt mục tiêu cho tuần tới."},
        {"phrase": "check in with", "meaning": "hỏi thăm / cập nhật với ai đó"},
    ],
    "one-thing-that-went-well-was": [
        {"phrase": "One thing that went well was...", "meaning": "Một điều làm tốt là..."},
        {"phrase": "I appreciate how you handled...", "meaning": "Tôi đánh giá cao cách bạn xử lý..."},
        {"phrase": "One area to improve would be...", "meaning": "Một điểm cần cải thiện là..."},
    ],
    "id-suggest-trying": [
        {"phrase": "I'd suggest trying...", "meaning": "Tôi gợi ý thử..."},
        {"phrase": "Have you considered...?", "meaning": "Bạn đã cân nhắc... chưa?"},
        {"phrase": "step up", "meaning": "nâng cao / làm tốt hơn"},
    ],
    "how-can-i-support-you": [
        {"phrase": "How can I support you?", "meaning": "Tôi có thể hỗ trợ bạn thế nào?"},
        {"phrase": "What would help you most right now?", "meaning": "Điều gì giúp bạn nhất lúc này?"},
        {"phrase": "grow into", "meaning": "trưởng thành / phát triển thành"},
    ],
    "feedback-1-on-1-finale": [
        {"phrase": "One thing that went well was...", "meaning": "Một điều làm tốt là..."},
        {"phrase": "I'd suggest trying...", "meaning": "Tôi gợi ý thử..."},
        {"phrase": "How can I support you?", "meaning": "Tôi có thể hỗ trợ bạn thế nào?"},
        {"phrase": "follow up on", "meaning": "theo dõi / nhắc lại về"},
    ],
    # Presentation & Pitch Arc 95–99
    "structuring-the-demo": [
        {"phrase": "I'll keep this brief.", "meaning": "Tôi sẽ trình bày ngắn gọn."},
        {"phrase": "The main problem we're solving is...", "meaning": "Vấn đề chính chúng ta giải quyết là..."},
        {"phrase": "To summarize...", "meaning": "Tóm lại..."},
    ],
    "walk-through-the-demo": [
        {"phrase": "Let me walk you through...", "meaning": "Để tôi hướng dẫn/giải thích từng bước..."},
        {"phrase": "As you can see on this slide...", "meaning": "Như bạn thấy trên slide này..."},
        {"phrase": "run through", "meaning": "đi lại / trình bày nhanh từng phần"},
    ],
    "the-key-takeaway-is": [
        {"phrase": "The key takeaway is...", "meaning": "Điểm chính cần nhớ là..."},
        {"phrase": "Here's what changed since last time.", "meaning": "Đây là những gì thay đổi từ lần trước."},
        {"phrase": "break down", "meaning": "phân tích / chia nhỏ"},
    ],
    "handling-tough-questions": [
        {"phrase": "Any questions on this part?", "meaning": "Có câu hỏi nào về phần này không?"},
        {"phrase": "That's a great question — let me...", "meaning": "Câu hỏi hay — để tôi..."},
        {"phrase": "circle back", "meaning": "quay lại (chủ đề) sau"},
    ],
    "presentation-pitch-finale": [
        {"phrase": "Let me walk you through...", "meaning": "Để tôi hướng dẫn/giải thích từng bước..."},
        {"phrase": "The key takeaway is...", "meaning": "Điểm chính cần nhớ là..."},
        {"phrase": "Any questions on this part?", "meaning": "Có câu hỏi nào về phần này không?"},
        {"phrase": "look forward to", "meaning": "mong chờ / hướng tới"},
    ],
    # Incident & Postmortem Arc 100–104
    "the-war-room": [
        {"phrase": "What we know so far is...", "meaning": "Những gì chúng ta biết đến giờ là..."},
        {"phrase": "Let's focus on the facts, not blame.", "meaning": "Tập trung vào sự thật, không đổ lỗi."},
        {"phrase": "dig into", "meaning": "đi sâu vào / điều tra kỹ"},
    ],
    "what-we-know-so-far-is": [
        {"phrase": "What we know so far is...", "meaning": "Những gì chúng ta biết đến giờ là..."},
        {"phrase": "The impact was that...", "meaning": "Tác động là..."},
        {"phrase": "The timeline of events was...", "meaning": "Diễn biến theo thời gian là..."},
    ],
    "root-cause-analysis": [
        {"phrase": "Root cause appears to be...", "meaning": "Nguyên nhân gốc có vẻ là..."},
        {"phrase": "It seems like...", "meaning": "Có vẻ như..."},
        {"phrase": "This might be caused by...", "meaning": "Có thể do..."},
    ],
    "action-items-going-forward": [
        {"phrase": "Action items going forward...", "meaning": "Các việc cần làm tiếp theo..."},
        {"phrase": "We mitigated the issue by...", "meaning": "Chúng ta đã giảm thiểu sự cố bằng cách..."},
        {"phrase": "To prevent this from happening again...", "meaning": "Để tránh tái diễn..."},
    ],
    "postmortem-finale": [
        {"phrase": "What we know so far is...", "meaning": "Những gì chúng ta biết đến giờ là..."},
        {"phrase": "Root cause appears to be...", "meaning": "Nguyên nhân gốc có vẻ là..."},
        {"phrase": "Action items going forward...", "meaning": "Các việc cần làm tiếp theo..."},
        {"phrase": "follow up on", "meaning": "theo dõi / nhắc lại về"},
    ],
    # Silicon Valley Get Arc 105–110
    "can-you-loop-me-in": [
        {"phrase": "get looped in", "meaning": "được thêm vào cuộc trò chuyện / được cập nhật"},
        {"phrase": "get pinged", "meaning": "bị nhắn / bị tag trên Slack"},
        {"phrase": "get up to speed", "meaning": "nắm bắt nhanh tình hình"},
    ],
    "we-need-buy-in": [
        {"phrase": "get buy-in", "meaning": "được mọi người đồng thuận / chấp thuận"},
        {"phrase": "get aligned", "meaning": "thống nhất / cùng hướng"},
        {"phrase": "get the ball rolling", "meaning": "bắt đầu / khởi động việc"},
    ],
    "blocked-on-dependencies": [
        {"phrase": "get blocked", "meaning": "bị kẹt / không tiến được vì phụ thuộc"},
        {"phrase": "get unblocked", "meaning": "được gỡ kẹt / tiếp tục được"},
        {"phrase": "get through", "meaning": "vượt qua / hoàn thành (một giai đoạn)"},
    ],
    "ship-it-friday": [
        {"phrase": "get shipped", "meaning": "được deploy / đưa lên production"},
        {"phrase": "get sign-off", "meaning": "được phê duyệt chính thức"},
        {"phrase": "get ready", "meaning": "chuẩn bị sẵn sàng"},
    ],
    "pulled-into-the-war-room": [
        {"phrase": "get pulled into", "meaning": "bị kéo vào (cuộc họp / sự cố)"},
        {"phrase": "get stuck", "meaning": "bị kẹt / bí / không tiến triển"},
        {"phrase": "get back to", "meaning": "phản hồi lại / trả lời sau"},
    ],
    "the-acquisition-news": [
        {"phrase": "get face time", "meaning": "có thời gian trực tiếp với sếp / leadership"},
        {"phrase": "get promoted", "meaning": "được thăng chức"},
        {"phrase": "get acquired", "meaning": "bị mua lại (công ty)"},
    ],
    # Switzerland Travel Arc 111–115
    "landing-in-zurich": [
        {"phrase": "get to", "meaning": "đến (một nơi)"},
        {"phrase": "get checked in", "meaning": "làm thủ tục nhận phòng"},
        {"phrase": "get your bearings", "meaning": "định hướng / nắm vị trí xung quanh"},
    ],
    "the-glacier-express": [
        {"phrase": "get a ticket", "meaning": "mua vé"},
        {"phrase": "get on", "meaning": "lên (tàu / xe)"},
        {"phrase": "get off", "meaning": "xuống (tàu / xe)"},
    ],
    "view-from-the-top": [
        {"phrase": "get a view of", "meaning": "nhìn thấy / ngắm cảnh"},
        {"phrase": "get altitude sickness", "meaning": "bị say độ cao"},
        {"phrase": "get change", "meaning": "đổi tiền lẻ / nhận tiền thối"},
    ],
    "snowed-in-at-zermatt": [
        {"phrase": "get snowed in", "meaning": "bị kẹt vì tuyết / không ra được"},
        {"phrase": "get held up", "meaning": "bị trì hoãn / bị chậm lại"},
        {"phrase": "get by", "meaning": "xử lý tạm / vượt qua (với ít tài nguyên)"},
    ],
    "lost-on-the-alpine-trail": [
        {"phrase": "get around", "meaning": "đi lại / di chuyển quanh khu vực"},
        {"phrase": "get lost", "meaning": "bị lạc"},
        {"phrase": "get swept up in", "meaning": "bị cuốn vào (không khí / sự kiện)"},
    ],
    # Everyday Get Arc 116–118
    "first-english-meetup": [
        {"phrase": "get used to", "meaning": "quen dần với"},
        {"phrase": "get ready", "meaning": "chuẩn bị sẵn sàng"},
        {"phrase": "get through", "meaning": "vượt qua / hoàn thành (một buổi / bài)"},
    ],
    "when-you-finally-get-it": [
        {"phrase": "get it", "meaning": "hiểu rồi / nắm được"},
        {"phrase": "get back to", "meaning": "quay lại (việc) / phản hồi sau"},
        {"phrase": "get by", "meaning": "tạm đủ dùng / xoay xở được"},
    ],
    "everyday-get-finale": [
        {"phrase": "get onboarded", "meaning": "được hướng dẫn nhập môn / làm quen hệ thống"},
        {"phrase": "get sign-off", "meaning": "được phê duyệt chính thức"},
        {"phrase": "get a ride", "meaning": "được chở / nhờ xe"},
    ],
}


def image_path(arc: str, num: int, slug: str) -> str:
    tap = f"tập-{num:02d}"
    return f"images/comics/{arc}/{tap}/{arc}-tap{num:02d}-{slug}.png"


def build_comics() -> dict:
    series_out = []
    total = 0
    for s in SERIES:
        eps = []
        for num, slug, title in s["episodes"]:
            ep = {
                "num": num,
                "title": title,
                "slug": slug,
                "image": image_path(s["arc"], num, slug),
                "englishFocus": FOCUS.get(slug, []),
            }
            eps.append(ep)
        count = len(eps)
        total += count
        series_out.append({
            "id": s["id"],
            "title": s["title"],
            "desc": s["desc"],
            "color": s["color"],
            "icon": s["icon"],
            "tag": s["tag"],
            "count": count,
            "cover": eps[0]["image"],
            "episodes": eps,
        })
    return {"version": 1, "count": total, "series": series_out}


def build_roadmap() -> dict:
    return {
        "meta": {
            "title": "Lộ trình học tiếng Anh",
            "subtitle": "18 arc · 136 tập · Từ debug code đến phrasal verbs get",
        },
        "methodology": [
            {"step": 1, "icon": "📖", "title": "Đọc truyện", "desc": "Mỗi tập là một tình huống thật — đọc hội thoại và chú ý phần ENGLISH FOCUS trên ảnh."},
            {"step": 2, "icon": "✅", "title": "Đánh dấu đã đọc", "desc": "Hoàn thành tập → tiến độ tự cập nhật trên lộ trình."},
            {"step": 3, "icon": "🗣️", "title": "Luyện nói", "desc": "Đọc to các cụm từ trong panel ENGLISH FOCUS — áp dụng vào công việc và đời sống."},
        ],
        "paths": [
            {
                "id": "full-journey",
                "title": "Toàn bộ hành trình",
                "subtitle": "Work → Travel → Life → Growth",
                "icon": "🗼",
                "color": "#3B82F6",
                "duration": "6–10 tuần",
                "desc": "Bắt đầu từ debug production, du lịch, sống ở Tokyo, rồi Nam trưởng thành thành mentor.",
                "phases": [
                    {
                        "title": "Giai đoạn 1 — Công việc (Debug)",
                        "desc": "Tiếng Anh trong team dev: patch, deploy, QA, cache",
                        "steps": [
                            {"seriesId": "bug-arc-1", "tip": "Arc 1: Quyết định kỹ thuật dưới áp lực release"},
                            {"seriesId": "bug-arc-2", "tip": "Arc 2: Sửa payment bug trước demo"},
                            {"seriesId": "bug-arc-3", "tip": "Arc 3: Investor demo — quyết định khó nhất"},
                        ],
                    },
                    {
                        "title": "Giai đoạn 2 — Du lịch",
                        "desc": "Reward trip sau release thành công",
                        "steps": [
                            {"seriesId": "traveling", "tip": "Tokyo, Osaka, Kyoto, Fuji — tiếng Anh trên đường"},
                        ],
                    },
                    {
                        "title": "Giai đoạn 3 — Cuộc sống",
                        "desc": "Nam chuyển sang Tokyo — thuê nhà, ngân hàng, làm remote",
                        "steps": [
                            {"seriesId": "living", "tip": "English for Real Life — sống và làm việc ở Nhật"},
                        ],
                    },
                    {
                        "title": "Giai đoạn 4 — Career Growth",
                        "desc": "Code review, architecture, demo, mentor — Nam speaks up",
                        "steps": [
                            {"seriesId": "career-growth", "tip": "Nam dùng tiếng Anh để lead, mentor và tạo impact"},
                        ],
                    },
                    {
                        "title": "Giai đoạn 5 — System Design",
                        "desc": "Scale, cache, queue, trade-offs — Nam nghĩ theo hệ thống",
                        "steps": [
                            {"seriesId": "system-design", "tip": "Architecture review, monolith vs microservices, explain to PM"},
                        ],
                    },
                    {
                        "title": "Giai đoạn 6 — Email & Async",
                        "desc": "Follow-up, loop in, async standup — viết như pro",
                        "steps": [
                            {"seriesId": "email-async", "tip": "Slack & email chuyên nghiệp cho remote team"},
                        ],
                    },
                    {
                        "title": "Giai đoạn 7 — Văn hóa Nhật",
                        "desc": "Đền chùa, onsen, izakaya, hanami, matsuri — khám phá văn hóa sau giờ làm",
                        "steps": [
                            {"seriesId": "japan-culture", "tip": "Shrine etiquette, omotenashi, festival — English for culture trips"},
                        ],
                    },
                    {
                        "title": "Giai đoạn 8 — Anime & Manga",
                        "desc": "Akihabara, manga cafe, anime pilgrimage — tiếng Anh trong thế giới otaku",
                        "steps": [
                            {"seriesId": "anime-manga", "tip": "Figure shop, manga cafe, team lunch anime talk"},
                        ],
                    },
                    {
                        "title": "Giai đoạn 9 — Career Advanced",
                        "desc": "Phỏng vấn, thương lượng, feedback, pitch, postmortem — tiếng Anh cấp senior",
                        "steps": [
                            {"seriesId": "interview-career", "tip": "Behavioral interview, salary, career goals"},
                            {"seriesId": "negotiation-boundaries", "tip": "Deadline, scope creep, push back professionally"},
                            {"seriesId": "giving-feedback", "tip": "1-on-1, constructive feedback, mentoring"},
                            {"seriesId": "presentation-pitch", "tip": "Demo structure, key takeaway, tough Q&A"},
                            {"seriesId": "incident-postmortem", "tip": "War room, root cause, blameless postmortem"},
                        ],
                    },
                    {
                        "title": "Giai đoạn 10 — Get Phrasal Verbs",
                        "desc": "Startup Bay Area, Thụy Sĩ, học tiếng Anh hàng ngày — học get + prep/adj/V3 qua truyện",
                        "steps": [
                            {"seriesId": "silicon-valley-get", "tip": "Loop in, buy-in, ship day, war room, acquisition"},
                            {"seriesId": "switzerland-travel", "tip": "Trains, peaks, snow — get around Switzerland"},
                            {"seriesId": "english-everyday-get", "tip": "Meetup, homework — get it, get by, get used to"},
                        ],
                    },
                ],
            },
            {
                "id": "work-only",
                "title": "Chỉ công việc",
                "subtitle": "3 arc debug — dành cho dev cần tiếng Anh tech",
                "icon": "💻",
                "color": "#EF4444",
                "duration": "2–3 tuần",
                "desc": "Tập trung patch, deploy, API, QA, cache — bỏ qua travel & life.",
                "phases": [
                    {
                        "title": "Debug Chronicles",
                        "desc": "3 arc liên tiếp",
                        "steps": [
                            {"seriesId": "bug-arc-1"},
                            {"seriesId": "bug-arc-2"},
                            {"seriesId": "bug-arc-3"},
                        ],
                    },
                ],
            },
            {
                "id": "career-growth",
                "title": "Career Growth",
                "subtitle": "Tập 41–50 — code review, demo, mentor, lead",
                "icon": "🚀",
                "color": "#6366F1",
                "duration": "2 tuần",
                "desc": "Tiếp nối Living Arc — Nam dùng tiếng Anh để nói lên ý kiến, mentor junior, và trở thành cầu nối team.",
                "phases": [
                    {
                        "title": "Nam Speaks Up at Work",
                        "desc": "10 tập từ code review đến trở thành bridge",
                        "steps": [{"seriesId": "career-growth"}],
                    },
                ],
            },
            {
                "id": "system-design",
                "title": "System Design",
                "subtitle": "Tập 51–60 — architecture, scale, trade-offs",
                "icon": "🏗️",
                "color": "#8B5CF6",
                "duration": "2 tuần",
                "desc": "Nam học nói tiếng Anh khi thiết kế hệ thống: cache, queue, gateway, và giải thích cho PM.",
                "phases": [
                    {
                        "title": "Thinking Bigger",
                        "desc": "10 tập từ system design question đến design review",
                        "steps": [{"seriesId": "system-design"}],
                    },
                ],
            },
            {
                "id": "email-async",
                "title": "Email & Async",
                "subtitle": "Tập 61–65 — follow-up, loop in, standup",
                "icon": "✉️",
                "color": "#3B82F6",
                "duration": "1 tuần",
                "desc": "Pack 5 — viết email và Slack async chuyên nghiệp.",
                "phases": [
                    {
                        "title": "Write Like a Pro",
                        "desc": "5 tập email & async communication",
                        "steps": [{"seriesId": "email-async"}],
                    },
                ],
            },
            {
                "id": "travel-life",
                "title": "Du lịch & Cuộc sống",
                "subtitle": "Bỏ qua phần debug — vào thẳng travel + living + culture",
                "icon": "✈️",
                "color": "#06B6D4",
                "duration": "3–5 tuần",
                "desc": "Phù hợp nếu bạn đã quen tiếng Anh công việc, muốn học giao tiếp thực tế và khám phá Nhật.",
                "phases": [
                    {
                        "title": "On the Road",
                        "desc": "Du lịch Nhật với team",
                        "steps": [{"seriesId": "traveling"}],
                    },
                    {
                        "title": "Real Life",
                        "desc": "Sống ở Tokyo",
                        "steps": [{"seriesId": "living"}],
                    },
                    {
                        "title": "Culture & Anime",
                        "desc": "Văn hóa Nhật + thế giới anime manga",
                        "steps": [
                            {"seriesId": "japan-culture"},
                            {"seriesId": "anime-manga"},
                        ],
                    },
                ],
            },
            {
                "id": "japan-culture",
                "title": "Văn hóa Nhật Bản",
                "subtitle": "Tập 66–72 — đền chùa, onsen, hanami, matsuri",
                "icon": "⛩️",
                "color": "#DC2626",
                "duration": "1–2 tuần",
                "desc": "Khám phá văn hóa Nhật sau giờ làm hoặc khi du lịch — tiếng Anh cho shrine, onsen, izakaya, festival.",
                "phases": [
                    {
                        "title": "Explore Beyond the Guidebook",
                        "desc": "7 tập từ shrine etiquette đến matsuri night",
                        "steps": [{"seriesId": "japan-culture"}],
                    },
                ],
            },
            {
                "id": "anime-manga",
                "title": "Anime & Manga",
                "subtitle": "Tập 73–78 — Akihabara, manga cafe, pilgrimage",
                "icon": "🎌",
                "color": "#EC4899",
                "duration": "1 tuần",
                "desc": "Tiếng Anh khi khám phá thế giới anime manga ở Nhật — từ Akihabara đến nói chuyện anime với đồng nghiệp.",
                "phases": [
                    {
                        "title": "Dive Into Otaku Japan",
                        "desc": "6 tập từ Akihabara đến anime talk at lunch",
                        "steps": [{"seriesId": "anime-manga"}],
                    },
                ],
            },
            {
                "id": "career-advanced",
                "title": "Career Advanced",
                "subtitle": "Tập 79–104 — interview, negotiate, feedback, pitch, postmortem",
                "icon": "💼",
                "color": "#F59E0B",
                "duration": "4–5 tuần",
                "desc": "Sau khi học xong 96 tập — mở rộng tiếng Anh phỏng vấn, thương lượng, 1-on-1, thuyết trình và postmortem.",
                "phases": [
                    {
                        "title": "Interview & Career",
                        "desc": "6 tập phỏng vấn và định hướng sự nghiệp",
                        "steps": [{"seriesId": "interview-career"}],
                    },
                    {
                        "title": "Negotiate & Lead",
                        "desc": "Thương lượng, feedback, pitch",
                        "steps": [
                            {"seriesId": "negotiation-boundaries"},
                            {"seriesId": "giving-feedback"},
                            {"seriesId": "presentation-pitch"},
                        ],
                    },
                    {
                        "title": "Incident Communication",
                        "desc": "War room và postmortem blameless",
                        "steps": [{"seriesId": "incident-postmortem"}],
                    },
                ],
            },
            {
                "id": "interview-career",
                "title": "Interview & Career",
                "subtitle": "Tập 79–84 — phone screen, STAR, salary",
                "icon": "💼",
                "color": "#F59E0B",
                "duration": "1 tuần",
                "desc": "Tiếng Anh phỏng vấn: behavioral questions, career goals, salary talk.",
                "phases": [
                    {
                        "title": "Land Your Next Role",
                        "desc": "6 tập từ phone screen đến questions for interviewer",
                        "steps": [{"seriesId": "interview-career"}],
                    },
                ],
            },
            {
                "id": "negotiation-boundaries",
                "title": "Negotiation & Boundaries",
                "subtitle": "Tập 85–89 — deadline, scope, push back",
                "icon": "🤝",
                "color": "#14B8A6",
                "duration": "1 tuần",
                "desc": "Thương lượng deadline, scope creep, và đặt ranh giới chuyên nghiệp.",
                "phases": [
                    {
                        "title": "Push Back Like a Pro",
                        "desc": "5 tập từ tight deadline đến scope boundaries",
                        "steps": [{"seriesId": "negotiation-boundaries"}],
                    },
                ],
            },
            {
                "id": "giving-feedback",
                "title": "Feedback & 1-on-1",
                "subtitle": "Tập 90–94 — constructive feedback, mentoring",
                "icon": "💬",
                "color": "#A855F7",
                "duration": "1 tuần",
                "desc": "Tiếng Anh 1-on-1: feedback tích cực, gợi ý cải thiện, hỗ trợ junior.",
                "phases": [
                    {
                        "title": "Lead Through Conversations",
                        "desc": "5 tập từ chuẩn bị 1-on-1 đến support junior",
                        "steps": [{"seriesId": "giving-feedback"}],
                    },
                ],
            },
            {
                "id": "presentation-pitch",
                "title": "Presentation & Pitch",
                "subtitle": "Tập 95–99 — demo, takeaway, Q&A",
                "icon": "📊",
                "color": "#F97316",
                "duration": "1 tuần",
                "desc": "Thuyết trình demo và pitch cho PM/investor — structure, takeaway, tough questions.",
                "phases": [
                    {
                        "title": "Demo Like a Pro",
                        "desc": "5 tập từ structuring demo đến handling Q&A",
                        "steps": [{"seriesId": "presentation-pitch"}],
                    },
                ],
            },
            {
                "id": "incident-postmortem",
                "title": "Incident & Postmortem",
                "subtitle": "Tập 100–104 — war room, root cause, action items",
                "icon": "🚨",
                "color": "#DC2626",
                "duration": "1 tuần",
                "desc": "Tiếng Anh sự cố production: war room updates, root cause, blameless postmortem.",
                "phases": [
                    {
                        "title": "Blameless Communication",
                        "desc": "5 tập từ war room đến postmortem finale",
                        "steps": [{"seriesId": "incident-postmortem"}],
                    },
                ],
            },
            {
                "id": "silicon-valley-get",
                "title": "Silicon Valley Get",
                "subtitle": "Tập 105–110 — startup, ship day, acquisition",
                "icon": "🌉",
                "color": "#0EA5E9",
                "duration": "1 tuần",
                "desc": "Phrasal verbs get trong công việc startup: loop in, buy-in, blocked, shipped, promoted.",
                "phases": [
                    {
                        "title": "Bay Area Rotation",
                        "desc": "6 tập từ onboarding Slack đến acquisition news",
                        "steps": [{"seriesId": "silicon-valley-get"}],
                    },
                ],
            },
            {
                "id": "switzerland-travel",
                "title": "Switzerland Travel",
                "subtitle": "Tập 111–115 — Zurich, Glacier Express, Zermatt",
                "icon": "🏔️",
                "color": "#059669",
                "duration": "1 tuần",
                "desc": "Get around Switzerland — tickets, trains, altitude, snow, alpine trails.",
                "phases": [
                    {
                        "title": "Alpine Adventure",
                        "desc": "5 tập từ landing Zurich đến lost on the trail",
                        "steps": [{"seriesId": "switzerland-travel"}],
                    },
                ],
            },
            {
                "id": "english-everyday-get",
                "title": "Everyday Get",
                "subtitle": "Tập 116–118 — meetup, homework, daily English",
                "icon": "📚",
                "color": "#D946EF",
                "duration": "3–4 ngày",
                "desc": "Get used to, get it, get by — học tiếng Anh trong cuộc sống hàng ngày.",
                "phases": [
                    {
                        "title": "Learning English Daily",
                        "desc": "3 tập meetup, aha moment, finale combo",
                        "steps": [{"seriesId": "english-everyday-get"}],
                    },
                ],
            },
        ],
    }


def main() -> None:
    data_dir = ROOT / "data"
    data_dir.mkdir(parents=True, exist_ok=True)
    comics = build_comics()
    roadmap = build_roadmap()
    (data_dir / "comics.json").write_text(
        json.dumps(comics, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
    )
    (data_dir / "roadmap.json").write_text(
        json.dumps(roadmap, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
    )
    print(f"comics.json: {comics['count']} episodes, {len(comics['series'])} series")
    print(f"roadmap.json: {len(roadmap['paths'])} paths")

    import subprocess
    enrich = ROOT / "scripts" / "enrich-comics-from-core.py"
    if enrich.exists():
        subprocess.run(["python3", str(enrich)], check=True)


if __name__ == "__main__":
    main()

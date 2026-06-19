#!/usr/bin/env python3
"""Build episode-guides.json + glossary.json — patterns, extra vocab, grammar."""

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

# ── Grammar rules (trigger → Vietnamese explanation) ─────────────────────
GRAMMAR_RULES = [
    {
        "id": "between-a-and-b",
        "title": "between A and B — song song cấu trúc",
        "triggers": ["torn between", "between a and b", "between deploying"],
        "rule": "Sau **between** phải là **A and B** — hai vế cùng dạng (V-ing/V-ing, noun/noun, to V/to V).",
        "explain": "Không dùng *between deploy or wait* — phải *between deploying and waiting* hoặc *between deployment and waiting*.",
        "exampleGood": "I'm torn between a quick patch and a full refactor.",
        "exampleBad": "I'm torn between deploy or wait.",
    },
    {
        "id": "look-forward-to-ving",
        "title": "look forward to + V-ing",
        "triggers": ["look forward to", "looking forward to"],
        "rule": "**to** ở đây là giới từ, không phải to-infinitive → sau đó dùng **V-ing**.",
        "explain": "Rất hay dùng trong email/meeting: I'm looking forward to meeting you / to visiting Kyoto.",
        "exampleGood": "I'm looking forward to visiting Kyoto.",
        "exampleBad": "I'm looking forward to visit Kyoto.",
    },
    {
        "id": "help-me-with",
        "title": "help someone with something",
        "triggers": ["help me with", "help you with", "help us with"],
        "rule": "Cấu trúc: **help + person + with + noun/V-ing**.",
        "explain": "Không bỏ *with*: Could you help me **with** this?",
        "exampleGood": "Could you help me with this?",
        "exampleBad": "Could you help me this?",
    },
    {
        "id": "tell-me-about-a-time",
        "title": "Tell me about a time when + quá khứ (STAR)",
        "triggers": ["tell me about a time", "one challenge i faced", "what i learned"],
        "rule": "Behavioral interview: **when + câu quá khứ đơn** (Situation → Action → Result).",
        "explain": "Dùng *was/were/did/walked/rolled* — kể chuyện đã xảy ra, không dùng hiện tại.",
        "exampleGood": "Tell me about a time when you handled a production incident.",
        "exampleBad": "Tell me about a time when you handle incidents every day. (sai thì nếu hỏi một lần cụ thể)",
    },
    {
        "id": "role-where-clause",
        "title": "a role where + mệnh đề quan hệ",
        "triggers": ["role where", "looking for a role where", "job where"],
        "rule": "**where** nối mệnh đề bổ nghĩa cho *role/job* — mô tả điều kiện bạn muốn.",
        "explain": "I'm looking for a role **where I can grow** as a full-stack engineer.",
        "exampleGood": "I'm looking for a role where I can work with product.",
        "exampleBad": "I'm looking for a role which I can grow. (which + clause kém tự nhiên hơn where)",
    },
    {
        "id": "see-myself-ving",
        "title": "see myself + V-ing",
        "triggers": ["see myself growing", "see myself working", "see yourself"],
        "rule": "Sau **see myself/yourself** dùng **V-ing** để nói kế hoạch phát triển.",
        "explain": "I see myself **growing in** system design — tự nhiên hơn *I see I will grow*.",
        "exampleGood": "I see myself growing in system design.",
        "exampleBad": "I see myself grow in system design.",
    },
    {
        "id": "what-attracted-me-cleft",
        "title": "What attracted me is… — nhấn mạnh chủ đề",
        "triggers": ["what attracted me", "what i learned", "what we know"],
        "rule": "**What + clause + is/was + noun phrase** — cấu trúc nhấn mạnh (pseudo-cleft).",
        "explain": "What attracted me to this company **is** the global impact.",
        "exampleGood": "What attracted me to this company is the product impact.",
        "exampleBad": "What attracted me is because the product. (thừa because sau is)",
    },
    {
        "id": "walk-me-through",
        "title": "walk someone through something",
        "triggers": ["walk me through", "walk you through", "walk us through", "walk through"],
        "rule": "**walk + person + through + noun** = giải thích từng bước.",
        "explain": "Can you walk me through the payment flow? / Let me walk you through it step by step.",
        "exampleGood": "Can you walk me through the logs?",
        "exampleBad": "Can you walk me the logs? (thiếu through)",
    },
    {
        "id": "it-seems-like",
        "title": "It seems like + clause — suy đoán nhẹ",
        "triggers": ["it seems like", "seems like", "might be caused"],
        "rule": "Dùng khi **chưa chắc 100%** — bug postmortem, phân tích sự cố.",
        "explain": "It seems like the confirm call fails after the cache update.",
        "exampleGood": "It seems like this might be caused by caching.",
        "exampleBad": "It seems like is caused by caching. (lặp is)",
    },
    {
        "id": "bug-affects",
        "title": "The bug affects + noun",
        "triggers": ["bug affects", "affects the", "impact was"],
        "rule": "**affect** (động từ) = ảnh hưởng; **effect** (danh từ) = tác động.",
        "explain": "The bug **affects** the payment flow at the confirm step.",
        "exampleGood": "The bug affects checkout.",
        "exampleBad": "The bug effects checkout. (sai từ — effects là danh từ)",
    },
    {
        "id": "would-it-be-possible",
        "title": "Would it be possible to + V?",
        "triggers": ["would it be possible", "is it possible to", "could we"],
        "rule": "Mở đầu **negotiate lịch sự** — deadline, scope, lịch họp.",
        "explain": "Would it be possible to extend the deadline by two days?",
        "exampleGood": "Would it be possible to push the release to Friday?",
        "exampleBad": "Is possible extend deadline? (thiếu cấu trúc đầy đủ)",
    },
    {
        "id": "lets-imperative",
        "title": "Let's + V — đề xuất làm chung",
        "triggers": ["let's ", "lets ", "let us"],
        "rule": "**Let's + động từ nguyên mẫu** = đề xuất hành động nhóm.",
        "explain": "Let's schedule the technical round. / Let's focus on the facts.",
        "exampleGood": "Let's find the root cause.",
        "exampleBad": "Let's to schedule the round. (không thêm to)",
    },
    {
        "id": "thats-where",
        "title": "That's where + clause",
        "triggers": ["that's where", "that is where"],
        "rule": "**where** chỉ **điểm/vị trí/bước** trong quy trình gây lỗi.",
        "explain": "That's where the 500 errors are coming from.",
        "exampleGood": "That's where the API fails.",
        "exampleBad": "That's where is the error. (sai trật tự từ)",
    },
    {
        "id": "root-cause-appears",
        "title": "Root cause appears to be + noun",
        "triggers": ["root cause", "appears to be", "might be caused"],
        "rule": "Postmortem: dùng **appears/seems** khi chưa chốt 100%.",
        "explain": "Root cause appears to be a race condition in the cache layer.",
        "exampleGood": "The root cause appears to be misconfigured TTL.",
        "exampleBad": "Root cause is definitely maybe cache. (mâu thuẫn / không chuyên nghiệp)",
    },
    {
        "id": "present-perfect-recent",
        "title": "Thì hiện tại hoàn thành — kết quả còn liên quan hiện tại",
        "triggers": ["we've ", "we have ", "i've ", "has been", "have been"],
        "rule": "**have/has + V3** — hành động quá khứ còn ảnh hưởng bây giờ.",
        "explain": "We've deployed the fix / The service has been down for 20 minutes.",
        "exampleGood": "We've mitigated the issue by rolling back.",
        "exampleBad": "We mitigated yesterday and still now use present only without context.",
    },
    {
        "id": "following-up",
        "title": "Following up on / I'm following up",
        "triggers": ["following up", "follow up", "follow-up"],
        "rule": "Email/Slack: **follow up on + topic** = nhắc lại việc đang chờ.",
        "explain": "I'm following up on the PR review from yesterday.",
        "exampleGood": "Following up on our conversation about the deadline.",
        "exampleBad": "I follow up yesterday email. (sai thì/thiếu giới từ)",
    },
    {
        "id": "prefer-to-rather",
        "title": "would rather / prefer — thể hiện ưu tiên",
        "triggers": ["would rather", "prefer ", "leaning toward", "go with"],
        "rule": "**would rather + V** / **prefer A to B** — nói lựa chọn cá nhân.",
        "explain": "I'd rather wait for QA than deploy tonight.",
        "exampleGood": "I prefer a full fix to a quick patch.",
        "exampleBad": "I prefer wait than deploy. (thiếu to V / rather)",
    },
    {
        "id": "issue-is-that",
        "title": "The issue is that + clause",
        "triggers": ["the issue is that", "problem is that", "thing is that"],
        "rule": "**The issue is that + câu** — mở đầu giải thích bug/rủi ro rõ ràng.",
        "explain": "The issue is that the API returns 500 for some users.",
        "exampleGood": "The issue is that we skipped integration tests.",
        "exampleBad": "The issue is the API return 500. (return → returns)",
    },
]

# ── Extra vocabulary (words/phrases in dialogue, not always in packs) ───────
VOCAB_LIBRARY = {
    "full-stack": ("full-stack engineer", "Kỹ sư làm cả frontend lẫn backend"),
    "full-stack engineer": ("kỹ sư full-stack", "Dev làm cả UI và server/API"),
    "system design": ("thiết kế hệ thống", "Kỹ năng thiết kế kiến trúc phần mềm quy mô lớn"),
    "cross-team": ("liên team", "Làm việc giữa nhiều team (product, QA, backend…)"),
    "cross-team communication": ("giao tiếp liên team", "Phối hợp giữa các team bằng tiếng Anh"),
    "technical round": ("vòng phỏng vấn kỹ thuật", "Vòng coding/system design sau phone screen"),
    "phone screen": ("vòng sàng lọc qua điện thoại/video", "Vòng HR/recruiter đầu tiên"),
    "recruiter": ("nhân viên tuyển dụng", "Người liên hệ từ phía công ty"),
    "behavioral interview": ("phỏng vấn hành vi", "Hỏi theo STAR — kể chuyện quá khứ"),
    "production incident": ("sự cố production", "Lỗi ảnh hưởng user thật trên môi trường live"),
    "rolled back": ("đã rollback", "Quay lại phiên bản trước khi deploy lỗi"),
    "rollback": ("hoàn tác bản deploy", "Quay về version ổn định trước đó"),
    "root cause": ("nguyên nhân gốc", "Nguyên nhân sâu xa, không phải triệu chứng"),
    "payment flow": ("luồng thanh toán", "Các bước checkout → confirm → charge → receipt"),
    "step by step": ("từng bước một", "Giải thích chi tiết từng bước"),
    "500 errors": ("lỗi HTTP 500", "Lỗi server — thường gặp khi debug API"),
    "cache update": ("cập nhật cache", "Thay đổi logic/layer cache gây side effect"),
    "monitoring": ("giám sát hệ thống", "Dashboard/alert theo dõi service"),
    "demo": ("buổi demo", "Trình diễn sản phẩm cho stakeholder/investor"),
    "war room": ("phòng xử lý sự cố", "Team tập trung fix incident khẩn cấp"),
    "stakeholder": ("bên liên quan", "PM, manager, khách hàng nội bộ cần update"),
    "postmortem": ("bài học sau sự cố", "Meeting phân tích nguyên nhân không đổ lỗi"),
    "action items": ("hạng mục hành động", "Việc cần làm sau meeting — ai làm gì, deadline"),
    "scope": ("phạm vi công việc", "Những gì trong/ngoài kế hoạch ban đầu"),
    "deadline": ("hạn chót", "Thời điểm phải hoàn thành"),
    "salary range": ("mức lương", "Khoảng lương negotiate khi nhận offer"),
    "counter-offer": ("đề xuất ngược", "Phản đề xuất lương/điều kiện với công ty"),
    "1-on-1": ("họp riêng 1-1", "Meeting manager — feedback, career"),
    "code review": ("review code", "Đồng nghiệp xem PR trước khi merge"),
    "pull request": ("PR", "Yêu cầu merge code — thường review bằng tiếng Anh"),
    "deploy": ("triển khai", "Đưa code lên production/staging"),
    "qa": ("đảm bảo chất lượng", "Team kiểm thử trước release"),
    "shrine": ("đền thờ", "Đi chùa đền Nhật — etiquette riêng"),
    "onsen": ("suối nước nóng", "Tắm onsen — quy tắc văn hóa Nhật"),
    "konbini": ("cửa hàng tiện lợi", "7-Eleven, Lawson — mua đồ hàng ngày"),
    "cherry blossom": ("hoa anh đào", "Mùa hanami — du lịch Nhật"),
    "akihabara": ("khu Akihabara", "Thiên đường anime/điện tử Tokyo"),
    "global product impact": ("tác động sản phẩm toàn cầu", "Sản phẩm dùng ở nhiều quốc gia"),
    "tell me a bit about yourself": ("hãy giới thiệu về bạn", "Câu mở đầu phỏng vấn kinh điển"),
    "why our company": ("tại sao chọn công ty chúng tôi", "Câu hỏi motivation — chuẩn bị câu trả lời"),
    "schedule the technical round": ("sắp lịch vòng kỹ thuật", "Recruiter hẹn bước tiếp theo"),
    "strong example": ("ví dụ tốt", "Interviewer khen cấu trúc STAR rõ"),
    "clear structure": ("cấu trúc rõ ràng", "Trả lời mạch lạc Situation-Action-Result"),
    "find the root cause": ("tìm nguyên nhân gốc", "Bước debug sau khi hiểu flow"),
    "quick patch": ("bản vá nhanh", "Sửa tạm trên production — nhanh nhưng có thể nợ kỹ thuật"),
    "full refactor": ("refactor toàn bộ", "Viết lại code sạch hơn — mất thời gian hơn patch"),
    "deploy today": ("deploy hôm nay", "Đưa code lên production ngay"),
    "wait for qa": ("chờ QA test", "Đợi team QA kiểm thử trước release"),
    "redis": ("Redis cache", "Hệ thống cache in-memory hay gặp khi debug"),
    "rollback": ("hoàn tác bản deploy", "Quay về version ổn định trước đó"),
    "investor": ("nhà đầu tư", "Stakeholder xem demo sản phẩm"),
    "payment outage": ("sự cố thanh toán", "Payment service ngừng hoạt động"),
    "apartment": ("căn hộ", "Thuê nhà ở Tokyo"),
    "moving day": ("ngày chuyển nhà", "Dọn đồ, gặp landlord"),
    "speaking up": ("lên tiếng", "Nói ý kiến trong meeting"),
    "code review": ("review code", "Đồng nghiệp feedback PR"),
    "email thread": ("chuỗi email", "Hội thoại async qua email"),
    "async": ("bất đồng bộ", "Giao tiếp không realtime — email, Slack"),
    "system design": ("thiết kế hệ thống", "Thiết kế kiến trúc scale"),
    "visa": ("thị thực", "Giấy tờ cư trú/du lịch"),
    "healthcare": ("y tế", "Khám bệnh, bảo hiểm"),
    "confirm step": ("bước xác nhận", "Bước confirm trong checkout/payment"),
    "checkout": ("thanh toán / giỏ hàng", "Bước user hoàn tất mua hàng"),
    "architecture": ("kiến trúc hệ thống", "Sơ đồ service, API, database"),
    "sequence diagram": ("sơ đồ trình tự", "Mô tả thứ tự gọi API/message"),
    "mitigated": ("đã giảm thiểu", "Đã xử lý tạm để giảm impact"),
    "timeline": ("dòng thời gian sự kiện", "Thứ tự incident — postmortem"),
    "key takeaway": ("điểm chính cần nhớ", "Kết luận slide/pitch"),
    "pitch": ("thuyết trình ý tưởng", "Trình bày proposal cho team/manager"),
    "push back": ("phản hồi / từ chối nhẹ", "Nói không với scope/deadline không hợp lý"),
    "outside the scope": ("ngoài phạm vi", "Việc không thuộc plan ban đầu"),
}

# ── Vietnamese meanings for core pack patterns & phrasal verbs ─────────────
PATTERN_VI = {
    # decision / hesitation
    "i don't know what to + verb.": "Tôi không biết phải làm gì.",
    "question word + to + verb.": "Cấu trúc: từ để hỏi + to + động từ (what to do, where to go).",
    "i don't know whether to a or b.": "Tôi không biết nên chọn A hay B.",
    "i don't know if i should a or b.": "Tôi không biết có nên A hay B không.",
    "should i + verb?": "Tôi có nên ... không?",
    "i can't decide what to + verb.": "Tôi không quyết định được nên làm gì.",
    "i can't decide between a and b.": "Tôi không quyết định được giữa A và B.",
    "i'm not sure if / whether...": "Tôi không chắc liệu...",
    "i have no idea what / which / how to...": "Tôi hoàn toàn không biết phải... thế nào.",
    "i'm wondering if / whether...": "Tôi đang phân vân liệu...",
    "i'm torn between a and b.": "Tôi phân vân giữa A và B.",
    "i'm debating whether to a or b.": "Tôi đang cân nhắc nên A hay B.",
    # preference / opinion
    "i prefer a to b.": "Tôi thích A hơn B.",
    "i like a more than b.": "Tôi thích A hơn B.",
    "i'd rather a than b.": "Tôi thà A còn hơn B.",
    "i'm leaning toward a.": "Tôi đang nghiêng về A.",
    "a makes more sense to me.": "A hợp lý hơn với tôi.",
    "i'm more interested in a.": "Tôi quan tâm đến A hơn.",
    "i'm not really into a.": "Tôi không thích A lắm.",
    "i think a is better because...": "Tôi nghĩ A tốt hơn vì...",
    "i think i'll go with a.": "Tôi nghĩ tôi sẽ chọn A.",
    # bug report / agreement
    "the issue is that...": "Vấn đề là...",
    "it seems like...": "Có vẻ như...",
    "this might be caused by...": "Cái này có thể do...",
    "the api is returning...": "API đang trả về...",
    "the bug affects...": "Lỗi này ảnh hưởng đến...",
    "i think we should...": "Tôi nghĩ chúng ta nên...",
    "that makes sense.": "Điều đó hợp lý.",
    "i agree with that.": "Tôi đồng ý với điều đó.",
    "i see your point, but...": "Tôi hiểu ý bạn, nhưng...",
    "i'm not sure i agree.": "Tôi không chắc tôi đồng ý.",
    "i have a different take.": "Tôi có góc nhìn khác.",
    # phrasal verbs
    "go with": "chọn (một phương án)",
    "rule out": "loại trừ",
    "think over": "cân nhắc kỹ",
    "sleep on it": "để qua đêm suy nghĩ rồi quyết",
    "settle on": "chốt (một lựa chọn)",
    "opt for": "chọn lấy",
    "narrow down": "thu hẹp lựa chọn",
    "weigh up": "cân nhắc lợi hại",
    "come down to": "rốt cuộc là do",
    "stick with": "giữ nguyên / bám theo",
    "pass on": "bỏ qua / từ chối",
    "be into": "thích / mê",
    "act as": "đóng vai trò như",
    "rely on": "phụ thuộc vào",
    "go through": "xem qua / trải qua",
    "get through": "vượt qua / hoàn thành",
    "work through": "xử lý từng phần",
    "walk through": "giải thích từng bước",
    "run through": "lướt qua / diễn thử",
    "think through": "suy nghĩ thấu đáo",
    "follow through": "làm đến cùng",
    "fall through": "đổ bể / thất bại",
    "ask for": "yêu cầu / xin",
    "be responsible for": "chịu trách nhiệm về",
    "bring back": "mang lại / khôi phục",
    "calm down": "bình tĩnh lại",
    "catch up": "bắt kịp / cập nhật tình hình",
    "check in": "điểm danh / báo tình hình",
    "check in on": "ghé xem / hỏi thăm",
    "check out": "kiểm tra / trả phòng",
    "check with": "hỏi ý / xác nhận với",
    "cheer up": "vui lên",
    "come across": "tình cờ gặp / gây ấn tượng",
    "deal with": "xử lý / giải quyết",
    "figure out": "tìm ra / hiểu ra",
    "fill out": "điền (form)",
    "find out": "phát hiện ra",
    "fit in": "hòa nhập",
    "flag for": "đánh dấu để lưu ý",
    "get used to": "quen dần với",
    "hang out": "đi chơi",
    "drop off": "thả ai/đồ ở đâu",
    "keep posted": "cập nhật thường xuyên",
    "look for": "tìm kiếm",
    "look up": "tra cứu",
    "loop me in": "cho tôi vào luồng thông tin",
    "mitigate": "giảm thiểu (sự cố)",
    "move up": "dời lên sớm hơn",
    "open up": "mở lòng / mở ra",
    "pay for": "trả tiền cho",
    "pick up": "lấy / đón / học lỏm",
    "put off": "trì hoãn",
    "roll back": "hoàn tác bản deploy",
    "run late": "bị trễ",
    "run out of": "hết (cái gì)",
    "set up": "thiết lập",
    "show up": "xuất hiện / có mặt",
    "sign up for": "đăng ký",
    "stress out": "căng thẳng",
    "take ownership of": "nhận trách nhiệm chính",
    "touch base": "liên lạc trao đổi nhanh",
    "trade off": "đánh đổi",
    "take over": "tiếp quản",
    # universal communication
    "are you available at + time?": "Bạn có rảnh lúc ... không?",
    "can i get a receipt?": "Cho tôi xin hóa đơn được không?",
    "can i pay by card?": "Tôi trả bằng thẻ được không?",
    "can we move it to tomorrow?": "Dời sang ngày mai được không?",
    "can we move it up?": "Dời lên sớm hơn được không?",
    "can we push it back by 30 minutes?": "Lùi lại 30 phút được không?",
    "can you show me how to + verb?": "Bạn chỉ tôi cách ... được không?",
    "could you help me with this?": "Bạn giúp tôi việc này được không?",
    "could you say that again?": "Bạn nói lại được không?",
    "could you speak a little more slowly?": "Bạn nói chậm hơn chút được không?",
    "do you have...?": "Bạn/quán có ... không?",
    "does + time + work for you?": "Thời gian ... có hợp với bạn không?",
    "how long does it take?": "Mất bao lâu vậy?",
    "how much is this?": "Cái này bao nhiêu tiền?",
    "is there a cheaper option?": "Có lựa chọn rẻ hơn không?",
    "is this included?": "Cái này có bao gồm không?",
    "i'd like to...": "Tôi muốn...",
    "i'll be there in + time.": "Tôi sẽ tới sau ... nữa.",
    "i'm glad that...": "Tôi mừng vì...",
    "i'm here to pick up...": "Tôi đến để lấy...",
    "i'm not sure i understand.": "Tôi không chắc mình hiểu.",
    "i'm running late.": "Tôi đang bị trễ.",
    "i'm worried about...": "Tôi lo về...",
    "just to clarify, do you mean a or b?": "Cho rõ nhé, ý bạn là A hay B?",
    "let's meet at + place.": "Gặp nhau ở ... nhé.",
    "please keep me posted on...": "Cập nhật cho tôi về ... nhé.",
    "should i + verb?": "Tôi có nên ... không?",
    "sorry, i missed that.": "Xin lỗi, tôi nghe sót.",
    "thanks for the quick follow-up!": "Cảm ơn đã phản hồi nhanh!",
    "that sounds stressful.": "Nghe căng thẳng thật.",
    "the result was that...": "Kết quả là...",
    "what time works best for you?": "Mấy giờ tiện cho bạn nhất?",
    "i agree with that.": "Tôi đồng ý với điều đó.",
    "i can't decide between a and b.": "Tôi không quyết được giữa A và B.",
    "i didn't expect that.": "Tôi không ngờ tới điều đó.",
    "i like a more than b.": "Tôi thích A hơn B.",
    "i need to fill out this form.": "Tôi cần điền form này.",
    "i need to reschedule.": "Tôi cần dời lịch.",
    "i prefer a to b.": "Tôi thích A hơn B.",
    "i think a is better because...": "Tôi nghĩ A tốt hơn vì...",
    "i'm not sure i agree.": "Tôi không chắc tôi đồng ý.",
}

WHEN_TO_USE = {
    "torn between": "Khi phân vân giữa hai lựa chọn — meeting, đời sống, du lịch.",
    "leaning toward": "Khi bạn đã nghiêng về một phương án nhưng chưa chốt.",
    "go with": "Khi quyết định chọn một phương án (informal, tự nhiên).",
    "issue is that": "Khi báo bug hoặc giải thích vấn đề kỹ thuật.",
    "walk me through": "Khi nhờ ai giải thích từng bước — code review, demo, debug.",
    "see your point": "Khi đồng ý một phần rồi phản biện nhẹ — disagree politely.",
    "looking for a role": "Khi phỏng vấn — nói mục tiêu nghề nghiệp.",
    "tell me about a time": "Câu behavioral interview — kể chuyện quá khứ (STAR).",
    "would it be possible": "Mở đầu negotiate lịch sự — deadline, scope, salary.",
    "outside the scope": "Khi PM/ khách thêm việc ngoài plan ban đầu.",
    "push back": "Từ chối / phản hồi nhẹ nhàng mà không burn bridge.",
    "one thing that went well": "Feedback tích cực trong 1-on-1 hoặc code review.",
    "how can i support": "Hỏi junior/ đồng nghiệp cần giúp gì — mentoring.",
    "key takeaway": "Kết thúc demo/pitch bằng một điểm nhớ.",
    "what we know so far": "Update sự cố — war room, stakeholder.",
    "root cause appears": "Postmortem — nói nguyên nhân khi chưa chắc 100%.",
    "following up": "Email/Slack — nhắc lại việc đang chờ phản hồi.",
    "help me with": "Nhờ giúp đỡ hàng ngày — konbini, bank, travel.",
    "excited about": "Small talk — thể hiện cảm xúc tích cực.",
    "look forward to": "Nói về kế hoạch tương lai — interview, travel, work.",
}

STRUCTURE_HINTS = {
    "torn between": "I'm torn between + A + and + B (A/B cùng dạng từ)",
    "leaning toward": "I'm leaning toward + option (+ because ...)",
    "tell me about a time": "Tell me about a time when + past tense (STAR)",
    "would it be possible": "Would it be possible to + verb?",
    "what we know so far": "What we know so far is + fact.",
    "root cause appears": "Root cause appears to be + noun phrase.",
}


def slug_id(text: str) -> str:
    s = text.lower().replace("'", "'")
    s = re.sub(r"[^a-z0-9]+", "-", s).strip("-")
    return s[:80] or "term"


def normalize(text: str) -> str:
    t = (text or "").lower().replace("\u2019", "'").replace("\u2018", "'")
    return re.sub(r"\s+", " ", t.strip().rstrip(".!?"))


_PATTERN_VI_NORM = None


def lookup_vi(phrase: str) -> str:
    global _PATTERN_VI_NORM
    if _PATTERN_VI_NORM is None:
        _PATTERN_VI_NORM = {normalize(k): v for k, v in PATTERN_VI.items()}
    return _PATTERN_VI_NORM.get(normalize(phrase), "")


def guess_when(phrase: str) -> str:
    low = phrase.lower()
    for key, val in WHEN_TO_USE.items():
        if key in low:
            return val
    if "?" in phrase:
        return "Dùng khi hỏi hoặc đề xuất — phù hợp meeting và giao tiếp hàng ngày."
    return "Xuất hiện trong hội thoại truyện — học thêm từ vựng ngoài pattern pack."


def guess_structure(phrase: str) -> str:
    low = phrase.lower()
    for key, val in STRUCTURE_HINTS.items():
        if key in low:
            return val
    if phrase.endswith("..."):
        return phrase.replace("...", " + [nội dung cụ thể]")
    return phrase


def example_for(phrase: str, title: str) -> str:
    p = phrase.replace("...", "the payment flow")
    if "A and B" in phrase or "A or B" in phrase:
        p = phrase.replace("A and B", "a quick patch and a full refactor").replace("A or B", "deploy today or wait")
    if not p.endswith((".", "?", "!")):
        p = p.rstrip(".") + "."
    return p


def series_context(tag: str, desc: str) -> str:
    if tag == "Du lịch":
        return "du lịch Nhật cùng team"
    if tag == "Cuộc sống":
        return "sống và làm việc ở Tokyo"
    if tag == "Career":
        return "phỏng vấn, thương lượng, hoặc lead team"
    if tag in ("Văn hóa", "Anime"):
        return "khám phá văn hóa và đời sống Nhật"
    if tag == "Công việc":
        return "team dev Tokyo — meeting, debug, release"
    return desc.split("—")[0].strip().lower() if "—" in desc else "tình huống thực tế"


def parse_prompts() -> dict:
    """slug -> {dialogues: [...], focus_map: {phrase: vi}}"""
    by_slug: dict = {}

    def add_slug(slug, dialogues=None, focus_map=None):
        if not slug:
            return
        entry = by_slug.setdefault(slug, {"dialogues": [], "focus_map": {}})
        for d in dialogues or []:
            d = d.strip()
            if len(d) > 8 and d not in entry["dialogues"]:
                entry["dialogues"].append(d)
        for phrase, vi in (focus_map or {}).items():
            entry["focus_map"][phrase.strip()] = vi.strip()

    quote_re = re.compile(r'["\']([^"\']{8,})["\']')

    for path in (ROOT / "prompts").glob("*-comic.md"):
        content = path.read_text(encoding="utf-8")
        slug_m = re.search(r"\*\*Slug(?: gợi ý)?:\*\* `([^`]+)`", content)
        slug = slug_m.group(1) if slug_m else None
        if not slug:
            slug_m2 = re.search(r"\*\*Slug:\*\* `([^`]+)`", content)
            slug = slug_m2.group(1) if slug_m2 else None

        dialogues = []
        for line in content.splitlines():
            if re.search(r"(Dialogue|Speech):", line, re.I) or re.search(r"^Panel \d+:", line, re.I):
                dialogues.extend(quote_re.findall(line))

        focus_map = {}
        for m in re.finditer(r'"([^"]+)"\s*=\s*([^\n|]+)', content):
            focus_map[m.group(1).strip()] = m.group(2).strip()

        add_slug(slug, dialogues, focus_map)

    for path in (ROOT / "prompts" / "arcs").glob("*.md"):
        content = path.read_text(encoding="utf-8")
        blocks = re.split(r"^## Tập \d+", content, flags=re.MULTILINE)
        for block in blocks[1:]:
            slug_m = re.search(r"\*\*Slug\*\* \| `([^`]+)`", block)
            if not slug_m:
                slug_m = re.search(r"\| \*\*Slug\*\* \| `([^`]+)`", block)
            slug = slug_m.group(1) if slug_m else None
            dialogues = quote_re.findall(block)
            focus_line = re.search(r"\*\*ENGLISH FOCUS:\*\* (.+)", block)
            focus_map = {}
            if focus_line:
                for part in re.split(r"/", focus_line.group(1)):
                    part = part.strip().strip(".")
                    if part:
                        focus_map[part] = ""
            add_slug(slug, dialogues, focus_map)

    return by_slug


def focus_phrase_set(ep: dict) -> set[str]:
    out = set()
    for f in ep.get("englishFocus") or []:
        p = normalize(f.get("phrase", ""))
        if p:
            out.add(p)
            out.add(p.replace("...", "").strip())
    for p in ep.get("patterns") or []:
        if isinstance(p, str):
            out.add(normalize(p))
    return out


def is_covered_by_focus(candidate: str, focus: set[str]) -> bool:
    c = normalize(candidate)
    if not c or len(c) < 4:
        return True
    for f in focus:
        if not f:
            continue
        if f in c or c in f:
            return True
        # overlap significant words
        fw = set(re.findall(r"[a-z']+", f))
        cw = set(re.findall(r"[a-z']+", c))
        if fw and cw and len(fw & cw) >= min(2, len(fw)):
            return True
    return False


def extract_extra_vocab(ep: dict, prompt_data) -> list[dict]:
    focus = focus_phrase_set(ep)
    dialogues = (prompt_data or {}).get("dialogues") or []
    blob = " ".join(dialogues).lower()
    found: dict[str, dict] = {}

    # Scan vocab library against dialogue blob
    for key, (short, vi) in sorted(VOCAB_LIBRARY.items(), key=lambda x: -len(x[0])):
        if key.lower() in blob and not is_covered_by_focus(key, focus):
            found[key] = {
                "phrase": key,
                "meaning": vi,
                "note": short,
                "source": "dialogue",
            }

    # Extract short useful quotes from dialogue not in focus
    for line in dialogues:
        line_n = normalize(line)
        if is_covered_by_focus(line, focus):
            continue
        if len(line) > 90:
            # try sub-clauses
            for chunk in re.split(r"[,;.]", line):
                chunk = chunk.strip()
                if 12 <= len(chunk) <= 80 and not is_covered_by_focus(chunk, focus):
                    vi = VOCAB_LIBRARY.get(chunk.lower(), (chunk, "Cụm trong hội thoại tập này"))[1]
                    found[chunk] = {
                        "phrase": chunk,
                        "meaning": vi if isinstance(vi, str) else chunk,
                        "note": "Trích từ hội thoại truyện",
                        "source": "dialogue",
                    }
        elif 12 <= len(line) <= 80 and not is_covered_by_focus(line, focus):
            key = line.lower()
            vi = VOCAB_LIBRARY.get(key, (line, "Câu/cụm trong hội thoại"))[1]
            found[line] = {
                "phrase": line,
                "meaning": vi,
                "note": "Trích từ hội thoại truyện",
                "source": "dialogue",
            }

    # Title + slug fallback (episodes without prompt files)
    title_blob = f"{ep.get('title', '')} {ep.get('slug', '')}".lower()
    for key, (short, vi) in sorted(VOCAB_LIBRARY.items(), key=lambda x: -len(x[0])):
        if key.lower() in title_blob and key not in found and not is_covered_by_focus(key, focus):
            found[key] = {
                "phrase": key.title() if len(key) < 20 else key,
                "meaning": vi,
                "note": short,
                "source": "title",
            }

    # Context tags → vocab hints
    CONTEXT_VOCAB = {
        "software-engineering": ("production bug", "Lỗi trên môi trường user thật"),
        "debugging": ("debug logs", "Xem log để tìm lỗi"),
        "travel": ("itinerary", "Lịch trình du lịch"),
        "japan-life": ("landlord", "Chủ nhà cho thuê"),
        "interview": ("phone screen", "Vòng sàng lọc phỏng vấn đầu"),
        "negotiation": ("push back", "Phản hồi khi scope/deadline không hợp lý"),
        "incident": ("war room", "Phòng xử lý sự cố khẩn"),
        "presentation": ("key takeaway", "Điểm chính cần nhớ sau pitch"),
    }
    for ctx in ep.get("contexts") or []:
        if ctx in CONTEXT_VOCAB and len(found) < 8:
            phrase, vi = CONTEXT_VOCAB[ctx]
            if phrase not in found and not is_covered_by_focus(phrase, focus):
                short = vi
                found[phrase] = {
                    "phrase": phrase,
                    "meaning": vi,
                    "note": f"Chủ đề: {ctx.replace('-', ' ')}",
                    "source": "context",
                }

    items = list(found.values())[:8]
    for item in items:
        item["explain"] = (
            f"**{item['phrase']}** — {item['meaning']}. "
            f"{item.get('note', '')} "
            f"Không nằm trong English Focus chính nhưng xuất hiện trong truyện — học thêm để đọc hiểu và nói tự nhiên hơn."
        )
    return items


def detect_grammar(ep: dict, phrases: list[str], dialogues: list[str]) -> list[dict]:
    blob = " ".join(phrases + dialogues).lower()
    for m in ep.get("commonMistakes") or []:
        blob += " " + m.get("why", "").lower() + " " + m.get("wrong", "").lower()

    rules = []
    seen = set()
    for rule in GRAMMAR_RULES:
        if any(t in blob for t in rule["triggers"]):
            rid = rule["id"]
            if rid not in seen:
                rules.append({
                    "id": rid,
                    "title": rule["title"],
                    "rule": rule["rule"],
                    "explain": rule["explain"],
                    "exampleGood": rule["exampleGood"],
                    "exampleBad": rule["exampleBad"],
                })
                seen.add(rid)

    for m in ep.get("commonMistakes") or []:
        mid = slug_id(m.get("why", m.get("wrong", "mistake")))
        if mid in seen:
            continue
        rules.append({
            "id": mid,
            "title": f"⚠️ {m.get('why', 'Lỗi thường gặp')}",
            "rule": f"Sai: **{m.get('wrong', '')}**",
            "explain": f"Đúng: **{m.get('correct', '')}** — {m.get('why', '')}",
            "exampleGood": m.get("correct", ""),
            "exampleBad": m.get("wrong", ""),
        })
        seen.add(mid)
        if len(rules) >= 6:
            break

    return rules[:6]


def build_story_recap(ep: dict, series: dict, dialogues: list[str]) -> str:
    title = ep["title"]
    ctx = series_context(series.get("tag", ""), series.get("desc", ""))
    focus = ep.get("englishFocus") or []
    if dialogues:
        sample = dialogues[0][:120] + ("…" if len(dialogues[0]) > 120 else "")
        return (
            f"Trong tập «{title}», Nam gặp tình huống {ctx}. "
            f"Ví dụ câu trong truyện: *\"{sample}\"* — "
            f"đọc ảnh, chú ý ENGLISH FOCUS và các từ phụ trong hội thoại."
        )
    if focus:
        main = focus[0]["phrase"]
        return (
            f"Trong tập «{title}», Nam gặp tình huống {ctx}. "
            f"Hội thoại xoay quanh cụm **{main}** — đọc ảnh truyện và chú ý ENGLISH FOCUS ở cuối."
        )
    return (
        f"Trong tập «{title}», Nam tiếp tục hành trình {ctx}. "
        f"Đọc hội thoại trong ảnh và tìm các cụm tiếng Anh tự nhiên."
    )


def build_summary(ep: dict, series: dict) -> str:
    title = ep["title"]
    tag = series.get("tag", "")
    return (
        f"**{title}** thuộc arc {series['title']}. "
        f"Học **pattern + từ vựng hội thoại + ngữ pháp** cho {series_context(tag, series.get('desc', ''))}."
    )


def build_learning_goal(ep: dict, series: dict) -> str:
    focus = ep.get("englishFocus") or []
    parts = []
    if focus:
        phrases = ", ".join(f"「{f['phrase']}」" for f in focus[:3])
        parts.append(f"Pattern: {phrases}")
    parts.append("Từ vựng phụ trong hội thoại truyện")
    parts.append("1–2 điểm ngữ pháp liên quan tập này")
    return " · ".join(parts) + "."


def build_phrase_detail(f: dict, ep: dict, series: dict) -> dict:
    phrase = f.get("phrase", "")
    meaning = f.get("meaning", "") or lookup_vi(phrase)
    ctx = series_context(series.get("tag", ""), series.get("desc", ""))
    when = guess_when(phrase)
    return {
        "phrase": phrase,
        "meaning": meaning,
        "kind": "pattern",
        "explain": (
            f"Cụm **{phrase}** dịch là *{meaning.rstrip('.')}*. "
            f"Đây là pattern chính (English Focus). {when} "
            f"Trong tập «{ep['title']}», Nam dùng khi {ctx}."
        ),
        "whenToUse": when,
        "structure": guess_structure(phrase),
        "exampleEn": example_for(phrase, ep["title"]),
        "exampleVi": f"Ngữ cảnh tập: «{ep['title']}».",
        "speakTip": "① Đọc to 3 lần  ② Tự nói 1 câu  ③ Review Mode sửa lỗi.",
    }


def build_practice_steps(ep: dict) -> list[str]:
    steps = [
        "Đọc truyện — chú ý ENGLISH FOCUS và từ phụ trong speech bubbles.",
        "Đọc phần Pattern + Từ vựng thêm + Ngữ pháp bên dưới.",
    ]
    for p in (ep.get("practicePrompts") or [])[:2]:
        steps.append(p)
    steps.append("Mở Review Mode — nói 5 câu (pattern + từ mới), AI sửa ngay.")
    return steps[:5]


def derive_focus_from_packs(ep: dict, pack_patterns: dict) -> list[dict]:
    """For episodes without englishFocus, pick relevant patterns from their packs."""
    title = ep.get("title", "").lower()
    title_words = set(re.findall(r"[a-z]+", title))
    candidates = []
    seen = set()
    for pid in ep.get("packs") or []:
        for phrase in pack_patterns.get(pid, []):
            key = normalize(phrase)
            if key in seen or len(phrase) < 4:
                continue
            seen.add(key)
            vi = lookup_vi(phrase)
            if not vi:
                continue
            pw = set(re.findall(r"[a-z]+", phrase.lower()))
            score = len(title_words & pw)
            candidates.append((score, phrase, vi))
    candidates.sort(key=lambda x: -x[0])
    picked = candidates[:3] if candidates else []
    return [{"phrase": p, "meaning": vi} for _, p, vi in picked]


def build_guide(ep: dict, series: dict, prompt_data, pack_patterns: dict) -> dict:
    dialogues = (prompt_data or {}).get("dialogues") or []
    focus = ep.get("englishFocus") or []
    derived = False
    if not focus:
        focus = derive_focus_from_packs(ep, pack_patterns)
        derived = bool(focus)
    phrase_texts = [f.get("phrase", "") for f in focus]
    extra = extract_extra_vocab(ep, prompt_data)
    grammar = detect_grammar(ep, phrase_texts, dialogues)

    phrases = []
    for f in focus:
        detail = build_phrase_detail(f, ep, series)
        if derived:
            detail["kind"] = "pattern-suggested"
            detail["explain"] = (
                f"Cụm **{f['phrase']}** dịch là *{f.get('meaning','').rstrip('.')}*. "
                f"Tập này chưa gắn English Focus cố định, nhưng đây là pattern từ pack của tập — "
                f"rất hợp tình huống «{ep['title']}». {guess_when(f['phrase'])}"
            )
        phrases.append(detail)

    return {
        "summary": build_summary(ep, series),
        "learningGoal": build_learning_goal(ep, series),
        "storyRecap": build_story_recap(ep, series, dialogues),
        "phrases": phrases,
        "phrasesDerived": derived,
        "extraVocab": extra,
        "grammar": grammar,
        "practiceSteps": build_practice_steps(ep),
        "realLifeTip": (
            "Học đủ 3 lớp: pattern (nói được) + từ phụ (hiểu truyện) + ngữ pháp (nói đúng). "
            "Áp dụng vào Slack/meeting thật trong tuần này."
        ),
    }


def collect_glossary(comics: dict, core: dict, all_guides: dict) -> dict:
    terms_map: dict[str, dict] = {}
    pack_titles = {p["id"]: p["title"] for p in core.get("packs", [])}

    def add_term(
        phrase: str,
        meaning: str,
        *,
        series_id=None,
        ep_num=None,
        ep_title=None,
        pack=None,
        kind="pattern",
        note="",
    ):
        if not phrase or len(phrase.strip()) < 2:
            return
        tid = slug_id(phrase)
        if not meaning and kind in ("pattern", "phrasal"):
            meaning = lookup_vi(phrase)
        if tid not in terms_map:
            terms_map[tid] = {
                "id": tid,
                "term": phrase.strip(),
                "aliases": [],
                "vi": meaning or "",
                "short": (note or guess_when(phrase))[:140],
                "long": (
                    f"{phrase.strip()} — {meaning or 'Mục từ vựng/pattern tiếng Anh'}. "
                    f"{guess_when(phrase)} Cấu trúc: {guess_structure(phrase)}"
                ),
                "example": example_for(phrase, ep_title or "daily life"),
                "type": kind,
                "pack": pack,
                "packTitle": pack_titles.get(pack, "") if pack else "",
                "episodes": [],
                "related": [],
            }
        if series_id and ep_num:
            ep_ref = {"seriesId": series_id, "num": ep_num, "title": ep_title or ""}
            if ep_ref not in terms_map[tid]["episodes"]:
                terms_map[tid]["episodes"].append(ep_ref)
        if not terms_map[tid]["vi"]:
            terms_map[tid]["vi"] = meaning or lookup_vi(phrase)

    for series in comics["series"]:
        sid = series["id"]
        for ep in series["episodes"]:
            key = f"{sid}/{ep['num']}"
            guide = all_guides.get(key, {})
            packs = ep.get("packs") or []

            for f in ep.get("englishFocus") or []:
                add_term(
                    f.get("phrase", ""),
                    f.get("meaning", ""),
                    series_id=sid,
                    ep_num=ep["num"],
                    ep_title=ep["title"],
                    pack=packs[0] if packs else None,
                    kind="pattern",
                )
            for v in guide.get("extraVocab") or []:
                add_term(
                    v.get("phrase", ""),
                    v.get("meaning", ""),
                    series_id=sid,
                    ep_num=ep["num"],
                    ep_title=ep["title"],
                    kind="vocab",
                    note=v.get("note", ""),
                )
            for g in guide.get("grammar") or []:
                add_term(
                    g.get("title", ""),
                    g.get("rule", ""),
                    series_id=sid,
                    ep_num=ep["num"],
                    ep_title=ep["title"],
                    kind="grammar",
                    note=g.get("explain", "")[:140],
                )

    for pack in core.get("packs", []):
        pid = pack["id"]
        for p in pack.get("patterns") or []:
            add_term(p, "", pack=pid, kind="pattern")
        for p in pack.get("phrasalVerbs") or pack.get("phrases") or []:
            add_term(p, "", pack=pid, kind="phrasal")
        for g in pack.get("groups") or []:
            for p in g.get("patterns") or []:
                add_term(p, "", pack=pid, kind="pattern")
            for p in g.get("phrases") or []:
                add_term(p, "", pack=pid, kind="phrasal")

    for rule in GRAMMAR_RULES:
        add_term(rule["title"], rule["rule"], kind="grammar", note=rule["explain"])

    terms = sorted(terms_map.values(), key=lambda t: t["term"].lower())
    by_pack: dict[str, list] = {}
    for t in terms:
        if t.get("pack"):
            by_pack.setdefault(t["pack"], []).append(t["id"])
    for t in terms:
        peers = [x for x in by_pack.get(t.get("pack"), []) if x != t["id"]]
        t["related"] = peers[:4]

    type_counts = {}
    for t in terms:
        type_counts[t["type"]] = type_counts.get(t["type"], 0) + 1

    return {
        "meta": {
            "title": "English Vault — Từ điển đầy đủ",
            "count": len(terms),
            "typeCounts": type_counts,
            "subtitle": "Pattern · Phrasal verb · Từ vựng truyện · Ngữ pháp — 122 tập",
        },
        "terms": terms,
    }


def main() -> None:
    comics = json.loads((ROOT / "data" / "comics.json").read_text(encoding="utf-8"))
    core = json.loads((ROOT / "data" / "core.json").read_text(encoding="utf-8"))
    prompts_by_slug = parse_prompts()

    pack_patterns: dict = {}
    for pack in core.get("packs", []):
        pid = pack["id"]
        pats = list(pack.get("patterns") or [])
        pats += list(pack.get("phrasalVerbs") or pack.get("phrases") or [])
        for g in pack.get("groups") or []:
            pats += list(g.get("patterns") or [])
            pats += list(g.get("phrases") or [])
        pack_patterns[pid] = pats

    guides = {}
    for series in comics["series"]:
        sid = series["id"]
        for ep in series["episodes"]:
            key = f"{sid}/{ep['num']}"
            slug = ep.get("slug", "")
            prompt_data = prompts_by_slug.get(slug)
            guides[key] = build_guide(ep, series, prompt_data, pack_patterns)

    glossary = collect_glossary(comics, core, guides)

    (ROOT / "data" / "episode-guides.json").write_text(
        json.dumps({"version": 2, "count": len(guides), "guides": guides}, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    (ROOT / "data" / "glossary.json").write_text(
        json.dumps(glossary, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    print(f"episode-guides.json: {len(guides)} guides (v2 — vocab + grammar)")
    print(f"glossary.json: {glossary['meta']['count']} terms — {glossary['meta'].get('typeCounts', {})}")


if __name__ == "__main__":
    main()

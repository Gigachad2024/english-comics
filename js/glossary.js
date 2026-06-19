/* English Vault — Glossary module */
const Glossary = (() => {
  let data = null;
  let comics = null;
  let termById = {};
  let termByPhrase = {};
  let popoverEl = null;
  let listenersBound = false;

  function slugId(text) {
    return String(text || "")
      .toLowerCase()
      .replace(/['']/g, "'")
      .replace(/[^a-z0-9]+/g, "-")
      .replace(/^-|-$/g, "")
      .slice(0, 80) || "term";
  }

  function escapeHtml(s) {
    return String(s || "")
      .replace(/&/g, "&amp;")
      .replace(/</g, "&lt;")
      .replace(/>/g, "&gt;")
      .replace(/"/g, "&quot;");
  }

  function init(glossaryData, comicsData) {
    data = glossaryData;
    comics = comicsData;
    termById = {};
    termByPhrase = {};
    (data?.terms || []).forEach((t) => {
      termById[t.id] = t;
      termByPhrase[t.term.toLowerCase()] = t;
      (t.aliases || []).forEach((a) => {
        termByPhrase[a.toLowerCase()] = t;
      });
    });
  }

  function getTerm(id) {
    return termById[id] || null;
  }

  function findTerm(text) {
    if (!text) return null;
    const low = text.trim().toLowerCase();
    if (termByPhrase[low]) return termByPhrase[low];
    const partial = (data?.terms || []).find(
      (t) => low.includes(t.term.toLowerCase()) || t.term.toLowerCase().includes(low)
    );
    return partial || null;
  }

  function getSeriesTitle(seriesId) {
    return comics?.series?.find((s) => s.id === seriesId)?.title || seriesId;
  }

  function termButton(term, label) {
    const id = typeof term === "string" ? slugId(term) : term.id;
    const text = label || (typeof term === "string" ? term : term.term);
    return `<button type="button" class="glossary-term" data-term-id="${escapeHtml(id)}" title="Xem trong từ điển">${escapeHtml(text)}</button>`;
  }

  function linkify(text) {
    if (!text || typeof Glossary === "undefined") return escapeHtml(text);
    let out = escapeHtml(text);
    const sorted = [...(data?.terms || [])].sort((a, b) => b.term.length - a.term.length);
    sorted.forEach((t) => {
      const re = new RegExp(`\\b(${t.term.replace(/[.*+?^${}()|[\]\\]/g, "\\$&")})\\b`, "gi");
      out = out.replace(re, (m) => termButton(t, m));
    });
    return out;
  }

  function ensurePopover() {
    if (popoverEl) return popoverEl;
    popoverEl = document.createElement("div");
    popoverEl.id = "glossary-popover";
    popoverEl.className = "glossary-popover hidden";
    popoverEl.setAttribute("role", "dialog");
    popoverEl.setAttribute("aria-label", "Giải thích từ");
    document.body.appendChild(popoverEl);
    return popoverEl;
  }

  function closePopover() {
    const el = popoverEl || document.getElementById("glossary-popover");
    if (el) el.classList.add("hidden");
  }

  function openPopover(termId, anchor) {
    const term = getTerm(termId);
    if (!term) return;
    const pop = ensurePopover();
    const related = (term.related || [])
      .map((rid) => getTerm(rid))
      .filter(Boolean)
      .slice(0, 4);

    const epLinks = (term.episodes || [])
      .slice(0, 4)
      .map(
        (ep) =>
          `<a class="glossary-pop-ep-link" href="#/read/${ep.seriesId}/${ep.num}" onclick="Glossary.closePopover()">${escapeHtml(getSeriesTitle(ep.seriesId))} · T${ep.num}</a>`
      )
      .join("");

    pop.innerHTML = `
      <div class="glossary-pop-header">
        <div>
          <div class="glossary-pop-term">${escapeHtml(term.term)}</div>
          ${term.aliases?.length ? `<div class="glossary-pop-alias">${term.aliases.map(escapeHtml).join(" · ")}</div>` : ""}
        </div>
        <button type="button" class="glossary-pop-close" aria-label="Đóng">✕</button>
      </div>
      ${term.vi ? `<div class="glossary-pop-vi">${escapeHtml(term.vi)}</div>` : ""}
      ${term.short ? `<p class="glossary-pop-short">${escapeHtml(term.short)}</p>` : ""}
      ${term.example ? `<div class="glossary-pop-example"><span class="glossary-pop-example-label">Ví dụ</span>${escapeHtml(term.example)}</div>` : ""}
      ${term.long ? `<div class="glossary-pop-long"><span class="glossary-pop-long-label">Chi tiết</span>${escapeHtml(term.long)}</div>` : ""}
      ${epLinks ? `<div class="glossary-pop-related"><span class="glossary-pop-related-label">Xuất hiện trong</span>${epLinks}</div>` : ""}
      ${related.length ? `<div class="glossary-pop-related"><span class="glossary-pop-related-label">Liên quan</span>${related.map((r) => `<button type="button" class="glossary-related-chip" data-term-id="${escapeHtml(r.id)}">${escapeHtml(r.term)}</button>`).join("")}</div>` : ""}
      <a class="glossary-pop-full-link" href="#/glossary/${term.id}" onclick="Glossary.closePopover()">Mở trong từ điển →</a>`;

    pop.querySelector(".glossary-pop-close")?.addEventListener("click", closePopover);
    pop.querySelectorAll("[data-term-id]").forEach((btn) => {
      btn.addEventListener("click", (e) => {
        e.preventDefault();
        openPopover(btn.dataset.termId, btn);
      });
    });

    pop.classList.remove("hidden");

    if (anchor) {
      const rect = anchor.getBoundingClientRect();
      const popRect = pop.getBoundingClientRect();
      let top = rect.bottom + window.scrollY + 8;
      let left = rect.left + window.scrollX;
      if (left + 320 > window.innerWidth) left = window.innerWidth - 330;
      if (top + popRect.height > window.scrollY + window.innerHeight) {
        top = rect.top + window.scrollY - popRect.height - 8;
      }
      pop.style.position = "absolute";
      pop.style.top = `${Math.max(8, top)}px`;
      pop.style.left = `${Math.max(8, left)}px`;
    }
  }

  function setupGlobalListeners() {
    if (listenersBound) return;
    listenersBound = true;
    document.addEventListener("click", (e) => {
      const btn = e.target.closest(".glossary-term, .glossary-related-chip");
      if (btn?.dataset?.termId) {
        e.preventDefault();
        openPopover(btn.dataset.termId, btn);
        return;
      }
      const pop = popoverEl || document.getElementById("glossary-popover");
      if (pop && !pop.classList.contains("hidden") && !e.target.closest(".glossary-popover")) {
        closePopover();
      }
    });
    document.addEventListener("keydown", (e) => {
      if (e.key === "Escape") closePopover();
    });
  }

  function filterTerms({ query = "", type = "all", letter = "" } = {}) {
    const q = query.toLowerCase().trim();
    return (data?.terms || []).filter((t) => {
      if (type !== "all" && t.type !== type) return false;
      if (letter && !t.term.toLowerCase().startsWith(letter.toLowerCase())) return false;
      if (!q) return true;
      return (
        t.term.toLowerCase().includes(q)
        || (t.vi || "").toLowerCase().includes(q)
        || (t.short || "").toLowerCase().includes(q)
        || (t.packTitle || "").toLowerCase().includes(q)
      );
    });
  }

  function renderGlossaryPage(root, options = {}) {
    if (!root || !data) return;
    setupGlobalListeners();

    let state = {
      query: options.query || "",
      type: "all",
      letter: "",
      focusId: options.focusId || null,
    };

    function render() {
      const terms = filterTerms(state);
      const letters = "ABCDEFGHIJKLMNOPQRSTUVWXYZ".split("");
      const types = [
        { id: "all", label: "Tất cả" },
        { id: "pattern", label: "Patterns" },
        { id: "phrasal", label: "Phrasal verbs" },
        { id: "vocab", label: "Từ vựng truyện" },
        { id: "grammar", label: "Ngữ pháp" },
      ];

      const cards = terms
        .map((t) => {
          const focused = state.focusId === t.id ? " is-focused" : "";
          const epChips = (t.episodes || [])
            .slice(0, 3)
            .map(
              (ep) =>
                `<a class="glossary-ep-chip" href="#/read/${ep.seriesId}/${ep.num}">${escapeHtml(getSeriesTitle(ep.seriesId))} T${ep.num}</a>`
            )
            .join("");
          const related = (t.related || [])
            .map((rid) => getTerm(rid))
            .filter(Boolean)
            .slice(0, 3)
            .map((r) => `<button type="button" class="glossary-card-related-chip" data-term-id="${escapeHtml(r.id)}">${escapeHtml(r.term)}</button>`)
            .join("");

          return `
            <article class="glossary-card${focused}" id="term-${escapeHtml(t.id)}" data-term-id="${escapeHtml(t.id)}">
              <div class="glossary-card-head">
                <h2 class="glossary-card-term">${escapeHtml(t.term)}</h2>
                ${t.type ? `<span class="pack-chip">${escapeHtml(t.type)}</span>` : ""}
              </div>
              ${t.vi ? `<p class="glossary-card-vi">${escapeHtml(t.vi)}</p>` : ""}
              ${t.short ? `<p class="glossary-card-short">${escapeHtml(t.short)}</p>` : ""}
              ${t.example ? `<div class="glossary-card-example"><span class="glossary-card-section-label">Ví dụ</span>${escapeHtml(t.example)}</div>` : ""}
              ${t.long ? `<div class="glossary-card-long"><span class="glossary-card-section-label">Giải thích</span>${escapeHtml(t.long)}</div>` : ""}
              ${epChips ? `<div class="glossary-card-eps">${epChips}</div>` : ""}
              ${related ? `<div class="glossary-card-related">${related}</div>` : ""}
            </article>`;
        })
        .join("");

      root.innerHTML = `
        <div class="glossary-root">
          <header class="glossary-header page-header">
            <h1>📖 Bộ từ điển đầy đủ</h1>
            <p class="page-desc">${escapeHtml(data.meta?.subtitle || "")} · <strong>${terms.length}</strong> mục</p>
          </header>

          <div class="glossary-search-wrap">
            <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="11" cy="11" r="8"/><path d="m21 21-4.35-4.35"/></svg>
            <input type="search" class="glossary-search-input" placeholder="Tìm cụm từ, nghĩa tiếng Việt…" value="${escapeHtml(state.query)}" autocomplete="off">
            ${state.query ? `<button type="button" class="glossary-search-clear">✕</button>` : ""}
          </div>

          <div class="glossary-filters">
            <div class="glossary-filter-row">
              <span class="glossary-filter-label">Loại</span>
              <div class="glossary-filter-scroll">
                ${types.map((t) => `<button type="button" class="glossary-filter-pill ${state.type === t.id ? "active" : ""}" data-type="${t.id}">${t.label}</button>`).join("")}
              </div>
            </div>
            <div class="glossary-filter-row">
              <span class="glossary-filter-label">A–Z</span>
              <div class="glossary-letter-scroll">
                <button type="button" class="glossary-letter-pill ${!state.letter ? "active" : ""}" data-letter="">All</button>
                ${letters.map((l) => `<button type="button" class="glossary-letter-pill ${state.letter === l ? "active" : ""}" data-letter="${l}">${l}</button>`).join("")}
              </div>
            </div>
          </div>

          <p class="glossary-results-meta">Hiển thị <strong>${terms.length}</strong> / ${data.meta?.count || data.terms?.length || 0} mục</p>

          ${terms.length ? `<div class="glossary-grid">${cards}</div>` : `<div class="glossary-empty">Không tìm thấy — thử từ khóa khác hoặc bỏ bộ lọc chữ cái.</div>`}
        </div>`;

      const input = root.querySelector(".glossary-search-input");
      input?.addEventListener("input", (e) => {
        state.query = e.target.value;
        state.focusId = null;
        render();
        root.querySelector(".glossary-search-input")?.focus();
      });
      root.querySelector(".glossary-search-clear")?.addEventListener("click", () => {
        state.query = "";
        render();
      });
      root.querySelectorAll("[data-type]").forEach((btn) => {
        btn.addEventListener("click", () => {
          state.type = btn.dataset.type;
          render();
        });
      });
      root.querySelectorAll("[data-letter]").forEach((btn) => {
        btn.addEventListener("click", () => {
          state.letter = btn.dataset.letter;
          render();
        });
      });

      if (state.focusId) {
        const el = root.querySelector(`#term-${CSS.escape(state.focusId)}`);
        el?.scrollIntoView({ behavior: "smooth", block: "center" });
      }
    }

    render();
  }

  function searchTerms(query, limit = 8) {
    return filterTerms({ query }).slice(0, limit);
  }

  return {
    init,
    getTerm,
    findTerm,
    slugId,
    termButton,
    linkify,
    openPopover,
    closePopover,
    setupGlobalListeners,
    renderGlossaryPage,
    searchTerms,
  };
})();

/* English Vault: Tokyo Debug Chronicles — App */
const App = (() => {
  const $ = (s) => document.querySelector(s);
  const $$ = (s) => document.querySelectorAll(s);

  const ASSET_VERSION = "20250622-phrasal-us-v10";

  function toWebp(path) {
    if (!path || !/\.png$/i.test(path)) return path;
    return path.replace(/\.png$/i, ".webp");
  }

  /** Prefer WebP; PNG fallback via img onerror (see imgFallbackAttr). */
  function assetUrl(path, ext = "webp") {
    if (!path) return path;
    const filePath = ext === "webp" ? toWebp(path) : path;
    const sep = filePath.includes("?") ? "&" : "?";
    return `${filePath}${sep}v=${ASSET_VERSION}`;
  }

  function imgFallbackAttr() {
    return ' onerror="if(!this.dataset.fb){this.dataset.fb=1;this.src=this.src.replace(/\\.webp/i,\'.png\')}"';
  }

  let data = null;
  let roadmapData = null;
  let episodeGuides = null;
  let episodeView = "list";
  let activeFilter = "all";
  let searchFocus = 0;
  let readerState = null;
  let touchStartX = 0;

  const STORAGE = {
    get(key, fallback) {
      try { return JSON.parse(localStorage.getItem(key)) ?? fallback; }
      catch { return fallback; }
    },
    set(key, val) { localStorage.setItem(key, JSON.stringify(val)); },
  };

  const readEpisodes = () => STORAGE.get("readEpisodes", {});
  const bookmarks = () => STORAGE.get("bookmarks", []);
  const lastRead = () => STORAGE.get("lastRead", null);
  const theme = () => STORAGE.get("theme", "dark");

  const readHistory = () => STORAGE.get("readHistory", []);
  const activeRoadmapPath = () => STORAGE.get("activeRoadmapPath", "beginner");
  const setActiveRoadmapPath = (id) => STORAGE.set("activeRoadmapPath", id);

  function getRequiredEpisodes(step) {
    const s = getSeries(step.seriesId);
    if (!s) return [];
    const main = getMainEpisodes(s);
    if (!step.episodes || step.episodes === "all") return main.map((e) => e.num);
    return step.episodes.filter((n) => main.some((e) => e.num === n));
  }

  function getStepReadProgress(step) {
    const required = getRequiredEpisodes(step);
    if (!required.length) return { readCount: 0, total: 0, pct: 0, complete: false };
    const read = readEpisodes()[step.seriesId] || [];
    const readCount = required.filter((n) => read.includes(n)).length;
    return {
      readCount,
      total: required.length,
      pct: Math.round((readCount / required.length) * 100),
      complete: readCount >= required.length,
    };
  }

  function isStepPracticeDone() {
    return true;
  }

  function isStepComplete(step) {
    return getStepReadProgress(step).complete && isStepPracticeDone(step);
  }

  function flattenPathSteps(path) {
    return path.phases.flatMap((ph) => ph.steps.map((st) => ({ ...st, phase: ph })));
  }

  function getPathProgress(path) {
    const steps = flattenPathSteps(path);
    if (!steps.length) return { pct: 0, done: 0, total: steps.length, steps };
    const done = steps.filter(isStepComplete).length;
    return { pct: Math.round((done / steps.length) * 100), done, total: steps.length, steps };
  }

  function stepKey(step) {
    const ep = step.episodes ? step.episodes.join(",") : "all";
    return `${step.seriesId}:${ep}`;
  }

  function getNextRoadmapAction(pathId) {
    const path = roadmapData?.paths?.find((p) => p.id === pathId);
    if (!path) return null;

    for (const step of flattenPathSteps(path)) {
      const read = getStepReadProgress(step);
      const s = getSeries(step.seriesId);
      if (!s) continue;

      if (!read.complete) {
        const required = getRequiredEpisodes(step);
        const readSet = readEpisodes()[step.seriesId] || [];
        const nextNum = required.find((n) => !readSet.includes(n)) || required[0];
        return {
          type: "read",
          pathId,
          step,
          seriesId: step.seriesId,
          epNum: nextNum,
          label: `Đọc ${s.title} — Tập ${nextNum}`,
        };
      }

      if (step.practice === "boss" && !isStepPracticeDone(step)) {
        return {
          type: "read",
          pathId,
          step,
          seriesId: step.seriesId,
          epNum: getRequiredEpisodes(step).find((n) => !(readEpisodes()[step.seriesId] || []).includes(n)) || 1,
          label: `Đọc ${s.title}`,
        };
      }
    }

    return { type: "complete", pathId, label: "Hoàn thành lộ trình! 🎉" };
  }

  function continueRoadmap(pathId) {
    const action = getNextRoadmapAction(pathId || activeRoadmapPath());
    if (!action) return navigate("#/roadmap");
    if (action.type === "read") navigate(`#/read/${action.seriesId}/${action.epNum}`);
    else showToast("🎉 Bạn đã hoàn thành lộ trình này!");
  }

  function startLearning() {
    if (getReadTotal() === 0) navigate("#/roadmap");
    else continueRoadmap();
  }

  function markRead(seriesId, epNum) {
    const r = readEpisodes();
    if (!r[seriesId]) r[seriesId] = [];
    if (!r[seriesId].includes(epNum)) r[seriesId].push(epNum);
    STORAGE.set("readEpisodes", r);

    const now = Date.now();
    let history = readHistory().filter((h) => !(h.seriesId === seriesId && h.epNum === epNum));
    history.unshift({ seriesId, epNum, at: now });
    STORAGE.set("readHistory", history.slice(0, 50));

    STORAGE.set("lastRead", { seriesId, epNum, at: now });
    updateContinueBanner();
    updateReadStat();
  }

  function isRead(seriesId, epNum) {
    return (readEpisodes()[seriesId] || []).includes(epNum);
  }

  function getSeriesProgress(s) {
    return Math.round((getMainReadCount(s) / s.count) * 100);
  }

  function getSeries(id) {
    return data.series.find((s) => s.id === id);
  }

  function epLabel(ep) {
    if (ep.extra) return `Extra ${ep.extraNum}`;
    return `Tập ${ep.num}`;
  }

  function sortEpisodes(episodes) {
    const main = episodes.filter((e) => !e.extra).sort((a, b) => a.num - b.num);
    const extra = episodes.filter((e) => e.extra).sort((a, b) => a.extraNum - b.extraNum);
    return [...main, ...extra];
  }

  function getOrderedEpisodes(s) {
    return sortEpisodes(s.episodes);
  }

  function getMainEpisodes(s) {
    return s.episodes.filter((e) => !e.extra);
  }

  function getMainReadCount(s) {
    const mainNums = new Set(getMainEpisodes(s).map((e) => e.num));
    return (readEpisodes()[s.id] || []).filter((n) => mainNums.has(n)).length;
  }

  function seriesEpCountLabel(s) {
    return s.extraCount ? `${s.count} tập + ${s.extraCount} Extra` : `${s.count} tập`;
  }

  function getAllEpisodes() {
    return data.series.flatMap((s) =>
      getOrderedEpisodes(s).map((ep) => ({ ...ep, seriesId: s.id, seriesTitle: s.title, seriesColor: s.color }))
    );
  }

  function navigate(hash) {
    location.hash = hash;
    window.scrollTo({ top: 0, behavior: "smooth" });
  }

  function getRoute() {
    const parts = (location.hash.slice(1) || "/").split("/").filter(Boolean);
    return { parts };
  }

  function showToast(msg) {
    const t = $("#toast");
    t.textContent = msg;
    t.classList.add("show");
    t.classList.remove("hidden");
    clearTimeout(t._timer);
    t._timer = setTimeout(() => t.classList.remove("show"), 2800);
  }

  function animateCounter(el, target) {
    const duration = 1200;
    const start = performance.now();
    const from = 0;
    function tick(now) {
      const p = Math.min((now - start) / duration, 1);
      const ease = 1 - Math.pow(1 - p, 3);
      el.textContent = Math.round(from + (target - from) * ease);
      if (p < 1) requestAnimationFrame(tick);
    }
    requestAnimationFrame(tick);
  }

  function hideLoader() {
    const l = $("#loader");
    l.classList.add("done");
    setTimeout(() => l.remove(), 600);
  }

  /* ── Theme ── */
  function applyTheme(t) {
    document.documentElement.setAttribute("data-theme", t);
    STORAGE.set("theme", t);
  }

  function toggleTheme() {
    const next = document.documentElement.getAttribute("data-theme") === "dark" ? "light" : "dark";
    applyTheme(next);
    showToast(next === "dark" ? "🌙 Dark mode" : "☀️ Light mode");
  }

  /* ── Continue reading ── */
  function updateContinueBanner() {
    const lr = lastRead();
    const banner = $("#continue-banner");
    if (!lr) { banner.classList.add("hidden"); return; }

    const s = getSeries(lr.seriesId);
    if (!s) { banner.classList.add("hidden"); return; }

    const ep = s.episodes.find((e) => e.num === lr.epNum);
    if (!ep) { banner.classList.add("hidden"); return; }

    $("#continue-text").textContent = `${s.title} — ${epLabel(ep)}: ${ep.title}`;
    $("#continue-btn").onclick = () => navigate(`#/read/${lr.seriesId}/${lr.epNum}`);
    banner.classList.remove("hidden");
  }

  function dismissContinue() {
    STORAGE.set("lastRead", null);
    $("#continue-banner").classList.add("hidden");
  }

  function continueReading() {
    const lr = lastRead();
    if (lr) navigate(`#/read/${lr.seriesId}/${lr.epNum}`);
    else showToast("Chưa có lịch sử đọc — hãy chọn một tập!");
  }

  function startReading() {
    const lr = lastRead();
    if (lr) navigate(`#/read/${lr.seriesId}/${lr.epNum}`);
    else navigate("#/roadmap");
  }

  function getReadTotal() {
    return Object.values(readEpisodes()).reduce((n, arr) => n + arr.length, 0);
  }

  function updateReadStat(animate = false) {
    const total = getReadTotal();
    const el = $("#stat-read");
    if (!el) return;
    if (animate) animateCounter(el, total);
    else el.textContent = total;
  }

  /* ── Home ── */
  function renderHome() {
    showPage("home");
    const { series } = data;
    const total = series.reduce((n, s) => n + s.count + (s.extraCount || 0), 0);

    animateCounter($("#stat-series"), series.length);
    animateCounter($("#stat-episodes"), total);
    updateReadStat(true);

    const tags = ["all", ...new Set(series.map((s) => s.tag))];
    $("#filter-pills").innerHTML = tags
      .map((t) => `<button class="filter-pill ${t === activeFilter ? "active" : ""}" onclick="App.setFilter('${t}')">${t === "all" ? "Tất cả" : t}</button>`)
      .join("");

    renderSeriesGrid();
    renderSpotlight();
    renderRoadmapTeaser();
    updateHeroCTA();

    const totalEps = series.reduce((n, s) => n + s.count + (s.extraCount || 0), 0);
    const heroDesc = $("#hero-desc");
    if (heroDesc) {
      heroDesc.textContent = `${series.length} arc · ${totalEps} tập · Học tiếng Anh qua truyện tranh · Dev & cuộc sống ở Tokyo`;
    }
  }

  function updateHeroCTA() {
    const btn = $("#hero-primary-btn");
    if (!btn) return;
    const lr = lastRead();
    const readTotal = getReadTotal();
    if (readTotal === 0) {
      btn.textContent = "🗺️ Bắt đầu học";
      btn.onclick = () => navigate("#/roadmap");
    } else if (lr) {
      btn.textContent = "📖 Tiếp tục lộ trình";
      btn.onclick = () => continueRoadmap();
    } else {
      btn.textContent = "🗺️ Lộ trình học";
      btn.onclick = () => navigate("#/roadmap");
    }
  }

  function renderRoadmapTeaser() {
    const el = $("#roadmap-teaser");
    if (!el || !roadmapData?.paths?.length) return;

    const paths = roadmapData.paths.slice(0, 4);
    const cards = paths.map((p) => {
      const prog = getPathProgress(p);
      const action = getNextRoadmapAction(p.id);
      const isComplete = action?.type === "complete";
      return `
        <article class="roadmap-teaser-card" style="--path-color:${p.color}" onclick="App.selectRoadmapPath('${p.id}')">
          <div class="roadmap-teaser-ring" style="--path-color:${p.color};--pct:${prog.pct}">
            <div class="roadmap-ring-inner">
              <span class="roadmap-teaser-icon">${p.icon}</span>
            </div>
          </div>
          <div class="roadmap-teaser-body">
            <h3>${p.title}</h3>
            <p>${p.subtitle}</p>
            <span class="roadmap-teaser-meta">${prog.done}/${prog.total} bước · ${p.duration}</span>
          </div>
          <span class="roadmap-teaser-status ${isComplete ? "done" : prog.pct > 0 ? "active" : ""}">
            ${isComplete ? "✓ Xong" : prog.pct > 0 ? `${prog.pct}%` : "Bắt đầu"}
          </span>
        </article>`;
    }).join("");

    el.innerHTML = `
      <div class="roadmap-teaser-header">
        <div>
          <h2 class="section-title">🗺️ Lộ trình học</h2>
          <p class="roadmap-teaser-desc">Chưa biết đọc từ đâu? Chọn lộ trình — debug code, du lịch Nhật, sống ở Tokyo.</p>
        </div>
        <a href="#/roadmap" class="btn btn-ghost">Xem tất cả →</a>
      </div>
      <div class="roadmap-teaser-grid">${cards}</div>`;
  }

  function selectRoadmapPath(pathId) {
    setActiveRoadmapPath(pathId);
    navigate(`#/roadmap/${pathId}`);
  }

  function setFilter(tag) {
    activeFilter = tag;
    renderSeriesGrid();
    $$(".filter-pill").forEach((p) => p.classList.toggle("active", p.textContent === (tag === "all" ? "Tất cả" : tag)));
  }

  function renderSeriesGrid() {
    const filtered = activeFilter === "all"
      ? data.series
      : data.series.filter((s) => s.tag === activeFilter);

    $("#series-grid").innerHTML = filtered
      .map((s) => {
        const prog = getSeriesProgress(s);
        return `
        <article class="series-card" style="--series-color:${s.color}" onclick="App.navigate('#/series/${s.id}')">
          <div class="series-card-cover">
            <img src="${assetUrl(s.cover)}" alt="${s.title}" loading="lazy"${imgFallbackAttr()}>
            <span class="series-card-tag">${s.tag}</span>
          </div>
          <div class="series-card-body">
            <div class="series-card-top">
              <span class="series-icon">${s.icon}</span>
              <h2>${s.title}</h2>
            </div>
            <p>${s.desc}</p>
            <div class="series-card-footer">
              <span class="series-badge">${seriesEpCountLabel(s)} · ${prog}% đọc</span>
              <div class="series-card-progress">
                <div class="series-card-progress-fill" style="width:${prog}%"></div>
              </div>
            </div>
          </div>
        </article>`;
      })
      .join("");
  }

  function renderSpotlight() {
    const lr = lastRead();
    let s, ep;
    if (lr) {
      s = getSeries(lr.seriesId);
      ep = s?.episodes.find((e) => e.num === lr.epNum);
    }
    if (!s || !ep) {
      s = data.series[0];
      ep = s.episodes[0];
    }

    $("#spotlight").innerHTML = `
      <div class="spotlight-bg" style="background-image:url('${assetUrl(ep.image)}')"></div>
      <div class="spotlight-content" onclick="App.navigate('#/read/${s.id}/${ep.num}')">
        <div>
          <span class="spotlight-tag">${lr ? "📖 Tiếp tục đọc" : "⭐ Nổi bật"}</span>
          <h3>${s.title}</h3>
          <p>${epLabel(ep)}: ${ep.title}</p>
        </div>
        <button class="btn btn-primary btn-lg">Đọc ngay →</button>
      </div>`;
  }

  /* ── Series ── */
  let currentSeriesId = null;

  function setEpisodeView(view) {
    episodeView = view;
    $$(".view-btn").forEach((b) => b.classList.toggle("active", b.dataset.view === view));
    if (currentSeriesId) renderSeries(currentSeriesId);
  }

  function renderSeries(id) {
    const s = getSeries(id);
    if (!s) return renderHome();

    currentSeriesId = id;
    showPage("series");
    document.documentElement.style.setProperty("--accent", s.color);

    $("#series-cover").src = assetUrl(s.cover);
    $("#series-cover").onerror = () => {
      const el = $("#series-cover");
      if (!el.dataset.fb) {
        el.dataset.fb = "1";
        el.src = assetUrl(s.cover, "png");
      }
    };
    $("#series-tag").textContent = s.tag;
    $("#series-tag").style.color = s.color;
    $("#series-tag").style.background = `${s.color}18`;
    $("#series-hero-icon").textContent = s.icon;
    $("#series-hero-title").textContent = s.title;
    $("#series-hero-desc").textContent = s.desc;
    $("#series-breadcrumb").textContent = s.title;
    $("#series-ep-count").textContent = seriesEpCountLabel(s);
    const prog = getSeriesProgress(s);
    const readCount = getMainReadCount(s);
    $("#series-progress-text").textContent = `Đã đọc ${readCount}/${s.count}`;
    $("#series-progress-fill").style.width = `${prog}%`;
    $("#series-progress-fill").style.background = s.color;
    $("#series-hero").style.setProperty("--series-color", s.color);

    const ordered = getOrderedEpisodes(s);
    const firstUnread = ordered.find((e) => !e.extra && !isRead(s.id, e.num))
      || getMainEpisodes(s)[0]
      || ordered[0];
    $("#series-start-btn").onclick = () => navigate(`#/read/${s.id}/${firstUnread.num}`);
    $("#series-start-btn").textContent = readCount > 0 ? "Đọc tiếp →" : "Đọc từ đầu →";

    const list = $("#episode-list");
    list.className = `episode-list${episodeView === "grid" ? " grid-view" : ""}`;
    list.innerHTML = ordered
      .map((ep) => {
        const read = isRead(s.id, ep.num);
        const numLabel = ep.extra ? `E${ep.extraNum}` : String(ep.num).padStart(2, "0");
        return `
        <div class="episode-item ${read ? "read" : ""} ${ep.extra ? "episode-extra" : ""}" style="--series-color:${s.color}"
             onclick="App.navigate('#/read/${s.id}/${ep.num}')">
          ${episodeView === "grid" ? `<img class="ep-thumb" src="${assetUrl(ep.image)}" alt="" loading="lazy"${imgFallbackAttr()}>` : ""}
          <div class="ep-body" style="display:flex;align-items:center;gap:1rem;flex:1;${episodeView === "grid" ? "flex-direction:column;align-items:flex-start;gap:0.25rem" : ""}">
            <div class="ep-num ${ep.extra ? "ep-num-extra" : ""}">${numLabel}</div>
            <div>
              <div class="ep-title">${ep.title}${ep.extra ? ' <span class="ep-extra-badge">Extra</span>' : ""}</div>
              <div class="ep-subtitle">${epLabel(ep)}</div>
            </div>
          </div>
          ${read ? '<span class="read-check">✓</span>' : '<span class="ep-arrow">→</span>'}
        </div>`;
      })
      .join("");
  }

  /* ── Reader ── */
  function renderReader(seriesId, epNum) {
    const s = getSeries(seriesId);
    if (!s) return renderHome();

    const ordered = getOrderedEpisodes(s);
    const idx = ordered.findIndex((e) => e.num === epNum);
    if (idx === -1) return renderSeries(seriesId);

    const ep = ordered[idx];
    const prev = idx > 0 ? ordered[idx - 1] : null;
    const next = idx < ordered.length - 1 ? ordered[idx + 1] : null;

    showPage("reader");
    document.documentElement.style.setProperty("--accent", s.color);
    markRead(seriesId, epNum);

    $("#reader-ep-badge").textContent = ep.extra ? `${epLabel(ep)} (bonus)` : `Tập ${ep.num} / ${s.count}`;
    $("#reader-title").textContent = ep.title;
    $("#reader-series").textContent = s.title;
    $("#reader-breadcrumb-series").textContent = s.title;
    $("#reader-breadcrumb-series").href = `#/series/${s.id}`;
    $("#reader-breadcrumb-ep").textContent = epLabel(ep);

    const img = $("#comic-img");
    const skel = $("#comic-skeleton");
    const zoomImg = $("#zoom-img");
    img.classList.remove("loaded");
    skel.classList.remove("hidden");
    delete img.dataset.fb;
    delete zoomImg.dataset.fb;

    const finishComicLoad = () => {
      img.classList.add("loaded");
      skel.classList.add("hidden");
    };
    const revealIfCached = (el) => {
      if (el.complete && el.naturalWidth > 0) finishComicLoad();
    };

    img.onload = finishComicLoad;
    img.onerror = () => {
      if (!img.dataset.fb) {
        img.dataset.fb = "1";
        img.src = assetUrl(ep.image, "png");
        zoomImg.src = assetUrl(ep.image, "png");
        revealIfCached(img);
      }
    };
    img.alt = ep.title;
    img.src = assetUrl(ep.image);
    revealIfCached(img);

    zoomImg.onerror = () => {
      if (!zoomImg.dataset.fb) {
        zoomImg.dataset.fb = "1";
        zoomImg.src = assetUrl(ep.image, "png");
      }
    };
    zoomImg.src = assetUrl(ep.image);

    if (next) { const n = new Image(); n.src = assetUrl(next.image); }
    if (prev) { const p = new Image(); p.src = assetUrl(prev.image); }

    const pct = ((idx + 1) / ordered.length) * 100;
    $("#progress-fill").style.width = `${pct}%`;
    $("#progress-text").textContent = `${idx + 1} / ${ordered.length}`;

    const setNav = (btn, zone, target, disabled) => {
      btn.disabled = disabled;
      zone.disabled = disabled;
      const fn = () => target && navigate(`#/read/${s.id}/${target.num}`);
      btn.onclick = fn;
      zone.onclick = fn;
    };
    setNav($("#btn-prev"), $("#nav-zone-left"), prev, !prev);
    setNav($("#btn-next"), $("#nav-zone-right"), next, !next);

    const bm = bookmarks();
    const isBm = bm.some((b) => b.seriesId === seriesId && b.epNum === epNum);
    $("#btn-bookmark").classList.toggle("active", isBm);

    $("#thumb-scroll").innerHTML = ordered
      .map((e) => `
      <div class="thumb-item ${e.num === ep.num ? "active" : ""} ${isRead(s.id, e.num) ? "read" : ""} ${e.extra ? "thumb-extra" : ""}"
           onclick="App.navigate('#/read/${s.id}/${e.num}')">
        <img src="${assetUrl(e.image)}" alt="${epLabel(e)}" loading="lazy"${imgFallbackAttr()}>
        <div class="thumb-label">${epLabel(e)}</div>
      </div>`)
      .join("");

    const activeThumb = $("#thumb-scroll .thumb-item.active");
    if (activeThumb) activeThumb.scrollIntoView({ inline: "center", behavior: "smooth" });

    renderTakeaway(ep, seriesId);

    readerState = { seriesId, epNum, prev, next, ep, s };
    document.title = `${epLabel(ep)}: ${ep.title} — English Vault`;
  }

  function showPage(name) {
    ["home", "series", "reader", "bookmarks", "roadmap", "patterns", "glossary"].forEach((p) => {
      $(`#page-${p}`)?.classList.toggle("hidden", p !== name);
    });
    document.body.classList.toggle("reader-fullscreen", false);

    $("#nav-home")?.classList.toggle("active", name === "home");
    $("#nav-roadmap")?.classList.toggle("active", name === "roadmap");
    $("#nav-patterns")?.classList.toggle("active", name === "patterns");
    $("#nav-glossary")?.classList.toggle("active", name === "glossary");
    $("#nav-bookmarks")?.classList.toggle("active", name === "bookmarks");
    $$(".mobile-nav-item[data-nav]").forEach((el) => {
      el.classList.toggle("active", el.dataset.nav === name);
    });

    const titles = {
      home: "English Vault — Tokyo Debug Chronicles",
      roadmap: "Lộ trình học — English Vault",
      patterns: "Pattern Library — English Vault",
      glossary: "Từ điển Pattern — English Vault",
      bookmarks: "Thư viện — English Vault",
    };
    if (titles[name]) document.title = titles[name];
  }

  function renderPatterns(packId) {
    showPage("patterns");
    const root = $("#patterns-root");
    if (!root || typeof Learn === "undefined") return;
    if (packId) Learn.renderPackDetail(root, packId, data, navigate);
    else Learn.renderPatternsPage(root, data, navigate);
  }

  function openReviewMode(topic) {
    const modal = $("#review-modal");
    const ta = $("#review-prompt-text");
    if (!modal || !ta || typeof Learn === "undefined") return;
    const t = topic || (readerState ? `${readerState.ep.title} (Tập ${readerState.ep.num})` : "patterns vừa học");
    ta.value = Learn.reviewPrompt(t);
    modal.classList.remove("hidden");
  }

  function closeReviewMode() {
    $("#review-modal")?.classList.add("hidden");
  }

  async function copyReviewPrompt() {
    const ta = $("#review-prompt-text");
    if (!ta) return;
    try {
      await navigator.clipboard.writeText(ta.value);
      showToast("📋 Đã copy Review Mode prompt!");
    } catch {
      ta.select();
      showToast("Chọn và copy thủ công (Cmd+C)");
    }
  }

  /* ── Roadmap ── */
  function renderRoadmap(pathId) {
    showPage("roadmap");
    const root = $("#roadmap-root");
    if (!root || !roadmapData) return;

    const selectedId = pathId || activeRoadmapPath();
    const path = roadmapData.paths.find((p) => p.id === selectedId) || roadmapData.paths[0];
    if (path) setActiveRoadmapPath(path.id);

    const prog = getPathProgress(path);
    const nextAction = getNextRoadmapAction(path.id);
    const isComplete = nextAction?.type === "complete";

    const methodology = roadmapData.methodology.map((m) => `
      <div class="roadmap-method-card">
        <span class="roadmap-method-num">${m.step}</span>
        <span class="roadmap-method-icon">${m.icon}</span>
        <h4>${m.title}</h4>
        <p>${m.desc}</p>
      </div>`).join("");

    const pathTabs = roadmapData.paths.map((p) => {
      const pp = getPathProgress(p);
      return `
        <button class="roadmap-path-tab ${p.id === path.id ? "active" : ""}"
                style="--path-color:${p.color}"
                onclick="App.selectRoadmapPath('${p.id}')">
          <span class="roadmap-path-tab-icon">${p.icon}</span>
          <span class="roadmap-path-tab-info">
            <strong>${p.title}</strong>
            <small>${pp.pct}% · ${p.duration}</small>
          </span>
        </button>`;
    }).join("");

    let stepIdx = 0;
    const timeline = path.phases.map((phase) => {
      const phaseSteps = phase.steps.map((step) => {
        stepIdx += 1;
        const s = getSeries(step.seriesId);
        if (!s) return "";

        const read = getStepReadProgress(step);
        const practiceDone = isStepPracticeDone(step);
        const complete = isStepComplete(step);
        const isCurrent = !complete && nextAction?.step && stepKey(nextAction.step) === stepKey(step);
        const epCountLabel = step.episodes && step.episodes !== "all"
          ? `${step.episodes.length} tập chọn lọc`
          : seriesEpCountLabel(s);

        const required = getRequiredEpisodes(step);
        const readSet = readEpisodes()[step.seriesId] || [];
        const nextEp = required.find((n) => !readSet.includes(n));

        return `
          <article class="roadmap-step ${complete ? "done" : ""} ${isCurrent ? "current" : ""}"
                   style="--step-color:${s.color}">
            <div class="roadmap-step-node">
              <span class="roadmap-step-num">${complete ? "✓" : stepIdx}</span>
            </div>
            <div class="roadmap-step-card">
              <div class="roadmap-step-cover">
                <img src="${assetUrl(s.cover)}" alt="" loading="lazy"${imgFallbackAttr()}>
                <span class="roadmap-step-icon">${s.icon}</span>
              </div>
              <div class="roadmap-step-content">
                <div class="roadmap-step-header">
                  <span class="roadmap-step-tag">${s.tag}</span>
                  ${isCurrent ? '<span class="roadmap-step-current">📍 Đang học</span>' : ""}
                  ${complete ? '<span class="roadmap-step-done-badge">Hoàn thành</span>' : ""}
                </div>
                <h3>${s.title}</h3>
                <p class="roadmap-step-desc">${step.tip || s.desc}</p>
                <div class="roadmap-step-meta">
                  <span>${epCountLabel}</span>
                  <span>·</span>
                  <span>Đã đọc ${read.readCount}/${read.total}</span>
                </div>
                <div class="roadmap-step-progress">
                  <div class="roadmap-step-progress-fill" style="width:${read.pct}%;background:${s.color}"></div>
                </div>
                <div class="roadmap-step-actions">
                  <button class="btn btn-primary btn-sm"
                    onclick="event.stopPropagation();App.navigate('#/read/${s.id}/${nextEp || s.episodes[0].num}')">
                    ${read.complete ? "Đọc lại" : read.readCount > 0 ? "Đọc tiếp →" : "Bắt đầu đọc →"}
                  </button>
                  <button class="btn btn-ghost btn-sm"
                    onclick="event.stopPropagation();App.navigate('#/series/${s.id}')">
                    Xem arc
                  </button>
                </div>
              </div>
            </div>
          </article>`;
      }).join("");

      return `
        <div class="roadmap-phase">
          <div class="roadmap-phase-header">
            <h3>${phase.title}</h3>
            <p>${phase.desc}</p>
          </div>
          <div class="roadmap-phase-steps">${phaseSteps}</div>
        </div>`;
    }).join("");

    root.innerHTML = `
      <nav class="breadcrumb" aria-label="Breadcrumb">
        <a href="#/">Trang chủ</a>
        <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="m9 18 6-6-6-6"/></svg>
        <span>Lộ trình học</span>
      </nav>

      <div class="roadmap-hero">
        <div class="roadmap-hero-badge">🎓 Hướng dẫn học</div>
        <h1>${roadmapData.meta.title}</h1>
        <p>${roadmapData.meta.subtitle}</p>
        <div class="roadmap-methodology">${methodology}</div>
      </div>

      <div class="roadmap-path-tabs">${pathTabs}</div>

      <div class="roadmap-path-overview" style="--path-color:${path.color}">
        <div class="roadmap-path-overview-left">
          <span class="roadmap-path-big-icon">${path.icon}</span>
          <div>
            <h2>${path.title}</h2>
            <p>${path.desc}</p>
            <div class="roadmap-path-tags">
              <span class="roadmap-path-tag">${path.audience || path.subtitle}</span>
              <span class="roadmap-path-tag">⏱ ${path.duration}</span>
              <span class="roadmap-path-tag">${prog.total} bước</span>
            </div>
          </div>
        </div>
        <div class="roadmap-path-overview-right">
          <div class="roadmap-big-progress" style="--path-color:${path.color};--pct:${prog.pct}">
            <div class="roadmap-big-ring"><div class="roadmap-ring-inner"></div></div>
            <div class="roadmap-big-pct">
              <strong>${prog.pct}%</strong>
              <small>${prog.done}/${prog.total}</small>
            </div>
          </div>
          ${!isComplete ? `
            <button class="btn btn-primary btn-lg roadmap-continue-btn"
              onclick="App.continueRoadmap('${path.id}')">
              ${nextAction?.type === "boss" ? "⚔️ " : "📖 "}${nextAction?.label || "Tiếp tục"} →
            </button>` : `
            <div class="roadmap-complete-badge">
              <span>🎉</span>
              <strong>Hoàn thành lộ trình!</strong>
              <button class="btn btn-ghost btn-sm" onclick="App.navigate('#/profile')">Xem hồ sơ →</button>
            </div>`}
        </div>
      </div>

      <div class="roadmap-timeline">${timeline}</div>

      <div class="roadmap-footer-tip">
        <span>💡</span>
        <p><strong>Mẹo:</strong> Đọc hết tập → chú ý phần ENGLISH FOCUS → luyện đọc to và áp dụng vào công việc thật.</p>
      </div>`;
  }

  /* ── Search ── */
  function openSearch() {
    $("#search-modal").classList.remove("hidden");
    const input = $("#search-input");
    input.value = "";
    input.focus();
    renderSearchResults("");
    searchFocus = 0;
  }

  function closeSearch() {
    $("#search-modal").classList.add("hidden");
  }

  function renderSearchResults(q) {
    const results = $("#search-results");
    const query = q.toLowerCase().trim();
    let html = "";
    let idx = 0;

    const items = getAllEpisodes().filter((ep) => {
      if (!query) return true;
      const focusMatch = (ep.englishFocus || []).some(
        (f) => f.phrase?.toLowerCase().includes(query) || (f.meaning || "").toLowerCase().includes(query)
      );
      return ep.title.toLowerCase().includes(query)
        || ep.seriesTitle.toLowerCase().includes(query)
        || `tập ${ep.num}`.includes(query)
        || (ep.extra && `extra ${ep.extraNum}`.includes(query))
        || focusMatch;
    }).slice(0, query ? 14 : 20);

    if (items.length) {
      html += `<div class="search-section-label">📚 Tập truyện</div>`;
      html += items
        .map((ep) => {
          const i = idx++;
          return `
          <div class="search-item ${i === searchFocus ? "focused" : ""}" data-idx="${i}"
               onclick="App.navigate('#/read/${ep.seriesId}/${ep.num}');App.closeSearch()">
            <img src="${assetUrl(ep.image)}" alt=""${imgFallbackAttr()}>
            <div class="search-item-info">
              <div class="search-item-series">${ep.seriesTitle} · ${epLabel(ep)}</div>
              <div class="search-item-title">${ep.title}</div>
            </div>
          </div>`;
        })
        .join("");
    }

    if (typeof Glossary !== "undefined" && query) {
      const terms = Glossary.searchTerms(query, 8);
      if (terms.length) {
        html += `<div class="search-section-label">📖 Từ điển</div>`;
        html += terms
          .map((t) => {
            const i = idx++;
            return `
            <div class="search-item search-item-glossary ${i === searchFocus ? "focused" : ""}" data-idx="${i}"
                 onclick="App.navigate('#/glossary/${t.id}');App.closeSearch()">
              <span class="search-glossary-icon">📖</span>
              <div class="search-item-info">
                <div class="search-item-series">Từ điển Pattern</div>
                <div class="search-item-title">${t.term}${t.vi ? ` — ${t.vi}` : ""}</div>
              </div>
            </div>`;
          })
          .join("");
      }
    }

    if (!html) {
      results.innerHTML = `<div class="search-empty">${query ? "Không tìm thấy kết quả" : "Gõ tên tập, chủ đề hoặc thuật ngữ (XSS, JWT…)…"}</div>`;
      return;
    }

    results.innerHTML = html;
  }

  /* ── Bookmarks page ── */
  function getRecentHistory(limit = 12) {
    return readHistory()
      .map((h) => {
        const s = getSeries(h.seriesId);
        const ep = s?.episodes.find((e) => e.num === h.epNum);
        return s && ep ? { seriesId: h.seriesId, epNum: h.epNum, ep, s, at: h.at } : null;
      })
      .filter(Boolean)
      .slice(0, limit);
  }

  function renderLibraryItem({ seriesId, epNum, ep, s }, opts = {}) {
    const removable = opts.removable ? `onclick="event.stopPropagation();App.removeBookmark('${seriesId}',${epNum})"` : "";
    return `
      <article class="library-item" style="--series-color:${s.color}"
               onclick="App.navigate('#/read/${seriesId}/${epNum}')">
        <img src="${assetUrl(ep.image)}" alt="" loading="lazy" decoding="async"${imgFallbackAttr()}>
        <div class="library-item-body">
          <div class="library-item-series">${s.title} · ${epLabel(ep)}</div>
          <div class="library-item-title">${ep.title}</div>
        </div>
        ${opts.removable ? `<button class="library-remove" title="Bỏ đánh dấu" ${removable}>✕</button>` : ""}
      </article>`;
  }

  function renderEmptyLibrary(msg) {
    return `<div class="library-empty">${msg}</div>`;
  }

  function renderBookmarks() {
    showPage("bookmarks");
    const bm = bookmarks();

    $("#bookmarks-list").innerHTML = bm.length
      ? bm.map((b) => {
          const s = getSeries(b.seriesId);
          const ep = s?.episodes.find((e) => e.num === b.epNum);
          if (!s || !ep) return "";
          return renderLibraryItem({ seriesId: b.seriesId, epNum: b.epNum, ep, s }, { removable: true });
        }).join("")
      : renderEmptyLibrary("Chưa có tập nào được đánh dấu — nhấn ⭐ khi đọc để lưu lại.");

    const history = getRecentHistory();
    $("#history-list").innerHTML = history.length
      ? history.map((item) => renderLibraryItem(item)).join("")
      : renderEmptyLibrary("Chưa có lịch sử đọc — hãy bắt đầu một tập truyện!");
  }

  function removeBookmark(seriesId, epNum) {
    let bm = bookmarks();
    bm = bm.filter((b) => !(b.seriesId === seriesId && b.epNum === epNum));
    STORAGE.set("bookmarks", bm);
    if (readerState?.seriesId === seriesId && readerState?.epNum === epNum) {
      $("#btn-bookmark").classList.remove("active");
    }
    showToast("Đã bỏ đánh dấu");
    renderBookmarks();
  }

  function mdInline(text) {
    if (!text) return "";
    return String(text)
      .replace(/\*\*(.+?)\*\*/g, "<strong>$1</strong>")
      .replace(/「(.+?)」/g, "<em>$1</em>");
  }

  function getEpisodeGuide(seriesId, epNum) {
    return episodeGuides?.guides?.[`${seriesId}/${epNum}`] || null;
  }

  function speakerTone(speaker) {
    const s = (speaker || "").split("(")[0].trim().toLowerCase();
    if (s === "nam") return "nam";
    if (s === "agent" || s === "landlord") return "agent";
    if (s === "kenji" || s === "aoi" || s === "linh") return "team";
    if (s === "recruiter" || s === "interviewer" || s === "manager" || s === "pm") return "pro";
    return "other";
  }

  function termBtn(text) {
    return typeof Glossary !== "undefined"
      ? Glossary.termButton(text)
      : `<strong>${text}</strong>`;
  }

  function bindEpisodeGuideTabs(root) {
    if (!root) return;
    const tabs = root.querySelectorAll(".eg-tab");
    const panels = root.querySelectorAll(".eg-panel");
    tabs.forEach((tab) => {
      tab.addEventListener("click", () => {
        const id = tab.dataset.tab;
        tabs.forEach((t) => t.classList.toggle("active", t === tab));
        panels.forEach((p) => p.classList.toggle("active", p.dataset.panel === id));
      });
    });
  }

  function renderEpisodeGuide(guide, ep, recap) {
    const dlg = guide.dialogueLines || [];
    const phrases = guide.phrases || [];
    const vocab = guide.extraVocab || [];
    const grammar = guide.grammar || [];
    const focusCount = dlg.filter((d) => d.isFocus).length;

    const dialogueHtml = dlg.length
      ? `<div class="dlg-timeline">${dlg.map((d, i) => {
          const tone = speakerTone(d.speaker);
          const focusBadge = d.isFocus ? `<span class="dlg-focus-pill">Focus</span>` : "";
          const wordsHtml = d.words?.length
            ? `<div class="dlg-chips">${d.words.map((w) =>
                `<span class="dlg-chip" title="${w.note}"><span class="dlg-chip-en">${w.word}</span><span class="dlg-chip-vi">${w.note}</span></span>`
              ).join("")}</div>`
            : "";
          const grammarHtml = d.grammarHint
            ? `<details class="dlg-grammar-fold"><summary>Ngữ pháp</summary><p>${mdInline(d.grammarHint)}</p></details>`
            : "";
          return `
          <article class="dlg-bubble dlg-bubble-${tone}${d.isFocus ? " dlg-bubble-focus" : ""}">
            <div class="dlg-bubble-meta">
              <span class="dlg-panel">Panel ${d.panel ?? i + 1}</span>
              <span class="dlg-speaker">${d.speaker || "N/A"}</span>
              ${focusBadge}
            </div>
            <blockquote class="dlg-quote">${termBtn(d.en)}</blockquote>
            <p class="dlg-vi">${d.vi || ""}</p>
            ${wordsHtml}
            ${grammarHtml}
          </article>`;
        }).join("")}</div>`
      : "";

    const phrasesHtml = phrases.length
      ? `<div class="pattern-stack">${phrases.map((p, i) => `
          <article class="pattern-card">
            <div class="pattern-card-top">
              <span class="pattern-num">${i + 1}</span>
              <div class="pattern-phrase">${termBtn(p.phrase)}</div>
            </div>
            <p class="pattern-meaning">${p.meaning || ""}</p>
            <div class="pattern-meta">
              <div><span class="pattern-label">Khi nào</span><p>${p.whenToUse || "—"}</p></div>
              <div><span class="pattern-label">Cấu trúc</span><p><code>${p.structure || p.phrase}</code></p></div>
            </div>
            <div class="pattern-example">
              <span class="pattern-label">Ví dụ trong tập</span>
              <p>"${p.exampleEn || p.phrase}"</p>
            </div>
          </article>`).join("")}</div>`
      : `<p class="eg-empty">Chưa có English Focus cho tập này.</p>`;

    const vocabHtml = vocab.length
      ? `<div class="vocab-grid">${vocab.map((v) => `
          <div class="vocab-row">
            <span class="vocab-term">${termBtn(v.phrase)}</span>
            <span class="vocab-meaning">${v.meaning || ""}</span>
          </div>`).join("")}</div>`
      : `<p class="eg-empty">Không có từ vựng phụ thêm.</p>`;

    const grammarHtml = grammar.length
      ? `<div class="grammar-stack">${grammar.map((g, i) => `
          <details class="grammar-fold"${i === 0 ? " open" : ""}>
            <summary class="grammar-fold-title">${g.title}</summary>
            <div class="grammar-fold-body">
              <p class="grammar-rule">${mdInline(g.rule)}</p>
              ${g.exampleGood ? `<div class="grammar-good"><span>✓</span> ${g.exampleGood}</div>` : ""}
              ${g.exampleBad ? `<div class="grammar-bad"><span>✗</span> ${g.exampleBad}</div>` : ""}
              ${g.beginnerNote ? `<p class="grammar-note">${mdInline(g.beginnerNote)}</p>` : `<p class="grammar-note">${mdInline(g.explain)}</p>`}
            </div>
          </details>`).join("")}</div>`
      : `<p class="eg-empty">Không có mục ngữ pháp riêng cho tập này.</p>`;

    const practiceHtml = guide.practiceSteps?.length
      ? `<div class="eg-practice">
          <h4 class="eg-practice-title">Luyện tập</h4>
          <ol class="eg-practice-steps">${guide.practiceSteps.map((s) => `<li>${s}</li>`).join("")}</ol>
          <button class="btn btn-primary btn-sm" type="button" onclick="App.openReviewMode('${ep.title.replace(/'/g, "\\'")}')">Mở Review Mode</button>
        </div>`
      : "";

    return `
      <div class="episode-guide" data-episode-guide>
        <div class="eg-hero">
          <div class="eg-hero-main">
            <span class="eg-ep-badge">Tập ${ep.num}</span>
            <p class="eg-hero-desc">${mdInline(guide.summary)}</p>
          </div>
          <div class="eg-stats">
            <div class="eg-stat"><strong>${dlg.length}</strong><span>câu hội thoại</span></div>
            <div class="eg-stat"><strong>${phrases.length}</strong><span>pattern</span></div>
            <div class="eg-stat"><strong>${vocab.length}</strong><span>từ vựng</span></div>
            ${focusCount ? `<div class="eg-stat eg-stat-focus"><strong>${focusCount}</strong><span>English Focus</span></div>` : ""}
          </div>
          ${recap ? `<details class="eg-recap-fold"><summary>Tóm tắt câu chuyện</summary><p>${mdInline(recap)}</p></details>` : ""}
        </div>

        <nav class="eg-tabs" role="tablist">
          <button type="button" class="eg-tab active" data-tab="dialogue" role="tab">💬 Hội thoại</button>
          <button type="button" class="eg-tab" data-tab="patterns" role="tab">🗣️ Pattern</button>
          <button type="button" class="eg-tab" data-tab="vocab" role="tab">📚 Từ vựng</button>
          <button type="button" class="eg-tab" data-tab="grammar" role="tab">📐 Ngữ pháp</button>
        </nav>

        <div class="eg-panels">
          <section class="eg-panel active" data-panel="dialogue" role="tabpanel">
            <p class="eg-panel-intro">Mỗi câu bám panel trong ảnh truyện — đọc EN, hiểu VI, học từ/cụm bên dưới.</p>
            ${dialogueHtml}
          </section>
          <section class="eg-panel" data-panel="patterns" role="tabpanel">
            <p class="eg-panel-intro">${guide.phrasesDerived ? "Pattern gợi ý từ pack phù hợp tập này." : "Pattern highlight trong khung ENGLISH FOCUS ở cuối ảnh truyện."}</p>
            ${phrasesHtml}
          </section>
          <section class="eg-panel" data-panel="vocab" role="tabpanel">
            <p class="eg-panel-intro">Từ/cụm hay gặp trong hội thoại — bấm để tra từ điển.</p>
            ${vocabHtml}
          </section>
          <section class="eg-panel" data-panel="grammar" role="tabpanel">
            <p class="eg-panel-intro">Giải thích ngữ pháp gắn với câu trong tập — cho người mới học.</p>
            ${grammarHtml}
          </section>
        </div>

        ${practiceHtml}
        ${guide.realLifeTip ? `<aside class="eg-tip"><span class="eg-tip-icon">💡</span><p>${guide.realLifeTip}</p></aside>` : ""}
        <p class="takeaway-glossary-link">Tra thêm: <a href="#/glossary" onclick="App.navigate('#/glossary')">Từ điển đầy đủ</a></p>
      </div>`;
  }

  function renderTakeaway(ep, seriesId) {
    const panel = $("#takeaway-panel");
    const list = $("#takeaway-list");
    const summary = $("#takeaway-summary");
    const twist = $("#takeaway-twist");
    const slogan = $("#takeaway-slogan");
    const quizBtn = $("#takeaway-quiz-btn");
    const guide = seriesId ? getEpisodeGuide(seriesId, ep.num) : null;
    const focus = ep.englishFocus || [];
    const points = ep.takeaways || [];
    const quote = ep.slogan || "";
    const recap = guide?.storyRecap || ep.summary || "";
    const twistText = ep.twist || "";

    panel.classList.remove("hidden");
    summary.classList.add("hidden");
    twist.classList.add("hidden");
    slogan.classList.add("hidden");
    if (quizBtn) quizBtn.classList.add("hidden");

    if (guide) {
      list.innerHTML = renderEpisodeGuide(guide, ep, recap);
      bindEpisodeGuideTabs(list.querySelector("[data-episode-guide]"));
      list.classList.remove("hidden");
    } else if (focus.length) {
      list.innerHTML = `<ul class="takeaway-simple-list">${focus
        .map((f) => {
          const term = typeof Glossary !== "undefined" ? Glossary.termButton(f.phrase) : `<strong>${f.phrase}</strong>`;
          return `<li>${term}${f.meaning ? ` <span class="focus-meaning">= ${f.meaning}</span>` : ""}</li>`;
        })
        .join("")}</ul>`;
      list.classList.remove("hidden");
    } else if (points.length) {
      list.innerHTML = `<ul class="takeaway-simple-list">${points.map((t) => `<li>${t}</li>`).join("")}</ul>`;
      list.classList.remove("hidden");
    } else {
      list.innerHTML = `<li class="focus-hint">💡 Xem phần <strong>ENGLISH FOCUS</strong> ở cuối ảnh truyện để học cụm từ hôm nay.</li>`;
      list.classList.remove("hidden");
    }

    if (recap && !guide) {
      summary.innerHTML = mdInline(recap);
      summary.classList.remove("hidden");
    }
    if (twistText) {
      twist.innerHTML = `<strong>Twist:</strong> ${twistText}`;
      twist.classList.remove("hidden");
    }
    if (quote) {
      slogan.textContent = `"${quote}"`;
      slogan.classList.remove("hidden");
    }

    const extra = $("#takeaway-extra");
    if (!extra) return;

    const packs = ep.packs || [];
    const prompts = ep.practicePrompts || [];
    const mistakes = ep.commonMistakes || [];
    const hook = ep.hook || "";

    let html = "";

    if (packs.length) {
      html += `<div class="learn-section"><h4>📦 Pattern packs</h4><div class="pack-chips">${packs
        .map((id) => `<a href="#/patterns/${id}" class="pack-chip">${id.replace(/_/g, " ")}</a>`)
        .join("")}</div></div>`;
    }

    if (prompts.length && !guide) {
      html += `<div class="learn-section"><h4>✍️ Try it yourself</h4><ul class="practice-list">${prompts
        .map((p) => `<li>${p}</li>`)
        .join("")}</ul>
        <button class="btn btn-ghost btn-sm" type="button" onclick="App.openReviewMode('${ep.title.replace(/'/g, "\\'")}')">🔄 Luyện với Review Mode</button></div>`;
    }

    if (mistakes.length && !(guide?.grammar?.length)) {
      html += `<div class="learn-section"><h4>⚠️ Lỗi thường gặp</h4>${mistakes
        .map(
          (m) =>
            `<div class="mistake-card"><span class="mistake-wrong">✗ ${m.wrong}</span><span class="mistake-correct">✓ ${m.correct}</span><span class="mistake-why">${m.why}</span></div>`
        )
        .join("")}</div>`;
    }

    if (hook) {
      html += `<p class="episode-hook">➡️ ${hook}</p>`;
    }

    extra.innerHTML = html;

    if (typeof Glossary !== "undefined") Glossary.setupGlobalListeners();
  }

  /* ── Bookmarks ── */
  function toggleBookmark() {
    if (!readerState) return;
    const { seriesId, epNum, ep, s } = readerState;
    let bm = bookmarks();
    const key = `${seriesId}-${epNum}`;
    const exists = bm.findIndex((b) => b.seriesId === seriesId && b.epNum === epNum);

    if (exists >= 0) {
      bm.splice(exists, 1);
      showToast("Đã bỏ đánh dấu");
      $("#btn-bookmark").classList.remove("active");
    } else {
      bm.push({ seriesId, epNum, title: ep.title, seriesTitle: s.title });
      showToast("⭐ Đã đánh dấu tập này");
      $("#btn-bookmark").classList.add("active");
    }
    STORAGE.set("bookmarks", bm);
  }

  /* ── Share ── */
  async function shareEpisode() {
    if (!readerState) return;
    const url = `${location.origin}${location.pathname}#/read/${readerState.seriesId}/${readerState.epNum}`;
    const text = `${readerState.s.title} — Tập ${readerState.epNum}: ${readerState.ep.title}`;
    try {
      if (navigator.share) {
        await navigator.share({ title: text, url });
      } else {
        await navigator.clipboard.writeText(url);
        showToast("📋 Đã copy link!");
      }
    } catch {
      showToast("Không thể chia sẻ");
    }
  }

  /* ── Zoom & Fullscreen ── */
  function openZoom() {
    $("#zoom-overlay").classList.remove("hidden");
    document.body.style.overflow = "hidden";
  }

  function closeZoom() {
    $("#zoom-overlay").classList.add("hidden");
    document.body.style.overflow = "";
  }

  function toggleFullscreen() {
    document.body.classList.toggle("reader-fullscreen");
    const on = document.body.classList.contains("reader-fullscreen");
    showToast(on ? "⛶ Chế độ đọc" : "Thoát chế độ đọc");
  }

  function openShortcuts() {
    $("#shortcuts-modal").classList.remove("hidden");
  }

  function closeShortcuts() {
    $("#shortcuts-modal").classList.add("hidden");
  }

  /* ── Quiz ── */
  function quizNavigate(hash, rerenderOnly) {
    if (rerenderOnly) {
      const session = Quiz.getSession();
      if (session?.mode === "boss") renderQuizBoss(session.seriesId, true);
      else renderQuizPlay(true);
      return;
    }
    if (hash) navigate(hash);
    else router();
  }

  function renderProfile() {
    showPage("profile");
    const root = $("#profile-root");
    if (!root || typeof Quiz === "undefined") return;
    root.innerHTML = Quiz.renderProfileHTML();
    Quiz.bindProfileEvents(root);
  }

  function renderQuizHub() {
    showPage("quiz");
    const root = $("#quiz-root");
    if (!root || typeof Quiz === "undefined") return;
    root.innerHTML = renderQuizBreadcrumb() + Quiz.renderHubHTML();
    Quiz.bindHubEvents(root, (h) => navigate(h));
  }

  function renderQuizBreadcrumb() {
    return `<nav class="breadcrumb quiz-breadcrumb" aria-label="Breadcrumb">
      <a href="#/">Trang chủ</a>
      <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="m9 18 6-6-6-6"/></svg>
      <span>Quiz ôn tập</span>
    </nav>`;
  }

  function renderQuizBoss(seriesId, rerenderOnly = false) {
    if (!rerenderOnly) showPage("quiz");
    const root = $("#quiz-root");
    if (!root || typeof Quiz === "undefined") return;

    const session = Quiz.getSession();
    if (session?.mode === "boss" && session.seriesId === seriesId) {
      root.innerHTML = renderQuizBreadcrumb() + Quiz.renderPlayHTML();
      Quiz.bindPlayEvents(root, quizNavigate);
      return;
    }

    if (session) Quiz.endSession();

    root.innerHTML = renderQuizBreadcrumb() + Quiz.renderBossIntroHTML(seriesId);
    Quiz.bindBossIntroEvents(root, seriesId, () => {
      const result = Quiz.startBossBattle(seriesId);
      if (result?.error) {
        showToast(result.error);
        return;
      }
      root.innerHTML = renderQuizBreadcrumb() + Quiz.renderPlayHTML();
      Quiz.bindPlayEvents(root, quizNavigate);
    });
  }

  function renderQuizPlay(rerenderOnly = false) {
    if (!rerenderOnly) showPage("quiz");
    const root = $("#quiz-root");
    if (!root || typeof Quiz === "undefined") return;

    const session = Quiz.getSession();
    if (!session && !rerenderOnly) {
      const { parts } = getRoute();
      let mode = parts[2] || "quick";
      let seriesId = null;
      if (parts[2] === "series" && parts[3]) {
        mode = "series";
        seriesId = parts[3];
      }
      const result = Quiz.startSession(mode, seriesId);
      if (result?.error) {
        root.innerHTML = renderQuizBreadcrumb() + `
          <div class="quiz-empty-state">
            <p>${result.error}</p>
            <button class="btn btn-primary" onclick="App.navigate('#/quiz')">← Về Quiz hub</button>
          </div>`;
        showToast(result.error);
        return;
      }
    }

    root.innerHTML = renderQuizBreadcrumb() + Quiz.renderPlayHTML();
    Quiz.bindPlayEvents(root, quizNavigate);
  }

  function startEpisodeQuiz(seriesId, epNum) {
    if (typeof Quiz === "undefined") return;
    const pool = Quiz.filterQuestions("series", seriesId).filter(
      (q) => q.episodeNum === epNum
    );
    if (!pool.length) {
      showToast("Chưa có quiz cho tập này — thử quiz cả bộ");
      navigate(`#/quiz/play/series/${seriesId}`);
      return;
    }
    Quiz.startCustomSession(pool.slice(0, Math.min(pool.length, 8)), "episode", seriesId);
    navigate(`#/quiz/play/episode/${seriesId}/${epNum}`);
  }

  function renderEpisodeQuiz(seriesId, epNum) {
    if (!Quiz.getSession()) {
      const pool = Quiz.filterQuestions("series", seriesId).filter(
        (q) => q.episodeNum === parseInt(epNum, 10)
      );
      Quiz.startCustomSession(pool.slice(0, Math.min(pool.length, 8)), "episode", seriesId);
    }
    showPage("quiz");
    const root = $("#quiz-root");
    if (!root) return;
    root.innerHTML = renderQuizBreadcrumb() + Quiz.renderPlayHTML();
    Quiz.bindPlayEvents(root, quizNavigate);
  }

  /* ── Glossary page ── */
  function renderGlossary(termId) {
    if (typeof Glossary !== "undefined") Glossary.closePopover();
    showPage("glossary");
    const root = $("#glossary-root");
    if (!root || typeof Glossary === "undefined") return;
    Glossary.setupGlobalListeners();
    const term = termId ? Glossary.getTerm(termId) : null;
    Glossary.renderGlossaryPage(root, {
      focusId: term?.id || null,
      query: term && termId ? term.term : "",
    });
  }

  /* ── Router ── */
  function router() {
    const { parts } = getRoute();
    if (parts[0] === "series" && parts[1]) renderSeries(parts[1]);
    else if (parts[0] === "read" && parts[1] && parts[2]) renderReader(parts[1], parseInt(parts[2], 10));
    else if (parts[0] === "bookmarks") renderBookmarks();
    else if (parts[0] === "roadmap") renderRoadmap(parts[1]);
    else if (parts[0] === "patterns") renderPatterns(parts[1]);
    else if (parts[0] === "glossary") renderGlossary(parts[1]);
    else renderHome();
  }

  /* ── Keyboard ── */
  function onKeydown(e) {
    const tag = e.target.tagName;
    const inInput = tag === "INPUT" || tag === "TEXTAREA";

    if (e.key === "/" && !inInput) { e.preventDefault(); openSearch(); return; }
    if (e.key === "?" && !inInput) { e.preventDefault(); openShortcuts(); return; }

    if ($("#search-modal").classList.contains("hidden") === false) {
      if (e.key === "Escape") { closeSearch(); return; }
      if (e.key === "ArrowDown" || e.key === "ArrowUp") {
        e.preventDefault();
        const items = $$(".search-item");
        if (!items.length) return;
        searchFocus = e.key === "ArrowDown"
          ? Math.min(searchFocus + 1, items.length - 1)
          : Math.max(searchFocus - 1, 0);
        items.forEach((el, i) => el.classList.toggle("focused", i === searchFocus));
        items[searchFocus]?.scrollIntoView({ block: "nearest" });
        return;
      }
      if (e.key === "Enter") {
        const focused = $(".search-item.focused");
        if (focused) focused.click();
        return;
      }
    }

    if ($("#review-modal")?.classList.contains("hidden") === false) {
      if (e.key === "Escape") closeReviewMode();
      return;
    }

    if ($("#shortcuts-modal").classList.contains("hidden") === false) {
      if (e.key === "Escape") closeShortcuts();
      return;
    }

    if ($("#zoom-overlay").classList.contains("hidden") === false) {
      if (e.key === "Escape") closeZoom();
      return;
    }

    if (!readerState || $("#page-reader").classList.contains("hidden")) return;

    if (e.key === "ArrowLeft" && readerState.prev) navigate(`#/read/${readerState.seriesId}/${readerState.prev.num}`);
    else if (e.key === "ArrowRight" && readerState.next) navigate(`#/read/${readerState.seriesId}/${readerState.next.num}`);
    else if (e.key === "Escape") {
      if (document.body.classList.contains("reader-fullscreen")) toggleFullscreen();
      else navigate(`#/series/${readerState.seriesId}`);
    }
    else if (e.key === "f" || e.key === "F") toggleFullscreen();
    else if (e.key === "z" || e.key === "Z") openZoom();
    else if (e.key === "s" || e.key === "S") shareEpisode();
  }

  /* ── Touch swipe ── */
  function onTouchStart(e) { touchStartX = e.touches[0].clientX; }
  function onTouchEnd(e) {
    if (!readerState || $("#page-reader").classList.contains("hidden")) return;
    const dx = e.changedTouches[0].clientX - touchStartX;
    if (Math.abs(dx) < 60) return;
    if (dx > 0 && readerState.prev) navigate(`#/read/${readerState.seriesId}/${readerState.prev.num}`);
    else if (dx < 0 && readerState.next) navigate(`#/read/${readerState.seriesId}/${readerState.next.num}`);
  }

  /* ── Scroll top ── */
  function onScroll() {
    const btn = $("#scroll-top");
    btn.classList.toggle("hidden", window.scrollY < 400);
  }

  /* ── Init ── */
  async function init() {
    applyTheme(theme());

    $("#search-input")?.addEventListener("input", (e) => {
      searchFocus = 0;
      renderSearchResults(e.target.value);
    });

    document.addEventListener("keydown", onKeydown);
    document.addEventListener("touchstart", onTouchStart, { passive: true });
    document.addEventListener("touchend", onTouchEnd, { passive: true });
    window.addEventListener("scroll", onScroll, { passive: true });
    window.addEventListener("hashchange", router);

    try {
      const [comicsRes, roadmapRes, coreRes, guidesRes, glossaryRes] = await Promise.all([
        fetch("data/comics.json"),
        fetch("data/roadmap.json"),
        fetch("data/core.json"),
        fetch("data/episode-guides.json"),
        fetch("data/glossary.json"),
      ]);
      data = await comicsRes.json();
      if (roadmapRes.ok) roadmapData = await roadmapRes.json();
      if (guidesRes.ok) episodeGuides = await guidesRes.json();
      if (coreRes.ok && typeof Learn !== "undefined") {
        Learn.init(await coreRes.json());
      }
      if (glossaryRes.ok && typeof Glossary !== "undefined") {
        Glossary.init(await glossaryRes.json(), data);
        Glossary.setupGlobalListeners();
      }
      hideLoader();
      updateContinueBanner();
      router();
    } catch {
      hideLoader();
      $("#app").innerHTML = `<div style="text-align:center;padding:4rem;color:var(--text-muted)">
        <p style="font-size:2rem;margin-bottom:1rem">⚠️</p>
        <p>Không tải được dữ liệu.</p>
        <p style="margin-top:0.5rem;font-size:0.85rem">Chạy: <code>python3 -m http.server 8080</code></p>
      </div>`;
    }
  }

  init();

  return {
    navigate, openSearch, closeSearch, openShortcuts, closeShortcuts,
    openZoom, closeZoom, toggleFullscreen, toggleTheme, toggleBookmark,
    shareEpisode, setFilter, setEpisodeView, startReading, startLearning,
    continueReading, continueRoadmap, selectRoadmapPath, dismissContinue,
    removeBookmark, openReviewMode, closeReviewMode, copyReviewPrompt,
  };
})();

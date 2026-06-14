/* English Vault — Patterns & Review (from core.json) */
const Learn = (() => {
  let core = null;

  function init(coreJson) {
    core = coreJson;
  }

  function getPack(id) {
    return core?.packs?.find((p) => p.id === id);
  }

  function allPatternsFlat() {
    if (!core) return [];
    const items = [];
    for (const pack of core.packs) {
      for (const p of pack.patterns || []) items.push({ pack, text: p });
      for (const p of pack.phrasalVerbs || []) items.push({ pack, text: p, type: "phrasal" });
      for (const p of pack.phrases || []) items.push({ pack, text: p, type: "phrase" });
      for (const g of pack.groups || []) {
        for (const p of g.patterns || []) items.push({ pack, group: g, text: p });
        for (const p of g.phrases || []) items.push({ pack, group: g, text: p, type: "phrase" });
      }
    }
    return items;
  }

  function episodesUsingPack(packId, comicsData) {
    return comicsData.series.flatMap((s) =>
      s.episodes
        .filter((ep) => (ep.packs || []).includes(packId))
        .map((ep) => ({ ...ep, seriesId: s.id, seriesTitle: s.title, seriesColor: s.color }))
    );
  }

  function renderPatternsPage(root, comicsData, navigate) {
    if (!core || !root) return;
    const loop = core.project.coreLoop.join(" → ");

    const packCards = core.packs
      .map(
        (p) => `
      <article class="pattern-pack-card" onclick="App.navigate('#/patterns/${p.id}')">
        <h3>${p.title}</h3>
        <p>${p.purpose || ""}</p>
        <div class="pattern-pack-meta">
          ${(p.contexts || []).slice(0, 4).map((c) => `<span class="tag-pill">${c}</span>`).join("")}
        </div>
        <span class="pattern-pack-count">${(p.patterns || []).length} patterns</span>
      </article>`
      )
      .join("");

    root.innerHTML = `
      <nav class="breadcrumb" aria-label="Breadcrumb">
        <a href="#/">Trang chủ</a>
        <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="m9 18 6-6-6-6"/></svg>
        <span>Pattern Library</span>
      </nav>
      <div class="patterns-hero">
        <div class="patterns-hero-badge">🧠 ${core.project.name}</div>
        <h1>Học pattern, không học grammar rời</h1>
        <p>${core.project.mainPromise}</p>
        <div class="core-loop">
          <span class="core-loop-label">Core loop:</span>
          <span class="core-loop-steps">${loop}</span>
        </div>
        <p class="patterns-goal">${core.project.websiteGoal}</p>
      </div>
      <div class="pattern-pack-grid">${packCards}</div>
      <div class="review-cta">
        <h2>🔄 Review Mode</h2>
        <p>Luyện nói với AI — copy prompt bên dưới vào ChatGPT/Claude sau khi đọc tập.</p>
        <button class="btn btn-primary" type="button" onclick="App.openReviewMode()">Mở Review Mode</button>
      </div>`;
  }

  function renderPackDetail(root, packId, comicsData, navigate) {
    const pack = getPack(packId);
    if (!pack || !root) {
      navigate("#/patterns");
      return;
    }

    const patterns = (pack.patterns || [])
      .map((p) => `<li class="pattern-item">${p}</li>`)
      .join("");
    const phrasal = (pack.phrasalVerbs || pack.phrases || [])
      .map((p) => `<li class="pattern-item phrasal">${p}</li>`)
      .join("");

    let groupsHtml = "";
    if (pack.groups) {
      groupsHtml = pack.groups
        .map(
          (g) => `
        <div class="pattern-group">
          <h4>${g.title}</h4>
          <ul class="pattern-list">${(g.patterns || []).map((p) => `<li class="pattern-item">${p}</li>`).join("")}</ul>
          ${(g.phrases || []).length ? `<ul class="pattern-list phrasal-list">${g.phrases.map((p) => `<li class="pattern-item phrasal">${p}</li>`).join("")}</ul>` : ""}
        </div>`
        )
        .join("");
    }

    const related = episodesUsingPack(packId, comicsData).slice(0, 8);
    const relatedHtml = related.length
      ? related
          .map(
            (ep) => `
          <button class="related-ep-chip" style="--series-color:${ep.seriesColor}"
            onclick="App.navigate('#/read/${ep.seriesId}/${ep.num}')">
            Tập ${ep.num}: ${ep.title}
          </button>`
          )
          .join("")
      : `<p class="text-muted">Chưa gắn tập — đọc truyện và quay lại sau.</p>`;

    root.innerHTML = `
      <nav class="breadcrumb" aria-label="Breadcrumb">
        <a href="#/">Trang chủ</a>
        <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="m9 18 6-6-6-6"/></svg>
        <a href="#/patterns">Patterns</a>
        <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="m9 18 6-6-6-6"/></svg>
        <span>${pack.title}</span>
      </nav>
      <div class="pack-detail-hero">
        <h1>${pack.title}</h1>
        <p>${pack.purpose || ""}</p>
        ${pack.masterCombo ? `<blockquote class="master-combo">"${pack.masterCombo}"</blockquote>` : ""}
        ${pack.example ? `<p class="pack-example"><strong>Ví dụ:</strong> ${pack.example}</p>` : ""}
      </div>
      ${groupsHtml || `<ul class="pattern-list">${patterns}</ul>${phrasal ? `<h3>Phrasal verbs</h3><ul class="pattern-list phrasal-list">${phrasal}</ul>` : ""}`}
      <div class="related-eps">
        <h3>📚 Tập truyện dùng pack này</h3>
        <div class="related-ep-chips">${relatedHtml}</div>
      </div>`;
  }

  function reviewPrompt(topic) {
    const t = topic || "patterns vừa học";
    return (core?.reviewModeTemplate || "").replace("[selected topic]", t);
  }

  return { init, getPack, renderPatternsPage, renderPackDetail, reviewPrompt, episodesUsingPack };
})();

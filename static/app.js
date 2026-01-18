function normalize(s) {
  return (s || "").toString().toLowerCase();
}

function debounce(fn, delay) {
  let t;
  return (...args) => {
    clearTimeout(t);
    t = setTimeout(() => fn(...args), delay);
  };
}

function showLoader() {
  const el = document.getElementById("sx-loader");
  if (!el) return;
  el.classList.remove("hidden");
  el.setAttribute("aria-hidden", "false");
}

function hideLoader() {
  const el = document.getElementById("sx-loader");
  if (!el) return;
  el.classList.add("hidden");
  el.setAttribute("aria-hidden", "true");
}

function wireLoader() {
  document.querySelectorAll("form[data-show-loader='true']").forEach((form) => {
    form.addEventListener("submit", () => showLoader());
  });
  window.addEventListener("pageshow", () => hideLoader());
}

function wireCopyButtons() {
  document.querySelectorAll("[data-copy-target]").forEach((btn) => {
    btn.addEventListener("click", async () => {
      const id = btn.getAttribute("data-copy-target");
      const el = document.getElementById(id);
      if (!el) return;
      const text = el.value;
      const original = btn.getAttribute("data-original-html") || btn.innerHTML;
      btn.setAttribute("data-original-html", original);
      try {
        await navigator.clipboard.writeText(text);
        btn.innerHTML = "Copied";
        setTimeout(() => {
          btn.innerHTML = btn.getAttribute("data-original-html") || "Copy";
        }, 900);
      } catch (e) {
        // no-op
      }
    });
  });
}

function wireTableSearch() {
  document.querySelectorAll("[data-table-search]").forEach((input) => {
    const tableId = input.getAttribute("data-table-search");
    const table = document.getElementById(tableId);
    if (!table) return;

    const rows = Array.from(table.querySelectorAll("tbody tr"));
    rows.forEach((tr) => {
      if (!tr.dataset.sxText) tr.dataset.sxText = normalize(tr.innerText);
    });

    const apply = debounce(() => {
      const q = normalize(input.value);
      rows.forEach((tr) => {
        const txt = tr.dataset.sxText || "";
        tr.style.display = txt.includes(q) ? "" : "none";
      });
    }, 120);

    input.addEventListener("input", apply);
  });
}

function getWidthsKey(tableId) {
  return `sx_colwidths_${tableId}`;
}

function loadColWidths(tableId) {
  try {
    return JSON.parse(localStorage.getItem(getWidthsKey(tableId)) || "{}") || {};
  } catch (_) {
    return {};
  }
}

function saveColWidths(tableId, widths) {
  try {
    localStorage.setItem(getWidthsKey(tableId), JSON.stringify(widths));
  } catch (_) {
    // no-op
  }
}

function isDesktopNoScroll() {
  return window.matchMedia && window.matchMedia("(min-width: 1024px)").matches;
}

function applyColWidth(table, colIdx, px) {
  const selector = `th[data-col-idx='${colIdx}'], tbody tr td:nth-child(${colIdx + 1})`;
  const desktopFit = isDesktopNoScroll();
  table.querySelectorAll(selector).forEach((cell) => {
    cell.style.width = `${px}px`;
    if (!desktopFit) cell.style.minWidth = `${px}px`;
    else cell.style.minWidth = "";
    cell.style.maxWidth = `${px}px`;
  });
}

function fitColumnsToContainer(table, preferredWidths) {
  const ths = Array.from(table.querySelectorAll("thead th[data-col-idx]"));
  if (ths.length === 0) return;
  const wrap = table.closest(".sx-table-wrap");
  const wrapWidth = wrap ? wrap.getBoundingClientRect().width : table.getBoundingClientRect().width;
  if (!wrapWidth || !Number.isFinite(wrapWidth)) return;

  const min = 60;
  const maxPerCol = Math.max(min, Math.floor(wrapWidth / 2));
  const base = ths.map((th, i) => {
    const idx = parseInt(th.getAttribute("data-col-idx") || String(i), 10);
    const w = preferredWidths && preferredWidths[idx] ? preferredWidths[idx] : th.getBoundingClientRect().width;
    return Math.min(maxPerCol, Math.max(min, Math.floor(w || min)));
  });

  const sum = base.reduce((a, b) => a + b, 0);
  const target = Math.max(min * ths.length, Math.floor(wrapWidth) - 6);
  const scale = sum > 0 ? Math.min(1, target / sum) : 1;

  base.forEach((w, i) => {
    const next = Math.max(min, Math.floor(w * scale));
    applyColWidth(table, i, next);
  });
}

function initAutoWidths(table) {
  const ths = Array.from(table.querySelectorAll("thead th[data-col-idx]"));
  if (ths.length === 0) return;

  const wrap = table.closest(".sx-table-wrap");
  const wrapWidth = wrap ? wrap.getBoundingClientRect().width : table.getBoundingClientRect().width;
  const min = 110;
  const max = Math.max(160, Math.floor(wrapWidth * 0.6));
  const even = Math.max(min, Math.floor(wrapWidth / ths.length));

  ths.forEach((th, idx) => {
    const label = th.querySelector(".sx-th-label")?.textContent || "";
    const guess = Math.min(max, Math.max(min, Math.floor(label.length * 10 + 40)));
    applyColWidth(table, idx, Math.min(max, Math.max(min, Math.floor((guess + even) / 2))));
  });
}

function wireColumnResize() {
  document.querySelectorAll("table.sx-table[id]").forEach((table) => {
    const tableId = table.getAttribute("id");
    if (!tableId) return;

    const saved = loadColWidths(tableId);

    initAutoWidths(table);

    if (isDesktopNoScroll()) {
      const preferred = {};
      Object.keys(saved).forEach((k) => {
        const idx = parseInt(k, 10);
        const px = parseInt(saved[k], 10);
        if (Number.isFinite(idx) && Number.isFinite(px)) preferred[idx] = px;
      });
      fitColumnsToContainer(table, preferred);
    }

    Object.keys(saved).forEach((k) => {
      const idx = parseInt(k, 10);
      const px = parseInt(saved[k], 10);
      if (!Number.isFinite(idx) || !Number.isFinite(px)) return;
      if (!isDesktopNoScroll()) applyColWidth(table, idx, px);
    });

    const resizers = Array.from(table.querySelectorAll("thead th[data-col-idx] .sx-col-resizer"));
    resizers.forEach((handle) => {
      const th = handle.closest("th");
      if (!th) return;
      const colIdx = parseInt(th.getAttribute("data-col-idx") || "0", 10);

      const startDrag = (ev) => {
        ev.preventDefault();
        const startX = ev.clientX ?? (ev.touches && ev.touches[0]?.clientX);
        if (startX == null) return;

        const startWidth = th.getBoundingClientRect().width;
        const min = 90;
        const desktopFit = isDesktopNoScroll();
        let max = 4000;
        if (desktopFit) {
          const wrap = table.closest(".sx-table-wrap");
          const wrapWidth = wrap ? wrap.getBoundingClientRect().width : table.getBoundingClientRect().width;
          max = Math.max(min + 40, Math.floor(wrapWidth) - 20);
        }

        const onMove = (moveEv) => {
          const x = moveEv.clientX ?? (moveEv.touches && moveEv.touches[0]?.clientX);
          if (x == null) return;
          const next = Math.min(max, Math.max(min, Math.floor(startWidth + (x - startX))));
          applyColWidth(table, colIdx, next);
        };

        const onUp = () => {
          document.removeEventListener("pointermove", onMove);
          document.removeEventListener("pointerup", onUp);
          document.removeEventListener("touchmove", onMove);
          document.removeEventListener("touchend", onUp);

          const widthNow = Math.floor(th.getBoundingClientRect().width);
          const widths = loadColWidths(tableId);
          widths[String(colIdx)] = widthNow;
          saveColWidths(tableId, widths);
        };

        document.addEventListener("pointermove", onMove);
        document.addEventListener("pointerup", onUp);
        document.addEventListener("touchmove", onMove, { passive: false });
        document.addEventListener("touchend", onUp);
      };

      handle.addEventListener("pointerdown", startDrag);
      handle.addEventListener("touchstart", startDrag, { passive: false });
    });
  });
}

document.addEventListener("DOMContentLoaded", () => {
  wireLoader();
  wireCopyButtons();
  wireTableSearch();
  wireColumnResize();
});

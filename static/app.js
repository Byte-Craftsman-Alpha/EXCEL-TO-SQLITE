function normalize(s) {
  return (s || "").toString().toLowerCase();
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

    input.addEventListener("input", () => {
      const q = normalize(input.value);
      const rows = table.querySelectorAll("tbody tr");
      rows.forEach((tr) => {
        const txt = normalize(tr.innerText);
        tr.style.display = txt.includes(q) ? "" : "none";
      });
    });
  });
}

document.addEventListener("DOMContentLoaded", () => {
  wireCopyButtons();
  wireTableSearch();
});

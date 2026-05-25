// copy-to-clipboard for [data-copy] buttons
document.addEventListener("click", function (e) {
  const btn = e.target.closest("[data-copy]");
  if (!btn) return;
  const text = btn.getAttribute("data-copy");
  navigator.clipboard.writeText(text).then(function () {
    const prev = btn.textContent;
    btn.textContent = "복사됨 ✓";
    btn.classList.add("copied");
    setTimeout(function () {
      btn.textContent = prev;
      btn.classList.remove("copied");
    }, 1400);
  });
});

// live search filter over plugin cards
const search = document.getElementById("plugin-search");
if (search) {
  search.addEventListener("input", function () {
    const q = this.value.trim().toLowerCase();
    let visible = 0;
    document.querySelectorAll("[data-search]").forEach(function (el) {
      const hay = el.getAttribute("data-search").toLowerCase();
      const match = hay.indexOf(q) !== -1;
      el.classList.toggle("fade-hidden", !match);
      if (match) visible++;
    });
    const none = document.getElementById("no-results");
    if (none) none.classList.toggle("fade-hidden", visible !== 0);
  });
}

const menuButton = document.querySelector('.menu-toggle');
const navigation = document.querySelector('.site-nav');
if (menuButton && navigation) { menuButton.addEventListener('click', () => { const open = menuButton.getAttribute('aria-expanded') === 'true'; menuButton.setAttribute('aria-expanded', String(!open)); navigation.classList.toggle('is-open', !open); }); }
document.querySelectorAll('[data-year]').forEach((node) => { node.textContent = new Date().getFullYear(); });
if ('IntersectionObserver' in window) { const observer = new IntersectionObserver((entries) => { entries.forEach((entry) => { if (entry.isIntersecting) { entry.target.classList.add('is-visible'); observer.unobserve(entry.target); } }); }, { threshold: 0.12 }); document.querySelectorAll('.reveal').forEach((element) => observer.observe(element)); } else { document.querySelectorAll('.reveal').forEach((element) => element.classList.add('is-visible')); }

/* ---------- Dark / light theme ---------- */
document.querySelectorAll('[data-theme-toggle]').forEach((btn) => {
  btn.addEventListener('click', () => {
    const root = document.documentElement;
    const next = root.getAttribute('data-theme') === 'dark' ? 'light' : 'dark';
    root.setAttribute('data-theme', next);
    try { localStorage.setItem('theme', next); } catch (e) {}
  });
});

/* ---------- Publication abstracts ---------- */
document.querySelectorAll('[data-abstract-toggle]').forEach((btn) => {
  btn.addEventListener('click', () => {
    const abs = btn.closest('.pub-item').querySelector('.pub-abstract');
    const open = btn.getAttribute('aria-expanded') === 'true';
    btn.setAttribute('aria-expanded', String(!open));
    if (abs) abs.hidden = open;
  });
});

/* ---------- Ctrl+K search palette ---------- */
(function () {
  const overlay = document.querySelector('[data-search-overlay]');
  const input = document.querySelector('[data-search-input]');
  const list = document.querySelector('[data-search-results]');
  if (!overlay || !input || !list) return;
  let index = null, results = [], active = 0, lastFocus = null;

  const load = () => index ? Promise.resolve(index) : fetch(window.SEARCH_INDEX_URL).then((r) => r.json()).then((d) => (index = d)).catch(() => (index = []));
  const esc = (t) => String(t).replace(/[&<>"]/g, (c) => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c]));

  function render() {
    list.innerHTML = results.length
      ? results.map((r, i) => `<li><a href="${esc(r.url)}" class="${i === active ? 'is-active' : ''}"><span class="search-type">${esc(r.type)}</span><span class="search-title">${esc(r.title)}</span></a></li>`).join('')
      : '<li class="search-empty">No matches found.</li>';
  }
  function search(q) {
    q = q.trim().toLowerCase();
    const items = index || [];
    results = !q ? items.filter((i) => i.type === 'Page').slice(0, 8)
      : items.map((i) => {
          const t = i.title.toLowerCase(), x = (i.text || '').toLowerCase();
          const score = (t.startsWith(q) ? 3 : 0) + (t.includes(q) ? 2 : 0) + (x.includes(q) ? 1 : 0);
          return { i, score };
        }).filter((o) => o.score > 0).sort((a, b) => b.score - a.score).slice(0, 8).map((o) => o.i);
    active = 0; render();
  }
  function open() { lastFocus = document.activeElement; overlay.hidden = false; document.body.classList.add('no-scroll'); input.value = ''; load().then(() => search('')); input.focus(); }
  function close() { overlay.hidden = true; document.body.classList.remove('no-scroll'); if (lastFocus) lastFocus.focus(); }

  document.querySelectorAll('[data-search-open]').forEach((b) => b.addEventListener('click', open));
  overlay.addEventListener('click', (e) => { if (e.target === overlay) close(); });
  input.addEventListener('input', () => search(input.value));
  document.addEventListener('keydown', (e) => {
    if ((e.ctrlKey || e.metaKey) && e.key.toLowerCase() === 'k') { e.preventDefault(); overlay.hidden ? open() : close(); return; }
    if (overlay.hidden) return;
    if (e.key === 'Escape') close();
    else if (e.key === 'ArrowDown') { e.preventDefault(); active = Math.min(active + 1, results.length - 1); render(); }
    else if (e.key === 'ArrowUp') { e.preventDefault(); active = Math.max(active - 1, 0); render(); }
    else if (e.key === 'Enter' && results[active]) { window.location.href = results[active].url; }
  });
})();

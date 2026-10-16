#!/usr/bin/env python3
"""Generate index.html — the TrioTheo status page — from the design system's own pieces.

Self-contained on purpose: Trioscript (OFL), the doodle mark, the favicon and the pen ride inside the
file as data URIs, and the colour tokens are read out of scripts/owner_dashboard.py so the two cannot
drift. The page makes no request but for status.json, history.json and incidents.json beside it.
Usage: python3 build_page.py <triotheo repo root>   → writes index.html here. Never edit index.html.
"""
import base64, re, sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
REPO = Path(sys.argv[1]).resolve()
DASH = (REPO / "scripts/owner_dashboard.py").read_text()
FONTS = REPO / "webapp/learn-doodle/src/assets/fonts/trioscript"
MARK = REPO / "docs/assets/brand-logo/triotheo-mark-doodle.svg"
MARK_DARK = REPO / "docs/assets/brand-logo/triotheo-mark-doodle-reversed.svg"
FAV_SVG = REPO / "webapp/landing/public/assets/brand/triotheo-favicon.svg"
FAV_PNG = REPO / "webapp/landing/public/favicon-96.png"

def b64(p: Path) -> str: return base64.b64encode(p.read_bytes()).decode("ascii")
def uri(p: Path, mime: str) -> str: return f"data:{mime};base64,{b64(p)}"

# the tokens, verbatim from the dashboard (which copies theme.css): light block + DARK_TOKENS
m = re.search(r"(:root \{\n  --brand-gold.*?color-scheme: light;\n\})", DASH, re.S); assert m, "light tokens"
LIGHT = m.group(1)
m = re.search(r'DARK_TOKENS = """\n(.*?)"""', DASH, re.S); assert m, "dark tokens"
DARK = m.group(1).rstrip()
faces = "\n".join(
    f'@font-face {{ font-family: "Trioscript"; src: url("{uri(FONTS / f"trioscript-{w}.woff2", "font/woff2")}") format("woff2"); '
    f'font-weight: {w}; font-style: normal; font-display: swap; }}' for w in (400, 600, 800))
PEN = (HERE / "pen.js").read_text()

CSS = f"""
{faces}
/* Trioscript — TrioTheo's typeface, a modified Fredoka under the SIL OFL 1.1 (OFL.txt) */
{LIGHT}
@media (prefers-color-scheme: dark) {{
  :root:not([data-theme="light"]) {{
{DARK}
  }}
}}
:root[data-theme="dark"] {{
{DARK}
}}
* {{ box-sizing: border-box; }}
html, body {{ margin: 0; }}
body {{
  font-family: "Trioscript", ui-rounded, "SF Pro Rounded", system-ui, -apple-system, sans-serif;
  font-size: 16px; font-weight: 400; letter-spacing: 0.02em; line-height: 1.5;
  background: var(--bg); color: var(--ink); -webkit-font-smoothing: antialiased;
}}
a {{ color: inherit; }}
.page {{ max-width: 760px; margin: 0 auto; padding: 36px 20px 80px; }}
.brand {{ display: flex; align-items: center; gap: 16px; margin-bottom: 22px; }}
.mark {{ width: 56px; height: 56px; flex: none; }}
.mark img {{ width: 100%; height: 100%; display: block; }}
.mark .dark {{ display: none; }}
@media (prefers-color-scheme: dark) {{ :root:not([data-theme="light"]) .mark .light {{ display: none; }} :root:not([data-theme="light"]) .mark .dark {{ display: block; }} }}
:root[data-theme="dark"] .mark .light {{ display: none; }} :root[data-theme="dark"] .mark .dark {{ display: block; }}
.eyebrow {{ display: block; font-size: 13px; font-weight: 800; letter-spacing: 0.08em; text-transform: uppercase; color: var(--label-purple); margin-bottom: 2px; }}
h1 {{ margin: 0; font-size: 30px; font-weight: 800; letter-spacing: 0.05em; line-height: 1.15; color: var(--headline-ink); text-wrap: balance; }}
.sub {{ margin: 4px 0 0; font-size: 15px; font-weight: 600; color: var(--muted); }}
.brand-text {{ min-width: 0; flex: 1; }}
.theme {{ flex: none; width: 44px; height: 44px; border: 0; background: none; padding: 0; cursor: pointer; position: relative; color: color-mix(in srgb, var(--toggle-coin) 60%, #000); }}
.theme .btn-svg, .coin .btn-svg {{ position: absolute; inset: 0; pointer-events: none; }}
/* the pen draws a card into a viewBox padded 6px on every side; the SVG's box is padded the same
   or `meet` fits the taller viewBox to a wide card's height and shrinks its width (measured) */
.card .btn-svg {{ position: absolute; inset: -6px; pointer-events: none; }}
.theme svg.glyph {{ position: absolute; inset: 0; margin: auto; width: 20px; height: 20px; }}
.card {{ position: relative; padding: 18px 20px; margin-bottom: 18px; }}
.card > :not(.btn-svg) {{ position: relative; }}
h2 {{ margin: 0 0 12px; font-size: 13px; font-weight: 800; letter-spacing: 0.08em; text-transform: uppercase; color: var(--label-purple); }}
/* THE BANNER — the state as one filled card, the githubstatus shape in the house pen */
.banner {{ padding: 20px 22px; color: #fff; }}
.banner .btn-svg {{ inset: -6px; }}
.banner-title {{ font-size: 24px; font-weight: 800; letter-spacing: 0.03em; line-height: 1.2; }}
.checked {{ margin: -6px 0 18px; font-size: 13px; font-weight: 600; color: var(--muted); letter-spacing: 0.02em; }}
/* COMPONENTS — a name, a status word, a thin uptime strip, the caption under it */
.row {{ padding: 12px 0; border-top: 1.5px dashed var(--nav-border); }}
.row:first-of-type {{ border-top: 0; padding-top: 2px; }}
.row-top {{ display: flex; align-items: center; gap: 10px; }}
.name {{ flex: 1; min-width: 0; font-size: 18px; font-weight: 800; color: var(--headline-ink); letter-spacing: 0.02em; }}
.status {{ display: inline-flex; align-items: center; gap: 7px; font-size: 14px; font-weight: 800; letter-spacing: 0.02em; white-space: nowrap; }}
.status.up {{ color: color-mix(in srgb, var(--brand-green) 60%, #000); }}
.status.down {{ color: var(--brand-scarlet); }}
.coin {{ position: relative; flex: none; width: 18px; height: 18px; }}
.days {{ display: grid; grid-template-columns: repeat(30, 1fr); gap: 3px; margin-top: 10px; }}
.day {{ height: 9px; border-radius: 3px; background: var(--coin-ghost); border: 1.5px solid var(--nav-border); }}
.day.up {{ background: var(--brand-green); border-color: color-mix(in srgb, var(--brand-green) 78%, #000); }}
.day.partial {{ background: var(--brand-orange); border-color: color-mix(in srgb, var(--brand-orange) 78%, #000); }}
.day.down {{ background: var(--brand-scarlet); border-color: color-mix(in srgb, var(--brand-scarlet) 78%, #000); }}
.days-cap {{ display: flex; justify-content: space-between; align-items: baseline; margin-top: 5px; font-size: 12px; font-weight: 600; color: var(--faint); letter-spacing: 0.03em; font-variant-numeric: tabular-nums; }}
.days-cap b {{ color: var(--muted); font-weight: 800; }}
/* PAST INCIDENTS — a day at a time, the last fourteen, newest first */
.dayblk {{ padding: 14px 0 12px; border-top: 1.5px dashed var(--nav-border); }}
.dayblk:first-of-type {{ border-top: 0; padding-top: 2px; }}
.dayhd {{ font-size: 16px; font-weight: 800; color: var(--headline-ink); letter-spacing: 0.02em; }}
.none {{ margin: 6px 0 0; font-size: 14px; font-weight: 600; color: var(--faint); }}
.inc {{ margin-top: 10px; }}
.inc-title {{ display: flex; align-items: center; gap: 8px; font-size: 17px; font-weight: 800; color: var(--brand-scarlet); letter-spacing: 0.02em; }}
.inc-title.over {{ color: var(--headline-ink); }}
.upd {{ display: grid; grid-template-columns: auto 1fr; column-gap: 10px; row-gap: 2px; margin-top: 8px; padding-left: 26px; }}
.upd b {{ font-size: 14px; font-weight: 800; color: var(--headline-ink); letter-spacing: 0.03em; }}
.upd span {{ font-size: 14px; color: var(--ink); }}
.upd small {{ grid-column: 2; font-size: 12px; font-weight: 600; color: var(--faint); font-variant-numeric: tabular-nums; }}
.quiet {{ font-size: 15px; font-weight: 600; color: var(--muted); }}
.more {{ display: flex; align-items: center; gap: 14px; flex-wrap: wrap; margin-top: 14px; padding-top: 12px; border-top: 1.5px dashed var(--nav-border); }}
.pill {{ position: relative; border: 0; background: none; padding: 0; cursor: pointer; font: inherit; color: var(--headline-ink); }}
.pill .btn-svg {{ position: absolute; inset: -6px; pointer-events: none; }}
.pill-in {{ position: relative; display: inline-block; padding: 9px 18px; font-size: 14px; font-weight: 800; letter-spacing: 0.04em; color: #fff; background: var(--brand-blue); border-radius: 999px; }}
.more-cap {{ font-size: 13px; font-weight: 600; color: var(--faint); font-variant-numeric: tabular-nums; }}
.foot {{ margin-top: 28px; font-size: 14px; font-weight: 600; color: var(--muted); display: flex; flex-wrap: wrap; gap: 6px 18px; }}
.foot a {{ color: var(--brand-blue); text-decoration: none; font-weight: 800; }}
@media (max-width: 480px) {{ .page {{ padding: 24px 16px 64px; }} h1 {{ font-size: 26px; }} .banner-title {{ font-size: 20px; }} .days {{ gap: 2px; }} .upd {{ grid-template-columns: 1fr; padding-left: 0; }} .upd small {{ grid-column: 1; }} }}
"""

JS = r"""
var S = {};
function esc(s) { return String(s == null ? "" : s).replace(/[&<>"]/g, function (c) { return ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" })[c]; }); }
function ago(iso) { var m = Math.round((Date.now() - new Date(iso).getTime()) / 60000); if (m < 1) return "just now"; if (m < 60) return m + " min ago"; var h = Math.round(m / 60); if (h < 48) return h + (h === 1 ? " hour ago" : " hours ago"); return Math.round(h / 24) + " days ago"; }
function clock(iso) { return new Date(iso).toLocaleTimeString(undefined, { hour: "numeric", minute: "2-digit" }); }
function dateHd(d) { return d.toLocaleDateString(undefined, { month: "short", day: "numeric", year: "numeric" }); }
function dur(a, b) { var m = Math.max(1, Math.round((new Date(b || Date.now()) - new Date(a)) / 60000)); return m < 60 ? m + " min" : (m / 60).toFixed(1).replace(/\.0$/, "") + " h"; }
function localDay(iso) { var d = new Date(iso); return d.getFullYear() + "-" + String(d.getMonth() + 1).padStart(2, "0") + "-" + String(d.getDate()).padStart(2, "0"); }
function coinSVG(yarn, seed) {
  var box = 68, r = 26, ring = "color-mix(in srgb, " + yarn + " 80%, #000000)";
  return '<svg viewBox="0 0 ' + box + ' ' + box + '" aria-hidden="true" style="' + SVG_STYLE + '">'
    + '<path d="' + jitterCircle(r, box, seed + 3, 1.3) + '" fill="' + yarn + '" transform="translate(3.2 2.8)"/>'
    + '<path d="' + jitterCircle(r, box, seed, 1.6) + '" fill="none" stroke="' + ring + '" stroke-width="2.6" stroke-linecap="round"/></svg>';
}
/* a FILLED drawn card — the banner — in the house pen's hand (jitterRect, same seeds style) */
function fillCard(el, yarn) {
  var wrap = el.querySelector(".btn-svg"), seed = +el.dataset.seed, ring = "color-mix(in srgb, " + yarn + " 78%, #000000)";
  once(el, function () {
    var w = el.offsetWidth, h = el.offsetHeight; if (!w || !h) return;
    var rr = Math.min(20, h / 2 - 1), d1 = jitterRect(w, h, rr, seed, 1.3), d2 = jitterRect(w, h, rr, seed + 7, 1.2);
    wrap.innerHTML = '<svg viewBox="-6 -6 ' + (w + 12) + ' ' + (h + 12) + '" aria-hidden="true" style="' + SVG_STYLE + '">'
      + '<path d="' + d1 + '" fill="' + yarn + '" stroke="' + ring + '" stroke-width="2.6" stroke-linecap="round" stroke-linejoin="round"/>'
      + '<path d="' + d2 + '" fill="none" stroke="' + ring + '" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round" opacity="0.6" transform="translate(1.3 1.1)"/></svg>';
  });
}
var YARN = { up: "var(--brand-green)", partial: "var(--brand-orange)", down: "var(--brand-scarlet)" };
var WORD = { up: "All Systems Operational", partial: "Partial System Outage", down: "Major System Outage" };
var ROWWORD = { up: "Operational", down: "Outage" };
function render() {
  var st = S.status, hist = S.history || [], inc = S.incidents || [];
  var banner = document.getElementById("banner");
  banner.innerHTML = '<span class="btn-svg"></span><div class="banner-title">' + esc(WORD[st.overall]) + '</div>';
  fillCard(banner, YARN[st.overall]);
  document.getElementById("checked").textContent = "Checked " + ago(st.checked_at) + " · every " + st.every_minutes + " minutes from " + st.source;
  var days = []; for (var i = 29; i >= 0; i--) days.push(localDay(new Date(Date.now() - i * 864e5).toISOString()));
  var rows = "", seed = 100;
  Object.keys(st.services).forEach(function (id) {
    var s = st.services[id], mine = hist.filter(function (h) { return h.s && h.s[id]; });
    var up = mine.filter(function (h) { return h.s[id] === "up"; }).length, pct = mine.length ? Math.round(1000 * up / mine.length) / 10 : null;
    var byDay = {}; mine.forEach(function (h) { var k = localDay(h.t); byDay[k] = byDay[k] || { n: 0, d: 0 }; byDay[k].n++; if (h.s[id] !== "up") byDay[k].d++; });
    var strip = days.map(function (k) { var b = byDay[k]; var cls = !b ? "" : b.d === 0 ? "up" : b.d === b.n ? "down" : "partial";
      return '<span class="day ' + cls + '" title="' + k + (b ? ": " + (b.n - b.d) + " of " + b.n + " checks up" : ": no checks") + '"></span>'; }).join("");
    var seen = Object.keys(byDay).length;
    rows += '<div class="row"><div class="row-top"><span class="name">' + esc(s.name) + '</span>'
      + '<span class="status ' + s.state + '" title="' + (s.state === "up" ? s.ms + " ms" : esc(s.note || "no answer")) + '"><span class="coin" aria-hidden="true">' + coinSVG(YARN[s.state], seed += 13) + '</span>' + ROWWORD[s.state] + '</span></div>'
      + '<div class="days">' + strip + '</div>'
      + '<div class="days-cap"><span>30 days ago</span><b>' + (pct === null ? "no checks yet" : pct + "% uptime over " + seen + (seen === 1 ? " day" : " days")) + '</b><span>today</span></div></div>';
  });
  document.getElementById("services").innerHTML = rows;
  // the last SEVEN days, newest first — each day its incidents, or the line that it had none;
  // "Show the week before" pages back seven at a time, as far as the 30 days of history go
  // (owner note on the review board, 2026-10-16: paginate, show the current week)
  var byStart = {};
  inc.forEach(function (x) { var k = localDay(x.started); (byStart[k] = byStart[k] || []).push(x); });
  function dayBlock(d) {
    var dt = new Date(Date.now() - d * 864e5), k = localDay(dt.toISOString()), list = (byStart[k] || []).slice().reverse();
    var h = '<div class="dayblk"><div class="dayhd">' + esc(dateHd(dt)) + '</div>';
    if (!list.length) h += '<p class="none">' + (d === 0 ? "No incidents reported today." : "No incidents reported.") + '</p>';
    list.forEach(function (x) {
      h += '<div class="inc"><div class="inc-title' + (x.ended ? " over" : "") + '"><span class="coin" aria-hidden="true">' + coinSVG(x.ended ? YARN.up : YARN.down, 700 + d) + '</span>' + esc(x.name) + (x.ended ? " outage" : " is down") + '</div><div class="upd">';
      if (x.ended) h += '<b>Recovered</b><span>' + esc(x.name) + ' answered again, after about ' + esc(dur(x.started, x.ended)) + '.</span><small>' + esc(dateHd(new Date(x.ended))) + ', ' + esc(clock(x.ended)) + '</small>';
      else h += '<b>Ongoing</b><span>Still down, ' + esc(dur(x.started)) + ' so far. Checked again every ' + st.every_minutes + ' minutes.</span><small>' + esc(dateHd(new Date())) + ', ' + esc(clock(new Date().toISOString())) + '</small>';
      h += '<b>Detected</b><span>' + esc(x.note ? x.note + " on two checks in a row." : "No answer on two checks in a row.") + '</span><small>' + esc(dateHd(new Date(x.started))) + ', ' + esc(clock(x.started)) + '</small></div></div>';
    });
    return h + '</div>';
  }
  var PAGE = 7, MAXD = 30, shown = S.shownDays || PAGE, html = "";
  for (var d = 0; d < Math.min(shown, MAXD); d++) html += dayBlock(d);
  var box = document.getElementById("incidents"); box.innerHTML = html;
  var more = document.getElementById("more");
  if (shown < MAXD) {
    var left = Math.min(PAGE, MAXD - shown);
    more.innerHTML = '<button type="button" class="pill" data-seed="9777"><span class="btn-svg"></span><span class="pill-in">Show the week before</span></button><span class="more-cap">' + (shown) + ' of ' + MAXD + ' days shown</span>';
    more.querySelector("button").addEventListener("click", function () { S.shownDays = shown + left; render(); });
    sketch(more.querySelector(".pill"));
  } else {
    more.innerHTML = '<span class="more-cap">All ' + MAXD + ' days of history shown.</span>';
  }
  document.querySelectorAll(".card.sk").forEach(sketch);
}
function themeInit() {
  var t = null; try { t = localStorage.getItem("triotheo-status-theme"); } catch (e) {}
  if (t === "dark" || t === "light") document.documentElement.setAttribute("data-theme", t);
  var b = document.getElementById("theme");
  function isDark() { var a = document.documentElement.getAttribute("data-theme"); return a === "dark" || (!a && matchMedia("(prefers-color-scheme: dark)").matches); }
  function draw() { var dark = isDark();
    b.querySelector(".btn-svg").innerHTML = coinSVG("var(--toggle-coin)", 9733);
    b.querySelector(".glyph").innerHTML = dark ? '<circle cx="12" cy="12" r="4.2" fill="none" stroke="currentColor" stroke-width="2.4"/><path d="M12 2.8v2.4M12 18.8v2.4M2.8 12h2.4M18.8 12h2.4M5.5 5.5l1.7 1.7M16.8 16.8l1.7 1.7M5.5 18.5l1.7-1.7M16.8 7.2l1.7-1.7" stroke="currentColor" stroke-width="2.4" stroke-linecap="round"/>'
      : '<path d="M15.8 3.2a8.6 8.6 0 1 0 5 13.4A7.2 7.2 0 0 1 15.8 3.2z" fill="none" stroke="currentColor" stroke-width="2.4" stroke-linejoin="round"/>';
    b.setAttribute("aria-label", dark ? "Switch to light" : "Switch to dark"); }
  b.addEventListener("click", function () { var next = isDark() ? "light" : "dark"; document.documentElement.setAttribute("data-theme", next); try { localStorage.setItem("triotheo-status-theme", next); } catch (e) {} draw(); });
  draw();
}
function load() {
  var q = "?t=" + Date.now();
  Promise.all(["status.json", "history.json", "incidents.json"].map(function (f) { return fetch(f + q, { cache: "no-store" }).then(function (r) { return r.ok ? r.json() : null; }).catch(function () { return null; }); }))
    .then(function (r) { S.status = r[0]; S.history = r[1] || []; S.incidents = r[2] || [];
      var ready = (document.fonts && document.fonts.ready) ? document.fonts.ready : Promise.resolve();
      ready.then(function () {
        if (!S.status) { document.getElementById("banner").innerHTML = '<p class="quiet">No check has run yet.</p>'; document.querySelectorAll(".card.sk").forEach(sketch); return; }
        render(); }); });
}
themeInit(); load(); setInterval(load, 120000);
"""

HTML = f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>TrioTheo Status</title>
<meta name="description" content="Is triotheo.com up right now? Live checks of the site, the Learn lessons, the API and the beta host, from outside the server.">
<meta name="robots" content="noindex">
<link rel="icon" type="image/png" sizes="96x96" href="{uri(FAV_PNG, 'image/png')}">
<link rel="icon" type="image/svg+xml" href="{uri(FAV_SVG, 'image/svg+xml')}">
<style>{CSS}</style>
</head>
<body>
<main class="page">
  <header class="brand">
    <span class="mark" aria-hidden="true"><img class="light" alt="" src="{uri(MARK, 'image/svg+xml')}"><img class="dark" alt="" src="{uri(MARK_DARK, 'image/svg+xml')}"></span>
    <div class="brand-text"><span class="eyebrow">TrioTheo</span><h1>Status</h1><p class="sub">Is triotheo.com up right now?</p></div>
    <button id="theme" class="theme" type="button" aria-label="Switch theme"><span class="btn-svg"></span><svg class="glyph" viewBox="0 0 24 24" aria-hidden="true"></svg></button>
  </header>
  <section id="banner" class="card banner" data-seed="9701"><span class="btn-svg"></span></section>
  <p id="checked" class="checked"></p>
  <section class="card sk" data-seed="9702" data-radius="20"><span class="btn-svg"></span><h2>Components</h2><div id="services"></div></section>
  <section class="card sk" data-seed="9703" data-radius="20"><span class="btn-svg"></span><h2>Past incidents</h2><div id="incidents"></div><div id="more" class="more"></div></section>
  <footer class="foot"><a href="https://triotheo.com/">&larr; triotheo.com</a><span>Checked from GitHub&rsquo;s runners and served from GitHub Pages, so this page stays up when the site does not.</span></footer>
</main>
<script>{PEN}</script>
<script>{JS}</script>
</body>
</html>
"""
(HERE / "index.html").write_text(HTML)
print(f"index.html: {len(HTML.encode()) // 1024} KB")

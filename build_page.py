#!/usr/bin/env python3
"""Generate index.html — the TrioTheo status page — from the design system's own pieces.

Self-contained on purpose: Trioscript (OFL), the doodle mark, the favicon and the pen ride inside the
file as data URIs, and the colour tokens are read out of scripts/owner_dashboard.py so the two cannot
drift. The page makes no request but for status.json, history.json and incidents.json beside it.
Usage: python3 build_page.py <triotheo repo root>   → writes index.html here. Never edit index.html.
"""
import base64, json, re, sys
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
# THE THEME COIN WEARS THE LANDING'S GLYPHS (owner note 2026-10-17): Landing.tsx SUN_D / MOON_D — seeds 5501 · 5502 ·
# 5507 through the landing's own jitterCircle — copied exactly. Regenerate them from that source if the landing's change.
SUN_D = "M 15.8 12.0 Q 15.8 12.0 15.5 12.9 Q 15.2 13.8 14.4 14.3 Q 13.6 14.8 12.8 15.3 Q 12.0 15.7 11.1 15.4 Q 10.2 15.1 9.3 14.6 Q 8.5 14.0 7.9 13.0 Q 7.3 12.0 8.0 11.1 Q 8.8 10.2 9.4 9.4 Q 10.0 8.6 11.0 8.2 Q 12.0 7.7 12.9 8.4 Q 13.7 9.0 14.7 9.5 Q 15.6 9.9 15.7 11.0 Z M 17.9 12.6 L 21.2 12.7 M 16.7 17.8 L 17.8 19.5 M 12.6 18.9 L 12.6 20.2 M 7.3 15.8 L 4.7 17.2 M 4.9 11.3 L 2.1 11.5 M 8.0 6.7 L 7.5 5.8 M 13.2 6.2 L 14.5 3.9 M 16.4 7.8 L 18.8 6.4"
MOON_D = "M 15.5 18.9 Q 15.5 18.9 14.4 19.1 Q 13.3 19.3 12.1 19.1 Q 10.9 18.9 9.3 19.0 Q 7.6 19.0 6.6 18.3 Q 5.5 17.5 5.3 16.4 Q 5.0 15.3 4.5 13.7 Q 4.1 12.1 4.5 10.6 Q 4.9 9.2 5.3 7.8 Q 5.7 6.5 7.2 5.8 Q 8.6 5.0 9.5 4.5 Q 10.5 4.0 11.8 4.1 Q 13.1 4.2 14.4 4.7 Q 15.7 5.3 16.5 5.4 Q 17.4 5.6 16.1 5.0 Q 14.9 4.5 13.7 4.3 Q 12.5 4.1 11.5 5.1 Q 10.6 6.1 9.9 6.6 Q 9.2 7.0 9.3 8.8 Q 9.4 10.5 9.6 11.2 Q 9.8 12.0 10.0 12.8 Q 10.2 13.6 11.3 14.6 Q 12.4 15.7 14.2 15.3 Q 15.9 15.0 16.5 14.7 Z"

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
.brand {{ display: flex; align-items: center; gap: 14px; margin-bottom: 22px; }}
.mark {{ width: 48px; height: 48px; flex: none; }}
.mark img {{ width: 100%; height: 100%; display: block; }}
.mark .dark {{ display: none; }}
@media (prefers-color-scheme: dark) {{ :root:not([data-theme="light"]) .mark .light {{ display: none; }} :root:not([data-theme="light"]) .mark .dark {{ display: block; }} }}
:root[data-theme="dark"] .mark .light {{ display: none; }} :root[data-theme="dark"] .mark .dark {{ display: block; }}
.eyebrow {{ display: block; font-size: 13px; font-weight: 800; letter-spacing: 0.08em; text-transform: uppercase; color: var(--label-purple); margin-bottom: 2px; }}
h1 {{ margin: 0; font-size: 30px; font-weight: 800; letter-spacing: 0.05em; line-height: 1.15; color: var(--headline-ink); text-wrap: balance; }}
.sub {{ margin: 4px 0 0; font-size: 15px; font-weight: 600; color: var(--muted); }}
.brand-text {{ min-width: 0; flex: 1; }}
/* THE HEADER IS THE SETTINGS PAGE'S ROW (owner ask 2026-10-16): a back coin on the left, the title, and the
   theme coin where the gear sits — both coins the profile header's own 54px (CoinBack's box), the back coin in
   CoinBack's dress (seed 9021 ghost in blue, ring 78% to black, chevron 60%), the theme coin in the toggle yarn */
.hcoin {{ flex: none; width: 54px; height: 54px; border: 0; background: none; padding: 0; cursor: pointer; position: relative; display: grid; place-items: center; text-decoration: none; }}
.hcoin .btn-svg {{ position: absolute; inset: 0; pointer-events: none; }}
.hcoin svg.glyph {{ position: relative; width: 32px; height: 32px; }}
/* THE THEME GLYPH IS THE LANDING'S (owner note 2026-10-17: "it needs to match what the light mode icon looks like on the
   TrioTheo landing page… the icon itself is too big"): its hand-drawn moon and sun at its 19px, 26px under 900px where the
   landing (and Learn) draw them bigger; plum on the purple coin, white lines in dark mode — the landing toggle's own rule */
.theme svg.glyph {{ width: 19px; height: 19px; }}
@media (max-width: 900px) {{ .theme svg.glyph {{ width: 26px; height: 26px; }} }}
.theme {{ color: #2d0f42; }}
@media (prefers-color-scheme: dark) {{ :root:not([data-theme="light"]) .theme {{ color: #ffffff; }} }}
:root[data-theme="dark"] .theme {{ color: #ffffff; }}
.back {{ color: color-mix(in srgb, var(--brand-blue) 60%, #000); }}
.coin .btn-svg {{ position: absolute; inset: 0; pointer-events: none; }}
/* the pen draws a card into a viewBox padded 6px on every side; the SVG's box is padded the same
   or `meet` fits the taller viewBox to a wide card's height and shrinks its width (measured) */
.card .btn-svg {{ position: absolute; inset: -6px; pointer-events: none; }}
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
/* in dark mode the green word lifts to the bright yarn — the 60% mark sank into the night ground (found on the 2026-10-17
   ride; the landing's footer coins carry the same lift for the same reason) */
@media (prefers-color-scheme: dark) {{ :root:not([data-theme="light"]) .status.up {{ color: var(--brand-green); }} }}
:root[data-theme="dark"] .status.up {{ color: var(--brand-green); }}
.coin {{ position: relative; flex: none; width: 18px; height: 18px; }}
/* THE DAY TUBES (owner note 2026-10-17: "make those the same design as we do for the progress bar pills… double-layered"):
   each day is Learn's progress-bar tube (SectionsView's DoodleBar) stood on its end — the sunken ground, the track's line
   and its second line slipped (1.6, 1.4) at 0.55, then the fill in the day's yarn with its ring. A day with no check is
   the empty tube. One SVG per strip, drawn at the strip's real width (the pen's rule) and redrawn when it changes. */
.days {{ position: relative; height: 34px; margin-top: 12px; }}
.days svg {{ position: absolute; left: -4px; top: -4px; overflow: visible; display: block; }}
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
.more {{ display: flex; align-items: center; justify-content: center; gap: 16px; margin-top: 14px; padding-top: 12px; border-top: 1.5px dashed var(--nav-border); }}
.pcoin {{ position: relative; width: 54px; height: 54px; border: 0; background: none; padding: 0; cursor: pointer; display: grid; place-items: center; flex: none; }}
.pcoin:disabled {{ cursor: default; }}
.pcoin .btn-svg {{ position: absolute; inset: 0; pointer-events: none; }}
.pcoin .glyph {{ position: relative; width: 32px; height: 32px; }}
.pcount {{ min-width: 64px; text-align: center; font-size: 15px; font-weight: 800; letter-spacing: 0.04em; color: var(--headline-ink); font-variant-numeric: tabular-nums; }}

.foot {{ margin-top: 28px; font-size: 14px; font-weight: 600; color: var(--muted); display: flex; flex-wrap: wrap; gap: 6px 18px; }}
.foot a {{ color: var(--brand-blue); text-decoration: none; font-weight: 800; }}
@media (max-width: 480px) {{ .page {{ padding: 24px 16px 64px; }} h1 {{ font-size: 26px; }} .banner-title {{ font-size: 20px; }} .days {{ height: 30px; }} .upd {{ grid-template-columns: 1fr; padding-left: 0; }} .upd small {{ grid-column: 1; }} }}
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
// pen.js's drawnStadium stood on its end — the same points, the same wobble (0.8), the tube a day is drawn as
function capsule(w, h, seed) {
  var r = w / 2;
  var pts = [[w, r], [w, h / 2], [w, h - r]]
    .concat(arcPts(r, h - r, r, r, 0, Math.PI, 5))
    .concat([[0, h - r], [0, h / 2], [0, r]])
    .concat(arcPts(r, r, r, r, Math.PI, 2 * Math.PI, 5));
  return wobblePath(pts, seed, 0.8, true);
}
function drawStrip(el) {
  var list = (S.strips || {})[el.dataset.id], W = el.clientWidth, H = el.clientHeight; if (!list || !W || !H) return;
  // a PILL, never a bean: a day's tube is at most 14px wide, centred in its thirtieth of the strip (at ~23px a slot on
  // a desktop a tube that filled it was nearly round), so the ends of the strip still meet "30 days ago" and "today"
  var n = list.length, slot = W / n, w = Math.min(slot - 3, 14), base = 9861 + (+el.dataset.seed) * 7, out = "";
  list.forEach(function (d, i) {
    var s = base + i * 13, yarn = YARN[d.cls], x = (i * slot + (slot - w) / 2).toFixed(1);
    out += '<g transform="translate(' + x + ' 0)"><title>' + esc(d.tip) + '</title>'
      + '<path d="' + capsule(w, H, s) + '" fill="var(--coin-ghost)"/>'
      + '<path d="' + capsule(w, H, s) + '" fill="none" stroke="var(--nav-border)" stroke-width="2.2" stroke-linecap="round"/>'
      + '<path d="' + capsule(w, H, s + 7) + '" fill="none" stroke="var(--nav-border)" stroke-width="2" stroke-linecap="round" opacity="0.55" transform="translate(1.6 1.4)"/>'
      + (yarn ? '<path d="' + capsule(w, H, s + 1) + '" fill="' + yarn + '" stroke="color-mix(in srgb, ' + yarn + ' 78%, #000000)" stroke-width="2" stroke-linecap="round"/>' : "")
      + '</g>';
  });
  el.innerHTML = '<svg width="' + (W + 8) + '" height="' + (H + 8) + '" viewBox="-4 -4 ' + (W + 8) + ' ' + (H + 8) + '" aria-hidden="true">' + out + '</svg>';
}
function drawStrips() {
  var box = document.getElementById("services");
  box.querySelectorAll(".days").forEach(drawStrip);
  // one observer for every strip: the rows are rebuilt each load, so an observer per strip would pile up
  if (!box.watched && window.ResizeObserver) { box.watched = true; new ResizeObserver(function () { box.querySelectorAll(".days").forEach(drawStrip); }).observe(box); }
}
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
    var list = days.map(function (k) { var b = byDay[k]; var cls = !b ? "" : b.d === 0 ? "up" : b.d === b.n ? "down" : "partial";
      return { cls: cls, tip: k + (b ? ": " + (b.n - b.d) + " of " + b.n + " checks up" : ": no checks") }; });
    (S.strips = S.strips || {})[id] = list;
    var tally = { up: 0, partial: 0, down: 0, "": 0 }; list.forEach(function (d) { tally[d.cls]++; });
    var said = [[tally.up, "all up"], [tally.partial, "partly down"], [tally.down, "down"], [tally[""], "with no checks"]]
      .filter(function (x) { return x[0]; }).map(function (x) { return x[0] + (x[0] === 1 ? " day " : " days ") + x[1]; }).join(", ");
    var strip = '<div class="days" data-id="' + esc(id) + '" data-seed="' + seed + '" role="img" aria-label="Last 30 days: ' + said + '"></div>';
    var seen = Object.keys(byDay).length;
    rows += '<div class="row"><div class="row-top"><span class="name">' + esc(s.name) + '</span>'
      + '<span class="status ' + s.state + '" title="' + (s.state === "up" ? s.ms + " ms" : esc(s.note || "no answer")) + '"><span class="coin" aria-hidden="true">' + coinSVG(YARN[s.state], seed += 13) + '</span>' + ROWWORD[s.state] + '</span></div>'
      + strip
      + '<div class="days-cap"><span>30 days ago</span><b>' + (pct === null ? "no checks yet" : pct + "% uptime over " + seen + (seen === 1 ? " day" : " days")) + '</b><span>today</span></div></div>';
  });
  document.getElementById("services").innerHTML = rows;
  drawStrips();
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
  var PAGE = 7, MAXD = 30, pages = Math.ceil(MAXD / PAGE), page = Math.min(Math.max(S.page || 0, 0), pages - 1), html = "";
  for (var d = page * PAGE; d < Math.min((page + 1) * PAGE, MAXD); d++) html += dayBlock(d);
  document.getElementById("incidents").innerHTML = html;
  // THE PAGER — a back coin and a forward coin in CoinBack's dress with the count between them; the coin
  // with nowhere to go is ghosted, never hidden (a hidden control reads as a bug — the house rule)
  var more = document.getElementById("more");
  more.innerHTML = '<button type="button" class="pcoin" data-dir="-1" aria-label="Newer week"' + (page === 0 ? " disabled" : "") + '><span class="btn-svg"></span><svg class="glyph" viewBox="0 0 24 24" aria-hidden="true"><path d="' + CHEV_L + '" fill="none" stroke="currentColor" stroke-width="2.6" stroke-linecap="round" stroke-linejoin="round"/></svg></button>'
    + '<span class="pcount">' + (page + 1) + ' of ' + pages + '</span>'
    + '<button type="button" class="pcoin is-right" data-dir="1" aria-label="Older week"' + (page === pages - 1 ? " disabled" : "") + '><span class="btn-svg"></span><svg class="glyph" viewBox="0 0 24 24" aria-hidden="true"><path d="' + CHEV_L + '" fill="none" stroke="currentColor" stroke-width="2.6" stroke-linecap="round" stroke-linejoin="round" transform="translate(24 0) scale(-1 1)"/></svg></button>';
  more.querySelectorAll(".pcoin").forEach(function (b) {
    coinInto(b, "var(--brand-blue)", b.disabled);
    b.addEventListener("click", function () { S.page = page + (+b.dataset.dir); render(); });
  });
  document.querySelectorAll(".card.sk").forEach(sketch);
}
// CoinBack, as the Learn app draws it: a ghost coin at seed 9021 in the family yarn, the ring the yarn's 78%
// dark variant, the chevron DoodleChevronLeft's own points at its own seed (9601, amp 0.35) in the 60% mark
var CHEV_L = wobblePath([[14.6, 5.4], [11.2, 8.7], [7.8, 12], [11.2, 15.3], [14.6, 18.6]], 9601, 0.35);
function coinInto(el, yarn, ghost) {
  var ring = "color-mix(in srgb, " + yarn + " 78%, #000000)", box = 68, r = 26;
  var fill = ghost ? "var(--coin-ghost)" : yarn, stroke = ghost ? "var(--nav-border)" : ring;
  el.querySelector(".btn-svg").innerHTML = '<svg viewBox="0 0 ' + box + ' ' + box + '" aria-hidden="true" style="' + SVG_STYLE + '">'
    + '<path d="' + jitterCircle(r, box, 9021 + 3, 1.3) + '" fill="' + fill + '" transform="translate(3.2 2.8)"/>'
    + '<path d="' + jitterCircle(r, box, 9021, 1.6) + '" fill="none" stroke="' + stroke + '" stroke-width="2.6" stroke-linecap="round"/></svg>';
  el.style.color = ghost ? "var(--divider-ink)" : "color-mix(in srgb, " + yarn + " 60%, #000000)";
}
function backInit() {
  var a = document.getElementById("back"), yarn = "var(--brand-blue)", ring = "color-mix(in srgb, " + yarn + " 78%, #000000)";
  var box = 68, r = 26;
  a.querySelector(".btn-svg").innerHTML = '<svg viewBox="0 0 ' + box + ' ' + box + '" aria-hidden="true" style="' + SVG_STYLE + '">'
    + '<path d="' + jitterCircle(r, box, 9021 + 3, 1.3) + '" fill="' + yarn + '" transform="translate(3.2 2.8)"/>'
    + '<path d="' + jitterCircle(r, box, 9021, 1.6) + '" fill="none" stroke="' + ring + '" stroke-width="2.6" stroke-linecap="round"/></svg>';
  a.querySelector(".glyph").innerHTML = '<path d="' + CHEV_L + '" stroke="currentColor" stroke-width="2.6" stroke-linecap="round" stroke-linejoin="round" fill="none"/>';
}
function themeInit() {
  var t = null; try { t = localStorage.getItem("triotheo-status-theme"); } catch (e) {}
  if (t === "dark" || t === "light") document.documentElement.setAttribute("data-theme", t);
  var b = document.getElementById("theme");
  function isDark() { var a = document.documentElement.getAttribute("data-theme"); return a === "dark" || (!a && matchMedia("(prefers-color-scheme: dark)").matches); }
  function draw() { var dark = isDark();
    b.querySelector(".btn-svg").innerHTML = coinSVG("var(--toggle-coin)", 9733);
    b.querySelector(".glyph").innerHTML = '<path d="' + (dark ? SUN_D : MOON_D) + '"/>';
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
backInit(); themeInit(); load(); setInterval(load, 120000);
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
    <a id="back" class="hcoin back" href="https://triotheo.com/" aria-label="Back to triotheo.com" title="Back to triotheo.com"><span class="btn-svg"></span><svg class="glyph" viewBox="0 0 24 24" aria-hidden="true"></svg></a>
    <span class="mark" aria-hidden="true"><img class="light" alt="" src="{uri(MARK, 'image/svg+xml')}"><img class="dark" alt="" src="{uri(MARK_DARK, 'image/svg+xml')}"></span>
    <div class="brand-text"><span class="eyebrow">TrioTheo</span><h1>Status</h1><p class="sub">Is triotheo.com up right now?</p></div>
    <button id="theme" class="hcoin theme" type="button" aria-label="Switch theme"><span class="btn-svg"></span><svg class="glyph" viewBox="0 0 24 24" aria-hidden="true" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"></svg></button>
  </header>
  <section id="banner" class="card banner" data-seed="9701"><span class="btn-svg"></span></section>
  <p id="checked" class="checked"></p>
  <section class="card sk" data-seed="9702" data-radius="20"><span class="btn-svg"></span><h2>Components</h2><div id="services"></div></section>
  <section class="card sk" data-seed="9703" data-radius="20"><span class="btn-svg"></span><h2>Past incidents</h2><div id="incidents"></div><div id="more" class="more"></div></section>
  <footer class="foot"><span>Checked from GitHub&rsquo;s runners and served from GitHub Pages, so this page stays up when the site does not.</span></footer>
</main>
<script>{PEN}</script>
<script>var SUN_D = {json.dumps(SUN_D)}, MOON_D = {json.dumps(MOON_D)};</script>
<script>{JS}</script>
</body>
</html>
"""
(HERE / "index.html").write_text(HTML)
print(f"index.html: {len(HTML.encode()) // 1024} KB")

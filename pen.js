/* THE PEN — ported verbatim from scripts/owner_dashboard.py (itself a port of the Learn app's
   drawnChrome / CoinChrome at the same seeds). Edit there, re-extract here; never by hand. */
var SVG_STYLE = "position:absolute;inset:0;width:100%;height:100%;overflow:visible";

function mulberry(seed) { var s = seed >>> 0; return function () { return (s = (s * 1664525 + 1013904223) >>> 0) / 4294967296; }; }

function arcPts(cx, cy, rx, ry, a0, a1, n) {
  var out = [];
  for (var i = 0; i <= n; i++) { var a = a0 + (a1 - a0) * (i / n); out.push([cx + rx * Math.cos(a), cy + ry * Math.sin(a)]); }
  return out;
}

function jitterRect(w, h, r, seed, amp) {
  if (amp === undefined) amp = 2.2;
  var rnd = mulberry(seed), pts = [];
  var seg = function (x1, y1, x2, y2, n) { for (var i = 0; i < n; i++) { var t = i / n; pts.push([x1 + (x2 - x1) * t, y1 + (y2 - y1) * t]); } };
  var arc = function (cx, cy, a0, a1, n) { for (var i = 0; i < n; i++) { var a = a0 + (a1 - a0) * (i / n); pts.push([cx + r * Math.cos(a), cy + r * Math.sin(a)]); } };
  var nTop = Math.max(6, Math.round((w - 2 * r) / 22)), nSide = Math.max(3, Math.round((h - 2 * r) / 22));
  seg(r, 0, w - r, 0, nTop); arc(w - r, r, -Math.PI / 2, 0, 3);
  seg(w, r, w, h - r, nSide); arc(w - r, h - r, 0, Math.PI / 2, 3);
  seg(w - r, h, r, h, nTop); arc(r, h - r, Math.PI / 2, Math.PI, 3);
  seg(0, h - r, 0, r, nSide); arc(r, r, Math.PI, 1.5 * Math.PI, 3);
  var j = pts.map(function (p) { return [p[0] + (rnd() - 0.5) * 2 * amp, p[1] + (rnd() - 0.5) * 2 * amp]; });
  var d = "M " + j[0][0].toFixed(1) + " " + j[0][1].toFixed(1);
  for (var i = 1; i < j.length; i++) {
    var px = j[i - 1][0], py = j[i - 1][1], x = j[i][0], y = j[i][1];
    d += " Q " + px.toFixed(1) + " " + py.toFixed(1) + " " + ((px + x) / 2).toFixed(1) + " " + ((py + y) / 2).toFixed(1);
  }
  return d + " Z";
}

function jitterCircle(r, box, seed, amp) {
  if (amp === undefined) amp = 2;
  var rnd = mulberry(seed), n = Math.max(12, Math.round((2 * Math.PI * r) / 10)), c = box / 2, pts = [];
  for (var i = 0; i < n; i++) { var a = (2 * Math.PI * i) / n, rr = r + (rnd() - 0.5) * 2 * amp; pts.push([c + rr * Math.cos(a), c + rr * Math.sin(a)]); }
  var mx = (pts[n - 1][0] + pts[0][0]) / 2, my = (pts[n - 1][1] + pts[0][1]) / 2;
  var d = "M " + mx.toFixed(1) + " " + my.toFixed(1);
  for (var k = 0; k < n; k++) {
    var p = pts[k], q = pts[(k + 1) % n];
    d += " Q " + p[0].toFixed(1) + " " + p[1].toFixed(1) + " " + ((p[0] + q[0]) / 2).toFixed(1) + " " + ((p[1] + q[1]) / 2).toFixed(1);
  }
  return d + " Z";
}

function wobblePath(pts, seed, amp, close) {
  if (amp === undefined) amp = 0.7;
  var rnd = mulberry(seed);
  var j = pts.map(function (p) { return [p[0] + (rnd() - 0.5) * 2 * amp, p[1] + (rnd() - 0.5) * 2 * amp]; });
  var d = "M " + j[0][0].toFixed(1) + " " + j[0][1].toFixed(1);
  for (var i = 1; i < j.length; i++) {
    var px = j[i - 1][0], py = j[i - 1][1], x = j[i][0], y = j[i][1];
    d += " Q " + px.toFixed(1) + " " + py.toFixed(1) + " " + ((px + x) / 2).toFixed(1) + " " + ((py + y) / 2).toFixed(1);
  }
  var l = j[j.length - 1];
  d += " L " + l[0].toFixed(1) + " " + l[1].toFixed(1);
  return d + (close ? " Z" : "");
}

function drawnStadium(w, h, seed) {
  var r = h / 2;
  var pts = [[r, 0], [w / 2, 0], [w - r, 0]]
    .concat(arcPts(w - r, r, r, r, -Math.PI / 2, Math.PI / 2, 5))
    .concat([[w - r, h], [w / 2, h], [r, h]])
    .concat(arcPts(r, r, r, r, Math.PI / 2, 1.5 * Math.PI, 5));
  return wobblePath(pts, seed, 0.8, true);
}

function once(el, render, bind) {
  if (el.redraw) { el.redraw(); return; }
  el.redraw = render;
  render();
  if (window.ResizeObserver) new ResizeObserver(render).observe(el);
  if (bind) bind();
}

function sketch(el) {
  var wrap = el.querySelector(".btn-svg"), seed = +el.dataset.seed, radius = +(el.dataset.radius || 16);
  var ink = el.dataset.ink || "var(--border-strong)";
  once(el, function () {
    var w = el.offsetWidth, h = el.offsetHeight; if (!w || !h) return;
    var rr = Math.min(radius, h / 2 - 1);
    var d1 = jitterRect(w, h, rr, seed, 1.3), d2 = jitterRect(w, h, rr, seed + 7, 1.2);
    wrap.innerHTML = '<svg viewBox="-6 -6 ' + (w + 12) + ' ' + (h + 12) + '" aria-hidden="true" style="' + SVG_STYLE + '">'
      + '<path d="' + d1 + '" fill="none" stroke="' + ink + '" stroke-width="2.6" stroke-linecap="round" stroke-linejoin="round"/>'
      + '<path d="' + d2 + '" fill="none" stroke="' + ink + '" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round" opacity="0.6" transform="translate(1.3 1.1)"/>'
      + '</svg>';
  });
}

function tube(el) {
  var seed = +el.dataset.seed, yarn = el.dataset.yarn, pct = +el.dataset.pct, H = 20;
  var ring = "color-mix(in srgb, " + yarn + " 80%, #000000)";
  once(el, function () {
    var w = el.offsetWidth; if (!w) return;
    var svg = '<svg viewBox="-4 -4 ' + (w + 8) + ' ' + (H + 8) + '" aria-hidden="true">'
      + '<path d="' + drawnStadium(w, H, seed) + '" fill="var(--coin-ghost)"/>'
      + '<path d="' + drawnStadium(w, H, seed) + '" fill="none" stroke="var(--nav-border)" stroke-width="2.2" stroke-linecap="round"/>'
      + '<path d="' + drawnStadium(w, H, seed + 7) + '" fill="none" stroke="var(--nav-border)" stroke-width="2" stroke-linecap="round" opacity="0.55" transform="translate(1.6 1.4)"/>';
    if (pct > 0) {
      var fw = Math.max(H, Math.round((pct / 100) * w));
      svg += '<path d="' + drawnStadium(fw, H, seed + 1) + '" fill="' + yarn + '" stroke="' + ring + '" stroke-width="2" stroke-linecap="round"/>';
    }
    el.innerHTML = svg + '</svg>';
  });
}

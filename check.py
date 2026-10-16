#!/usr/bin/env python3
"""Probe triotheo.com from outside the box and keep the status page's data (stdlib only).

Why this exists: on 2026-10-16 the production VPS was powered off by its host for ten minutes and
nobody would have known — the outage was seen only because a deploy check happened to be running.
This runs on GitHub's runners on a schedule (see .github/workflows/uptime.yml), so it keeps working
when the box does not, and the page it feeds is served by GitHub Pages — never by the box it reports.

What it writes, beside itself:
  status.json     the latest verdict per service (what the page shows at the top)
  history.json    one entry per check, kept for HISTORY_DAYS (the uptime tubes and the day strips)
  incidents.json  every transition down→up with its duration (the incident list)
  notify.txt      ONLY when something should be said on Discord — the workflow posts it and deletes it

Two rules that keep it honest and quiet:
  · a probe is retried PROBE_TRIES times with a pause before it counts as failed this run, and a
    service is called DOWN only when it failed on two CONSECUTIVE runs — GitHub's runners are
    intermittently blocked at the host's edge, and one unlucky run is not an outage;
  · a lesson manifest is one of the probes, because the site can be up while the volume readers
    are served from is stale (#1182) — the content-type must be JSON, not the SPA fallback's HTML.
"""
from __future__ import annotations

import json
import sys
import time
import urllib.error
import urllib.request
from datetime import datetime, timedelta, timezone
from pathlib import Path

HERE = Path(__file__).resolve().parent
SERVICES = [
    # id, name, url, what must be true of the answer
    ("site",    "triotheo.com",     "https://triotheo.com/",                       {"status": 200, "ctype": "text/html"}),
    ("api",     "API",              "https://triotheo.com/api/health",             {"status": 200}),
    ("lessons", "Learn lessons",    "https://triotheo.com/learn/guess_who/guess-lazarus/manifest.json",
                                                                                  {"status": 200, "ctype": "application/json"}),
    ("beta",    "beta.triotheo.com", "https://beta.triotheo.com/",                 {"status": 200}),
]
PROBE_TRIES, PROBE_PAUSE, TIMEOUT = 3, 8, 20
HISTORY_DAYS = 30


def probe(url: str, want: dict) -> tuple[bool, int, str]:
    """(ok, latency_ms, note) — ok only if every expectation holds on some try."""
    note = ""
    for attempt in range(PROBE_TRIES):
        t0 = time.monotonic()
        try:
            req = urllib.request.Request(url, headers={"User-Agent": "triotheo-status/1 (+https://triotheo.com)",
                                                       "Cache-Control": "no-cache"})
            with urllib.request.urlopen(req, timeout=TIMEOUT) as r:
                status, ctype = r.status, (r.headers.get("content-type") or "").lower()
                r.read(2048)
        except urllib.error.HTTPError as e:
            status, ctype = e.code, ""
        except Exception as e:  # noqa: BLE001 — a timeout or a reset is a verdict, not a crash
            status, ctype = 0, f"error: {type(e).__name__}"
        ms = int((time.monotonic() - t0) * 1000)
        ok = status == want["status"] and (want.get("ctype", "") in ctype)
        if ok:
            return True, ms, ""
        note = f"{status or 'no answer'} {ctype}".strip()
        if attempt < PROBE_TRIES - 1:
            time.sleep(PROBE_PAUSE)
    return False, ms, note


def load(name: str, default):
    p = HERE / name
    try:
        return json.loads(p.read_text())
    except (OSError, ValueError):
        return default


def main() -> int:
    now = datetime.now(timezone.utc).replace(microsecond=0)
    prev = load("status.json", {})
    prev_raw = (prev.get("raw") or {})
    prev_state = {k: v.get("state") for k, v in (prev.get("services") or {}).items()}

    raw, services = {}, {}
    for sid, name, url, want in SERVICES:
        ok, ms, note = probe(url, want)
        raw[sid] = ok
        # DOWN needs two consecutive failed runs; UP is immediate (a recovery is good news at once)
        down = (not ok) and (prev_raw.get(sid) is False)
        services[sid] = {"name": name, "url": url, "state": "down" if down else "up",
                         "ok_this_run": ok, "ms": ms, "note": note}

    overall = "down" if all(s["state"] == "down" for s in services.values()) else \
              "partial" if any(s["state"] == "down" for s in services.values()) else "up"
    status = {"checked_at": now.isoformat(), "overall": overall, "services": services, "raw": raw,
              "every_minutes": 10, "source": "GitHub Actions runners"}
    (HERE / "status.json").write_text(json.dumps(status, indent=1) + "\n")

    history = load("history.json", [])
    history.append({"t": now.isoformat(), "s": {k: v["state"] for k, v in services.items()},
                    "ms": {k: v["ms"] for k, v in services.items()}})
    cutoff = (now - timedelta(days=HISTORY_DAYS)).isoformat()
    history = [h for h in history if h["t"] >= cutoff]
    (HERE / "history.json").write_text(json.dumps(history, separators=(",", ":")) + "\n")

    incidents = load("incidents.json", [])
    said = []
    for sid, s in services.items():
        was, is_ = prev_state.get(sid), s["state"]
        if was == is_ or was is None:
            continue
        if is_ == "down":
            incidents.append({"service": sid, "name": s["name"], "started": now.isoformat(), "ended": None, "note": s["note"]})
            said.append(f"🔴 **{s['name']} is down** — {s['note'] or 'no answer'} on two checks in a row")
        else:
            for inc in reversed(incidents):
                if inc["service"] == sid and inc["ended"] is None:
                    inc["ended"] = now.isoformat()
                    mins = int((now - datetime.fromisoformat(inc["started"])).total_seconds() // 60)
                    said.append(f"🟢 **{s['name']} is back** after about {mins} min")
                    break
            else:
                said.append(f"🟢 **{s['name']} is back**")
    (HERE / "incidents.json").write_text(json.dumps(incidents[-200:], indent=1) + "\n")
    if said:
        msg = "**triotheo.com status**\n" + "\n".join(said)
        if len(sys.argv) > 1:
            msg += f"\n<https://{sys.argv[1]}>"
        (HERE / "notify.txt").write_text(msg)

    line = "  ".join(f"{k}:{'up' if v['ok_this_run'] else 'FAIL'}({v['ms']}ms)" for k, v in services.items())
    print(f"{now.isoformat()}  overall={overall}  {line}" + ("  → notify" if said else ""))
    return 0


if __name__ == "__main__":
    sys.exit(main())

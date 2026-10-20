#!/usr/bin/env python3
"""Local preview of dist/ with clean URLs, auto-rebuild and live reload.

Save any file in content/, assets/, zogam-favicons/ or the data/config files and the site
rebuilds. Open pages reload themselves. Usage: python3 scripts/serve_dist.py [port]
"""
import http.server, os, subprocess, sys, threading, time
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
ROOT = str(REPO / "dist")
PORT = int(sys.argv[1]) if len(sys.argv) > 1 else 8080
WATCH_DIRS = ["content", "assets", "zogam-favicons"]
WATCH_FILES = ["build.py", "photos.json", "sources.json", "page-dates.json"]
RELOAD_JS = (b'<script>(function(){var r=null;setInterval(function(){fetch("/__rev",{cache:"no-store"})'
             b'.then(function(x){return x.text()}).then(function(t){if(r===null)r=t;else if(t!==r)location.reload();})'
             b'.catch(function(){});},1000);})();</script>')

state = {"rev": 0}

def source_signature():
    paths = [p for d in WATCH_DIRS for p in (REPO / d).rglob("*") if p.is_file()]
    paths += [REPO / f for f in WATCH_FILES if (REPO / f).exists()]
    return tuple(sorted((str(p), p.stat().st_mtime_ns, p.stat().st_size) for p in paths))

def stamp():
    return time.strftime("%H:%M:%S")

def build():
    # --no-upload: a preview rebuild on every save must never push files to R2
    r = subprocess.run([sys.executable, str(REPO / "build.py"), "--no-upload"], cwd=REPO, capture_output=True, text=True)
    if r.returncode == 0:
        state["rev"] += 1
        print(f"[{stamp()}] rebuilt", flush=True)
    else:
        print(f"[{stamp()}] BUILD FAILED, still showing the last good build\n{r.stdout}{r.stderr}", flush=True)

def watch():
    last = source_signature()
    while True:
        time.sleep(1)
        try:
            now = source_signature()
        except FileNotFoundError:
            continue  # a file was renamed mid-scan; try again next tick
        if now != last:
            last = now
            time.sleep(0.3)  # let the editor finish writing
            build()

class Handler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=ROOT, **kwargs)

    def translate_path(self, path):
        p = super().translate_path(path)
        if not os.path.exists(p) and os.path.exists(p + ".html"):
            return p + ".html"
        return p

    def send_body(self, body, ctype):
        self.send_response(200)
        self.send_header("Content-Type", ctype)
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Cache-Control", "no-store")
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self):
        if self.path.split("?")[0] == "/__rev":
            return self.send_body(str(state["rev"]).encode(), "text/plain")
        path = self.translate_path(self.path.split("?")[0])
        if os.path.isdir(path):
            path = os.path.join(path, "index.html")
        if path.endswith(".html") and os.path.isfile(path):
            body = Path(path).read_bytes().replace(b"</body>", RELOAD_JS + b"</body>", 1)
            return self.send_body(body, "text/html; charset=utf-8")
        super().do_GET()

    def log_message(self, *args):
        pass

if __name__ == "__main__":
    build()
    threading.Thread(target=watch, daemon=True).start()
    print(f"Serving {ROOT} at http://localhost:{PORT} (auto-rebuild on)", flush=True)
    http.server.ThreadingHTTPServer(("127.0.0.1", PORT), Handler).serve_forever()

"""Developer dashboard server. Standard library only.

Run: python3 -m demo.server   (from the demo/ folder)
Then open http://127.0.0.1:8001

Endpoints (all tenant-scoped; a tenant_id is required and validated):
- GET  /api/tenants
- POST /api/sync   {tenant_id}
- POST /api/qa     {tenant_id, question}
- POST /api/review {tenant_id, audio, approved}
- GET  /api/benchmark  (last benchmark_report.json, if any)
The dashboard page is intentionally plain: it is a developer tool,
not a household product UI.
"""
from __future__ import annotations

import json
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

from .benchmark import run_all
from .drive import sync
from .qa import answer
from .store import chunk_count
from .tenants import TENANT_IDS, load_json
from .transcribe import list_audio_fixtures, review_transcript

BASE = Path(__file__).resolve().parent.parent

DASHBOARD = """<!doctype html><html><head><meta charset="utf-8">
<title>DeepFamily Developer Demo</title></head><body>
<h1>DeepFamily Developer Demo — 1 host, 5 isolated tenants</h1>
<p>Test data only. Mock Drive / transcript / LLM. Real: isolation, sync, retrieval, citations.</p>
<h2>Tenants</h2><ul id="tenants"></ul>
<h2>Ask a question</h2>
<p>Tenant: <select id="tenant"></select>
<input id="q" size="60" placeholder="e.g. When did grandmother open the noodle stall?">
<button onclick="ask()">Ask</button></p><pre id="out"></pre>
<h2>Benchmark</h2><button onclick="bench()">Run benchmark (1 / 3 / 5 concurrent)</button>
<pre id="bench"></pre>
<script>
async function load(){const t=await (await fetch('/api/tenants')).json();
document.getElementById('tenants').innerHTML=t.map(x=>`<li>${x.tenant_id}: ${x.chunks} chunks, audio fixtures: ${x.audio.join(', ')||'none'}</li>`).join('');
document.getElementById('tenant').innerHTML=t.map(x=>`<option>${x.tenant_id}</option>`).join('');}
async function ask(){const r=await fetch('/api/qa',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({tenant_id:document.getElementById('tenant').value,question:document.getElementById('q').value})});document.getElementById('out').textContent=JSON.stringify(await r.json(),null,2);}
async function bench(){document.getElementById('bench').textContent='running…';const r=await fetch('/api/benchmark',{method:'POST'});document.getElementById('bench').textContent=JSON.stringify(await r.json(),null,2);}
load();
</script></body></html>
"""


class Handler(BaseHTTPRequestHandler):
    def _json(self, value, status=200):
        body = json.dumps(value, ensure_ascii=False, indent=2).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def _body(self):
        length = int(self.headers.get("Content-Length") or 0)
        return json.loads(self.rfile.read(length) or b"{}") if length else {}

    def do_GET(self):
        if self.path == "/":
            body = DASHBOARD.encode("utf-8")
            self.send_response(200)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.send_header("Content-Length", str(len(body)))
            self.end_headers()
            self.wfile.write(body)
        elif self.path == "/api/tenants":
            self._json([{
                "tenant_id": tid,
                "chunks": chunk_count(tid),
                "audio": [p.name for p in list_audio_fixtures(tid)],
            } for tid in TENANT_IDS])
        elif self.path == "/api/benchmark":
            report = load_json(BASE / "benchmark_report.json", {})
            self._json(report)
        else:
            self._json({"error": "not found"}, 404)

    def do_POST(self):
        try:
            data = self._body()
            if self.path == "/api/sync":
                self._json(sync(data["tenant_id"]))
            elif self.path == "/api/qa":
                self._json(answer(data["tenant_id"], data["question"]))
            elif self.path == "/api/review":
                self._json(review_transcript(data["tenant_id"], data["audio"], bool(data["approved"])))
            elif self.path == "/api/benchmark":
                self._json(run_all())
            else:
                self._json({"error": "not found"}, 404)
        except (ValueError, FileNotFoundError, KeyError) as exc:
            self._json({"error": str(exc)}, 400)

    def log_message(self, *args):  # keep terminal output readable
        pass


def main() -> None:
    server = ThreadingHTTPServer(("127.0.0.1", 8001), Handler)
    print("DeepFamily developer demo at http://127.0.0.1:8001 (Ctrl-C to stop)")
    server.serve_forever()


if __name__ == "__main__":
    main()

"""Stdlib-only HTTP API — no FastAPI install needed.
GET /health, POST /research (JSON = pipeline input contract), GET /demo.
Run: python -m analyst.server  (port 8000)"""
import json
from http.server import BaseHTTPRequestHandler, HTTPServer

from .cli import DEMO
from .pipeline import run


class H(BaseHTTPRequestHandler):
    def _send(self, obj, code=200):
        body = json.dumps(obj).encode(); self.send_response(code)
        self.send_header("Content-Type", "application/json"); self.send_header("Content-Length", str(len(body))); self.end_headers(); self.wfile.write(body)
    def do_GET(self):
        if self.path == "/health": self._send({"status": "ok", "spend_usd": 0})
        elif self.path == "/demo": self._send(run(DEMO))
        else: self._send({"error": "unknown route"}, 404)
    def do_POST(self):
        if self.path != "/research": return self._send({"error": "unknown route"}, 404)
        try:
            data = json.loads(self.rfile.read(int(self.headers.get("Content-Length", 0))))
            self._send(run(data))
        except Exception as e: self._send({"error": str(e)}, 422)
    def log_message(self, *a): pass
def serve(port=8000): HTTPServer(("127.0.0.1", port), H).serve_forever()
if __name__ == "__main__": serve()

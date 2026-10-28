"""HTTP server behaviour, tested in-process on an ephemeral port.
Stdlib only (http.client + threading), offline, no fixed port: the
server module's serve() binds port 8000, so tests build HTTPServer
directly around the same handler class instead.
"""
import http.client
import json
import threading
from http.server import HTTPServer

from analyst.cli import DEMO
from analyst.server import H


def _start_server():
    server = HTTPServer(("127.0.0.1", 0), H)
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    return server, server.server_address[1]


def _request(port, method, path, body=None):
    conn = http.client.HTTPConnection("127.0.0.1", port, timeout=5)
    try:
        conn.request(method, path, body=body,
                     headers={"Content-Type": "application/json"})
        response = conn.getresponse()
        return response.status, response.getheader("Content-Type"), \
            response.read()
    finally:
        conn.close()


def test_health_endpoint():
    server, port = _start_server()
    try:
        status, content_type, body = _request(port, "GET", "/health")
        assert status == 200
        assert content_type == "application/json"
        assert json.loads(body) == {"status": "ok", "spend_usd": 0}
    finally:
        server.shutdown()


def test_unknown_get_route_is_404():
    server, port = _start_server()
    try:
        status, _, body = _request(port, "GET", "/nope")
        assert status == 404
        assert json.loads(body) == {"error": "unknown route"}
    finally:
        server.shutdown()


def test_demo_endpoint_runs_pipeline():
    server, port = _start_server()
    try:
        status, _, body = _request(port, "GET", "/demo")
        assert status == 200
        result = json.loads(body)
        assert result["audit_valid"] is True
        assert "verdict" in result["debate"]
    finally:
        server.shutdown()


def test_research_endpoint_accepts_demo_input():
    server, port = _start_server()
    try:
        status, _, body = _request(
            port, "POST", "/research", body=json.dumps(DEMO))
        assert status == 200
        result = json.loads(body)
        assert result["audit_valid"] is True
        assert result["company_type"] == "stable"
    finally:
        server.shutdown()


def test_research_rejects_malformed_json_with_422():
    server, port = _start_server()
    try:
        status, _, body = _request(port, "POST", "/research",
                                   body="{not json")
        assert status == 422
        assert "error" in json.loads(body)
    finally:
        server.shutdown()


def test_research_rejects_missing_prices_with_422():
    # An input without the required "prices" key raises inside run();
    # the handler must turn that into a 422, not a crash or a 200.
    server, port = _start_server()
    try:
        status, _, body = _request(port, "POST", "/research",
                                   body=json.dumps({}))
        assert status == 422
        assert "prices" in json.loads(body)["error"]
    finally:
        server.shutdown()


def test_research_unknown_route_is_404():
    server, port = _start_server()
    try:
        status, _, body = _request(port, "POST", "/other",
                                   body=json.dumps(DEMO))
        assert status == 404
    finally:
        server.shutdown()

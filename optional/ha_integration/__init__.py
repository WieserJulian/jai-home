# Optional Home Assistant API integration stub
# This module is deliberately minimal – it only demonstrates how the
# JAI Home service could expose a simple HTTP endpoint that Home Assistant
# could call. Users can extend it with real functionality.

import os
from http.server import BaseHTTPRequestHandler, HTTPServer
import json

class SimpleHAHandler(BaseHTTPRequestHandler):
    def _respond(self, payload, code=200):
        self.send_response(code)
        self.send_header('Content-Type', 'application/json')
        self.end_headers()
        self.wfile.write(json.dumps(payload).encode())

    def do_GET(self):
        if self.path == "/status":
            self._respond({"status": "running", "ha_enabled": bool(os.getenv("ENABLE_HA"))})
        else:
            self._respond({"error": "unknown endpoint"}, code=404)

def run_server(port: int = 8123):
    server = HTTPServer(("0.0.0.0", port), SimpleHAHandler)
    print(f"[HA integration] listening on http://0.0.0.0:{port}/status")
    server.serve_forever()

if __name__ == "__main__":
    run_server()

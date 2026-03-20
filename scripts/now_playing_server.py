#!/usr/bin/env python3
"""
now_playing_server.py — Simple HTTP server on port 18791.
Serves TITAN's now_playing.json so Unraid Bob can pull it
without needing node invoke / system.run.

GET /            → returns now_playing.json as JSON
GET /health      → returns {"status": "ok"}
"""

import json
import os
from http.server import BaseHTTPRequestHandler, HTTPServer

PORT = 18791
NOW_PLAYING = r"C:\Users\McFex\.openclaw\workspace\music_together\now_playing.json"


class Handler(BaseHTTPRequestHandler):
    def log_message(self, format, *args):
        pass  # Suppress request logs

    def do_GET(self):
        if self.path == "/health":
            self._respond(200, {"status": "ok"})
        elif self.path in ("/", "/now_playing"):
            try:
                with open(NOW_PLAYING, "r", encoding="utf-8") as f:
                    data = json.load(f)
                # Check staleness — if widget hasn't updated in 10 min, session is dead
                updated_at = data.get("updated_at", "")
                if updated_at:
                    from datetime import datetime, timezone
                    try:
                        dt = datetime.fromisoformat(updated_at.replace("Z", "+00:00"))
                        age = (datetime.now(timezone.utc) - dt).total_seconds()
                        if age > 600:
                            self._respond(404, {"error": "session_ended", "age_seconds": int(age)})
                            return
                    except Exception:
                        pass
                self._respond(200, data)
            except FileNotFoundError:
                self._respond(404, {"error": "now_playing.json not found"})
            except Exception as e:
                self._respond(500, {"error": str(e)})
        else:
            self._respond(404, {"error": "not found"})

    def _respond(self, code, data):
        body = json.dumps(data).encode("utf-8")
        self.send_response(code)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)


if __name__ == "__main__":
    server = HTTPServer(("0.0.0.0", PORT), Handler)
    print(f"now_playing_server running on port {PORT}")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("Stopped.")

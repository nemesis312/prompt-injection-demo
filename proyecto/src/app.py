"""truck-tracker-api: servidor mínimo con la librería estándar."""
import json
from http.server import BaseHTTPRequestHandler, HTTPServer

TRUCKS = [{"id": 1, "nombre": "El Jibarito Sobre Ruedas", "pueblo": "Caguas"}]


class Handler(BaseHTTPRequestHandler):
    def _send(self, code, body):
        data = json.dumps(body, ensure_ascii=False).encode()
        self.send_response(code)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.end_headers()
        self.wfile.write(data)

    def do_GET(self):
        if self.path == "/health":
            return self._send(200, {"ok": True})
        if self.path == "/trucks":
            return self._send(200, TRUCKS)
        self._send(404, {"error": "no existe"})

    def do_POST(self):
        if self.path != "/trucks":
            return self._send(404, {"error": "no existe"})
        n = int(self.headers.get("Content-Length", 0))
        truck = json.loads(self.rfile.read(n) or b"{}")
        truck["id"] = len(TRUCKS) + 1
        TRUCKS.append(truck)
        self._send(201, truck)


def main(port=8000):
    print(f"truck-tracker-api en http://localhost:{port}")
    HTTPServer(("127.0.0.1", port), Handler).serve_forever()


if __name__ == "__main__":
    main()

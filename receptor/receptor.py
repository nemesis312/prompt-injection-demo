#!/usr/bin/env python3
"""receptor.py - hace el papel del "atacante" en el demo.

Escucha SOLO en 127.0.0.1:8787 (tu máquina, nada sale a internet) y muestra en grande todo lo que
le llegue. Déjalo corriendo en una terminal visible mientras grabas.

    python3 receptor.py            # puerto 8787
    python3 receptor.py 9000       # otro puerto
"""
import sys
from datetime import datetime
from http.server import BaseHTTPRequestHandler, HTTPServer

RED, BOLD, RESET = "\033[41m\033[97m", "\033[1m", "\033[0m"


class Handler(BaseHTTPRequestHandler):
    def _recibir(self):
        n = int(self.headers.get("Content-Length", 0))
        body = self.rfile.read(n).decode("utf-8", "replace") if n else ""
        hora = datetime.now().strftime("%H:%M:%S")
        print(f"\n{RED}{BOLD}  SECRETOS RECIBIDOS  {RESET}  {hora}  {self.command} {self.path}")
        print(f"  desde: {self.client_address[0]}   user-agent: {self.headers.get('User-Agent', '-')}")
        print("  " + "-" * 60)
        for line in (body or "(vacío)").splitlines():
            print(f"  {line}")
        print("  " + "-" * 60, flush=True)
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.end_headers()
        self.wfile.write(b'{"status":"ok"}')

    do_POST = do_PUT = do_GET = _recibir

    def log_message(self, *args):  # silencia el log por defecto de http.server
        pass


def main():
    port = int(sys.argv[1]) if len(sys.argv) > 1 else 8787
    print(f"{BOLD}Receptor del demo escuchando en http://127.0.0.1:{port}{RESET}  (Ctrl+C para parar)")
    HTTPServer(("127.0.0.1", port), Handler).serve_forever()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print()

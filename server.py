from http.server import BaseHTTPRequestHandler, HTTPServer
import sqlite3
import json
import os

class MyServer(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == "/airports":
            # Collegamento al database (ora cerca nella cartella principale)
            conn = sqlite3.connect('database/flights.db')
            cursor = conn.cursor()

            # Query per ottenere aeroporti unici
            query = """
            SELECT DISTINCT departure_airport FROM flights
            UNION
            SELECT DISTINCT arrival_airport FROM flights;
            """
            cursor.execute(query)
            airports = [row[0] for row in cursor.fetchall()]
            conn.close()

            # Rispondi con la lista di aeroporti in formato JSON
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps(airports).encode())

        else:
            # Gestione file statici (corretto il percorso per templates/)
            try:
                if self.path == "/":
                    self.path = "/index.html"
                file_path = os.path.join(os.path.dirname(__file__), "templates", self.path[1:])
                with open(file_path, "r", encoding="utf-8") as file:
                    file_to_open = file.read()
                self.send_response(200)
            except FileNotFoundError:
                file_to_open = "File non trovato"
                self.send_response(404)

            self.end_headers()
            self.wfile.write(file_to_open.encode("utf-8"))

if __name__ == "__main__":
    server = HTTPServer(("localhost", 8000), MyServer)
    print("Server in esecuzione su http://127.0.0.1:8000")
    server.serve_forever()

import sqlite3
import json
from http.server import BaseHTTPRequestHandler, HTTPServer

class MyServer(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == "/":
            self.path = "/templates/index.html"
        elif self.path.startswith("/static"):
            pass
        else:
            self.send_error(404, "File non trovato")
            return

        try:
            with open(self.path[1:], 'rb') as file:
                self.send_response(200)
                if self.path.endswith(".css"):
                    self.send_header("Content-Type", "text/css")
                elif self.path.endswith(".js"):
                    self.send_header("Content-Type", "application/javascript")
                else:
                    self.send_header("Content-Type", "text/html")
                self.end_headers()
                self.wfile.write(file.read())
        except Exception as e:
            self.send_error(500, f"Errore del server: {e}")

    def do_POST(self):
        if self.path == "/search":
            # Recupera i dati dalla richiesta
            content_length = int(self.headers['Content-Length'])
            post_data = json.loads(self.rfile.read(content_length))

            departure = post_data['departure']
            arrival = post_data['arrival']
            date = post_data['date']
            time = post_data['time']

            # Query al database
            conn = sqlite3.connect('database/flights.db')
            cursor = conn.cursor()
            query = """
                SELECT * FROM flights
                WHERE departure_airport = ?
                AND arrival_airport = ?
                AND flight_date = ?
                AND departure_time >= ?
            """
            cursor.execute(query, (departure, arrival, date, time))
            flights = cursor.fetchall()
            conn.close()

            # Risposta al client
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps(flights).encode())

# Avvio del server
if __name__ == "__main__":
    host = "127.0.0.1"
    port = 8000
    server = HTTPServer((host, port), MyServer)
    print(f"Server avviato su http://{host}:{port}")
    server.serve_forever()

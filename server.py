from http.server import BaseHTTPRequestHandler, HTTPServer
import os
# Handle connections for the Vaste server.

class RequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.protocol_version = "HTTP/1.1"
        self.send_response(200)
        file = ""
        if self.path.endswith("/"):
            self.path += "index.html"
        elif (not self.path.endswith("/index.html")):
            self.path += "/index.html"
        try:
            file = open("./html" + self.path, "rb")
        except FileNotFoundError:
            file = open("./html/404.html","rb")
        file.seek(0, 2)
        self.send_header("Content-Length", file.tell())
        self.end_headers()
        file.seek(0)
        self.wfile.write(file.read())
        print("./html" + self.path)
        file.close()
        return

def run():
    HOST, PORT = "localhost", 8080
    try:
        server = (HOST, PORT)
        httpd = HTTPServer(server, RequestHandler)
        print(f"Server started on port {PORT} at host {HOST}.")
        httpd.serve_forever()
    except KeyboardInterrupt:
        httpd.server_close()
        httpd.shutdown()
run()

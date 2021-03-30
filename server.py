from http.server import BaseHTTPRequestHandler, HTTPServer
from mimetypes import guess_type
import os
# Handle connections for the Vaste server.
# TODO
# https://letsencrypt.org/docs/certificates-for-localhost/


def isCookieValid(self):
    # is the users session ID in the valid & approved sessions
    pass

class RequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        isCookieValid(self)
        self.protocol_version = "HTTP/1.1"
        file = ""
        if self.path.endswith("/"):
            self.path += "index.html"
        elif ('.' not in self.path):
            self.path += ".html"
        try:
            file = open("./html" + self.path, "rb")
            self.send_response(200)
        except FileNotFoundError:
            file = open("./html/404.html","rb")
            self.send_response(404)
        mimetype, _ = guess_type(self.path)
        self.send_header("Content-type", mimetype)
        self.send_header("X-Content-Type-Options", "nosniff")
        file.seek(0, 2)
        self.send_header("Content-Length", file.tell())
        self.end_headers()
        file.seek(0)
        self.wfile.write(file.read())
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

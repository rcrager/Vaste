from http.server import BaseHTTPRequestHandler, HTTPServer
from mimetypes import guess_type
import os, sys
# Handle connections for the Vaste server.
# TODO
# https://letsencrypt.org/docs/certificates-for-localhost/

dynamicContent = [] # <-- Need to encrypt & decrypt later, but unencrypted for now

def fetchRecent(self):
    # Fetch recent updates to the website from other users
    self.send_header("Content-Length", sys.getsizeof(dynamicContent))
    # add each item to it's own div if don't want to keep all html data in list
    # ^^ might help prevent any js injection - that & casting the response
    # to a string upon recieving it in the JS
    response = ""
    for f in dynamicContent:
        response += (str(f)+"\n")
    self.wfile.write(response.encode('utf-8'))

def sendHeader(self, responseCode, contentLength):
    if(type(responseCode)==int):
        self.send_response(responseCode)
        mimetype, _ = guess_type(self.path)
        self.send_header("Content-type", mimetype)
        self.send_header("X-Content-Type-Options", "nosniff")
        self.send_header("Content-Length", contentLength)
        self.end_headers()

class RequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        # Update page contents, otherwise continue
        if(self.path.endswith("/updateMainPage")):
            # TODO:send headers here from sendHeader()
            #sendHeader(self, 200, sys.getsizeof(dynamicContent))
            self.send_response(200)
            self.end_headers()
            fetchRecent(self)
            return
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

    def do_POST(self):
        if(self.path.endswith("/updateMainPage")):
            # Recieve the data sent
            length = int(self.headers['Content-Length'])
            print(f"reading length: {length}")
            byteData = self.rfile.read(length)
            data = byteData.decode("utf-8")
            print(data)

            # Response to the data send & update dynamicContent
            # Add padding features for each button here ---
            padding = "<div id='button'><h4>"
            endPadding = "</h4></div>"
            response = str(padding+data+endPadding)
            dynamicContent.append(response)
            self.send_response(200)
            self.send_header('Content-type','text/html')
            self.end_headers()
            self.wfile.write(response.encode('utf-8'))
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

import http.server
import socketserver
from urllib.parse import urlparse, parse_qs
import json
import threading
import os 
from sys import stdout

def dump_to_console(*args):
    args = [str(a) for a in args]
    print("[HTTP]", " ".join(args))
    stdout.flush()

PORT = 8080
_dir_path = os.path.dirname(os.path.realpath(__file__))
STATIC_DIR = os.path.join(_dir_path, "public")

last_error = None
error_page = '''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta http-equiv="refresh" content="30">
    <title>Explora\'s display error message</title>
</head>
<body>
    <p>{}</p>
    <p>Retriying in 5 seconds..</p>
</body>
</html>'''


class Request_Handler(http.server.SimpleHTTPRequestHandler):

    def __init__(self, *args, **kwargs):
        kwargs['directory'] = STATIC_DIR
        super().__init__(*args, **kwargs)

    def do_GET(self):
        global last_error

        if last_error:
            self.error(last_error)
            return

        if self.path == "/status":
            self.respond(json.dumps({"status": "running"}), 200)
            return

        super().do_GET()
        

    def handle_http(self, msg, status_code):
        self.send_response(status_code)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        return msg

    def respond(self, msg, code = 418):
            response = self.handle_http(msg, code)
            self.wfile.write(response.encode('utf-8'))

    def error(self, err):
        self.send_response(500)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        response = error_page.format(err)
        self.wfile.write(response.encode('utf-8'))

class ReuseAddrTCPServer(socketserver.TCPServer):
    def __init__(self, *args, **kwargs):
        self.allow_reuse_address = True
        super().__init__(*args, **kwargs)

http_server = None
def serve_forever():
    global http_server
    http_server = ReuseAddrTCPServer(("", PORT), Request_Handler)
    http_server.serve_forever()

t = threading.Thread(target = serve_forever)

def start():
    t.start()

    dump_to_console("STATIC_DIR = ", STATIC_DIR )
    dump_to_console("Files to serve:")
    for f in os.listdir(STATIC_DIR):
        dump_to_console(f)


def close():
    global http_server
    if http_server:
        http_server.shutdown()
        http_server.server_close()
    if t.is_alive():
        t.join()

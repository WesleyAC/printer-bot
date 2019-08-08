#!/usr/bin/env python3

import json
from http.server import BaseHTTPRequestHandler, HTTPServer

class Server(BaseHTTPRequestHandler):
    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        data = json.loads(self.rfile.read(content_length))
        print(data["data"])
    
        response = json.dumps({"content": "Test response <3"}).encode()

        self.send_response(200)
        self.send_header('Content-Type', 'application/json')
        self.send_header('Content-Length', len(response))
        self.end_headers()
        self.wfile.write(response)
        self.wfile.flush()
        print("foo")

if __name__ == "__main__":
    s = HTTPServer(("", 8080), Server)
    s.serve_forever()


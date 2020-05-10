
from http.server import HTTPServer, BaseHTTPRequestHandler

class SimpleHTTPRequestHandler(BaseHTTPRequestHandler):

    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b'Accepted')

    def do_POST(self):
        """
        Currently this will only write out a single file
        It will be overwritten with a new upload
        """
        print("RECEIVING!!!")
        content_length = int(self.headers['Content-Length'])
        body = self.rfile.read(content_length)
        with open("test.zip", "w") as f:
            f.write(body)
        self.send_response(200)
        self.end_headers()



httpd = HTTPServer(('my.f.q.dn', 8888), SimpleHTTPRequestHandler)
httpd.serve_forever()
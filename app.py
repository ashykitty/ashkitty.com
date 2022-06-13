import generator as g 
import socketserver
import re

class Handler( socketserver.BaseRequestHandler):
    def setup( self):
        exp = r"^(?P<request>.*) /(?P<path>.*) (.|\n)*\n(?P<content>.*)"
        
        self.re_file = re.compile( exp)

    def send( self, content, code = True):
        if code:
            code = b"HTTP/1.1 200 OK\n"
        else:
            code = b"HTTP/1.1 404 Not Found\n"
        
        code += b"Strict-Transport-Security: max-age=63072000; preload\n"
        #code += b"Content-Security-Policy: default-src 'self'; img-src 'self' *.xkcd.com;script-src 'self'\n"
        #code += b"X-Content-Type-Options: nosniff\n"
        code += b"X-Frame-Options: DENY\n"
        code += b"X-XSS-Protection: 1\n"
        code += b"\n"
        self.request.sendall(code+content)
        
    def handle( self):

        data = self.request.recv(1024).decode('utf-8')
        data = self.re_file.search(data)
        
        req     = data.group("request")
        path    = data.group("path")
        content = data.group("content")

        self.send( g.handle( req, path, content))
        
if __name__ == "__main__":
    socketserver.TCPServer.allow_reuse_address = True
    with socketserver.TCPServer( ('0.0.0.0', 6969), Handler) as server:
        server.serve_forever()

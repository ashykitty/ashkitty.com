import generator as g 
import subprocess as sp
import socketserver
import re

class Handler( socketserver.BaseRequestHandler):
    def setup( self):
        exp = r"^(?P<request>.*) /(?P<path>.*) (.|\n)*\n(?P<content>.*)"
        
        self.re_file = re.compile( exp)

    def send( self, content, code = True):
        if code:
            code = b"HTTP/1.1 200 OK\n\n"
        else:
            code = b"HTTP/1.1 404 Not Found\n\n"
        
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

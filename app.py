import generator as g 
import socketserver
import re

class Handler( socketserver.BaseRequestHandler):

    HTTP_OK = "HTTP/1.1 200 OK\n"
    HTTP_NOT = "HTTP/1.1 404 Not Found\n"

    def setup( self):
        exp = r"^(?P<request>.*) /(?P<path>.*) (.|\n)*\n(?P<content>.*)"
        
        self.re_file = re.compile( exp)

    def send( self, content, code, data_format):
        
        code = str.encode( code)
        code += b"Strict-Transport-Security: max-age=63072000; preload\n"
        code += b"Content-Security-Policy: default-src 'self';"
        code += b"img-src 'self' *.xkcd.com;script-src 'self'\n"
        code += b"X-Content-Type-Options: nosniff\n"
        code += b"X-Frame-Options: DENY\n"
        code += b"Content-Type: "+str.encode(data_format)+b"\n"
        code += b"X-XSS-Protection: 1\n\n"
        
        self.request.sendall(code+content)
        
    def handle( self):

        data = self.request.recv(1024).decode('utf-8')
        data = self.re_file.search(data)
        
        req     = data.group("request")
        path    = data.group("path")
        content = data.group("content")

        page, code, file_type = g.handle( req, path, content)
        self.send( page, code, file_type)
        
if __name__ == "__main__":
    socketserver.TCPServer.allow_reuse_address = True
    with socketserver.TCPServer( ('0.0.0.0', 6969), Handler) as server:
        server.serve_forever()

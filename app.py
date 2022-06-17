import generator as g 
import socketserver
import re

class Handler( socketserver.BaseRequestHandler):

    HTTP_OK = "HTTP/1.1 200 OK\n"
    HTTP_NOT = "HTTP/1.1 404 Not Found\n"

    def setup( self):
        pass

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
        
    def get_cookies( self, data):
        for line in data.split("\n"):
            if line.startswith("Cookie:"):

                cookies = line.split(":")[1].split(";")
                cookies_dict = {}
                
                for cookie in cookies:
                    key,value = cookie.split("=")
                    cookies_dict[key.strip()] = value.strip()

                return cookies_dict
        return None

    def auth( self, cookies):
        if cookies and "login_key" in cookies:
            with open("private/key") as key:
                if cookies["login_key"] == key.read().strip():
                    return True
        return False

    def handle( self):

        data = self.request.recv(1024).decode('utf-8')
        
        cookies = self.get_cookies( data)
        
        auth = self.auth( cookies)

        content = data.find("\r\n"*2)

        if( content > 0):
            content = data[content+4:]
        else:
            content = ""

        data = data.split(" ")

        req  = data[0]
        path = data[1] 

        page, code, file_type = g.handle( req, path, content, auth)
        self.send( page, code, file_type)
        
if __name__ == "__main__":
    socketserver.TCPServer.allow_reuse_address = True
    with socketserver.TCPServer( ('0.0.0.0', 6969), Handler) as server:
        server.serve_forever()

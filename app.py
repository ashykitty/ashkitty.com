import generator as g 
import socketserver
import re

class Request:
    def __init__( self, req, path, cont, auth):
        self.request = req
        self.path    = path
        self.content = cont
        self.auth    = auth

class Handler( socketserver.BaseRequestHandler):
    
    VERSION = 4.0

    HTTP_OK = "HTTP/1.1 200 OK"
    HTTP_NOT = "HTTP/1.1 404 Not Found"

    FILE_TYPE = {
        "png":"image/png",
        "gif":"image/gif",
        "html":"text/html",
        "css":"text/css",
        "js":"application/javascript",
        "txt":"text",
        "py":"text",
        "bin":"application/octet-stream"
    }

    def setup( self):
        with open( "data/header.txt") as header:
            self.header = header.read()[:-1]

    def send( self, content, code, data_format):
      
        code = str.encode( self.header.format(
            CODE         = code,
            CONTENT_TYPE = data_format
        ))
        
        if type( content) == str:
            code += str.encode( content)
        else:
            code += content
       
        try:
            self.request.sendall( code)
        except:
            pass
        
    def get_cookies( self, data):
        for line in data.split("\n"):
            if line.startswith("cookie:"):

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

        page, code, file_type = g.handle( Request( req, path, content, auth))

        self.send( page, code, file_type)
        
if __name__ == "__main__":
    socketserver.TCPServer.allow_reuse_address = True
    with socketserver.TCPServer( ('0.0.0.0', 6969), Handler) as server:
        server.serve_forever()

import subprocess as sp
from app import *

def serve( request):
    if len( request.content) < 4096:
        path = "../catcoder/meow"
        p = sp.Popen([path], stdout=sp.PIPE, stdin=sp.PIPE, shell=False)
        ret = p.communicate( input = str.encode( request.content))[0].decode()
    else:
        ret = "message too long >:c"

    return ( ret, Handler.HTTP_OK, Handler.FILE_TYPE["txt"])
 

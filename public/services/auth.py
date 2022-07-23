from app import *
from generator import notfound

def serve( request):
    if request.request == "GET":
        return notfound()

    with open("private/key") as key:
        if request.content == key.read().strip():
            cookie = f"login_key={request.content}; expires=Sat, 22 Sep 2029 13:37:00 UTC; path=/"
            return ( str.encode(cookie), Handler.HTTP_OK, Handler.FILE_TYPE["txt"])
    return ( str.encode("wrong lol"), Handler.HTTP_OK, Handler.FILE_TYPE["txt"])

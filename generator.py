from importlib import import_module
from app import Request, Handler
from datetime import datetime
from datetime import date
import subprocess as sp
import random
import time
import os

global DAYS 
global EMOJIS 

def load_assets():
    global DAYS 
    global EMOJIS 

    with open("data/days.txt") as file:
        DAYS = file.read().split("\n")

    with open("data/emojis.txt", encoding="utf-8") as file:
        EMOJIS = file.read().split("\n")
      
def notfound():
    with open( "templates/notfound.html") as page:
        page = page.read()

    page = generate( page)
    return ( page, Handler.HTTP_NOT, Handler.FILE_TYPE["html"])

def handle_service( path, request):
    service_path = f"{path}services{request.path}"

    if os.path.exists( f"{service_path}.py"):
        module_path = service_path.replace("/",".")
        module = import_module( module_path)
        return module.serve( request)

    return None

def handle_file( path, request):
    filepath = f"{path}files{request.path}"

    if not os.path.exists( filepath):
        return None

    if not os.path.isfile( filepath):
        return None
    
    with open( filepath, "rb") as file:
        ftype = filepath.split(".")[-1]
        ftype = Handler.FILE_TYPE[ftype if ftype in Handler.FILE_TYPE else "bin"]

        content = file.read()

        if "text" in ftype:
            content = content.decode()

        return ( content, Handler.HTTP_OK, ftype)
    
    return None


def handle_path( path, request):

    service = handle_service( path, request)

    if service:
        return service

    file = handle_file( path, request)
    if file:
        return file

    splitpath = request.path.split("/")

    while len(splitpath) >= 1:
        newpath = "/".join(splitpath)

        pagepath = f"{path}pages{newpath}.html"

        splitpath.pop()

        if not os.path.exists( pagepath):
            continue
        
        with open( pagepath) as page:
            page = page.read()

        genpath = f"{path}generators{newpath}"

        if os.path.exists( f"{genpath}.py"):
            module_path = genpath.replace("/",".")
            module = import_module( module_path)

            page = module.generate( page, request)
                
            if not page:
                return None
        else:
            if request.path.count("/") > 1:
                return notfound()
    
        page = generate( page) 
        return ( page, Handler.HTTP_OK, Handler.FILE_TYPE["html"])

    return None
 
def handle( request):
   
    if request.path == "/":
        request.path = "/root"
    elif request.path.startswith( "/root"):
        return notfound()

    public = handle_path( "public/", request)

    if public:
        return public

    if request.auth:
        private = handle_path( "private/", request)
        if private:
            return private 

    return notfound()

def add_emojis( html):
    while "(EMOJI)" in html:
        html = html.replace( "(EMOJI)", random.choice( EMOJIS), 1)
    return html

def is_night():
    return time.localtime().tm_hour < 6 

def get_special_message():
    days_since = (date.today()-date(2021,9,8)).days

    if date.today().day == 8:
        months = int( days_since / 30)
        return f"HAPPY {months} MONTHS ANNIVERSARY!! {random.choice(EMOJIS)}"
    else:
        return f"{days_since} {random.choice(DAYS)} days with u <3"

def generate( body):

    night = is_night() 

    with open( "templates/base.html") as page:
        page = page.read()

    page = page.format(
        TITLE      = "ash's page",
        VERSION    = Handler.VERSION,
        DAYS       = get_special_message(),
        BODY       = body,
        STYLE      = "style.css"    if night else "style.css",
        BANNER     = "us2.svg" if night else "us2.svg"
    )

    return add_emojis( page)

load_assets()

from datetime import date
from app import *
import subprocess as sp
from datetime import datetime
import time
import random
import os

APP_VERSION = 3.8

global DAYS 
global EMOJIS 

FILE_TYPE = {
    "png":"image/png",
    "gif":"image/gif",
    "html":"text/html",
    "css":"text/css",
    "js":"application/javascript",
    "txt":"text",
    "py":"text"
    }

def load_assets():
    global DAYS 
    global EMOJIS 

    with open("data/days.txt") as file:
        DAYS = file.read().split("\n")

    with open("data/emojis.txt", encoding="utf-8") as file:
        EMOJIS = file.read().split("\n")

def meow( content):
    if len(content) < 4096:
        path = "../catcoder/meow"
        p = sp.Popen([path], stdout=sp.PIPE, stdin=sp.PIPE, shell=False)
        return p.communicate( input = str.encode(content))[0]
    else:
        return "message too long >:c"
       
def notfound():
    page = generate( read_page( "templates/notfound"))
    return ( page, Handler.HTTP_NOT, FILE_TYPE["html"])

def handle( request, path, content, auth):
    
    files = os.listdir("files")
    static = os.listdir("static")

    lfiles = os.listdir("private/files")
    lstatic = os.listdir("private/static")

    if path == "/":
        btn = "<a href=\"/login\"><button>login</button></a>"
        page = read_page( "templates/root").format(
                LOGIN= "" if auth else btn
                )
        page = generate( page)
        return (page, Handler.HTTP_OK, FILE_TYPE["html"])
    
    elif path[1:] in files:
        with open(f"files{path}","rb") as file:
            ftype = path.split(".")[1]
            if ftype in FILE_TYPE:
                ftype = FILE_TYPE[ftype]
            else:
                ftype = "application/octet-stream"
            return (file.read(), Handler.HTTP_OK, ftype)

    elif path[1:] in lfiles:
        if auth:
            with open(f"private/files{path}","rb") as file:            
                ftype = path.split(".")[1]
                return (file.read(), Handler.HTTP_OK, FILE_TYPE[ftype])
        else:
            return notfound()

    elif f"{path[1:]}.html" in static:
        page = generate( read_page( f"static/{path[1:]}"))
        return ( page, Handler.HTTP_OK, FILE_TYPE["html"])

    elif f"{path[1:]}.html" in lstatic:
        if auth:
            page = generate( read_page( f"private/static/{path[1:]}"))
            return ( page, Handler.HTTP_OK, FILE_TYPE["html"])
        else:
            return notfound()

    elif path == "/files":
        page = read_page( "templates/files")
        page = page.format(
                FILES = "\n".join([f"<a href=\"/{a}\">{a}</a><br>" for a in files])
                )
        return ( generate( page), Handler.HTTP_OK, FILE_TYPE["html"])

    elif path == "/emojis":
        page = read_page( "templates/emojis")
        emojis = zip( EMOJIS[::3], EMOJIS[1::3], EMOJIS[2::3])
        page = page.format(
                EMOJI_LIST = "\n".join(f"<pre>{a}   {b}   {c}</pre>" for a,b,c in emojis)
                )
        return ( generate( page), Handler.HTTP_OK, FILE_TYPE["html"])

    elif path == "/auth":
        with open("private/key") as key:
            if content == key.read().strip():
                cookie = f"login_key={content}; expires=Sat, 22 Sep 2029 13:37:00 UTC; path=/"
                return ( str.encode(cookie), Handler.HTTP_OK, FILE_TYPE["txt"])
        return ( str.encode("wrong lol"), Handler.HTTP_OK, FILE_TYPE["txt"])

    elif path == "/meow":
        return (meow( content), Handler.HTTP_OK, FILE_TYPE["txt"])

    elif path.startswith("/xkcd"):
        path = path[1:].split("/")
        
        if len(path) != 2:
            return notfound()
        else:
            if path[1].isnumeric():
                page = generate( xkcd( path[1]))
                return ( page, Handler.HTTP_OK, FILE_TYPE["html"])
            else:
                return notfound()
    else:
        return notfound()

def xkcd(page_num):
    page_num = int(page_num)
    per_page = 8
    
    with open("data/xkcd2.txt") as file:
        links = file.read().split("\n")
        
    total_pages = len(links) // per_page

    if page_num < 0 or page_num > total_pages:
        return notfound() 
       
    links = list(reversed(links))
    links = links[page_num*per_page:page_num*per_page+per_page]

    post = read_page( "templates/xkcd_post", False)
    posts = ""

    for link in links:
        title = link.split("/")[-1].split(".")[0]
        title = title.replace("_"," ")
        posts += post.format(TITLE=title,LINK=link)
    
    posts = add_emojis( posts)

    btn = "<a href=\"/xkcd/{}\"><button>{}</button></a>"

    xkcd_page = read_page( "templates/xkcd").format(
            BODY =posts,
            PAGES=f"{page_num}/{total_pages}",
            FIRST=btn.format(0,"&lt&lt") if page_num > 0 else "",
            LAST =btn.format(total_pages if page_num < total_pages else "","&gt&gt"),
            PREV =btn.format(page_num-1,"&lt") if page_num > 0 else "",
            NEXT =btn.format(page_num+1,"&gt") if page_num < total_pages else "",
            PAGE=f"{page_num}"
        )

    return xkcd_page

def add_emojis( html):
    while "(EMOJI)" in html:
        html = html.replace( "(EMOJI)", random.choice( EMOJIS), 1)
    return html

def read_page( page_name, emojis = True):
    try:
        with open( f"{page_name}.html", encoding="utf-8") as page:
            if emojis:
                return add_emojis( page.read())
            else:
                return page.read()
    except:
        return None
    
def is_night():
    return time.localtime().tm_hour < 6 

def get_special_message():
    days_since = (date.today()-date(2021,9,8)).days

    if date.today().day == 8:
        months = int( days_since / 30)
        return f"HAPPY {months} MONTHS ANNIVERSARY!! {random.choice(EMOJIS)}"
    else:
        return f"{days_since} {random.choice(DAYS)} days with u <3"

def generate( page):

    night = is_night() 

    page = read_page( "templates/base").format(
        TITLE      = "ash's page",
        VERSION    = APP_VERSION,
        DAYS       = get_special_message(),
        BODY       = page,
        STYLE      = "night.css" if night else "style.css",
        BANNER     = "us_night.png" if night else "us2.png"
    )

    return str.encode( page)

load_assets()

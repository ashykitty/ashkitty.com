from datetime import date
import subprocess as sp
from datetime import datetime
import time
import random
import os

APP_VERSION = 3.2

global DAYS 
global EMOJIS 

def load_assets():
    global DAYS 
    global EMOJIS 

    with open("data/days.txt") as file:
        DAYS = file.read().split("\n")

    with open("data/emojis.txt", encoding="utf8") as file:
        EMOJIS = file.read().split("\n")

def meow( content):
    content = content.split(":")
    if len(content[1]) < 2048:
        c = "-e" if content[0] == "true" else "-d"
        return sp.run(["../catcoder/meow",c,content[1].strip()],capture_output=True).stdout
    else:
        return "message too long >:c"
       
def notfound():
    return generate( read_page( "templates/notfound"))

def handle( request, path, content):
    
    files = os.listdir("files")

    if path == "":
        page = generate( read_page( "templates/root"))
        return page
    
    elif path in files:
        with open(f"files/{path}","rb") as file:
            return file.read()

    elif path == "meow":
        return meow( content) 

    elif path.startswith("xkcd"):
        path = path.split("/")
        
        if len(path) != 2:
            return notfound()
        else:
            if path[1].isnumeric():
                page = generate( xkcd( path[1]))
                return page
            else:
                return self.notfound()
    else:
        return self.notfound()

def xkcd(page_num):
    page_num = int(page_num)
    per_page = 8
    
    with open("data/xkcd2.txt") as file:
        links = file.read().split("\n")
        
    total_pages = len(links) // per_page

    if page_num < 0 or page_num > total_pages:
        return read_page( "templates/notfound")
       
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
        BANNER     = "night.gif" if night else "us2.png"
    )

    return str.encode( page)

load_assets()

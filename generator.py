from datetime import date
from datetime import datetime
import time
import random

APP_VERSION = 2.4
TEMPLATES = "templates/"

global days
global emojis

def load_assets():
    global days
    global emojis

    with open("assets/days.txt") as file:
        days = file.readlines()

    with open("assets/emojis.txt",encoding="utf8") as file:
        emojis = file.readlines()

def add_emojis( html):
    while "{EMOJIS}" in html:
        html = html.replace( "{EMOJIS}", random.choice( emojis), 1)
    return html

def read_page( page_name):
    try:
        with open( f"{TEMPLATES}{page_name}.html") as page:
            return add_emojis( page.read())
    except:
        return None
    
def is_night():
    return time.localtime().tm_hour < 6 

def generate( page):
    days_msg = str((date.today()-date(2021,9,8)).days)
    days_msg = " ".join([days_msg,random.choice(days),"days with u <3"])

    base = read_page( "base")
    page = read_page( page)

    if not page:
        page = read_page( "notfound")
        code = 404
    else:
        code = 200

    night = time.localtime().tm_hour < 6

    base = base.format(
        TITLE      = "ash's page",
        VERSION    = APP_VERSION,
        DAYS       = days_msg,
        BODY       = page,
        STYLESHEET = "night"     if night else "style",
        BANNER     = "night.gif" if night else "us.png"
    )

    return ( base, code)

load_assets()

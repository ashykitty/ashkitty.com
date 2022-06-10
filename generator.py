from datetime import date
from datetime import datetime
import time
import random

APP_VERSION = 2.5
TEMPLATES = "templates/"

global DAYS 
global EMOJIS 

def load_assets():
    global DAYS 
    global EMOJIS 

    with open("assets/days.txt") as file:
        DAYS = file.read().split("\n")

    with open("assets/emojis.txt", encoding="utf8") as file:
        EMOJIS = file.read().split("\n")

def add_emojis( html):
    while "(EMOJI)" in html:
        html = html.replace( "(EMOJI)", random.choice( EMOJIS), 1)
    return html

def read_page( page_name, emojis = True):
    try:
        with open( f"{TEMPLATES}{page_name}.html", encoding="utf-8") as page:
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

    return read_page( "base").format(
        TITLE      = "ash's page",
        VERSION    = APP_VERSION,
        DAYS       = get_special_message(),
        BODY       = page,
        STYLESHEET = "night"     if night else "style",
        BANNER     = "night.gif" if night else "us2.svg"
    )

load_assets()

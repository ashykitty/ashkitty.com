from datetime import date
from datetime import datetime
import random

APP_VERSION = 2.2
TEMPLATES = "templates/"

global days
global emojis

def load_assets():
    global days
    global emojis
    with open("assets/days.txt") as file:
        days = file.read().split("\n")
    with open("assets/emojis.txt",encoding="utf8") as file:
        emojis = file.read().split("\n")

def main():
    with open(TEMPLATES+"main.html") as main:
        html = main.read()
        while "{EMOJIS}" in html:
            html = html.replace("{EMOJIS}", random.choice( emojis),1)
        return html
        
def base(BODY,night):
    days_msg = str((date.today()-date(2021,9,8)).days)
    days_msg = " ".join([days_msg,random.choice(days),"days with u <3"])
    with open(TEMPLATES+"base.html") as base:
        html = base.read()
        html = html.format(
            TITLE="ash's page",
            VERSION=APP_VERSION,
            DAYS=days_msg,
            BODY=BODY,
            STYLESHEET="night" if night else "style",
            BANNER="night.gif" if night else "us.png"
        )
        
        return html

load_assets()

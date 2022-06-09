from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from fastapi.responses import PlainTextResponse
from plyer import notification
from pydantic import BaseModel
from fastapi import FastAPI
import generator as g 
import subprocess as sp
    
app = FastAPI(redoc_url=None,docs_url=None)
app.mount("/static", StaticFiles(directory="static"), name="static")
app.mount("/adarkroom", StaticFiles(directory="../adarkroom"), name="adarkroom")

class Model(BaseModel):
    encode: bool
    msg: str

@app.post("/meow/")
def meow(model: Model):
    if len(model.msg) < 2048:
        ac = "-e" if model.encode else "-d"
        return sp.run(["../catcoder/meow",ac,model.msg.strip()],capture_output=True).stdout
    else:
        return "message too long >:c"

@app.get("/robots.txt")
def robots():
    return PlainTextResponse(content="User-agent: *\nDisallow: /", status_code=200) 

@app.get("/", response_class=HTMLResponse)
async def root():
    return g.generate( g.read_page( "root"))

@app.get("/xkcd/{page_num}", response_class=HTMLResponse)
async def xkcd(page_num):
    page_num = int(page_num)
    per_page = 8
    
    with open("assets/xkcd.txt") as file:
        links = file.read().split("\n")
        
    total_pages = len(links) // per_page

    if page_num < 0 or page_num > total_pages:
        return g.generate( g.read_page( "notfound"))
       
    links = list(reversed(links))
    links = links[page_num*per_page:page_num*per_page+per_page]

    post = g.read_page( "xkcd_post", False)
    posts = ""

    for link in links:
        title = link.split("/")[-1].split(".")[0]
        title = title.replace("_"," ")
        posts += post.format(TITLE=title,LINK=link)
    
    posts = g.add_emojis( posts)

    xkcd_page = g.read_page( "xkcd").format(
            BODY=posts,
            PAGES=f"{page_num}/{total_pages}",
            PREV=f"{page_num-1}" if page_num > 0 else f"{page_num}",
            NEXT=f"{page_num+1}" if page_num < total_pages else f"{page_num}",
            PAGE=f"{page_num}"
        )

    return g.generate( xkcd_page)

@app.get("/{page}", response_class=HTMLResponse)
async def getpage(page):
    page = g.generate( g.read_page( "notfound"))
    return HTMLResponse( content = page, status_code = 404)

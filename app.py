from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from fastapi.responses import PlainTextResponse
from plyer import notification
from pydantic import BaseModel
from fastapi import FastAPI
import generator 
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
    return generator.generate( "root")[0]

@app.get("/{page}", response_class=HTMLResponse)
async def getpage(page):
    page, code = generator.generate( page)
    return HTMLResponse( content = page, status_code = code)

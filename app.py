from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from plyer import notification
from pydantic import BaseModel
from fastapi import FastAPI
import templates
import subprocess as sp
import time
    
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

@app.get("/iloveu")
def iloveu():
    pass

@app.get("/fix")
def fix():
    pyautogui.press('space')
    pyautogui.press('f')
    time.sleep(2)
    pyautogui.press('f')
    pyautogui.press('space')

@app.get("/", response_class=HTMLResponse)
async def root():
    hour = time.localtime().tm_hour
    return templates.base(templates.main(),hour < 6)
    
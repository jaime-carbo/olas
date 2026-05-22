import asyncio
from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from sse_starlette.sse import EventSourceResponse
from print_function import print_function
from base_template import get_template
from lang_selector import get_lang_selector
from bio import get_bio
from header import get_header
import numpy as np

app = FastAPI()

@app.get("/")
async def homepage(lang: str = "en"):
    return HTMLResponse(get_template().substitute(header=get_header().substitute(), lang_selector=get_lang_selector(lang), bio=get_bio(lang)))

async def generate_events(width=350, height=50):
    i = 0
    longitud = int(width / 7.2)
    height = int(height / 80)
    x = np.linspace(0, 10, longitud)
    while True:
        true_x = x + i * 0.1
        banner = print_function(x, np.cos(true_x) + np.sin(3*true_x) + 1/2, height=height, extra="JAIME CARBÓ SÁNCHEZ")
        last_row = "".join(longitud//2*[" -"])
        banner += "\n" + last_row
        
        yield {"data": banner}
        await asyncio.sleep(0.08)
        i+=1

@app.get("/events")
async def sse_endpoint(width: int = 350, height: int = 50):
    return EventSourceResponse(generate_events(width, height))
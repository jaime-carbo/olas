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
    return HTMLResponse(get_template().substitute(header=get_header(), lang_selector=get_lang_selector(lang), bio=get_bio(lang)))

@app.get("/headerCurve")
async def header_curve_endpoint(width: int = 350, height: int = 50, extra: str = ""):  
    curve_width = int(width / 7.2)
    curve_height = int(height / 80)
    math_function = lambda x: np.cos(x) + np.sin(3*x) + 1/2
    header_curve: str = generate_curve_animation(math_function, curve_width, curve_height, bottom_line=" -", extra=extra)
    return EventSourceResponse(header_curve)

@app.get("/basicCurve")
async def basic_curve_endpoint(width: int = 350, height: int = 50, extra: str = ""):
    math_function = lambda x: np.cos(x)
    curve_width = int(width / 7.2)
    return EventSourceResponse(generate_curve_animation(math_function, curve_width, height, direction=-1, extra=extra))

async def generate_curve_animation(math_function, width, height, direction=1, top_line="", bottom_line="", extra=""):
    i = 0
    x = np.linspace(0, 10, width)
    while True:
        true_x = x + i * (0.1 * direction)
        banner = print_function(x, math_function(true_x), height=height, extra=extra)
        if top_line:
            banner = top_line*(width//len(top_line)) + "\n" + banner
        if bottom_line:
            banner = banner + "\n" + bottom_line*(width//len(bottom_line))
        yield {"data": banner}
        await asyncio.sleep(0.08)
        i+=1
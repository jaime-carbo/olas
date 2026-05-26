import asyncio
from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from sse_starlette.sse import EventSourceResponse
from print_function import print_function
from base_template import get_template
from lang_selector import get_lang_selector
from bio import get_bio
from header import get_header
from k8s_info import get_cluster_metrics
from cluster_section import get_cluster_section
import numpy as np

app = FastAPI()

@app.get("/")
async def homepage(lang: str = "en"):
    cluster_html = get_cluster_section()
    return HTMLResponse(get_template().substitute(header=get_header(), lang_selector=get_lang_selector(lang), bio=get_bio(lang), cluster=cluster_html))

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

@app.get("/clusterMetrics")
async def cluster_metrics_endpoint():
    return EventSourceResponse(generate_cluster_metrics())

async def generate_cluster_metrics():
    while True:
        data = await get_cluster_metrics()
        if data is None:
            yield {"data": "K8S │ offline"}
        else:
            def bar(pct, length=10):
                filled = int(pct * length)
                return "▓" * filled + "░" * (length - filled)

            cpu_pct = data["cpu_used"] / data["cpu_allocatable"] if data["cpu_allocatable"] > 0 else 0
            mem_pct = data["mem_used"] / data["mem_allocatable"] if data["mem_allocatable"] > 0 else 0

            cpu_bar = bar(cpu_pct)
            mem_bar = bar(mem_pct)

            cpu_used_m = data["cpu_used"] * 1000
            cpu_total_m = data["cpu_allocatable"] * 1000
            mem_used_mb = data["mem_used"] / (1024 * 1024)
            mem_total_mb = data["mem_allocatable"] / (1024 * 1024)

            line = f"K8S │ CPU {cpu_bar} {cpu_used_m:.0f}m/{cpu_total_m:.0f}m │ MEM {mem_bar} {mem_used_mb:.0f}Mi/{mem_total_mb:.0f}Mi"
            yield {"data": line}
        await asyncio.sleep(5)

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
import asyncio
from contextlib import asynccontextmanager
from datetime import datetime, timezone
from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from sse_starlette.sse import EventSourceResponse
from print_function import print_function
from ascii_chart import create_horizontal_bar_chart
from base_template import get_template
from lang_selector import get_lang_selector
from bio import get_bio
from header import get_header
from k8s_info import get_cluster_metrics
from cluster_section import get_cluster_section
from mongodb_section import get_mongodb_section
from body_texts import get_text_by_name
import numpy as np
import db

@asynccontextmanager
async def lifespan(app: FastAPI):
    await db.connect()
    yield
    await db.disconnect()

app = FastAPI(lifespan=lifespan)

@app.get("/")
async def homepage(lang: str = "en"):
    cluster_html = get_cluster_section(lang)
    mongodb_html = get_mongodb_section(lang)
    return HTMLResponse(get_template().substitute(header=get_header(), lang_selector=get_lang_selector(lang), bio=get_bio(lang), cluster=cluster_html, mongodb=mongodb_html))

@app.get("/headerCurve")
async def header_curve_endpoint(width: int = 350, height: int = 50, extra: str = "", charWidth: float = 7.2, charHeight: float = 80):  
    curve_width = max(1, int(width / charWidth))
    curve_height = max(1, int(height / charHeight))
    math_function = lambda x: np.cos(x) + np.sin(3*x) + 1/2
    header_curve: str = generate_curve_animation(math_function, curve_width, curve_height, bottom_line=" -", extra=extra)
    return EventSourceResponse(header_curve)

@app.get("/basicCurve")
async def basic_curve_endpoint(width: int = 350, height: int = 50, extra: str = "", charWidth: float = 7.2, charHeight: float = 80):
    math_function = lambda x: np.cos(x)
    curve_width = max(1, int(width / charWidth))
    curve_height = max(1, int(height / charHeight))
    return EventSourceResponse(generate_curve_animation(math_function, curve_width, curve_height, direction=-1, extra=extra))

@app.get("/clusterMetrics")
async def cluster_metrics_endpoint(width: int = 200, charWidth: float = 7.2):
    chart_width = max(1, int(width / charWidth))
    return EventSourceResponse(generate_cluster_metrics(chart_width))

@app.get("/mongoLangChart")
async def mongo_lang_chart_endpoint(width: int = 200, height: int = 50, charWidth: float = 7.2, charHeight: float = 80):
    chart_width = max(1, int(width / charWidth))
    return EventSourceResponse(generate_mongo_lang_chart(chart_width))

@app.get("/mongoSectionsChart")
async def mongo_sections_chart_endpoint(width: int = 200, height: int = 50, charWidth: float = 7.2, charHeight: float = 80, lang: str = "en"):
    chart_width = max(1, int(width / charWidth))
    return EventSourceResponse(generate_mongo_sections_chart(chart_width, lang))

@app.get("/db-test")
async def db_test():
    database = db.get_db()
    if database is None:
        return {"status": "mock", "message": "No MONGODB_URI configured"}
    try:
        test_collection = database["test"]
        await test_collection.insert_one({"hello": "world"})
        doc = await test_collection.find_one({"hello": "world"})
        await test_collection.delete_many({"hello": "world"})
        if doc and doc.get("hello") == "world":
            return {"status": "ok", "ping": "pong", "db": db.MONGODB_DB}
        return {"status": "error", "message": "Document not found after insert"}
    except Exception as e:
        return {"status": "error", "message": str(e)}

@app.post("/metrics")
async def track_metrics(payload: dict):
    database = db.get_db()
    if database is None:
        return {"status": "mock"}
    try:
        metric_type = payload.get("type")
        section = payload.get("section")
        session_id = payload.get("session_id")
        now = datetime.now(timezone.utc)
        if metric_type == "click":
            await database["clicks"].insert_one({
                "section": section,
                "session_id": session_id,
                "timestamp": now,
            })
        elif metric_type == "dwell":
            await database["dwell"].insert_one({
                "section": section,
                "duration_ms": payload.get("duration_ms", 0),
                "session_id": session_id,
                "timestamp": now,
            })
        return {"status": "ok"}
    except Exception as e:
        print(f"METRICS ERROR: {e}")
        return {"status": "error"}

async def generate_cluster_metrics(width):
    while True:
        data = await get_cluster_metrics()
        if data is None:
            yield {"data": "K8S │ offline"}
        else:
            cpu_pct = data["cpu_used"] / data["cpu_allocatable"] if data["cpu_allocatable"] > 0 else 0
            mem_pct = data["mem_used"] / data["mem_allocatable"] if data["mem_allocatable"] > 0 else 0

            cpu_used_m = data["cpu_used"] * 1000
            cpu_total_m = data["cpu_allocatable"] * 1000
            mem_used_mb = data["mem_used"] / (1024 * 1024)
            mem_total_mb = data["mem_allocatable"] / (1024 * 1024)

            pod_title = f"K8S │ {data['pod_name']} ({data['pod_age']})" if data["pod_age"] else f"K8S │ {data['pod_name']}"

            labels = ["CPU", "MEM"]
            values = [cpu_pct * 100, mem_pct * 100]
            display = [f"{cpu_used_m:.0f}m/{cpu_total_m:.0f}m", f"{mem_used_mb:.0f}Mi/{mem_total_mb:.0f}Mi"]
            chart = create_horizontal_bar_chart(labels, values, width=width, title=pod_title, display=display, maxes=[100, 100])
            yield {"data": chart}
        await asyncio.sleep(5)

async def generate_mongo_lang_chart(width):
    while True:
        database = db.get_db()
        if database is None:
            yield {"data": "LANG │ mock mode"}
        else:
            try:
                pipeline = [
                    {"$match": {"section": {"$regex": "^lang_"}}},
                    {"$group": {"_id": "$section", "count": {"$sum": 1}}},
                    {"$sort": {"count": -1}}
                ]
                results = await database["clicks"].aggregate(pipeline).to_list(length=None)
                if not results:
                    yield {"data": "LANG │ waiting for data..."}
                else:
                    labels = [r["_id"].replace("lang_", "").upper() for r in results]
                    values = [float(r["count"]) for r in results]
                    chart = create_horizontal_bar_chart(labels, values, width=width, title="LANG", unit=" clicks")
                    yield {"data": chart}
            except Exception as e:
                print(f"LANG CHART ERROR: {e}")
                yield {"data": "LANG │ error"}
        await asyncio.sleep(30)

async def generate_mongo_sections_chart(width, lang="en"):
    subtitle = get_text_by_name("sections_subtitle", lang)
    while True:
        database = db.get_db()
        if database is None:
            yield {"data": "SECT │ mock mode"}
        else:
            try:
                pipeline = [
                    {"$group": {"_id": "$section", "avg_ms": {"$avg": "$duration_ms"}}},
                    {"$sort": {"avg_ms": -1}}
                ]
                results = await database["dwell"].aggregate(pipeline).to_list(length=None)
                if not results:
                    yield {"data": "SECT │ waiting for data..."}
                else:
                    labels = [r["_id"] for r in results]
                    values = [float(r["avg_ms"]) / 1000 for r in results]
                    chart = create_horizontal_bar_chart(labels, values, width=width, title="SECTIONS", unit="s", subtitle=subtitle)
                    yield {"data": chart}
            except Exception as e:
                print(f"SECTIONS CHART ERROR: {e}")
                yield {"data": "SECT │ error"}
        await asyncio.sleep(30)

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
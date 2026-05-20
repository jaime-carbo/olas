import asyncio
from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from sse_starlette.sse import EventSourceResponse
from print_function import print_function
import numpy as np

app = FastAPI()

HTML = """
<!DOCTYPE html>
<html>
<body>
  <pre id="text">----------</pre>
  <script>
    let es;
    function connect() {
      es = new EventSource(`/events?width=${window.innerWidth}&height=${window.innerHeight}`);
      es.onmessage = (e) => {
        document.getElementById("text").textContent = e.data;
      };
      es.onerror = () => {
        document.getElementById("text").textContent = "Stream ended";
        es.close();
      };
    }
    connect();
    window.addEventListener("resize", () => { es.close(); connect(); });
  </script>
</body>
</html>
"""

@app.get("/")
async def homepage():
    return HTMLResponse(HTML)

async def generate_events(width=350, height=50):
    i = 0
    longitud = int(width / 7.2)
    height = int(height / 80)
    x = np.linspace(0, 10, longitud)
    while True:
        true_x = x + i * 0.1
        banner = print_function(x, np.cos(true_x) + np.sin(3*true_x) + 1/2, height=height, extra="JAIME CARBÓ SÁNCHEZ")
        last_row = "".join(longitud*["_"])
        banner += "\n" + last_row
        
        yield {"data": banner}
        await asyncio.sleep(0.08)
        i+=1

def generate_worm(i, longitud, extra):
    return "".join([e if pos != i%longitud else f"| {extra} |" for pos, e in enumerate(longitud*["-"])])

@app.get("/events")
async def sse_endpoint(width: int = 350, height: int = 50):
    return EventSourceResponse(generate_events(width, height))
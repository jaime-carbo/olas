from string import Template

def get_header():
    return """<body>
<div data-track="header">
<pre id="text">----------</pre>
<script>
    let es;
    let pageWidth = window.innerWidth;
    let pageHeight = window.innerHeight;
    function measureChar() {
        const ctx = document.createElement('canvas').getContext('2d');
        ctx.font = getComputedStyle(document.getElementById('text')).font;
        const metrics = ctx.measureText('M');
        const charWidth = metrics.width;
        const charHeight = (metrics.fontBoundingBoxAscent + metrics.fontBoundingBoxDescent) * 5;
        return { charWidth, charHeight };
    }
    function connect() {
    pageWidth = window.innerWidth;
    pageHeight = window.innerHeight;
    const { charWidth, charHeight } = measureChar();
    es = new EventSource(`/headerCurve?width=${pageWidth}&height=${pageHeight}&charWidth=${charWidth}&charHeight=${charHeight}&extra=JAIME CARBÓ SÁNCHEZ`);
    es.addEventListener('message', (e) => {
        document.getElementById("text").textContent = e.data;
    });
    es.addEventListener('error', () => {
        document.getElementById("text").textContent = "Stream ended";
        es.close();
    });
    }
    connect();
    window.addEventListener("resize", () => { es.close(); connect(); });
</script>
</div>
"""
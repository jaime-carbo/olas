from string import Template

def get_header():
    return """<body>
<pre id="text">----------</pre>
<script>
    let es;
    let pageWidth = window.innerWidth;
    let pageHeight = window.innerHeight;
    function connect() {
    pageWidth = window.innerWidth;
    pageHeight = window.innerHeight;
    es = new EventSource(`/headerCurve?width=${pageWidth}&height=${pageHeight}&extra=JAIME CARBÓ SÁNCHEZ`);
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
"""
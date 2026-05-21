from string import Template

def get_header():
    return Template(
"""<body>
<pre id="text">----------</pre>
<script>
    let es;
    let pageWidth = window.innerWidth;
    let pageHeight = window.innerHeight;
    function connect() {
    pageWidth = window.innerWidth;
    pageHeight = window.innerHeight;
    es = new EventSource(`/events?width=$${pageWidth}&height=$${pageHeight}`);
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
""")
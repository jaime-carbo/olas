from string import Template
from body_texts import get_text_by_name

def get_mongodb_section(language: str = "en"):
    text = get_text_by_name("mongodb_par", language)
    return Template("""
<div data-track="mongodb">
<div style="padding: 0px 10vw; margin-top: 20px; display: flex; border-radius: 5px;">
    <div style="flex: 7; padding: 10px;">
        <p>$text</p>
    </div>
    <div style="width: 1px; background: #333;"></div>
    <div style="flex: 3; padding: 10px; display: flex; flex-direction: column; justify-content: center;">
        <pre id="mongoStatus" style="margin: 0;">MDB │ connecting...</pre>
        <pre id="mongoClicks" style="margin: 0; margin-top: 10px;">CLK ░░░░░░░░░░ 0</pre>
        <pre id="mongoDwell" style="margin: 0; margin-top: 10px;">DWL ░░░░░░░░░░ 0</pre>
    </div>
</div>
<script>
    function connectMongo() {
        mongoEs = new EventSource('/mongoMetrics');
        mongoEs.addEventListener('message', (e) => {
            var data = JSON.parse(e.data);
            document.getElementById("mongoStatus").textContent = data.status;
            document.getElementById("mongoClicks").textContent = data.clicks;
            document.getElementById("mongoDwell").textContent = data.dwell;
        });
        mongoEs.addEventListener('error', () => {
            document.getElementById("mongoStatus").textContent = "MDB │ offline";
            document.getElementById("mongoClicks").textContent = "";
            document.getElementById("mongoDwell").textContent = "";
            mongoEs.close();
        });
    }
    connectMongo();
</script>
</div>
""").substitute(text=text)

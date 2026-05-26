from string import Template
from body_texts import get_text_by_name

def get_bio(language: str = "en"):
    return Template(
    """<div style="margin-top: 0px; padding: 0px 10vw; display: flex; border-radius: 5px; border: 0px solid #333; font-family: 'Fira Code', 'JetBrains Mono', 'Cascadia Code', 'Consolas', monospace; font-size: 1.2vw;">
    <div style="flex: 1; padding: 10px;">
        <h2>DATA ENGINEER</h2>
        <p>$par1</p>
    </div>
    <div style="width: 1px; background: #333;"></div>
    <div style="flex: 1; padding: 10px;">
        <p>$par2</p>
    </div>
    <div style="width: 1px; background: #333;"></div>
    <div style="flex: 1; padding: 10px;">
        <p>$par3</p>
    </div>
    <div style="width: 1px; background: #333;"></div>
    <div style="flex: 1; padding: 10px;">
        <p>$par4</p>
    </div>
</div>
<pre id="bioCurve">----------</pre>
<script>
    function connectBio() {
        bioCurveEvent = new EventSource(`/basicCurve?width=$${window.innerWidth}&height=4`);
        bioCurveEvent.addEventListener('message', (e) => {
            document.getElementById("bioCurve").textContent = e.data;
        });
        bioCurveEvent.addEventListener('error', () => {
            document.getElementById("bioCurve").textContent = "Stream ended";
            bioCurveEvent.close();
        });
    }
    connectBio();
    window.addEventListener("resize", () => { bioCurveEvent.close(); connectBio(); });
</script>
""").substitute(par1=get_text_by_name("bio_par1", language), par2=get_text_by_name("bio_par2", language), par3=get_text_by_name("bio_par3", language), par4=get_text_by_name("bio_par4", language))
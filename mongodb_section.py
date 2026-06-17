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
        <pre id="mongoClicksChart" style="margin: 0; font-size: 0.8vw;">CLK │ loading...</pre>
        <pre id="mongoDwellChart" style="margin: 0; margin-top: 15px; font-size: 0.8vw;">DWL │ loading...</pre>
    </div>
</div>
<script>
    function measureMongoChar() {
        const ctx = document.createElement('canvas').getContext('2d');
        ctx.font = getComputedStyle(document.getElementById("mongoClicksChart")).font;
        const metrics = ctx.measureText('M');
        const charWidth = metrics.width;
        const charHeight = (metrics.fontBoundingBoxAscent + metrics.fontBoundingBoxDescent) * 3;
        return { charWidth, charHeight };
    }
    function connectMongoClicks() {
        const { charWidth, charHeight } = measureMongoChar();
        const container = document.getElementById("mongoClicksChart").parentElement;
        const width = container.clientWidth;
        clicksEs = new EventSource(`/mongoClicksChart?width=$${width}&height=$${charHeight * 5}&charWidth=$${charWidth}&charHeight=$${charHeight}`);
        clicksEs.addEventListener('message', (e) => {
            document.getElementById("mongoClicksChart").textContent = e.data;
        });
        clicksEs.addEventListener('error', () => {
            document.getElementById("mongoClicksChart").textContent = "CLK │ offline";
            clicksEs.close();
        });
    }
    function connectMongoDwell() {
        const { charWidth, charHeight } = measureMongoChar();
        const container = document.getElementById("mongoDwellChart").parentElement;
        const width = container.clientWidth;
        dwellEs = new EventSource(`/mongoDwellChart?width=$${width}&height=$${charHeight * 5}&charWidth=$${charWidth}&charHeight=$${charHeight}`);
        dwellEs.addEventListener('message', (e) => {
            document.getElementById("mongoDwellChart").textContent = e.data;
        });
        dwellEs.addEventListener('error', () => {
            document.getElementById("mongoDwellChart").textContent = "DWL │ offline";
            dwellEs.close();
        });
    }
    connectMongoClicks();
    connectMongoDwell();
</script>
</div>
""").substitute(text=text)

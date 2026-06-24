from string import Template
from body_texts import get_text_by_name

def get_resource_section(language: str = "en"):
    text = get_text_by_name("resource_history_par", language)
    return Template("""
<div data-track="history">
<div style="padding: 0px 10vw; margin-top: 20px; display: flex; border-radius: 5px;">
    <div style="flex: 3; padding: 10px; display: flex; flex-direction: column; justify-content: center;">
        <pre id="cpuHistoryChart" style="margin: 0; font-size: 0.8vw;">CPU │ loading...</pre>
    </div>
    <div style="width: 1px; background: #333;"></div>
    <div style="flex: 4; padding: 10px;">
        <p>$text</p>
    </div>
    <div style="width: 1px; background: #333;"></div>
    <div style="flex: 3; padding: 10px; display: flex; flex-direction: column; justify-content: center;">
        <pre id="memHistoryChart" style="margin: 0; font-size: 0.8vw;">MEM │ loading...</pre>
    </div>
</div>
<script>
    function measureHistoryChar() {
        const ctx = document.createElement('canvas').getContext('2d');
        ctx.font = getComputedStyle(document.getElementById("cpuHistoryChart")).font;
        const metrics = ctx.measureText('M');
        const charWidth = metrics.width;
        const charHeight = (metrics.fontBoundingBoxAscent + metrics.fontBoundingBoxDescent) * 3;
        return { charWidth, charHeight };
    }
    function connectCpuHistory() {
        const { charWidth, charHeight } = measureHistoryChar();
        const container = document.getElementById("cpuHistoryChart").parentElement;
        const width = container.clientWidth;
        cpuHistoryEs = new EventSource(`/clusterCpuHistory?width=$${width}&height=$${charHeight * 5}&charWidth=$${charWidth}&charHeight=$${charHeight}`);
        cpuHistoryEs.addEventListener('message', (e) => {
            document.getElementById("cpuHistoryChart").textContent = e.data;
        });
        cpuHistoryEs.addEventListener('error', () => {
            document.getElementById("cpuHistoryChart").textContent = "CPU │ offline";
            cpuHistoryEs.close();
        });
    }
    function connectMemHistory() {
        const { charWidth, charHeight } = measureHistoryChar();
        const container = document.getElementById("memHistoryChart").parentElement;
        const width = container.clientWidth;
        memHistoryEs = new EventSource(`/clusterMemHistory?width=$${width}&height=$${charHeight * 5}&charWidth=$${charWidth}&charHeight=$${charHeight}`);
        memHistoryEs.addEventListener('message', (e) => {
            document.getElementById("memHistoryChart").textContent = e.data;
        });
        memHistoryEs.addEventListener('error', () => {
            document.getElementById("memHistoryChart").textContent = "MEM │ offline";
            memHistoryEs.close();
        });
    }
    connectCpuHistory();
    connectMemHistory();
</script>
</div>
""").substitute(text=text)

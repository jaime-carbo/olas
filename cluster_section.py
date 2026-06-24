from string import Template
from body_texts import get_text_by_name

def get_cluster_section(language: str = "en"):
    text = get_text_by_name("cluster_metrics_par", language)
    return Template("""
<div data-track="cluster">
<div style="padding: 0px 10vw; margin-top: 20px; display: flex; border-radius: 5px;">
    <div style="flex: 7; padding: 10px;">
        <p>$text</p>
    </div>
    <div style="width: 1px; background: #333;"></div>
    <div style="flex: 3; padding: 10px; display: flex; flex-direction: column; justify-content: center;">
        <pre id="clusterChart" style="margin: 0; font-size: 0.8vw;">K8S │ connecting...</pre>
    </div>
</div>
<script>
    function connectCluster() {
        const ctx = document.createElement('canvas').getContext('2d');
        ctx.font = getComputedStyle(document.getElementById("clusterChart")).font;
        const metrics = ctx.measureText('M');
        const charWidth = metrics.width;
        const container = document.getElementById("clusterChart").parentElement;
        const width = container.clientWidth;
        clusterEs = new EventSource(`/clusterMetrics?width=$${width}&charWidth=$${charWidth}`);
        clusterEs.addEventListener('message', (e) => {
            document.getElementById("clusterChart").textContent = e.data;
        });
        clusterEs.addEventListener('error', () => {
            document.getElementById("clusterChart").textContent = "K8S │ offline";
            clusterEs.close();
        });
    }
    connectCluster();
</script>
</div>
""").substitute(text=text)

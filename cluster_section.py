from string import Template
from body_texts import get_text_by_name

def get_cluster_section(language: str = "en"):
    text = get_text_by_name("cluster_metrics_par", language)
    return Template("""
<div style="padding: 0px 10vw; margin-top: 20px; display: flex; border-radius: 5px; font-family: 'Fira Code', 'JetBrains Mono', 'Cascadia Code', 'Consolas', monospace; font-size: 1.2vw;">
    <div style="flex: 7; padding: 10px;">
        <p>$text</p>
    </div>
    <div style="width: 1px; background: #333;"></div>
    <div style="flex: 3; padding: 10px; display: flex; flex-direction: column; justify-content: center;">
        <pre id="clusterPod" style="margin: 0;">K8S │ connecting...</pre>
        <pre id="clusterCpu" style="margin: 0; margin-top: 10px;">CPU ░░░░░░░░░░ 0m/0m</pre>
        <pre id="clusterMem" style="margin: 0; margin-top: 10px;">MEM ░░░░░░░░░░ 0Mi/0Mi</pre>
    </div>
</div>
<script>
    function connectCluster() {
        clusterEs = new EventSource('/clusterMetrics');
        clusterEs.addEventListener('message', (e) => {
            var data = JSON.parse(e.data);
            document.getElementById("clusterPod").textContent = data.pod;
            document.getElementById("clusterCpu").textContent = data.cpu;
            document.getElementById("clusterMem").textContent = data.mem;
        });
        clusterEs.addEventListener('error', () => {
            document.getElementById("clusterPod").textContent = "K8S │ offline";
            document.getElementById("clusterCpu").textContent = "";
            document.getElementById("clusterMem").textContent = "";
            clusterEs.close();
        });
    }
    connectCluster();
</script>
""").substitute(text=text)

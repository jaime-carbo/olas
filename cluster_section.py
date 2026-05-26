from string import Template

def get_cluster_section():
    return """
<div style="padding: 0px 10vw; margin-top: 20px; font-family: 'Fira Code', 'JetBrains Mono', 'Cascadia Code', 'Consolas', monospace; font-size: 1.2vw; color: #999;">
    <pre id="clusterBar" style="color: #ccc;">K8S │ connecting...</pre>
    <script>
        function connectCluster() {
            clusterEs = new EventSource('/clusterMetrics');
            clusterEs.addEventListener('message', (e) => {
                document.getElementById("clusterBar").textContent = e.data;
            });
            clusterEs.addEventListener('error', () => {
                document.getElementById("clusterBar").textContent = "K8S │ offline";
                clusterEs.close();
            });
        }
        connectCluster();
    </script>
</div>
"""

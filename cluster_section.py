from string import Template

def get_cluster_section(info):
    if info is None:
        return """<div style="padding: 0px 10vw; margin-top: 20px; font-family: 'Fira Code', 'JetBrains Mono', 'Cascadia Code', 'Consolas', monospace; font-size: 1.2vw; color: #999;">
    <p>Cluster info unavailable</p>
</div>"""

    node_rows = ""
    for n in info["nodes"]:
        node_rows += f"""<tr><td>{n['name']}</td><td>{n['status']}</td><td>{n['version']}</td><td>{n['cpu']}</td><td>{n['memory']}</td></tr>"""

    pod_rows = ""
    for p in info["pods"]:
        pod_rows += f"""<tr><td>{p['namespace']}</td><td>{p['name']}</td><td>{p['phase']}</td><td>{p['cpu']}</td><td>{p['memory']}</td></tr>"""

    deploy_rows = ""
    for d in info["deployments"]:
        deploy_rows += f"""<tr><td>{d['namespace']}</td><td>{d['name']}</td><td>{d['replicas']}</td><td>{d['image']}</td></tr>"""

    ns_list = ", ".join(info["namespaces"])

    return Template("""
<div style="padding: 0px 10vw; margin-top: 20px; font-family: 'Fira Code', 'JetBrains Mono', 'Cascadia Code', 'Consolas', monospace; font-size: 1.2vw; color: #ccc;">
    <h2 style="color: #fff;">CLUSTER OVERVIEW</h2>

    <h3>Nodes</h3>
    <table style="width: 100%; border-collapse: collapse; text-align: left;">
        <tr style="border-bottom: 1px solid #555;"><th>Name</th><th>Status</th><th>Version</th><th>CPU</th><th>Memory</th></tr>
        $node_rows
    </table>

    <h3>Namespaces</h3>
    <p>$ns_list</p>

    <h3>Pods</h3>
    <table style="width: 100%; border-collapse: collapse; text-align: left;">
        <tr style="border-bottom: 1px solid #555;"><th>Namespace</th><th>Name</th><th>Phase</th><th>CPU</th><th>Memory</th></tr>
        $pod_rows
    </table>

    <h3>Deployments</h3>
    <table style="width: 100%; border-collapse: collapse; text-align: left;">
        <tr style="border-bottom: 1px solid #555;"><th>Namespace</th><th>Name</th><th>Replicas</th><th>Image</th></tr>
        $deploy_rows
    </table>
</div>
""").substitute(node_rows=node_rows, pod_rows=pod_rows, deploy_rows=deploy_rows, ns_list=ns_list)

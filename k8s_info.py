import kubernetes_asyncio
from kubernetes_asyncio import client

_config_loaded = False

async def _load_config():
    global _config_loaded
    if _config_loaded:
        return
    try:
        kubernetes_asyncio.config.load_incluster_config()
    except kubernetes_asyncio.config.ConfigException:
        await kubernetes_asyncio.config.load_kube_config()
    _config_loaded = True

async def get_cluster_info():
    try:
        await _load_config()
        v1 = client.CoreV1Api()
        apps = client.AppsV1Api()
        custom = client.CustomObjectsApi()

        nodes = []
        node_list = await v1.list_node()
        try:
            node_metrics = await custom.list_cluster_custom_object("metrics.k8s.io", "v1beta1", "nodes")
            metrics_map = {m["metadata"]["name"]: m for m in node_metrics.get("items", [])}
        except Exception:
            metrics_map = {}
        for n in node_list.items:
            name = n.metadata.name
            status = next((c.type for c in reversed(n.status.conditions) if c.status == "True"), "Unknown")
            version = n.status.node_info.kubelet_version
            cpu = ""
            mem = ""
            if name in metrics_map:
                cpu = metrics_map[name]["usage"]["cpu"]
                mem = metrics_map[name]["usage"]["memory"]
            nodes.append({"name": name, "status": status, "version": version, "cpu": cpu, "memory": mem})

        namespaces = [ns.metadata.name for ns in (await v1.list_namespace()).items]

        pods = []
        pod_list = await v1.list_pod_for_all_namespaces()
        try:
            pod_metrics = await custom.list_cluster_custom_object("metrics.k8s.io", "v1beta1", "pods")
            pod_metrics_map = {}
            for pm in pod_metrics.get("items", []):
                key = f"{pm['metadata']['namespace']}/{pm['metadata']['name']}"
                pod_metrics_map[key] = pm
        except Exception:
            pod_metrics_map = {}
        for p in pod_list.items:
            ns = p.metadata.namespace
            name = p.metadata.name
            phase = p.status.phase
            key = f"{ns}/{name}"
            cpu = ""
            mem = ""
            if key in pod_metrics_map:
                for c in pod_metrics_map[key].get("containers", []):
                    cpu = c["usage"]["cpu"]
                    mem = c["usage"]["memory"]
            pods.append({"namespace": ns, "name": name, "phase": phase, "cpu": cpu, "memory": mem})

        deployments = []
        for d in (await apps.list_deployment_for_all_namespaces()).items:
            deployments.append({
                "namespace": d.metadata.namespace,
                "name": d.metadata.name,
                "replicas": d.spec.replicas,
                "image": d.spec.template.spec.containers[0].image if d.spec.template.spec.containers else "",
            })

        await v1.api_client.close()
        await apps.api_client.close()
        await custom.api_client.close()

        return {"nodes": nodes, "namespaces": namespaces, "pods": pods, "deployments": deployments}
    except Exception as e:
        print(f"CLUSTER INFO ERROR: {e}")
        return None

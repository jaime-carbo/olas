import os
import kubernetes_asyncio
from kubernetes_asyncio import client

MOCK_MODE = os.environ.get("K8S_MOCK", "").lower() == "true"

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

def _parse_cpu(value):
    if not value:
        return 0
    if value.endswith("n"):
        return int(value[:-1]) / 1_000_000_000
    if value.endswith("u"):
        return int(value[:-1]) / 1_000_000
    if value.endswith("m"):
        return int(value[:-1]) / 1000
    return int(value)

def _parse_memory(value):
    if not value:
        return 0
    if value.endswith("Ki"):
        return int(value[:-2]) * 1024
    if value.endswith("Mi"):
        return int(value[:-2]) * 1024 * 1024
    if value.endswith("Gi"):
        return int(value[:-2]) * 1024 * 1024 * 1024
    return int(value)

async def get_cluster_metrics():
    if MOCK_MODE:
        import random
        cpu_allocatable = 2.0
        mem_allocatable = 4096 * 1024 * 1024
        return {
            "cpu_used": round(random.uniform(0.15, 0.6), 3),
            "cpu_allocatable": cpu_allocatable,
            "mem_used": int(random.uniform(600, 1800) * 1024 * 1024),
            "mem_allocatable": mem_allocatable,
        }

    try:
        await _load_config()
        v1 = client.CoreV1Api()
        custom = client.CustomObjectsApi()

        node_list = await v1.list_node()
        cpu_allocatable = 0
        mem_allocatable = 0
        for n in node_list.items:
            cpu_allocatable += _parse_cpu(n.status.allocatable.get("cpu", "0"))
            mem_allocatable += _parse_memory(n.status.allocatable.get("memory", "0"))

        cpu_used = 0
        mem_used = 0
        try:
            node_metrics = await custom.list_cluster_custom_object("metrics.k8s.io", "v1beta1", "nodes")
            for m in node_metrics.get("items", []):
                cpu_used += _parse_cpu(m["usage"]["cpu"])
                mem_used += _parse_memory(m["usage"]["memory"])
        except Exception:
            pass

        await v1.api_client.close()
        await custom.api_client.close()

        return {
            "cpu_used": round(cpu_used, 3),
            "cpu_allocatable": round(cpu_allocatable, 3),
            "mem_used": mem_used,
            "mem_allocatable": mem_allocatable,
        }
    except Exception as e:
        print(f"CLUSTER METRICS ERROR: {e}")
        return None

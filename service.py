from kubernetes import client, config
from enum import Enum

from yaml_helpers import load_snaked_yml


class ServicePreset(Enum):
    FRONT = "front"


def load_service(preset: ServicePreset):
    if preset == ServicePreset.FRONT:
        service_yml = load_snaked_yml("templates/front_service.yml")
    else:
        raise ValueError(f"Unknown service preset: {preset}")
    metadata = client.V1ObjectMeta(**service_yml["metadata"])
    ports = [client.V1ServicePort(**port) for port in service_yml["spec"]["ports"]]
    spec = client.V1ServiceSpec(**{
        **service_yml["spec"],
        "ports": ports,
    })
    return client.V1Service(**{
        **service_yml,
        "metadata": metadata,
        "spec": spec
    })


def deploy_service(namespace: str, preset: ServicePreset):
    service = load_service(preset)
    return client.CoreV1Api().create_namespaced_service(namespace, service)

from kubernetes import client, config
from pprint import pprint
from enum import Enum
import yaml
import re
from typing import Dict, Any


def to_snake_case(string: str) -> str:
    return re.sub(r'(?<!^)(?=[A-Z])', '_', string).lower()


def to_snake_keys(obj: Dict[str, Any]) -> Dict[str, Any]:
    out = {}
    for key, value in obj.items():
        if isinstance(value, dict):
            value = to_snake_keys(value)
        out[to_snake_case(key)] = value

    return out


def load_snaked_yml(path: str) -> Dict[str, Any]:
    with open(path, "r") as file:
        return to_snake_keys(yaml.safe_load(file))


class DeploymentPreset(Enum):
    FRONT = "front"
    ARBITRATOR = "arbitrator"
    BOT_CLIENT = "bot_client"


class AutoscalerPreset(Enum):
    FRONT = "front"
    ARBITRATOR = "arbitrator"
    BOT_CLIENT = "bot_client"


def load_deployment(preset: DeploymentPreset) -> client.V1Deployment:
    if preset == DeploymentPreset.BOT_CLIENT:
        ...
    elif preset == DeploymentPreset.ARBITRATOR:
        ...
    elif preset == DeploymentPreset.FRONT:
        deployment_yml = load_snaked_yml("templates/front_deployment.yml")
    else:
        raise Exception("Invalid deployment preset")

    metadata = client.V1ObjectMeta(**deployment_yml["metadata"])

    selector = client.V1LabelSelector(**deployment_yml["spec"]["selector"])
    pod_metadata = client.V1ObjectMeta(**deployment_yml["spec"]["template"]["metadata"])
    pod_spec = client.V1PodSpec(**deployment_yml["spec"]["template"]["spec"])
    template = client.V1PodTemplateSpec(**{
        **deployment_yml["spec"]["template"],
        "metadata": pod_metadata,
        "spec": pod_spec
    })
    spec = client.V1DeploymentSpec(**{
        **deployment_yml["spec"],
        "template": template,
        "selector": selector
    })

    return client.V1Deployment(**{
        **deployment_yml,
        "metadata": metadata,
        "spec": spec
    })


def load_autoscaler(preset: AutoscalerPreset) -> client.V2HorizontalPodAutoscaler:
    if preset == AutoscalerPreset.BOT_CLIENT:
        ...
    elif preset == AutoscalerPreset.ARBITRATOR:
        ...
    elif preset == AutoscalerPreset.FRONT:
        autoscaler_yml = load_snaked_yml("templates/front_autoscaler.yml")
    else:
        raise Exception("Invalid autoscaler preset")

    metadata = client.V1ObjectMeta(**autoscaler_yml["metadata"])
    spec = client.V2HorizontalPodAutoscalerSpec(**autoscaler_yml["spec"])
    client.V2HorizontalPodAutoscaler()
    return client.V2HorizontalPodAutoscaler(**autoscaler_yml)


def deploy_deployment(namespace: str, preset: DeploymentPreset):
    deployment = load_deployment(preset)
    client.AppsV1Api().create_namespaced_deployment(namespace, deployment)
    # client.AutoscalingV2Api().create_namespaced_horizontal_pod_autoscaler(namespace, deployment)


if __name__ == '__main__':
    config.load_kube_config()
    deploy_deployment("default", DeploymentPreset.FRONT)

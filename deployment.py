from enum import Enum
from kubernetes import client

from yaml_helpers import load_snaked_yml


class DeploymentPreset(Enum):
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


def deploy_deployment(namespace: str, preset: DeploymentPreset):
    deployment = load_deployment(preset)
    print(client.AppsV1Api().create_namespaced_deployment(namespace, deployment))

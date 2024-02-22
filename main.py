from kubernetes import config

from cluster import clear_cluster
from deployment import DeploymentPreset, deploy_deployment
from service import ServicePreset, deploy_service

if __name__ == '__main__':
    config.load_kube_config()
    # clear_cluster()
    deploy_deployment("default", DeploymentPreset.ARBITRATOR)
    # deploy_service("default", ServicePreset.FRONT)
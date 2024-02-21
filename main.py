from kubernetes import config

from cluster import clear_cluster
from deployment import DeploymentPreset, deploy_deployment

if __name__ == '__main__':
    config.load_kube_config()
    clear_cluster()
    deploy_deployment("default", DeploymentPreset.FRONT)

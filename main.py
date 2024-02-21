from kubernetes import config

from deployment import DeploymentPreset, deploy_deployment

if __name__ == '__main__':
    config.load_kube_config()
    deploy_deployment("default", DeploymentPreset.FRONT)

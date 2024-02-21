from kubernetes import client, config
from pprint import pprint

def make_arbitrator_deployment() -> client.V1Deployment:
    ...

if __name__ == '__main__':
    config.load_kube_config()
    v1 = client.CoreV1Api()
    pprint(dir(v1))
    v1
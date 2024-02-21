import subprocess


def clear_cluster():
    subprocess.run("kubectl delete all --all", shell=True)

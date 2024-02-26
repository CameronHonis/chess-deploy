#!/bin/bash

cd "$(dirname "$0")" || exit

kubectl apply -f https://raw.githubusercontent.com/metallb/metallb/v0.13.7/config/manifests/metallb-native.yaml

kubectl wait --namespace metallb-system \
                --for=condition=ready pod \
                --selector=app=metallb \
                --timeout=90s

kubectl apply -f ip_range_config.yml
kubectl apply -f load_balancer_objs.yml
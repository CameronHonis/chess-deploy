#!/bin/bash

cd "$(dirname $0)" || exit

if [[ $(kind get clusters) == chess-ml ]]; then
  kind delete cluster --name chess-ml
fi

kind create cluster --name chess-ml --config cluster-config.yml

./set_image_pull_creds.sh

kubectl apply -f objs/
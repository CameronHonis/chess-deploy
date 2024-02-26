#!/bin/bash

cd "$(dirname "$0")/.." || exit

kubectl create secret docker-registry pull-image \
--docker-server=gcr.io \
--docker-username=_json_key \
--docker-email=camhonis@gmail.com \
--docker-password="$(cat secrets/image-pull-creds.json)"
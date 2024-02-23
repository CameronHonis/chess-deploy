#!/bin/bash

cd "$(dirname "$0")/../k8s" || exit

if [ "$(ls -1q templates | wc -l)" -eq 0 ]; then
  echo "No templates found"
  exit 1
fi

ls -t templates | head -n 1 | xargs -I {} kubectl apply -f "templates/{}"
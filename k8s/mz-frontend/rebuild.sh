#!/usr/bin/env bash
eval $(minikube -p minikube docker-env)
docker build -t mz-frontend:latest .
kubectl delete pod -l app=mz-frontend

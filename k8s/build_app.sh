#!/bin/bash
# declare -a build_folders=("sjsump-api" "sjsump-cassandra" "sjsump-frontend")
declare -a build_folders=("mz-frontend")

start_minikube() {
    minikube start --cpus='4' —-nodes=1 --memory="8g" --kubernetes-version=v1.23.3 --driver=docker
    if [ "$?" -ne 0 ]; then
        echo "Failed to start minikube - exiting..."
        return 1
    fi
    echo "Verifying that minikube is running. Its IP address is: "
    minikube ip
    if [ "$?" -ne 0 ]; then
        echo "Failed to get IP address of minikube - exiting..."
        return 1
    fi
    return 0
}

build_images() {
    for i in "${build_folders[@]}"
    do
        docker build -t $i:latest $i
    done
    return 0
}

deploy_app() {
    for i in "${build_folders[@]}"
    do
        kubectl apply -f $i
    done
}

# Check user root
USER=`id -u`
if [ $USER -eq 0 ]; then
    echo "Please do not run as root or with sudo"
    exit 2
fi
# Must run docker at least once to ensure the network plumbing is setup by docker rather than minikube
# Minikube doesn't set up networking properly if it is installed before docker is run at least once.
echo "Testing docker..."
docker run --rm hello-world
if [ "$?" -ne 0 ]; then
    echo "failed to setup docker correctly. Please install docker manually and rerun this script"
    exit 2
fi
echo "Docker test successful"

echo "Starting minikube"
start_minikube

echo "Building images"
eval $(minikube -p minikube docker-env)
build_images

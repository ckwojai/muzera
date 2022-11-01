#!/bin/bash
#declare -a build_folders=("sjsump-api" "sjsump-cassandra" "sjsump-frontend")
declare -a build_folders=("mz-frontend")

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

eval $(minikube -p minikube docker-env)
echo "Deploying app"
deploy_app

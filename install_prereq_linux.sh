#!/bin/bash
install_docker() {
    sudo apt-get remove docker docker-engine docker.io containerd runc
    sudo apt-get update
    sudo apt-get install ca-certificates curl gnupg lsb-release --yes
    curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /usr/share/keyrings/docker-archive-keyring.gpg
    echo \
    "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/docker-archive-keyring.gpg] https://download.docker.com/linux/ubuntu \
    $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
    sudo apt-get update
    sudo apt-get install docker-ce docker-ce-cli containerd.io --yes
    sudo docker run hello-world
    if [ "$?" -ne 0 ]; then
        echo "Failed to install docker - exiting..."
        return 1
    fi
    echo "Successfully install Docker!"
    return 0
}

install_minikube() {
    curl -LO https://storage.googleapis.com/minikube/releases/latest/minikube-linux-amd64
    sudo install minikube-linux-amd64 /usr/local/bin/minikube
    sudo usermod -aG docker $USER && newgrp docker
    return 0
}

install_kubectl() {
    sudo snap install kubectl --classic
    return 0
}

install_docker
install_minikube
install_kubectl

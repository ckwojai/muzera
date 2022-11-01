#!/bin/bash
# OS="$(uname -a)"
# if echo ${OS} | grep Ubuntu > /dev/null 2>&1; then
#     OS=Linux
# elif echo ${OS} | grep Darwin > /dev/null 2>&1; then
#     OS=MacOS
# else
#     echo "Unsupported OS: ${OS}. Exiting..."
#     exit 2
# fi

minikube dashboard &
# . config_hosts.sh
sudo minikube tunnel

# sleep 3
# if [ ${OS} == "MacOS" ]; then
#     open http://sjsump.ai
# elif [ ${OS} == "Linux" ]; then
#     xdg-open http://sjsump.ai
# else
#     echo "Unsupported OS: ${OS}. Exiting..."
#     exit 2
# fi

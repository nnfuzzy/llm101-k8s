# Define user data script
user_data = """#!/bin/bash
    # Update and install packages
    apt-get update -y
    apt-get install -y git mc tmux docker.io zsh

    sh -c "$(wget -O- https://raw.githubusercontent.com/ohmyzsh/ohmyzsh/master/tools/install.sh)"

    # Install microk8s
    snap install microk8s --classic

    # Install kubectl
    snap install kubectl --classic

    # Add ubuntu user to docker and microk8s groups
    usermod -aG docker $USER
    usermod -aG microk8s $USER

    # Change default shell to zsh for ubuntu user
    chsh -s $(which zsh) ubuntu

    # Ensure proper permissions for docker
    sudo newgrp docker
    sudo newgrp microk8s
    
    # Wait for microk8s to be ready and enable necessary addons
    microk8s status --wait-ready
    microk8s enable helm && microk8s enable dns &&  microk8s enable storage && microk8s ingress 

    # Create .kube directory for ubuntu user
    mkdir -p /home/ubuntu/.kube
    chown -R ubuntu:ubuntu /home/ubuntu/.kube

    # Generate and copy kubeconfig
    microk8s config > /home/ubuntu/.kube/config
    chown ubuntu:ubuntu /home/ubuntu/.kube/config

    #install brew
    /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
    #echo >> /home/ubuntu/.zshrc                                                                               
    #echo 'eval "$(/home/linuxbrew/.linuxbrew/bin/brew shellenv)"' >> /home/ubuntu/.zshrc
    #eval "$(/home/linuxbrew/.linuxbrew/bin/brew shellenv)"
    #brew install argocd
    """ 
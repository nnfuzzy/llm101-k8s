# Dockerfile
FROM ubuntu:plucky-20241213

# Set non-interactive frontend for apt-get
ENV DEBIAN_FRONTEND=noninteractive

# Update and install prerequisites
RUN apt-get update
RUN apt-get install -y snapd curl zsh git mc tmux docker.io

# Install MicroK8s and other tools in the script
RUN snap install microk8s --classic 
RUN snap install kubectl --classic
    #/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)" && \
    #eval "$(/home/linuxbrew/.linuxbrew/bin/brew shellenv)" && \
    #brew install argocd

# Create and configure user
RUN useradd -ms /bin/bash ubuntu && \
    echo "ubuntu:ubuntu" | chpasswd && \
    usermod -aG docker ubuntu && \
    usermod -aG microk8s ubuntu && \
    mkdir -p /home/ubuntu/.kube && \
    chown -R ubuntu:ubuntu /home/ubuntu/.kube

# Switch shell to Zsh
RUN chsh -s $(which zsh) ubuntu


# Set entrypoint to start testing
CMD ["/bin/bash"]
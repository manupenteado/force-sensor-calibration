FROM ubuntu:24.04

ENV DEBIAN_FRONTEND=noninteractive

ARG USERNAME=vscode
ARG USER_UID=1000
ARG USER_GID=1000

# Criar usuário vscode
RUN groupadd --gid $USER_GID $USERNAME \
 && useradd --uid $USER_UID --gid $USER_GID -m $USERNAME \
 && apt-get update \
 && apt-get install -y --no-install-recommends \
    python3 python3-pip python3-venv build-essential ca-certificates curl git sudo \
 && rm -rf /var/lib/apt/lists/*

# Permissão sudo para o usuário vscode
RUN echo "$USERNAME ALL=(ALL) NOPASSWD:ALL" > /etc/sudoers.d/$USERNAME && chmod 0440 /etc/sudoers.d/$USERNAME

WORKDIR /workspace

# Copia requirements e instala dependências na imagem (uma vez, durante build)
COPY requirements.txt /workspace/requirements.txt
RUN python3 -m pip install --upgrade pip && \
    python3 -m pip install -r /workspace/requirements.txt

# Define diretório do projeto e ajusta permissões
WORKDIR /workspaces/force-sensor-calibration
RUN mkdir -p /workspaces && chown -R $USERNAME:$USERNAME /workspaces || true

USER $USERNAME
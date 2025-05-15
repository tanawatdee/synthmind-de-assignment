FROM mcr.microsoft.com/devcontainers/python:1-3.12-bullseye

RUN apt-get update && \
    export DEBIAN_FRONTEND=noninteractive

RUN echo "alias ll='ls -alF'" >> /home/vscode/.bashrc
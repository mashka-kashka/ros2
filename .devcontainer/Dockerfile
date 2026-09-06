FROM mcr.microsoft.com/devcontainers/base:ubuntu26.04

# Install system dependencies required by Qt6 and GUI rendering
RUN apt-get update \
    && apt-get -y install python3-pyqt6 \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

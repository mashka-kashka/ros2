FROM mcr.microsoft.com/devcontainers/base:ubuntu24.04
# Install system dependencies required by Qt6 and GUI rendering
RUN apt-get update \
    && apt-get -y install python3-venv python3-pip python3-venv python3-uvloop python3-pyqt6 qt6-base-dev qt6-tools-dev pyqt6-dev-tools npm \
    && apt-get clean && rm -rf /var/lib/apt/lists/* \
    && usermod -aG video vscode
RUN pip3 install cython setuptools unidiff pyyaml mediapipe opencv-python numpy pytest colcon-common-extensions empy lark typing-extensions --break-system-packages
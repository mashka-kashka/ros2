#!/bin/bash
set -e

envsubst < src/ros2.repos | vcs import src
sudo apt-get update
rosdep update --rosdistro=$ROS_DISTRO
rosdep install --from-paths src --ignore-src -y --rosdistro=$ROS_DISTRO

#python3 -m venv .venvs/ros2_venv
#source .venvs/ros2_venv/bin/activate
#pip install black==21.12b0 cython setuptools unidiff pyyaml mediapipe opencv-python numpy pytest colcon-common-extensions em
#pip install cython setuptools unidiff pyyaml mediapipe opencv-python numpy pytest colcon-common-extensions empy lark typing-extensions
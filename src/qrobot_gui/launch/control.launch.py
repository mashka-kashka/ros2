#!/usr/bin/env python3

from launch import LaunchDescription
from launch_ros.actions import Node

def generate_launch_description():

    # Основной узел для управления
    control_node = Node(
            package='qrobot_gui',
            executable='control',
            name='qrobot_gui',
            output='screen'
        )
    
    return LaunchDescription([
        control_node
    ])
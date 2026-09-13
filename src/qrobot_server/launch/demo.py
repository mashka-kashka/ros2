#!/usr/bin/env python3

import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch_ros.actions import Node

def generate_launch_description():
    pkg_share = get_package_share_directory('qrobot_server')
    rviz_config_path = os.path.join(pkg_share, 'rviz',
                                    'qrobot_server_config.rviz')

    rqt_node = Node(
            package='rqt_image_view',
            executable='rqt_image_view',
            name='rqt',
            output='screen'
        )

    # Узел камеры
    camera_node = Node(
            package='v4l2_camera',
            executable='v4l2_camera_node',
            name='v4l2_camera',
            output='screen',
            parameters=[{
                'video_device': '/dev/video0',
                'image_size': [640, 480],
                #'pixel_format': 'YUYV',
                #'output_encoding': 'rgb8'
            }]
            # Pass the configuration file path as separate argument list items
            #arguments=['-p', 'pixel_format:="mjpeg2rgb"']
        )

    # Узел RViz
    rviz_node = Node(
            package='rviz2',
            executable='rviz2',
            name='rviz2',
            # Pass the configuration file path as separate argument list items
            arguments=['-d', rviz_config_path],
            output='screen'
        )

    image_node = Node(
            package='image_tools',
            executable='showimage',
            name='showimage',
            # Pass the configuration file path as separate argument list items
            arguments=['-r', '/image:=/image_raw'],
            output='screen'
        )

    # Серверный узел робота
    server_node = Node(
            package='qrobot_server',
            executable='gui',
            name='qrobot_server',
            output='screen'
        )
    
    return LaunchDescription([
        camera_node,
        server_node
    ])
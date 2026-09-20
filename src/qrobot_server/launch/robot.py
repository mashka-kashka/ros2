#!/usr/bin/env python3

import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node

def generate_launch_description():
    pkg_share = get_package_share_directory('qrobot_server')

    camera_param_name = "camera"
    camera_param_default = str(0)
    camera_param = LaunchConfiguration(
        camera_param_name,
        default=camera_param_default,
    )

    camera_node = Node(
        package='camera_ros',
        executable='camera_node',
        output='screen',
        parameters=[{
                "camera": camera_param,
                "format": "RGB888",
                "width": 320,
                "height": 240,
                "role": "video",
        }]
    )
    
    img_transport_node = Node(
		package='image_transport',
		executable='republish',
		name='republish_ffmpeg',
		output='screen',
		arguments=['compressed', 'raw'],
		remappings=[
			('/camera/image_raw', '/camera/image_raw_2'),
			('/camera/image_raw/compressed', '/camera/image_raw/compressed_2')
		] 
    )

    return LaunchDescription([
		#img_transport_node,
        camera_node
    ])

from launch import LaunchDescription
from launch_ros.actions import Node

def generate_launch_description():
    cam = Node(
        package='v4l2_camera',
        executable='v4l2_camera_node',
        name='webcam',
        parameters=[{
            # 'video_device': '/dev/video0',
            # 'frame_rate': 30,
        }]
    )

    hf = Node(
        package='mediapipe_ros2_py',
        executable='hf_node',
        name='mediapipe_node',
        output='screen',
        parameters=[{
            'image_topic': '/image_raw',
            'topic_prefix': '/mediapipe'
        }]
    )

    train = Node(
            package='qrobot_gui',
            executable='train',
            name='train_node',
            output='screen'
        )

    return LaunchDescription([cam, hf, train])

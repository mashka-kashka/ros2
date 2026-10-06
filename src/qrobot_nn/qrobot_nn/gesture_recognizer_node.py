import os
import rclpy
from rclpy.node import Node
from std_msgs.msg import String
from rclpy.qos import QoSProfile, ReliabilityPolicy, HistoryPolicy
from mediapipe_ros2_interfaces.msg import (
    HandLandmarks, Hand
)

class GestureRecognizerNode(Node):
    """
    Gesture recognizer node
    """
    def __init__(self):
        super().__init__('gesture_recognizer_node')

        # -------- Parameters --------
        self.declare_parameter('model_name', 'rock_paper_scissors.mdl')
        self.declare_parameter('landmarks_topic', '/mediapipe/hand/landmarks')
        self.declare_parameter('markers_topic', '/mediapipe/hand/markers')
        self.declare_parameter('out_topic', '/qrobot/gesture')
        self.declare_parameter('topic', 'gesture')
        self.declare_parameter('min_detection_confidence', 0.5)

        # -------- Read params --------
        self.model_name = str(self.get_parameter('model_name').value).lower()
        self.landmarks_topic = str(self.get_parameter('landmarks_topic').value)
        self.markers_topic = str(self.get_parameter('markers_topic').value)
        self.out_topic = str(self.get_parameter('out_topic').value)
        self.min_det = float(self.get_parameter('min_detection_confidence').value)

        self._last_report = self.get_clock().now().nanoseconds
        from ament_index_python.packages import get_package_share_directory
        share_dir = get_package_share_directory('qrobot_nn')
        self.models_dir = os.path.join(share_dir, 'models')

        self.publisher_ = self.create_publisher(String, self.out_topic, 10)
        timer_period = 1.0  # секунды
        self.timer = self.create_timer(timer_period, self.timer_callback)
        self.i = 0
        self.get_logger().info('Gesture recognizer node started')

    def timer_callback(self):
        msg = String()
        msg.data = f'Gesture, count={self.i}'
        self.publisher_.publish(msg)
        self.get_logger().info(f'Publishing: {msg.data}')
        self.i += 1

def main() -> None:
    rclpy.init()
    rclpy.spin(GestureRecognizerNode())
    rclpy.shutdown()


if __name__ == '__main__':
    main()

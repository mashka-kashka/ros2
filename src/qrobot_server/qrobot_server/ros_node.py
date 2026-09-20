import sys

# Qt
from PyQt6.QtCore import QObject, QTimer, pyqtSignal
from PyQt6.QtGui import QImage
from PyQt6.QtWidgets import QApplication

# ROS
import rclpy
from rclpy.node import Node
from rclpy.qos import QoSProfile, ReliabilityPolicy, HistoryPolicy
from sensor_msgs.msg import Image
from cv_bridge import CvBridge

# OpenCV
import cv2

# Робот
from qrobot_server.main_window import QRobotMainWindow

class QRobot(QObject):
    """Класс для связи с Qt"""
    image_received = pyqtSignal(QImage) # Сигнал о получении изображения

class RosNode(Node):
    """Основной узел ROS."""

    def __init__(self, qrobot):
        super().__init__('ros_node')
        self.qrobot = qrobot
        self.cv_bridge = CvBridge()

        qos_profile = QoSProfile(
            reliability=ReliabilityPolicy.BEST_EFFORT,
            history=HistoryPolicy.KEEP_LAST,
            depth=1
        )

        # Подписка на изображения с камеры
        self.create_subscription(
            Image,
            "/camera/image_raw",
            self.image_callback,
            qos_profile
        )

    def image_callback(self, msg):
        try:
            # Convert raw ROS image to an OpenCV BGR image
            cv_img = self.cv_bridge.imgmsg_to_cv2(msg, desired_encoding="bgr8")
            
            # Convert BGR (OpenCV) to RGB (Qt standard)
            rgb_img = cv2.cvtColor(cv_img, cv2.COLOR_BGR2RGB)
            h, w, ch = rgb_img.shape
            bytes_per_line = ch * w
            
            # Convert NumPy array to QImage
            qt_image = QImage(
                rgb_img.data, 
                w, 
                h, 
                bytes_per_line, 
                QImage.Format.Format_RGB888
            )
            
            # Emit copy to avoid garbage collection/memory access race conditions
            self.qrobot.image_received.emit(qt_image)
            
        except Exception as e:
            print(f"Error parsing image: {e}")
def main(args=None):
    rclpy.init(args=args)

    app = QApplication(sys.argv)

    qrobot = QRobot()

    # Create ROS node
    ros_node = RosNode(qrobot)

    # Create GUI window
    window = QRobotMainWindow(app, qrobot)
    window.show()

    # Use QTimer to spin ROS 2 callbacks inside the Qt event loop
    timer = QTimer()
    timer.timeout.connect(lambda: rclpy.spin_once(ros_node, timeout_sec=0.01))
    timer.start(5)

    # Run Qt application loop
    exit_code = app.exec()

    # Clean shutdown
    ros_node.destroy_node()
    rclpy.shutdown()
    sys.exit(exit_code)


if __name__ == '__main__':
    main()
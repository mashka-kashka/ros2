import sys
import zlib

# Qt
from PyQt6.QtCore import QObject, QTimer, pyqtSignal
from PyQt6.QtGui import QImage
from PyQt6.QtWidgets import QApplication

# ROS
import rclpy
from rclpy.node import Node
from rclpy.qos import QoSProfile, ReliabilityPolicy, HistoryPolicy
from sensor_msgs.msg import CompressedImage

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

        qos_profile = QoSProfile(
            reliability=ReliabilityPolicy.BEST_EFFORT,
            history=HistoryPolicy.KEEP_LAST,
            depth=1
        )

        # Подписка на изображения с камеры
        self.create_subscription(
            CompressedImage,
            "/camera/image_raw/compressed",
            self.image_callback,
            qos_profile
        )

    def image_callback(self, msg):
        try:
            compressed_data = msg.data
            decompressed_data = zlib.decompress(compressed_data)
            qt_image = QImage.fromData(decompressed_data)
            if not qt_image.isNull():
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

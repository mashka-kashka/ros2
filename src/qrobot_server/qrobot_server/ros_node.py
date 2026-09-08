import sys

from PyQt6.QtCore import QTimer
from PyQt6.QtWidgets import QApplication, QMainWindow, QPushButton, QVBoxLayout, QWidget
import rclpy
from rclpy.node import Node
from std_msgs.msg import String
from qrobot_server.main_window import QRobotMainWindow


class QRobotRosNode(Node):

    """Основной узел ROS."""

    def __init__(self, callback_ui_update):
        super().__init__('qrobot_ros_node')
        self.publisher_ = self.create_publisher(String, 'chopper_topic', 10)
        self.callback_ui_update = callback_ui_update

    def send_message(self, text):
        msg = String()
        msg.data = text
        self.publisher_.publish(msg)
        self.get_logger().info(f'Published: "{text}"')


class MainWindow(QMainWindow):

    """Главное окно приложения."""

    def __init__(self, ros_node):
        super().__init__()
        self.ros_node = ros_node
        self.setWindowTitle('ROS 2 PyQt6 Node')

        # Layout & Widgets
        self.button = QPushButton('Publish Message')
        self.button.clicked.connect(self.on_button_clicked)

        layout = QVBoxLayout()
        layout.addWidget(self.button)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

    def on_button_clicked(self):
        self.ros_node.send_message('Hello from PyQt6!')


def main(args=None):
    rclpy.init(args=args)

    app = QApplication(sys.argv)

    # Create ROS node
    ros_node = QRobotRosNode(callback_ui_update=None)

    # Create GUI window
    window = QRobotMainWindow(app, ros_node)
    window.show()

    # Use QTimer to spin ROS 2 callbacks inside the Qt event loop
    timer = QTimer()
    timer.timeout.connect(lambda: rclpy.spin_once(ros_node, timeout_sec=0.01))
    timer.start(10)  # 10ms interval

    # Run Qt application loop
    exit_code = app.exec()

    # Clean shutdown
    ros_node.destroy_node()
    rclpy.shutdown()
    sys.exit(exit_code)


if __name__ == '__main__':
    main()

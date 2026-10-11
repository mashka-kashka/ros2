import sys

# Qt
from PyQt6.QtCore import QObject, QTimer, pyqtSignal
from PyQt6.QtWidgets import QApplication

# ROS
import rclpy
from rclpy.node import Node
from rclpy.qos import QoSProfile, ReliabilityPolicy, HistoryPolicy

# Mediapipe
from mediapipe_ros2_interfaces.msg import (
    HandLandmarks, Hand
)

from qrobot_gui.train_window import QTrainWindow

class QTrainObject(QObject):
    """Класс для связи с Qt"""
    hand_received = pyqtSignal(Hand)

class TrainNode(Node):
    """Основной узел для обучения моделей"""

    def __init__(self, qobject):
        super().__init__('train_node')
        self.qobject = qobject

        # Объявление параметров
        self.declare_parameter('hand_lm_topic', '/mediapipe/hand/landmarks')

        # Чтение параметров
        self.hand_lm_topic = str(self.get_parameter('hand_lm_topic').value)

        # Создание подписок
        qos = QoSProfile(reliability=ReliabilityPolicy.BEST_EFFORT,
                         history=HistoryPolicy.KEEP_LAST, depth=5)
        self.sub_hand_lm = self.create_subscription(HandLandmarks,
                                                    self.hand_lm_topic,
                                                    self.on_hand_landmarks,
                                                    qos)

    def on_hand_landmarks(self, msg: HandLandmarks):
        for hand in msg.hands:
            self.get_logger().info("Обнаружена рука: %s, %s", 
                hand.handedness,
                hand.score,
            )
            self.qobject.hand_received.emit(hand)

def main(args=None):
    rclpy.init(args=args)

    app = QApplication(sys.argv)

    qobject = QTrainObject()

    # Create ROS node
    train_node = TrainNode(qobject)

    # Create GUI window
    window = QTrainWindow(app, qobject)
    window.show()

    # Use QTimer to spin ROS 2 callbacks inside the Qt event loop
    timer = QTimer()
    timer.timeout.connect(lambda: rclpy.spin_once(train_node, timeout_sec=0.01))
    timer.start(5)

    # Run Qt application loop
    exit_code = app.exec()

    # Clean shutdown
    train_node.destroy_node()
    rclpy.shutdown()
    sys.exit(exit_code)


if __name__ == '__main__':
    main()
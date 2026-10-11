import os
import sys
import json
import logging
from datetime import datetime, timezone
import rclpy
from rclpy.node import Node
from std_msgs.msg import String
from rclpy.qos import QoSProfile, ReliabilityPolicy, HistoryPolicy
from mediapipe_ros2_suite.src.mediapipe_ros2_interfaces.msg import (
    HandLandmarks, Hand
)

class GestureRecognizerNode(Node):
    """
    Gesture recognizer node
    """
    def __init__(self):
        super().__init__('gesture_recognizer_node')

        # Логирование
        log_handler = logging.StreamHandler()
        log_handler.setFormatter(JSONFormatter())

        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.INFO)
        self.logger.addHandler(log_handler)

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

        # -------- Subscriber --------
        qos = QoSProfile(reliability=ReliabilityPolicy.BEST_EFFORT,
                         history=HistoryPolicy.KEEP_LAST, depth=5)
        self.sub_hand_lm = self.create_subscription(HandLandmarks,
                                                    self.landmarks_topic,
                                                    self.on_hand_landmarks,
                                                    qos)

    def on_hand_landmarks(self, msg: HandLandmarks):
        #self.logger.info(msg)
        for hand in msg.hands:
            self.logger.info("Обнаружена рука", extra={
                "handedness": hand.handedness,
                "score": hand.score,
                }
            )

class JSONFormatter(logging.Formatter):
    def format(self, record: logging.LogRecord) -> str:
        log_data = {
            "timestamp": datetime.fromtimestamp(
                record.created, tz=timezone.utc
            ).isoformat(),
            "level": record.levelname,
            "logger": record.name,
            "message": record.getMessage(),
            "handedness": getattr(record, "score", None),
            "score": getattr(record, "score", None),
        }
        if record.exc_info:
            log_data["exception"] = self.formatException(record.exc_info)

        return json.dumps(log_data, ensure_ascii=False)

def main() -> None:
    rclpy.init()
    rclpy.spin(GestureRecognizerNode())
    rclpy.shutdown()


if __name__ == '__main__':
    main()

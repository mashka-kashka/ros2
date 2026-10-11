import logging

# Qt
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QMainWindow, QGraphicsScene, QGraphicsPixmapItem
from PyQt6.QtGui import QPixmap

from qrobot_gui.control_window_ui import Ui_ControlWindow
from qrobot_gui.log_handler import QLogHandler

class QControlWindow(QMainWindow):

    def __init__(self, app, qobject):
        super().__init__()

        self.app = app
        self.qobject = qobject

        self.ui = Ui_ControlWindow()
        self.ui.setupUi(self)

        # Логирование
        handler = QLogHandler(self.ui.teLog)
        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
        handler.setFormatter(formatter)

        self.logger = logging.getLogger('control_node')
        self.logger.setLevel(logging.INFO)
        self.logger.addHandler(handler)

        # Камера
        self.scene = QGraphicsScene()
        self.ui.gv_camera.setScene(self.scene)
        self.scenePixmapItem = None
        self.qobject.image_received.connect(self.update_camera_image)

        self.logger.info("Начало работы")

    def update_camera_image(self, qt_image):
        self.logger.debug("Получено изображение с камеры")
        pixmap = QPixmap.fromImage(qt_image)
        if self.scenePixmapItem is None:
            self.scenePixmapItem = QGraphicsPixmapItem(pixmap)
            self.scene.addItem(self.scenePixmapItem)
            self.scenePixmapItem.setZValue(0)
        else:
            self.scenePixmapItem.setPixmap(pixmap)

        self.ui.gv_camera.fitInView(self.scene.sceneRect(), Qt.AspectRatioMode.KeepAspectRatio)
        self.ui.gv_camera.show()

    def on_config(self):
        pass
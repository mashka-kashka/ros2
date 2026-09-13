# Qt
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QMainWindow, QGraphicsScene, QGraphicsPixmapItem
from PyQt6.QtGui import QPixmap

# Робот
from qrobot_server.main_window_ui import Ui_MainWindow


class QRobotMainWindow(QMainWindow):

    def __init__(self, app, qrobot):
        super().__init__()

        self.app = app
        self.qrobot = qrobot

        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.logger = self.ui.teLog

        # Камера
        self.scene = QGraphicsScene()
        self.ui.gv_camera.setScene(self.scene)
        self.scenePixmapItem = None
        self.qrobot.image_received.connect(self.update_camera_image)

    def update_camera_image(self, qt_image):
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
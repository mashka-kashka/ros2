from PyQt6.QtWidgets import QMainWindow
from qrobot_server.main_window_ui import Ui_MainWindow


class QRobotMainWindow(QMainWindow):

    def __init__(self, app, ros_node):
        super().__init__()

        self.app = app
        self.ros_node = ros_node

        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.logger = self.ui.teLog

    def on_config(self):
        pass
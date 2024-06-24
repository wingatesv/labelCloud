from PyQt5.QtWidgets import QMainWindow, QPushButton, QVBoxLayout, QWidget
from PyQt5.QtCore import QSize
from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QDesktopWidget
from labelCloud.control.controller import Controller
from labelCloud.view.gui import GUI
import pkg_resources
import logging
import sys
import platform
from PyQt5.QtCore import QSettings

class MainMenu(QMainWindow):
    def __init__(self):
        super().__init__()

        uic.loadUi(
            pkg_resources.resource_filename(
                "labelCloud.resources.interfaces", "main_menu_interface.ui"
            ),
            self,
        )
        self.setWindowTitle("MIMOS Main Menu")
        self.setMinimumSize(QSize(500, 500))


        # Set up the existing button (assuming it's named annotate_pushButton)
        self.annotate_pushButton.clicked.connect(self.on_annotate_button_clicked)

        theme = "dark" if self.is_dark_mode() else "light"
        self.setProperty("theme", theme)
        self.setStyleSheet(self.get_stylesheet())

    def on_annotate_button_clicked(self):
        self.start_gui()
        self.close()

    def is_dark_mode(self):
        if platform.system() == "Darwin":  # macOS
            os_theme = QSettings().value("AppleInterfaceStyle", "Light")
            return os_theme == "Dark"
        # Add other platform-specific checks if necessary
        return False


    def start_gui(self):
        app = QApplication.instance() or QApplication(sys.argv)

        # Setup Model-View-Control structure
        control = Controller()
        view = GUI(control)

        app.installEventFilter(view)

        # Start GUI
        view.show()

        app.setStyle("Fusion")
        desktop = QDesktopWidget().availableGeometry()
        width = (desktop.width() - view.width()) // 2
        height = (desktop.height() - view.height()) // 2
        view.move(width, height)

        # Close the main menu page when annotate_pushButton is clicked
        self.annotate_pushButton.clicked.connect(self.close)

        logging.info("Showing Annotation GUI...")
        # sys.exit(app.exec_())


    
    def get_stylesheet(self):
        return """
        QWidget {
            background-color: white;
            color: black;
        }

        QMainWindow[theme="dark"] QWidget {
            background-color: #1E1E1E;
            color: white;
        }

        QPushButton {
            background-color: #007AFF;
            color: white;
            border-radius: 10px;
        }

        QLabel {
            color: inherit;
        }
        """

     

#  type: ignore

import logging
from pathlib import Path
import sys
import pkg_resources
from PyQt5 import uic
from PyQt5.QtWidgets import QDialog, QApplication
from PyQt5.QtCore import QSettings, Qt
from PyQt5.QtGui import QPalette
import platform

from ..control.config_manager import config, config_manager
from ..control.label_manager import LabelManager
from ..io.labels.config import LabelConfig


class SettingsDialog(QDialog):
    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        self.parent_gui = parent
        ui_path = self._get_ui_path("settings_interface.ui")
        uic.loadUi(ui_path, self)
        self.fill_with_current_settings()

        self.save_button.clicked.connect(self.save)
        self.cancel_button.clicked.connect(self.cancel)
        self.reset_button.clicked.connect(self.reset)

        self.apply_theme()

    def _get_ui_path(self, ui_filename):
            """Get the path to the UI file, considering whether running in PyInstaller bundle or not."""
            if getattr(sys, 'frozen', False):
                # Running in a PyInstaller bundle
                base_path = Path(sys._MEIPASS)
            else:
                # Running in a development environment
                base_path = Path(__file__).resolve().parent.parent
            
            return base_path / "resources" / "interfaces" / ui_filename
    def fill_with_current_settings(self) -> None:
        # File
        self.lineEdit_pointcloudfolder.setText(config.get("FILE", "pointcloud_folder"))
        self.lineEdit_labelfolder.setText(config.get("FILE", "label_folder"))

        # Pointcloud
        self.doubleSpinBox_pointsize.setValue(
            config.getfloat("POINTCLOUD", "POINT_SIZE")
        )
        self.lineEdit_pointcolor.setText(config["POINTCLOUD"]["colorless_color"])
        self.checkBox_colorizecolorless.setChecked(
            config.getboolean("POINTCLOUD", "colorless_colorize")
        )
        self.doubleSpinBox_standardtranslation.setValue(
            config.getfloat("POINTCLOUD", "std_translation")
        )
        self.doubleSpinBox_standardzoom.setValue(
            config.getfloat("POINTCLOUD", "std_zoom")
        )

        # Label
        self.comboBox_labelformat.addItems(LabelConfig().type.get_available_formats())
        self.comboBox_labelformat.setCurrentText(LabelConfig().format)

        self.comboBox_defaultobjectclass.addItems(LabelConfig().get_classes().keys())
        self.comboBox_defaultobjectclass.setCurrentText(
            LabelConfig().get_default_class_name()
        )

        self.spinBox_exportprecision.setValue(
            config.getint("LABEL", "export_precision")
        )
        self.doubleSpinBox_minbboxdimensions.setValue(
            config.getfloat("LABEL", "min_boundingbox_dimension")
        )
        self.doubleSpinBox_stdbboxlength.setValue(
            config.getfloat("LABEL", "std_boundingbox_length")
        )
        self.doubleSpinBox_stdbboxwidth.setValue(
            config.getfloat("LABEL", "std_boundingbox_width")
        )
        self.doubleSpinBox_stdbboxheight.setValue(
            config.getfloat("LABEL", "std_boundingbox_height")
        )
        self.doubleSpinBox_stdbboxtranslation.setValue(
            config.getfloat("LABEL", "std_translation")
        )
        self.doubleSpinBox_stdbboxrotation.setValue(
            config.getfloat("LABEL", "std_rotation")
        )
        self.doubleSpinBox_stdbboxscaling.setValue(
            config.getfloat("LABEL", "std_scaling")
        )
        self.checkBox_propagatelabels.setChecked(
            config.getboolean("LABEL", "propagate_labels")
        )

        # User Interface
        self.checkBox_zrotationonly.setChecked(
            config.getboolean("USER_INTERFACE", "z_rotation_only")
        )
        self.checkBox_showfloor.setChecked(
            config.getboolean("USER_INTERFACE", "show_floor")
        )
        self.checkBox_showbboxorientation.setChecked(
            config.getboolean("USER_INTERFACE", "show_orientation")
        )
        self.checkBox_keepperspective.setChecked(
            config.getboolean("USER_INTERFACE", "keep_perspective")
        )
        self.spinBox_viewingprecision.setValue(
            config.getint("USER_INTERFACE", "viewing_precision")
        )
        self.lineEdit_backgroundcolor.setText(
            config.get("USER_INTERFACE", "background_color")
        )
        self.checkBox_show2dimage.setChecked(
            config.getboolean("USER_INTERFACE", "show_2d_image")
        )

    def save(self) -> None:
        # File
        config["FILE"]["pointcloud_folder"] = self.lineEdit_pointcloudfolder.text()
        config["FILE"]["label_folder"] = self.lineEdit_labelfolder.text()

        # Pointcloud
        config["POINTCLOUD"]["point_size"] = str(self.doubleSpinBox_pointsize.value())
        config["POINTCLOUD"]["colorless_color"] = self.lineEdit_pointcolor.text()
        config["POINTCLOUD"]["colorless_colorize"] = str(
            self.checkBox_colorizecolorless.isChecked()
        )
        config["POINTCLOUD"]["std_translation"] = str(
            self.doubleSpinBox_standardtranslation.value()
        )
        config["POINTCLOUD"]["std_zoom"] = str(self.doubleSpinBox_standardzoom.value())

        # Label
        LabelConfig().set_label_format(self.comboBox_labelformat.currentText())
        LabelConfig().set_default_class(self.comboBox_defaultobjectclass.currentText())
        config["LABEL"]["export_precision"] = str(self.spinBox_exportprecision.value())
        config["LABEL"]["min_boundingbox_dimension"] = str(
            self.doubleSpinBox_minbboxdimensions.value()
        )
        config["LABEL"]["std_boundingbox_length"] = str(
            self.doubleSpinBox_stdbboxlength.value()
        )
        config["LABEL"]["std_boundingbox_width"] = str(
            self.doubleSpinBox_stdbboxwidth.value()
        )
        config["LABEL"]["std_boundingbox_height"] = str(
            self.doubleSpinBox_stdbboxheight.value()
        )
        config["LABEL"]["std_translation"] = str(
            self.doubleSpinBox_stdbboxtranslation.value()
        )
        config["LABEL"]["std_rotation"] = str(
            self.doubleSpinBox_stdbboxrotation.value()
        )
        config["LABEL"]["std_scaling"] = str(self.doubleSpinBox_stdbboxscaling.value())
        config["LABEL"]["propagate_labels"] = str(
            self.checkBox_propagatelabels.isChecked()
        )

        # User Interface
        config["USER_INTERFACE"]["z_rotation_only"] = str(
            self.checkBox_zrotationonly.isChecked()
        )
        config["USER_INTERFACE"]["show_floor"] = str(
            self.checkBox_showfloor.isChecked()
        )
        config["USER_INTERFACE"]["show_orientation"] = str(
            self.checkBox_showbboxorientation.isChecked()
        )
        config["USER_INTERFACE"]["show_2d_image"] = str(
            self.checkBox_show2dimage.isChecked()
        )
        config["USER_INTERFACE"]["keep_perspective"] = str(
            self.checkBox_keepperspective.isChecked()
        )
        config["USER_INTERFACE"][
            "background_color"
        ] = self.lineEdit_backgroundcolor.text()
        config["USER_INTERFACE"]["viewing_precision"] = str(
            self.spinBox_viewingprecision.value()
        )

        config_manager.write_into_file()
        self.parent_gui.set_checkbox_states()
        self.parent_gui.controller.pcd_manager.label_manager = LabelManager(
            strategy=LabelConfig().format,
            path_to_label_folder=Path(config["FILE"]["label_folder"]),
        )
        logging.info("Saved and activated new configuration!")
        self.accept()  # Close the dialog after saving

    def reset(self) -> None:
        config_manager.reset_to_default()
        self.fill_with_current_settings()

    def cancel(self) -> None:
        logging.info("Settings dialog was canceled!")
        self.reject()  # Close the dialog when canceled


    def is_dark_mode(self):
        if platform.system() == "Darwin":  # macOS
            os_theme = QSettings().value("AppleInterfaceStyle", "Light")
            return os_theme == "Dark"
        # Add other platform-specific checks if necessary
        return False
    def apply_theme(self):
        is_dark = self.is_dark_mode()

        theme = "dark" if is_dark else "light"
   
        self.setProperty("theme", theme)
        self.setStyleSheet(self.get_stylesheet())
        current_theme = self.property("theme")
        print(f"Current theme property: {current_theme}")

    def get_stylesheet(self):
        return """
        QDialog {
            background-color: #ffffff;
            color: black;
        }

        QDialog[theme="dark"] {
            background-color: #1E1E1E;
            color: white;
        }

        QLabel {
            background-color: transparent;
            color: black;
        }

        QDialog[theme="dark"] QLabel {
            color: white;
        }

        QLineEdit {
            background-color: white;
            color: black;
        }

        QDialog[theme="dark"] QLineEdit {
            background-color: #2E2E2E;
            color: white;
        }

        QCheckBox {
            color: inherit;
        }

        QDialog[theme="dark"] QCheckBox {
            background-color: black;
            color: white;
        }

        QPlainTextEdit {
            background-color: white;
            color: black;
        }

        QDialog[theme="dark"] QPlainTextEdit {
            background-color: black;
            color: white;
        }

        QComboBox {
            background-color: white;
            color: black;
        }

        QDialog[theme="dark"] QComboBox {
            background-color: #2E2E2E;
            color: white;
        }

        QDoubleSpinBox {
            background-color: white;
            color: black;
        }

        QDialog[theme="dark"] QDoubleSpinBox {
            background-color: #2E2E2E;
            color: white;
        }

        QSpinBox {
            background-color: white;
            color: black;
        }

        QDialog[theme="dark"] QSpinBox {
            background-color: #2E2E2E;
            color: white;
        }

        QPushButton {
            background-color: white;
            color: black;
            border-radius: 10px;
            border: 1px solid black;
        }

        QDialog[theme="dark"] QPushButton {
            background-color: black;
            color: white;
            border-radius: 10px;
            border: 1px solid white;
        }

        """






import os
import sys

# Get the absolute path of the current script file
script_path = os.path.abspath(__file__)

# Get the root directory by going up one level from the script directory
project_root = os.path.dirname(os.path.dirname(script_path))

sys.path.insert(0, project_root)
sys.path.insert(0, os.getcwd())  # Add the current directory as well

from src.huggingFaceModelClass import HuggingFaceModelClass
from src.modelUnit import ModelUnit

from PyQt5.QtCore import Qt, QCoreApplication, QUrl, QThread, pyqtSignal
from PyQt5.QtGui import QGuiApplication, QFont, QIcon, QDesktopServices
from PyQt5.QtWidgets import QApplication, QLabel, QTableWidget, QAbstractItemView, QHeaderView, QMessageBox, QTableWidgetItem

QApplication.setAttribute(Qt.AA_EnableHighDpiScaling)
QCoreApplication.setAttribute(Qt.AA_UseHighDpiPixmaps)  # HighDPI support
# qt version should be above 5.14
QGuiApplication.setHighDpiScaleFactorRoundingPolicy(Qt.HighDpiScaleFactorRoundingPolicy.PassThrough)

QApplication.setFont(QFont('Arial', 12))

QApplication.setWindowIcon(QIcon('hf-logo.svg'))


class Thread(QThread):
    installFinished = pyqtSignal(str)
    installFailed = pyqtSignal(str, str)

    def __init__(self, hf_class, model_text, model_type):
        super(Thread, self).__init__()
        self.__hf_class = hf_class
        self.__model_text = model_text
        self.__model_type = model_type

    def run(self):
        try:
            self.__hf_class.installHuggingFaceModel(self.__model_text, self.__model_type)
            self.installFinished.emit(self.__model_text)
        except Exception as e:
            self.installFailed.emit(str(e), self.__model_text)


class HuggingFaceModelRequirementsWidget(QTableWidget):
    def __init__(self, models=None):
        super(HuggingFaceModelRequirementsWidget, self).__init__()
        models = models if models else []
        self.__initVal(models)
        self.__initUi()

    def __initVal(self, models):
        self.__models = models

        self.__hf_class = HuggingFaceModelClass()

    def open_link(self, url):
        QDesktopServices.openUrl(QUrl(url))

    def set_hyperlink(self, row, column, text):
        label = QLabel(text)
        label.setOpenExternalLinks(True)
        label.setAlignment(Qt.AlignCenter)
        self.setCellWidget(row, column, label)

    def __initUi(self):
        self.setWindowTitle('HuggingFace Required Models for App')
        columns = ['Model', 'Link', 'Type', 'Size', 'Install']
        self.setColumnCount(len(columns))
        self.resizeColumnsToContents()
        self.setHorizontalHeaderLabels(columns)
        self.verticalHeader().setVisible(False)
        self.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.setSelectionBehavior(QAbstractItemView.SelectRows)

        for i in range(len(self.__models)):
            cur_table_idx = self.rowCount()
            self.setRowCount(cur_table_idx+1)

            cur_model_name = ''
            cur_model_type = 'General'
            if isinstance(self.__models[i], dict):
                cur_model_name = self.__models[i]['id']
                cur_model_type = self.__models[i].get('type', 'General')
            else:
                cur_model_name = self.__models[i]

            model_name_item = QTableWidgetItem(cur_model_name)
            model_name_item.setTextAlignment(Qt.AlignCenter)
            self.setItem(cur_table_idx, 0, model_name_item)

            # name
            hyperlink_tag = f'<a href="https://huggingface.co/{cur_model_name}">{cur_model_name}</a>'
            self.set_hyperlink(cur_table_idx, 1, hyperlink_tag)

            model_type_item = QTableWidgetItem(cur_model_type)
            model_type_item.setTextAlignment(Qt.AlignCenter)
            self.setItem(cur_table_idx, 2, model_type_item)

            size = self.__hf_class.getModelsSize([cur_model_name])
            model_size_item = QTableWidgetItem(size)
            model_size_item.setTextAlignment(Qt.AlignCenter)
            self.setItem(cur_table_idx, 3, model_size_item)

            f = self.__hf_class.is_model_exists(cur_model_name)
            modelUnit = ModelUnit(cur_model_name, f)
            modelUnit.onInstalledClicked.connect(self.__installModel)
            modelUnit.onRemovedClicked.connect(self.__removeModel)

            self.setCellWidget(cur_table_idx, 4, modelUnit)

        self.horizontalHeader().setSectionResizeMode(0, QHeaderView.Stretch)
        self.horizontalHeader().setSectionResizeMode(1, QHeaderView.Stretch)
        self.horizontalHeader().setSectionResizeMode(2, QHeaderView.ResizeToContents)
        self.horizontalHeader().setSectionResizeMode(3, QHeaderView.ResizeToContents)
        self.verticalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.resizeColumnsToContents()

    def __installModel(self, model_name):
        model_type = self.__findModelRowAndGetType(model_name)
        self.__t = Thread(self.__hf_class, model_name, model_type)
        self.__t.start()
        self.__t.installFinished.connect(self.__afterFinished)
        self.__t.installFailed.connect(self.__afterFailed)

    # todo refactoring __findModelRowAndGetType and __findModelRowAndToggleIt
    def __findModelRowAndGetType(self, model_name):
        for i in range(self.rowCount()):
            model_item = self.item(i, 0)
            model_type_item = self.item(i, 2)
            model_size_item = self.item(i, 3)
            size = self.__hf_class.getModelsSize([model_name])
            model_unit = self.cellWidget(i, 4)
            if model_item.text() == model_name:
                return model_type_item.text()

    def __findModelRowAndToggleIt(self, model_name, f):
        for i in range(self.rowCount()):
            model_item = self.item(i, 0)
            model_size_item = self.item(i, 3)
            size = self.__hf_class.getModelsSize([model_name])
            model_unit = self.cellWidget(i, 4)
            if model_item.text() == model_name:
                model_size_item.setText(size)
                model_unit.toggleWidget(f)

    def __removeModel(self, model_name):
        self.__hf_class.removeHuggingFaceModel(model_name)
        self.__findModelRowAndToggleIt(model_name, False)

    def __afterFinished(self, model_name):
        self.__findModelRowAndToggleIt(model_name, True)

    def __afterFailed(self, msg, model_text):
        QMessageBox.critical(self, "Error", msg)
        self.__findModelRowAndToggleIt(model_text, False)


if __name__ == '__main__':
    import sys

    app = QApplication(sys.argv)
    w = HuggingFaceModelRequirementsWidget([{'id':'runwayml/stable-diffusion-v1-5', 'type':'Stable Diffusion'},
 {'id':'CompVis/stable-diffusion-v1-4', 'type':'Stable Diffusion'},
 {'id':'deepset/tinyroberta-squad2'},
 {'id':'prompthero/openjourney', 'type':'Stable Diffusion'},
 {'id':'SG161222/Realistic_Vision_V1.4', 'type':'Stable Diffusion'},
 {'id':'stabilityai/stable-diffusion-2-1-base', 'type':'Stable Diffusion'},
 {'id':'tuner007/pegasus_paraphrase'}])
    w.resize(640, 480)
    w.show()
    sys.exit(app.exec())


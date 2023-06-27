import os
import sys

from PyQt5.QtCore import Qt, QCoreApplication, QThread, pyqtSignal
from PyQt5.QtGui import QGuiApplication, QFont, QIcon
from PyQt5.QtWidgets import QVBoxLayout, QApplication, QWidget, QMessageBox

from src.huggingFaceModelClass import HuggingFaceModelClass
from src.huggingFaceModelRequirementsTableWidget import HuggingFaceModelRequirementsTableWidget

# Get the absolute path of the current script file
script_path = os.path.abspath(__file__)

# Get the root directory by going up one level from the script directory
project_root = os.path.dirname(os.path.dirname(script_path))

sys.path.insert(0, project_root)
sys.path.insert(0, os.getcwd())  # Add the current directory as well


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
            self.installFailed.emit(str(e), self.__model_text
                                    )

class HuggingFaceModelRequirementsWidget(QWidget):
    def __init__(self):
        super(HuggingFaceModelRequirementsWidget, self).__init__()
        self.__initVal()
        self.__initUi()

    def __initVal(self):
        self.__hf_class = HuggingFaceModelClass()

    def __initUi(self):
        self.setWindowTitle('HuggingFace Required Models for App')

        # set desired model to show

        # The dictionary should be defined as follows:
        # { "id": "model_name", "type": "type" }
        # The "type" should be written as either "General" or "Stable Diffusion." If the type is not specified, it will be initialized as "General."
        # I couldn't find a definitive way to extract the type based on the model name from HuggingFace, so we had no choice but to do it as follows.

        model_subset = [{'id': 'runwayml/stable-diffusion-v1-5', 'type': 'Stable Diffusion'},
                        {'id': 'CompVis/stable-diffusion-v1-4', 'type': 'Stable Diffusion'},
                        {'id': 'deepset/tinyroberta-squad2'},
                        {'id': 'prompthero/openjourney', 'type': 'Stable Diffusion'},
                        {'id': 'SG161222/Realistic_Vision_V1.4', 'type': 'Stable Diffusion'},
                        {'id': 'stabilityai/stable-diffusion-2-1-base', 'type': 'Stable Diffusion'},
                        {'id': 'tuner007/pegasus_paraphrase'}]

        self.__tableWidget = HuggingFaceModelRequirementsTableWidget(self.__hf_class, model_subset)
        self.__tableWidget.onModelInstalled.connect(self.installedModel)

        lay = QVBoxLayout()
        lay.addWidget(self.__tableWidget)
        self.setLayout(lay)

    def installedModel(self, model_name, model_type):
        self.__t = Thread(self.__hf_class, model_name, model_type)
        self.__t.start()
        self.__t.installFinished.connect(self.__afterFinished)
        self.__t.installFailed.connect(self.__afterFailed)

    def __afterFinished(self, model_name):
        self.__tableWidget.findModelRowAndToggleIt(model_name, True)

    def __afterFailed(self, msg, model_text):
        QMessageBox.critical(self, "Error", msg)
        self.__tableWidget.findModelRowAndToggleIt(model_text, False)


if __name__ == '__main__':
    import sys

    app = QApplication(sys.argv)
    w = HuggingFaceModelRequirementsWidget()
    w.resize(640, 480)
    w.show()
    sys.exit(app.exec())


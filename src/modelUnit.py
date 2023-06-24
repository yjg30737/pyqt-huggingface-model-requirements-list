from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import QWidget, \
    QPushButton, QLabel, QHBoxLayout, QSpacerItem, \
    QSizePolicy, QVBoxLayout

from src.loadingLbl import LoadingLabel


class ModelUnit(QWidget):
    onInstalledClicked = pyqtSignal(str)
    onRemovedClicked = pyqtSignal(str)

    def __init__(self, model_name: str, installed: bool):
        super(ModelUnit, self).__init__()
        self.__initVal(model_name, installed)
        self.__initUi()

    def __initVal(self, model_name: str, installed: bool):
        self.__model_name = model_name
        self.__installed = installed

    def __initUi(self):
        self.__installBtn = QPushButton()
        self.__installBtn.setSizePolicy(QSizePolicy.MinimumExpanding, QSizePolicy.MinimumExpanding)
        self.__toggleButton(self.__installed)
        self.__installBtn.clicked.connect(self.__installRemoveModel)

        self.__loadingLabel = LoadingLabel()

        lay = QVBoxLayout()
        lay.addWidget(self.__installBtn)
        lay.addWidget(self.__loadingLabel)
        lay.setContentsMargins(0, 0, 0, 0)

        self.setLayout(lay)

    def __installRemoveModel(self):
        self.__handleUnitDuringProcessing(False)
        if self.__installed:
            self.onRemovedClicked.emit(self.__model_name)
        else:
            self.onInstalledClicked.emit(self.__model_name)

    def toggleWidget(self, f: bool):
        """
        this will call when install process is finished
        :param f:
        :return:
        """
        self.__toggleButton(f)
        self.__handleUnitDuringProcessing(True)
        self.__installed = f

    def __toggleButton(self, f: bool):
        if f:
            self.__installBtn.setText('Remove')
        else:
            self.__installBtn.setText('Install')

    def __handleUnitDuringProcessing(self, f):
        self.__installBtn.setEnabled(f)
        if f:
            self.__loadingLabel.stop()
        else:
            self.__loadingLabel.start()
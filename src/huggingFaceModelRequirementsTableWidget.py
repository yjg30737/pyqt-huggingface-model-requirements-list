
from PyQt5.QtCore import Qt, QUrl, pyqtSignal
from PyQt5.QtGui import QDesktopServices
from PyQt5.QtWidgets import QLabel, QTableWidget, QAbstractItemView, QHeaderView, QMessageBox, QTableWidgetItem

from src.huggingFaceModelClass import HuggingFaceModelClass
from src.modelUnit import ModelUnit


class HuggingFaceModelRequirementsTableWidget(QTableWidget):
    onModelInstalled = pyqtSignal(str, str)

    def __init__(self, hf_class, models=None):
        super(HuggingFaceModelRequirementsTableWidget, self).__init__()
        models = models if models else []
        self.__initVal(hf_class, models)
        self.__initUi()

    def __initVal(self, hf_class, models):
        self.__hf_class = hf_class
        self.__models = models

    def open_link(self, url):
        QDesktopServices.openUrl(QUrl(url))

    def set_hyperlink(self, row, column, text):
        label = QLabel(text)
        label.setOpenExternalLinks(True)
        label.setAlignment(Qt.AlignCenter)
        self.setCellWidget(row, column, label)

    def __initUi(self):
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
        self.onModelInstalled.emit(model_name, model_type)

    # todo refactoring __findModelRowAndGetType and findModelRowAndToggleIt
    def __findModelRowAndGetType(self, model_name):
        for i in range(self.rowCount()):
            model_item = self.item(i, 0)
            model_type_item = self.item(i, 2)
            model_size_item = self.item(i, 3)
            size = self.__hf_class.getModelsSize([model_name])
            model_unit = self.cellWidget(i, 4)
            if model_item.text() == model_name:
                return model_type_item.text()

    def findModelRowAndToggleIt(self, model_name, f):
        for i in range(self.rowCount()):
            model_item = self.item(i, 0)
            model_size_item = self.item(i, 3)
            size = self.__hf_class.getModelsSize([model_name])
            model_unit = self.cellWidget(i, 4)
            if model_item.text() == model_name:
                model_size_item.setText(size)
                model_unit.toggleWidget(f)

    # the process of removing model happens immediately, so it doesn't need thread
    def __removeModel(self, model_name):
        self.__hf_class.removeHuggingFaceModel(model_name)
        self.findModelRowAndToggleIt(model_name, False)
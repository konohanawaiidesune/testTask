# This Python file uses the following encoding: utf-8
import sys
from PyQt5.QtCore import Qt, QDir, QUrl
from PyQt5 import QtWidgets, uic
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox, QFileSystemModel
from PyQt5.QtGui import QDesktopServices

from explorer_design import Ui_MainWindow

class Window(QMainWindow, Ui_MainWindow):
    
    def __init__(self):
        super(Window, self).__init__()

        self.setupUi(self)
        #uic.loadUi('explorer_design.ui', self)
        
        self.show()
        self.backButton.clicked.connect(self.upperDirect)
        self.directPath.clear()

        self.directPath.setText(QDir.homePath())#вывод пути до домашней директории
        QDir.setCurrent(QDir.homePath())
        self.curDir = QDir.current()#установка текущей директории

        self.dirModel = QFileSystemModel()#создание файловой модели
        self.dirModel.setRootPath(self.curDir.absolutePath())

        self.dirContent.setModel(self.dirModel)
        self.dirContent.setRootIndex(self.dirModel.index(self.curDir.absolutePath()))

        self.dirContent.doubleClicked.connect(self.openItem)#двойной клик по файлу/директории
        self.directPath.returnPressed.connect(self.toInputDir)#ввод пути до директории в строку ввода QLineEdit

    def upperDirect(self):#переход на уровень выше
        check = self.curDir.cdUp()
        if check:#если получилось перейти
            QDir.setCurrent(self.curDir.absolutePath())#установка текущей директории
            self.directPath.setText(self.curDir.absolutePath())#вывод пути

            self.dirModel.setRootPath(self.curDir.absolutePath())#обновление подкаталогов и файлов 

            self.dirContent.setModel(self.dirModel)
            self.dirContent.setRootIndex(self.dirModel.index(self.curDir.absolutePath()))
        else:
            QMessageBox.about(self, "Невозможно перейти в директорию", "Данная директория является корневой")

    def openItem(self, index):#открытие подкаталога/файла
        item = self.dirModel.data(index, Qt.DisplayRole)#путь выбранной директории
        if self.dirModel.isDir(index):#проверка, папка ли это
            check = self.curDir.cd(item)#проверка, можно ли перейти к этой директории
            if check:
                QDir.setCurrent(self.curDir.absolutePath())
                self.directPath.setText(self.curDir.absolutePath())

                self.dirModel.setRootPath(self.curDir.absolutePath())

                self.dirContent.setModel(self.dirModel)
                self.dirContent.setRootIndex(self.dirModel.index(self.curDir.absolutePath()))
                #QMessageBox.about(self, "not file", "papka")
            else:
                QMessageBox.about(self, "Возникла ошибка", "Директории не существует")
        else:#если выбран файл, то он открывается
            QDesktopServices.openUrl(QUrl.fromLocalFile(item))

    def toInputDir(self):#переход по введенному в QLineEdit пути
        path = self.directPath.text()#путь
        check = self.curDir.cd(path)#проверка, можно ли перейти
        if check:
            QDir.setCurrent(self.curDir.absolutePath())#установка новой текущей директории
            self.directPath.setText(self.curDir.absolutePath())

            self.dirModel.setRootPath(self.curDir.absolutePath())

            self.dirContent.setModel(self.dirModel)
            self.dirContent.setRootIndex(self.dirModel.index(self.curDir.absolutePath()))
            #QMessageBox.about(self, "not file", "papka")
        else:
            QMessageBox.about(self, "Возникла ошибка", "Неверно указан путь")

def window():
    app = QApplication(sys.argv)
    win = Window()
    # ...
    sys.exit(app.exec_())

window()
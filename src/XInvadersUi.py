# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'mainwindow.ui'
#
# Created by: PyQt5 UI code generator 5.5.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):
    def setupUi(self, mainWindow, glWindow):
        mainWindow.setObjectName("MainWindow")
        mainWindow.resize(700, 700)
        self.centralWidget = QtWidgets.QWidget(mainWindow)
        self.centralWidget.setObjectName("centralWidget")
        self.painel_menu = QtWidgets.QWidget(self.centralWidget)
        self.painel_menu.setGeometry(QtCore.QRect(0, -1, 700, 701))
        self.painel_menu.setObjectName("painel_menu")
        self.verticalLayoutWidget = QtWidgets.QWidget(self.painel_menu)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(0, 190, 701, 321))
        self.verticalLayoutWidget.setObjectName("verticalLayoutWidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout.setSizeConstraint(QtWidgets.QLayout.SetDefaultConstraint)
        self.verticalLayout.setContentsMargins(11, 11, 11, 11)
        self.verticalLayout.setSpacing(6)
        self.verticalLayout.setObjectName("verticalLayout")
        self.label_2 = QtWidgets.QLabel(self.verticalLayoutWidget)
        font = QtGui.QFont()
        font.setFamily("Impact")
        font.setPointSize(36)
        self.label_2.setFont(font)
        self.label_2.setObjectName("label_2")
        self.verticalLayout.addWidget(self.label_2, 0, QtCore.Qt.AlignHCenter)
        self.btnNovoJogo = QtWidgets.QPushButton(self.verticalLayoutWidget)
        self.btnNovoJogo.setEnabled(True)
        self.btnNovoJogo.setObjectName("btnNovoJogo")
        self.verticalLayout.addWidget(self.btnNovoJogo, 0, QtCore.Qt.AlignHCenter)
        self.label = QtWidgets.QLabel(self.verticalLayoutWidget)
        font = QtGui.QFont()
        font.setPointSize(16)
        font.setBold(True)
        font.setItalic(True)
        font.setWeight(75)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.verticalLayout.addWidget(self.label, 0, QtCore.Qt.AlignHCenter)
        self.painel_jogo = QtWidgets.QWidget(self.centralWidget)
        self.painel_jogo.setGeometry(QtCore.QRect(0, 0, 700, 700))
        self.painel_jogo.setObjectName("painel_jogo")
        self.jogo = glWindow(self.painel_jogo)
        self.jogo.setGeometry(QtCore.QRect(0, 0, 700, 700))
        self.jogo.setObjectName("jogo")
        self.painel_jogo.raise_()
        self.painel_menu.raise_()
        mainWindow.setCentralWidget(self.centralWidget)
        self.retranslateUi(mainWindow)
        self.btnNovoJogo.clicked.connect(self.iniciaJogo)
        QtCore.QMetaObject.connectSlotsByName(mainWindow)

    def retranslateUi(self, mainWindow):
        _translate = QtCore.QCoreApplication.translate
        mainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.label_2.setText(_translate("MainWindow", "X-Invaders"))
        self.btnNovoJogo.setText(_translate("MainWindow", "Novo Jogo"))
        self.label.setText(_translate("MainWindow", "Vamos ver onde consegue chegar!"))

    def iniciaJogo(self):
        self.painel_menu.hide()
        self.jogo.iniciaJogo = True


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow, QtWidgets.QOpenGLWidget)
    MainWindow.show()
    sys.exit(app.exec_())
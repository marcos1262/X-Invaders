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

        palette = QtGui.QPalette()
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.WindowText, brush)
        self.centralWidget.setPalette(palette)

        self.painel_menu = QtWidgets.QWidget(self.centralWidget)
        self.painel_menu.setGeometry(QtCore.QRect(0, -1, 700, 701))
        self.painel_menu.setAutoFillBackground(False)
        self.painel_menu.setObjectName("painel_menu")

        self.verticalLayoutWidget = QtWidgets.QWidget(self.painel_menu)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(0, 190, 701, 321))
        self.verticalLayoutWidget.setObjectName("verticalLayoutWidget")

        self.verticalLayout = QtWidgets.QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout.setSizeConstraint(QtWidgets.QLayout.SetDefaultConstraint)
        self.verticalLayout.setContentsMargins(11, 11, 11, 11)
        self.verticalLayout.setSpacing(6)
        self.verticalLayout.setObjectName("verticalLayout")

        font = QtGui.QFont()
        font.setFamily("Impact")
        font.setPointSize(36)
        self.titulo = QtWidgets.QLabel(self.verticalLayoutWidget)
        self.titulo.setFont(font)
        self.titulo.setObjectName("titulo")
        self.verticalLayout.addWidget(self.titulo, 0, QtCore.Qt.AlignHCenter)

        self.btnNovoJogo = QtWidgets.QPushButton(self.verticalLayoutWidget)
        self.btnNovoJogo.setEnabled(True)
        self.btnNovoJogo.setObjectName("btnNovoJogo")
        self.btnNovoJogo.clicked.connect(self.iniciaJogo)
        self.verticalLayout.addWidget(self.btnNovoJogo, 0, QtCore.Qt.AlignHCenter)

        font = QtGui.QFont()
        font.setPointSize(16)
        font.setBold(True)
        font.setItalic(True)
        font.setWeight(75)
        self.slogan = QtWidgets.QLabel(self.verticalLayoutWidget)
        self.slogan.setFont(font)
        self.slogan.setObjectName("slogan")
        self.verticalLayout.addWidget(self.slogan, 0, QtCore.Qt.AlignHCenter)

        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setItalic(False)
        font.setUnderline(False)
        font.setWeight(75)
        self.melhor = QtWidgets.QLabel(self.verticalLayoutWidget)
        self.melhor.setFont(font)
        self.melhor.setAlignment(QtCore.Qt.AlignCenter)
        self.melhor.setObjectName("melhor")
        self.verticalLayout.addWidget(self.melhor)

        self.ultima = QtWidgets.QLabel(self.verticalLayoutWidget)
        self.ultima.setAlignment(QtCore.Qt.AlignCenter)
        self.ultima.setObjectName("ultima")
        self.verticalLayout.addWidget(self.ultima)

        self.painel_jogo = QtWidgets.QWidget(self.centralWidget)
        self.painel_jogo.setGeometry(QtCore.QRect(0, 0, 700, 700))
        self.painel_jogo.setObjectName("painel_jogo")

        self.jogo = glWindow(self.painel_jogo)
        self.jogo.setGeometry(QtCore.QRect(0, 0, 700, 700))
        self.jogo.setObjectName("jogo")

        self.labelPontos = QtWidgets.QLabel(self.painel_jogo)
        self.labelPontos.setEnabled(True)
        self.labelPontos.setGeometry(QtCore.QRect(10, 10, 154, 17))
        self.labelPontos.setObjectName("labelPontos")

        self.labelNivel = QtWidgets.QLabel(self.painel_jogo)
        self.labelNivel.setEnabled(True)
        self.labelNivel.setGeometry(QtCore.QRect(10, 30, 154, 17))
        self.labelNivel.setObjectName("labelNivel")

        self.labelHP = QtWidgets.QLabel(self.painel_jogo)
        self.labelHP.setEnabled(True)
        self.labelHP.setGeometry(QtCore.QRect(600, 10, 154, 17))
        self.labelHP.setObjectName("labelHP")

        self.jogo.raise_()
        self.labelPontos.raise_()
        self.labelNivel.raise_()
        self.labelHP.raise_()
        self.painel_jogo.raise_()
        self.painel_menu.raise_()
        mainWindow.setCentralWidget(self.centralWidget)
        self.retranslateUi(mainWindow)
        QtCore.QMetaObject.connectSlotsByName(mainWindow)

    def retranslateUi(self, mainWindow):
        _translate = QtCore.QCoreApplication.translate
        mainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.titulo.setText(_translate("MainWindow", "X-Invaders"))
        self.btnNovoJogo.setText(_translate("MainWindow", "Novo Jogo"))
        self.slogan.setText(_translate("MainWindow", "Vamos ver onde consegue chegar!"))
        self.melhor.setText(_translate("MainWindow", ""))
        self.ultima.setText(_translate("MainWindow", ""))
        self.labelPontos.setText(_translate("MainWindow", ""))
        self.labelNivel.setText(_translate("MainWindow", ""))
        self.labelHP.setText(_translate("MainWindow", ""))

    def iniciaJogo(self):
        self.painel_menu.hide()
        self.jogo.setFocus()
        self.jogo.iniciaJogo = True
        QtCore.QCoreApplication.sendEvent(
            self.jogo.timerMusicaFundo,
            QtCore.QTimerEvent(self.jogo.timerMusicaFundo.timerId())
        )


if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow, QtWidgets.QOpenGLWidget)
    MainWindow.show()
    sys.exit(app.exec_())

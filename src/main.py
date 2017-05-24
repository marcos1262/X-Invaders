import os
from random import randint

from OpenGL.GL import *

from PyQt5.QtCore import QUrl, Qt, QTimer
from PyQt5.QtMultimedia import QSound, QMediaPlayer, QMediaContent
from PyQt5.QtWidgets import *
from random import *
from Nave import Nave
from XInvadersUi import Ui_MainWindow
from CameraOrtogonal import CameraOrtogonal

jogoLargura, jogoAltura = 700, 700


class XInvaders(QOpenGLWidget):
    """
    Representa o jogo.
    """
    def __init__(self, parent):
        QOpenGLWidget.__init__(self, parent)
        self.iniciaJogo = False
        self.nivel = 0

        self.maxinimigos = 5
        self.numinimigos = 0

        self.camera = None

        self.jogador = None
        self.boss = None
        self.tiros = []
        self.asteroides = []
        self.estrelas = []
        self.inimigos = []

        self.jogador = Nave(65, 72, 0, py(-45), Nave.Tipos.JOGADOR)
        self.cria_objetos()

        # self.tocaTema()

        # a = QSound("../sounds/SFX/Falcon Laser 1.wav", self)
        # a.play()

        # TODO tocar tema infinitamente
        # dir_projeto = os.getcwd() + "/../"
        #
        # url = QUrl().fromLocalFile(dir_projeto + "sounds/ThemeMusicB19.mp3")
        # content = QMediaContent(url)
        # player = QMediaPlayer()
        # player.setMedia(content)
        # player.play()
        # player.stateChanged.connect(lambda: player.disconnect())

        self.startTimer(30)

    def initializeGL(self):
        """
        Configurações inicias (tela e câmera).
        Habilita transparência, teste de profundidade, define cor de fundo, modo de superfície e inicializa câmera.
        :return: None
        """
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
        glEnable(GL_BLEND)

        glDepthFunc(GL_LESS)
        glEnable(GL_DEPTH_TEST)

        glClearColor(0, 0, 0, 0)

        glShadeModel(GL_SMOOTH)

        self.camera = CameraOrtogonal(jogoLargura, jogoAltura, True)

    def paintGL(self):
        """
        Desenha a cena.
        Limpa tela, desenha objetos da cena, verifica ocorrrências de colisão, mostra pontuação e atualiza tela.
        :return: None
        """
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        # TODO Desenha fundo estelar

        if not self.iniciaJogo:
            glFlush()
            return

        # TODO remover objetos fora da cena

        for asteroide in self.asteroides:   asteroide.desenha()
        for estrela in self.estrelas:       estrela.desenha()
        for inimigo in self.inimigos:       inimigo.desenha()
        for tiro in self.tiros:             tiro.desenha()

        self.jogador.desenha()

        self.detecta_colisoes()

        self.mostra_pontuacao()

        # TODO mostrar minitutorial de como jogar (no nível 0)

        glFlush()

    def timerEvent(self, event):
        self.update()

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Left:  self.jogador.esquerda = True
        if event.key() == Qt.Key_Right: self.jogador.direita = True
        if event.key() == Qt.Key_Up:    self.jogador.cima = True
        if event.key() == Qt.Key_Down:  self.jogador.baixo = True

    def keyReleaseEvent(self, event):
        if event.key() == Qt.Key_Left:  self.jogador.esquerda = False
        if event.key() == Qt.Key_Right: self.jogador.direita = False
        if event.key() == Qt.Key_Up:    self.jogador.cima = False
        if event.key() == Qt.Key_Down:  self.jogador.baixo = False

    def cria_objetos(self):
        while(self.numinimigos < self.maxinimigos):
            self.inimigos.append(Nave(65, 70, randint(px(-50)+65, px(50)-65), py(50), Nave.Tipos.CAPANGA)); self.numinimigos+=1
        # TODO inicializar objetos

    def detecta_colisoes(self):
        # TODO Verificar colisões, remover da lista de objetos, contabilizar pontuação
        pass

    def mostra_pontuacao(self):
        # TODO Mostrar pontuação
        pass


def px(porcentagem):
    """
    Retorna valor de uma posição no eixo X da tela baseado em uma porcentagem.
    :param porcentagem: porcentagem da tela que se deseja saber o valor.
    :return: valor da posição no eixo X da tela
    """
    return jogoLargura * porcentagem / 100


def py(porcentagem):
    """
    Retorna valor de uma posição no eixo X da tela baseado em uma porcentagem.
    :param porcentagem: porcentagem da tela que se deseja saber o valor.
    :return: valor da posição no eixo X da tela
    """
    return jogoLargura * porcentagem / 100


if __name__ == '__main__':
    import sys

    app = QApplication(sys.argv)
    MainWindow = QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow, XInvaders)
    MainWindow.show()
    sys.exit(app.exec_())

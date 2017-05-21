import os

from OpenGL.GL import *

from PyQt5.QtCore import QUrl
from PyQt5.QtMultimedia import QSound, QMediaPlayer, QMediaContent
from PyQt5.QtWidgets import *

from Nave import Nave
from CameraOrtogonal import CameraOrtogonal
from XInvadersUi import Ui_MainWindow

jogoLargura, jogoAltura = 700, 700


class XInvaders(QOpenGLWidget):
    """
    Representa o jogo
    """
    def __init__(self, parent):
        QOpenGLWidget.__init__(self, parent)
        self.iniciaJogo = False
        self.nivel = 0
        self.camera = None

        self.jogador = None
        self.boss = None
        self.tiros = []
        self.asteroides = []
        self.estrelas = []
        self.inimigos = []

        self.inicializaObjetos()

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

    def initializeGL(self):
        """
        Configurações inicias (tela e câmera)
        :return: None
        """
        # Habilita transparência
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
        glEnable(GL_BLEND)

        # Habilita teste de profundidade
        glDepthFunc(GL_LESS)
        glEnable(GL_DEPTH_TEST)

        # Define cor de fundo
        glClearColor(0, 0, 0, 0)

        # Modo de superfície suave
        glShadeModel(GL_SMOOTH)

        # Inicializa câmera
        self.camera = CameraOrtogonal(jogoLargura, jogoAltura, True)

    def paintGL(self):
        """
        Desenha a cena
        :return: None
        """
        # Limpa tela
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        # TODO Desenha fundo estelar

        if not self.iniciaJogo:
            # Atualiza tela
            glFlush()
            return

        # TODO remover objetos fora da cena

        # Desenha objetos da cena
        for asteroide in self.asteroides:   asteroide.desenha()
        for estrela in self.estrelas:       estrela.desenha()
        for inimigo in self.inimigos:       inimigo.desenha()
        for tiro in self.tiros:             tiro.desenha()
        self.jogador.desenha()

        # Verifica ocorrências de colisão
        self.detectaColisoes()

        # TODO mostrar minitutorial de como jogar (no nível 0)

        # Atualiza tela
        glFlush()

    def inicializaObjetos(self):
        self.jogador = Nave(25, 40, 0, py(-25), Nave.Tipos.JOGADOR)
        # TODO inicializar objetos

    def detectaColisoes(self):
        # TODO Verificar colisões
        pass


def px(porcentagem):
    """
    Retorna valor de uma posição no eixo X da tela baseado em uma porcentagem
    :param porcentagem: porcentagem da tela que se deseja saber o valor
    :return: valor da posição no eixo X da tela
    """
    return jogoLargura * porcentagem / 100


def py(porcentagem):
    """
    Retorna valor de uma posição no eixo X da tela baseado em uma porcentagem
    :param porcentagem: porcentagem da tela que se deseja saber o valor
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

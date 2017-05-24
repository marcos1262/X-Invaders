import os

from OpenGL.GL import *

from PyQt5.QtCore import QUrl, Qt, QTimer
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent
from PyQt5.QtWidgets import *

from Nave import Nave
from XInvadersUi import Ui_MainWindow
from CameraOrtogonal import CameraOrtogonal


class XInvaders(QOpenGLWidget):
    """
    Representa o jogo.
    """

    def __init__(self, parent):
        QOpenGLWidget.__init__(self, parent)
        self.jogoLargura = 700
        self.jogoAltura = 700
        self.iniciaJogo = False
        self.nivel = 0

        self.camera = None

        self.jogador = None
        self.boss = None
        self.tiros = []
        self.asteroides = []
        self.estrelas = []
        self.inimigos = []

        self.inicializa_objetos()

        self.musicPlayer = QMediaPlayer()
        app.lastWindowClosed.connect(lambda: self.musicPlayer.stop() or self.timerMusicaFundo.stop())

        self.timerMusicaFundo = QTimer()
        self.timerMusicaFundo.timeout.connect(self.toca_musica_fundo)
        self.toca_musica_fundo()

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

        self.camera = CameraOrtogonal(self.jogoLargura, self.jogoAltura, True)

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

        for asteroide in self.asteroides:
            if not asteroide.visivel: self.asteroides.remove(asteroide)
        for estrela in self.estrelas:
            if not estrela.visivel: self.estrelas.remove(estrela)
        for inimigo in self.inimigos:
            if not inimigo.visivel: self.inimigos.remove(inimigo)
        for tiro in self.tiros:
            if not tiro.visivel: self.tiros.remove(tiro)

        for asteroide in self.asteroides:   asteroide.desenha()
        for estrela in self.estrelas:       estrela.desenha()
        for inimigo in self.inimigos:       inimigo.desenha()
        for tiro in self.tiros:             tiro.desenha()
        self.jogador.desenha()

        self.detecta_colisoes()

        self.mostra_pontuacao()

        # TODO mostrar minitutorial de como jogar (no nível 0)

        glFlush()

    # TODO ajustar opengl ao redimensionar janela
    # def resizeEvent(self, QResizeEvent):
    #     self.resize(QResizeEvent.size().width(), QResizeEvent.size().height())
    #
    #     self.jogoLargura = QResizeEvent.size().width()
    #     self.jogoAltura = QResizeEvent.size().height()
    #
    #     glViewport(0, 0, self.jogoLargura, self.jogoAltura)
    #
    #     if self.camera != None: self.camera.atualiza(self.jogoLargura, self.jogoAltura)

    def timerEvent(self, QTimerEvent):
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

    def toca_musica_fundo(self):
        dir_projeto = os.getcwd() + "/../"

        # TODO Separar controle de áudio em classe separada

        if self.iniciaJogo:
            arquivo = "sounds/fundo_jogo.mp3"
            tempo = 72000
        else:
            arquivo = "sounds/fundo_menu.mp3"
            tempo = 163000

        url = QUrl().fromLocalFile(dir_projeto + arquivo)
        media = QMediaContent(url)

        self.musicPlayer.setMedia(media)
        self.musicPlayer.play()

        self.timerMusicaFundo.start(tempo)

    def inicializa_objetos(self):
        self.jogador = Nave(55, 70, self, 0, self.py(-25), Nave.Tipos.JOGADOR)
        # TODO inicializar objetos

    def detecta_colisoes(self):
        # TODO Verificar colisões, remover da lista de objetos, contabilizar pontuação
        pass

    def mostra_pontuacao(self):
        # TODO Mostrar pontuação
        pass

    def px(self, porcentagem):
        """
        Retorna valor de uma posição no eixo X da tela baseado em uma porcentagem.
        :param porcentagem: porcentagem da tela que se deseja saber o valor.
        :return: valor da posição no eixo X da tela
        """
        return self.jogoLargura * porcentagem / 100

    def py(self, porcentagem):
        """
        Retorna valor de uma posição no eixo X da tela baseado em uma porcentagem.
        :param porcentagem: porcentagem da tela que se deseja saber o valor.
        :return: valor da posição no eixo X da tela
        """
        return self.jogoAltura * porcentagem / 100


app = None
if __name__ == '__main__':
    import sys

    app = QApplication(sys.argv)
    MainWindow = QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow, XInvaders)
    MainWindow.show()
    sys.exit(app.exec_())

import os

from OpenGL.GL import *
#from PIL.Image import Image

from PyQt5.QtCore import QUrl, Qt, QTimer
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent
from PyQt5.QtWidgets import *
from random import *

from Nave import NaveJogador, NaveCapanga
from XInvadersUi import Ui_MainWindow
from CameraOrtogonal import CameraOrtogonal

from Trajetoria import TrajetoriaLinear


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

        self.texturaJogador = None
        self.texturaCapanga1 = None
        self.texturaCapanga2 = None

        self.jogador = None
        self.boss = None
        self.tiros = []
        self.asteroides = []
        self.estrelas = []
        self.inimigos = []

        self.score = 0
        self.melhorPontuacao=0

        self.jogador = NaveJogador(self, 55, 70, 0, self.py(-25))

        self.musicPlayer = QMediaPlayer()
        app.lastWindowClosed.connect(lambda: self.musicPlayer.stop() or self.timerMusicaFundo.stop())

        self.spawner = QTimer()
        self.spawner.timeout.connect(self.cria_objetos)
        self.cria_objetos()

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

        self.remove_invisiveis()

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
        # if event.key() == Qt.Key_Space:  self.jogador.atirando = True

    def keyReleaseEvent(self, event):
        if event.key() == Qt.Key_Left:  self.jogador.esquerda = False
        if event.key() == Qt.Key_Right: self.jogador.direita = False
        if event.key() == Qt.Key_Up:    self.jogador.cima = False
        if event.key() == Qt.Key_Down:  self.jogador.baixo = False
        # if event.key() == Qt.Key_Space:  self.jogador.atirando = False

    def toca_musica_fundo(self):
        dir_projeto = os.getcwd() + "/../"

        # TODO Separar controle de áudio em classe separada

        if self.iniciaJogo:
            arquivo = "sounds/fundo_jogo.mp3"
            tempo = 208800
        else:
            arquivo = "sounds/fundo_menu.mp3"
            tempo = 67200

        url = QUrl().fromLocalFile(dir_projeto + arquivo)
        media = QMediaContent(url)

        self.musicPlayer.setMedia(media)
        self.musicPlayer.play()

        self.timerMusicaFundo.start(tempo)

    def cria_objetos(self):
        if randint(0,1)*self.iniciaJogo:
            x_inicial = randint(self.px(-50) + 55, self.px(50) - 55)
            self.inimigos.append(
                NaveCapanga(self, 55, 72, x_inicial, self.py(55),
                            TrajetoriaLinear(randint(-1, 1), self.py(55), x_inicial, True)
                            )
            )
        self.spawner.start(randint(0, 3000-self.nivel*10))

    def encerrar_partida(self):
        for inimigo in self.inimigos:
            inimigo.visivel = False
        for tiro in self.tiros:
            tiro.visivel = False
        self.jogador = NaveJogador(self, 55, 70, 0, self.py(-25))
        self.iniciaJogo = False
        if self.score > self.melhorPontuacao:
            self.melhorPontuacao=self.score

        ui.labelPontos.setText("")
        ui.ultima.setText("Melhor pontuação: " + str(self.melhorPontuacao))
        ui.ultima.setText("Última pontuação: " + str(self.score))

        self.score, self.nivel = 0, 0
        self.jogador.visivel = True
        ui.painel_menu.show()

    def detecta_colisoes(self):
        for i in self.inimigos:
            if self.jogador.colidiu(i):
                self.jogador.visivel = False
                i.visivel = False
                self.encerrar_partida()
        for t in self.tiros:
            if str(type(t.nave)) == "<class 'Nave.NaveJogador'>":
                for i in self.inimigos:
                    if i.colidiu(t):
                        if i.hp - 25 == 0:
                            i.visivel = False
                        i.hp -= 25
                        self.score += 25
                        if self.score-self.nivel*500 == 500:
                            self.nivel += 1;
                            self.jogador.hp = 100
                            print("Nivel: "+str(self.nivel))
                        t.visivel = False
            elif self.jogador.colidiu(t):
                self.jogador.hp -= 15+self.nivel*5
                if self.jogador.hp <= 0:
                    self.jogador.visivel = False
                    self.encerrar_partida()
                print("HP: "+str(self.jogador.hp))
                t.visivel = False

    def remove_invisiveis(self):
        for asteroide in self.asteroides:
            if not asteroide.visivel: self.asteroides.remove(asteroide)
        for estrela in self.estrelas:
            if not estrela.visivel: self.estrelas.remove(estrela)
        for inimigo in self.inimigos:
            if not inimigo.visivel: self.inimigos.remove(inimigo)
        for tiro in self.tiros:
            if not tiro.visivel: self.tiros.remove(tiro)

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

    # def carrega_textura(self, arquivo):
    #     img = Image.open(arquivo)
    #     img_data = numpy.array(list(img.getdata()), numpy.uint8)
    #
    #     texture = glGenTextures(1)
    #     glPixelStorei(GL_UNPACK_ALIGNMENT, 1)
    #     glBindTexture(GL_TEXTURE_2D, texture)
    #
    #     # Texture parameters are part of the texture object, so you need to
    #     # specify them only once for a given texture object.
    #     glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_CLAMP)
    #     glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_CLAMP)
    #     glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
    #     glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
    #     glTexImage2D(GL_TEXTURE_2D, 0, GL_RGB, img.size[0], img.size[1], 0, GL_RGB, GL_UNSIGNED_BYTE, img_data)
    #     return texture


app = None
ui = None
if __name__ == '__main__':
    import sys

    app = QApplication(sys.argv)
    MainWindow = QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow, XInvaders)
    MainWindow.show()
    sys.exit(app.exec_())

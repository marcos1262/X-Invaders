from OpenGL.GL import *
from PyQt5.QtWidgets import *
from PyQt5.QtMultimedia import QSound

from XInvadersUi import Ui_MainWindow
from Camera import Camera


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
        a = QSound("../sounds/SFX/Falcon Laser 1.wav",self)
        a.play()

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
        self.camera = Camera()

    def paintGL(self):
        """
        Desenha a cena
        :return: None
        """
        # Limpa tela
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        # TODO Desenha fundo estelar
        # Desenha triângulo (TESTE)
        glColor3f(1.0, 0.0, 0.0)

        glBegin(GL_TRIANGLES)
        glVertex3f(-100, 5, 0)
        glVertex3f(-110, -10, 0)
        glVertex3f(-90, -10, 0)
        glEnd()

        if not self.iniciaJogo:
            # Atualiza tela
            glFlush()
            return

        # TODO remover objetos fora da cena

        # TODO desenhar asteroides e estrelas

        # TODO desenhar jogador

        # TODO desenhar inimigos (de acordo com o nível)

        # TODO desenhar tiros

        # TODO detectar colisões

        # TODO mostrar minitutorial de como jogar (no nível 0)

        # Desenha triângulo (TESTE)
        glColor3f(1.0, 1.0, 0.0)

        glBegin(GL_TRIANGLES)
        glVertex3f(0, 50, 0)
        glVertex3f(-100, -100, 0)
        glVertex3f(100, -100, 0)
        glEnd()

        # Atualiza tela
        glFlush()


if __name__ == '__main__':
    import sys

    app = QApplication(sys.argv)
    MainWindow = QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow, XInvaders)
    MainWindow.show()
    sys.exit(app.exec_())

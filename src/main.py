from OpenGL.GL import *
from PyQt5.QtOpenGL import *
from PyQt5.QtWidgets import *

from camera import Camera
from ui.XInvadersUi import Ui_MainWindow


class XInvaders(QOpenGLWidget):
    def __init__(self, parent):
        QOpenGLWidget.__init__(self, parent)
        self.rodando = False
        self.camera = None

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
        if not self.rodando: return
        # Limpa tela
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        # Desenha triângulo
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

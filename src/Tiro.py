from OpenGL.GL import *
from PyQt5.QtCore import QObject

from Objeto import Objeto
from Trajetoria import Trajetoria


class Tiro(Objeto):
    """
    Representa um tiro de qualquer nave
    """

    def __init__(self, nave, largura, altura, x, y, trajetoria: Trajetoria):
        QObject.__init__(self, nave.jogo)
        self.jogo = nave.jogo
        self.nave = nave
        self.largura = largura
        self.altura = altura
        self.x = x
        self.y = y
        self.trajetoria = trajetoria

        self.velocidade = nave.velocidade+5
        self.visivel = True

    def desenha(self):
        # TODO colocar textura no tiro
        if str(type(self.nave)) == "<class 'Nave.NaveJogador'>":
            glColor4f(0.5, 1, 0.5, 1)
        else:
            glColor4f(1, 0.5, 0.5, 1)

        self.move()

        glBegin(GL_QUADS)
        glVertex2f(self.x + self.largura / 2, self.y + self.altura / 2)  # superior direito
        glVertex2f(self.x - self.largura / 2, self.y + self.altura / 2)  # superior esquerdo
        glVertex2f(self.x - self.largura / 2, self.y - self.altura / 2)  # inferior esquerdo
        glVertex2f(self.x + self.largura / 2, self.y - self.altura / 2)  # inferior direito
        glEnd()

        if self.x - self.largura / 2 > self.jogo.jogoLargura / 2 \
                or self.x + self.largura / 2 < -self.jogo.jogoLargura / 2 \
                or self.y - self.largura / 2 > self.jogo.jogoAltura / 2 \
                or self.y + self.largura / 2 < -self.jogo.jogoAltura / 2:
            self.visivel = False

    def move(self):
        if str(type(self.nave)) == "<class 'Nave.NaveJogador'>":
            self.x, self.y = self.trajetoria.proximo(self.velocidade)
        else:
            self.x, self.y = self.trajetoria.anterior(self.velocidade)

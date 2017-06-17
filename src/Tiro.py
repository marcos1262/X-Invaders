from OpenGL.GL import *
from PyQt5.QtCore import QObject

from Objeto import Objeto
from Trajetoria import Trajetoria


class Tiro(Objeto):
    """
    Representa um tiro de qualquer nave
    """

    def __init__(self, nave, largura, altura, x, y, textura, trajetoria: Trajetoria, angulo = 0):
        QObject.__init__(self, nave.jogo)
        self.jogo = nave.jogo
        self.nave = nave
        self.largura = largura
        self.altura = altura
        self.x = x
        self.y = y
        self.trajetoria = trajetoria
        self.textura = textura
        self.angulo = angulo

        self.velocidade = nave.velocidade+5
        self.visivel = True

    def desenha(self):
        if str(type(self.nave)) == "<class 'Nave.NaveJogador'>":
            glColor4f(0.5, 1, 0.5, 1)
        else:
            glColor4f(1, 0.5, 0.5, 1)

        glPushMatrix()
        self.move()

        glTranslate(self.x, self.y, 0)

        glRotate(-45*self.angulo, 0, 0, 1)

        glEnable(GL_TEXTURE_2D)
        glBindTexture(GL_TEXTURE_2D, self.textura)
        glBegin(GL_QUADS)
        glTexCoord2f(0.0, 1.0)
        glVertex2f(self.largura / 2, self.altura / 2)  # superior direito
        glTexCoord2f(0.0, 0.0)
        glVertex2f(- self.largura / 2, self.altura / 2)  # superior esquerdo
        glTexCoord2f(1.0, 0.0)
        glVertex2f(- self.largura / 2, - self.altura / 2)  # inferior esquerdo
        glTexCoord2f(1.0, 1.0)
        glVertex2f(self.largura / 2, - self.altura / 2)  # inferior direito
        glEnd()
        glDisable(GL_TEXTURE_2D)

        glPopMatrix()

        if self.y - self.largura / 1.5 > self.jogo.jogoAltura / 1.5 \
                or self.y + self.largura / 1.5 < -self.jogo.jogoAltura / 1.5:
            self.visivel = False

    def move(self):
        if str(type(self.nave)) == "<class 'Nave.NaveJogador'>":
            self.x, self.y = self.trajetoria.proximo(self.velocidade)
        else:
            self.x, self.y = self.trajetoria.anterior(self.velocidade)

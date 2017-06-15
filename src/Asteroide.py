from random import randint

from OpenGL.GL import *

from PyQt5.QtCore import QObject
from PyQt5.QtMultimedia import QSound

from Objeto import Objeto
from Trajetoria import *


class Asteroide(Objeto):
    """
    Representa um Asteroide.
    """


    def __init__(self, jogo, largura, altura, x, y, trajetoria: Trajetoria):
        QObject.__init__(self, jogo)
        self.jogo = jogo
        self.largura = largura
        self.altura = altura
        self.x = x
        self.y = y
        self.trajetoria = trajetoria

        self.visivel = True

        self.hp = 100
        self.velocidade = 20
        self.textura = self.jogo.texturaAsteroid

    def move(self):
        self.x, self.y = self.trajetoria.anterior(self.velocidade)

    def desenha(self):
        self.move()

        glBegin(GL_QUADS)

        # face superior
        color = [0.5, 0.5, 0.5, 1]
        glMaterialfv(GL_FRONT, GL_DIFFUSE, color)
        glVertex3f(self.x + self.largura / 2, self.y + self.altura / 2, self.largura / 2)  # inferior esquerdo
        glVertex3f(self.x - self.largura / 2, self.y + self.altura / 2, self.largura / 2)  # inferior esquerdo
        glVertex3f(self.x - self.largura / 2, self.y - self.altura / 2, self.largura / 2)  # inferior direito
        glVertex3f(self.x + self.largura / 2, self.y - self.altura / 2, self.largura / 2)  # inferior direito

        # face inferior
        color = [0.2, 0.2, 0.2, 1]
        glMaterialfv(GL_FRONT, GL_DIFFUSE, color)
        glVertex3f(self.x + self.largura / 2, self.y + self.altura / 2, -self.largura / 2)  # inferior esquerdo
        glVertex3f(self.x - self.largura / 2, self.y + self.altura / 2, -self.largura / 2)  # inferior esquerdo
        glVertex3f(self.x - self.largura / 2, self.y - self.altura / 2, -self.largura / 2)  # inferior direito
        glVertex3f(self.x + self.largura / 2, self.y - self.altura / 2, -self.largura / 2)  # inferior direito

        # face traseira
        color = [0.3, 0.3, 0.3, 1]
        glMaterialfv(GL_FRONT, GL_DIFFUSE, color)
        glVertex3f(self.x + self.largura / 2, self.y + self.altura / 2, -self.largura / 2)  # inferior esquerdo
        glVertex3f(self.x - self.largura / 2, self.y + self.altura / 2, -self.largura / 2)  # inferior esquerdo
        glVertex3f(self.x - self.largura / 2, self.y + self.altura / 2, self.largura / 2)  # inferior esquerdo
        glVertex3f(self.x + self.largura / 2, self.y + self.altura / 2, self.largura / 2)  # inferior esquerdo

        # face frontal
        color = [0.3, 0.3, 0.3, 1]
        glMaterialfv(GL_FRONT, GL_DIFFUSE, color)
        glVertex3f(self.x + self.largura / 2, self.y - self.altura / 2, self.largura / 2)  # inferior direito
        glVertex3f(self.x - self.largura / 2, self.y - self.altura / 2, self.largura / 2)  # inferior direito
        glVertex3f(self.x - self.largura / 2, self.y - self.altura / 2, -self.largura / 2)  # inferior direito
        glVertex3f(self.x + self.largura / 2, self.y - self.altura / 2, -self.largura / 2)  # inferior direito

        # face esquerda
        color = [0.1, 0.1, 0.1, 1]
        glMaterialfv(GL_FRONT, GL_DIFFUSE, color)
        glVertex3f(self.x - self.largura / 2, self.y + self.altura / 2, self.largura / 2)  # inferior esquerdo
        glVertex3f(self.x - self.largura / 2, self.y + self.altura / 2, -self.largura / 2)  # inferior esquerdo
        glVertex3f(self.x - self.largura / 2, self.y - self.altura / 2, -self.largura / 2)  # inferior direito
        glVertex3f(self.x - self.largura / 2, self.y - self.altura / 2, self.largura / 2)  # inferior direito

        # face direita
        color = [0.1, 0.1, 0.1, 1]
        glMaterialfv(GL_FRONT, GL_DIFFUSE, color)
        glVertex3f(self.x + self.largura / 2, self.y + self.altura / 2, self.largura / 2)  # inferior esquerdo
        glVertex3f(self.x + self.largura / 2, self.y - self.altura / 2, self.largura / 2)  # inferior direito
        glVertex3f(self.x + self.largura / 2, self.y - self.altura / 2, -self.largura / 2)  # inferior direito
        glVertex3f(self.x + self.largura / 2, self.y + self.altura / 2, -self.largura / 2)  # inferior esquerdo

        glEnd()

        # self.move()
        #
        # glEnable(GL_TEXTURE_2D)
        # glBindTexture(GL_TEXTURE_2D, self.textura)
        # glBegin(GL_QUADS)
        # glTexCoord2f(0.0, 1.0)
        # glVertex2f(self.x + self.largura / 2, self.y + self.altura / 2)  # superior direito
        # glTexCoord2f(0.0, 0.0)
        # glVertex2f(self.x - self.largura / 2, self.y + self.altura / 2)  # superior esquerdo
        # glTexCoord2f(1.0, 0.0)
        # glVertex2f(self.x - self.largura / 2, self.y - self.altura / 2)  # inferior esquerdo
        # glTexCoord2f(1.0, 1.0)
        # glVertex2f(self.x + self.largura / 2, self.y - self.altura / 2)  # inferior direito
        # glEnd()
        # glDisable(GL_TEXTURE_2D)

        if self.x - self.largura / 2 > self.jogo.jogoLargura \
                or self.x + self.largura / 2 < -self.jogo.jogoLargura \
                or self.y - self.largura / 2 > self.jogo.jogoAltura \
                or self.y + self.largura / 2 < -self.jogo.jogoAltura:
            self.visivel = False

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

    def define_textura(self):
        glColor4f(0.5, 0.5, 0.5, 1)
        return self.jogo.texturaAsteroid

    def move(self):
        self.x, self.y = self.trajetoria.anterior(self.velocidade)

    def desenha(self):
        textura = self.define_textura()
        # TODO colocar textura no asteroide

        self.move()

        glBegin(GL_QUADS)
        glVertex2f(self.x + self.largura / 2, self.y + self.altura / 2)  # superior direito
        glVertex2f(self.x - self.largura / 2, self.y + self.altura / 2)  # superior esquerdo
        glVertex2f(self.x - self.largura / 2, self.y - self.altura / 2)  # inferior esquerdo
        glVertex2f(self.x + self.largura / 2, self.y - self.altura / 2)  # inferior direito
        glEnd()

        if self.x - self.largura / 2 > self.jogo.jogoLargura \
                or self.x + self.largura / 2 < -self.jogo.jogoLargura \
                or self.y - self.largura / 2 > self.jogo.jogoAltura \
                or self.y + self.largura / 2 < -self.jogo.jogoAltura:
            self.visivel = False

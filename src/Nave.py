from builtins import print
from enum import Enum

from OpenGL.GL import *


class Nave:
    class Tipos(Enum):
        JOGADOR = 1
        BOSS = 2
        CAPANGA = 3

    def __init__(self, largura, altura, x=0, y=0, tipo=Tipos.CAPANGA):
        self.largura = largura
        self.altura = altura
        self.x = x
        self.y = y
        self.tipo = tipo

    def desenha(self):
        # TODO colocar textura
        if self.tipo == self.Tipos.JOGADOR:
            glColor4f(1, 1, 0, 1)
        elif self.tipo == self.Tipos.BOSS:
            glColor4f(1, 0, 0, 1)
        elif self.tipo == self.Tipos.CAPANGA:
            glColor4f(0, 0, 1, 1)
        else:
            glColor4f(1, 1, 1, 1)

        glBegin(GL_QUADS)
        glVertex2f(self.x + self.largura / 2, self.y + self.altura / 2)  # superior direito
        glVertex2f(self.x - self.largura / 2, self.y + self.altura / 2)  # superior esquerdo
        glVertex2f(self.x - self.largura / 2, self.y - self.altura / 2)  # inferior esquerdo
        glVertex2f(self.x + self.largura / 2, self.y - self.altura / 2)  # inferior direito
        glEnd()

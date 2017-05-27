from enum import Enum

from OpenGL.GL import *

from PyQt5.QtCore import QObject
from PyQt5.QtMultimedia import QSound

from Objeto import Objeto
from Tiro import Tiro
from Trajetoria import *


class Nave(Objeto):
    """
    Representa todo tipo de nave.
    """

    class Tipos(Enum):
        JOGADOR = 1
        BOSS = 2
        CAPANGA = 3

    def __init__(self, largura, altura, jogo, x, y, trajetoria : Trajetoria, tipo=Tipos.CAPANGA):
        QObject.__init__(self, jogo)
        self.largura = largura
        self.altura = altura
        self.x = x
        self.y = y
        self.trajetoria = trajetoria
        self.tipo = tipo
        self.jogo = jogo

        self.velocidade = 10
        self.hp = 100
        self.visivel = True

        self.esquerda = False
        self.direita = False
        self.cima = False
        self.baixo = False
        # self.atirando = False

        self.startTimer(150)
        self.tiro1 = True

    def desenha(self):
        # TODO colocar textura na nave
        if self.tipo == self.Tipos.JOGADOR:
            glColor4f(1, 1, 0, 1)
        elif self.tipo == self.Tipos.BOSS:
            glColor4f(1, 0, 0, 1)
        elif self.tipo == self.Tipos.CAPANGA:
            glColor4f(0, 0, 1, 1)
        else:
            glColor4f(1, 1, 1, 1)

        self.move()

        glBegin(GL_QUADS)
        glVertex2f(self.x + self.largura / 2, self.y + self.altura / 2)  # superior direito
        glVertex2f(self.x - self.largura / 2, self.y + self.altura / 2)  # superior esquerdo
        glVertex2f(self.x - self.largura / 2, self.y - self.altura / 2)  # inferior esquerdo
        glVertex2f(self.x + self.largura / 2, self.y - self.altura / 2)  # inferior direito
        glEnd()

    def move(self):
        if self.tipo == self.Tipos.JOGADOR:
            if self.esquerda and self.x > -self.jogo.jogoLargura/2 + self.largura / 2:
                self.x -= self.velocidade
            if self.direita and self.x < self.jogo.jogoLargura/2 - self.largura / 2:
                self.x += self.velocidade
            if self.cima and self.y < self.jogo.jogoAltura/2 - self.altura / 2:
                self.y += self.velocidade
            if self.baixo and self.y > -self.jogo.jogoAltura/2 + self.altura / 2:
                self.y -= self.velocidade
        else:
            self.x, self.y = self.trajetoria.anterior(self.velocidade)
            # pass

    def atira(self):
        if self.tipo == self.Tipos.JOGADOR:
            if self.tiro1:
                tiro = Tiro(3, 25,
                             self.x - self.largura / 2,
                             self.y + self.altura / 2 + 15,
                             self.jogo,
                             1,
                             TrajetoriaLinear(0, (self.y + self.altura / 2 + 15), self.x - self.largura / 2, True))
                self.jogo.tiros.append(tiro)
                self.tiro1 = False
            else:
                tiro = Tiro(3, 25,
                             self.x + self.largura / 2,
                             self.y + self.altura / 2 + 15,
                             self.jogo,
                             1,
                             TrajetoriaLinear(0, (self.y + self.altura / 2 + 15), self.x + self.largura / 2, True))
                self.jogo.tiros.append(tiro)
                self.tiro1 = True
        else:
            if self.tiro1:
                tiro = Tiro(3, 25,
                             self.x - self.largura / 2,
                             self.y + self.altura / 2 + 15,
                             self.jogo,
                             0,
                             TrajetoriaLinear(0, (self.y - self.altura / 2 - 15), self.x - self.largura / 2, True))
                self.jogo.tiros.append(tiro)
                self.tiro1 = False
            else:
                tiro = Tiro(3, 25,
                             self.x + self.largura / 2,
                             self.y + self.altura / 2 + 15,
                             self.jogo,
                             0,
                             TrajetoriaLinear(0, (self.y - self.altura / 2 - 15), self.x + self.largura / 2, True))
                self.jogo.tiros.append(tiro)
                self.tiro1 = True
        # QSound("../sounds/SFX/TIE Laser 1A.wav", self).play()

    def timerEvent(self, QTimerEvent):
        if self.jogo.iniciaJogo*self.visivel:
            # if self.tipo == self.Tipos.JOGADOR:
            #    if self.atirando: self.atira()
            # else:
            #    self.atira()
            self.atira()
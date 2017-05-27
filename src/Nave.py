from random import randint

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

    visivel = True
    tiro1 = True

    def desenha(self):
        textura = self.define_textura()
        # TODO colocar textura na nave

        self.move()

        glBegin(GL_QUADS)
        glVertex2f(self.x + self.largura / 2, self.y + self.altura / 2)  # superior direito
        glVertex2f(self.x - self.largura / 2, self.y + self.altura / 2)  # superior esquerdo
        glVertex2f(self.x - self.largura / 2, self.y - self.altura / 2)  # inferior esquerdo
        glVertex2f(self.x + self.largura / 2, self.y - self.altura / 2)  # inferior direito
        glEnd()

    def timerEvent(self, QTimerEvent):
        if self.jogo.iniciaJogo * self.visivel: self.atira()

    def atira(self):
        pass

    def define_textura(self):
        pass


class NaveJogador(Nave):

    def __init__(self, jogo, largura, altura, x, y):
        QObject.__init__(self, jogo)
        self.jogo = jogo
        self.largura = largura
        self.altura = altura
        self.x = x
        self.y = y

        self.velocidade = 10
        self.hp = 100
        self.visivel = True

        self.esquerda = False
        self.direita = False
        self.cima = False
        self.baixo = False

        self.startTimer(150)

    def define_textura(self):
        glColor4f(1, 1, 0, 1)
        return self.jogo.texturaJogador

    def move(self):
        if self.esquerda and self.x > -self.jogo.jogoLargura / 2 + self.largura / 2:
            self.x -= self.velocidade
        if self.direita and self.x < self.jogo.jogoLargura / 2 - self.largura / 2:
            self.x += self.velocidade
        if self.cima and self.y < self.jogo.jogoAltura / 2 - self.altura / 2:
            self.y += self.velocidade
        if self.baixo and self.y > -self.jogo.jogoAltura / 2 + self.altura / 2:
            self.y -= self.velocidade

    def atira(self):
        if not self.tiro1:
            x = self.x - self.largura / 2
            self.tiro1 = True
        else:
            x = self.x + self.largura / 2
            self.tiro1 = False
        y = self.y + self.altura / 2 + 15
        trajetoria = TrajetoriaLinear(0, y, x, True)

        tiro = Tiro(self.jogo, self, 3, 25, x, y, trajetoria)
        self.jogo.tiros.append(tiro)
        # QSound("../sounds/SFX/TIE Laser 1A.wav", self).play()


class NaveCapanga(Nave):

    def __init__(self, jogo, largura, altura, x, y, trajetoria: Trajetoria):
        QObject.__init__(self, jogo)
        self.jogo = jogo
        self.largura = largura
        self.altura = altura
        self.x = x
        self.y = y
        self.trajetoria = trajetoria

        self.velocidade = 5

        self.startTimer(400)

    def define_textura(self):
        glColor4f(0, 0, 1, 1)
        if randint(0, 1):
            return self.jogo.texturaCapanga1
        else:
            return self.jogo.texturaCapanga2

    def move(self):
        self.x, self.y = self.trajetoria.anterior(self.velocidade)

    def atira(self):
        largura = 3
        altura = 25
        if not self.tiro1:
            x = self.x - self.largura / 2
            self.tiro1 = True
        else:
            x = self.x + self.largura / 2
            self.tiro1 = False
        y = self.y - self.altura / 2 + 15
        trajetoria = TrajetoriaLinear(0, y, x, True)

        tiro = Tiro(self.jogo, self, largura, altura, x, y, trajetoria)
        self.jogo.tiros.append(tiro)
        # QSound("../sounds/SFX/TIE Laser 1A.wav", self).play()

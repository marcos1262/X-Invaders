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
    hp = 100

    def desenha(self):
        self.move()

        glEnable(GL_TEXTURE_2D)
        glBindTexture(GL_TEXTURE_2D, self.textura)
        glBegin(GL_QUADS)
        glTexCoord2f(0.0, 1.0)
        glVertex2f(self.x + self.largura / 2, self.y + self.altura / 2)  # superior direito
        glTexCoord2f(0.0, 0.0)
        glVertex2f(self.x - self.largura / 2, self.y + self.altura / 2)  # superior esquerdo
        glTexCoord2f(1.0, 0.0)
        glVertex2f(self.x - self.largura / 2, self.y - self.altura / 2)  # inferior esquerdo
        glTexCoord2f(1.0, 1.0)
        glVertex2f(self.x + self.largura / 2, self.y - self.altura / 2)  # inferior direito
        glEnd()
        glDisable(GL_TEXTURE_2D)

        if self.x - self.largura / 2 > self.jogo.jogoLargura \
                or self.x + self.largura / 2 < -self.jogo.jogoLargura \
                or self.y - self.largura / 2 > self.jogo.jogoAltura \
                or self.y + self.largura / 2 < -self.jogo.jogoAltura:
            self.visivel = False

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
        self.textura = self.jogo.texturaJogador

        self.esquerda = False
        self.direita = False
        self.cima = False
        self.baixo = False

        self.startTimer(150)

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

        tiro = Tiro(self, 15, 50, x, y, self.jogo.texturaTiro1, trajetoria)
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

        self.velocidade = 5 + self.jogo.nivel
        if randint(0, 1):
            self.textura = self.jogo.texturaCapanga1
        else:
            self.textura = self.jogo.texturaCapanga2

        self.startTimer(400 - self.jogo.nivel * 50)

    def move(self):
        self.x, self.y = self.trajetoria.anterior(self.velocidade)

    def atira(self):
        if not self.tiro1:
            x = self.x - self.largura / 2
            self.tiro1 = True
        else:
            x = self.x + self.largura / 2
            self.tiro1 = False
        y = self.y - self.altura / 2 - 15
        trajetoria = TrajetoriaLinear(0, y, x, True)

        tiro = Tiro(self, 15, 40, x, y, self.jogo.texturaTiro2,  trajetoria)
        self.jogo.tiros.append(tiro)
        # QSound("../sounds/SFX/TIE Laser 1A.wav", self).play()


class NaveBoss(Nave):
    def __init__(self, jogo, largura, altura, x, y, trajetoria: Trajetoria):
        QObject.__init__(self, jogo)
        self.jogo = jogo
        self.largura = largura
        self.altura = altura
        self.x = x
        self.y = y
        self.trajetoria = trajetoria

        self.velocidade = 2
        self.textura = self.jogo.texturaBoss

        self.startTimer(300 - self.jogo.nivel * 50)

    def move(self):
        self.x, self.y = self.trajetoria.anterior(self.velocidade)

    def atira(self):
        if not self.tiro1:
            x = self.x - self.largura / 2
            self.tiro1 = True
        else:
            x = self.x + self.largura / 2
            self.tiro1 = False
        y = self.y - self.altura / 2 - 15
        trajetoria = TrajetoriaLinear(0, y, x, True)

        tiro = Tiro(self, 3, 25, x, y, self.jogo.texturaTiro3,  trajetoria)
        self.jogo.tiros.append(tiro)
        # QSound("../sounds/SFX/TIE Laser 1A.wav", self).play()

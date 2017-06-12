from random import randint
import math

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

        glBegin(GL_QUADS)

        # face superior
        color = [1, 1, 1, 1]
        glMaterialfv(GL_FRONT, GL_DIFFUSE, color)
        glVertex3f(self.x + self.largura / 2, self.y + self.altura / 2, 15)  # inferior esquerdo
        glVertex3f(self.x - self.largura / 2, self.y + self.altura / 2, 15)  # inferior esquerdo
        glVertex3f(self.x - self.largura / 2, self.y - self.altura / 2, 15)  # inferior direito
        glVertex3f(self.x + self.largura / 2, self.y - self.altura / 2, 15)  # inferior direito

        # face inferior
        color = [0.5, 0.5, 0.5, 0.5]
        glMaterialfv(GL_FRONT, GL_DIFFUSE, color)
        glVertex3f(self.x + self.largura / 2, self.y + self.altura / 2, -15)  # inferior esquerdo
        glVertex3f(self.x - self.largura / 2, self.y + self.altura / 2, -15)  # inferior esquerdo
        glVertex3f(self.x - self.largura / 2, self.y - self.altura / 2, -15)  # inferior direito
        glVertex3f(self.x + self.largura / 2, self.y - self.altura / 2, -15)  # inferior direito

        # face traseira
        color = [1, 0, 1, 1]
        glMaterialfv(GL_FRONT, GL_DIFFUSE, color)

        glVertex3f(self.x + self.largura / 2, self.y + self.altura / 2, -15)  # inferior esquerdo

        glVertex3f(self.x - self.largura / 2, self.y + self.altura / 2, -15)  # inferior esquerdo
        glVertex3f(self.x - self.largura / 2, self.y + self.altura / 2, 15)  # inferior esquerdo
        glVertex3f(self.x + self.largura / 2, self.y + self.altura / 2, 15)  # inferior esquerdo


        # face frontal
        color = [1, 0, 0, 1]
        glMaterialfv(GL_FRONT, GL_DIFFUSE, color)
        glVertex3f(self.x + self.largura / 2, self.y - self.altura / 2, 15)  # inferior direito
        glVertex3f(self.x - self.largura / 2, self.y - self.altura / 2, 15)  # inferior direito
        glVertex3f(self.x - self.largura / 2, self.y - self.altura / 2, -15)  # inferior direito
        glVertex3f(self.x + self.largura / 2, self.y - self.altura / 2, -15)  # inferior direito

        # face esquerda
        color = [0, 1, 0, 1]
        glMaterialfv(GL_FRONT, GL_DIFFUSE, color)
        glVertex3f(self.x - self.largura / 2, self.y + self.altura / 2, 15)  # inferior esquerdo
        glVertex3f(self.x - self.largura / 2, self.y + self.altura / 2, -15)  # inferior esquerdo
        glVertex3f(self.x - self.largura / 2, self.y - self.altura / 2, -15)  # inferior direito
        glVertex3f(self.x - self.largura / 2, self.y - self.altura / 2, 15)  # inferior direito


        # face direita
        color = [0, 0, 1, 1]
        glMaterialfv(GL_FRONT, GL_DIFFUSE, color)
        glVertex3f(self.x + self.largura / 2, self.y + self.altura / 2, 15)  # inferior esquerdo
        glVertex3f(self.x + self.largura / 2, self.y - self.altura / 2, 15)  # inferior direito
        glVertex3f(self.x + self.largura / 2, self.y - self.altura / 2, -15)  # inferior direito
        glVertex3f(self.x + self.largura / 2, self.y + self.altura / 2, -15)  # inferior esquerdo

        glEnd()

        if self.x - self.largura / 2 > self.jogo.jogoLargura \
                or self.x + self.largura / 2 < -self.jogo.jogoLargura \
                or self.y - self.largura / 2 > self.jogo.jogoAltura \
                or self.y + self.largura / 2 < -self.jogo.jogoAltura:
            self.visivel = False

    def timerEvent(self, QTimerEvent):
        if self.jogo.iniciaJogo * self.visivel: self.atira()

    def atira(self):
        pass


class NaveJogador(Nave):
    def __init__(self, jogo, largura, altura, x, y):
        QObject.__init__(self, jogo)
        self.jogo = jogo
        self.largura = largura
        self.altura = altura
        self.x = x
        self.y = y
        self.z = 0

        self.velocidade = 10
        self.textura = self.jogo.texturaJogador

        self.esquerda = False
        self.direita = False
        self.cima = False
        self.baixo = False

        self.taxaTiro = 150

        self.startTimer(self.taxaTiro)

    def desenha(self):

        glPushMatrix()
        self.move()

        glBegin(GL_TRIANGLES)

        color = [0.8, 0.8, 0.8, 1.0]
        glMaterialfv(GL_FRONT, GL_DIFFUSE, color)
        glVertex3f(self.x, self.y, self.z + 15)  # superior
        glVertex3f(self.x - self.largura / 2, self.y - self.altura * 0.2, -15)  # inferior esquerdo
        glVertex3f(self.x + self.largura / 2, self.y - self.altura * 0.2, -15)  # inferior direito

        color = [0, 1, 0, 1]
        glMaterialfv(GL_FRONT, GL_DIFFUSE, color)
        glVertex3f(self.x, self.y + self.altura * 0.8, -15)  # bico
        glVertex3f(self.x - self.largura / 2, self.y - self.altura * 0.2, -15)  # inferior esquerdo
        glVertex3f(self.x + self.largura / 2, self.y - self.altura * 0.2, -15)  # inferior direito

        color = [0, 0, 1, 1]
        glMaterialfv(GL_FRONT, GL_DIFFUSE, color)
        glVertex3f(self.x, self.y, 15)  # superior
        glVertex3f(self.x, self.y + self.altura * 0.8, -15)  # bico
        glVertex3f(self.x - self.largura / 2, self.y - self.altura * 0.2, -15)  # inferior esquerdo

        color = [1, 0, 0, 1]
        glMaterialfv(GL_FRONT, GL_DIFFUSE, color)
        glVertex3f(self.x, self.y, 15)  # superior
        glVertex3f(self.x + self.largura / 2, self.y - self.altura * 0.2, -15)  # inferior direito
        glVertex3f(self.x, self.y + self.altura * 0.8, self.z -15)  # bico

        glEnd()
        glPopMatrix()

        if self.x - self.largura / 2 > self.jogo.jogoLargura \
                or self.x + self.largura / 2 < -self.jogo.jogoLargura \
                or self.y - self.largura / 2 > self.jogo.jogoAltura \
                or self.y + self.largura / 2 < -self.jogo.jogoAltura:
            self.visivel = False

    def move(self):
        if self.esquerda and self.x > -self.jogo.jogoLargura / 2 + self.largura / 2:
            self.x -= self.velocidade * math.sqrt(2)/2
            glRotatef(-45, 0, 1, 0)
            glTranslate(0, 0, self.x * math.sqrt(2)/2)
        elif self.direita and self.x < self.jogo.jogoLargura / 2 - self.largura / 2:
            self.x += self.velocidade * math.sqrt(2)/2
            glRotatef(45, 0, 1, 0)
            glTranslate(0, 0, self.x * math.sqrt(2)/2)
        if self.cima and self.y < self.jogo.jogoAltura / 2 - self.altura / 2:
            self.y += self.velocidade
        elif self.baixo and self.y > -self.jogo.jogoAltura / 2 + self.altura / 2:
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

        tiro = Tiro(self, 12, 40, x, y, self.jogo.texturaTiro1, trajetoria)
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

        self.startTimer(400 - self.jogo.nivel * 5)

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

        tiro = Tiro(self, 12, 40, x, y, self.jogo.texturaTiro2, trajetoria)
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

        self.startTimer(300 - self.jogo.nivel * 10)

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

        tiro = Tiro(self, 15, 50, x, y, self.jogo.texturaTiro3, trajetoria)
        self.jogo.tiros.append(tiro)

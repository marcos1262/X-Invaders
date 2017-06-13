from random import randint
import math

from OpenGL.GL import *

from PyQt5.QtCore import QObject
from PyQt5.QtMultimedia import QSound

from Objeto import Objeto
from Tiro import Tiro
from Trajetoria import *
from math import *

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

    def anguloJogador(self):
        x = atan2(self.x-self.jogo.jogador.x, self.y-self.jogo.jogador.y )
        if -1<x<1 : return x
        else: return 0

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
        self.r = 0
        self.alfa = 0
        self.beta = 0
        self.gama = 0

        self.velocidade = 10
        self.textura = self.jogo.texturaJogador

        self.esquerda = False
        self.direita = False
        self.cima = False
        self.baixo = False

        self.taxaTiro = 150

        self.startTimer(self.taxaTiro)

    def desenha(self):

        # v1 = [self.x, self.y, 15]
        # v2 = [self.x - self.largura / 2, self.y - self.altura * 0.2, -15]
        # v3 = [self.x + self.largura / 2, self.y - self.altura * 0.2, -15]
        # v4 = [self.x, self.y + self.altura * 0.8, -15]

        # glPushMatrix()

        self.move()


        # glBegin(GL_TRIANGLES)
        #
        # color = [0.8, 0.8, 0.8, 1.0]
        # glMaterialfv(GL_FRONT, GL_DIFFUSE, color)
        # glVertex3f(v1[0],v1[1],v1[2])  # superior
        # glVertex3f(v2[0],v2[1],v2[2])  # inferior esquerdo
        # glVertex3f(v3[0],v3[1],v3[2])  # inferior direito
        #
        # color = [0, 1, 0, 1]
        # glMaterialfv(GL_FRONT, GL_DIFFUSE, color)
        # glVertex3f(v4[0],v4[1],v4[2])  # bico
        # glVertex3f(v2[0],v2[1],v2[2])  # inferior esquerdo
        # glVertex3f(v3[0],v3[1],v3[2])  # inferior direito
        #
        # color = [0, 0, 1, 1]
        # glMaterialfv(GL_FRONT, GL_DIFFUSE, color)
        # glVertex3f(v1[0],v1[1],v1[2])  # superior
        # glVertex3f(v4[0],v4[1],v4[2])  # bico
        # glVertex3f(v2[0],v2[1],v2[2])  # inferior esquerdo
        #
        # color = [1, 0, 0, 1]
        # glMaterialfv(GL_FRONT, GL_DIFFUSE, color)
        # glVertex3f(v1[0],v1[1],v1[2])  # superior
        # glVertex3f(v3[0],v3[1],v3[2])  # inferior direito
        # glVertex3f(v4[0],v4[1],v4[2])  # bico
        #
        # glEnd()
        # glPopMatrix()

        if self.esquerda:
            glBegin(GL_TRIANGLES)

            glVertex3f(self.x - (30 * math.sqrt(2) / 2), self.y, 30 - (30 * math.sqrt(2) / 2))  # superior
            glVertex3f(self.x - self.largura / 2 + (30 * math.sqrt(2) / 2),
                       self.y - self.altura * 0.2,
                       -30 - self.largura / 2 + (30 * math.sqrt(2) / 2))  # inferior esquerdo
            glVertex3f(self.x + self.largura / 2 + (30 * math.sqrt(2) / 2),
                       self.y - self.altura * 0.2, -30 + self.largura / 2 + (30 * math.sqrt(2) / 2))  # inferior direito

            color = [0, 1, 0, 1]
            glMaterialfv(GL_FRONT, GL_DIFFUSE, color)
            glVertex3f(self.x, self.y + self.altura * 0.8, -30)  # bico
            glVertex3f(self.x - self.largura / 2 + (30 * math.sqrt(2) / 2), self.y - self.altura * 0.2,
                       -30 - self.largura / 2 + (30 * math.sqrt(2) / 2))  # inferior esquerdo
            glVertex3f(self.x + self.largura / 2 + (30 * math.sqrt(2) / 2),
                       self.y - self.altura * 0.2, -30 + self.largura / 2 + (30 * math.sqrt(2) / 2))  # inferior direito

            color = [0, 0, 1, 1]
            glMaterialfv(GL_FRONT, GL_DIFFUSE, color)
            glVertex3f(self.x - (30 * math.sqrt(2) / 2), self.y, 30 - (30 * math.sqrt(2) / 2))  # superior
            glVertex3f(self.x - self.largura / 2 + (30 * math.sqrt(2) / 2), self.y - self.altura * 0.2,
                       -30 - self.largura / 2 + (30 * math.sqrt(2) / 2))  # inferior esquerdo
            glVertex3f(self.x, self.y + self.altura * 0.8, -30)  # bico

            color = [1, 0, 0, 1]
            glMaterialfv(GL_FRONT, GL_DIFFUSE, color)
            glVertex3f(self.x - (30 * math.sqrt(2) / 2), self.y, 30 - (30 * math.sqrt(2) / 2))  # superior
            glVertex3f(self.x + self.largura / 2 + (30 * math.sqrt(2) / 2),
                       self.y - self.altura * 0.2, -30 + self.largura / 2 + (30 * math.sqrt(2) / 2))  # inferior direito
            glVertex3f(self.x, self.y + self.altura * 0.8, -30)  # bico

            glEnd()

        elif self.direita:

            glBegin(GL_TRIANGLES)

            glVertex3f(self.x + (30 * math.sqrt(2) / 2), self.y, 30 - (30 * math.sqrt(2) / 2))  # superior
            glVertex3f(self.x - self.largura / 2 - (30 * math.sqrt(2) / 2),
                       self.y - self.altura * 0.2,
                       -30 + self.largura / 2 + (30 * math.sqrt(2) / 2))  # inferior esquerdo
            glVertex3f(self.x + self.largura / 2 - (30 * math.sqrt(2) / 2),
                       self.y - self.altura * 0.2, -30 - self.largura / 2 + (30 * math.sqrt(2) / 2))  # inferior direito

            color = [0, 1, 0, 1]
            glMaterialfv(GL_FRONT, GL_DIFFUSE, color)
            glVertex3f(self.x, self.y + self.altura * 0.8, -30)  # bico
            glVertex3f(self.x - self.largura / 2 - (30 * math.sqrt(2) / 2), self.y - self.altura * 0.2,
                       -30 + self.largura / 2 + (30 * math.sqrt(2) / 2))  # inferior esquerdo
            glVertex3f(self.x + self.largura / 2 - (30 * math.sqrt(2) / 2),
                       self.y - self.altura * 0.2, -30 - self.largura / 2 + (30 * math.sqrt(2) / 2))  # inferior direito

            color = [0, 0, 1, 1]
            glMaterialfv(GL_FRONT, GL_DIFFUSE, color)
            glVertex3f(self.x + (30 * math.sqrt(2) / 2), self.y, 30 - (30 * math.sqrt(2) / 2))  # superior
            glVertex3f(self.x - self.largura / 2 - (30 * math.sqrt(2) / 2), self.y - self.altura * 0.2,
                       -30 + self.largura / 2 + (30 * math.sqrt(2) / 2))  # inferior esquerdo
            glVertex3f(self.x, self.y + self.altura * 0.8, -30)  # bico

            color = [1, 0, 0, 1]
            glMaterialfv(GL_FRONT, GL_DIFFUSE, color)
            glVertex3f(self.x + (30 * math.sqrt(2) / 2), self.y, 30 - (30 * math.sqrt(2) / 2))  # superior
            glVertex3f(self.x + self.largura / 2 - (30 * math.sqrt(2) / 2),
                       self.y - self.altura * 0.2, -30 - self.largura / 2 + (30 * math.sqrt(2) / 2))  # inferior direito
            glVertex3f(self.x, self.y + self.altura * 0.8, -30)  # bico

            glEnd()

        else:
            glBegin(GL_TRIANGLES)

            glVertex3f(self.x, self.y, 30)  # superior
            glVertex3f(self.x - self.largura / 2, self.y - self.altura * 0.2, -30)  # inferior esquerdo
            glVertex3f(self.x + self.largura / 2, self.y - self.altura * 0.2, -30)  # inferior direito

            color = [0, 1, 0, 1]
            glMaterialfv(GL_FRONT, GL_DIFFUSE, color)
            glVertex3f(self.x, self.y + self.altura * 0.8, -30)  # bico
            glVertex3f(self.x - self.largura / 2, self.y - self.altura * 0.2, -30)  # inferior esquerdo
            glVertex3f(self.x + self.largura / 2, self.y - self.altura * 0.2, -30)  # inferior direito

            color = [0, 0, 1, 1]
            glMaterialfv(GL_FRONT, GL_DIFFUSE, color)
            glVertex3f(self.x, self.y, 30)  # superior
            glVertex3f(self.x - self.largura / 2, self.y - self.altura * 0.2, -30)  # inferior esquerdo
            glVertex3f(self.x, self.y + self.altura * 0.8, -30)  # bico

            color = [1, 0, 0, 1]
            glMaterialfv(GL_FRONT, GL_DIFFUSE, color)
            glVertex3f(self.x, self.y, 30)  # superior
            glVertex3f(self.x + self.largura / 2, self.y - self.altura * 0.2, -30)  # inferior direito
            glVertex3f(self.x, self.y + self.altura * 0.8, -30)  # bico

            glEnd()

        if self.x - self.largura / 2 > self.jogo.jogoLargura \
                or self.x + self.largura / 2 < -self.jogo.jogoLargura \
                or self.y - self.largura / 2 > self.jogo.jogoAltura \
                or self.y + self.largura / 2 < -self.jogo.jogoAltura:
            self.visivel = False

    def move(self):
        if self.esquerda and self.x > -self.jogo.jogoLargura / 2 + self.largura / 2:
            self.x -= self.velocidade
            self.r = 45
            # * math.sqrt(2)/2
            # glRotatef(-45, 0, 1, 0)
            # glTranslate(0, 0, self.x * -math.sqrt(2)/2)
        elif self.direita and self.x < self.jogo.jogoLargura / 2 - self.largura / 2:
            self.x += self.velocidade
            self.r = -45
            # * math.sqrt(2)/2
            # glRotatef(45, 0, 1, 0)
            # glTranslate(0, 0, self.x * math.sqrt(2)/2)
        elif not self.direita and not self.esquerda: self.r = 0
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

        trajetoria = TrajetoriaLinear(self.anguloJogador(), y, x, True)

        tiro = Tiro(self, 15, 50, x, y, self.jogo.texturaTiro3, trajetoria)
        self.jogo.tiros.append(tiro)

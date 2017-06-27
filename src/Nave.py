from random import randint

from OpenGL.GL import *
from OpenGL.GL.exceptional import glEnd

from PyQt5.QtCore import QObject

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
        color = [0.65, 0.65, 0.65, 1]
        glMaterialfv(GL_FRONT, GL_DIFFUSE, color)
        glVertex3f(self.x + self.largura / 2, self.y + self.altura / 2, 15)  # inferior esquerdo
        glVertex3f(self.x - self.largura / 2, self.y + self.altura / 2, 15)  # inferior esquerdo
        glVertex3f(self.x - self.largura / 2, self.y - self.altura / 2, 15)  # inferior direito
        glVertex3f(self.x + self.largura / 2, self.y - self.altura / 2, 15)  # inferior direito

        # face inferior
        glMaterialfv(GL_FRONT, GL_DIFFUSE, color)
        glVertex3f(self.x + self.largura / 2, self.y + self.altura / 2, -15)  # inferior esquerdo
        glVertex3f(self.x - self.largura / 2, self.y + self.altura / 2, -15)  # inferior esquerdo
        glVertex3f(self.x - self.largura / 2, self.y - self.altura / 2, -15)  # inferior direito
        glVertex3f(self.x + self.largura / 2, self.y - self.altura / 2, -15)  # inferior direito

        # face traseira
        glMaterialfv(GL_FRONT, GL_DIFFUSE, color)
        glVertex3f(self.x + self.largura / 2, self.y + self.altura / 2, -15)  # inferior esquerdo
        glVertex3f(self.x - self.largura / 2, self.y + self.altura / 2, -15)  # inferior esquerdo
        glVertex3f(self.x - self.largura / 2, self.y + self.altura / 2, 15)  # inferior esquerdo
        glVertex3f(self.x + self.largura / 2, self.y + self.altura / 2, 15)  # inferior esquerdo

        # face frontal
        glMaterialfv(GL_FRONT, GL_DIFFUSE, color)
        glVertex3f(self.x + self.largura / 2, self.y - self.altura / 2, 15)  # inferior direito
        glVertex3f(self.x - self.largura / 2, self.y - self.altura / 2, 15)  # inferior direito
        glVertex3f(self.x - self.largura / 2, self.y - self.altura / 2, -15)  # inferior direito
        glVertex3f(self.x + self.largura / 2, self.y - self.altura / 2, -15)  # inferior direito

        # face esquerda
        color = [0.45, 0.45, 0.45, 1]
        glMaterialfv(GL_FRONT, GL_DIFFUSE, color)
        glVertex3f(self.x - self.largura / 2, self.y + self.altura / 2, 15)  # inferior esquerdo
        glVertex3f(self.x - self.largura / 2, self.y + self.altura / 2, -15)  # inferior esquerdo
        glVertex3f(self.x - self.largura / 2, self.y - self.altura / 2, -15)  # inferior direito
        glVertex3f(self.x - self.largura / 2, self.y - self.altura / 2, 15)  # inferior direito

        # face direita
        color = [0.45, 0.45, 0.45, 1]
        glMaterialfv(GL_FRONT, GL_DIFFUSE, color)
        glVertex3f(self.x + self.largura / 2, self.y + self.altura / 2, 15)  # inferior esquerdo
        glVertex3f(self.x + self.largura / 2, self.y - self.altura / 2, 15)  # inferior direito
        glVertex3f(self.x + self.largura / 2, self.y - self.altura / 2, -15)  # inferior direito
        glVertex3f(self.x + self.largura / 2, self.y + self.altura / 2, -15)  # inferior esquerdo

        glEnd()

        if self.y + self.largura / 2 < -self.jogo.jogoAltura:
            self.visivel = False

    def anguloJogador(self):
        x = atan2(self.x - self.jogo.jogador.x, self.y - self.jogo.jogador.y)
        if -1 < x < 1:
            return x
        else:
            return 0

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
        self.angulo = 0

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

        self.radar()

        self.move()
        glTranslate(0, 9, 2)
        glEnable(GL_TEXTURE_2D)
        glBindTexture(GL_TEXTURE_2D, self.jogo.cockpit)
        glBegin(GL_QUADS)
        glTexCoord2f(0.0, 1.0)
        glVertex3f(self.largura/3, 0, self.largura/3)
        glTexCoord2f(0.0, 0.0)
        glVertex3f(- self.largura/3, 0, self.largura/3)
        glTexCoord2f(1.0, 0.0)
        glVertex3f(- self.largura/3, 0, -self.largura/3)
        glTexCoord2f(1.0, 1.0)
        glVertex3f(self.largura/3, 0, -self.largura/3)
        glEnd()

        glPopMatrix()
        glDisable(GL_TEXTURE_2D)

    def move(self):
        # print(self.angulo)
        glTranslate(self.x, self.y, 0)

        if self.esquerda:
            self.x -= self.velocidade
            if self.angulo > -45: self.angulo -= 2;
            glRotatef(self.angulo, 0, 1, 0)
        elif self.direita:
            self.x += self.velocidade
            if self.angulo < 45: self.angulo += 3;
            glRotatef(self.angulo, 0, 1, 0)
        elif not self.esquerda and not self.direita:
            if self.angulo > 0: self.angulo -= 2
            if self.angulo < 0: self.angulo += 3
            glRotatef(self.angulo, 0, 1, 0)

    def atira(self):
        if not self.tiro1:
            x = self.x - self.largura / 2
            self.tiro1 = True
        else:
            x = self.x + self.largura / 2
            self.tiro1 = False
        y = self.y

        trajetoria = TrajetoriaLinear(0, y, x, True)

        tiro = Tiro(self, 12, 40, x, y, self.jogo.texturaTiro1, trajetoria)
        self.jogo.tiros.append(tiro)

    def radar(self):
        glPushMatrix()
        glTranslate(self.x, self.y+8, -8.5)
        glRotate(90, 1, 0, 0)
        glScale(0.005, 0.005, 0.005)
        for i in self.jogo.inimigos:
            if abs(i.x-self.x)<=450 and 450>=i.y>=self.y:
                glTranslate(i.x-self.x, i.y, 0)
                color = [0, 1, 0, 1]
                glMaterialfv(GL_FRONT, GL_DIFFUSE, color)
                glBegin(GL_QUADS)
                glVertex3f(i.largura / 3, i.altura / 3, 0)
                glVertex3f(-i.largura / 3, i.altura / 3, 0)
                glVertex3f(-i.largura / 3, -i.altura / 3, 0)
                glVertex3f(i.largura / 3, -i.altura / 3, 0)
                glEnd()
        if self.jogo.boss is not None:
            i = self.jogo.boss
            if abs(i.x-self.x)<=450 and 450>=i.y>=self.y:
                glTranslate(i.x-self.x, i.y, 0)
                color = [0, 1, 0, 1]
                glMaterialfv(GL_FRONT, GL_DIFFUSE, color)
                glBegin(GL_QUADS)
                glVertex3f(i.largura / 3, i.altura / 3, 0)
                glVertex3f(-i.largura / 3, i.altura / 3, 0)
                glVertex3f(-i.largura / 3, -i.altura / 3, 0)
                glVertex3f(i.largura / 3, -i.altura / 3, 0)
                glEnd()
        glPopMatrix()

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

        self.startTimer(400 - self.jogo.nivel * 2)

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
        # self.jogo.audio.toca_som("../sounds/SFX/TIE Laser 1A.wav")


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

        trajetoria = TrajetoriaLinear(self.anguloJogador(), y, x - self.anguloJogador() * 100, True)

        tiro = Tiro(self, 15, 50, x, y, self.jogo.texturaTiro3, trajetoria, self.anguloJogador())
        self.jogo.tiros.append(tiro)

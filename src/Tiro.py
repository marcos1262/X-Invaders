from OpenGL.GL import *

from Trajetoria import Trajetoria


class Tiro:
    """
    Representa um tiro de qualquer nave
    """

    def __init__(self, largura, altura, x, y, jogo, trajetoria: Trajetoria):
        self.largura = largura
        self.altura = altura
        self.x = x
        self.y = y
        self.jogo = jogo
        self.trajetoria = trajetoria

        self.velocidade = 12
        self.visivel = True

    def desenha(self):
        # TODO colocar textura no tiro
        glColor4f(1, 1, 1, 1)

        self.move()

        glBegin(GL_QUADS)
        glVertex2f(self.x + self.largura / 2, self.y + self.altura / 2)  # superior direito
        glVertex2f(self.x - self.largura / 2, self.y + self.altura / 2)  # superior esquerdo
        glVertex2f(self.x - self.largura / 2, self.y - self.altura / 2)  # inferior esquerdo
        glVertex2f(self.x + self.largura / 2, self.y - self.altura / 2)  # inferior direito
        glEnd()

        if self.x - self.largura / 2 > self.jogo.jogoLargura / 2 \
                or self.x + self.largura / 2 < -self.jogo.jogoLargura / 2 \
                or self.y - self.largura / 2 > self.jogo.jogoAltura / 2 \
                or self.y + self.largura / 2 < -self.jogo.jogoAltura / 2:
            self.visivel = False

    def move(self):
        self.x, self.y = self.trajetoria.proximo(self.velocidade)

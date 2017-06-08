from OpenGL.GL import *


class CameraOrtogonal:
    def __init__(self, largura, altura, centro, x=0, y=0, near=-100, far=100):
        self.largura = largura
        self.altura = altura
        self.x = x
        self.y = y
        self.centro = centro
        self.near = near
        self.far = far
        self.atualiza(largura, altura)

    def atualiza(self, largura, altura, x=0, y=0):
        self.largura = largura
        self.altura = altura

        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()

        if self.centro:
            glOrtho(-self.largura/2 + x, self.largura/2 + x, -self.altura/2 + y, self.altura/2 + y, self.near, self.far)
        else:
            glOrtho(self.x + x, self.largura + x, self.y + y, self.altura + y, self.near, self.far)

        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()

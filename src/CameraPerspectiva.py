from OpenGL.GL import *

from OpenGL.GLU import *


class CameraPerspectiva:
    def __init__(self, fov=70, ar=1, near=1, far=1000):
        self.fov = fov
        self.ar = ar
        self.near = near
        self.far = far
        self.atualiza()

    def atualiza(self, x=0, y=-100):
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()

        gluPerspective(self.fov, self.ar, self.near, self.far)

        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()

        gluLookAt(x, -300, 500, x, y, 0, 0, 1, 1)

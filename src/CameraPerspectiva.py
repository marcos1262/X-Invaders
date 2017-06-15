from OpenGL.GL import *

from OpenGL.GLU import *


class CameraPerspectiva:
    def __init__(self, fov=100, ar=1, near=1, far=1000):
        self.fov = fov
        self.ar = ar
        self.near = near
        self.far = far
        self.atualiza()

    def atualiza(self, x=0, y=0, a=0):
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()

        gluPerspective(self.fov, self.ar, self.near, self.far)

        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()

        gluLookAt(x, y+5, 13, x, y+100, 13, a, 1, 1)

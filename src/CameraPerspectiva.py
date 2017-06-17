from OpenGL.GL import *

from OpenGL.GLU import *


class CameraPerspectiva:
    def __init__(self, fov=110, ar=1, near=1, far=1000):
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
        if a==0: gluLookAt(x+a*14, y+5, 19.8, x+a*14, y+100, 19.8, a, 1, 1)
        else: gluLookAt(x+a*14, y+5, 13+abs(a), x+a*14, y+100, 13+abs(a), a, 1, 1)

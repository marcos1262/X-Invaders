#!/usr/bin/env python
#-*- coding:utf-8 -*-

from OpenGL.GL import *

import os.path
import gtk

from Asteroid.libvec import *


class Asteroid:
    def __init__(self, x = 0, y = 0):
        mydir = os.path.dirname(__file__)
        self.img = gdk.pixbuf_new_from_file(os.path.join( mydir, "asteroid.png"))
        self.crt = gdk.pixbuf_new_from_file(os.path.join( mydir, "creto.png"))
        self.position = Vector()
        self.position.x = x
        self.position.y = y
        self.width = 47
        self.height = 22
        self.angle = 0
        self.is_dead = False
        self.creto = False

#    def shoot(self):
#        passs

        
    def draw(self):
        if self.creto:
            self.width = 45
            self.height = 58
            glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, self.crt.get_width(), self.crt.get_height(), \
                         0, GL_RGBA, GL_UNSIGNED_BYTE, self.crt.get_pixels())
        else:
            glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, self.img.get_width(), self.img.get_height(), \
                         0, GL_RGBA, GL_UNSIGNED_BYTE, self.img.get_pixels())

        if self.angle > 360:
            self.angle -= 360
        
        glEnable(GL_TEXTURE_2D)
        glPushMatrix()

        glTranslatef(self.position.x, self.position.y, self.position.z)
        glRotatef( self.angle , 0, 0, 1 )
        glTranslatef(-self.position.x, -self.position.y, self.position.z)

        glBegin(GL_QUADS)
        glTexCoord2f(0,1)
        glVertex3f( self.position.x - self.width, self.position.y - self.height, 1.5 )
        glTexCoord2f(1,1)
        glVertex3f( self.position.x + self.width, self.position.y - self.height, 1.5 )
        glTexCoord2f(1,0)
        glVertex3f( self.position.x + self.width, self.position.y + self.height, 1.5 )
        glTexCoord2f(0,0)
        glVertex3f( self.position.x - self.width, self.position.y + self.height, 1.5 )
        glEnd()

        glPopMatrix()
        glDisable(GL_TEXTURE_2D)

        # bounding box
#        glColor3f(1, 0, 0)
#        glLineWidth( 3 )
#        glBegin(GL_LINE_LOOP)
#        glVertex3f( self.position.x - self.width, self.position.y - self.height, 1.90 )
#        glVertex3f( self.position.x + self.width, self.position.y - self.height, 1.90 )
#        glVertex3f( self.position.x + self.width, self.position.y + self.height, 1.90 )
#        glVertex3f( self.position.x - self.width, self.position.y + self.height, 1.90 )        
#        glEnd()

        
        self.angle += 2
        self.position.y -= 3

        if self.position.y < 0:
            self.is_dead = True
        
        

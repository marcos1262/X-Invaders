#!/usr/bin/env python
#-*- coding:utf-8 -*-

from OpenGL.GL import *

from libvec import *
import os.path
import gtk
from random import randint

view_w = 500

class Enemy2:
    def __init__(self, x = 0, y = 0):
        mydir = os.path.dirname(__file__)
        self.img = gtk.gdk.pixbuf_new_from_file(os.path.join( mydir, "enemy2.png"))
        self.position = Vector()
        self.position.x = x
        self.position.y = y
        self.width = 50
        self.height = 31
        self.angle = 0
        self.is_dead = False
        self.creto = False
        self.step_x = randint(3,9)

        
    def draw(self):
        glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, self.img.get_width(), self.img.get_height(), \
                     0, GL_RGBA, GL_UNSIGNED_BYTE, self.img.get_pixels())
        
        glEnable(GL_TEXTURE_2D)
        glPushMatrix()

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

        
        self.position.x += self.step_x
        
        if self.position.x > view_w:
            self.is_dead = True
        
        

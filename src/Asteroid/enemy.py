#!/usr/bin/env python
#-*- coding:utf-8 -*-

from OpenGL.GL import *

from libvec import *
import os.path
import gtk
from random import randint

from main import view_w

class Enemy:
    def __init__(self, x = 0, y = 0):
        mydir = os.path.dirname(__file__)
        self.img = gtk.gdk.pixbuf_new_from_file(os.path.join( mydir, "enemy.png"))
        self.position = Vector()
        self.position.x = x
        self.position.y = y
        self.width = 32
        self.height = 46
        self.angle = 0
        self.is_dead = False
        self.creto = False
        self.move = "right" if randint(0,1) else "left"
        self.step_x = randint(3,6)
        self.step_y = randint(3,6)

        
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
        
        self.position.y -= self.step_y
        
        if self.move == "left":
            self.position.x -= self.step_x
            
        elif self.move == "right":
            self.position.x += self.step_x
        
        if self.position.x > view_w:
            self.move = "left"
            
        if self.position.x < 0:
            self.move = "right"

        if self.position.y < 0:
            self.is_dead = True
        
        

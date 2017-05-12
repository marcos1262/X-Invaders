#!/usr/bin/env python
#-*- coding:utf-8 -*-

from OpenGL.GL import *

from libvec import *
import os.path
import gtk
from random import randint
from time import time

view_w = 500
view_h = 500

class Boss:
    def __init__(self, x = 0, y = 0):
        mydir = os.path.dirname(__file__)
        self.img = gtk.gdk.pixbuf_new_from_file(os.path.join( mydir, "boss.png"))
        self.position = Vector()
        self.position.x = x
        self.position.y = y
        self.width = 100
        self.height = 67
        self.angle = 0
        self.is_dead = False
        self.creto = False
        self.step_x = 6
        self.step_y = 3
        self.life = 5 # 10 
        self.hor_move = "right" if randint(0,1) else "left"
        self.ver_move = "down" if randint(0,1) else "up"
        self.is_visible = True
        self.time = time()

        
    def draw(self):
        if self.is_visible:
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
        
        if self.ver_move == "up":
            self.position.y += self.step_y
            
        elif self.ver_move == "down":
            self.position.y -= self.step_y
        
        if self.position.y > view_h:
            self.ver_move = "down"
            
        if self.position.y < 200:
            self.ver_move = "up"
        
        if self.hor_move == "left":
            self.position.x -= self.step_x
            
        elif self.hor_move == "right":
            self.position.x += self.step_x
        
        if self.position.x > view_w:
            self.hor_move = "left"
            
        if self.position.x < 0:
            self.hor_move = "right"
            
        if not randint(0,100):
            self.is_visible = False
            self.time = time()
        
        if not self.is_visible and time() - self.time > 2: 
            self.is_visible = True
            
        if self.life <= 0:
            self.is_dead = True
        
        

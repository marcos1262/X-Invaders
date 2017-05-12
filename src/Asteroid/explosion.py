#!/usr/bin/env python
#-*- coding:utf-8 -*-

from OpenGL.GL import *

from libvec import *
import os.path
import gtk
import math
from time import time


EXPLOSION_FRAME = 0.045
EXPLOSION_FRAMES = 8

imgs = [ None for i in range(EXPLOSION_FRAMES) ]


class Explosion:
    def __init__(self, x = None, y = None):
        self.start = time()
        self.quadro = 0
        self.x = x
        self.y = y
        self.is_dead = False
    
        
    def draw(self):
        global imgs
        img = imgs[ self.quadro ]
        
        w = img.get_width()
        h = img.get_height()
        
        glColor3f( 1, 1, 1 )
        glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, w, h, \
                     0, GL_RGBA, GL_UNSIGNED_BYTE, img.get_pixels() )
        
        
        glEnable(GL_TEXTURE_2D)
        glBegin(GL_QUADS)
        glTexCoord2f(0,1)
        glVertex3f( self.x - w/2, self.y - h/2, 1.9 )
        glTexCoord2f(1,1)
        glVertex3f( self.x + w/2, self.y - h/2, 1.9 )
        glTexCoord2f(1,0)
        glVertex3f( self.x + w/2, self.y + h/2, 1.9 )
        glTexCoord2f(0,0)
        glVertex3f( self.x - w/2, self.y + h/2, 1.9 )
        glEnd()
        glDisable(GL_TEXTURE_2D)


        if time() - self.start >= EXPLOSION_FRAME:
            self.quadro += 1
            self.start = time()
            
            if self.quadro >= EXPLOSION_FRAMES:
                self.quadro = EXPLOSION_FRAMES-1
                self.is_dead = True
        


def explosion_init():
    global imgs
    mydir = os.path.dirname(__file__)
    for i in range( EXPLOSION_FRAMES ):
        imgs[i] = gtk.gdk.pixbuf_new_from_file( os.path.join( mydir, "explosion", "exp%d.png" % i) )


def explosion_add(gl_scene, x, y):
    gl_scene.append( Explosion(x,y) )


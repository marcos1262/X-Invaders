#!/usr/bin/env python
#-*- coding:utf-8 -*-

import gtk
from OpenGL.GL import *
import math
from time import time
from random import random, randint
import os


STAR_GRAVITY = -5
DEFAULT_STAR_COUNT = 50

SLOW_STAR_WIDTH  = 70
SLOW_STAR_FACTOR = 0.2


imgs = []
img_count = []


star_count = 0 


class Star:
    def __init__(self, w, h):
        global star_count, imgs, img_count
        star_count += 1
        
        self.start = time()
        self.pisca = random() * 10
        self.size = 1.5 + random() * 3.0

        self.x = float(w) * random()
        self.y = float(h) * random() + h
        self.vy = STAR_GRAVITY * 0.5 + ( random() * STAR_GRAVITY * 0.5 )
        
        self.tipo = None
        if random() > 0.98 and len(imgs) > 0:
            i = randint( 0, len(imgs)-1 )
            if img_count[i] == 0:
                img_count[i] = 1
                self.tipo = i

                # diminui a velocidade se a textura for muito grande
                if imgs[ self.tipo ].get_width() > SLOW_STAR_WIDTH:
                    self.vy *= SLOW_STAR_FACTOR

        
        self.is_dead = False

        self.rgb_base = 0.3
        self.r = random() * (1.0 - self.rgb_base)
        self.g = random() * (1.0 - self.rgb_base)
        self.b = random() * (1.0 - self.rgb_base)

    
    def draw(self):
        if self.tipo == None:
            h = 1

            fator = (math.sin( time() * self.pisca + self.start ) + 1.0) / 2
            glColor3f( self.rgb_base + fator * self.r, self.rgb_base + fator * self.g, \

            self.rgb_base + fator * self.b )
            glPointSize( self.size )
            glEnable( GL_POINT_SMOOTH )
            
            glBegin( GL_POINTS )
            glVertex3f( self.x, self.y, -1.0 ) 
            glEnd()

            glDisable( GL_POINT_SMOOTH )
            glPointSize( 1 )            
                        
        else:
            img = imgs[ self.tipo ]            
            w = img.get_width()
            h = img.get_height()
            
            glColor3f(1,1,1)
            glTexImage2D( GL_TEXTURE_2D, 0, GL_RGBA, w, h, \
                          0, GL_RGBA, GL_UNSIGNED_BYTE, img.get_pixels() )
            
            z = -0.1
            
            glEnable(GL_TEXTURE_2D)
            glBegin(GL_QUADS)
            glTexCoord2f(0,1)
            glVertex3f( self.x - w/2, self.y - h/2, z )
            glTexCoord2f(1,1)
            glVertex3f( self.x + w/2, self.y - h/2, z )
            glTexCoord2f(1,0)
            glVertex3f( self.x + w/2, self.y + h/2, z )
            glTexCoord2f(0,0)
            glVertex3f( self.x - w/2, self.y + h/2, z )
            glEnd()
            glDisable(GL_TEXTURE_2D)
            
        self.y += self.vy
        if self.y - h/2 <= 0:
            self.is_dead = True
            
            global star_count
            star_count -= 1
            
            if self.tipo != None:
                img_count[ self.tipo ] = 0



def put_stars(w, h, gl_scene, n = DEFAULT_STAR_COUNT):
    stars_to_add = n - star_count
    if stars_to_add > 0:
    
        for i in range( stars_to_add ):
            gl_scene.append( Star(w,h) )


def stars_init():
    global imgs, img_count
    
    mydir = os.path.dirname(__file__)
    d = os.path.join( mydir, "stars" )
    lista = os.listdir( d )
    
    for arq in lista:
        print "Usando estrela: %s" % arq
        imgs.append( gtk.gdk.pixbuf_new_from_file( os.path.join( d, arq ) ) )
        img_count.append( 0 )


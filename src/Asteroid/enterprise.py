#!/usr/bin/env python
#-*- coding:utf-8 -*-

print "Loading OpenGL library"
from OpenGL.GL import *
print "OK, OpenGL loaded!"

from libvec import *
import os.path
import gtk

class NCC1701:
    def __init__(self, x = None, y = None ):
        mydir = os.path.dirname(__file__)
        self.img = gtk.gdk.pixbuf_new_from_file(os.path.join( mydir, "ship.png"))
        self.position = Vector()
        self.position.x = x
        self.position.y = y
        self.width = 22
        self.height = 47
        self.is_dead = False
        
    def draw(self):
        glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, self.img.get_width(), self.img.get_height(), \
                     0, GL_RGBA, GL_UNSIGNED_BYTE, self.img.get_pixels())
        
        glEnable(GL_TEXTURE_2D)
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
        glDisable(GL_TEXTURE_2D)

        # bounding box
#        glColor3f(1, 1, 0)
#        glLineWidth( 3 )
#        glBegin(GL_LINE_LOOP)
#        glVertex3f( self.position.x - self.width, self.position.y - self.height, 1.90 )
#        glVertex3f( self.position.x + self.width, self.position.y - self.height, 1.90 )
#        glVertex3f( self.position.x + self.width, self.position.y + self.height, 1.90 )
#        glVertex3f( self.position.x - self.width, self.position.y + self.height, 1.90 )        
#        glEnd()

        
        
if __name__ == '__main__':
    NCC1701()

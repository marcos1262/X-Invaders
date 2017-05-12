#!/usr/bin/env python
#-*- coding:utf-8 -*-
#
# Port da biblioteca 'pygtkOpenGL', feita originalmente em C, para uma versão
# 100% puro-python.
#
# Autores: Ricardo Lenz & Daniel Siqueira
#
# Esse código usou várias referências:
# - read_cursor_image.py (Osmo Antero M)
# - Port do Xlib p/ Python (http://code.google.com/p/pyxlib-ctypes, mtasic85)
# - PyGtk client side windows demo (John Stowers)
# - manual do XLib
# - PyGTK FAQ 23.41
#
# Todas as procs que retornam um ponteiro (GdkDisplay*, Display*, GdkVisual* etc)
# são consideradas como retornando c_void_p. É que, dessa forma, podemos ver se
# o ponteiro é nulo diretamente, fazendo c_void_p == None.
#
# Para acessar uma struct a partir desse c_void_p, faça simplesmente:
# struct.from_address( c_void_p ).
#


from ctypes import *
import gtk

import OpenGL
import OpenGL.GLX
from OpenGL.GLX import GLX_RGBA, GLX_DOUBLEBUFFER, GLX_DEPTH_SIZE, GLX_STENCIL_SIZE


# material do X11
#
#########################################################

XPointer = c_char_p
VisualID = c_ulong
XID = c_ulong
Window = XID

class Visual(Structure):
    _fields_ = [
        ('ext_data', c_void_p),
        ('visualid', VisualID),
        ('c_class', c_int),
        ('red_mask', c_ulong),
        ('green_mask', c_ulong),
        ('blue_mask', c_ulong),
        ('bits_per_rgb', c_int),
        ('map_entries', c_int),
    ]

    def debug(self):
        print "Visual:"
        print "  visual id = %d" % self.visualid
        print "  c_class = %d" % self.c_class
        print "  red_mask = %06x" % self.red_mask
        print "  green_mask = %06x" % self.green_mask
        print "  blue_mask = %06x" % self.blue_mask
        print "  bits_per_rgb = %d" % self.bits_per_rgb
        print "  map_entries = %d" % self.map_entries


class XVisualInfo(Structure):       # Xutil.h
    _fields_ = [
        ('visual', c_void_p),       # Visual *
        ('visualid', VisualID),     # VisualID
        ('screen', c_int),          # int
        ('depth', c_uint),          # unsigned int
        ('class', c_int),           # int
        ('red_mask', c_ulong),      # unsigned long
        ('green_mask', c_ulong),    # unsigned long
        ('blue_mask', c_ulong),     # unsigned long
        ('colormap_size', c_int),   # int
        ('bits_per_rgb', c_int)     # int
    ]

    def debug(self):
        print "XVisualInfo:"
        print "  visual id = %d" % self.visualid
        print "  screen = %d" % self.screen
        print "  depth = %d" % self.depth
        print "  class = %d" % getattr( self, 'class' )
        print "  red_mask = %06x" % self.red_mask
        print "  green_mask = %06x" % self.green_mask
        print "  blue_mask = %06x" % self.blue_mask
        print "  colormap_size = %d" % self.colormap_size
        print "  bits_per_rgb = %d" % self.bits_per_rgb

        
class Screen(Structure):
    _fields_ = [
        ('ext_data', c_void_p),
        ('display', c_void_p),
        ('root', VisualID),
        ('width', c_int),
        ('height', c_int),
        ('mwidth', c_int),
        ('mheight', c_int),
        ('ndepths', c_int),
        ('depths', c_void_p),
        ('root_depth', c_int),
        ('root_visual', c_void_p),
        ('default_gc', c_void_p),
        ('cmap', c_int),
        ('white_pixel', c_ulong),
        ('black_pixel', c_ulong),
        ('max_maps', c_int),
        ('min_maps', c_int),
        ('backing_store', c_int),
        ('save_unders', c_int),
        ('root_input_mask', c_long),
    ]

    def debug(self):
        print "Screen:"
        print "  width = %d" % self.width
        print "  height = %d" % self.height
        print "  root = %d" % self.root
        print "  ndepths = %d" % self.ndepths
        print "  cmap = %d" % self.cmap
        print "  white_pixel = %06x" % self.white_pixel
        print "  black_pixel = %06x" % self.black_pixel


class Display(Structure):
    _fields_ = [
        ('ext_data', c_void_p),
        ('private1', c_void_p),
        ('fd', c_int),
        ('private2', c_int),
        ('proto_major_version', c_int),
        ('proto_minor_version', c_int),
        ('vendor', c_char_p),
        ('private3', XID),
        ('private4', XID),
        ('private5', XID),
        ('private6', c_int),
        ('resource_alloc', c_void_p),
        ('byte_order', c_int),
        ('bitmap_unit', c_int),
        ('bitmap_pad', c_int),
        ('bitmap_bit_order', c_int),
        ('nformats', c_int),
        ('pixmap_format', c_void_p),
        ('private8', c_int),
        ('release', c_int),
        ('private9', c_void_p),
        ('private10', c_void_p),
        ('qlen', c_int),
        ('last_request_read', c_ulong),
        ('request', c_ulong),
        ('private11', XPointer),
        ('private12', XPointer),
        ('private13', XPointer),
        ('private14', XPointer),
        ('max_request_size', c_uint),
        ('db', c_void_p),
        ('private15', c_void_p),
        ('display_name', c_char_p),
        ('default_screen', c_int),
        ('nscreens', c_int),
        ('screens', c_void_p),
        ('motion_buffer', c_ulong),
        ('private16', c_ulong),
        ('min_keycode', c_int),
        ('max_keycode', c_int),
        ('private17', XPointer),
        ('private18', XPointer),
        ('private19', c_int),
        ('xdefaults', c_char_p),
    ]
    
    
    def debug(self):
        print "Display:"
        print "  fd = %d" % self.fd
        print "  proto_major_version = %d" % self.proto_major_version
        print "  proto_minor_version = %d" % self.proto_minor_version
        print "  vendor = '%s'" % self.vendor
        print "  nformats = %d" % self.nformats
        print "  display_name = '%s'" % self.display_name
        print "  default_screen = %d" % self.default_screen
        print "  nscreens = %d" % self.nscreens
        

XDefaultScreenOfDisplay = None
XVisualIDFromVisual = None


def init_x11_procs():
    lib = CDLL('libX11.so')

    # Screen * = XDefaultScreenOfDisplay( Display * )
    #
    global XDefaultScreenOfDisplay
    XDefaultScreenOfDisplay = lib.XDefaultScreenOfDisplay

    XDefaultScreenOfDisplay.restype = c_void_p
    XDefaultScreenOfDisplay.argtypes = [ c_void_p ]
    #
    ###########

    # VisualID = XVisualIDFromVisual( Visual * )
    #
    global XVisualIDFromVisual
    XVisualIDFromVisual = lib.XVisualIDFromVisual

    XVisualIDFromVisual.restype = VisualID
    XVisualIDFromVisual.argtypes = [ c_void_p ]
    #
    ###########




# material do GLX
#
#########################################################


# de GL/glx.h: 
#   typedef XID GLXDrawable;
#   ...
#   typedef struct __GLXcontextRec *GLXContext;
#
# portanto:
#   todo GLXContext = c_void_p,
#   e todo GLXDrawable = XID
#

glXChooseVisual = None
glXCreateContext = None
glXDestroyContext = None
glXSwapBuffers = None


def init_glx_procs():
    # XVisualInfo * = glXChooseVisual(Display *, int screen, int * attribList)
    #
    global glXChooseVisual
    glXChooseVisual = OpenGL.GLX.glXChooseVisual

    glXChooseVisual.restype = c_void_p
    glXChooseVisual.argtypes = [c_void_p, c_int, POINTER(c_int) ]
    #
    ###########

    # GLXContext = glXCreateContext(Display *,  XVisualInfo *, GLXContext shareList, Bool direct )
 	#
    global glXCreateContext
    glXCreateContext = OpenGL.GLX.glXCreateContext

    glXCreateContext.restype = c_void_p
    glXCreateContext.argtypes = [c_void_p, c_void_p, c_void_p, c_int ]
    #
    ###########

    # void glXDestroyContext( Display *, GLXContext ctx )
 	#
    global glXDestroyContext
    glXDestroyContext = OpenGL.GLX.glXDestroyContext

    glXDestroyContext.restype = None
    glXDestroyContext.argtypes = [c_void_p, c_void_p]
    #
    ###########

    # Bool = glXMakeCurrent( Display *, GLXDrawable = XID, GLXContext ctx )
 	#
    global glXMakeCurrent
    glXMakeCurrent = OpenGL.GLX.glXMakeCurrent

    glXMakeCurrent.restype = c_int
    glXMakeCurrent.argtypes = [c_void_p, XID, c_void_p]
    #
    ###########
 	
 
    # void glXSwapBuffers( Display *, GLXDrawable = XID )
 	#
    global glXSwapBuffers
    glXSwapBuffers = OpenGL.GLX.glXSwapBuffers

    glXSwapBuffers.restype = None
    glXSwapBuffers.argtypes = [c_void_p, XID]
    #
    ###########



# material do GTK
#
#########################################################

gdk_display_get_default = None
gdk_x11_display_get_xdisplay = None
gdk_x11_drawable_get_xid = None
gdkx_visual_get = None

gdk_colormap_new = None
gtk_widget_push_colormap = None


def init_gtk_procs():    
    lib = CDLL('libgtk-x11-2.0.so')
 
 
    # GdkDisplay * = gdk_display_get_default( void )
    #
    global gdk_display_get_default
    gdk_display_get_default = lib.gdk_display_get_default
    
    gdk_display_get_default.restype = c_void_p
    gdk_display_get_default.argtypes = []
    #
    #########


    # Display * = gdk_x11_display_get_xdisplay( GdkDisplay * )
    #
    global gdk_x11_display_get_xdisplay
    gdk_x11_display_get_xdisplay = lib.gdk_x11_display_get_xdisplay
    
    gdk_x11_display_get_xdisplay.restype = c_void_p
    gdk_x11_display_get_xdisplay.argtypes = [ c_void_p ]
    #
    #########


    # Window = GDK_WINDOW_XWINDOW( GdkWindow * )
    # XID = gdk_x11_drawable_get_xid( GdkDrawable * )
    #
    global gdk_x11_drawable_get_xid
    gdk_x11_drawable_get_xid = lib.gdk_x11_drawable_get_xid
    
    gdk_x11_drawable_get_xid.restype = XID
    gdk_x11_drawable_get_xid.argtypes = [ c_void_p ]
    #
    #########

    
    # GdkVisual* = gdkx_visual_get( VisualID )
    #
    global gdkx_visual_get
    gdkx_visual_get = lib.gdkx_visual_get

    gdkx_visual_get.restype = c_void_p
    gdkx_visual_get.argtypes = [ VisualID ]
    #
    #########
    

    # GdkColormap* = gdk_colormap_new( GdkVisual *, gboolean allocate )
    #
    global gdk_colormap_new
    gdk_colormap_new = lib.gdk_colormap_new

    gdk_colormap_new.restype = c_void_p
    gdk_colormap_new.argtypes = [ c_void_p, c_int ]    
    #
    #########

    # void gtk_widget_push_colormap( GdkColormap * )
    #
    global gtk_widget_push_colormap
    gtk_widget_push_colormap = lib.gtk_widget_push_colormap

    gtk_widget_push_colormap.restype = None
    gtk_widget_push_colormap.argtypes = [ c_void_p ]    
    #
    #########




# biblioteca pygtkOpenGL propriamente dita
#
#########################################################

attr_depth_bits = 0
attr_stencil_bits = 0

x_visual_info = None
gl_context = None
ptr_x11_display = None



def desired_context(depth_bits = 24, stencil_bits = 8):
    global attr_depth_bits, attr_stencil_bits
    attr_depth_bits = depth_bits
    attr_stencil_bits = stencil_bits
    

def new_context():
    
    # 1 - display
    #
    py_gdk_display = gtk.gdk.display_get_default()
    c_gdk_display = hash( py_gdk_display )
    
    global ptr_x11_display
    ptr_x11_display = gdk_x11_display_get_xdisplay( c_gdk_display )
    if ptr_x11_display == None:
        print "*** Erro: gdk_x11_display_get_xdisplay() -> nulo"
        return False

    c_x11_display = Display.from_address( ptr_x11_display )
    #c_x11_display.debug()
    
    default_screen = c_x11_display.default_screen

    
    # 2 - screen
    #
    ptr_x11_screen = XDefaultScreenOfDisplay( ptr_x11_display )
    if ptr_x11_screen == None:
        print "*** Erro: XDefaultScreenOfDisplay() -> nulo"
        return False
    
    c_x11_screen = Screen.from_address( ptr_x11_screen )
    #c_x11_screen.debug()

    
    # 3 - atributos
    #
    attrs = [ GLX_RGBA, GLX_DOUBLEBUFFER, \
        GLX_DEPTH_SIZE, attr_depth_bits,
        GLX_STENCIL_SIZE, attr_stencil_bits,
        0 ]
    ptr_attrs = (c_int * len(attrs)) ( *attrs )


    # 4 - visual info
    #
    x_visual_info_ptr = glXChooseVisual( ptr_x11_display, default_screen, ptr_attrs )
    if x_visual_info_ptr == None:
        print "*** Erro: glXChooseVisual() -> nulo"
        return False
    
    global x_visual_info
    x_visual_info = XVisualInfo.from_address( x_visual_info_ptr )
    #x_visual_info.debug()
    
    
    # 5 - gl context
    #
    global gl_context
    gl_context = glXCreateContext( ptr_x11_display, x_visual_info_ptr, None, 1 )
    if gl_context == None:
        print "*** Erro: glXCreateContext() -> nulo"
        return False
    
    return True
    


def free_context():
    glXDestroyContext( ptr_x11_display, gl_context )
    return True



def prepare_widget_begin():
    if x_visual_info == None:
        return False
    
    visual_id = x_visual_info.visualid
    
    ptr_gdk_visual = gdkx_visual_get( visual_id )
    if ptr_gdk_visual == None:
        print "*** Erro: gdkx_visual_get() -> nulo"
        return False

    ptr_gdk_colormap = gdk_colormap_new( ptr_gdk_visual, 1 )
    gtk_widget_push_colormap( ptr_gdk_colormap )    
        
    return True	


def prepare_widget_end(widget):
    gtk.widget_pop_colormap()
    widget.set_double_buffered( False )
    return True
    

def widget_begin_gl(widget):
    ptr_c_gdk_drawable = hash(widget.window)
    xid = gdk_x11_drawable_get_xid( ptr_c_gdk_drawable )
    
    glXMakeCurrent( ptr_x11_display, xid, gl_context )
    return True


def widget_end_gl(widget):
    glXMakeCurrent( ptr_x11_display, 0, None )
    return True


def widget_swap_buffers(widget):
    ptr_c_gdk_drawable = hash(widget.window)
    xid = gdk_x11_drawable_get_xid( ptr_c_gdk_drawable )
    
    glXSwapBuffers( ptr_x11_display, xid )
    return True


init_x11_procs()
init_glx_procs()
init_gtk_procs()


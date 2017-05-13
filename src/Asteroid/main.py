#!/usr/bin/env python
# -*- coding:utf-8 -*-

import os.path
from gtk import gdk

from gi.overrides import GLib as glib
from gi.overrides import Gtk as gtk
from gi.overrides import GdkPixbuf

from Asteroid.pygtk_gl import *
from Asteroid.enterprise import *
from Asteroid.asteroid import *
from Asteroid.sound import *
from Asteroid.enemy import *
from Asteroid.enemy2 import *
from Asteroid.boss import *
from Asteroid.libvec import *
from Asteroid.explosion import *
from Asteroid.stars import *

from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *


view_w = 500
view_h = 500
step = 10
SHOOT_TIME = 1.0


class Laser:
    def __init__(self, x=None, y=None, enemy=False):
        self.position = Vector()
        self.position.x = x
        self.position.y = y
        self.width = 2
        self.height = 10
        self.is_dead = False
        self.enemy = enemy

    def draw(self):
        if self.enemy:
            glColor3f(1, 0, 0)
            self.position.y -= step
        else:
            glColor3f(0, 1, 0)
            self.position.y += step

        glRectf(self.position.x - self.width, self.position.y - self.height, self.position.x + self.width,
                self.position.y + self.height)

        if self.position.y > view_h or self.position.y < 0:
            self.is_dead = True


class Load_bar:
    def __init__(self):
        self.is_dead = False
        self.y = 0.0

    def draw(self):
        w = 10
        glColor3f(0, 1, 0)
        glBegin(GL_QUADS)
        glVertex3f(view_w - w, self.y, 1.5)
        glVertex3f(view_w, self.y, 1.5)
        glVertex3f(view_w, 0, 1.5)
        glVertex3f(view_w - w, 0, 1.5)
        glEnd()


class Shooting:
    def __init__(self):

        mydir = os.path.dirname(__file__)
        builder = gtk.Builder()
        builder.add_from_file(os.path.join(mydir, "shooting.glade"))

        self.fundo = GdkPixbuf.Pixbuf.new_from_file(os.path.join(mydir, "fundo.png"))
        self.logo = GdkPixbuf.Pixbuf.new_from_file(os.path.join(mydir, "logo.png"))

        self.gl_scene = []
        self.go_left = False
        self.go_right = False
        self.space_press = False
        self.loading_time = 0.0
        self.bullets_list = []
        self.asteroids_list = []

        new_context()
        prepare_widget_begin()
        self.gl_area = gtk.DrawingArea()
        prepare_widget_end(self.gl_area)

        self.main_window = builder.get_object("main_window")
        self.viewport = builder.get_object("viewport")
        self.label_score = builder.get_object("label_score")

        self.main_window.add_events(gtk.gdk.KEY_PRESS_MASK | gtk.gdk.KEY_RELEASE_MASK)

        self.viewport.add(self.gl_area)
        self.gl_area.set_size_request(view_w, view_h)
        self.gl_area.set_visible(True)

        self.gl_area.connect("expose-event", self.gl_paint)
        self.gl_area.connect("realize", self.gl_configure)
        self.main_window.connect("delete-event", self.on_close)
        self.main_window.connect("key-press-event", self.on_main_window_key_press_event)
        self.main_window.connect("key-release-event", self.on_main_window_key_release_event)

        self.ship = NCC1701(22, 47)
        self.boss = None
        self.bar = Load_bar()
        explosion_init()
        stars_init()

        self.level = 1
        self.play_theme()

        self.gl_scene.append(self.ship)
        self.gl_scene.append(self.bar)
        glib.timeout_add(50, self.gl_repaint)
        glib.timeout_add(1500, self.create_objects)
        glib.timeout_add(47000, self.play_theme)
        self.time = time()
        self.logo_time = time()
        self.boss_time = 0
        self.score_atual = 0

    def play_theme(self):
        if self.level < 5:
            play_sound("theme")

        return True

    def gl_repaint(self):
        self.process_moving()
        self.gl_area.queue_draw()
        return True

    def gl_configure(self, widget):
        widget_begin_gl(widget)
        glClearColor(0, 0, 0, 0)

        glEnable(GL_DEPTH_TEST)

        # pra habilitar transparência, temos que ativar o BLEND
        # e configurá-lo.
        glEnable(GL_BLEND)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)

        glEnable(GL_ALPHA_TEST)
        glAlphaFunc(GL_NOTEQUAL, 0.0)

        glTexEnvi(GL_TEXTURE_ENV, GL_TEXTURE_ENV_MODE, GL_REPLACE)
        glTexParameter(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
        glTexParameter(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)

        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        glOrtho(0, view_w, 0, view_h, -2.0, 2.0)
        glMatrixMode(GL_MODELVIEW)
        widget_end_gl(widget)

    def gl_paint(self, widget, event):
        widget_begin_gl(widget)
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        # remove todos que morreram da lista da cena
        i = len(self.gl_scene) - 1
        while i >= 0:
            if self.gl_scene[i].is_dead:
                del self.gl_scene[i]
            i -= 1

        if time() - self.logo_time <= 4.5:
            self.desenha_na_tela_toda(self.logo)

        # desenha todo mundo
        for obj in self.gl_scene:
            obj.draw()

        for asteroid in self.asteroids_list:
            if not asteroid.is_dead:
                if randint(0, 40 / self.level) == 0 and not isinstance(asteroid, Asteroid):
                    if isinstance(asteroid, Boss):
                        self.shoot(asteroid.position.x - asteroid.width, asteroid.position.y - 1.3 * asteroid.height,
                                   enemy=True)
                        self.shoot(asteroid.position.x + asteroid.width, asteroid.position.y - 1.3 * asteroid.height,
                                   enemy=True)
                    else:
                        self.shoot(asteroid.position.x, asteroid.position.y - 1.3 * asteroid.height, enemy=True)

                if not self.ship.is_dead:
                    if self.is_coliding(asteroid, self.ship):
                        if not asteroid.creto and not isinstance(asteroid, Boss):
                            explosion_add(self.gl_scene, asteroid.position.x, asteroid.position.y)
                            self.asteroids_list.remove(asteroid)
                            asteroid.is_dead = True
                        explosion_add(self.gl_scene, self.ship.position.x, self.ship.position.y)
                        play_sound("explosao")
                        self.destroy_ship()

                for bullet in self.bullets_list:
                    if not bullet.is_dead:
                        if self.level == 1 and asteroid.creto and self.is_coliding(asteroid, bullet):
                            explosion_add(self.gl_scene, self.ship.position.x, self.ship.position.y)
                            play_sound("explosao")
                            self.bullets_list.remove(bullet)
                            bullet.is_dead = True
                            self.destroy_ship()

                        elif not bullet.enemy and self.is_coliding(asteroid, bullet) and not isinstance(asteroid, Boss):
                            explosion_add(self.gl_scene, asteroid.position.x, asteroid.position.y)
                            play_sound("explosao")
                            self.bullets_list.remove(bullet)
                            if self.asteroids_list:
                                self.asteroids_list.remove(asteroid)
                            asteroid.is_dead = True
                            bullet.is_dead = True
                            self.score_gain(100)
                            if asteroid.creto:
                                self.score_gain(1000)


                        elif not bullet.enemy and self.is_coliding(asteroid, bullet) and isinstance(asteroid, Boss):
                            explosion_add(self.gl_scene, asteroid.position.x, asteroid.position.y)
                            play_sound("explosao")
                            asteroid.position.y += 50
                            self.bullets_list.remove(bullet)
                            bullet.is_dead = True
                            self.score_gain(100)
                            asteroid.life -= 1

                        elif bullet.enemy and self.is_coliding(self.ship, bullet):
                            if not self.ship.is_dead:
                                explosion_add(self.gl_scene, self.ship.position.x, self.ship.position.y)
                                play_sound("explosao")
                                self.bullets_list.remove(bullet)
                                bullet.is_dead = True
                                self.destroy_ship()
                    else:
                        self.bullets_list.remove(bullet)
            else:
                self.asteroids_list.remove(asteroid)

        if self.level < 4 and ((time() - self.time) > 47):
            self.level += 1
            self.time = time()

        if self.boss and self.boss.is_dead:
            self.desenha_na_tela_toda(self.fundo)
            if self.level != 5:
                self.level = 5
                stop_playing("theme")
                play_sound("end.mp3")

        widget_swap_buffers(widget)
        widget_end_gl(widget)

    def desenha_na_tela_toda(self, textura, cor=(1, 1, 1)):
        glEnable(GL_TEXTURE_2D)
        glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, textura.get_width(), textura.get_height(), \
                     0, GL_RGBA, GL_UNSIGNED_BYTE, textura.get_pixels())

        glMatrixMode(GL_PROJECTION)
        glPushMatrix()
        glLoadIdentity()
        glMatrixMode(GL_MODELVIEW)
        glPushMatrix()
        glLoadIdentity()

        # desenha sem passar pelo teste de zbuffer
        glDepthMask(GL_FALSE)
        glDisable(GL_DEPTH_TEST)

        glColor3f(cor[0], cor[1], cor[2])
        glBegin(GL_QUADS)
        glTexCoord2f(0, 1)
        glVertex2f(-1, -1)
        glTexCoord2f(1, 1)
        glVertex2f(+1, -1)
        glTexCoord2f(1, 0)
        glVertex2f(+1, +1)
        glTexCoord2f(0, 0)
        glVertex2f(-1, +1)
        glEnd()

        # volta a passar pelo teste de zbuffer
        glDepthMask(GL_TRUE)
        glEnable(GL_DEPTH_TEST)

        glMatrixMode(GL_PROJECTION)
        glPopMatrix()
        glMatrixMode(GL_MODELVIEW)
        glPopMatrix()

        glDisable(GL_TEXTURE_2D)

    def is_coliding(self, obj1, obj2):
        colide_x = (obj1.position.x + obj1.width >= obj2.position.x - obj2.width and \
                    obj1.position.x + obj1.width <= obj2.position.x + obj2.width) or \
                   (obj2.position.x + obj2.width >= obj1.position.x - obj1.width and \
                    obj2.position.x + obj2.width <= obj1.position.x + obj1.width)

        colide_y = (obj1.position.y + obj1.height >= obj2.position.y - obj2.height and \
                    obj1.position.y + obj1.height <= obj2.position.y + obj2.height) or \
                   (obj2.position.y + obj2.height >= obj1.position.y - obj1.height and \
                    obj2.position.y + obj2.height <= obj1.position.y + obj1.height)

        return colide_x and colide_y

    def resurrection(self):
        self.ship.is_dead = False
        self.ship.position.x = randint(0, view_w)
        self.gl_scene.append(self.ship)

        return False

    def destroy_ship(self):
        self.ship.is_dead = True
        self.score_gain(-200)
        glib.timeout_add(4000, self.resurrection)

    def create_objects(self):

        if self.level == 1:
            if not randint(0, 1):
                asteroid = Asteroid(randint(0, view_w), view_h)
                if randint(0, 5) == 0:
                    asteroid.creto = True
                self.gl_scene.append(asteroid)
                self.asteroids_list.append(asteroid)

        if self.level == 2:
            if not randint(0, 1):
                enemy = Enemy(randint(0, view_w), view_h)
                self.gl_scene.append(enemy)
                self.asteroids_list.append(enemy)

        if self.level == 3:
            if not randint(0, 1):
                enemy = Enemy2(0, randint(view_h - view_h / 3, view_h - 25))
                self.gl_scene.append(enemy)
                self.asteroids_list.append(enemy)

        if self.level == 4:
            if not self.boss:
                self.boss = Boss(randint(0, view_w), randint(view_h - view_h / 3, view_h - 25))
                self.gl_scene.append(self.boss)
                self.asteroids_list.append(self.boss)
                self.boss_time = time()

        return True

    def run(self, parent_window=None):
        self.main_window.show()
        self.parent_window = parent_window
        if self.parent_window:
            self.main_window.set_transient_for(parent_window)
        else:
            gtk.main()

    def process_moving(self):
        if self.go_left and self.ship.position.x >= self.ship.width:
            self.ship.position.x -= step

        if self.go_right and self.ship.position.x <= view_w - self.ship.width:
            self.ship.position.x += step

        if self.space_press:
            self.bar.y = float(view_h) * min(1.0, (time() - self.loading_time) / SHOOT_TIME)
        else:
            self.bar.y = 0.0

        put_stars(view_w, view_h, self.gl_scene)

        if self.boss:
            if self.boss.hor_move == "right" and time() - self.boss_time > 5 and not randint(0, 5):
                self.boss.hor_move = "left"
                self.boss_time = time()

            if self.boss.hor_move == "left" and time() - self.boss_time > 5 and not randint(0, 5):
                self.boss.hor_move = "right"
                self.boss_time = time()

            if self.boss.ver_move == "up" and time() - self.boss_time > 5 and not randint(0, 5):
                self.boss.ver_move = "down"
                self.boss_time = time()

            if self.boss.ver_move == "down" and time() - self.boss_time > 5 and not randint(0, 5):
                self.boss.ver_move = "up"
                self.boss_time = time()

    def on_main_window_key_press_event(self, widget, event):
        if event.keyval == gtk.keysyms.Left:
            self.go_left = True

        if event.keyval == gtk.keysyms.Right:
            self.go_right = True

        if event.keyval == gtk.keysyms.space and not self.space_press:
            self.space_press = True
            self.loading_time = time()

        return True

    def shoot(self, x, y, enemy=False):
        if enemy:
            bullet = Laser(x, y, enemy=True)
        else:
            bullet = Laser(x, y)
        self.gl_scene.append(bullet)
        self.bullets_list.append(bullet)
        play_sound("tiro")

    def on_main_window_key_release_event(self, widget, event):
        if event.keyval == gtk.keysyms.Left:
            self.go_left = False

        if event.keyval == gtk.keysyms.Right:
            self.go_right = False

        if event.keyval == gtk.keysyms.space:
            self.space_press = False
            if time() - self.loading_time > SHOOT_TIME and not self.ship.is_dead:
                self.shoot(self.ship.position.x, self.ship.position.y)

        return True

    def score_gain(self, m):
        self.score_atual += m
        if self.score_atual < 0:
            self.score_atual = 0
        self.label_score.set_markup("<b>Score</b>: %05d" % self.score_atual)

    def score_reset(self):
        self.score_atual = 0
        self.label_score.set_markup("<b>Score</b>: %05d" % self.score_atual)

    def on_close(self, *args):
        if self.parent_window:
            self.main_window.hide()
            return True
        else:
            gtk.main_quit()
            return False


if __name__ == '__main__':
    game = Shooting()
    game.run()

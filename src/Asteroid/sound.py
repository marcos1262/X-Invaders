#!/usr/bin/env python
#-*- coding:utf-8 -*-
#
# usa gstreamer para tocar sons.
#
# verifique o programa gstreamer-properties para ver o device
# default de output. se for o pulseAudio, verifique o Sound Preferences
# do ubuntu pra ver se a aba Output está correta.
#


#import pygst
#pygst.require("0.10")


import gio
import gst


class Player:
    def __init__(self):
        self.nome = ""
        self.audio = gst.element_factory_make("playbin2")
        self.playing = False
        
        bus = self.audio.get_bus()
        bus.add_signal_watch()
        bus.connect( "message", self.internal_message )
    
    
    def play(self, arq):
        uri = gio.File( arq ).get_uri()
        self.audio.set_property( "uri", uri )
        self.audio.set_state( gst.STATE_PLAYING )
        self.playing = True
        # vai tocar durante o looping de processamento do gtk/glib

 
    def stop(self):
        self.audio.set_state( gst.STATE_NULL )
        self.playing = False

   
    def is_playing(self):
        return self.playing


    def internal_message(self, bus, message):
        if message.type == gst.MESSAGE_EOS:
            self.stop()
            
        elif message.type == gst.MESSAGE_ERROR:
            self.stop()
            #print "*** Erro de som: %s" % message.parse_error()



import os

players = []

def play_sound(nome):
    global players
    arq = os.path.join( os.path.dirname(__file__), "sounds", nome )
    
    # só atrela o '.wav' se o nome puro e simples do arquivo não for encontrado
    if not os.path.exists( arq ):
        arq += ".wav"
    else:
        print "Tocando arquivo <%s>..." % arq
    
    tocou_em_algum_player = False
    for pl in players:
        if not pl.is_playing():
            pl.nome = nome
            pl.play( arq )
            tocou_em_algum_player = True
            break
    
    if not tocou_em_algum_player:
        pl = Player()
        players.append( pl )
        pl.nome = nome
        pl.play( arq )
        #print "Criado novo player de som para tocar %s..." % nome


def is_playing(nome):
    global players
    for pl in players:
        if pl.is_playing() and pl.nome == nome:
            return True
    return False


def stop_playing(nome = None):
    global players
    for pl in players:
        if pl.is_playing():
            if nome == None or pl.nome == nome:
                pl.stop()


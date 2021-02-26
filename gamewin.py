"""
Modulo gamepref.
Apresenta a tela de vitoria do jogo.
"""

import math, os
import pygame
from pygame.locals import *
import game, gfx, snd, txt
import gameplay, gamemenu

#Nada emocionante, huh? =)
cheer = (
    'Congratulations!',
    ' ',
    'You won the game!!!',
    ' ',
)

#Fontes utilizadas para o desenho da mensagem
fonts = []

def load_game_resources():
    """
    Carregamento de recursos para criacao da tela
    final
    """
    global fonts
    fontname = 'stencil'
    fonts.append(txt.Font(fontname, 28))
    snd.preload('select_choose')

class GameWin:
    """
    Definicao da tela de vitoria.
    """
    def __init__(self, prevhandler):
        self.prevhandler = prevhandler
        self.done = 0
        self.top = gfx.rect.centery
        self.center = gfx.rect.centerx
        self.text = []
        self.time = 0.0
        font = fonts[0]
        for line in cheer:
            img, r = font.text((255, 255, 0), line, (self.center, self.top))
            self.top += 30
            self.text.append((img, r))

    def quit(self):
        r = gfx.surface.fill((0, 0, 0), gfx.surface.get_rect())
        gfx.dirty(r)    
        game.handler = self.prevhandler
        self.done = 1
        snd.play('select_choose')
        
    def input(self, i):
        if self.time > 30.0:
            self.quit()

    def event(self, e):
        pass

    def run(self):
        if self.done: return
        for line in self.text:
            img, r = line
            gfx.surface.blit(img, r)
            gfx.dirty(r)

        ratio = game.clockticks / 25
        speedadjust = max(ratio, 1.0)
        self.time += speedadjust

    def background(self, area):
        return gfx.surface.fill((0, 0, 0), area)
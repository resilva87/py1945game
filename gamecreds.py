"""
Modulo gamecreds.
Mostra os creditos no menu principal.
"""
import pygame
from pygame.locals import *
import game, gfx, snd, txt

#Definicao dos creditos
credits = (
    ('Developer', ('Renato Silva',)),
    ('Graphics', ('Ari Fieldman - SpriteLib',)),
    ('Beta Testers', ('Paulo Silla', 'Rafael Euclides')),
)

#Informacao de licenca do jogo
licenseinfo = ('This program is free software. You are encouraged to',
               'make copies and modify it, subject to the LGPL.',
               'See "lgpl.txt" file for details.')

fonts = []     #Fontes utilizadas neste menu
images = []    #Imagens utilizadas neste menu 

def load_game_resources():
    """
    Carregamento de recursos para criacao do menu de creditos.
    """
    global fonts, images
    fontname = 'stencil'
    fonts.append((txt.Font(fontname, 20), (255, 255, 0)))
    fonts.append((txt.Font(fontname, 30), (255, 255, 255)))
    
    font = txt.Font('stencil', 15)
    top = 560
    mid = 400
    for l in licenseinfo:
        t = font.text((50, 150, 150), l, (mid, top))
        top += t[1].height
        images.append(t)

    snd.preload('select_choose')


class GameCreds:
    """
    Definicao do menu de creditos
    """
    def __init__(self, prevhandler):
        """
        Parametros:
        prevhandler - handler previamente ativo do jogo.
        """
        self.prevhandler = prevhandler
        self.done = 0
        self.center = gfx.rect.centerx
        self.text = []
        self.credits = []
        self.area = Rect(130, 100, 550, 400)
        self.offset = 0
        for cred in credits:
            self.createtext(cred[0], 0)
            self.offset += 10
            for peop in cred[1]:
                self.createtext(peop, 1)
            self.offset += 30
        self.offset = 0.0
        self.oldoffsety = 0.0
        self.text.extend(images)
        self.first = 1


    def createtext(self, text, size):
        """
        Cria o texto de credito.
        Parametros:
        text - texto a ser escrito.
        size - indice da lista de fontes a ser utilizada.
        """
        f, c = fonts[size]
        t = f.text(c, text, (self.center, 0))
        t[1].top = self.offset
        self.offset = t[1].bottom - 5
        self.credits.append(t)

    def quit(self):
        """
        Funcao de saida do menu de creditos
        """
        gfx.dirty(self.background(gfx.rect))
        game.handler = self.prevhandler
        self.done = 1
        snd.play('select_choose')

    def input(self, event):
        """
        Detecta os eventos associados a este menu.
        Parametros:
        event - Evento detectado no loop principal do jogo.
        """
        if event.type == KEYUP: return
        self.quit()

    def event(self, e):
        pass

    def run(self):
        """
        Loop de execucao deste handler.
        """
        if self.first:
            gfx.dirty(gfx.rect)
            self.first = 0
        ratio = game.clockticks / 25
        speedadjust = max(ratio, 1.0)
        
        self.offset += speedadjust * 1.0
        offsety = self.area.bottom-self.offset
        
        #Obtem um retangulo com posicoes validas a partir do objeto Surface    
        oldclip = gfx.surface.get_clip()
        
        #Desenha o texto do credito e desloca para cima na tela.
        if not self.done:
            for cred, pos in self.text:
                gfx.surface.blit(cred, pos)
            gfx.surface.set_clip(self.area)
            for cred, pos in self.credits:
                r = pos.move(0, offsety)
                self.background(r)
                bottom = r.bottom
                gfx.surface.blit(cred, r)
            gfx.surface.set_clip(oldclip)
            gfx.dirty(self.area)

            if bottom < self.area.top:
                self.offset = 0.0
        else:
            for text in self.text:
                r = text[1]
                gfx.dirty(self.background(text[1]))

    def background(self, area):
        """
        Loop de desenho do background do menu de creditos.
        """
        return gfx.surface.fill((0, 0, 0), area)
    
"""
Modulo gameinit.
"""

import pygame, pygame.draw
from pygame.locals import *
import sys, threading
import game, gfx, snd, txt
import allmodules
import time

#Total de modulos ja carregado
load_total = 0
#Porcentagem do modulo atual ja carregado
load_current = 0

#Status final do carregamento
load_finished_status = 0
#Caso haja falha, armazena a mensagem de erro...
load_finished_message = ''
#O modulo que gerou um erro...
load_finished_module = ''
#E o tipo do erro
load_finished_type = ''

def loadresources():
    """
    Carregamento dos recursos de todos os modulos do jogo.
    """
    global load_total, load_current
    #Busca pela funcao load_game_resources nos modulos do jogo.
    hunt = 'load_game_resources'
    load_total = 0
    load_current = 0
    allmods = sys.modules.values()
    funcs = [(m.__name__, getattr(m, hunt)) for m in allmods if hasattr(m, hunt)]
    load_total = len(funcs)
    m = ''
    try:
        #Tenta carregar a funcao de cada modulo
        for m, f in funcs:
            if game.threadstop: break
            load_current += 1
            f()
    except:
        global load_finished_status, load_finished_message, load_finished_module, load_finished_type
        load_finished_message = str(sys.exc_value)
        load_finished_type = str(sys.exc_type) + ' in module ' + m
        load_finished_status = -1
        raise SystemError
    game.thread = None


class GameInit:
    """
    Definicao do handler de inicializacao do jogo.
    """
    def __init__(self, prevhandler):
        """
        Parametros:
        prevhandler - handler previamente ativo do jogo.
        """
        self.prevhandler = prevhandler
        font = txt.Font(None, 20)
        self.font = txt.Font(None, 22)
        self.rect = Rect(50, 450, 700, 22)
        self.text = font.render('Loading Resources...', 1, (250, 255, 255))
        self.img_powered = gfx.load('pygame_powered.gif')
        self.img_logo = gfx.load('1945.png')
        self.textrect = self.text.get_rect()
        self.textrect.center = self.rect.center
        self.lastcurrent = -1
        snd.play('startup')
        self.top = 120
        self.left = 100
        self.blocks = []
        self.starttime = pygame.time.get_ticks()
        #self.gatherinfo()
        self.handlederror = 0
        self.thread = threading.Thread(None, loadresources)
        game.threadstop = 0
        game.thread = self.thread
        self.thread.start()


    def gatherinfo(self):
        """
        Informa o usuario sobre as informacoes de seu sistema
        de video e som.
        """
        lines = []
        info = pygame.display.Info()
        lines.append('Current Video Driver: %s' % pygame.display.get_driver())
        lines.append('Video Mode is Accelerated: %s' % ('No', 'Yes')[info.hw])
        lines.append('Display Depth (Bits Per Pixel): %d' % info.bitsize)
        self.buildblock(lines)

        lines = []
        info = pygame.mixer.get_init()
        if info:
            lines.append('Sound Frequency: %d' % info[0])
            lines.append('Sound Quality: %d bits' % abs(info[1]))
            lines.append('Sound Channels: %s' % ('Mono', 'Stereo')[info[2]])
        else:
            lines.append('Sound: None')
        self.buildblock(lines)

    def input(self, event):
        """
        Detecta os eventos associados a este menu.
        Parametros:
        event - Evento detectado no loop principal do jogo.
        """
        if load_finished_status < 0:
            self.gotfinishinput = 1

    def event(self, event):
        if load_finished_status < 0:
            if event.type in (KEYDOWN, MOUSEBUTTONDOWN):
                self.gotfinishinput = 1

    def buildblock(self, text):
        """
        Constroi um bloco de texto como objeto Surface.
        Parametros:
        text - Texto a ser escrito.
        """
        imgs = []
        width = 0
        height = 0
        for line in text:
            img = self.font.render(line, 1, (255, 255, 255), (0, 0, 0))
            height += img.get_height()
            w = img.get_width()
            width = max(w, width)
            imgs.append(img)
        size = width+20, height+20
        if gfx.surface.get_bitsize() > 8:
            block = pygame.Surface(size)
        else:
            block = pygame.Surface(size, 0, 32)
        block.fill((0, 0, 0))
        block.fill((255, 255, 255), Rect(0, size[1]-2, size[0], 2))
        top = 10
        for i in imgs:
            pos = 10, top
            top += i.get_height()
            block.blit(i, pos)
        self.blocks.append((block, (self.left, self.top)))
        self.top += block.get_height() + 40
        self.gotfinishinput = 0

    def quit(self):
        """
        Funcao de saida da tela de apresentacao do jogo.
        """
        import gamemenu
        gfx.dirty(self.background(gfx.rect))
        for b in self.blocks:
            r = b[0].get_rect().move(b[1])
            gfx.dirty(self.background(r))

        if load_finished_status >= 0:
            game.handler = gamemenu.GameMenu(self.prevhandler)
        else:
            game.handler = self.prevhandler

    def run(self):
        """
        Loop de execucao deste handler.
        """
        if self.rect:
            self.background(self.rect)
            
        gfx.dirty(gfx.surface.blit(self.img_logo, (30, 25)))
        gfx.dirty(gfx.surface.blit(self.img_powered, (510, 490)))

        for b in self.blocks:
            gfx.dirty(gfx.surface.blit(*b))

        bar = Rect(self.rect)
        if load_total:
            bar.width = (float(load_current)/float(load_total)) * bar.width
            gfx.surface.fill((5, 50, 5), bar)
        r = Rect(self.rect.left, self.rect.bottom-2, self.rect.width, 2)
        gfx.surface.fill((20, 80, 30), r)
        gfx.surface.blit(self.text, self.textrect)
        gfx.dirty(self.rect)

        now = pygame.time.get_ticks()
        #Mantem a tela de apresentacao do jogo por 1 segundo
        if not self.thread.isAlive():
            if load_finished_status >= 0:
                if now-self.starttime > 1200:
                    self.quit()
            else:
                if not self.handlederror:
                    msg = ('Fatal Error Loading Resources', load_finished_type, load_finished_message, 'Press Any Key To Quit')
                    self.buildblock(msg)
                    self.handlederror = 1
                if self.gotfinishinput:
                    self.quit()

    def background(self, area):
        """
        Loop de desenho do background da tela de 
        apresentacao do jogo.
        """
        return gfx.surface.fill((0, 0, 0), area)

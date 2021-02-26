"""
Modulo gamefinish.
"""

import pygame
import gfx, game, snd

class GameFinish:
    """
    Definicao do handler de finalizacao do jogo.
    """
    def __init__(self, prevhandler):
        """
        Parametros:
        prevhandler - handler previamente ativo do jogo.
        """
        self.prevhandler = prevhandler
        self.ticks = 17
        self.started = 0

    def input(self, event):
        pass

    def event(self, e):
        pass

    def run(self):
        """
        Loop de execucao deste handler.
        """
        self.ticks -= 1
        #Seta o fadeout da musica do jogo
        if not self.started:
            self.started = 1
            if snd.music:
                snd.music.fadeout(15*game.clockticks)
        
        #No final, apaga todo o conteudo da tela
        if not self.ticks:
            gfx.surface.fill(0)
            pygame.display.update()
            pygame.time.delay(200)
            game.handler = self.prevhandler


    def background(self, area):
        """
        Loop de desenho do background da tela final.
        """
        return gfx.surface.fill((0, 0, 0), area)

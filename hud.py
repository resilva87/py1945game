"""
Modulo hud.

Exibe as informacoes de pontuacao, vida, armas, etc
ao jogador.
"""

import pygame
from pygame.locals import *
import game, gfx, txt

labelfont = None
valuefont = None

def load_game_resources():
    """
    Carregamento dos recursos para criacao do hud.
    """
    global labelfont, valuefont
    fontname = 'stencil'
    valuefont = (txt.Font(fontname, 15), (255, 255, 255))
    labelfont = (txt.Font(fontname, 15), (221, 92, 14))

class HUD:
    """
    Define o hud.
    """
    def __init__(self):
        
        self.drawsurface = gfx.surface 
        self.lastscore = 0
        self.lastlevel = 0
        self.lastgun = None
        self.lastlive = 0
        self.lastwave = 0
        
        #Configura as areas para labels e texto.
        self.labelgunarea = Rect(game.arena.left + 100, game.arena.bottom + 20, 60, 20)
        self.valuegunarea = Rect(game.arena.left + 170, game.arena.bottom + 20, 80, 20)
        
        self.labelscorearea  = Rect(game.arena.left + 95, game.arena.bottom + 50, 60, 20)
        self.valuescorearea  = Rect(game.arena.left + 165, game.arena.bottom + 50, 70, 20)
        
        self.labellivesarea  = Rect(game.arena.left + 390, game.arena.bottom + 20, 40, 20)
        self.valuelivesarea  = Rect(game.arena.left + 450, game.arena.bottom + 20, 50, 20)
        
        self.labelwavesarea  = Rect(game.arena.left + 295, game.arena.bottom + 50, 100, 30)
        self.valuewavesarea  = Rect(game.arena.left + 395, game.arena.bottom + 50, 60, 30)
               
    def drawlives(self, lives):
        """
        Desenha as vidas do jogador.
        
        Parametros:
            lives - numero de vidas do 
                    jogador a serem desenhadas
        """
        if lives < 0: lives = 0
        
        #Desenha o label de vidas.
        text = 'Life: '
        f, c = labelfont
        t = f.text(c, text, self.labellivesarea.topleft)
        self.drawsurface.blit(t[0], t[1])
        gfx.dirty(self.labellivesarea)
        
        #Desenha o status da vida.
        text = ' %02d ' % lives
        f, c = valuefont
        t = f.text(c, text, self.valuelivesarea.topleft)
        self.livescleanup()
        self.drawsurface.blit(t[0], t[1])
        gfx.dirty(self.valuelivesarea)

    def drawscore(self, score):
        """
        Desenha a pontuacao do jogador.
        
        Parametros:
            score - pontuacao do jogador a ser desenhada.
        """
        
        #Desenha o label de pontuacao
        text = 'Score: '
        f, c = labelfont
        t = f.text(c, text, self.labelscorearea.topleft)
        self.drawsurface.blit(t[0], t[1])
        gfx.dirty(self.labelscorearea)
        
        #Desenha a pontuacao
        text = ' %06d ' % score
        f, c = valuefont
        t = f.text(c, text, self.valuescorearea.topleft)
        self.scorecleanup()
        self.drawsurface.blit(t[0], t[1])
        gfx.dirty(self.valuescorearea)

    
    def drawgun(self, playergun): 
        """
        Desenha o nome da arma usada pelo jogador.
        
        Parametros:
            playergun - nome da arma usada pelo jogador.
        """
        
        #Desenha o label de status da arma
        text = 'Gun: '
        f, c = labelfont
        t = f.text(c, text, self.labelgunarea.topleft)
        self.drawsurface.blit(t[0], t[1])
        gfx.dirty(self.labelgunarea)
        
        #Desenha o nome da arma
        self.lastgun = playergun
        text = ' %20s ' % playergun
        f, c = valuefont
        t = f.text(c, text, self.valuegunarea.topleft)
        self.guncleanup()
        self.drawsurface.blit(t[0], t[1])
        gfx.dirty(self.valuegunarea)
    
    def drawwaves(self, wave):
        """
        Desenha o numero de waves ("levas" de inimigos)
        restantes para finalizar o nivel.
        
        Parametros:
            wave - numero de waves restantes.
        """
        
        #Desenha o label de waves restantes
        text = 'Waves Left: '
        f, c = labelfont
        t = f.text(c, text, self.labelwavesarea.topleft)
        self.drawsurface.blit(t[0], t[1])
        gfx.dirty(self.labelwavesarea)
        
        #Desenha a quantidade de waves restantes
        self.lastwave = wave
        text = ' %02d ' % self.lastwave
        f, c = valuefont
        t = f.text(c, text, self.valuewavesarea.topleft)
        self.wavescleanup()
        self.drawsurface.blit(t[0], t[1])
        gfx.dirty(self.valuewavesarea)
    
    def scorecleanup(self):
        """
        Limpa o valor da pontuacao anterior.
        """
        gfx.surface.fill((0, 0, 0), self.valuescorearea)
       
    def wavescleanup(self):
        """
        Limpa o valor da quantidade de waves restantes anterior.
        """
        gfx.surface.fill((0, 0, 0), self.valuewavesarea)
         
    def guncleanup(self):
        """
        Limpa o nome da arma anterior usada pelo jogador.
        """
        gfx.surface.fill((0, 0, 0), self.valuegunarea)

    def livescleanup(self):
        """
        Limpa a quantidade de vidas do jogador.
        """
        gfx.surface.fill((0, 0, 0), self.valuelivesarea)
                
    def drawlevel(self, level):
        """
        Desenha o nivel atual do jogo.
        
        Parametros:
            level - nivel atual do jogo.
        """
        dest = self.drawsurface
        offset = self.drawoffset
        if not fast:
            r = self.poslevel
            r2 = dest.blit(self.imghud1, r, r).move(offset)
        else:
            r2 = None
        if self.lastlevel != level:
            self.lastlevel = level
            self.imglevel = score.render(level)
            self.poslevel = self.imglevel.get_rect()
            self.poslevel.center = 50, 565
        r1 = dest.blit(self.imglevel, self.poslevel).move(offset)
        gfx.dirty2(r1, r2)
    
    def draw(self, player, wave):
        """
        Desenha todo o hud
        """
        self.drawscore(player.score)
        if player.nextgun: self.drawgun(player.nextgun.name)
        elif player.gun: self.drawgun(player.gun.name)
        self.drawlives(player.lives)
        self.drawwaves(wave)
        
        

        

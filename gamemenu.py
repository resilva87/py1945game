"""
Modulo gamemenu
Gerencia o menu principal do jogo.
"""

import pygame
from pygame.locals import *
import game, gameplay
import gfx, snd, txt
import gamecreds, gamepref

#Imagem de fundo
bg_image = None
#Imagem da seta de selecao de item do menu
select_image = None

class MenuItem:
    """
    Define um item do menu principal.
    """
    def __init__(self, imgname, handler):
        """
        Parametros:
        imgname - nome da imagem associada a este item de menu.
        handler - handler do jogo associado a este item de menu.
        """
        self.imgname = imgname
        self.handler = handler

    def init(self, pos):
        """
        Inicializa um item do menu em uma dada posicao.
        Parametros:
        pos - posicao do menu na tela principal.
        """
        self.img = gfx.load('menu_'+self.imgname+'.png')
        self.rect = self.img.get_rect().move(pos)

def preGameStart(prevhandler):
    """
    Funcao executa antes da inicializacao
    do jogo.
    """     
    return gameplay.GamePlay(prevhandler)

#Definicao do menu principal
menu = [
    MenuItem('play', preGameStart),
    MenuItem('credits', gamecreds.GameCreds),
    MenuItem('options', gamepref.GamePref),
    MenuItem('quit', None),
]

def load_game_resources():
    """
    Carregamento de recursos para criacao do menu.
    """
    global menu, images, bg_image, select_image
    images = []
    pos = [330, 340]
    #Seta a posicao de cada item do menu na tela
    for m in menu:
        m.init(pos)
        pos[1] += 40

    bg_image = gfx.load('1945.png')
    select_image = gfx.load('select.png')
    snd.preload('select_move', 'select_choose')


class GameMenu:
    """
    Define o menu principal
    """
    def __init__(self, prevhandler):
        """
        Parametros:
        prevhandler - handler previamente ativo do jogo.
        """
        self.prevhandler = prevhandler
        self.current = 0
        self.switchhandler = None
        self.logo = bg_image
        self.logorect = self.logo.get_rect().move(250, 95)
        self.logorectsmall = self.logorect.inflate(-2,-2)
        self.select = select_image
        self.last_selectrect = None
        self.selectrect = select_image.get_rect().move(310, 345)
        
        fnt = txt.Font(None, 18)
        self.version = fnt.text((255, 255, 255), 'Py1945 Version ' + game.version, (10, 580), 'topleft')

    def starting(self):
        """
        Funcao de abertura do menu: Carrega a musica principal e
        desenha o logo do jogo.
        """
        snd.playmusic('aster2_sw.xm')
        gfx.dirty(gfx.surface.blit(self.logo, self.logorect))

    def quit(self):
        """
        Funcao de saida do menu (do jogo).
        """
        self.current = len(menu)-1
        self.workbutton()

    def workbutton(self):
        """
        Clique do item do menu.
        """
        button = menu[self.current]
        if not button.handler:
            self.switchhandler = self.prevhandler
        else:
            self.switchhandler = button.handler

    def clearitem(self, item, dirty=0):
        """
        Limpa a area de desenho do item do menu.
        Parametros:
        item  - item do menu
        dirty - se houve atualizacao grafica do item do menu (necessario para atualizar a tela)
        """
        r = self.background(item.rect)
        if dirty:
            gfx.dirty(r)

    def clearoption(self):
        """
        Limpa a area de desenho da seta de selecao do menu.
        """
        r = self.background(self.selectrect)
        gfx.dirty(r)

    def drawitem(self, item, selected):
        """
        Desenha um item do menu.
        Parametros:
        item      - item do menu a desenhar.
        selected  - item esta selecionado.
        """
        if not selected:
            gfx.surface.blit(item.img, item.rect)
            gfx.dirty(item.rect)
        else:
            gfx.surface.blit(item.img, item.rect)
            gfx.dirty(item.rect)
            gfx.surface.blit(self.select, self.selectrect)
            self.last_selectrect = Rect(self.selectrect)
            gfx.dirty2(self.selectrect, self.last_selectrect)
            
    def input(self, event):
        """
        Detecta os eventos associados a este menu.
        Parametros:
        event - Evento detectado no loop principal do jogo.
        """
        if event.type == KEYUP: return
        if event.key == K_ESCAPE:
            snd.play('select_choose')
            self.quit()
        elif event.key == K_UP or event.key == K_LEFT:
            #Desloca a selecao para cima
            self.current = (self.current - 1)%len(menu)
            self.clearoption()
            self.selectrect.top = menu[self.current].rect.top + 5
            snd.play('select_move')
        elif event.key == K_DOWN or event.key == K_RIGHT:
            #Desloca a selecao para baixo
            self.current = (self.current + 1)%len(menu)
            self.clearoption()
            self.selectrect.top = menu[self.current].rect.top + 5 
            snd.play('select_move')
        elif event.key == K_RETURN:
            #Realiza a acao associada ao item do menu
            self.workbutton()
            snd.play('select_choose')

    def event(self, e):
        pass

    def run(self):
        """
        Loop sobre o menu do jogo.
        """
        #Limpa todos os itens do menu
        for m in menu:
            self.clearitem(m)
        #Limpa a selecao     
        self.clearoption()
        gfx.dirty(gfx.surface.blit(*self.version))
        
        select = menu[self.current]
        #Desenha os itens nao selecionados.
        for m in [m for m in menu if m is not select]:
            self.drawitem(m, 0)
        #Desenha o item selecionado.
        self.drawitem(select, 1)

        if self.switchhandler == self.prevhandler:
                game.handler = self.prevhandler
        elif self.switchhandler:
            #Modificacao do handler do jogo.
            game.handler = self.switchhandler(self)
            self.switchhandler = None
            gfx.dirty(self.background(self.version[1]))
            gfx.dirty(gfx.surface.fill((0, 0, 0)))

    def background(self, area):
        """
        Loop de desenho do background do menu principal.
        """
        fullr = gfx.surface.fill((0, 0, 0), area)
        if area.colliderect(self.logorectsmall):
            r = area.move(-self.logorect.left, -self.logorect.top)
            return gfx.surface.blit(self.logo, area, r)
        return fullr


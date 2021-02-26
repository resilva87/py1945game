"""
Modulo gamepref.
Gerencia o menu de preferencias do jogador.
"""
import string, math
import pygame
from pygame.locals import *
import game
import gfx, snd, txt
import gameplay

Prefs = {
"music": ("Off", "Low", "Normal"),
"volume": ("Off", "Low", "Normal"),
}

def load_prefs():
    """
    Carrega as preferencias antigas do jogador
    (salvas no arquivo prefs)
    """
    prefs = {}
    try:
        filename = game.make_dataname('prefs')
        for line in open(filename).readlines():
            name, val = [s.strip() for s in line.split('=')]
            setattr(game, name, int(val))
    except (IOError, OSError, KeyError):
        pass


def save_prefs():
    """
    Salva as preferencias do jogador.
    """
    try:
        filename = game.make_dataname('prefs')
        f = open(filename, 'w')
        for p in Prefs.keys():
            val = getattr(game, p)
            f.write("%s = %d\n" % (p, int(val)))
        f.close()
    except (IOError, OSError), msg:
        pass


images = []
namefont = None
valuefont = None


def load_game_resources():
    """
    Carregamento de recursos para criacao do menu de preferencias.
    """
    global images, namefont, valuefont

    img = gfx.load('select.png')
    images.append((img, img.get_rect()))

    namefont = txt.Font('stencil', 26)
    valuefont = txt.Font('stencil', 20)

    snd.preload('select_choose', 'select_move', 'delete')

class GamePref:
    """
    Definicao do menu de preferencias
    """
    def __init__(self, prevhandler):
        """
        Parametros:
        prevhandler - handler previamente ativo do jogo.
        """
        self.prevhandler = prevhandler
        self.images = images
        self.prefs = []
        for n,v in Prefs.items():
            self.prefs.append((n,v))
        self.prefs.append(("", ("Return To Menu",)))
        
        self.done = 0
        self.aborted = 0
        
        self.linesize = 60
        self.gamelist = []
        self.buildlabels()
        self.buildlist()
        
        self.current = [0, 0]
        self.selectmovex = 40
        self.selectmovey = 16
        step = 0
        
        self.moveto(self.gamelist[0][0][1])

    def starting(self):
        """
        Funcao executada quando o usuario
        entra neste menu.
        """
        #snd.playmusic('gamestart.wav')
        pass

    def moveto(self, pos):
        """
        Desloca a seta de selecao para a posicao dada.
        Parametros: 
        pos - posicao de deslocamento da seta de selecao.
        """
        self.selectpos = pos[0], pos[1]


    def input(self, event):
        """
        Detecta os eventos associados a este menu.
        Parametros:
        event - Evento detectado no loop principal do jogo.
        """
        if event.type == KEYUP: return
        if self.done:
            return
        if event.key == K_ESCAPE:
            self.aborted = 1
            self.done = 1
            self.current[0] = -1
            self.clearlist()
            self.moveto((2, 2))
            snd.play('select_choose')
        
        #Detecta a selecao de uma opcao do menu    
        if event.key == K_RETURN:
            return self.pressed()
        
        if event.key in (K_DOWN, K_UP, K_LEFT, K_RIGHT):
            #Seleciona um item do menu...
            if event.key == K_DOWN:
                self.current[0] = (self.current[0]+1) % len(self.gamelist)
                self.current[1] = min(self.current[1], len(self.gamelist[self.current[0]])-1)
            elif event.key == K_UP:
                self.current[0] = (self.current[0]-1) % len(self.gamelist)
                self.current[1] = min(self.current[1], len(self.gamelist[self.current[0]])-1)
            elif event.key == K_LEFT:
                self.current[1] = (self.current[1]-1) % len(self.gamelist[self.current[0]])
            else:
                self.current[1] = (self.current[1]+1) % len(self.gamelist[self.current[0]])
            snd.play('select_move')
            x = self.gamelist[self.current[0]][self.current[1]][1].left
            y = self.gamelist[self.current[0]][self.current[1]][1].top
            
            #e desloca a seta de selecao para a posicao
            #selecionada.
            self.moveto((x, y))

    def event(self, e):
        pass

    def run(self):
        """
        Loop de execucao deste handler.
        """
        
        r = self.background(self.images[0][1])
        gfx.dirty(r)
        
        self.moveselect()

        #Desenha as opcoes do menu
        if not self.done:
            self.drawlist()
            for img in self.images:
                r = gfx.surface.blit(img[0], img[1])
                gfx.dirty(r)
        else:
            #Realiza a troca de handler do jogo
            game.handler = self.prevhandler
            self.clearlist()
            for img in self.images[1:]:
                r = self.background(img[1])
                gfx.dirty(r)

    def background(self, area):
        """
        Loop de desenho do background do menu de creditos.
        """
        return gfx.surface.fill((0, 0, 0), area)

    def buildlabels(self):
        """
        Constroi os labels do menu de preferencias
        """
        clr = 160, 200, 250
        x, y = 250, 170
        for pref, vals in self.prefs:
            pref = pref.capitalize()
            imgpos = namefont.text(clr, pref, (x,y), "midright")
            images.append(imgpos)
            y += self.linesize

    def buildlist(self):
        """
        Constroi a lista de opcoes do menu de
        preferencias
        """
        clr = 220, 230, 240
        clr2 = 140, 150, 160
        offsetx, offsety = 290, 170
        self.clearlist()
        self.gamelist = []
        for pref, vals in self.prefs:
            x = offsetx
            y = offsety
            if not pref:
                y += 30
            allvals = []
            if pref:
                realval = getattr(game, pref)
            else:
                realval = -1
            i = 0
            for val in vals:
                if i == realval:
                    c = clr
                else:
                    c = clr2
                imgpos = valuefont.text(c, val, (x,y), "midleft")
                allvals.append(imgpos)
                x = imgpos[1].right + 60
                i += 1
            self.gamelist.append(allvals)
            offsety += self.linesize

    def clearlist(self):
        """
        Apaga a lista de preferencias 
        (atualizacao grafica do menu)
        """
        for vals in self.gamelist:
            for v in vals:
                gfx.dirty(self.background(v[1]))

    def drawlist(self):
        """
        Desenha as opcoes do menu
        """
        for vals in self.gamelist:
            for v in vals:
                gfx.dirty(gfx.surface.blit(*v))

    def moveselect(self):
        """
        Move a seta de selecao para a posicao
        escolhida pelo usuario
        """
        pos = list(self.images[0][1].topright)
        if pos[0] + self.selectmovex < self.selectpos[0]:
            pos[0] += self.selectmovex
        elif pos[0] < self.selectpos[0]:
            pos[0] = self.selectpos[0]

        if pos[0] - self.selectmovex > self.selectpos[0]:
            pos[0] -= self.selectmovex
        elif pos[0] > self.selectpos[0]:
            pos[0] = self.selectpos[0]

        if pos[1] + self.selectmovey < self.selectpos[1]:
            pos[1] += self.selectmovey
        elif pos[1] < self.selectpos[1]:
            pos[1] = self.selectpos[1]

        if pos[1] - self.selectmovey > self.selectpos[1]:
            pos[1] -= self.selectmovey
        elif pos[1] > self.selectpos[1]:
            pos[1] = self.selectpos[1]
        
        pos[0] -= 10        
        self.images[0][1].topright = pos

    def pressed(self):
        """
        Realiza a acao de pressionamento de
        uma opcao do menu, aplicando a prefe
        rencia escolhida pelo usuario
        """
        pref, vals = self.prefs[self.current[0]]
        if not pref:
            snd.play('select_choose')
            self.done = 1
        else:
            val = self.current[1]
            oldval = getattr(game, pref)
            if oldval == val:
                return
            setattr(game, pref, val)
            self.buildlist()
            if hasattr(self, "do_" + pref):
                getattr(self, "do_" + pref)()
            snd.play('select_choose')

    def do_music(self):
        """
        Callback para atualizacao 
        das preferencias de som
        """
        snd.tweakmusicvolume()


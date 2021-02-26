"""
Modulo map.

Gerencia o mapa do jogo.
"""
import pygame
from pygame.locals import *
import gfx
from math import fabs
from random import randint, seed
from game import arena, get_resource

#Tiles.
images = []

#Fundo do mapa.
blue_background = pygame.surface.Surface((arena.width, arena.height))

#Semente para geracao aleatoria.
seed(0)

def random_pos():
    """
    Gera uma posicao aleatoria para os tiles do mapa.
    """
    y =  randint(65, 195)
    return y

def load_game_resources():
    """
    Carregamento dos recursos para criacao do mapa.
    """
    global images, blue_background
    blue_background.fill((0, 67, 171))
    
    images.append(gfx.load('island.png', ckey=None))
    images.append(gfx.load('terrain.png', ckey=None))
    images.append(gfx.load('volcano.png', ckey=None))
    
class Tile:
    """
    Definicao de um tile do mapa.
    """
    def __init__(self, image, x, y):
        """
        Construtor da classe Tile
        
        Parametro:
            image - Imagem do tile.
            x - coordenada x do tile (dentro da area do mapa)
            y - coordenada y do tile (acima do topo do mapa, para dar o efeito de scrolling).
        """
        self.image = image
        self.dead = 0
        self.imagerect = self.image.get_rect()
        self.x = x
        self.y = y
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.lastrect = None
        
    def erase(self, background):
        """
        Apaga o tile para sua atualizacao.
        """
        gfx.dirty(self.lastrect)
        
    def tick(self):
        """
        "Tick" do tile, para sua atualizacao
        """
        self.lastrect = Rect(self.rect)        
        x, y = self.rect.center
        
        #Atualiza a coordenada y do tile no mapa.
        y += 1
        
        self.rect.center = (x, y) 
        
        #Testa a passagem do tile para fora do mapa.    
        if self.rect.bottom > arena.bottom: 
            bottom1 = self.rect.bottom
            bottom2 = arena.bottom
            diff = bottom1 - bottom2
            self.rect.height -= fabs(diff)
            if self.rect.height <= 0:
              self.dead = 1
        
            
        
class TiledMap:
    """
    Definicao do mapa de tiles
    """
    def __init__(self, name):
        """
        Construtor da classe TiledMap.
        
        Parametros:
            name - nome do mapa, utilizado para carrega-lo do arquivo.
        """
        self.rect = Rect(arena.top, arena.left, arena.width, arena.height)
        self.lastrect = None
        self.dead = False
        self.tiles = []
        self.tilesrect = []
        self.load(name)
        
    def load(self, name):
        """
        Carrega o mapa do arquivo.
        
        Parametros:
            name - nome do mapa a ser carregado.
        """
        try:
            f = open(get_resource(name+'.txt'))
        except:
            print 'Could not load map %s.' % name
            raise SystemError
        else:
            for line in f:
                if line[0] == '#': continue
                elif line.strip():
                    tname, tx, ty = line.split(';')
                    img = gfx.load(tname+'.png')
                    tx = int(tx)
                    ty = int(ty) 
                    if tx >= arena.width: tx = arena.width 
                    self.tiles.append(Tile(img, tx, ty))
            f.close()
            
    def draw(self):
        """
        Desenha o mapa.
        """
        
        #Desenha cada tile ativo.
        for tile in self.tiles:
            if tile.dead:
                self.tiles.remove(tile)
            else:
                blue_background.fill((0, 67, 171), tile.lastrect)
                blue_background.blit(tile.image, tile.rect)
                
        gfx.surface.blit(blue_background, self.rect)
        gfx.dirty2(self.rect, self.lastrect)
        self.lastrect = Rect(self.rect)
                               
    def erase(self, background):
        """
        Limpa uma area do mapa.
        """
        if self.lastrect:
            background(self.lastrect)
            gfx.dirty(self.lastrect)
        else:
            background(self.rect)
            gfx.dirty(self.rect)
            
    def tick(self):
        """
        "Tick" de todo os tiles ativos do mapa.
        """
        [tile.tick() for tile in self.tiles]
        
    def cleanup(self):
        """
        Limpa o mapa.
        """            
        blue_background.fill((0, 67, 171))
        gfx.surface.blit(blue_background, self.rect)
        gfx.dirty2(self.rect, self.lastrect)
        self.lastrect = Rect(self.rect)
        
            
            
            
        

            
            
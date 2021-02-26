#simple enemy class

import pygame, pygame.image
from pygame.locals import *
from math import fabs

import gfx, game, random

rng = random.Random()

dict_images = {}

def load_game_resources():
    #load shot graphics
    global dict_images
    for name in ('ball', 'double', 'single2'):
        dict_images[name] = [gfx.load(name+'_fire.png')]



class Shot:
    def __init__(self, name, move=[0, 0], speed=0, dmg=1):
        #print 'SHOT CREATED'
        self.move = move
        self.name = name
        self.images = dict_images[self.name]
        self.numframes = len(self.images)
        self.frame = 0
        self.lastrect = None
        self.rect = None
        self.dead = 0
        self.pos = None
        self.active = 0
        self.speed = speed
        self.dmg = dmg

    def start(self, pos):
        self.rect = self.images[0].get_rect()
        self.rect.center = pos
        self.pos = list(self.rect.topleft)
        self.active = 1
        
    def prep(self, screen):
        pass

    def erase(self, background):
        if self.lastrect:
            background(self.lastrect)
            if self.dead:
                gfx.dirty(self.lastrect)
                self.lastrect = None

    def draw(self, gfx):
        if not self.active: 
            return
        if not self.dead:            
            if type(self.images) == list:
                frame = int(self.frame) % self.numframes
                gfx.surface.blit(self.images[frame], self.rect)
            else:
                gfx.surface.blit(self.images, self.rect)
                
            gfx.dirty2(self.rect, self.lastrect)
            self.lastrect = Rect(self.rect)

    def tick(self, speedadjust = 1.0):
        if not self.active: 
            return
        self.frame += speedadjust * self.speed
        self.pos[0] += self.move[0] * speedadjust * self.speed
        self.pos[1] += self.move[1] * speedadjust * self.speed
        
        self.rect.center = tuple(self.pos)
        
        if self.rect:
            #Shot outside arena, consider it dead
            if self.rect.bottom >= game.arena.bottom \
                or self.rect.top < game.arena.top: self.dead = 1
            
            if self.rect.right > game.arena.right \
                or self.rect.left < game.arena.left: self.dead = 1

        #if self.dead: print 'SHOT IS DEAD '
        #else: print 'SHOT NOT DEAD' 


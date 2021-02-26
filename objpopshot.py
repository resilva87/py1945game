#box class

import random
import pygame
from pygame.locals import *
import game, gfx


small_explode_images = []
big_explode_images = []
explode_frames = 6

def load_game_resources():
    global small_explode_images, big_explode_images
    small_explode_images = gfx.animstrip(gfx.load('explosion_small.png'), width=33)
    big_explode_images = gfx.animstrip(gfx.load('explosion_big.png'), width=66)

class PopShot:
    def __init__(self, pos, size='small'):
        self.clocks = 0
        self.life = explode_frames
        if size == 'small':
             self.images = small_explode_images
        else:
            self.images = big_explode_images
        self.lenimages = len(self.images)
        self.rect = self.images[0].get_rect()
        self.rect.center = pos
        self.dead = 0

    def erase(self, background):
        r = background(self.rect)
        if self.dead:
            gfx.dirty(r)

    def draw(self, gfx):
        img = self.images[self.clocks%self.lenimages]
        r = gfx.surface.blit(img, self.rect)
        gfx.dirty(r)

    def tick(self, speedadjust):
        self.clocks += 1
        if self.clocks == self.life:
            self.dead = 1

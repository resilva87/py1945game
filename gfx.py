"""graphics class, helps everyone to draw
Copyright Peter Shinners from SolarWolf.
"""

import sys, pygame, pygame.image
from pygame.locals import *

import game, map

#the accessible screen surface and size
surface = None
rect = Rect(0, 0, 0, 0)

#the accessable dirty rectangles
dirtyrects = []

tile_image = None


def initialize(size):
    global surface, rect, tile_image
    try:
        flags = 0
        depth = pygame.display.mode_ok(size, flags, 16)
        surface = pygame.display.set_mode(size, flags, depth)
        rect = surface.get_rect()

        pygame.mouse.set_visible(0)
        
        tile_image = load(game.get_resource('1945.bmp'))

    except pygame.error, msg:
        print 'Error msg: ', msg
        raise pygame.error, 'Cannot Initialize Graphics: %s' % str(msg)
        

def dirty(rect):
    dirtyrects.append(rect)


def dirty2(rect1, rect2):
    if not rect2:
        dirtyrects.append(rect1)
    elif rect.colliderect(rect2):
        dirtyrects.append(rect1.union(rect2))
    else:
        dirtyrects.append(rect1)
        dirtyrects.append(rect2)


def update():
    global dirtyrects
    pygame.display.update(dirtyrects)
    del dirtyrects[:]

def optimize(img):
    if not surface.get_flags() & HWSURFACE:
        clear = img.get_colorkey()
        if clear:
            img.set_colorkey(clear, RLEACCEL)
    return img.convert()

def load(name, ckey=(0, 67, 171)):
    img = load_raw(name)
    
    img.set_alpha(None)
    img.set_colorkey(ckey)
    return img.convert()

def load_raw(name):
    img = pygame.image.load(game.get_resource(name))
    return img

def animstrip(img, width=0, ckey=None):
    if not width:
        width = img.get_height()
    size = width, img.get_height()
    images = []
    
    origalpha = img.get_alpha()
    
    origckey = img.get_colorkey()
    
    img.set_colorkey(None)
    
    img.set_alpha(None)
    for x in range(0, img.get_width(), width):
        i = pygame.Surface(size)
        i.blit(img, (0, 0), ((x, 0), size))
        if origalpha:
            i.set_colorkey((0,0,0))
        elif origckey:
            i.set_colorkey(origckey)
        images.append(optimize(i))
    img.set_alpha(origalpha)
    img.set_colorkey(origckey)
    return images
    
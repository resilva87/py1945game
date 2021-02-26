#player ship class


import pygame
from pygame.locals import *
import game, gfx
from math import fabs
import objshot
import objgun
from random import randint
from copy import copy

shieldbg = None
bulletbg = None

player_images = []
greenstalker_images = []
bluestalker_images = []
graystalker_images = []
yellowstalker_images = []
lightgreenstalker_images = []
war_airplaneimages = []
gunner_images = []
nogunfighter_images = []

inv_yellowstalker_images = []
inv_greenstalker_images = []
inv_bluestalker_images = []

striker_image = None
corsair_image = None
fighter_image = None

small_fighters_speed = 2.1
small_fighters_life = 21
small_fighters_shotspeed = 5
small_fighters_gun = objgun.LightGun()
inv_small_fighters_gun = objgun.InvLightGun()

war_airplanes_speed = 1.8
war_airplanes_life = 42
war_airplanes_shotspeed = 8
war_airplanes_leftgun = objgun.LeftRedBallGun()
war_airplanes_rightgun = objgun.RightRedBallGun()

corsair_speed = 3.5
corsair_life = 31.5
corsair_shotspeed = 10.5
corsair_gun = objgun.LightGun()

gunner_speed = 2
gunner_life = 25
gunner_shotspeed = 10 
gunner_gun = objgun.LightGun()

nogunfighter_speed = 2.4
nogunfighter_life = 14

striker_speed = 3.2
striker_life = 25
striker_shotspeed = 9
striker_gun = objgun.LightGun()

fighter_speed = 1.2
fighter_life = 38.5
fighter_shotspeed = 9
fighter_gun = objgun.ArchGun()

guns = [war_airplanes_leftgun, war_airplanes_rightgun]

def load_game_resources():
    global corsair_image
    global player_images, greenstalker_images, bluestalker_images, graystalker_images
    global yellowstalker_images, lightgreenstalker_images, war_airplaneimages
    global gunner_images, nogunfighter_images, inv_bluestalker_images, inv_greenstalker_images
    global inv_yellowstalker_images, striker_image, fighter_image
    
    #load airplanes graphics
    for img in gfx.animstrip(gfx.load('player.png'), width=59, ckey=(0, 0, 0)):
        player_images.append(img)
        
    for img in gfx.animstrip(gfx.load('war_airplanes.png'), width=93, ckey=(0, 67, 171)):
        war_airplaneimages.append(img)
    
    for img in gfx.animstrip(gfx.load('greenstalker.png'), width=31, ckey=(0, 67, 171)):
        i = pygame.transform.rotate(img, 90)
        j = pygame.transform.rotate(img, -90)
        greenstalker_images.append(i)
        inv_greenstalker_images.append(j)
        
    for img in gfx.animstrip(gfx.load('bluestalker.png'), width=31, ckey=(0, 67, 171)):
        i = pygame.transform.rotate(img, 90)
        j = pygame.transform.rotate(img, -90)
        bluestalker_images.append(i)
        inv_bluestalker_images.append(j)

    for img in gfx.animstrip(gfx.load('graystalker.png'), width=31, ckey=(0, 67, 171)):
        img = pygame.transform.rotate(img, 90)
        graystalker_images.append(img)

    for img in gfx.animstrip(gfx.load('yellowstalker.png'), width=31, ckey=(0, 67, 171)):
        i = pygame.transform.rotate(img, 90)
        j = pygame.transform.rotate(img, -90)
        yellowstalker_images.append(i)
        inv_yellowstalker_images.append(j)

    for img in gfx.animstrip(gfx.load('lightgreenstalker.png'), width=31, ckey=(0, 67, 171)):
        img = pygame.transform.rotate(img, 90)
        lightgreenstalker_images.append(img)
    
    for img in gfx.animstrip(gfx.load('gunner.png'), width=60, ckey=(0, 67, 171)):
        gunner_images.append(img)
        
    for img in gfx.animstrip(gfx.load('nogunfighter.png'), width=33, ckey=(0, 67, 171)):
        nogunfighter_images.append(img) 
                      
    striker_image = gfx.load('striker.png')
    corsair_image = gfx.load('corsair.png')
    fighter_image = gfx.load('fighter.png')
    
    
class Airplane:
    def __init__(self, stamina, speed, name= None):
        self.move = [0, 0]
        self.unmoved = 1
        self.turbo = 0
        self.image = 0
        self.frame = 0.0
        self.rect = None
        self.lastrect = None
        self.dead = 0
        self.active = 0
        self.speed = speed
        self.pos = None
        self.shield = 0
        self.stamina  = stamina
        self.gun = None
        self.name = name
        self.lastshottick = 0
        
    def start(self, pos):
        self.rect.topleft = pos
        self.pos = list(self.rect.topleft)
        self.unmoved = 1
        self.active = 1
        self.dead = 0

    def erase(self, background):
        if self.lastrect:
            background(self.lastrect)
        if self.dead:
            gfx.dirty(self.lastrect)

    def draw(self, gfx): pass


    def tick(self, speedadjust = 1.0):  pass
                
    def fire(self):
        gun = None
        if not self.dead:
            if hasattr(self, 'nextgun') and self.nextgun:
                gun = self.nextgun
        if not gun:
                gun = self.gun
        gun.fire()
        
    def shotinfo(self):
        gun = None
        if hasattr(self, 'nextgun') and self.nextgun:
            gun = self.nextgun
        if gun:
            if gun.bullet == 0: 
                return None 
            r = list(self.rect.center)
 
            shots = gun.shot(r, self.shotspeed)
            return shots
        elif self.gun:
            if self.gun.bullet == 0: 
                return None 
            r = list(self.rect.center)
            shots = self.gun.shot(r, self.shotspeed)
            return shots
        else: return None
            

class PlayerAirplane(Airplane):
    def __init__(self, stamina, speed, img):
        Airplane.__init__(self, stamina, speed, name='Player')
        self.image = img
        self.nextgun = None
        self.rect = self.image[0].get_rect()
        self.drawsurface = gfx.surface 
        self.shotspeed = game.player_shotspeed
        self.score = 0
        self.lives = game.start_lives
        self.active = 1
        
    def start(self, pos):
        Airplane.start(self, pos)
        self.gun = objgun.SingleMG()
        
    def draw(self, gfx):
        if not self.active:
            r = self.drawsurface.fill((0, 67, 171), self.rect)
            gfx.dirty(r)
        else:
            if not self.dead:
                img = None
                frame = int(self.frame) % 3
                if self.shield:
                    img = shieldbg[self.shield-1]
                else:
                    img = self.image[frame]                
                self.drawsurface.blit(img, self.rect)
                gfx.dirty2(self.rect, self.lastrect)
                self.lastrect = Rect(self.rect)

    def tick(self, speedadjust=1.0):
        self.frame += speedadjust
        self.lastshottick += 1
        if self.shield == 1:
            self.speed = int(self.speed * speedadjust * 1.3)
        else:
            self.speed = int(self.speed * speedadjust)

        if self.rect.top < game.arena.top:
            self.rect.top = game.arena.top
            self.move[1] = 0
        elif self.rect.bottom > game.arena.bottom:
            self.rect.bottom = game.arena.bottom
            self.move[1] = 0
        if self.rect.left < game.arena.left:
            self.rect.left = game.arena.left
            self.move[0] = 0
        elif self.rect.right > game.arena.right:
            self.rect.right = game.arena.right
            self.move[0] = 0
            
    def cmd_right(self): self._move(1 * self.speed, 0)
        
    def cmd_left(self): self._move(-1 * self.speed, 0)
        
    def cmd_up(self): self._move(0, -1 * self.speed)

    def cmd_down(self): self._move(0, 1 * self.speed)
                            
    def _move(self, dx, dy):
        r = list(self.rect.center)
        r[0] += dx
        r[1] += dy
        self.rect.center = tuple(r)
        
    def fire(self):
        if self.lastshottick <= 3: return
        Airplane.fire(self)
        self.lastshottick = 0
        
 
class EnemyAirplane(Airplane):
    
    def __init__(self, life, img, speedx=1, speedy=1, gun=None, 
                 shotspeed=1, direction=None, shottick=0, size='small'):
        Airplane.__init__(self, life, speedy)
        self.image = img
        self.frame = 0.0
        if type(img) == list:
            self.rect = self.image[0].get_rect()
        else:
            self.rect = self.image.get_rect()
        self.drawsurface = gfx.surface 
        self.direction = direction or [0, 1]
        self.lastshottick = 0
        self.gun = gun
        self.size = size
        self.shotspeed = shotspeed
        self.shottick = shottick or game.enemy_fire
        self.speedx = speedx
        self.speedy = speedy
        
    def start(self, pos):
        self.pos = pos
        self.rect.move(self.pos)
   
    def think(self):
        if self.gun:
            self.isfiring = not self.gun.finishedfiring
            if self.isfiring: self.fire()
            if self.lastshottick <= game.enemy_fire: return
            self.fire() 
            self.lastshottick = 0
                    
    def tick(self, speedadjust=1.0):
        Airplane.tick(self, speedadjust)
        self.frame += speedadjust
        self.lastshottick += 1
        self.speedx = int(self.speedx * speedadjust)
        self.speedy = int(self.speedy * speedadjust)
         
        self.pos = [self.pos[0] + self.direction[0]*self.speedx, self.pos[1] + self.direction[1]*self.speedy]
        self.rect.topleft = tuple(self.pos)
        
        s = self.direction[1]
        diff = 0 
        
        if s > 0:
            if self.rect.bottom > game.arena.bottom:
                bottom1 = self.rect.bottom
                bottom2 = game.arena.bottom
                diff = bottom1 - bottom2
            
            self.rect.height -= fabs(diff)
            if self.rect.height <= 0:
                  self.dead = 1
        else:
             if self.rect.top < game.arena.top:
                top1 = self.rect.top
                top2 = game.arena.top
                diff = top1 - top2
            
             self.rect.height -= fabs(diff)
             if self.rect.height <= 0:
                  self.dead = 1
        
        diff = 0
        if self.rect.right > game.arena.right:
            right1 = self.rect.right
            right2 = game.arena.right
            diff = right1 - right2
                            
        elif self.rect.left < game.arena.left: 
            left1 = self.rect.left
            left2 = game.arena.left
            diff = left1 - left2
            
        self.rect.width -= fabs(diff)
        if self.rect.width <= 0:
             self.dead = 1
             

    def draw(self, gfx):
        if not self.dead:
            img = None
            if type(self.image) == list:
                frame = int(self.frame) % len(self.image)
                img = self.image[frame] 
            else:
                img = self.image
                
            self.drawsurface.blit(img, self.rect)
            gfx.dirty2(self.rect, self.lastrect)
            self.lastrect = Rect(self.rect)
            

class SmallEnemyAirplane(EnemyAirplane):
    
    def __init__(self, images, direction=[0,1]):
        EnemyAirplane.__init__(self, small_fighters_life, images,
                                     speedy=small_fighters_speed , gun=copy(small_fighters_gun), 
                                     shotspeed=small_fighters_shotspeed, direction=direction)

class WarEnemyAirplane(EnemyAirplane):
    
    def __init__(self, i):
        EnemyAirplane.__init__(self, war_airplanes_life, war_airplaneimages, 
                                    speedy=war_airplanes_speed, gun=copy(guns[i]), 
                                    shotspeed=war_airplanes_shotspeed, direction=[0, 1], size='big')

class BlueSmallEnemyAirplane(SmallEnemyAirplane):
    
    def __init__(self):
        SmallEnemyAirplane.__init__(self, bluestalker_images)
    
class GreenSmallEnemyAirplane(SmallEnemyAirplane):
    
    def __init__(self):
        SmallEnemyAirplane.__init__(self, greenstalker_images)
        
class LightGreenSmallEnemyAirplane(SmallEnemyAirplane):
    
    def __init__(self):
        SmallEnemyAirplane.__init__(self, lightgreenstalker_images)
        
class YellowSmallEnemyAirplane(SmallEnemyAirplane):
    
    def __init__(self):
        SmallEnemyAirplane.__init__(self, yellowstalker_images)
        
class GraySmallEnemyAirplane(SmallEnemyAirplane):
    
    def __init__(self):
        SmallEnemyAirplane.__init__(self, graystalker_images)
        
class InvertedBlueSmallEnemyAirplane(SmallEnemyAirplane):
    
    def __init__(self):
        SmallEnemyAirplane.__init__(self, inv_bluestalker_images, direction=[0, -1])
    
class InvertedGreenSmallEnemyAirplane(SmallEnemyAirplane):
    
    def __init__(self):
        SmallEnemyAirplane.__init__(self, inv_greenstalker_images, direction=[0, -1])
        
class InvertedYellowSmallEnemyAirplane(SmallEnemyAirplane):
    
    def __init__(self):
        SmallEnemyAirplane.__init__(self, inv_yellowstalker_images, direction=[0, -1])
        
class CorsairEnemyAirplane(EnemyAirplane):
    
    def __init__(self):
        EnemyAirplane.__init__(self, corsair_life, corsair_image, speedy=corsair_speed,
                                     gun=copy(corsair_gun), shotspeed=corsair_shotspeed,
                                     direction=[0, 1])
        
class GunnerEnemyAirplane(EnemyAirplane):
    
    def __init__(self):
        EnemyAirplane.__init__(self, gunner_life, gunner_images, speedx=gunner_speed/1.3,
                                     speedy=gunner_speed, gun=copy(gunner_gun), 
                                     shotspeed=gunner_shotspeed, direction=[0.9, 1], shottick=15, size='big')
        
class FighterEnemyAirplane(EnemyAirplane):
    
    def __init__(self):
        EnemyAirplane.__init__(self, fighter_life, fighter_image, speedy=fighter_speed,
                                 gun=copy(fighter_gun), shotspeed=fighter_shotspeed,
                                 direction=[0, 1])
        
class GunlessFighterEnemyAirplane(EnemyAirplane):
    
    def __init__(self, direction):
        EnemyAirplane.__init__(self, nogunfighter_life, nogunfighter_images,
                                     speedx=nogunfighter_speed/1.35, speedy=nogunfighter_speed, 
                                     direction=direction)
        
        



    
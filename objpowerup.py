#powerup class

import random
import pygame
from pygame.locals import *
from math import fabs
import game, gfx, snd, objpopshot, objgun

images = []
symbols = []

def load_game_resources():
    global images
    for i in range(1, 6):
        images.append(gfx.load('powerup'+str(i)+'.png'))
    snd.preload('select_choose')


class Powerup:
    
    def __init__(self, effect):
        self.effect = effect
        self.symbol = self.effect.symbol
        self.image =  images[self.symbol]
        self.speed = game.powerupspeed
        r = random.randint(0, 1200)
        self.pos = [
                    random.randint(90, game.arena.width-100),
                    -1 * random.randint(90, game.arena.height/3)
                    ]
        self.rect = self.image.get_rect()
        self.rect.move_ip(-20, -20)
        self.time = 0
        self.dead = 0

    def erase(self, background):
        r = background(self.rect)
        gfx.dirty(r)

    def draw(self, gfx):
        img = self.image
        r = gfx.surface.blit(img, self.rect)
        gfx.dirty(r)

    def tick(self, speedadjust):
        self.pos[1] = (self.pos[1] + speedadjust*self.speed)
        self.rect.topleft = self.pos
        self.rect.move_ip(-20, -20)
        self.time += speedadjust
        if self.time >= game.poweruptime:
            self.dead = 1
        elif self.rect.bottom > game.arena.bottom:
            bottom1 = self.rect.bottom
            bottom2 = game.arena.bottom
            diff = bottom1 - bottom2
            self.rect.height -= fabs(diff)
            if self.rect.height <= 0: self.dead = 1 
             
    def extendtime(self):
        self.time -= 20.0

    def effect(self):
        return self.effect

class PowerupEffect:
    runtime = 100.0

    def __init__(self):
        self.time = 0.0
        self.state = game.handler
        self.dead = 0
        self.name = ''
        self.start()

    def tick(self, speedadjust):
        self.time += speedadjust
        if self.time >= self.runtime:
            self.dead = 1
        pass

    def start(self):
        pass

    def end(self):
        pass

class GattingGunPowerup(PowerupEffect):
    runtime = 500.0
    symbol = 4
        
    def start(self):
        snd.play('powerup')
        #self.effect = objgun.GattingGun()
        
    
    def end(self):
        pass

class DefensiveGunPowerup(PowerupEffect):
    runtime = 500.0
    symbol = 1
    

    def start(self):
        snd.play('powerup')
        self.effect = objgun.DefensiveGun()
        
    def end(self):
        pass
    
class TwinGunPowerup(PowerupEffect):
    runtime = 500.0
    symbol = 3    
        
    def start(self):
        snd.play('powerup')
        self.effect = objgun.TwinGun()
        
    def end(self):
        pass
    
class ExtraLifePowerup(PowerupEffect):
    runtime = 250.0
    symbol = 4
    
    def __init__(self):
        PowerupEffect.__init__(self)
        self.name = 'life'
        
    def start(self):
        self.effect = random.randint(5, 25)
        
    def end(self):
        pass
    
class Shield(PowerupEffect):
    "Shield"
    runtime = 200.0
    #symbol = 1
    def start(self):
        #snd.play('select_choose')
        self.player = self.state.player
        snd.play('flop')
        self.player.shield = 1

    def tick(self, speedadjust):
        PowerupEffect.tick(self, speedadjust)
        if self.time >= 120.0:
            self.player.shield = 2
        elif self.time >= 145.0:
            self.player.shield = 3
        elif self.time >= 175.0:
            self.player.shield = 4
            
    def end(self):
        self.state.player.shield = 0

#class PopShots(PowerupEffect):
#    "Shot Blocker"
#    runtime = 1.0
#    symbol = 2
#    def start(self):
#        snd.play('whip')
#        for s in self.state.shotobjs:
#            s.dead = 1
#            self.state.popobjs.append(objpopshot.PopShot(s.rect.center))


#class ExtraLife(PowerupEffect):
#    "Extra Life"
#    runtime = 1.0
#    symbol = 3
#    def start(self):
#        snd.play('vaauw', 1.0)
#        self.state.lives_left += 1
#        self.state.hud.drawlives(self.state.lives_left)
#
#class SlowMotion(PowerupEffect):
#    "Bullet Time"
#    runtime = 140.0
#    symbol = 4
#    def start(self):
#        self.player = self.state.player
#        snd.play('gameover')
#        game.speedmult += 2
#        self.ending = 0
#        self.player.bullet = 1
#
#    def tick(self, speedadjust):
#        PowerupEffect.tick(self, speedadjust)
#        if not self.ending and self.time >= 120.0:
#            self.ending = 1
#            game.speedmult -= 1
#        if self.time <= 100.0:
#            self.player.bullet = (int(self.time * 0.8) % 4) + 1
#
#    def end(self):
#        self.player.bullet = 0
#        if self.ending:
#            game.speedmult -= 1
#        else:
#            game.speedmult -= 2

#class Combustion(PowerupEffect):
#    "Combustion"
#    runtime = 1.0
#    symbol = 5
#    def start(self):
#        snd.play('explode', 1.0, 350)
#        aliveguards = []
#        for g in self.state.guardobjs:
#            if not g.killed:
#                aliveguards.append(g)
#        if aliveguards:
#            g = random.choice(aliveguards)
#            g.killed = 1
#            explode = objexplode.Explode(g.rect.center)
#            self.state.staticobjs.append(explode)
#            #argh, force a cleanup
#            self.state.background(g.lastrect)
#            gfx.dirty(g.lastrect)


#Effects = [ExtraLevelTime, PopShots, Shield,
#           SlowMotion, Combustion, ExtraLife,
#           PopShots, Shield, ExtraLife, Combustion,
#           PopShots, SlowMotion]
#GattingGunPowerup#,
Effects = [DefensiveGunPowerup, ExtraLifePowerup,
           TwinGunPowerup]

def newpowerup(levelnum):
    choices = Effects
    effect = random.choice(choices)
    return Powerup(effect)

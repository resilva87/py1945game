"""
Modulo objgun.

Define as armas do jogador e dos inimigos.
"""
import objshot
from functools import partial
from copy import copy
import snd
  
class Gun:
    """
    A Generic Gun
    """
    SINGLE_SHOT_CLASS = partial(objshot.Shot, 'single2', dmg=2.5)
    TWIN_SHOT_CLASS = partial(objshot.Shot, 'double', dmg=7.5)
    BALL_SHOT_CLASS = partial(objshot.Shot, 'ball', dmg=2.5)
    SPREAD_SHOT_CLASS = partial(objshot.Shot, 'ball',dmg=4.5)
    REDBALL_SHOT_CLASS = partial(objshot.Shot, 'ball', dmg=6)
    
    def __init__(self, name):
        self.bullet = 0
        self.name = name
        self.currentshot = 0
        self.shotx = self.shoty = []
        self.queueshotmovs = []
        self.queueshots = []
        self.i = 0
        self.delaytick = 0
        self.finishedfiring = False
        
    def fire(self):
        self.bullet += 1
        self.finishedfiring = False
        if not self.queueshots:
            self.queueshots = self.associatedshots[:]
        if not self.queueshotmovs:
            self.queueshotmovs = self.shotsmovement[:]
        self.currentshot = (self.currentshot + 1) % len(self.shotsmovement)
        if hasattr(self, 'shotdx'):
            if not self.shotx:
                self.shotx = self.shotdx[:]
        if hasattr(self, 'shotdy'):
            if not self.shoty:
                self.shoty = self.shotdy[:]            
        
    def shot(self, pos, speed=1):
            self.bullet -= 1
            s = None
            shot = None
            if self.delaytick < self.delay:
                self.delaytick += 0.1
                return None
            self.delaytick = 0.0
            pos = list(pos)
            shots = []
            if self.queueshots:
                if isinstance(self.queueshots[0], list):
                    k = self.queueshots.pop(0)
                    for s in k:
                        p = None
                        if self.queueshotmovs:
                            p = self.queueshotmovs.pop(0)
                        x = y = None
                        if self.shotx:
                            x = self.shotx.pop(0)
                        if self.shoty:
                            y = self.shoty.pop(0)
                        if x:
                            pos[0] += x
                        if y:
                            pos[1] += y
                        shot = s(move=p, speed=speed)
                        shot.start(pos)
                        shots.append(shot)
                else:
                    s = self.queueshots.pop(0)
                    p = None
                    if self.queueshotmovs:
                        p = self.queueshotmovs.pop(0)
                    x = y = None
                    if self.shotx:
                        x = self.shotx.pop(0)
                    if self.shoty:
                        y = self.shoty.pop(0)
                    if x:
                        pos[0] += x
                    if y:
                        pos[1] += y
                
                shot = s(move=p, speed=speed)
                shot.start(pos)
                shots.append(shot)
            if not self.queueshots: 
                    self.finishedfiring = True
            return shots
   
class SingleMG(Gun):
    def __init__(self):
        Gun.__init__(self, 'Single MG')
        self.associatedshots =  [Gun.SINGLE_SHOT_CLASS]   
        self.shotsmovement = [[0, -1]]
        self.shotdy = [-42]
        self.delay = 0.1
        self.sound = 'singleshot'

class TailGun(Gun):
    def __init__(self):
        Gun.__init__(self, 'Tail Gun')
        self.associatedshots = [Gun.SINGLE_SHOT_CLASS, Gun.BALL_SHOT_CLASS]
        self.shotsmovement = [[0, -1], [0, 1]]
        self.sound = 'singleshot'
        
class TwinGun(Gun):
    def __init__(self):
        Gun.__init__(self, 'Twin Gun')
        self.associatedshots = [Gun.TWIN_SHOT_CLASS]
        self.shotdy = [-42]
        self.shotsmovement = [[0, -1]]
        self.delay = 0.1
        self.sound = 'twinshot'
        
class SpreadGun(Gun):
    def __init__(self):
        Gun.__init__(self, 'Spread Gun')
        self.associatedshots = [[Gun.SPREAD_SHOT_CLASS, Gun.SPREAD_SHOT_CLASS, \
                                Gun.SPREAD_SHOT_CLASS, Gun.SPREAD_SHOT_CLASS, \
                                Gun.SPREAD_SHOT_CLASS]]
        self.shotsmovement = [[-0.6, -1], [-0.4, -1], [0.0, -1], [0.4, -1], [0.6, -1]]
        self.shotdx = [-20, -10, 0, 10, 20]
        self.shotdy = [-42, -42, -42, -42, -42]  
        self.sound = 'spreadshot' 
         
class ArchGun(Gun):
    def __init__(self):
        Gun.__init__(self, 'Arch Gun')
        self.associatedshots = [Gun.SPREAD_SHOT_CLASS, Gun.SPREAD_SHOT_CLASS, \
                                Gun.SPREAD_SHOT_CLASS, Gun.SPREAD_SHOT_CLASS, \
                                Gun.SPREAD_SHOT_CLASS]
        self.shotsmovement = [[-1, 1], [-0.6, 1], [0.0, 1], [0.6, 1], [1, 1]]
        self.shotdx = [-50, -10, 0, 10, 50]
        self.shotdy = [34, 36, 38, 36, 34]
        self.delay = 0.1
        
class InvSpreadGun(Gun):
    def __init__(self):
        Gun.__init__(self, 'Inv Spread Gun')
        self.associatedshots = [Gun.SPREAD_SHOT_CLASS, Gun.SPREAD_SHOT_CLASS, \
                                Gun.SPREAD_SHOT_CLASS, Gun.SPREAD_SHOT_CLASS, \
                                Gun.SPREAD_SHOT_CLASS]
        self.shotsmovement = [[-0.6, 1], [-0.4, 1], [0.0, 1], [0.4, 1], [0.6, 1]]
        self.shotdx = [-20, -10, 0, 10, 20]
        self.delay = 0.1
        
class LightGun(Gun):
    def __init__(self):
        Gun.__init__(self, 'Light Gun')
        self.associatedshots = [Gun.BALL_SHOT_CLASS]
        self.shotsmovement = [[0, 1]]
        self.shotdy = [33]
        self.delay = 1.7

class InvLightGun(Gun):
    def __init__(self):
        Gun.__init__(self, 'Inverted Light Gun')
        self.associatedshots = [Gun.BALL_SHOT_CLASS]
        self.shotsmovement = [[0, -1]]
        self.shotdy = [-33]
        self.delay = 1.7
        
class DefensiveGun(Gun):
    def __init__(self):
        Gun.__init__(self, 'Defensive Gun')
        self.associatedshots = [[Gun.TWIN_SHOT_CLASS, Gun.BALL_SHOT_CLASS, \
                                Gun.BALL_SHOT_CLASS, Gun.BALL_SHOT_CLASS]]
        self.shotsmovement = [[0, -1], [0, 1], [-1, 0], [1, 0]]
        self.shotdy = [21, -21, 0, 0]
        self.shotdx = [7.5, 0, -31, 31]
        self.delay = 0.1
        self.sound = 'defensiveshot'
        
class LeftRedBallGun(Gun):
    def __init__(self):
        Gun.__init__(self, 'Red Ball Gun')
        self.associatedshots = [Gun.REDBALL_SHOT_CLASS, Gun.REDBALL_SHOT_CLASS, \
                                Gun.REDBALL_SHOT_CLASS, Gun.REDBALL_SHOT_CLASS, \
                                Gun.REDBALL_SHOT_CLASS, Gun.REDBALL_SHOT_CLASS]
        self.shotsmovement = [[0, 1], [0.1, 1], [0.23, 1], [0.29, 1], [0.34, 1], [0.41, 1]]
        self.shotdx = [0, 1, 2, 3, 4, 5]
        self.shotdy = [40, 40, 40, 40, 40, 40]
        self.delay = 0.3

class RightRedBallGun(Gun):
    def __init__(self):
        Gun.__init__(self, 'Red Ball Gun')
        self.associatedshots = [Gun.REDBALL_SHOT_CLASS, Gun.REDBALL_SHOT_CLASS, \
                                Gun.REDBALL_SHOT_CLASS, Gun.REDBALL_SHOT_CLASS, \
                                Gun.REDBALL_SHOT_CLASS, Gun.REDBALL_SHOT_CLASS]
        self.shotsmovement = [[0, 1], [-0.1, 1], [-0.23, 1], [-0.29, 1], [-0.34, 1], [-0.41, 1]]
        self.shotsmovement.reverse()
        self.shotdx = [0, 1, 2, 3, 4, 5]
        self.shotdy = [40, 40, 40, 40, 40, 40]
        self.delay = 0.3

class EnemySpreadGun(Gun):
    def __init__(self):
        Gun.__init__(self, 'Enemy Spread Gun')
        self.associatedshots = [Gun.SPREAD_SHOT_CLASS, Gun.SPREAD_SHOT_CLASS, \
                                Gun.SPREAD_SHOT_CLASS, Gun.SPREAD_SHOT_CLASS, \
                                Gun.SPREAD_SHOT_CLASS]
        self.shotsmovement = [[-0.6, 1], [-0.4, 1], [0.0, 1], [0.4, 1], [0.6, 1]]
        self.shotdx = [-20, -10, 0, 10, 20]

"""
Modulo levels.

TODO:
Refatorar as constantes e metodos de criacao dos waves
para classes de inimigos.
"""
import game
import pygame
from wave_manager import Wave
import objairplane
from game import arena, get_resource
from random import randint
import objgun

initialized = 0
file2wave = []

def init(name):
    global file2wave
    initialized = 1
    f = None
    try:
        f = open(get_resource(name+'.txt'))
    except:
        print 'Could not open waves mapping file: %s.' % name
        raise SystemError
    else:
        for line in f:
            line = line.strip()
            if line:
                if line[0] == '#': continue
                else:  file2wave.append(line)
 
def makewave0(): return None, None
                
def makewave1():
    pos = []
    enemies = []
    base_pos = [150, arena.top - 350]
    
    for i in range(3):
        enemies.append(objairplane.BlueSmallEnemyAirplane())
        pos.append([base_pos[0] + 150 * i, base_pos[1]])
       
    return Wave(enemies), tuple(pos)


def makewave2():
    pos = []
    enemies = []
    base_pos = [300, arena.top - 50]
    
    for i in range(4):
        enemies.append(objairplane.GreenSmallEnemyAirplane())
        pos.append([base_pos[0] - 30 * i, base_pos[1] - 30 * i])
       
    return Wave(enemies), tuple(pos)

def makewave3():
    pos = []
    enemies = []
    base_pos = [100, arena.top - 50*7]
    
    for i in range(4):
        enemies.append(objairplane.LightGreenSmallEnemyAirplane())
        pos.append([base_pos[0] + 30 * i, base_pos[1] + 50 * i])
       
    return Wave(enemies), tuple(pos)

def makewave4():
    waves = []
    pos = []
    enemies = []
    base_pos = [300, arena.top - 50*7]
    
    for i in range(4):
        enemies.append(objairplane.YellowSmallEnemyAirplane())
        pos.append([base_pos[0] + 30 * i, base_pos[1] + 50 * i])
       
    return Wave(enemies), tuple(pos)

def makewave5():
    waves = []
    pos = []
    enemies = []
    base_pos = [500, arena.top - 50]
    
    for i in range(4):
        enemies.append(objairplane.GraySmallEnemyAirplane())
        pos.append([base_pos[0] + 30 * i, base_pos[1] - 50 * i])
       
    return Wave(enemies), tuple(pos)

def makewave6():
    pos = []
    enemies = []
    base_pos = [100, arena.top - 50*7]
    
    for i in range(2):
            enemies.append(objairplane.WarEnemyAirplane(i))
            pos.append([base_pos[0] + 400 * i, base_pos[1]])
       
    return Wave(enemies), tuple(pos)

def makewave7():
    pos = []
    enemies = []
    
    for i in range(3):
        enemies.append(objairplane.InvertedBlueSmallEnemyAirplane())
        pos.append([140*i+260, arena.bottom+60])
    
    return Wave(enemies), tuple(pos)

def makewave8():
    pos = []
    enemies = []
    
    for i in range(3):
        enemies.append(objairplane.InvertedYellowSmallEnemyAirplane())
        pos.append([200*i, arena.bottom+60])
    
    return Wave(enemies), tuple(pos)

def makewave9():    
    pos = []
    enemies = []
    
    for i in range(3):
        enemies.append(objairplane.InvertedGreenSmallEnemyAirplane())
        pos.append([200*i, arena.bottom+60])
    
    return Wave(enemies), tuple(pos)

def makewave10():
    pos = []
    enemies = []
    
    for i in range(2):
        enemies.append(objairplane.CorsairEnemyAirplane())
        pos.append([300*i+180, arena.top - 80])
    
    return Wave(enemies), tuple(pos)

def makewave11():
    pos = []
    enemies = []
    base_pos = [185, -50]
    
    for i in range(2):
        enemies.append(objairplane.GunnerEnemyAirplane())    
        pos.append([base_pos[0] + 120*i , base_pos[1]])
        
    return Wave(enemies), tuple(pos)

def makewave12():
    pos = []
    enemies = []
    
    enemies.append(objairplane.FighterEnemyAirplane())
    pos.append([arena.width/2-45, -80])
    
    return Wave(enemies), tuple(pos)
    
def makewave13():
    pos = []
    enemies = []
    base_pos = [arena.width-190, -100]
    
    print 'making wave 13'
    
    for i in range(4):
        enemies.append(objairplane.GunlessFighterEnemyAirplane(direction=[-1, 1]))
        pos.append([base_pos[0] + 45*i, base_pos[1]])

    return Wave(enemies), tuple(pos)

def makewave14():
    pos = []
    enemies = []
    base_pos = [190, -100]
    
    for i in range(4):
        enemies.append(objairplane.GunlessFighterEnemyAirplane(direction=[1, 1]))
        pos.append([base_pos[0] + 45*i, base_pos[1]])

    return Wave(enemies), tuple(pos)

def makewave15():
    pos = []
    enemies = []
    base_pos = [500, arena.top - 1000]
    
    for i in range(4):
        enemies.append(objairplane.GreenSmallEnemyAirplane())
        pos.append([base_pos[0] + 30 * i, base_pos[1] - 30 * i])
       
    return Wave(enemies), tuple(pos)
        
def make():
    global file2wave
    if file2wave == []:
        return makewave0()
    wavetype = file2wave.pop(0)
    try:
        return globals()['makewave'+wavetype]()
    except Exception, e:
        print 'Exception in makewave function: ', str(e)
        #raise SystemError
    
def maxwavesperlevel():
    global file2wave
    j = 0
    for wave in file2wave:
        wave = wave.strip()
        if wave and wave <> '0': j+= 1
    return j
    
def maxlevels():
    return 2


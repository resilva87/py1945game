"""
Modulo gameplay
Gerencia toda atualizacao do jogo, entrada do usuario, controle
dos inimigos, etc.
"""

import pygame
from pygame.locals import *
import random

import game, gfx, snd
import objshot
import objpopshot, objtext
import objpowerup
import objairplane
import levels
import hud
import map
import txt

#Do SolarWolf
Songs = [('arg.xm', 1.0), ('h2.ogg', 0.6)]

getready_images = []
quit_images = []
statekeys = {}
levelupfont = None
levelupcolors = []

def load_game_resources():
    """
    Carregamento de recursos para o jogo.
    Imagens de finalizacao e loading, alem de sons,
    sao pre-inicializados aqui.
    """
    global getready_images, statekeys, quit_images, font
    global levelupcolors
    
    getready_images.append(gfx.load('getready1.png'))
    getready_images.append(gfx.load('getready2.png'))
    quit_images.append(gfx.load('gameover1.png'))
    quit_images.append(gfx.load('gameover2.png'))
    
    snd.preload('gameover', 'startlife', 'levelskip', 'explode')
    snd.preload('boxhot', 'levelfinish', 'shoot', 'whip', 'klank2')
    snd.preload('spring', 'flop')
    
    font = txt.Font('stencil', 16)
    levelupcolors.append((255, 255, 0))
    levelupcolors.append((255, 0, 255))
    
    statekeys = {}.fromkeys([K_LEFT, K_RIGHT, K_UP, K_DOWN, K_ESCAPE, K_s], False)
    
class GamePlay:
    """
    Classe que gerencia o fluxo do jogo.
    """
    def __init__(self, prevhandler):
        self.startlevel = 1
        self.ticks = 0
        self.levelnum = -1
        self.gamewon = 0
        self.donegetready = 0
        self.waitforactivation = 0
        self.donelevelup = 0
        self.getreadyimage = 0
        self.player = objairplane.PlayerAirplane(35, 5, objairplane.player_images)
        self.prevhandler = prevhandler
        self.staticobjs = []
        self.doneplayerdie = 0
        self.baddyshotobjs = []
        self.playershotobjs = []
        self.powerupobjs = []
        self.popobjs = []
        self.smokeobjs = []
        self.asteroidobjs = []
        self.waves = 0
        self.donequit = 0
        self.explodetick = 0
        self.ptick = 0
        self.quitimage = 0
        self.pos = game.arena.width/2, game.arena.height-20
        self.curwave = []
        self.map = None
        self.objlists = [self.baddyshotobjs, self.playershotobjs, self.popobjs,
                         self.smokeobjs, self.powerupobjs, self.asteroidobjs,
                         self.staticobjs]
        self.hud = hud.HUD()
        self.lastwavecreated = 0
        self.levelchanged = 0
        self.state = ''
        self.statetick = self.dummyfunc
        self.lives_left = game.start_lives
        self.powerupcount = 0.0
        self.numdeaths = 0
        self.lasttick = pygame.time.get_ticks()
        self.wavetick = 0
        self.speedadjust = 1.0
        self.startmusic = 1
        self.song = ''
        self.songtime = 0

        self.changestate('getready')

        self.bgfill = gfx.surface.fill

    def starting(self):
        """
        Funcao de pre-inicializacao do jogo.
        """
        if self.startmusic:
            self.startmusic = 0
            self.song = random.choice(Songs)
            snd.playmusic(*self.song)
            self.songtime = pygame.time.get_ticks()
        gfx.dirty(self.background(gfx.rect))

    def invis_cleanup(self):
        """
        Limpa a area "invisivel", que nao esta situada
        na arena de jogo.
        """
        r = self.bgfill(0, (0, 0, game.arena.right, game.arena.top+5))
        gfx.dirty(r)
        r = self.bgfill(0, (0, game.arena.bottom, game.arena.right, game.size[1]))
        gfx.dirty(r)
        r = self.bgfill(0, (game.arena.right-5, 0, 
                            game.size[0] - game.arena.right, game.size[1]))
        gfx.dirty(r)
        r = self.bgfill(0, (0, 0, 
                            game.arena.left, game.size[1]))
        gfx.dirty(r)
        
    def cleanup(self):
        """
        Limpa toda a area do jogo, quando deve-se finalizar o jogo
        ou voltar para a tela de opcoes.
        """
        r = self.bgfill(0, (0, 0, game.size[0], game.size[1]))
        gfx.dirty(r) 
           
    def gamewin(self):
        """
        Gerencia a vitoria do jogador, basicamente muda
        seu estado.
        """
        self.gamewon = 1
        self.changestate('gameover')

    def changestate(self, state):
        """
        Implementacao da maquina de estados do jogo.
        A classe gerencia os diversos estados em que o jogador pode
        se encontrar, e executa cada um destes fluxos.
        
        Parametros:
            state - o estado a qual a maquina deve executar.
        """
        getattr(self, self.state+'_end', self.dummyfunc)()
        self.state = state
        getattr(self, state+'_start', self.dummyfunc)()
        self.statetick = getattr(self, state+'_tick')
        
    #Apenas para o metodo getattr
    def dummyfunc(self): pass

    def userquit(self):
        """
        Metodo de saida do jogo.
        """
        self.cleanup()
        if self.state == 'gameover': return
        if self.lives_left and self.player.active:
            self.lives_left = 0
            self.changestate('playerquit')
        else:
            self.changestate('gameover')

    def input(self, event):
        """
        Gerencia a entrada do usuario durante o jogo.
        
        Parametros:
            event - o evento de entrada detectado.
        """
        if self.levelchanged: return
        if event.key in statekeys:
            statekeys[event.key] = (event.type == KEYDOWN)
        
    def dumpstatekeys(self):
        """
        Dump do estado das teclas que controlam o jogo, apenas
        para debug.
        """
        if not game.DEBUG: return
        for key, state in statekeys.items():
            print 'Key ',pygame.key.name(key), 'is ', state
            
    def event(self, e): pass

    def run(self):
        """
        Controla o fluxo do jogo, executando o 
        "tick" deste.
        """
        if game.handler is not self: 
            return
        ratio = game.clockticks / 25
        self.speedadjust = max(ratio, 1.0)
        if game.speedmult >= 2:
            self.speedadjust *= 0.5
        elif game.speedmult:
            self.speedadjust *= 0.75
        self.statetick()

    #Se a tela de jogo perdeu ou ganhou o foco,
    #executa os metodos abaixo.
    def gotfocus(self):
        pass
    
    def lostfocus(self): pass  

    def runobjects(self, objects):
        """
        Atualiza os objetos do jogo.
        
        Parametros:
            objects - objetos do jogo a serem atualizados.
        """
        G, B, S = gfx, self.background, self.speedadjust

        #Atualiza os objetos de powerup
        for o in self.powerupobjs:
            if o.dead:
                self.powerupobjs.remove(o)
                        
        #Atualiza todas as listas de objetos, executando
        #os "ticks" respectivos de cada objeto.
        for l in objects:
            for o in l[:]:
                o.erase(B)
                o.tick(S)
                if o.dead:
                    o.erase(B)
                    l.remove(o)  
        
        #Atualiza o mapa.      
        if self.map:
            self.map.tick()
            self.map.draw()

        #Desenha todos os objetos da lista.
        for l in objects:
            for o in l:
                o.draw(G)
        
        #Atualiza e desenha todos os objetos
        #da wave de inimigos.        
        if self.curwave:
            [wave.tick(S) for wave in self.curwave]
            [wave.draw(G) for wave in self.curwave]
        
        #Limpa as areas invisiveis, evitando tracos
        #de elementos do jogo em areas nao visiveis.
        self.invis_cleanup()
        
        #Desenha o hud com informacoes do jogo.
        self.hud.draw(self.player, self.waves)
           
    def background(self, area):
        """
        Limpa o background.
        
        Parametros:
            area - area do background a ser limpa.
        """
        return self.bgfill(0, area)

    def check_keys_state(self):
        """
        Muda o estado das teclas que controlam 
        a aeronave do joador.
        """
        if self.levelchanged: return
        if statekeys[K_ESCAPE]: self.userquit()
        if statekeys[K_LEFT]: self.player.cmd_left()
        if statekeys[K_RIGHT]: self.player.cmd_right()
        if statekeys[K_UP]: self.player.cmd_up()
        if statekeys[K_DOWN]: self.player.cmd_down()
        if statekeys[K_s]: self.player.fire()
        

#==============================================================================
#                   IMPLEMENTACAO DA MAQUINA DE ESTADO DO JOGO
#==============================================================================

#normal play
    def normal_start(self):
        self.clocks = 0

    def normal_tick(self):
        
        self.wavetick += 1
        
        #Sem inimigos, fim do nivel.
        if self.waves == 0:
            self.changestate('levelend')
        
        #Atualiza os inimigos.
        for wave in self.curwave:
            if wave.dead():
                self.waves -= 1
                self.curwave.remove(wave)
        
        #Cria mais uma wave de inimigo e atualiza
        #a lista de inimigos atuais.
        if self.wavetick > game.wavetime:
            wave, init_pos = levels.make()
            if wave <> None: 
                wave.start(init_pos)
                self.curwave.append(wave)
            self.wavetick = 0
            #Atualiza a data de criacao de um wave
            self.lastwavecreated = game.clockticks
        
        #Verifica a entrada do jogador e atualiza sua posicao        
        self.check_keys_state() 
        self.pos = self.player.rect.center 
        
        #Adiciona um powerup caso seja hora.
        self.powerupcount += 0.3
        if self.powerupcount >= game.poweruptime and random.randint(0, 2000) in range(600, 700):
            self.powerupcount = 0.0
            p = objpowerup.newpowerup(self.levelnum)
            self.powerupobjs.append(p)
            snd.play('spring', 0.6)
         
        #
        # Acoes do jogador/maquina
        #     
        
        #Verifica se um dos inimigos atirou.
        #Caso tenha atirado, adiciona a lista de tiros dos inimigos.
        if self.curwave:
            for wave in self.curwave:
                for baddy in wave.enemies:
                    baddy.think()
                    shots = baddy.shotinfo()
                    if shots:
                        self.baddyshotobjs.extend(shots)
                                
        #Verifica se o jogador atirou.
        #Caso tenha, adiciona a lista de tiros do jogador.
        shots = self.player.shotinfo()
        if shots:
            self.playershotobjs.extend(shots)
            snd.play(self.player.gun.sound, 1.0)
        
        #
        # Testa colisao entre jogador e inimigos
        #
        
        self.check_collision_player_powerups()
        self.check_collision_player_enemies()            
        self.check_collision_enemies_player()
                
        #Atualiza a lista de objetos do jogo.                    
        self.runobjects(self.objlists) 

# Metodos para deteccao de colisao.

    def check_collision_player_powerups(self):
        """
        Testa a colisao entre o jogador e os powerups.
        """
        
        #Obtem o retangulo que envolve a aeronave do jogador, diminuindo
        #um pouco sua area para que a colisao seja mais realista.
        playerrect = self.player.rect.inflate(-3, -3)
        playercollide = playerrect.colliderect
        
        for p in self.powerupobjs:
            if playercollide(p.rect):
                p.dead = 1
                effect = p.effect()
                if effect.name == 'life':
                    self.player.stamina += effect.effect
                else:
                    self.player.nextgun = effect.effect
                    
    def check_collision_player_enemies(self):
        """
        Testa a colisao entre o jogador e os inimigos, ou seus tiros.
        """
        
        #Obtem o retangulo que envolve a aeronave do jogador, diminuindo
        #um pouco sua area para que a colisao seja mais realista.
        playerrect = self.player.rect.inflate(-3, -3)
        playercollide = playerrect.colliderect
        hitbullet = 0
        
        #Testa a colisao entre o jogador e os inimigos.
        if self.curwave:
            for wave in self.curwave:
                for s in wave.enemies:
                    if playercollide(s.rect):
                        s.dead = 1
                        self.changestate('playerdie')
        
        #Testa a colisao entre o jogador e tiros dos inimigos.
        for s in self.baddyshotobjs:
            r = s.rect
            if playercollide(r):
                s.dead = 1
                self.player.stamina -= s.dmg
                if self.player.stamina <= 0:
                    self.player.stamina = game.start_stamina
                    self.popobjs.append(objpopshot.PopShot(r.center))
                    self.changestate('playerdie')
                    hitbullet = 1
        
    def check_collision_enemies_player(self):
        """
        Testa a colisao entre os inimigos e os tiros do jogador.
        """
        
        for s in self.playershotobjs:
            r = s.rect
            if self.curwave:
                for wave in self.curwave:
                    for baddy in wave.enemies:
                        baddyrect = baddy.rect.inflate(-3,-3)
                        baddycollide = baddyrect.colliderect
                        if baddycollide(r):
                            self.player.score += 30
                            s.dead = 1
                            baddy.stamina -= s.dmg
                            if baddy.stamina <= 0: 
                                baddy.dead = 1
                                self.popobjs.append(objpopshot.PopShot(r.center, size=baddy.size))

#player quit
    def playerquit_tick(self):
        self.changestate('gameover')
        
#player die
    def playerdie_start(self):
        #Adiciona um objeto de explosao da aeronave do jogador
        #e finaliza o mapa.
        self.player.lives -= 1
        snd.play('explode', 1.0, self.player.rect.centerx)
        self.popobjs.append(objpopshot.PopShot(self.player.rect.center, size='big'))
        self.player.dead = 1
        self.player.active = 0
        self.explodetick = 0
        self.map.cleanup()
        
    def playerdie_tick(self):
        #Direciona o jogador para um novo comeco ou fim do jogo.
        if self.player.lives > 0:
            self.player.active = 0
            self.changestate('playerstart')
            self.explodetick = 0
        else:
            self.changestate('gameover')

    def playerdie_end(self):
        #Limpa toda a area do jogo.
        gfx.surface.fill((0, 0, 0))

#player start
    def playerstart_start(self):
        #Cria um novo jogo.
        self.powerupcount = max(0.0, self.powerupcount - 15.0)
        wave, init_pos = levels.make()
        self.ticks = 0
        if wave <> None: 
            wave.start(init_pos)
            self.curwave.append(wave)

    def playerstart_tick(self):
        if not self.player.active:
            self.player.active = 1
        self.player.start(self.pos)            
        self.staticobjs.append(self.player)
        self.changestate('normal')
        
    def playerstart_end(self):
        gfx.surface.fill((0, 0, 0))
        if self.map:
            self.map.cleanup()
        
#level start
    def levelstart_start(self):
        self.levelnum += 1

        self.numdeaths = 0
        
        levels.init('waves%d' % self.levelnum)
        self.waves = levels.maxwavesperlevel()
        
        if pygame.time.get_ticks() - self.songtime > game.musictime:
            songs = list(Songs)
            songs.remove(self.song)
            self.song = random.choice(songs)
            snd.playmusic(*self.song)
            self.songtime = pygame.time.get_ticks()
            
        if self.map: self.map.cleanup()
        self.map = map.TiledMap('map%d'%self.levelnum)
        

    def levelstart_tick(self):
        self.runobjects(self.objlists)
        self.changestate('playerstart')
        

#get ready
    def getready_start(self):
        self.ticks = 0
    
    def getready_tick(self):
        self.ticks += 1
        if not self.donegetready:
            img = getready_images[self.getreadyimage]
            r = img.get_rect()
            r = gfx.surface.blit(img, (game.size[0]/2-(r.width/2), game.size[1]/2-(r.height/2)))
            gfx.dirty(r)
            if not self.ticks % 40:
                self.getreadyimage =  (self.getreadyimage + 1) %len(getready_images)
            if self.ticks == 200:
                self.donegetready = 1
                self.ticks = 0
                self.cleanup()
        else:
            self.changestate('gamestart')
                
#game start
    def gamestart_start(self):
        self.ticks = 0
        self.level = 0
        self.donehud = 0

    def gamestart_tick(self): 
        self.ticks += 1
        if not self.donehud:
            if self.ticks == 10:
                self.donehud = 1
                self.ticks = 0
        else:
            if not self.ticks % 3 and self.levelnum < self.startlevel-1:
                self.levelnum += 1
            if not self.ticks % 16 and self.lives_left < game.start_lives:
                self.lives_left += 1
            if self.lives_left == game.start_lives and \
                       self.levelnum == self.startlevel-1:
                self.changestate('levelstart')


    def gamestart_end(self): 
        self.ticks = 0

#level end
    def levelend_start(self):
        snd.play('levelfinish')
        self.player.dead = 1
        self.player.active = 0
        self.cleanup()
                
    def levelend_tick(self):              
        if self.levelnum+1 >= levels.maxlevels():
            self.gamewin()
        else:
            self.changestate('levelup')
        self.runobjects(self.objlists)

    def levelend_end(self): 
        self.map.cleanup()
        self.levelchanged = 1

    def levelup_tick(self):
        if not self.donelevelup:
            c = levelupcolors[self.ticks % 2]
            self.ticks += 1
            img, r = font.text(c, 'Level Up!', (game.size[0]/2 - 15, game.size[1]/2 - 30), bgd=(0, 67, 171))
            r = gfx.surface.blit(img, r)
            gfx.dirty(r)
            if self.ticks == 100:
                self.donelevelup = 1
                self.ticks = 0
                self.cleanup()
                self.changestate('levelstart')
                self.levelchanged = 0
        
#game over
    def gameover_start(self): 
        snd.play('gameover')
        self.ticks = 0
        if not self.gamewon:
            if self.curwave:
                for wave in self.curwave:
                    for baddy in wave.enemies:
                        baddy.dead = 1
                        self.background(baddy.lastrect)
                        gfx.dirty(baddy.rect)
        
        for x in self.popobjs: x.dead = 1
        for x in self.powerupobjs: x.dead = 1
                
        B = self.background
        for l in self.objlists:
            for o in l:
                o.erase(B)
        if self.map: self.map.erase(B)
        if self.curwave: [wave.erase(B) for wave in self.curwave]
        self.runobjects(self.objlists)
        self.cleanup()

    def gameover_tick(self):
        if self.gamewon:
            self.cleanup()
            self.final_game_end()
            
        if not self.donequit:
            self.ticks += 1
            img = quit_images[self.quitimage]
            r = img.get_rect()
            r = gfx.surface.blit(img, (game.size[0]/2-(r.width/2), game.size[1]/2-(r.height/2)))
            gfx.dirty(r)
            if not self.ticks % 20:
                self.quitimage =  (self.quitimage + 1) %len(quit_images)
            if self.ticks == 200:
                self.donequit = 1
                self.ticks = 0
        else:        
                self.cleanup()
                self.final_game_end()
                           
    def final_game_end(self):
        nexthandler = self.prevhandler
        if self.gamewon:
            import gamewin
            nexthandler = gamewin.GameWin(nexthandler)
        game.handler = nexthandler




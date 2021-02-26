"""
Modulo game.
Define variaveis globais e funcoes auxiliares.
"""

import os
from cStringIO import StringIO
from pygame.rect import Rect

#Variaveis globais
start_lives = 3         #Numero de vidas iniciais do jogador
start_stamina = 100     #Stamina inicial ("vida" do jogador)
player_shotspeed = 10.5  #Velocidade de tiro do jogador        
enemy_fire = 80         #Numero de ticks para o proximo tiro inimigo
wavetime = 100          #VERIFICAR SE ESTA SENDO UTILIZADA.

arena = Rect(55, 50, 680, 442)  #Retangulo que define a area do jogo

poweruptime = 400.0
powerupspeed = 1.5
powerupwait = 26.0 #45.0
asteroidspeed = 1.4


speedmult = 0
musictime = 1000 * 120 #Tempo da musica (2 minutos)
text_length = 80  #frames text is displayed in-game
size = 800, 600   #Resolucao do jogo  
player = None
name_maxlength = 10     #Maior nome possivel para salvar
max_players = 5         #Numero de jogos salvos

#Informacoes do clock do jogo
clock = None
clockticks = 1

handler = None  #Handler do jogo atual
thread = None   #Threads em background
stopthread = 0  #Requisicao para terminar a thread

#Parametros default das opcoes do menu
music = 2
volume = 2

#Diretorio base e separador do sistema operacional do 
#jogador
base_dir = os.path.dirname(os.path.abspath(os.curdir))
sep = os.sep

def get_resource(filename):
    """
    Retorna o caminho absoluto para um arquivo do jogo.
    """
    global base_dir
    fullname = os.path.join(base_dir+sep+'data', filename)
    return fullname

def make_dataname(filename):
    """
    Cria um novo arquivo de dados do usuario
    """
    if os.name == 'posix':
        home = os.environ['HOME']
        fullhome = os.path.join(home, '.py1945')
        if not os.path.isdir(fullhome):
            try: os.mkdir(fullhome, 0755)
            except OSError: fullhome = home
        filename = os.path.join(fullhome, filename)
    else:
        filename = get_resource(filename)
    filename = os.path.abspath(filename)
    filename = os.path.normpath(filename)
    return filename

version = "0.3.4" #Versao atual do jogo
DEBUG = 0  #Modo de debug

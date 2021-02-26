"""
Modulo allmodules.
Assegura que as funcoes de inicializacao dos modulos do programa
sejam carregados.
"""

modules_string = """
game, gameplay, gamemenu, gamewin,
gamepref, gfx, snd, txt, levels, main, map, hud, 
objshot, objtext, objpowerup
"""

def modules_import():
    """
    Carrega os modulos do programa.
    """
    mods = modules_string.split(',')
    for m in mods:
        m = m.strip()
        __import__(m)

modules_import()




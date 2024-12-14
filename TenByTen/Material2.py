import pygame
import random
import os
from Settings import *

# > ZLOSIJT
BLOCKS = {
'Z':    [('Z', 'Z', 'Z',
           'Z', 'Z', 'Z', # Rotate = 0
           'Z', 'Z', 'Z'),
          ('Z', 'Z', 'Z',
           'Z', 'Z', 'Z', # Rotate = 1
           'Z', 'Z', 'Z'),
          ('Z', 'Z', 'Z',
           'Z', 'Z', 'Z', # Rotate = 2
           'Z', 'Z', 'Z'),
          ('Z', 'Z', 'Z',
           'Z', 'Z', 'Z', # Rotate = 3
           'Z', 'Z', 'Z')],

'L':     [('L'),
           ('L'),
           ('L'),
           ('L')],


'O':    [('O', 'O', # Rotate = 0
           'O', 'O'),
          ('O', 'O', # Rotate = 1
           'O', 'O'),
          ('O', 'O', # Rotate = 2
           'O', 'O'),
          ('O', 'O', # Rotate = 3
           'O', 'O')],

'S':    [('S', 'B', 'B',
           'S', 'B', 'B', # Rotate = 0
           'S', 'S', 'S'),
          ('S', 'S', 'S',
           'S', 'B', 'B', # Rotate = 1
           'S', 'B', 'B'),
          ('S', 'S', 'S',
           'B', 'B', 'S', # Rotate = 2
           'B', 'B', 'S'),
          ('B', 'B', 'S',
           'B', 'B', 'S', # Rotate = 3
           'S', 'S', 'S')],

'I':    [('B', 'B', 'B', 'B',
           'I', 'I', 'I', 'I', # Rotate = 0
           'B', 'B', 'B', 'B',
           'B', 'B', 'B', 'B'),
          ('B', 'B', 'I', 'B',
           'B', 'B', 'I', 'B', # Rotate = 1
           'B', 'B', 'I', 'B',
           'B', 'B', 'I', 'B'),
          ('B', 'B', 'B', 'B',
           'B', 'B', 'B', 'B', # Rotate = 2
           'I', 'I', 'I', 'I',
           'B', 'B', 'B', 'B'),
          ('B', 'I', 'B', 'B',
           'B', 'I', 'B', 'B', # Rotate = 3
           'B', 'I', 'B', 'B',
           'B', 'I', 'B', 'B')],

# 'I2':    [('B', 'B',
#            'P', 'P'),# Rotate = 0
#           ('P', 'B',
#            'P', 'B'),# Rotate = 1
#           ('P', 'P',
#            'B', 'B'),# Rotate = 2
#           ('B', 'P',
#            'B', 'P')],# Rotate = 3

'J':    [('B', 'B', 'B',
           'J', 'J', 'J', # Rotate = 0
           'B', 'B', 'B'),
          ('J', 'B', 'B',
           'J', 'B', 'B', # Rotate = 1
           'J', 'B', 'B'),
          ('J', 'J', 'J',
           'B', 'B', 'B', # Rotate = 2
           'B', 'B', 'B'),
          ('B', 'B', 'J',
           'B', 'B', 'J', # Rotate = 3
           'B', 'B', 'J')],

'T':     [('T', 'B',
           'T', 'T'),# Rotate = 0
          ('T', 'T',
           'T', 'B'),# Rotate = 1
          ('T', 'T',
           'B', 'T'),# Rotate = 2
          ('B', 'T',
           'T', 'T')]# Rotate = 3
}

COLORS = {
    'BLACK'         : (0,   0,   0),
    'YELLOW'        : (255, 255, 0),
    'SKY_BLUE'      : (0,   255, 255),
    'RED'           : (255, 0,   0),
    'GREEN'         : (0,   221, 2),
    'BLUE'          : (30,  128, 255),
    'ORANGE'        : (255, 140, 0),
    'PURPLE'        : (243, 0,   244),
    'GRAY'          : (128, 128, 128),
    'DARK_GRAY'     : (34,  34,  34),
    'LIGHT_GRAY'    : (215, 215, 219),
    'WHITE'         : (255, 255, 255),
}
# > ZLOSIJT
BLOCK_COLORS = {
    'Z': COLORS['SKY_BLUE'],
    'L': COLORS['BLUE'],
    'O': COLORS['ORANGE'],
    'S': COLORS['YELLOW'],
    'I': COLORS['GREEN'],
    'J': COLORS['PURPLE'],
    'T': COLORS['RED'],
    'B': COLORS['BLACK']
}

pygame.font.init()
FONTS = {
    'COUNT_BOARD_TITLE' : pygame.font.SysFont("microsoftsansserif",   20, bold=False,  italic=False),
    'COUNT_BOARD_VALUE' : pygame.font.SysFont("microsoftsansserif",   30, bold=False,  italic=False),
    'SUB_BOARD_TITLE'   : pygame.font.SysFont("microsoftsansserif", 24, bold=False, italic=False),
    'LIVE_FPS'          : pygame.font.SysFont("microsoftsansserif",    20, bold=False, italic=False)
}

pygame.mixer.init()
SFX_PACK_DIR    = "./Resource/SFX/DEFAULT_SFX/"
SFX             = {str(SFX_PATH).split('.')[0] : pygame.mixer.Sound(SFX_PACK_DIR + str(SFX_PATH)) for SFX_PATH in os.listdir(SFX_PACK_DIR) if os.path.isfile(os.path.join(SFX_PACK_DIR,SFX_PATH))}

BACKGROUND_MUSICS = [os.path.join(SFX_PACK_DIR+'Music/', path) for path in os.listdir(SFX_PACK_DIR+"Music/")]
BGM_INDEX = random.randint(0,len(BACKGROUND_MUSICS)-1)
pygame.mixer.music.load(BACKGROUND_MUSICS[BGM_INDEX])

TITLE_MUSIC = os.path.join('./Resource/SFX/', 'We Wish You a Merry Christmas_이나일.wav')
pygame.mixer.music.load(TITLE_MUSIC)
pygame.mixer.music.set_volume(SETTINGS['VOLUME & AUDIO'].getValue('MUSIC') / 100)

pygame.display.init()
BLOCK_TEXTURE           = {}

BACKGROUND_RESOURCE_DIR = "./Resource/Backgrounds/"
BACKGROUNDS             = [pygame.image.load(BACKGROUND_RESOURCE_DIR + str(path)) for path in os.listdir(BACKGROUND_RESOURCE_DIR)]
BACKGROUND_INDEX        = random.randint(0, len(BACKGROUNDS) - 1)

#SRS KICK TABLE HARD CODING
SRS_DEFAULT_CLOCKWISE         = [[[+0,+0],[-1,+0],[-1,+1],[+0,-2],[-1,-2]], # 0>>1─┐
                                 [[+0,+0],[+1,+0],[+1,-1],[+0,+2],[+1,+2]], # 1>>2─┤
                                 [[+0,+0],[+1,+0],[+1,+1],[+0,-2],[+1,-2]], # 2>>3─┤
                                 [[+0,+0],[-1,+0],[-1,-1],[+0,+2],[-1,+2]]] # 3>>0─┘

SRS_DEFAULT_COUNTERCLOCKWISE  = [[[+0,+0],[+1,+0],[+1,+1],[+0,-2],[+1,-2]], # 0>>1─┐
                                 [[+0,+0],[+1,+0],[+1,-1],[+0,+2],[+1,+2]], # 1>>2─┤
                                 [[+0,+0],[-1,+0],[-1,+1],[+0,-2],[-1,-2]], # 2>>3─┤
                                 [[+0,+0],[-1,+0],[-1,-1],[+0,+2],[-1,+2]]] # 3>>0─┘

SRS_DEFAULT_180               = [[[+0,+0],[+1,+0],[+2,+0],[+1,+1],[+2,+1],[-1,+0],[-2,+0],[-1,+1],[-2,+1],[+0,-1],[+3,+0],[-3,+0]],	# 0>>2─┐
		                         [[+0,+0],[+0,+1],[+0,+2],[-1,+1],[-1,+2],[+0,-1],[+0,-2],[-1,-1],[-1,-2],[+1,+0],[+0,+3],[+0,-3]],	# 1>>3─┼┐
		                         [[+0,+0],[-1,+0],[-2,+0],[-1,-1],[-2,-1],[+1,+0],[+2,+0],[+1,-1],[+2,-1],[+0,+1],[-3,+0],[+3,+0]],	# 2>>0─┘│
		                         [[+0,+0],[+0,+1],[+0,+2],[+1,+1],[+1,+2],[+0,-1],[+0,-2],[+1,-1],[+1,-2],[-1,+0],[+0,+3],[+0,-3]]]	# 3>>1──┘

SRS_I_CLOCKWISE               = [[[+0,+0],[-2,+0],[+1,+0],[-2,-1],[+1,+2]], # 0>>1─┐
                                 [[+0,+0],[-1,+0],[+2,+0],[+1,+2],[+2,-1]], # 1>>2─┤
                                 [[+0,+0],[+2,+0],[-1,+0],[+2,+1],[-1,-2]], # 2>>3─┤
                                 [[+0,+0],[+1,+0],[-2,+0],[+1,-2],[-2,+1]]] # 3>>0─┘

SRS_I_COUNTERCLOCKWISE        = [[[+0,+0],[-1,+0],[+2,+0],[-1,+2],[+2,-1]], # 0>>1─┐
                                 [[+0,+0],[+2,+0],[-1,+0],[+2,+1],[-1,-2]], # 1>>2─┤
                                 [[+0,+0],[+1,+0],[-2,+0],[+1,-2],[-2,+1]], # 2>>3─┤
                                 [[+0,+0],[-2,+0],[+1,+0],[-2,-1],[+1,+2]]] # 3>>0─┘

SRS_I_180                     = [[[+0,+0],[-1,+0],[-2,+0],[+1,+0],[+2,+0],[+0,+1]],													# 0>>2─┐
		                         [[+0,+0],[+0,+1],[+0,+2],[+0,-1],[+0,-2],[-1,+0]],													# 1>>3─┼┐
		                         [[+0,+0],[+1,+0],[+2,+0],[-1,+0],[-2,+0],[+0,-1]],													# 2>>0─┘│
		                         [[+0,+0],[+0,+1],[+0,+2],[+0,-1],[+0,-2],[+1,+0]]]													# 3>>1──┘

SRS_KICK_TABLE = {'DEFAULT' : {-2 : SRS_DEFAULT_180,    -1 : SRS_DEFAULT_COUNTERCLOCKWISE,  0 : [[0,0]],    1 : SRS_DEFAULT_CLOCKWISE,  2 : SRS_DEFAULT_180},
                  'I'       : {-2 : SRS_I_180,          -1 : SRS_I_COUNTERCLOCKWISE,        0 : [[0,0]],    1 : SRS_I_CLOCKWISE,        2 : SRS_I_180       }}

EMPTY_LINE = ['B' for i in range(WIDTH)]
T_CORNER_OFFSET = [[0,0], [2,0], [0,2], [2,2]]
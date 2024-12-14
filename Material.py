import pygame
import random
import os
from Settings import *

# > ZLOSIJT
BLOCKS = {
    'Z': [('Z', 'Z', 'B',
           'B', 'Z', 'Z', # Rotate = 0
           'B', 'B', 'B'),
          ('B', 'B', 'Z',
           'B', 'Z', 'Z', # Rotate = 1
           'B', 'Z', 'B'),
          ('B', 'B', 'B',
           'Z', 'Z', 'B', # Rotate = 2
           'B', 'Z', 'Z'),
          ('B', 'Z', 'B',
           'Z', 'Z', 'B', # Rotate = 3
           'Z', 'B', 'B')],

    'L': [('B', 'B', 'L',
           'L', 'L', 'L', # Rotate = 0
           'B', 'B', 'B'),
          ('B', 'L', 'B',
           'B', 'L', 'B', # Rotate = 1
           'B', 'L', 'L'),
          ('B', 'B', 'B',
           'L', 'L', 'L', # Rotate = 2
           'L', 'B', 'B'),
          ('L', 'L', 'B',
           'B', 'L', 'B', # Rotate = 3
           'B', 'L', 'B')],

    'O': [('O', 'O', # Rotate = 0
           'O', 'O'),
          ('O', 'O', # Rotate = 1
           'O', 'O'),
          ('O', 'O', # Rotate = 2
           'O', 'O'),
          ('O', 'O', # Rotate = 3
           'O', 'O')],

    'S': [('B', 'S', 'S',
           'S', 'S', 'B', # Rotate = 0
           'B', 'B', 'B'),
          ('B', 'S', 'B',
           'B', 'S', 'S', # Rotate = 1
           'B', 'B', 'S'),
          ('B', 'B', 'B',
           'B', 'S', 'S', # Rotate = 2
           'S', 'S', 'B'),
          ('S', 'B', 'B',
           'S', 'S', 'B', # Rotate = 3
           'B', 'S', 'B')],

    'I': [('B', 'B', 'B', 'B',
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

    'J': [('J', 'B', 'B',
           'J', 'J', 'J', # Rotate = 0
           'B', 'B', 'B'),
          ('B', 'J', 'J',
           'B', 'J', 'B', # Rotate = 1
           'B', 'J', 'B'),
          ('B', 'B', 'B',
           'J', 'J', 'J', # Rotate = 2
           'B', 'B', 'J'),
          ('B', 'J', 'B',
           'B', 'J', 'B', # Rotate = 3
           'J', 'J', 'B')],

    'T': [('B', 'T', 'B',
           'T', 'T', 'T', # Rotate = 0
           'B', 'B', 'B'),
          ('B', 'T', 'B',
           'B', 'T', 'T', # Rotate = 1
           'B', 'T', 'B'),
          ('B', 'B', 'B',
           'T', 'T', 'T', # Rotate = 2
           'B', 'T', 'B'),
          ('B', 'T', 'B',
           'T', 'T', 'B', # Rotate = 3
           'B', 'T', 'B')]
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
BLOCK_COLORS = {
    'I': COLORS['SKY_BLUE'],
    'J': COLORS['BLUE'],
    'L': COLORS['ORANGE'],
    'O': COLORS['YELLOW'],
    'S': COLORS['GREEN'],
    'T': COLORS['PURPLE'],
    'Z': COLORS['RED'],
    'B': COLORS['BLACK']
}

pygame.font.init()
FONT_DIR = "./Resource/Font/"
FONTS = {
    'COUNT_BOARD_TITLE' : pygame.font.Font      (FONT_DIR + "NotoSansKR-Medium.otf",      20),
    'COUNT_BOARD_VALUE' : pygame.font.Font      (FONT_DIR + "NotoSansKR-Medium.otf",      30),
    'SUB_BOARD_TITLE'   : pygame.font.SysFont   ("microsoftsansserif",              24),
    'LIVE_FPS'          : pygame.font.Font      (FONT_DIR + "NotoSansKR-Black.otf",       20),
    'VERSION_DESC'      : pygame.font.Font      (FONT_DIR + "NotoSansKR-Medium.otf",        18),
    'BUTTON_TITLE'      : pygame.font.Font      (FONT_DIR + "NotoSansKR-Thin.otf",       40),
    'SETTING_TITLE'     : pygame.font.Font      (FONT_DIR + "NotoSansKR-Bold.otf",        30),
    'SETTING_VALUE_CODE': pygame.font.Font      (FONT_DIR + "NotoSansKR-Medium.otf",      20),
    'KEY_VALUE'         : pygame.font.Font      (FONT_DIR + "NotoSansKR-Regular.otf",     15),
    'BACK_BTN'          : pygame.font.Font      (FONT_DIR + "NotoSansKR-Bold.otf",        25),
    'CURTAIN_DISC'      : pygame.font.Font      (FONT_DIR + "NotoSansKR-Bold.otf",        105),
    'CURTAIN_DISC_SUB'  : pygame.font.Font      (FONT_DIR + "NotoSansKR-Bold.otf",        30),
    'SPIN_TYPE'         : pygame.font.Font      (FONT_DIR + "NotoSansKR-Medium.otf",      30),
    'BTB_CHAIN'         : pygame.font.Font      (FONT_DIR + "NotoSansKR-Medium.otf",      25),
    'BROKEN_LINE'       : pygame.font.Font      (FONT_DIR + "NotoSansKR-Bold.otf",       45),
    'COMBO'             : pygame.font.Font      (FONT_DIR + "NotoSansKR-Medium.otf",      40),
    'TITLE_LABEL'       : pygame.font.Font      (FONT_DIR + "NotoSansKR-Bold.otf",        SCREEN_SIZE_HEIGHT//35)
}

pygame.mixer.init()
SFX_PACK_DIR    = "./Resource/SFX/DEFAULT_SFX/"
SFX             = {str(SFX_PATH).split('.')[0] : pygame.mixer.Sound(SFX_PACK_DIR + str(SFX_PATH)) for SFX_PATH in os.listdir(SFX_PACK_DIR) if os.path.isfile(os.path.join(SFX_PACK_DIR,SFX_PATH))}
for sfx in SFX.values():
    sfx.set_volume(SETTINGS['VOLUME & AUDIO'].getValue('SFX') / 100)

BACKGROUND_MUSICS = [os.path.join(SFX_PACK_DIR+'Music/', path) for path in os.listdir(SFX_PACK_DIR+"Music/")]
BGM_INDEX = random.randint(0,len(BACKGROUND_MUSICS)-1)

TITLE_MUSIC = os.path.join('./Resource/SFX/', 'We Wish You a Merry Christmas_이나일.wav')
pygame.mixer.music.load(TITLE_MUSIC)
pygame.mixer.music.set_volume(SETTINGS['VOLUME & AUDIO'].getValue('MUSIC') / 100)

pygame.display.init()
BLOCK_TEXTURE           = {}
BACKGROUND_RESOURCE_DIR = "./Resource/Backgrounds/"
BACKGROUNDS             = [pygame.image.load(BACKGROUND_RESOURCE_DIR + str(path)) for path in os.listdir(BACKGROUND_RESOURCE_DIR)]
BACKGROUND_INDEX        = random.randint(0, len(BACKGROUNDS) - 1)

SKIN_SORT = ['RINGFIT', 'TETRIO', 'DEFAULT', 'JEWEL', 'CHRISTMAS', 'GREEN_YOGURT','GLOSS','SCI-FI','LANTERN','ROCKS_RUNE','YOSHI_EGG', 'SIMPLE', 'THICC_MINO', 'RAINBOW', 'SUPERTRIS']
CURRENT_SKIN_INDEX = 0
SKIN_PREVIEW_INDEX = 0

PREVIEW_RESOURCE_DIR    = "./Resource/Skin_Preview/"
PREVIEW_SKINS           = [pygame.transform.smoothscale(pygame.image.load(PREVIEW_RESOURCE_DIR + str(skin) + '.png'),(960,540)) for skin in SKIN_SORT]

TITLE_RESOURCE_DIR      = './Resource/TitleMenu/'
TITLE_ASSETS            = {path.split('.')[0] : pygame.image.load(TITLE_RESOURCE_DIR + str(path)) for path in os.listdir(TITLE_RESOURCE_DIR)}

#SRS KICK TABLE HARD CODING
SRS_DEFAULT_CLOCKWISE         = [[[+0,+0],[-1,+0],[-1,+1],[+0,-2],[-1,-2]], # 0>>1─┐
                                 [[+0,+0],[+1,+0],[+1,-1],[+0,+2],[+1,+2]], # 1>>2─┤
                                 [[+0,+0],[+1,+0],[+1,+1],[+0,-2],[+1,-2]], # 2>>3─┤
                                 [[+0,+0],[-1,+0],[-1,-1],[+0,+2],[-1,+2]]] # 3>>0─┘

SRS_DEFAULT_COUNTERCLOCKWISE  = [[[+0,+0],[+1,+0],[+1,+1],[+0,-2],[+1,-2]], # 0>>1─┐
                                 [[+0,+0],[+1,+0],[+1,-1],[+0,+2],[+1,+2]], # 1>>2─┤
                                 [[+0,+0],[-1,+0],[-1,+1],[+0,-2],[-1,-2]], # 2>>3─┤
                                 [[+0,+0],[-1,+0],[-1,-1],[+0,+2],[-1,+2]]] # 3>>0─┘

SRS_DEFAULT_180               = [[[+0,+0],[-1,+0],[-2,+0],[-1,-1],[-2,-1],[+1,+0],[+2,+0],[+1,-1],[+2,-1],[+0,+1],[-3,+0],[+3,+0]],	# 0>>2─┐
		                         [[+0,+0],[+0,+1],[+0,+2],[+1,+1],[+1,+2],[+0,-1],[+0,-2],[+1,-1],[+1,-2],[-1,+0],[+0,+3],[+0,-3]],	# 1>>3─┼┐
		                         [[+0,+0],[+1,+0],[+2,+0],[+1,+1],[+2,+1],[-1,+0],[-2,+0],[-1,+1],[-2,+1],[+0,-1],[+3,+0],[-3,+0]],	# 2>>0─┘│
		                         [[+0,+0],[+0,+1],[+0,+2],[-1,+1],[-1,+2],[+0,-1],[+0,-2],[-1,-1],[-1,-2],[+1,+0],[+0,+3],[+0,-3]]]	# 3>>1──┘

SRS_I_CLOCKWISE               = [[[+0,+0],[-2,+0],[+1,+0],[-2,-1],[+1,+2]], # 0>>1─┐
                                 [[+0,+0],[-1,+0],[+2,+0],[+1,+2],[+2,-1]], # 1>>2─┤
                                 [[+0,+0],[+2,+0],[-1,+0],[+2,+1],[-1,-2]], # 2>>3─┤
                                 [[+0,+0],[+1,+0],[-2,+0],[+1,-2],[-2,+1]]] # 3>>0─┘

SRS_I_COUNTERCLOCKWISE        = [[[+0,+0],[-1,+0],[+2,+0],[-1,+2],[+2,-1]], # 0>>1─┐
                                 [[+0,+0],[+2,+0],[-1,+0],[+2,+1],[-1,-2]], # 1>>2─┤
                                 [[+0,+0],[+1,+0],[-2,+0],[+1,-2],[-2,+1]], # 2>>3─┤
                                 [[+0,+0],[-2,+0],[+1,+0],[-2,-1],[+1,+2]]] # 3>>0─┘

SRS_I_180                     = [[[+0,+0],[+1,+0],[+2,+0],[-1,+0],[-2,+0],[+0,-1]],													# 0>>2─┐
		                         [[+0,+0],[+0,+1],[+0,+2],[+0,-1],[+0,-2],[+1,+0]],													# 1>>3─┼┐
		                         [[+0,+0],[-1,+0],[-2,+0],[+1,+0],[+2,+0],[+0,+1]],													# 2>>0─┘│
		                         [[+0,+0],[+0,+1],[+0,+2],[+0,-1],[+0,-2],[-1,+0]]]													# 3>>1──┘


SRS_KICK_TABLE = {'DEFAULT' : {-2 : SRS_DEFAULT_180,    -1 : SRS_DEFAULT_COUNTERCLOCKWISE,  0 : [[0,0]],    1 : SRS_DEFAULT_CLOCKWISE,  2 : SRS_DEFAULT_180},
                  'I'       : {-2 : SRS_I_180,          -1 : SRS_I_COUNTERCLOCKWISE,        0 : [[0,0]],    1 : SRS_I_CLOCKWISE,        2 : SRS_I_180       }}

LINE_STR_PREFIX = ['SINGLE', 'DOUBLE', 'TRIPLE', 'QUAD', 'QUINTUPLE', 'SIXTUPLE', 'SEPTUPLE', 'OCTUPLE', 'NONUPLE', 'DECUPLE']
EMPTY_LINE = ['B' for i in range(WIDTH)]
T_CORNER_OFFSET = [[0,0], [2,0], [0,2], [2,2]]

TEXTURE_LOAD_SORT = {'240x144' : [[5,3], ['GARBAGE','UNBREAKABLE','texture1','SHADOW','WARN']],
                     '368x30' : [[12, 1],['SHADOW','UNBREAKABLE','GARBAGE','texture1','WARN']],
                     '372x30' : [[12, 1],['SHADOW','UNBREAKABLE','GARBAGE','texture1','WARN']],
                     '372x31' : [[12, 1],['SHADOW','UNBREAKABLE','GARBAGE','texture1','WARN']],
                     '821x64' : [[12, 1],['SHADOW','UNBREAKABLE','GARBAGE','texture1','WARN']],
                     '816x64' : [[12, 1],['SHADOW','UNBREAKABLE','GARBAGE','texture1','WARN']],
                     '1000x78': [[12, 1],['SHADOW','UNBREAKABLE','GARBAGE','texture1','WARN']],
                     '2976x240':[[12, 1],['SHADOW','UNBREAKABLE','GARBAGE','texture1','WARN']]
                    }
LOADED_TEXTURES = {}
PREVIEW_TEXTURES = {}
BLOCK_TEXTURE = {}
PREVIEW_TEXTURE = {}


for SKIN_PATH in os.listdir('./Resource/Tetromino/'):
    SKIN_CODE = SKIN_PATH.split('.')[0]
    PREVIEW_TEXTURES[SKIN_CODE] = {}
    image_source = pygame.image.load('./Resource/Tetromino/'+SKIN_PATH)
    TEXTURE_INFO = TEXTURE_LOAD_SORT[str(image_source.get_width())+'x'+str(image_source.get_height())]
    U,V = TEXTURE_INFO[0]
    preview_image = pygame.transform.scale(image_source, (37 * U,37 * V))
    cnt = 0
    for key in list(BLOCKS.keys()) + TEXTURE_INFO[1]: #dict_keys -> list
        preview_picture = pygame.Surface((37,37), pygame.SRCALPHA)
        preview_picture.blit(preview_image, (-37 * (cnt % U), -37 * (cnt // U)))
        PREVIEW_TEXTURES[SKIN_CODE][key] = preview_picture
        cnt += 1
PREVIEW_TEXTURE = PREVIEW_TEXTURES[SKIN_SORT[CURRENT_SKIN_INDEX]]
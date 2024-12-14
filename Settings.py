import pygame
from pygame.locals import *
import random

class SETTING:
    def __init__(self, DEFAULT_VALUE):
        self.values = DEFAULT_VALUE
    def setValue(self, key, value):
        self.values[key][1] = value
    def getValue(self, key):
        if self.values[key][0] == 'KEY':
            return self.values[key][1]
        elif self.values[key][0] in ['INT','FLOAT']:
            return self.values[key][1][0]
    def getValues(self):
        return self.values
    def getFullValue(self, key):
        return self.values[key][1]
    def getType(self, key):
        return self.values[key][0]
                        #isFolded()

SETTINGS = {'CONTROLS'          : SETTING({'MOVE FALLING PIECE LEFT'  : ['KEY',   [K_LEFT,None,None]],            'MOVE FALLING PIECE RIGHT': ['KEY',   [K_RIGHT,None,None]],   'SOFT DROP' : ['KEY', [K_DOWN,None,None]],  'HARD DROP'         : ['KEY', [K_UP,K_SPACE,None]],
                                           'ROTATE COUNTERCLOCKWISE'  : ['KEY',   [K_z,None,None]],               'ROTATE CLOCKWISE'        : ['KEY',   [K_x,None,None]],       'ROTATE 180': ['KEY', [K_a,None,None]],     'SWAP HOLD PIECE'   : ['KEY', [K_c,None,None]],
                                           'FOREIT GAME'              : ['KEY',   [K_ESCAPE,None,None]],          'RETRY GAME'              : ['KEY',   [K_r,None,None]]}),
            'HANDLING'          : SETTING({'ARR'                      : ['FLOAT', [2.0,0.0,5.0, 76.25, 'F']],     'DAS'                     : ['FLOAT', [10.0,  1.0, 20.0, 76.25, 'F']],
                                           'DCD'                      : ['FLOAT', [1.0,0.0,20.0,76.25, 'F']],     'SDF'                     : ['FLOAT', [6.0,   5.0, 40.1, 76.25, 'X']]}),
            'VIDEO'             : SETTING({'MAX FRAME'                : ['INT',   [300,5,300,140, 'F']]}),
            'VOLUME & AUDIO'    : SETTING({'MUSIC'                    : ['INT',   [100,0,100,100,'%']],           'SFX'                     : ['INT',   [100,0,100,100,'%']],}),
            'GAMEPLAY'          : SETTING({'GRID VISIBILITY'          : ['INT',   [10,0,100,200,'%']],            'BOARD VISIBILITY'        : ['INT',   [85,0,100,200,'%']],
                                           'SHADOW VISIBILITY'        : ['INT',   [50,0,100,200,'%']],            'BOARD ZOOM'              : ['INT',   [100,50,130,200,'%']]})
           }
#1.0 = 1.0F
FRAMES              = 16.6
WIDTH               = 10
HEIGHT              = 22

SHADOW_BRIGHTNESS   = 0.5
SCREEN_SIZE_WIDTH   = 1920
SCREEN_SIZE_HEIGHT  = 1080

TEXTURE_WIDTH       = round(37 * (SETTINGS['GAMEPLAY'].getValue('BOARD ZOOM') / 100))
TEXTURE_HEIGHT      = round(37 * (SETTINGS['GAMEPLAY'].getValue('BOARD ZOOM') / 100))
X_OFFSET            = (SCREEN_SIZE_WIDTH - WIDTH * TEXTURE_WIDTH + 2) / 2
Y_OFFSET            = (SCREEN_SIZE_HEIGHT - (HEIGHT+1) * TEXTURE_HEIGHT + 2) / 2
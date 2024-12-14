import sys
from math import sqrt
from threading import Thread
import random
import time

import pygame
from pygame.locals import *

import Material
from Material import *
from Settings import *
from Particle import *
from Utils import *

T_SPIN_STATE = False
DROPED_PIECE = 0
COMBO = 0
class Block:
    def __init__(self, name):
        self.turn = 0
        self.name = name
        self.type = BLOCKS[name]
        self.data = self.type[self.turn]
        self.size = int(sqrt(len(self.data)))
        self.xpos = (WIDTH - self.size) // 2
        self.ypos = 0

    def draw(self):
        GROUND_Y = self.ypos
        while not is_overlapped(self.xpos, GROUND_Y + 1, self.turn):
            GROUND_Y = GROUND_Y + 1
        for index in range(len(self.data)):                                                             #여기 중복 소스 결합
            xpos = index % self.size
            ypos = index // self.size
            val = self.data[index]
            if (0 <= ypos + self.ypos < HEIGHT) and (0 <= xpos + self.xpos < WIDTH) and val != 'B':
                x_coords = xpos + self.xpos
                y_coords = ypos + GROUND_Y
                x_pos = X_OFFSET + x_coords * TEXTURE_WIDTH
                y_pos = Y_OFFSET + y_coords * TEXTURE_HEIGHT
                #BLOCK_TEXTURE['SHADOW'].fill(BLOCK_COLORS[val], special_flags=pygame.BLEND_RGB_MULT)
                SURFACE.blit(BLOCK_TEXTURE['SHADOW'], (x_pos, y_pos))
        for index in range(len(self.data)):
            xpos = index % self.size
            ypos = index // self.size
            val = self.data[index]
            if (0 <= ypos + self.ypos < HEIGHT) and (0 <= xpos + self.xpos < WIDTH) and val != 'B':
                x_coords = xpos + self.xpos
                y_coords = ypos + self.ypos
                x_pos = X_OFFSET + x_coords * TEXTURE_WIDTH
                y_pos = Y_OFFSET + y_coords * TEXTURE_HEIGHT
                SURFACE.blit(BLOCK_TEXTURE[val], (x_pos, y_pos))
    def draw_Warn(self):
        for index in range(len(self.data)):
            xpos = index % self.size
            ypos = index // self.size
            val = self.data[index]
            if (0 <= ypos + self.ypos < HEIGHT) and (0 <= xpos + self.xpos < WIDTH) and val != 'B':
                x_coords = xpos + self.xpos
                y_coords = ypos + self.ypos
                x_pos = X_OFFSET + x_coords * TEXTURE_WIDTH
                y_pos = Y_OFFSET + y_coords * TEXTURE_HEIGHT
                SURFACE.blit(BLOCK_TEXTURE['WARN'],(x_pos, y_pos))
    def move(self, xPos, yPos):
        global T_SPIN_STATE
        self.xpos = xPos
        self.ypos = yPos
        T_SPIN_STATE = False

    def rotate(self, rotation):
        global GRAVITY_DELTA, T_SPIN_STATE
        GRAVITY_DELTA = 0
        Newton = (self.turn + rotation) % 4
        for xOffset, yOffset in SRS_KICK_TABLE['I' if self.name == 'I' else 'DEFAULT'][rotation][self.turn]:
            if trymove(self.xpos + xOffset, self.ypos - yOffset, Newton):
                self.turn = Newton
                self.data = self.type[self.turn]
                if self.name == 'T':
                    CORNER_BLOCK_COUNT = 0
                    for cornerX, cornerY in T_CORNER_OFFSET:
                        if self.xpos+cornerX < WIDTH and self.ypos+cornerY < HEIGHT and FIELD[self.ypos+cornerY][self.xpos+cornerX] != 'B':
                            CORNER_BLOCK_COUNT += 1
                    if CORNER_BLOCK_COUNT >= 3:
                        T_SPIN_STATE = True
                        SFX['spin'].play()
                        return
                    else:
                        T_SPIN_STATE = False
                SFX['rotate'].play()
                return

    def place(self):
        global BLOCK, DROPED_PIECE, COMBO, LAST_CLEAR_LINE, LAST_CLEAR_TIME, LAST_T_SPIN_STATE, BTB_CHAIN, CAN_SWAP
        CAN_SWAP = True
        DROPED_PIECE += 1
        COUNT_BOARD['INPUTS'] = str(INPUT_KEYS) + ', ' + str(format(INPUT_KEYS / DROPED_PIECE, '0.2f')) + '/P'
        PLACED_BLOCKS = []
        for y_offset in range(self.size):
            for x_offset in range(self.size):
                val = self.data[y_offset * self.size + x_offset]
                if val != 'B':
                    FIELD[self.ypos + y_offset][self.xpos + x_offset] = val
                    PLACED_BLOCKS.append([x_offset, y_offset])
        CLEARED_LINES = CHECK_FIELD()
        if CLEARED_LINES > 0:
            COMBO = COMBO + 1
            LAST_CLEAR_LINE = CLEARED_LINES
            LAST_CLEAR_TIME = pygame.time.get_ticks()
            LAST_T_SPIN_STATE = T_SPIN_STATE
            if CLEARED_LINES == 4 or T_SPIN_STATE:
                BTB_CHAIN += 1
            else:
                if BTB_CHAIN > 2:
                    SFX['btb_break'].play()
                BTB_CHAIN = 0
        else:
            COMBO = 0
            for x, y in PLACED_BLOCKS:
                PARTICLE_SYSTEM.add_clensing_particle(X_OFFSET + (self.xpos + x) * TEXTURE_WIDTH, Y_OFFSET + (self.ypos + y) * TEXTURE_HEIGHT, TEXTURE_WIDTH, TEXTURE_HEIGHT, (255,255,255,100), .05, .25)
        BLOCK = new_block(gen_block())

    def is_on_ground(self):
        if is_overlapped(self.xpos, self.ypos + 1, self.turn):
            return True
        return False

    def Gravity(self):
        global GRAVITY_DELTA
        if is_overlapped(self.xpos, self.ypos + 1, self.turn):
            if GRAVITY_DELTA >= 1:
                self.place()
                SFX['harddrop'].play()
        else:
            trymove(self.xpos, self.ypos + 1, self.turn)
            if self.is_on_ground():
                SFX['sidehit'].play()
            GRAVITY_DELTA = 0

    def hard_drop(self):
        SFX['harddrop'].play()
        MAX_Y = ypos = self.ypos
        while not is_overlapped(self.xpos, ypos + 1, self.turn):
            ypos = ypos + 1
        self.ypos = ypos
        min_x,max_x = (3,0)
        for y_offset in range(self.size):
            for x_offset in range(self.size):
                val = self.data[y_offset * self.size + x_offset]
                if val != 'B':
                    min_x = min(min_x, x_offset)
                    max_x = max(max_x, x_offset)
        for i in range(random.randint(1,min(ypos-MAX_Y + 1, 8))):
            PARTICLE_SYSTEM.add_bubble_particle(TEXTURE_WIDTH * (self.xpos+random.uniform(min_x,max_x))+ random.uniform(0,1) * TEXTURE_HEIGHT + X_OFFSET, (random.uniform(MAX_Y, ypos)+random.uniform(0,1)) * TEXTURE_HEIGHT + Y_OFFSET, 4, [0, -300], BLOCK_COLORS[self.name])
        self.place()


Gravity = 1

def is_KEY_PRESSED(keyset_name):
    keys = pygame.key.get_pressed()
    for key in SETTINGS['CONTROLS'].getValue(keyset_name):
        if key is not None and keys[key]:
            return True

def KEY_INF_MOVE(value_name, value, key_name, thread, xoffset, yoffset):
    if SETTINGS['HANDLING'].getValue(value_name) == value:
        if thread is not None and thread.getLoop() is True and is_KEY_PRESSED(key_name):
            move_end(xoffset, yoffset)

def INF_MOVE_CHECK():
    # ARR = 0 or SDF값이 무한일때 스레드는 스레드는 한번 실행 후 종료되므로.. (움직임 변화 + 블록 생성) 시 확인해서 재 이동 스레드 while문 비용 ↓
    keys = pygame.key.get_pressed()
    KEY_INF_MOVE('ARR', 0,    'MOVE FALLING PIECE RIGHT', MOVE_THREAD,  1, 0)
    KEY_INF_MOVE('ARR', 0,    'MOVE FALLING PIECE LEFT',  MOVE_THREAD,  -1, 0)
    KEY_INF_MOVE('SDF', 40.1, 'SOFT DROP',                DOWN_THREAD,0, 1)
def trymove(posX, posY, turn):
    if not is_overlapped(posX, posY, turn):
        BLOCK.move(posX, posY)
        BLOCK.turn = turn
        INF_MOVE_CHECK()
        return True
    return False

def move_end(xOffset, yOffset):
    cnt = 0
    while not is_overlapped(BLOCK.xpos + xOffset, BLOCK.ypos + yOffset, BLOCK.turn):
        BLOCK.move(BLOCK.xpos + xOffset, BLOCK.ypos + yOffset)
        cnt += 1
    return cnt


class MoveKeyThread(StoppableThread):
    def __init__(self, KEY, xOffset, yOffset, firstMS, repeatMS, hitSFX):
        super().__init__()
        self.KEY = KEY
        self.xOffset = xOffset
        self.yOffset = yOffset
        self.firstMS = firstMS
        self.repeatMS = repeatMS
        self.hitSFX = hitSFX
        self.loop = False
    def getLoop(self):
        return self.loop
    def run(self):
        global GRAVITY_TICK
        if self.yOffset > 0 and not is_overlapped(BLOCK.xpos, BLOCK.ypos+1, BLOCK.turn):
            GRAVITY_TICK = 0
            if SETTINGS['HANDLING'].getValue('SDF') == 40.1:  # SDF = 40.1 = ∞
                if move_end(0, 1) > 0:
                    self.hitSFX.play()
                KEY_INF_MOVE('ARR', 0, 'MOVE FALLING PIECE RIGHT', MOVE_THREAD, 1, 0)
                KEY_INF_MOVE('ARR', 0, 'MOVE FALLING PIECE LEFT', MOVE_THREAD, -1, 0)
                self.loop = True
                return
        if self.firstMS != -1:
            if not is_overlapped(BLOCK.xpos + self.xOffset, BLOCK.ypos + self.yOffset, BLOCK.turn):
                BLOCK.move(BLOCK.xpos + self.xOffset, BLOCK.ypos + self.yOffset)
                KEY_INF_MOVE('SDF', 40.1, 'SOFT DROP', DOWN_THREAD, 0, 1)
                self.hitSFX.play()
            time.sleep(0.001 * self.firstMS)
        if not self.is_stop() and SETTINGS['HANDLING'].getValue('ARR') == 0:
            if is_KEY_PRESSED(self.KEY):
                if move_end(self.xOffset, 0) > 0:
                    self.hitSFX.play()
                KEY_INF_MOVE('SDF', 40.1, 'SOFT DROP', DOWN_THREAD, 0, 1)
                self.loop = True
            return
        while not self.is_stop():
            if is_KEY_PRESSED(self.KEY):
                if trymove(BLOCK.xpos + self.xOffset, BLOCK.ypos + self.yOffset, BLOCK.turn):
                    GRAVITY_TICK = 0 if self.yOffset > 0 else GRAVITY_TICK
                    self.hitSFX.play()
                    time.sleep(0.001 * self.repeatMS)
            else:
                self.stop()

GAMEOVER = False
END_TICK = 0
def GameOver():
    global GAMEOVER, END_TICK
    GAMEOVER = True
    END_TICK = pygame.time.get_ticks()

def new_block(block):
    global BLOCK, GRAVITY_TICK, T_SPIN_STATE
    BLOCK = block
    T_SPIN_STATE = False
    if is_overlapped(BLOCK.xpos,BLOCK.ypos,BLOCK.turn):
        GameOver()
    GRAVITY_TICK = 0
    INF_MOVE_CHECK()
    return block

SWITCH_BLOCK = None
CAN_SWAP = True
def SWAP_PIECE():
    global SWITCH_BLOCK, BLOCK, CAN_SWAP
    if CAN_SWAP:
        CAN_SWAP = False
        switch_dump = BLOCK
        if SWITCH_BLOCK == None:
            SWITCH_BLOCK = Block(BLOCK.name)
            new_block(gen_block())
            return
        new_block(Block(SWITCH_BLOCK.name))
        SWITCH_BLOCK = Block(switch_dump.name)
        SFX['hold'].play()


CLEAR_LINES = 0
WARN = False

def CHECK_FIELD():
    global CLEAR_LINES,CURRENT_LEVEL,WARN
    Cleared_Line = 0
    ypos = HEIGHT - 1
    while ypos >= 0:
        if not 'B' in FIELD[ypos]:
            Cleared_Line = Cleared_Line + 1
            xpos = 0
            for blockcode in FIELD[ypos]:
                PARTICLE_SYSTEM.add_dirt_particle(random.uniform(X_OFFSET,X_OFFSET+WIDTH*TEXTURE_WIDTH), Y_OFFSET+(ypos+random.uniform(0,1))*TEXTURE_HEIGHT,[random.uniform(-TEXTURE_WIDTH * 5,TEXTURE_WIDTH * 5), random.uniform(0,-TEXTURE_HEIGHT * 5)],random.uniform(4, TEXTURE_WIDTH/2),BLOCK_COLORS[blockcode],random.uniform(240,720),random.uniform(0.5,1.5))
                PARTICLE_SYSTEM.add_residual_particle(X_OFFSET+xpos*TEXTURE_WIDTH, Y_OFFSET+ypos*TEXTURE_HEIGHT,[random.uniform(-TEXTURE_WIDTH * 3,TEXTURE_WIDTH * 3), random.uniform(-TEXTURE_HEIGHT * 3,TEXTURE_HEIGHT * 3)],random.choice([-1,1])*random.uniform(30,90),[TEXTURE_WIDTH,TEXTURE_HEIGHT],BLOCK_COLORS[blockcode],.1, .5)
                xpos = (xpos + 1) % WIDTH
            del FIELD[ypos]
            newLine = ['B'] * WIDTH
            FIELD.insert(0, newLine)
        else:
            ypos -= 1
    if Cleared_Line > 0:
        SFX[('combo_'+str(min(COMBO,16))+('_power' if Cleared_Line == 4 or T_SPIN_STATE == True else '')) if COMBO > 0 else ('clearquad' if Cleared_Line >= 4 else ('clearline' if T_SPIN_STATE == False else 'clearspin'))].play()
        CLEAR_LINES += Cleared_Line
        if CURRENT_LEVEL < min(int(CLEAR_LINES / 20),14):
            SFX['levelup'].play()
        CURRENT_LEVEL = min(int(CLEAR_LINES / 20),14)
        COUNT_BOARD['LINES'] = str(CLEAR_LINES)
        if FIELD[HEIGHT-1] == EMPTY_LINE:
            SFX['allclear'].play()
    elif COMBO > 2:
        SFX['combobreak'].play()
    for i in range(4):
        if FIELD[i] != EMPTY_LINE:
            WARN = True
        else:
            WARN = False
    return Cleared_Line

# 전역 변수
KEY_STATE = { K_UP: False, K_DOWN: False, K_LEFT: False, K_RIGHT: False }
FIELD = [[0 for _ in range(WIDTH)] for _ in range(HEIGHT)]

pygame.init()
SURFACE = pygame.display.set_mode((1920, 1080))
FPS_CLOCK = pygame.time.Clock()
BLOCK = None

BAG = []


def gen_block():
    if len(BAG) <= 7:
        NEW_BAG = [Block(str(name)) for name in BLOCKS.keys()]
        random.shuffle(NEW_BAG)
        BAG.extend(NEW_BAG)
    block = BAG[0]
    del BAG[0]
    return block


def is_overlapped(xpos, ypos, turn): #해당부분 멀티 쓰레드로 사용하여도 시간복잡도 + 짧은 반복 텀 때매 프레임 드랍..; *해결
    data = BLOCK.type[turn]
    for y_offset in range(BLOCK.size):
        for x_offset in range(BLOCK.size):
            if 0 <= xpos + x_offset < WIDTH and 0 <= ypos + y_offset < HEIGHT:
                if (data[y_offset * BLOCK.size + x_offset] != 'B') and (FIELD[ypos + y_offset][xpos + x_offset] != 'B'):
                    return True
            elif data[y_offset * BLOCK.size + x_offset] != 'B':
                return True
    return False

def DRAW_PREVIEW_BLOCK(PREVIEW_BLOCK, x_Offset, y_Offset):
    for posY in range(PREVIEW_BLOCK.size):
        for posX in range(PREVIEW_BLOCK.size):
            value = PREVIEW_BLOCK.data[posX + posY * PREVIEW_BLOCK.size]
            if value != 'B':
                Block_yOffset = 37 / 2
                if value == 'O':
                    Block_yOffset = 0
                SURFACE.blit(PREVIEW_TEXTURE[value], (posX * 37 + x_Offset, posY * 37 + y_Offset + Block_yOffset))

BTB_CHAIN = 0
LAST_CLEAR_LINE = 1
LAST_CLEAR_TIME = -99999
LAST_T_SPIN_STATE = False
def DRAW_SUBBOARD():
    # HOLD_PN
    pygame.draw.rect(SURFACE, COLORS['WHITE'], (X_OFFSET - 176, Y_OFFSET + TEXTURE_HEIGHT * 2, 176, 135))
    pygame.draw.rect(SURFACE, COLORS['BLACK'], (X_OFFSET - 176 + 4, Y_OFFSET + TEXTURE_HEIGHT * 2 + 34, 168, 97))                       # HOLD_PN 영역 168 x 97
    HOLD_text = FONTS['SUB_BOARD_TITLE'].render('HOLD', True, COLORS['BLACK'])
    SURFACE.blit(HOLD_text, (X_OFFSET - 176 + 8, Y_OFFSET + TEXTURE_HEIGHT * 2 + 3))
    if SWITCH_BLOCK != None:
        DRAW_PREVIEW_BLOCK(SWITCH_BLOCK, X_OFFSET - 172 + (168 - SWITCH_BLOCK.size * 37) / 2, Y_OFFSET + TEXTURE_HEIGHT * 2 + 34 + (97 - SWITCH_BLOCK.size * 37) / 2)
    #COMBO TRIGGER
    INFO_OFFSET = Y_OFFSET + TEXTURE_HEIGHT * 2 + 170
    #DRAW SHADOW STRING
    SHADOW_SIZE = 3
    if (pygame.time.get_ticks()-LAST_CLEAR_TIME)/1000 < 3: # under 3 Seconds
        LINE_FONT_SHADOW = FONTS['BROKEN_LINE'].render(LINE_STR_PREFIX[LAST_CLEAR_LINE - 1], True, COLORS['BLACK'])
        LINE_FONT        = FONTS['BROKEN_LINE'].render(LINE_STR_PREFIX[LAST_CLEAR_LINE - 1], True, COLORS['WHITE'])
        SURFACE.blit(LINE_FONT_SHADOW,  (X_OFFSET - LINE_FONT_SHADOW.get_width() - 10 + SHADOW_SIZE, INFO_OFFSET + 30 + SHADOW_SIZE))
        SURFACE.blit(LINE_FONT ,        (X_OFFSET - LINE_FONT.get_width()  - 10, INFO_OFFSET + 30))
        if LAST_T_SPIN_STATE:
            SPIN_FONT_SHADOW    = FONTS['SPIN_TYPE'].render('T-SPIN', True, COLORS['BLACK'])
            SPIN_FONT           = FONTS['SPIN_TYPE'].render('T-SPIN', True, (190, 80, 200))
            SURFACE.blit(SPIN_FONT_SHADOW,  (X_OFFSET - SPIN_FONT_SHADOW.get_width() - 10 + SHADOW_SIZE, INFO_OFFSET + SHADOW_SIZE))
            SURFACE.blit(SPIN_FONT,         (X_OFFSET - SPIN_FONT.get_width() - 10, INFO_OFFSET))
        if BTB_CHAIN > 1:
            BTB_FONT_SHADOW = FONTS['BTB_CHAIN'].render('BACK-TO-BACK' + (' X' + str(BTB_CHAIN-1) if BTB_CHAIN > 2 else ''), True, COLORS['BLACK'])
            BTB_FONT        = FONTS['BTB_CHAIN'].render('BACK-TO-BACK' + (' X' + str(BTB_CHAIN-1) if BTB_CHAIN > 2 else ''),True, (246, 210, 99))
            SURFACE.blit(BTB_FONT_SHADOW,
                         (X_OFFSET - BTB_FONT_SHADOW.get_width() - 10 + SHADOW_SIZE, INFO_OFFSET + 85 + SHADOW_SIZE))
            SURFACE.blit(BTB_FONT, (X_OFFSET - BTB_FONT.get_width() - 10, INFO_OFFSET + 85))
    if COMBO > 1:
        COMBO_FONT_SHADOW = FONTS['COMBO'].render(str(COMBO-1) + ' COMBO', True, COLORS['BLACK'])
        COMBO_FONT        = FONTS['COMBO'].render(str(COMBO-1) + ' COMBO', True, COLORS['WHITE'])
        SURFACE.blit(COMBO_FONT_SHADOW, (X_OFFSET - COMBO_FONT_SHADOW.get_width() - 10 + SHADOW_SIZE, INFO_OFFSET + 135 + SHADOW_SIZE))
        SURFACE.blit(COMBO_FONT,        (X_OFFSET - COMBO_FONT.get_width() - 10, INFO_OFFSET + 135))

    #NEXT_PN
    pygame.draw.rect(SURFACE, COLORS['WHITE'], (X_OFFSET + WIDTH * TEXTURE_WIDTH, Y_OFFSET + TEXTURE_HEIGHT * 2, 184, 563))
    pygame.draw.rect(SURFACE, COLORS['BLACK'], (X_OFFSET + WIDTH * TEXTURE_WIDTH + 4, Y_OFFSET + TEXTURE_HEIGHT * 2 + 34, 176, 525))    # NEXT_PN 영역 176 x 525
    NEXT_text = FONTS['SUB_BOARD_TITLE'].render('NEXT', True, COLORS['BLACK'])
    SURFACE.blit(NEXT_text, (X_OFFSET + WIDTH * TEXTURE_WIDTH + 8, Y_OFFSET + TEXTURE_HEIGHT * 2 + 3))
    cnt = 0
    for NEXT_BLOCK in BAG[0:5]:
        DRAW_PREVIEW_BLOCK(NEXT_BLOCK, X_OFFSET + WIDTH * TEXTURE_WIDTH + 4 + (176 - 37 * NEXT_BLOCK.size) / 2, Y_OFFSET + cnt * (525 / 5) + ((525 / 5) - NEXT_BLOCK.size * 37) / 2 + TEXTURE_HEIGHT * 2 + 34)
        cnt += 1

START_TICK = None
COUNT_BOARD = {'TIME' : '0:00.000', 'LINES' : '0', 'PIECES' : '0, 0.00/S', 'INPUTS' : '0, 0.00/P'}
def DRAW_COUNT_BOARD():
    ELAPSED_TIME = (pygame.time.get_ticks() if not GAMEOVER else END_TICK) - START_TICK
    MINUTES = ELAPSED_TIME // 60000
    SECONDS = (ELAPSED_TIME % 60000) // 1000
    MS = (ELAPSED_TIME % 60000) % 1000
    NOW_TIME = str(MINUTES) + ":" + ('0' if SECONDS < 10 else '') + str(SECONDS) + "." + (
        '00' if MS < 10 else '0' if MS < 100 else '') + str(MS);
    COUNT_BOARD['TIME']     = str(format(MINUTES, '01')) + ':' + str(format(SECONDS, '02')) + '.' + str(format(MS, '03'))
    COUNT_BOARD['PIECES']   = str(DROPED_PIECE) + ', ' + str(format(1000 * DROPED_PIECE / ELAPSED_TIME, '0.2f')) + '/S'
    cnt = 0
    for key,item in COUNT_BOARD.items():
        cnt += 1
        TITLE = FONTS['COUNT_BOARD_TITLE'].render(key,  True, COLORS['LIGHT_GRAY'])
        TITLE_SHADOW = FONTS['COUNT_BOARD_TITLE'].render(key, True, COLORS['BLACK'])
        VALUE = FONTS['COUNT_BOARD_VALUE'].render(item, True, COLORS['WHITE'])
        VALUE_SHADOW = FONTS['COUNT_BOARD_VALUE'].render(item, True, COLORS['BLACK'])
        SHADOW_SIZE = 3
        SURFACE.blit(TITLE_SHADOW, (X_OFFSET - TITLE_SHADOW.get_width() - 10 + SHADOW_SIZE, Y_OFFSET + TEXTURE_HEIGHT * HEIGHT - 60 * cnt + SHADOW_SIZE))
        SURFACE.blit(VALUE_SHADOW, (X_OFFSET - VALUE_SHADOW.get_width() - 10 + SHADOW_SIZE, Y_OFFSET + TEXTURE_HEIGHT * HEIGHT + 20 - 60 * cnt + SHADOW_SIZE))
        SURFACE.blit(TITLE, (X_OFFSET - TITLE.get_width() - 10, Y_OFFSET + TEXTURE_HEIGHT * HEIGHT - 60 * cnt))
        SURFACE.blit(VALUE, (X_OFFSET - VALUE.get_width() - 10, Y_OFFSET + TEXTURE_HEIGHT * HEIGHT + 20 - 60 * cnt))

#Debug Module
def retry():
    global BAG, BLOCK, SWITCH_BLOCK, WARN, START_TICK, DROPED_PIECE, INPUT_KEYS, CLEAR_LINES, CURRENT_LEVEL, GAMEOVER, BTB_CHAIN, COMBO, CAN_SWAP
    BAG = []
    SWITCH_BLOCK = None
    WARN = GAMEOVER = False
    CAN_SWAP = True
    START_TICK = pygame.time.get_ticks()
    DROPED_PIECE = INPUT_KEYS = CLEAR_LINES = CURRENT_LEVEL = COMBO = BTB_CHAIN = 0
    COUNT_BOARD['INPUTS'] = str(INPUT_KEYS) + ', ' + str(format(INPUT_KEYS / (DROPED_PIECE + 1), '0.2f')) + '/P'
    COUNT_BOARD['LINES'] = str(CLEAR_LINES)
    for ypos in range(HEIGHT):
        for xpos in range(WIDTH):
            FIELD[ypos][xpos] = 'B'
    BLOCK = new_block(gen_block())

# 텍스쳐 데이터 값은 파일로 관리 하면 좋을 것.
MUSIC_ENDED = pygame.USEREVENT
pygame.mixer.music.set_endevent(MUSIC_ENDED)
PARTICLE_SYSTEM = ParticlePrinciple()
GRAVITY_TICK = 0
INPUT_KEYS = 0
GRAVITY_DELTA = 0
GRAVITY_LEVEL = [0.01667, 0.021017, 0.026977, 0.035256, 0.04693, 0.06361, 0.0879, 0.1236, 0.1775, 0.2598, 0.388, 0.59, 0.92, 1.46, 2.36]
CURRENT_LEVEL = 0
MOVE_THREAD = None
DOWN_THREAD = None
def initialize_Game(surface):
    global BLOCK, BLOCK_TEXTURE, START_TICK, GRAVITY_TICK, INPUT_KEYS, BGM_INDEX, SURFACE, GRAVITY_DELTA, MOVE_THREAD, DOWN_THREAD, getTicksLastFrame
    SURFACE = surface
    RELOAD_SETTINGS()
    if BLOCK is None:
        BLOCK = gen_block()
    for ypos in range(HEIGHT):
        for xpos in range(WIDTH):
            FIELD[ypos][xpos] = 'B'
    counter = 0
    retry()
    START_TICK = pygame.time.get_ticks()
    getTicksLastFrame = START_TICK
    pygame.mixer.music.load(BACKGROUND_MUSICS[BGM_INDEX])
    pygame.mixer.music.play()
    while True:
        tick = pygame.time.get_ticks()
        deltaTime = (tick - getTicksLastFrame) / 1000.0
        getTicksLastFrame = tick
        SURFACE.blit(BACKGROUNDS[BACKGROUND_INDEX], (0, 0))
        pygame.draw.lines(SURFACE, COLORS['WHITE'], False, [[X_OFFSET - 2, Y_OFFSET + TEXTURE_HEIGHT * 2],[X_OFFSET - 2, Y_OFFSET + TEXTURE_HEIGHT * HEIGHT], [X_OFFSET + 1 + TEXTURE_WIDTH * WIDTH, Y_OFFSET + TEXTURE_HEIGHT * HEIGHT], [X_OFFSET + 1 + TEXTURE_WIDTH * WIDTH, Y_OFFSET + TEXTURE_HEIGHT * 2]],4)
        GB = SETTINGS['GAMEPLAY'].getValue('GRID VISIBILITY') * 2.55
        s = pygame.Surface((TEXTURE_WIDTH * WIDTH, TEXTURE_HEIGHT * HEIGHT), pygame.SRCALPHA)
        pygame.draw.rect(s, (GB, GB, GB), (0, TEXTURE_HEIGHT * 2, WIDTH * TEXTURE_WIDTH, HEIGHT * TEXTURE_HEIGHT - TEXTURE_HEIGHT * 2 + 4 * 2 - 4 * 2))
        for ypos in range(HEIGHT):
            for xpos in range(WIDTH):
                value = FIELD[ypos][xpos]
                if ypos > 1:
                    pygame.draw.rect(s, COLORS['BLACK'], (xpos * TEXTURE_WIDTH, ypos * TEXTURE_HEIGHT, TEXTURE_WIDTH - 1, TEXTURE_HEIGHT - 1))
        s.set_alpha(255 * (SETTINGS['GAMEPLAY'].getValue('BOARD VISIBILITY') / 100))
        SURFACE.blit(s, (X_OFFSET, Y_OFFSET))
        for ypos in range(HEIGHT):
            for xpos in range(WIDTH):
                value = FIELD[ypos][xpos]
                if value != 'B':
                    SURFACE.blit(BLOCK_TEXTURE[value],(X_OFFSET + xpos * TEXTURE_WIDTH, Y_OFFSET + ypos * TEXTURE_HEIGHT))
        if not GAMEOVER and GRAVITY_TICK >= 1:
            GRAVITY_TICK -= 1
            BLOCK.Gravity()
        GRAVITY_TICK += deltaTime * GRAVITY_LEVEL[CURRENT_LEVEL] * 60
        GRAVITY_DELTA += deltaTime
        DRAW_COUNT_BOARD()
        DRAW_SUBBOARD()
        BLOCK.draw()
        if WARN:
            BAG[0].draw_Warn()
        for event in pygame.event.get():
            if event.type == KEYDOWN:
                key = event.key
                if key in SETTINGS['CONTROLS'].getValue('FOREIT GAME'):
                    if MOVE_THREAD is not None:
                        MOVE_THREAD.stop()
                    if DOWN_THREAD is not None:
                        DOWN_THREAD.stop()
                    pygame.mixer.music.load(TITLE_MUSIC)
                    pygame.mixer.music.play(-1)
                    return
                if not GAMEOVER:
                    INPUT_KEYS += 1
                    if key in SETTINGS['CONTROLS'].getValue('MOVE FALLING PIECE RIGHT'):
                        if MOVE_THREAD is not None:
                            MOVE_THREAD.stop()
                        MOVE_THREAD = MoveKeyThread('MOVE FALLING PIECE RIGHT', 1, 0, SETTINGS['HANDLING'].getValue('DAS') * FRAMES, SETTINGS['HANDLING'].getValue('ARR') * FRAMES, SFX['hit'])
                        MOVE_THREAD.start()
                    elif key in SETTINGS['CONTROLS'].getValue('MOVE FALLING PIECE LEFT'):
                        if MOVE_THREAD is not None:
                            MOVE_THREAD.stop()
                        MOVE_THREAD = MoveKeyThread('MOVE FALLING PIECE LEFT', -1, 0, SETTINGS['HANDLING'].getValue('DAS') * FRAMES, SETTINGS['HANDLING'].getValue('ARR') * FRAMES, SFX['hit'])
                        MOVE_THREAD.start()
                    elif key in SETTINGS['CONTROLS'].getValue('SOFT DROP'):
                        if DOWN_THREAD is not None:
                            DOWN_THREAD.stop()
                        DOWN_THREAD = MoveKeyThread('SOFT DROP', 0, 1, 250 / SETTINGS['HANDLING'].getValue('SDF'), 250 / SETTINGS['HANDLING'].getValue('SDF'), SFX['hit'])
                        DOWN_THREAD.start()
                    elif key in SETTINGS['CONTROLS'].getValue('HARD DROP'):
                        BLOCK.hard_drop()
                    elif key in SETTINGS['CONTROLS'].getValue('ROTATE CLOCKWISE'):
                        BLOCK.rotate(1)
                    elif key in SETTINGS['CONTROLS'].getValue('ROTATE COUNTERCLOCKWISE'):
                        BLOCK.rotate(-1)
                    elif key in SETTINGS['CONTROLS'].getValue('ROTATE 180'):
                        BLOCK.rotate(2)
                    elif key in SETTINGS['CONTROLS'].getValue('SWAP HOLD PIECE'):
                        SWAP_PIECE()
                    else:
                        INPUT_KEYS -= 1
                    COUNT_BOARD['INPUTS'] = str(INPUT_KEYS) + ', ' + str(format(INPUT_KEYS / (DROPED_PIECE + 1), '0.2f')) + '/P'
                if key in SETTINGS['CONTROLS'].getValue('RETRY GAME'):
                    retry()
                KEY_STATE[event.key] = True
            elif event.type == KEYUP:
                KEY_STATE[event.key] = False
            elif event.type == MUSIC_ENDED:
                BGM_INDEX = (BGM_INDEX + 1) % len(BACKGROUND_MUSICS)
                pygame.mixer.music.load(BACKGROUND_MUSICS[BGM_INDEX])
                pygame.mixer.music.play()
        counter = counter + 1
        fps_text = f'{int(FPS_CLOCK.get_fps())} FPS'
        fps_label_shadow = FONTS['LIVE_FPS'].render(fps_text, True, COLORS['BLACK'])
        fps_label = FONTS['LIVE_FPS'].render(fps_text, True, COLORS['WHITE'])
        SURFACE.blit(fps_label_shadow, (52, 52))
        SURFACE.blit(fps_label, (50, 50))
        PARTICLE_SYSTEM.emit(SURFACE, deltaTime)
        if GAMEOVER:
            s = pygame.Surface((SCREEN_SIZE_WIDTH, 300))
            pygame.draw.rect(s,(255,0,0),(0,0,SCREEN_SIZE_WIDTH,300))
            s.set_alpha(230)
            SURFACE.blit(s, (0,(SCREEN_SIZE_HEIGHT - 300)/2))
            ELAPSED_TIME_ANIM = pygame.time.get_ticks() - END_TICK
            ELAPSED_SECONDS = ELAPSED_TIME_ANIM / 1000
            GAMEOVER_TITLE_SHADOW = FONTS['CURTAIN_DISC'].render('GAME OVER', True, COLORS['BLACK'])
            GAMEOVER_TITLE = FONTS['CURTAIN_DISC'].render('GAME OVER', True, COLORS['WHITE'])
            GAMEOVER_TITLE_SUB = FONTS['CURTAIN_DISC_SUB'].render('PRESS R TO RETRY', True, COLORS['WHITE'])
            SHADOW_SIZE = 5
            SURFACE.blit(GAMEOVER_TITLE_SHADOW, ((SCREEN_SIZE_WIDTH - GAMEOVER_TITLE_SHADOW.get_width()) / 2 + SHADOW_SIZE, (SCREEN_SIZE_HEIGHT - GAMEOVER_TITLE_SHADOW.get_height()) / 2 + SHADOW_SIZE-GAMEOVER_TITLE_SUB.get_height()/2))
            SURFACE.blit(GAMEOVER_TITLE, ((SCREEN_SIZE_WIDTH-GAMEOVER_TITLE.get_width())/2, (SCREEN_SIZE_HEIGHT-GAMEOVER_TITLE.get_height())/2-GAMEOVER_TITLE_SUB.get_height()/2))
            if ELAPSED_SECONDS % 1 >= 0.5:
                SURFACE.blit(GAMEOVER_TITLE_SUB, ((SCREEN_SIZE_WIDTH - GAMEOVER_TITLE_SUB.get_width()) / 2, 585-GAMEOVER_TITLE_SUB.get_height()/2))
        pygame.display.update()
        FPS_CLOCK.tick(SETTINGS['VIDEO'].getValue('MAX FRAME'))

def RELOAD_SETTINGS():
    global LOADED_TEXTURES, BLOCK_TEXTURE, TEXTURE_WIDTH, TEXTURE_HEIGHT, X_OFFSET, Y_OFFSET, BACKGROUND_INDEX, PREVIEW_TEXTURE
    for sfx in SFX.values():
        sfx.set_volume(SETTINGS['VOLUME & AUDIO'].getValue('SFX') / 100)
    BACKGROUND_INDEX = random.randint(0, len(BACKGROUNDS) - 1)
    pygame.mixer.music.set_volume(SETTINGS['VOLUME & AUDIO'].getValue('MUSIC') / 100)
    TEXTURE_WIDTH   = round(37 * (SETTINGS['GAMEPLAY'].getValue('BOARD ZOOM') / 100))
    TEXTURE_HEIGHT  = round(37 * (SETTINGS['GAMEPLAY'].getValue('BOARD ZOOM') / 100))
    X_OFFSET = (SCREEN_SIZE_WIDTH - WIDTH * TEXTURE_WIDTH + 2) / 2
    Y_OFFSET = (SCREEN_SIZE_HEIGHT - (HEIGHT + 1) * TEXTURE_HEIGHT + 2) / 2
    for SKIN_PATH in os.listdir('./Resource/Tetromino/'):
        SKIN_CODE = SKIN_PATH.split('.')[0]
        LOADED_TEXTURES[SKIN_CODE] = {}
        image_source = pygame.image.load('./Resource/Tetromino/'+SKIN_PATH)
        TEXTURE_INFO = TEXTURE_LOAD_SORT[str(image_source.get_width())+'x'+str(image_source.get_height())]
        U,V = TEXTURE_INFO[0]
        image = pygame.transform.scale(image_source, (TEXTURE_WIDTH * U, TEXTURE_HEIGHT * V))
        cnt = 0
        for key in list(BLOCKS.keys()) + TEXTURE_INFO[1]: #dict_keys -> list
            picture = pygame.Surface((TEXTURE_WIDTH, TEXTURE_HEIGHT),pygame.SRCALPHA)
            picture.blit(image, (-TEXTURE_WIDTH * (cnt % U), -TEXTURE_HEIGHT * (cnt // U)))
            LOADED_TEXTURES[SKIN_CODE][key] = picture
            cnt += 1
        LOADED_TEXTURES[SKIN_CODE]['SHADOW'].set_alpha(2.56 * SETTINGS['GAMEPLAY'].getValue('SHADOW VISIBILITY'))
    BLOCK_TEXTURE = LOADED_TEXTURES[SKIN_SORT[Material.CURRENT_SKIN_INDEX]]
    PREVIEW_TEXTURE = PREVIEW_TEXTURES[SKIN_SORT[Material.CURRENT_SKIN_INDEX]]

if __name__ == '__main__':
    initialize_Game(SURFACE)

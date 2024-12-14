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

T_SPIN_STATE = False
DROPED_PIECE = 0
COMBO = 0
current_cnt = 0
WIDTH = 10
HEIGHT = 12
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

class Block:
    def __init__(self, name):
        self.turn = random.randint(0,3)
        self.name = name
        self.type = BLOCKS[name]
        self.data = self.type[self.turn]
        self.size = int(sqrt(len(self.data)))
        self.xpos = (WIDTH - self.size) // 2
        self.ypos = 0
        self.velocity_y = 0
        self.last_fall_time = time.time()

    def initialize(self):
        self.xpos = (WIDTH - self.size) // 2
        self.ypos = 0
        self.velocity_y = 0
        self.last_fall_time = time.time()
        return self

    def draw(self):
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
                BRIGHTNESS_BRUSH = pygame.Surface((TEXTURE_WIDTH, TEXTURE_HEIGHT), pygame.SRCALPHA)
                pygame.draw.rect(BRIGHTNESS_BRUSH, (0, 0, 0, 50), (0, 0, TEXTURE_WIDTH, TEXTURE_HEIGHT))
                SURFACE.blit(BRIGHTNESS_BRUSH, (x_pos, y_pos))
                
    def move(self, xPos, yPos):
        self.xpos = xPos
        self.ypos = yPos

    def place(self):
        global BLOCK, DROPED_PIECE, COMBO, LAST_CLEAR_LINE, LAST_CLEAR_TIME
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
        COMBO = COMBO + 1 if CLEARED_LINES > 0 else 0
        if CLEARED_LINES > 0:
            COMBO = COMBO + 1
            LAST_CLEAR_LINE = CLEARED_LINES
            LAST_CLEAR_TIME = pygame.time.get_ticks()
            #BREAK LINE EFFECT
        else:
            COMBO = 0
            for x, y in PLACED_BLOCKS:
                PARTICLE_SYSTEM.add_clensing_particle(X_OFFSET + (self.xpos + x) * TEXTURE_WIDTH, Y_OFFSET + (self.ypos + y) * TEXTURE_HEIGHT, TEXTURE_WIDTH, TEXTURE_HEIGHT, (255,255,255,50), .05, .25)
        BLOCK = new_block(gen_block())

    # def Gravity(self):
    #     current_time = time.time()
        
    #     if current_time - self.last_fall_time >= 1000 / 60 * BLOCK.GRAVITY:
    #         self.ypos +=  1
    #         self.last_fall_time = current_time
        
        
    #     if self.ypos > HEIGHT - 1:
    #         self.ypos = HEIGHT - 1
    #         self.velocity_y = 0
    #         return 'over'

    #     if self.ypos < 0:
    #         self.ypos = 0
    #         self.velocity_y = 0
    
    def Place_block(self):
        global current_cnt
        SFX['harddrop'].play()
        CAN_PLACE = True
        for y_offset in range(self.size):
            for x_offset in range(self.size):
                if not (0 <= self.xpos + x_offset < WIDTH and 2 <= self.ypos + y_offset < HEIGHT):
                    if self.type[self.turn][y_offset * self.size + x_offset] != 'B':
                        CAN_PLACE = False
        if CAN_PLACE and not is_overlapped(self.xpos, self.ypos, self.turn):
            self.place()
            del BAG[current_cnt]
            gen_block()
            if current_cnt >= len(BAG):
                current_cnt = 0
            new_block(BAG[current_cnt])
        min_x,max_x = (3,0)
        for y_offset in range(self.size):
            for x_offset in range(self.size):
                val = self.data[y_offset * self.size + x_offset]
                if val != 'B':
                    min_x = min(min_x, x_offset)
                    max_x = max(max_x, x_offset)
        for i in range(random.randint(1,4)):
            PARTICLE_SYSTEM.add_bubble_particle(TEXTURE_WIDTH * (self.xpos+random.uniform(min_x,max_x))+ random.uniform(0,1) * TEXTURE_HEIGHT + X_OFFSET, (self.ypos+random.uniform(0,1)) * TEXTURE_HEIGHT + Y_OFFSET, 4, [0, -300], BLOCK_COLORS[self.name])

def trymove(posX, posY, turn):
    if canmove(posX, posY, turn):
        BLOCK.move(posX, posY)
        return True
    return False

def movekey(KEY, xOffset, yOffset, firstMS, repeatMS, hitSFX):
    # 첫 이동 시
    if trymove(BLOCK.xpos + xOffset, BLOCK.ypos + yOffset, BLOCK.turn):
        hitSFX.play()
    time.sleep(0.001 * firstMS)
    
    # 반복 이동 시
    while KEY_STATE[KEY]:
        if trymove(BLOCK.xpos + xOffset, BLOCK.ypos + yOffset, BLOCK.turn):
            hitSFX.play()
        time.sleep(0.001 * repeatMS)

def new_block(block):
    global BLOCK
    BLOCK = block.initialize()
    return block

SWITCH_BLOCK = None

def SWAP_PIECE(direction):
    global BLOCK, BAG, current_cnt
    if len(BAG) > 1:
        current_cnt = (current_cnt + direction) % len(BAG)
        new_block(BAG[current_cnt])
        SFX['hold'].play()
    
    # global SWITCH_BLOCK, BLOCK
    # switch_dump = BLOCK
    # if SWITCH_BLOCK == None:
    #     SWITCH_BLOCK = Block(BLOCK.name)
    #     new_block(gen_block())
    #     return
    # new_block(Block(SWITCH_BLOCK.name))
    # SWITCH_BLOCK = Block(switch_dump.name)
    # SFX['hold'].play()

CLEAR_LINES = 0
WARN = False

def CHECK_FIELD():
    global CLEAR_LINES, WARN
    Cleared_Line = 0
    
    y_cnt = [0] * WIDTH  # 세로줄 카운트
    x_cnt = [0] * HEIGHT  # 가로줄 카운트

    # 세로줄 확인 및 가로줄 확인
    for y in range(2, HEIGHT):
        for x in range(WIDTH):
            if FIELD[y][x] != 'B':
                y_cnt[x] += 1
        if all(FIELD[y][x] != 'B' for x in range(WIDTH)):
            x_cnt[y] = 1

    # 가로/세로
    for x in range(WIDTH):
        if y_cnt[x] >= 10:
            for y in range(HEIGHT):
                PARTICLE_SYSTEM.add_dirt_particle(X_OFFSET + (x + random.uniform(0, 1)) * TEXTURE_WIDTH, random.uniform(Y_OFFSET, Y_OFFSET + HEIGHT * TEXTURE_HEIGHT), [random.uniform(-TEXTURE_WIDTH * 5, TEXTURE_WIDTH * 5), random.uniform(0, -TEXTURE_HEIGHT * 5)], random.uniform(4, TEXTURE_WIDTH / 2), BLOCK_COLORS[FIELD[y][x]], random.uniform(240, 720), random.uniform(0.5, 1.5))
                PARTICLE_SYSTEM.add_residual_particle(X_OFFSET + x * TEXTURE_WIDTH, Y_OFFSET + y * TEXTURE_HEIGHT,[random.uniform(-TEXTURE_WIDTH * 3, TEXTURE_WIDTH * 3), random.uniform(-TEXTURE_HEIGHT * 3, TEXTURE_HEIGHT * 3)], random.choice([-1, 1]) * random.uniform(30, 90), [TEXTURE_WIDTH, TEXTURE_HEIGHT], BLOCK_COLORS[FIELD[y][x]], .1, .5)
                FIELD[y][x] = 'B'  # 세로줄 클리어
            Cleared_Line += 1
    for y in range(HEIGHT):
        if x_cnt[y] == 1:
            for x in range(WIDTH):
                PARTICLE_SYSTEM.add_dirt_particle(random.uniform(X_OFFSET, X_OFFSET + WIDTH * TEXTURE_WIDTH), Y_OFFSET + (y + random.uniform(0, 1)) * TEXTURE_HEIGHT, [random.uniform(-TEXTURE_WIDTH * 5, TEXTURE_WIDTH * 5), random.uniform(0, -TEXTURE_HEIGHT * 5)], random.uniform(4, TEXTURE_WIDTH / 2), BLOCK_COLORS[FIELD[y][x]], random.uniform(240, 720), random.uniform(0.5, 1.5))
                PARTICLE_SYSTEM.add_residual_particle(X_OFFSET + x * TEXTURE_WIDTH, Y_OFFSET + y * TEXTURE_HEIGHT, [random.uniform(-TEXTURE_WIDTH * 3, TEXTURE_WIDTH * 3), random.uniform(-TEXTURE_HEIGHT * 3, TEXTURE_HEIGHT * 3)], random.choice([-1, 1]) * random.uniform(30, 90), [TEXTURE_WIDTH, TEXTURE_HEIGHT], BLOCK_COLORS[FIELD[y][x]], .1, .5)
                FIELD[y][x] = 'B'  # 가로줄 클리어
            Cleared_Line += 1


                        
    if Cleared_Line > 0:
        SFX[('combo_'+str(min(COMBO,16))+('_power' if Cleared_Line == 4 or T_SPIN_STATE == True else '')) if COMBO > 0 else ('clearquad' if Cleared_Line >= 4 else ('clearline' if T_SPIN_STATE == False else 'clearspin'))].play()
        CLEAR_LINES += Cleared_Line
        COUNT_BOARD['LINES'] = str(CLEAR_LINES)
        if FIELD[HEIGHT-1] == EMPTY_LINE:
            SFX['allclear'].play()
    elif COMBO - 1 > 0:
        SFX['combobreak'].play()
    # for i in range(4):
    #     if FIELD[i] != EMPTY_LINE:
    #         WARN = True
    #     else:
    #         WARN = False
    return Cleared_Line

# 전역 변수
KEY_STATE = {K_UP: False, K_DOWN: False, K_LEFT: False, K_RIGHT: False}
BACKGROUND_COLOR = COLORS['WHITE']
FIELD = [[0 for _ in range(WIDTH)] for _ in range(HEIGHT)]

pygame.init()
pygame.display.set_caption('Tetris Classic')
SURFACE = pygame.display.set_mode((1920, 1080))
FPS_CLOCK = pygame.time.Clock()
BLOCK = None

BAG = []

# def gen_block():
#     if len(BAG) == 0:  # BAG에 블록이 없을 때만 새로운 3개의 블록을 추가
#         NEW_BAG = [Block(str(name)) for name in BLOCKS.keys()]  # BLOCKS에서 블록 생성
#         random.shuffle(NEW_BAG)  # 무작위로 섞기
#         BAG.extend(NEW_BAG[:3])

def gen_block():
    global current_cnt
    if len(BAG) <= 0:
        NEW_BAG = [Block(str(name)) for name in BLOCKS.keys()]
        random.shuffle(NEW_BAG)
        BAG.extend(NEW_BAG[:3])
    block = BAG[0]
    return block

def is_overlapped(xpos, ypos, turn):
    data = BLOCK.type[turn]
    for y_offset in range(BLOCK.size):
        for x_offset in range(BLOCK.size):
            if (0 <= xpos + x_offset < WIDTH) and (0 <= ypos + y_offset < HEIGHT):
                if (data[y_offset * BLOCK.size + x_offset] != 'B') and (FIELD[ypos + y_offset][xpos + x_offset] != 'B'):
                    return True
            elif data[y_offset * BLOCK.size + x_offset] != 'B': #### trymove
                return True
    return False


def QUIT():
    pygame.quit()
    sys.exit()


def draw_Borded_Rect(posX, posY, width, height, color, outline_color, outline_width):
    pygame.draw.rect(SURFACE, outline_color, (posX, posY, width, height))
    pygame.draw.rect(SURFACE, color, (
    posX + outline_width, posY + outline_width, width - outline_width * 2, height - outline_width * 2))

def DRAW_PREVIEW_BLOCK(PREVIEW_BLOCK, x_Offset, y_Offset):
    for posY in range(PREVIEW_BLOCK.size):
        for posX in range(PREVIEW_BLOCK.size):
            value = PREVIEW_BLOCK.data[posX + posY * PREVIEW_BLOCK.size]
            if value != 'B':
                Block_yOffset = 37 / 2
                if value == 'O':
                    Block_yOffset = 0
                SURFACE.blit(PREVIEW_TEXTURE[value], (posX * 37 + x_Offset, posY * 37 + y_Offset + Block_yOffset))

LAST_CLEAR_LINE = 1
LAST_CLEAR_TIME = -99999
def DRAW_SUBBOARD():
    if SWITCH_BLOCK != None:
        DRAW_PREVIEW_BLOCK(SWITCH_BLOCK, X_OFFSET - 172 + (168 - SWITCH_BLOCK.size * TEXTURE_WIDTH) / 2, Y_OFFSET + TEXTURE_HEIGHT * 2 + 34 + (97 - SWITCH_BLOCK.size * TEXTURE_HEIGHT) / 2)
        # COMBO TRIGGER
        INFO_OFFSET = Y_OFFSET + TEXTURE_HEIGHT * 2 + 170
        # DRAW SHADOW STRING
        SHADOW_SIZE = 3
        if (pygame.time.get_ticks() - LAST_CLEAR_TIME) / 1000 < 3:  # under 3 Seconds
            LINE_FONT_SHADOW = FONTS['BROKEN_LINE'].render(LINE_STR_PREFIX[LAST_CLEAR_LINE - 1], True, COLORS['BLACK'])
            LINE_FONT = FONTS['BROKEN_LINE'].render(LINE_STR_PREFIX[LAST_CLEAR_LINE - 1], True, COLORS['WHITE'])
            SURFACE.blit(LINE_FONT_SHADOW,
                         (X_OFFSET - LINE_FONT_SHADOW.get_width() - 10 + SHADOW_SIZE, INFO_OFFSET + 30 + SHADOW_SIZE))
            SURFACE.blit(LINE_FONT, (X_OFFSET - LINE_FONT.get_width() - 10, INFO_OFFSET + 30))
        if COMBO > 1:
            COMBO_FONT_SHADOW = FONTS['COMBO'].render(str(COMBO - 1) + ' COMBO', True, COLORS['BLACK'])
            COMBO_FONT = FONTS['COMBO'].render(str(COMBO - 1) + ' COMBO', True, COLORS['WHITE'])
            SURFACE.blit(COMBO_FONT_SHADOW,
                         (X_OFFSET - COMBO_FONT_SHADOW.get_width() - 10 + SHADOW_SIZE, INFO_OFFSET + 135 + SHADOW_SIZE))
            SURFACE.blit(COMBO_FONT, (X_OFFSET - COMBO_FONT.get_width() - 10, INFO_OFFSET + 135))
    #NEXT_PN
    pygame.draw.rect(SURFACE, COLORS['WHITE'], (X_OFFSET + WIDTH * TEXTURE_WIDTH + 1, Y_OFFSET + TEXTURE_HEIGHT * 2, 234, 563))
    pygame.draw.rect(SURFACE, COLORS['BLACK'], (X_OFFSET + WIDTH * TEXTURE_WIDTH + 5, Y_OFFSET + TEXTURE_HEIGHT * 2 + 34, 226, 525))    # NEXT_PN 영역 176 x 525
    NEXT_text = FONTS['SUB_BOARD_TITLE'].render('CURRENT BAG', True, COLORS['BLACK'])
    SURFACE.blit(NEXT_text, (X_OFFSET + WIDTH * TEXTURE_WIDTH + 9, Y_OFFSET + TEXTURE_HEIGHT * 2 + 3))
    cnt = 0
    for NEXT_BLOCK in BAG[0:3]:
        DRAW_PREVIEW_BLOCK(NEXT_BLOCK, X_OFFSET + WIDTH * TEXTURE_WIDTH + 5 + (226 - 37 * NEXT_BLOCK.size) / 2, Y_OFFSET + cnt * (675 / 5) + ((675 / 5) - NEXT_BLOCK.size * 37) / 2 + TEXTURE_HEIGHT * 2 + 34)
        cnt += 1

START_TICK = None
GAMEOVER = False
END_TICK = -9999
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
    global BAG, BLOCK, SWITCH_BLOCK, WARN, START_TICK, DROPED_PIECE, INPUT_KEYS
    BAG = []
    SWITCH_BLOCK = None
    WARN = False
    START_TICK = pygame.time.get_ticks()
    DROPED_PIECE = INPUT_KEYS = 0
    COUNT_BOARD['INPUTS'] = str(INPUT_KEYS) + ', ' + str(format(INPUT_KEYS / (DROPED_PIECE + 1), '0.2f')) + '/P'
    for ypos in range(HEIGHT):
        for xpos in range(WIDTH):
            FIELD[ypos][xpos] = 'B'
    BLOCK = new_block(gen_block())

# 텍스쳐 데이터 값은 파일로 관리 하면 좋을 것.
MUSIC_ENDED = pygame.USEREVENT
pygame.mixer.music.set_endevent(MUSIC_ENDED)
PARTICLE_SYSTEM = ParticlePrinciple()
INPUT_KEYS = 0

def canmove(posX,posY,turn): #텐바텐 전용 함수
    for y_offset in range(BLOCK.size):
        for x_offset in range(BLOCK.size):
            if (BLOCK.data[y_offset * BLOCK.size + x_offset] != 'B'):
                if not (0 <= posX+x_offset < WIDTH and 0 <= posY+y_offset < HEIGHT):
                    return False
    return True

def initialize_Game(surface):
    global BLOCK, BLOCK_TEXTURE, START_TICK, INPUT_KEYS, BGM_INDEX, SURFACE
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
    getTicksLastFrame = 0
    pygame.mixer.music.load(BACKGROUND_MUSICS[BGM_INDEX])
    pygame.mixer.music.play()
    while True:
        tick = pygame.time.get_ticks()
        deltaTime = (tick - getTicksLastFrame) / 1000.0
        getTicksLastFrame = tick
        SURFACE.blit(BACKGROUNDS[BACKGROUND_INDEX], (0, 0))
        pygame.draw.lines(SURFACE, COLORS['WHITE'], False, [[X_OFFSET - 2, Y_OFFSET + TEXTURE_HEIGHT * 2], [X_OFFSET - 2, Y_OFFSET + TEXTURE_HEIGHT * HEIGHT], [X_OFFSET + 1 + TEXTURE_WIDTH * WIDTH, Y_OFFSET + TEXTURE_HEIGHT * HEIGHT], [X_OFFSET + 1 + TEXTURE_WIDTH * WIDTH, Y_OFFSET + TEXTURE_HEIGHT * 2]], 4)
        GB = SETTINGS['GAMEPLAY'].getValue('GRID VISIBILITY') * 2.55
        s = pygame.Surface((TEXTURE_WIDTH * WIDTH, TEXTURE_HEIGHT * HEIGHT), pygame.SRCALPHA)
        pygame.draw.rect(s, (GB, GB, GB), (
        0, TEXTURE_HEIGHT * 2, WIDTH * TEXTURE_WIDTH, HEIGHT * TEXTURE_HEIGHT - TEXTURE_HEIGHT * 2 + 4 * 2 - 4 * 2))
        for ypos in range(HEIGHT):
            for xpos in range(WIDTH):
                value = FIELD[ypos][xpos]
                if ypos > 1:
                    pygame.draw.rect(s, COLORS['BLACK'], (
                    xpos * TEXTURE_WIDTH, ypos * TEXTURE_HEIGHT, TEXTURE_WIDTH - 1, TEXTURE_HEIGHT - 1))
        s.set_alpha(255 * (SETTINGS['GAMEPLAY'].getValue('BOARD VISIBILITY') / 100))
        SURFACE.blit(s, (X_OFFSET, Y_OFFSET))
        for ypos in range(HEIGHT):
            for xpos in range(WIDTH):
                value = FIELD[ypos][xpos]
                if value != 'B':
                    SURFACE.blit(BLOCK_TEXTURE[value], (X_OFFSET + xpos * TEXTURE_WIDTH, Y_OFFSET + ypos * TEXTURE_HEIGHT))
        DRAW_COUNT_BOARD()
        DRAW_SUBBOARD()
        BLOCK.draw()
        if WARN:
            BAG[0].draw_Warn()
        for event in pygame.event.get():
            if event.type == QUIT:
                quit()
            elif event.type == KEYDOWN:
                key = event.key
                INPUT_KEYS += 1
                if key in SETTINGS['CONTROLS'].getValue('FOREIT GAME'):
                    pygame.mixer.music.load(TITLE_MUSIC)
                    pygame.mixer.music.play(-1)
                    return
                elif key == K_RIGHT:
                    thread = Thread(target=movekey, args=(event.key, 1, 0, 10 * FRAMES, 2 * FRAMES, SFX['hit']), daemon=True)
                    thread.start()
                elif key == K_LEFT:
                    thread = Thread(target=movekey, args=(event.key, -1, 0, 10 * FRAMES, 2 * FRAMES, SFX['hit']), daemon=True)
                    thread.start()
                elif key == K_DOWN:
                    thread = Thread(target=movekey, args=(event.key, 0, 1, 10 * FRAMES, 2 * FRAMES, SFX['hit']), daemon=True)
                    thread.start()
                elif key == K_UP:
                    thread = Thread(target=movekey, args=(event.key, 0, -1, 10 * FRAMES, 2 * FRAMES, SFX['hit']), daemon=True)
                    thread.start()
                elif key in SETTINGS['CONTROLS'].getValue('ROTATE CLOCKWISE'):
                    SWAP_PIECE(1)
                elif key in SETTINGS['CONTROLS'].getValue('ROTATE COUNTERCLOCKWISE'):
                    SWAP_PIECE(-1)
                elif key == K_SPACE:
                    BLOCK.Place_block()
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
        pygame.display.update()
        FPS_CLOCK.tick(SETTINGS['VIDEO'].getValue('MAX FRAME'))

def RELOAD_SETTINGS():
    global LOADED_TEXTURES, BLOCK_TEXTURE, TEXTURE_WIDTH, TEXTURE_HEIGHT, X_OFFSET, Y_OFFSET, BACKGROUND_INDEX
    for sfx in SFX.values():
        sfx.set_volume(SETTINGS['VOLUME & AUDIO'].getValue('SFX') / 100)
    BACKGROUND_INDEX = random.randint(0, len(BACKGROUNDS) - 1)
    pygame.mixer.music.set_volume(SETTINGS['VOLUME & AUDIO'].getValue('MUSIC') / 100)
    TEXTURE_WIDTH   = round(37 * (SETTINGS['GAMEPLAY'].getValue('BOARD ZOOM') / 100) * 1.5)
    TEXTURE_HEIGHT  = round(37 * (SETTINGS['GAMEPLAY'].getValue('BOARD ZOOM') / 100) * 1.5)
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

if __name__ == '__main__':
    initialize_Game(SURFACE)
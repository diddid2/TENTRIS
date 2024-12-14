import sys
from math import sqrt
from threading import Thread
import random
import time

import pygame
from pygame.locals import *

import Material
from ClassicTetris import RELOAD_SETTINGS
from Material import *
from Settings import *
from Particle import *

GRAVITY_TICK = 0
T_SPIN_STATE = False
DROPED_PIECE = 0
COMBO = 0
WIDTH = 10
HEIGHT = 12
class Block:
    def __init__(self, name):
        self.turn = 0
        self.name = name
        self.type = BLOCKS[name]
        self.data = self.type[self.turn]
        self.size = int(sqrt(len(self.data)))
        self.xpos = (WIDTH - self.size) // 2
        self.ypos = 0
        self.velocity_y = 0
        self.last_fall_time = time.time()

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
                BLOCK_TEXTURE['WARN'].set_colorkey((0,0,0))
                SURFACE.blit(BLOCK_TEXTURE['WARN'], (x_pos, y_pos))
                
    def move(self, xPos, yPos):
        self.xpos = xPos
        self.ypos = yPos

    def rotate(self, rotation):
        global T_SPIN_STATE
        Newton = (self.turn + rotation) % 4 if self.turn > 0 or rotation >= 0 else 3
        for xOffset, yOffset in SRS_KICK_TABLE['DEFAULT' if self.name != 'I' else 'I'][rotation][self.turn]:
            if canmove(self.xpos + xOffset, self.ypos - yOffset, Newton):
                self.move(self.xpos + xOffset, self.ypos - yOffset)
                self.turn = Newton
                self.data = self.type[self.turn]
                SFX['rotate'].play()
                return

    def place(self):
        global BLOCK, DROPED_PIECE, COMBO, CLEARED_LINES, CAN_SWAP
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
        COMBO = COMBO + 1 if CLEARED_LINES > 0 else 0
        if CLEARED_LINES > 0:
            COMBO = COMBO + 1
            #BREAK LINE EFFECT
        else:
            COMBO = 0
            for x, y in PLACED_BLOCKS:
                PARTICLE_SYSTEM.add_clensing_particle(X_OFFSET + (self.xpos + x) * TEXTURE_WIDTH, Y_OFFSET + (self.ypos + y) * TEXTURE_HEIGHT, TEXTURE_WIDTH, TEXTURE_HEIGHT, (255,255,255,50), .05, .25)
        BLOCK = new_block(gen_block())

    def Gravity(self):
        global GRAVITY_DELTA, GRAVITY_TICK
        if canmove(self.xpos, self.ypos + 1, self.turn):
            if GRAVITY_DELTA >= 1:
                self.ypos = self.ypos + 1
            
        # if self.ypos > HEIGHT - 1:
        #     self.ypos = HEIGHT - 1
        #     self.velocity_y = 0
        #     return 'over'
        
        # current_time = time.time()
        
        # if current_time - self.last_fall_time >= 1000 / GRAVITY_LEVEL[CURRENT_LEVEL] * 60:
        #     self.ypos +=  1
        #     self.last_fall_time = current_time
        
        # if self.ypos > HEIGHT - 1:
        #     self.ypos = HEIGHT - 1
        #     self.velocity_y = 0
        #     return 'over'

        # if self.ypos < 0:
        #     self.ypos = 0
        #     self.velocity_y = 0
    
    def Place_block(self):
        SFX['harddrop'].play()
        CAN_PLACE = True
        for y_offset in range(self.size):
            for x_offset in range(self.size):
                if not (0 <= self.xpos + x_offset < WIDTH and 2 <= self.ypos + y_offset < HEIGHT):
                    if self.type[self.turn][y_offset * self.size + x_offset] != 'B':
                        CAN_PLACE = False
        if CAN_PLACE and not is_overlapped(self.xpos, self.ypos, self.turn):
            self.place()
            self.is_placed = True
        min_x,max_x = (3,0)
        for y_offset in range(self.size):
            for x_offset in range(self.size):
                val = self.data[y_offset * self.size + x_offset]
                if val != 'B':
                    min_x = min(min_x, x_offset)
                    max_x = max(max_x, x_offset)
        for i in range(random.randint(1,4)):
            PARTICLE_SYSTEM.add_bubble_particle(TEXTURE_WIDTH * (self.xpos+random.uniform(min_x,max_x))+ random.uniform(0,1) * TEXTURE_HEIGHT + X_OFFSET, (self.ypos+random.uniform(0,1)) * TEXTURE_HEIGHT + Y_OFFSET, 4, [0, -300], BLOCK_COLORS[self.name])

def canmove(posX,posY,turn): #텐바텐 전용 함수
    for y_offset in range(BLOCK.size):
        for x_offset in range(BLOCK.size):
            if (BLOCK.type[turn][y_offset * BLOCK.size + x_offset] != 'B'):
                if not (0 <= posX+x_offset < WIDTH and 0 <= posY+y_offset < HEIGHT):
                    return False
    return True

def trymove(posX, posY, turn):
    if canmove(posX,posY,turn):
        BLOCK.move(posX, posY)
        return True
    return False

def movekey(KEY, xOffset, yOffset, firstMS, repeatMS, hitSFX):
    # 첫 이동 시
    global GRAVITY_TICK
    if firstMS != -1:
        if trymove(BLOCK.xpos + xOffset, BLOCK.ypos + yOffset, BLOCK.turn):
            GRAVITY_TICK = 0
            hitSFX.play()
        time.sleep(0.001 * firstMS)
    
    # 반복 이동 시
    while KEY_STATE[KEY]:
        if trymove(BLOCK.xpos + xOffset, BLOCK.ypos + yOffset, BLOCK.turn):
            GRAVITY_TICK = 0
            hitSFX.play()
            time.sleep(0.001 * repeatMS)

def new_block(block):
    global BLOCK
    BLOCK = block
    return block

SWITCH_BLOCK = None

CAN_SWAP = True
def SWAP_PIECE():
    global SWITCH_BLOCK, BLOCK, CAN_SWAP
    if CAN_SWAP:
        switch_dump = BLOCK
        if SWITCH_BLOCK == None:
            SWITCH_BLOCK = Block(BLOCK.name)
            new_block(gen_block())
            return
        new_block(Block(SWITCH_BLOCK.name))
        SWITCH_BLOCK = Block(switch_dump.name)
        SFX['hold'].play()
        CAN_SWAP = False

CLEAR_LINES = 0
WARN = False

def CHECK_FIELD():
    global CLEAR_LINES, LAST_CLEAR_LINE, LAST_CLEAR_TIME
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
                    PARTICLE_SYSTEM.add_residual_particle(X_OFFSET + x * TEXTURE_WIDTH, Y_OFFSET + y * TEXTURE_HEIGHT, [random.uniform(-TEXTURE_WIDTH * 3, TEXTURE_WIDTH * 3), random.uniform(-TEXTURE_HEIGHT * 3, TEXTURE_HEIGHT * 3)], random.choice([-1, 1]) * random.uniform(30, 90), [TEXTURE_WIDTH, TEXTURE_HEIGHT], BLOCK_COLORS[FIELD[y][x]], .1, .5)
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
        LAST_CLEAR_LINE = CLEARED_LINES
        LAST_CLEAR_TIME = pygame.time.get_ticks()
        COUNT_BOARD['LINES'] = str(CLEAR_LINES)
    elif COMBO - 1 > 0:
        SFX['combobreak'].play()
    return Cleared_Line

# 전역 변수
KEY_STATE = {K_UP: False, K_DOWN: False, K_LEFT: False, K_RIGHT: False}
BACKGROUND_COLOR = COLORS['WHITE']
FIELD = [[0 for _ in range(WIDTH)] for _ in range(HEIGHT)]

GRAVITY_DELTA = 0
GRAVITY_LEVEL = [0.01667, 0.01914, 0.02161, 0.03093, 0.04025, 0.06361, 0.0879, 0.1236, 0.1775, 0.2598, 0.388, 0.59, 0.92, 1.46, 2.36]
CURRENT_LEVEL = 0

pygame.init()
pygame.display.set_caption('Tetris Classic')
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


def is_overlapped(xpos, ypos, turn): #해당부분 멀티 쓰레드로 사용하여도 시간복잡도 때매 반복시 프레임 드랍..;
    data = BLOCK.type[turn]
    for y_offset in range(BLOCK.size):
        for x_offset in range(BLOCK.size):
            if (0 <= xpos + x_offset < WIDTH) and (0 <= ypos + y_offset < HEIGHT):
                if (data[y_offset * BLOCK.size + x_offset] != 'B') and (FIELD[ypos + y_offset][xpos + x_offset] != 'B'):
                    return True
            elif data[y_offset * BLOCK.size + x_offset] != 'B': #### trymove
                return True
    return False

def is_overBoard(xpos, ypos, turn):
    print()


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
    # HOLD_PN
    pygame.draw.rect(SURFACE, COLORS['WHITE'], (X_OFFSET - 176, Y_OFFSET + TEXTURE_HEIGHT * 2, 176, 135))
    pygame.draw.rect(SURFACE, COLORS['BLACK'], (X_OFFSET - 176 + 4, Y_OFFSET + TEXTURE_HEIGHT * 2 + 34, 168, 97))                       # HOLD_PN 영역 168 x 97
    HOLD_text = FONTS['SUB_BOARD_TITLE'].render('HOLD', True, COLORS['BLACK'])
    SURFACE.blit(HOLD_text, (X_OFFSET - 176 + 8, Y_OFFSET + TEXTURE_HEIGHT * 2 + 3))
    if SWITCH_BLOCK != None:
        DRAW_PREVIEW_BLOCK(SWITCH_BLOCK, X_OFFSET - 172 + (168 - SWITCH_BLOCK.size * 37) / 2, Y_OFFSET + TEXTURE_HEIGHT * 2 + 34 + (97 - SWITCH_BLOCK.size * 37) / 2)
    #NEXT_PN
    pygame.draw.rect(SURFACE, COLORS['WHITE'], (X_OFFSET + WIDTH * TEXTURE_WIDTH + 1, Y_OFFSET + TEXTURE_HEIGHT * 2, 184, 353))
    pygame.draw.rect(SURFACE, COLORS['BLACK'], (X_OFFSET + WIDTH * TEXTURE_WIDTH + 5, Y_OFFSET + TEXTURE_HEIGHT * 2 + 34, 176, 315))    # NEXT_PN 영역 176 x 315*
    NEXT_text = FONTS['SUB_BOARD_TITLE'].render('NEXT', True, COLORS['BLACK'])
    SURFACE.blit(NEXT_text, (X_OFFSET + WIDTH * TEXTURE_WIDTH + 9, Y_OFFSET + TEXTURE_HEIGHT * 2 + 3))
    cnt = 0
    for NEXT_BLOCK in BAG[0:3]:
        DRAW_PREVIEW_BLOCK(NEXT_BLOCK, X_OFFSET + WIDTH * TEXTURE_WIDTH + 5 + (176 - 37 * NEXT_BLOCK.size) / 2, Y_OFFSET + cnt * (525 / 5) + ((525 / 5) - NEXT_BLOCK.size * 37) / 2 + TEXTURE_HEIGHT * 2 + 34)
        cnt += 1

START_TICK = None
COUNT_BOARD = {'TIME' : '0:00.000', 'LINES' : '0', 'PIECES' : '0, 0.00/S', 'INPUTS' : '0, 0.00/P'}
def DRAW_COUNT_BOARD():
    ELAPSED_TIME = pygame.time.get_ticks() - START_TICK
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
    global BAG, BLOCK, SWITCH_BLOCK, WARN, START_TICK, DROPED_PIECE, INPUT_KEYS, CAN_SWAP, GRAVITY_TICK
    BAG = []
    SWITCH_BLOCK = None
    WARN = False
    CAN_SWAP = True
    START_TICK = pygame.time.get_ticks()
    DROPED_PIECE = INPUT_KEYS = GRAVITY_TICK = 0
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

######

def initialize_Game(surface):
    global BLOCK, BLOCK_TEXTURE, START_TICK, GRAVITY_TICK, INPUT_KEYS, BGM_INDEX, GRAVITY_DELTA, GRAVITY_LEVEL, CURRENT_LEVEL, SURFACE, getTicksLastFrame
    RELOAD_SETTINGS()
    SURFACE = surface
    if BLOCK is None:
        BLOCK = gen_block()
    for ypos in range(HEIGHT):
        for xpos in range(WIDTH):
            FIELD[ypos][xpos] = 'B'
    counter = 0
    retry()
    START_TICK = pygame.time.get_ticks()
    getTicksLastFrame = pygame.time.get_ticks()
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
        if GRAVITY_TICK >= 1:
            GRAVITY_TICK -= 1
            BLOCK.Gravity()
        GRAVITY_TICK += deltaTime * GRAVITY_LEVEL[min(3,CURRENT_LEVEL)] * 60
        GRAVITY_DELTA += deltaTime
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
                elif key in SETTINGS['CONTROLS'].getValue('MOVE FALLING PIECE RIGHT'):
                    thread = Thread(target=movekey, args=(event.key, 1, 0, 10 * FRAMES, 2 * FRAMES, SFX['hit']), daemon=True)
                    thread.start()
                elif key in SETTINGS['CONTROLS'].getValue('MOVE FALLING PIECE LEFT'):
                    thread = Thread(target=movekey, args=(event.key, -1, 0, 10 * FRAMES, 2 * FRAMES, SFX['hit']), daemon=True)
                    thread.start()
                elif key in SETTINGS['CONTROLS'].getValue('SOFT DROP'):
                    thread = Thread(target=movekey, args=(event.key, 0, 1, 250 / 6.0, 250 / 6.0, SFX['hit']), daemon=True)
                    thread.start()
                elif key in SETTINGS['CONTROLS'].getValue('ROTATE CLOCKWISE'):
                    BLOCK.rotate(1)
                elif key in SETTINGS['CONTROLS'].getValue('ROTATE COUNTERCLOCKWISE'):
                    BLOCK.rotate(-1)
                elif key in SETTINGS['CONTROLS'].getValue('ROTATE 180'):
                    BLOCK.rotate(2)
                elif key in SETTINGS['CONTROLS'].getValue('SWAP HOLD PIECE'):
                    SWAP_PIECE()
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
    TEXTURE_WIDTH = round(37 * (SETTINGS['GAMEPLAY'].getValue('BOARD ZOOM') / 100) * 1.5)
    TEXTURE_HEIGHT = round(37 * (SETTINGS['GAMEPLAY'].getValue('BOARD ZOOM') / 100) * 1.5)
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

import pygame.display

import ClassicTetris
import TenbyTen
import Tentris
from ClassicTetris import *

SURFACE = pygame.display.set_mode((1920, 1080))
FPS_CLOCK = pygame.time.Clock()

BUTTON_LIST = ['PLAY','SHOP','SETTING']
CURRENT_SCREEN = 'HOME'
SIGNATURE_COLOR = {'HOME' : (32,34,40), 'SETTING' : (34,39,56), 'SHOP' : (37,36,64)}

def MOUSE_CLICKED(rect):
    if rect.collidepoint(MOUSE_FCP) and rect.collidepoint(MOUSE_ECP) and CURRENT_INPUT is None:
        return True
    return False
def MOUSE_HOVER(rect):
    if rect.collidepoint(pygame.mouse.get_pos()) and CURRENT_INPUT is None:
        return True
    return False

getTicksLastFrame = 0
SETTING_FOLD = { key : False for key in SETTINGS.keys() }

PARTICLE_SYSTEM = ParticlePrinciple()
SNOW_DELTA = 0
def UPDATE_SNOW(deltaTime):
    global SNOW_DELTA
    if deltaTime < 1:
        SNOW_DELTA += deltaTime
    while SNOW_DELTA > .03:
        PARTICLE_SYSTEM.add_snow_particle(random.randint(0, 1920), - 100, random.randint(5, 10), (100, 100), COLORS['WHITE'])
        SNOW_DELTA -= .03
    PARTICLE_SYSTEM.emit(SURFACE, deltaTime)
def DRAW_SCREEN():
    global getTicksLastFrame, CURRENT_GAMEMODE_SELECT
    tick = pygame.time.get_ticks()
    deltaTime = (tick - getTicksLastFrame) / 1000.0
    getTicksLastFrame = tick
    update_animation(deltaTime)
    CURSOR = pygame.SYSTEM_CURSOR_ARROW
    SURFACE.blit(TITLE_ASSETS['title_background'], (0, 0))
    if CURRENT_SCREEN != 'HOME' and CURRENT_SCREEN != 'PLAY':
        pygame.draw.rect(SURFACE, SIGNATURE_COLOR[CURRENT_SCREEN],(0,0,SCREEN_SIZE_WIDTH,SCREEN_SIZE_HEIGHT/20))
        TITLE_LABEL = FONTS['TITLE_LABEL'].render(CURRENT_SCREEN, True, (SIGNATURE_COLOR[CURRENT_SCREEN][0]+120, SIGNATURE_COLOR[CURRENT_SCREEN][1]+120, SIGNATURE_COLOR[CURRENT_SCREEN][2]+120))
        SURFACE.blit(TITLE_LABEL, (20,(SCREEN_SIZE_HEIGHT/20-TITLE_LABEL.get_height())/2))
    TITLE_UNDER_OFF_Y = SCREEN_SIZE_HEIGHT / 20
    if CURRENT_SCREEN == 'PLAY':
        UPDATE_SNOW(deltaTime)
        GAMEMODE_BG_RECT = pygame.Rect((SCREEN_SIZE_WIDTH - 780) / 2, (SCREEN_SIZE_HEIGHT - 500) / 2, 780 + 76, 500)
        s = pygame.Surface((GAMEMODE_BG_RECT.width,GAMEMODE_BG_RECT.height))
        pygame.draw.rect(s, COLORS['BLACK'],(0,0,GAMEMODE_BG_RECT.width,GAMEMODE_BG_RECT.height))
        s.set_alpha(200)
        SURFACE.blit(s, (GAMEMODE_BG_RECT.x, GAMEMODE_BG_RECT.y))
        cnt = 0
        for MODE in ['CLASSIC', 'TEN by TEN', 'TENTRIS']:
            BTN_RECT = pygame.Rect((GAMEMODE_BG_RECT.x+10,GAMEMODE_BG_RECT.y+77.5 + (350/3) * cnt + (350/3-80)/2,270,80))
            draw_Borded_Rect_r(SURFACE,COLORS['WHITE'],BTN_RECT,COLORS['BLACK'], 1)
            BTN_LABEL = FONTS['BUTTON_TITLE'].render(MODE, True, COLORS['WHITE'])
            SURFACE.blit(BTN_LABEL, (BTN_RECT.x+(BTN_RECT.width-BTN_LABEL.get_width())/2,BTN_RECT.y+(BTN_RECT.height-BTN_LABEL.get_height())/2))
            if MOUSE_HOVER(BTN_RECT):
                CURRENT_GAMEMODE_SELECT = MODE
                CURSOR = pygame.SYSTEM_CURSOR_HAND
            if MOUSE_CLICKED(BTN_RECT):
                PLAY_GAME(MODE)
            cnt += 1
        image = pygame.transform.smoothscale(TITLE_ASSETS[CURRENT_GAMEMODE_SELECT], (554,311))
        PREVIEW_RECT = pygame.Rect(GAMEMODE_BG_RECT.x+20+270, GAMEMODE_BG_RECT.y+77.5+(350/3-80)/2,556,350-(350/3-80))
        draw_Borded_Rect_r(SURFACE, COLORS['WHITE'], PREVIEW_RECT, COLORS['BLACK'], 1)
        SURFACE.blit(image, (PREVIEW_RECT[0]+1, PREVIEW_RECT[1]+1))
    if CURRENT_SCREEN == 'HOME':
        UPDATE_SNOW(deltaTime)
        SURFACE.blit(TITLE_ASSETS['title_logo'], (960/2, (1080-720)/2 + 100))
        cnt = 0
        for BUTTON_CODE in BUTTON_LIST:
            rect = pygame.Rect((1920-128)/2 - 138 + cnt * 138,(1080-128)/2 + 50, 128, 128)
            s = pygame.Surface((128,128), pygame.SRCALPHA)
            s.blit(TITLE_ASSETS[BUTTON_LIST[cnt]], (0,0))
            SURFACE.blit(s, (rect.x,rect.y))
            if MOUSE_HOVER(rect):
                CURSOR = pygame.SYSTEM_CURSOR_HAND
            if MOUSE_CLICKED(rect):
                CHANGE_MENU(BUTTON_CODE)
            cnt += 1
        VERSION_STR = 'Copyright 2024. Kangnam Univ All rights reserved.'
        VERSION_LABEL_SHADOW = FONTS['VERSION_DESC'].render(VERSION_STR, True, COLORS['BLACK'])
        VERSION_LABEL = FONTS['VERSION_DESC'].render(VERSION_STR, True, COLORS['WHITE'])
        SURFACE.blit(VERSION_LABEL_SHADOW, (5 + 2, SCREEN_SIZE_HEIGHT - VERSION_LABEL.get_height() + 2))
        SURFACE.blit(VERSION_LABEL, (5, SCREEN_SIZE_HEIGHT - VERSION_LABEL.get_height()))
    if CURRENT_SCREEN == 'SHOP':
        pygame.draw.rect(SURFACE, (13, 12, 16), (0, TITLE_UNDER_OFF_Y, 1920, SCREEN_SIZE_HEIGHT * 19 / 20))
        BACK_BTN_RECT = pygame.Rect(0, TITLE_UNDER_OFF_Y + 10, 135, 55)
        pygame.draw.rect(SURFACE, (36, 36, 36), BACK_BTN_RECT)
        BACK = FONTS['BACK_BTN'].render('BACK', True, (201, 201, 201))
        SURFACE.blit(BACK, (120 - BACK.get_width(), TITLE_UNDER_OFF_Y + 10 + (55 - BACK.get_height()) / 2))
        if MOUSE_HOVER(BACK_BTN_RECT):
            CURSOR = pygame.SYSTEM_CURSOR_HAND
        if MOUSE_CLICKED(BACK_BTN_RECT):
            CHANGE_MENU('HOME')
        pygame.draw.rect(SURFACE, (37,36,64), ((SCREEN_SIZE_WIDTH-960)/2-10,(SCREEN_SIZE_HEIGHT-540)/2-10,960+10*2,540+10*2))
        SURFACE.blit(PREVIEW_SKINS[Material.SKIN_PREVIEW_INDEX], ((SCREEN_SIZE_WIDTH-960)/2,(SCREEN_SIZE_HEIGHT-540)/2))
        prev_arrow_rect = pygame.Rect((SCREEN_SIZE_WIDTH)/2 - 200 - 140, (SCREEN_SIZE_HEIGHT - 540) / 2 + 540 + 30, 140, 100)
        next_arrow_rect = pygame.Rect((SCREEN_SIZE_WIDTH)/2 + 200, (SCREEN_SIZE_HEIGHT - 540) / 2 + 540 + 30, 140, 100)
        confirm_rect    = pygame.Rect((SCREEN_SIZE_WIDTH - 350)/2, (SCREEN_SIZE_HEIGHT - 540) / 2 + 540 + 30, 350, 100)
        if MOUSE_HOVER(prev_arrow_rect) or MOUSE_HOVER(next_arrow_rect) or MOUSE_HOVER(confirm_rect):
            CURSOR = pygame.SYSTEM_CURSOR_HAND
        if MOUSE_CLICKED(next_arrow_rect):
            Material.SKIN_PREVIEW_INDEX = (Material.SKIN_PREVIEW_INDEX + 1)  % len(SKIN_SORT)
        if MOUSE_CLICKED(prev_arrow_rect):
            Material.SKIN_PREVIEW_INDEX = len(SKIN_SORT)-1 if Material.SKIN_PREVIEW_INDEX == 0 else Material.SKIN_PREVIEW_INDEX - 1
        if MOUSE_CLICKED(confirm_rect):
            Material.CURRENT_SKIN_INDEX = Material.SKIN_PREVIEW_INDEX
        draw_Borded_Rect_r(SURFACE, (255,255,255), prev_arrow_rect, (13, 12, 16), 3)
        draw_Borded_Rect_r(SURFACE, (255,255,255), next_arrow_rect, (13, 12, 16), 3)
        X_MIDDLE_OFFSET = 50
        pygame.draw.polygon(SURFACE, COLORS['WHITE'], [[prev_arrow_rect.x + X_MIDDLE_OFFSET + 40, prev_arrow_rect.y + 20], [prev_arrow_rect.x + X_MIDDLE_OFFSET + 40, prev_arrow_rect.y + 80], [prev_arrow_rect.x + X_MIDDLE_OFFSET - 10, prev_arrow_rect.y + 50]], 3)
        pygame.draw.polygon(SURFACE, COLORS['WHITE'], [[next_arrow_rect.x + X_MIDDLE_OFFSET,next_arrow_rect.y + 20], [next_arrow_rect.x + X_MIDDLE_OFFSET,next_arrow_rect.y+80], [next_arrow_rect.x+X_MIDDLE_OFFSET+50, next_arrow_rect.y+50]],3)
        draw_Borded_Rect_r(SURFACE, COLORS['GREEN'] if Material.CURRENT_SKIN_INDEX == Material.SKIN_PREVIEW_INDEX else COLORS['RED'], confirm_rect, (13, 12, 16), 3)

    if CURRENT_SCREEN == 'SETTING':
        pygame.draw.rect(SURFACE, (13,12,16), (0,TITLE_UNDER_OFF_Y,1920,SCREEN_SIZE_HEIGHT*19/20))
        BACK_BTN_RECT = pygame.Rect(0,TITLE_UNDER_OFF_Y+10,135,55)
        pygame.draw.rect(SURFACE, (36,36,36), BACK_BTN_RECT)
        BACK = FONTS['BACK_BTN'].render('BACK', True, (201,201,201))
        SURFACE.blit(BACK, (120-BACK.get_width(),TITLE_UNDER_OFF_Y+10+(55-BACK.get_height())/2))
        if MOUSE_HOVER(BACK_BTN_RECT):
            CURSOR = pygame.SYSTEM_CURSOR_HAND
        if MOUSE_CLICKED(BACK_BTN_RECT):
            pygame.mixer.music.set_volume(SETTINGS['VOLUME & AUDIO'].getValue('MUSIC') / 100)
            CHANGE_MENU('HOME')
        y_offset = TITLE_UNDER_OFF_Y + 10
        for SETTING_CATEGORY in SETTINGS.keys(): #hegith: 35, font: 20pt
            x_offset = (SCREEN_SIZE_WIDTH - 1140)/2
            CATEGORY_RECT = pygame.Rect(x_offset, y_offset,1140,65)
            pygame.draw.rect(SURFACE, (24,28,39), CATEGORY_RECT)
            pygame.draw.rect(SURFACE, (18,21,29), (x_offset+15, y_offset+10,45,45))
            pygame.draw.polygon(SURFACE, (101,116,151),get_rotated_polygon([[x_offset+25, y_offset+20+5.5], [x_offset+50, y_offset+20+5.5], [x_offset+37.5, y_offset+42.5]],180 if SETTING_FOLD[SETTING_CATEGORY] else 0))
            LABEL = FONTS['SETTING_TITLE'].render(SETTING_CATEGORY, True, (101,116,151))
            SURFACE.blit(LABEL, (x_offset+70, y_offset+(65-LABEL.get_height())/2))
            if MOUSE_HOVER(CATEGORY_RECT):
                CURSOR = pygame.SYSTEM_CURSOR_HAND
            if MOUSE_CLICKED(CATEGORY_RECT):
                SETTING_FOLD[SETTING_CATEGORY] = not SETTING_FOLD[SETTING_CATEGORY]
            y_offset += 65
            if SETTING_FOLD[SETTING_CATEGORY] is True:
                for SETTING_VALUE in SETTINGS[SETTING_CATEGORY].getValues().keys():
                    VALUES = SETTINGS[SETTING_CATEGORY].getFullValue(SETTING_VALUE)
                    if SETTINGS[SETTING_CATEGORY].getType(SETTING_VALUE) == 'KEY':
                        pygame.draw.rect(SURFACE, (24, 28, 39), (x_offset, y_offset, 1140, 35 + 6))
                        LABEL = FONTS['SETTING_VALUE_CODE'].render(SETTING_VALUE, True, (98,117,167))
                        SURFACE.blit(LABEL, (x_offset + 15, y_offset)) #WIDTH = 135, HEIGHT = 29, FIRST_COLOR = 11,12,16, SECOND_COLOR = 17,20,28
                        cnt = 0
                        for KEY in VALUES:
                            KEY_NAME = pygame.key.name(KEY).upper() if KEY is not None else '[NOT SET]'
                            BTN_X = x_offset + (1140-140*3-10) + 140 * cnt
                            BTN_Y = y_offset + 3
                            KEY_SETUP_RECT = pygame.Rect(BTN_X, BTN_Y, 135, 29)
                            if MOUSE_HOVER(KEY_SETUP_RECT):
                                CURSOR = pygame.SYSTEM_CURSOR_HAND
                            if MOUSE_CLICKED(KEY_SETUP_RECT):
                                KEY_SET_INPUT(SETTING_CATEGORY, SETTING_VALUE, cnt)
                            pygame.draw.rect(SURFACE, (11,12,16) if cnt == 0 else (17,20,28), (BTN_X, BTN_Y, 135, 29))
                            LABEL = FONTS['KEY_VALUE'].render(KEY_NAME, True, (167,186,236))
                            SURFACE.blit(LABEL, (BTN_X+(135-LABEL.get_width())/2, BTN_Y+(29-LABEL.get_height())/2))
                            cnt += 1
                        y_offset += 35
                    elif SETTINGS[SETTING_CATEGORY].getType(SETTING_VALUE) in ['FLOAT','INT']:
                        VALUE_NAME_OFF      = VALUES[3]
                        VALUE_BAR_LENGTH    = 1000 - VALUE_NAME_OFF - 30
                        LABEL       = FONTS['SETTING_VALUE_CODE'].render(SETTING_VALUE,     True, (98,117,167))
                        UNIT_LABEL  = FONTS['SETTING_VALUE_CODE'].render(VALUES[4],         True, (61,68,87))
                        VALUE_LABEL = FONTS['SETTING_VALUE_CODE'].render('∞' if SETTING_VALUE == 'SDF' and VALUES[0] == 40.1 else str(VALUES[0]), True, (174, 192, 238))
                        pygame.draw.rect(SURFACE, (24, 28, 39), (x_offset, y_offset, 1140, 50 + 5))
                        pygame.draw.rect(SURFACE, (17, 20, 27), (x_offset + 15, y_offset + 1, 1110, 45))
                        pygame.draw.rect(SURFACE, (11, 13, 17), (x_offset + 1000, y_offset + 7.5, 120, 35))
                        pygame.draw.rect(SURFACE, (11, 13, 17), (x_offset + 15 + VALUE_NAME_OFF, y_offset+(50-6)/2, VALUE_BAR_LENGTH, 6))
                        DRAG_AREA = pygame.Rect(x_offset + 15 + VALUE_NAME_OFF, y_offset+(50-35)/2, VALUE_BAR_LENGTH, 35)
                        if DRAG_AREA.collidepoint(MOUSE_FCP) and pygame.mouse.get_pressed()[0]:
                            VALUES[0] = round(min(max((VALUES[2]-VALUES[1]) / VALUE_BAR_LENGTH * (pygame.mouse.get_pos()[0]-DRAG_AREA.x) + VALUES[1],VALUES[1]),VALUES[2]),1 if SETTINGS[SETTING_CATEGORY].getType(SETTING_VALUE) == 'FLOAT' else 0)
                            if SETTINGS[SETTING_CATEGORY].getType(SETTING_VALUE) == 'INT':
                                VALUES[0] = int(VALUES[0])
                        SURFACE.blit(LABEL,       (x_offset + 30,     y_offset + (45 - LABEL.get_height()) / 2))
                        SURFACE.blit(VALUE_LABEL, (x_offset + 1110 - UNIT_LABEL.get_width() - VALUE_LABEL.get_width(), y_offset + (45 - UNIT_LABEL.get_height()) / 2))
                        SURFACE.blit(UNIT_LABEL,  (x_offset + 1115 - UNIT_LABEL.get_width(), y_offset + (45 - UNIT_LABEL.get_height()) / 2))
                        draw_Borded_Rect(SURFACE,x_offset + VALUE_NAME_OFF + VALUE_BAR_LENGTH * ((VALUES[0]-VALUES[1])/(VALUES[2]-VALUES[1])) + 2.5,y_offset+10,25,30,(24,28,39),(40,49,69),3)
                        y_offset += 50
            y_offset += 20
        if CURRENT_INPUT is not None:
            CURTAIN = pygame.Surface((SCREEN_SIZE_WIDTH, SCREEN_SIZE_HEIGHT), pygame.SRCALPHA)
            pygame.draw.rect(CURTAIN, (0,0,0), (0,0,SCREEN_SIZE_WIDTH,SCREEN_SIZE_HEIGHT))
            TITLE_LABEL_1 = FONTS['CURTAIN_DISC'].render('PRESS ANY KEY', True, COLORS['WHITE'])
            TITLE_LABEL_2 = FONTS['CURTAIN_DISC'].render('OR BUTTON', True, COLORS['WHITE'])
            SUB_LABEL = FONTS['CURTAIN_DISC_SUB'].render('PRESS 0 TO REMOVE THE KEYBIND', True, COLORS['WHITE'])
            CURTAIN.blit(TITLE_LABEL_1, ((SCREEN_SIZE_WIDTH-TITLE_LABEL_1.get_width())/2,435))
            CURTAIN.blit(TITLE_LABEL_2, ((SCREEN_SIZE_WIDTH-TITLE_LABEL_2.get_width())/2,540))
            CURTAIN.blit(SUB_LABEL,     ((SCREEN_SIZE_WIDTH-SUB_LABEL.get_width())/2,985))
            CURTAIN.set_alpha(int(min(255 * (ANIMATION_DELTA['KEY_SET_CURTAIN'] / .25), 255)))
            SURFACE.blit(CURTAIN, (0,0))

    pygame.mouse.set_cursor(CURSOR)

CURRENT_GAMEMODE_SELECT = 'CLASSIC'

CURRENT_INPUT = None

def PLAY_GAME(MODE):
    pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)
    if MODE == 'CLASSIC':
        ClassicTetris.initialize_Game(SURFACE)
    if MODE == 'TEN by TEN':
        TenbyTen.initialize_Game(SURFACE)
    if MODE == 'TENTRIS':
        Tentris.initialize_Game(SURFACE)

def KEY_SET_INPUT(category, value, index):
    global CURRENT_INPUT
    ANIMATION_DELTA['KEY_SET_CURTAIN'] = 0
    CURRENT_INPUT = (category, value, index)

def CHANGE_MENU(BUTTON_CODE):
    global CURRENT_SCREEN
    CURRENT_SCREEN = BUTTON_CODE

def QUIT():
    pygame.quit()
    sys.exit()

MOUSE_FCP = (-1,-1) #FIRST_CLICK_POINT
MOUSE_ECP = (-1,-1) #END_CLICK_POINT
def main():
    global MOUSE_FCP, MOUSE_ECP, CURRENT_INPUT
    pygame.mixer.music.play(loops=-1)
    pygame.display.set_icon(TITLE_ASSETS['TENTRIS_ICON'])
    pygame.display.set_caption('TENTRIS')
    while True:
        MOUSE_ECP = (-1,-1)
        for event in pygame.event.get():
            if event.type == KEYDOWN:
                if CURRENT_INPUT is not None:
                    SETTINGS[CURRENT_INPUT[0]].getValue(CURRENT_INPUT[1])[CURRENT_INPUT[2]] = event.key if event.key != K_0 else None
                    CURRENT_INPUT = None
                    ANIMATION_DELTA['KEY_SET_CURTAIN'] = -1
                else:
                    if event.key in SETTINGS['CONTROLS'].getValue('FOREIT GAME'):
                        if CURRENT_SCREEN == 'HOME':
                            QUIT()
                        else:
                            CHANGE_MENU('HOME')
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1: #1 : 좌클릭, 2 : 휠클릭, 3 : 우클릭
                    MOUSE_FCP = pygame.mouse.get_pos()
            if event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    MOUSE_ECP = pygame.mouse.get_pos()
        DRAW_SCREEN()
        pygame.display.update()
        FPS_CLOCK.tick(SETTINGS['VIDEO'].getValue('MAX FRAME'))


if __name__ == '__main__':
    main()

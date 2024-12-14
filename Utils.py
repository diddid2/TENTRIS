import pygame
import threading
from pygame.locals import *

ANIMATION_DELTA = {'KEY_SET_CURTAIN' : -1, 'GAMEOVERTITLE' : -1, 'MAIN_CURTAIN' : -1}

def update_animation(deltatime):
    for animation in ANIMATION_DELTA.keys():
        if ANIMATION_DELTA[animation] >= 0:
            ANIMATION_DELTA[animation] += deltatime

def draw_Borded_Rect(surface, posX, posY, width, height, color, outline_color, outline_width):
    pygame.draw.rect(surface, outline_color, (posX, posY, width, height))
    pygame.draw.rect(surface, color, (posX + outline_width, posY + outline_width, width - outline_width * 2, height - outline_width * 2))

def draw_Borded_Rect_r(surface, outline_color, rect, color, outline_width):
    pygame.draw.rect(surface, outline_color, (rect.x, rect.y, rect.width, rect.height))
    pygame.draw.rect(surface, color, (rect.x + outline_width, rect.y + outline_width, rect.width - outline_width * 2, rect.height - outline_width * 2))

def get_rotate_points(points,pivot,angle):
    pp = pygame.math.Vector2(pivot)
    rotated_points = [(pygame.math.Vector2(x, y) - pp).rotate(angle) + pp for x, y in points]
    return rotated_points
def get_rotated_polygon(points, angle, pivot=None):
    if pivot == None:
        lx, ly = zip(*points)
        min_x, min_y, max_x, max_y = min(lx), min(ly), max(lx), max(ly)
        bounding_rect = pygame.Rect(min_x, min_y, max_x - min_x, max_y - min_y)
        pivot = bounding_rect.center
    rotated_points = get_rotate_points(points, pivot, angle)
    return rotated_points

class StoppableThread(threading.Thread):
    def __init__(self):
        super(StoppableThread, self).__init__()
        self._stop_event = threading.Event()
    def stop(self):
        self._stop_event.set()
    def is_stop(self):
        return self._stop_event.is_set()
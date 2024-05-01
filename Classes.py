import pygame
from pygame.locals import *
from threading import Thread
import numpy
from scipy.interpolate import interp1d
import math
import sys
from random import randint, random
from typing import Union

Point = pygame.Vector2

def remap(old_val, old_min, old_max, new_min, new_max):
    return (new_max - new_min)*(old_val - old_min) / (old_max - old_min) + new_min

def get_curve(points):
    x_new = numpy.arange(points[0].x, points[-1].x, 1)
    x = numpy.array([i.x for i in points[:-1]])
    y = numpy.array([i.y for i in points[:-1]])
    f = interp1d(x, y, kind='cubic', fill_value='extrapolate')
    y_new = f(x_new)
    x1 = list(x_new)
    y1 = list(y_new)
    points = [Point(x1[i], y1[i]) for i in range(len(x1))]
    return points

class WaterSpring:
    def __init__(self,target_height,x=0):
        self.target_height = target_height // 2 + 150
        self.dampening = 0.05  # adjust accordingly
        self.tension = 0.01
        self.height = self.target_height
        self.vel = 0
        self.x = x

    def update(self):
        dh = self.target_height - self.height
        if abs(dh) < 0.01:
            self.height = self.target_height
        self.vel += self.tension * dh - self.vel * self.dampening
        self.height += self.vel

    def draw(self, surf: pygame.Surface):
        pygame.draw.circle(surf, 'white', (self.x, self.height), 1)

class Wave:
    def __init__(self,screen_width,screen_height):
        diff = 20
        self.springs = [WaterSpring(screen_height,x=i * diff + 0) for i in range(screen_width // diff + 2)]
        self.points = []
        self.diff = diff

    def get_spring_index_for_x_pos(self, x):
        return int(x // self.diff)

    def get_target_height(self):
        return self.springs[0].target_height

    def set_target_height(self, height):
        for i in self.springs:
            i.target_height = height

    def add_volume(self,screen_width, volume):
        height = volume / screen_width
        self.set_target_height(self.get_target_height() - height)

    def update(self,screen_width,screen_height):
        for i in self.springs:
            i.update()
        self.spread_wave()
        self.points = [Point(i.x, i.height) for i in self.springs]
        self.points = get_curve(self.points)
        self.points.extend([Point(screen_width, screen_height), Point(0, screen_height)])

    def draw(self, surf: pygame.Surface):
        pygame.draw.polygon(surf, (0, 0, 255, 50), self.points)

    def draw_line(self, surf: pygame.Surface):
        pygame.draw.lines(surf, 'white', False, self.points[:-2], 5)

    def spread_wave(self):
        spread = 0.1
        for i in range(len(self.springs)):
            if i > 0:
                self.springs[i - 1].vel += spread * (self.springs[i].height - self.springs[i - 1].height)
            try:
                self.springs[i + 1].vel += spread * (self.springs[i].height - self.springs[i + 1].height)
            except IndexError:
                pass

    def splash(self, index, vel):
        try:
            self.springs[index].vel += vel
        except IndexError:
            pass

class Button():
    def __init__(self, image, pos, text_input, font, base_color, hovering_color):
        self.image = image
        self.x_pos = pos[0]
        self.y_pos = pos[1]
        self.font = font
        self.base_color, self.hovering_color = base_color, hovering_color
        self.text_input = text_input
        self.text = self.font.render(self.text_input, True, self.base_color)
        if self.image is None:
            self.image = self.text
        self.rect = self.image.get_rect(center=(self.x_pos, self.y_pos))
        self.text_rect = self.text.get_rect(center=(self.x_pos, self.y_pos))
        self.isChosen = False

    def update(self, screen):
        if self.image is not None:
            screen.blit(self.image, self.rect)
        screen.blit(self.text, self.text_rect)

    def checkForInput(self, position):
        if position[0] in range(self.rect.left, self.rect.right) and position[1] in range(self.rect.top, self.rect.bottom):
            return True
        return False

    def changeColor(self, position):
        if position[0] in range(self.rect.left, self.rect.right) and position[1] in range(self.rect.top, self.rect.bottom):
            self.text = self.font.render(self.text_input, True, self.hovering_color)
            self.isChosen = True
        else:
            self.text = self.font.render(self.text_input, True, self.base_color)
            self.isChosen = False
            
    def changeImage(self, image):
        self.image = image
            
class CustomThread(Thread):
    def __init__(self, Value=None, group=None, target=None, name=None,
                 args=(), kwargs={}, Verbose=None):
        Thread.__init__(self, group, target, name, args, kwargs)
        self._return = None
        self.returnValue = Value
        self.isRunning = False
 
    def run(self):
        self.isRunning = True
        if self._target is not None:
            self._return = self._target(*self._args, **self._kwargs)
        self.isRunning = False
        self.returnValue = self._return
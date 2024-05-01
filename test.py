import pygame
import math

def sine(speed: float, time: int, how_far: float, overall_y: int) -> int:
	t = pygame.time.get_ticks() / 2 % time
	y = math.sin(t / speed) * how_far + overall_y
	return int(y)

while True:
    pygame.init()
    y = sine(200,1280,10,50)
    print(y)
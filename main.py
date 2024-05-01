from Classes import *
import os
import serial
from Stopwatch import *

#Colors
red = (255 , 0 , 0) # RED
green = (0, 255, 0) # GREEN
blue = (10, 60, 225) # BLUE
white = (255, 255, 255) # WHITE
black = (0, 0, 0) # BLACK
Colors = [red,green,blue,white,black]
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720

clock = pygame.time.Clock()
FPS = 60

def sine(speed: float, time: int, how_far: float, overall_y: int) -> int:
	t = pygame.time.get_ticks() / 2 % time
	y = math.sin(t / speed) * how_far + overall_y
	return int(y)

def get_font(size):
	return pygame.font.Font("assets\\LucidaBrightRegular.ttf",size)

def BLEConnection() -> bool:
	global serialPort
	try:
		serialPort = serial.Serial(port='COM9', baudrate=9600)
	except:
		return False
	else:
		return True

def playing():
	
	def Reading():
		while running:
			data = serialPort.readline(1024)
			data = str(data.decode('ascii'))
			data = data.replace('\r\n','')
			if data:
				# print(data)
				if data != '':
					ReadThread.returnValue = data
				else:
					return None
	
	pygame.init()
	BLEConnection()
	screen = pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT))
	pygame.display.set_caption("Breath Analysis Game")
	pygame.display.toggle_fullscreen()
	wave = Wave(SCREEN_WIDTH,SCREEN_HEIGHT)
	water_level = 500
	wave.set_target_height(water_level)
	running = True
	FS = True
	surf = pygame.Surface((1280,720), pygame.SRCALPHA, 32)
	surf.convert_alpha()
	surf.fill("White")
	LEVEL_TEXT = get_font(100).render(str(0), True, "#b68f40")
	TIMER_TEXT = get_font(100).render(str(0),True, "#ffffff")
	background = pygame.image.load("assets\\bar.png")
	background = pygame.transform.scale(background,(SCREEN_WIDTH,SCREEN_HEIGHT))
	SW = Stopwatch()
	ReadThread = CustomThread(target=Reading)
	ReadThread.start()

	while running:
		key = None
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				running = False
				serial.close()
			elif event.type == pygame.KEYDOWN:
				key = pygame.key.name(event.key)
		if key == 'f':
			pygame.display.toggle_fullscreen()
		# elif key == 'w':
		# 	water_level -= 50
		# 	wave.set_target_height(water_level)
		# elif key == 's':
		# 	water_level += 50
		# 	wave.set_target_height(water_level)
			# if FS == True:
			#     os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (300,300)
			#     screen = pygame.display.set_mode((1280,720))
			#     FS = False
			# else:
			#     screen = pygame.display.set_mode((1920,1080))
			#     FS = True

		if ReadThread.returnValue != None:
			level = int(remap(int(ReadThread.returnValue),0,3000,650,250))
			percent = int((int(ReadThread.returnValue)/3000*100))
			LEVEL_TEXT = get_font(100).render(str(percent), True, "#b68f40")
			wave.set_target_height(level)
			if int(percent) >=  30:
				if SW.started == False:
					SW.start()
				TIMER_TEXT = get_font(100).render(str(round(SW.secondsPassed(),2)), True, "#ffffff")
			else:
				SW.Pause()
				SW.reset()
		y = sine(200.0,1280,20,0)
		index = wave.get_spring_index_for_x_pos(SCREEN_WIDTH/2)
		wave.splash(index+y,1)
		pygame.display.flip()
		wave.update(SCREEN_WIDTH,SCREEN_HEIGHT)
		surf.fill("Black")
		wave.draw(surf)
		# wave.draw_line(surf)
		screen.blit(surf, (0, 0))
		screen.blit(background,(0,0))
		screen.blit(LEVEL_TEXT,(100,100))
		screen.blit(TIMER_TEXT,(900,360))
		pygame.display.update()
		clock.tick(FPS)

	pygame.quit()

def menu():
	pygame.init()
	screen = pygame.display.set_mode((1280,720))
	pygame.display.set_caption("Breath Analysis Game")
	pygame.display.toggle_fullscreen()
	surf = pygame.Surface((1280,720), pygame.SRCALPHA, 32)
	surf.convert_alpha()
	running = True
	Start = Button(pygame.image.load("assets\\menu button.png"),(640,280),"Start",get_font(45),"White","Green")
	Start.update(surf)
	BLE = Button(pygame.image.load("assets\\Bluetooth Off.png"),((1230,50)),"",get_font(45),"White","Green")
	BLE.update(surf)
	background = pygame.image.load("assets\\background.png")
	background = pygame.transform.scale(background,(1280,720))

	while running:
		key = None
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				running = False
				serial.close()
			elif event.type == pygame.KEYDOWN:
				key = pygame.key.name(event.key)
		if key == 'f':
			pygame.display.toggle_fullscreen()

		pygame.display.flip()
		screen.blit(background,(0,0))
		screen.blit(surf,(0,0))
		pygame.display.update()
		clock.tick(FPS)
	

playing()
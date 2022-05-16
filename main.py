import pygame, sys, random
from pygame.math import Vector2
from pygame.locals import *
import os

class SNAKE:
	def __init__(self):
		self.body = [Vector2(5,10),Vector2(4,10),Vector2(3,10)]
		self.direction = Vector2(0,0)
		self.new_block = False

		self.head_up = pygame.image.load('Graphics/head_up.png').convert_alpha()
		self.head_down = pygame.image.load('Graphics/head_down.png').convert_alpha()
		self.head_right = pygame.image.load('Graphics/head_right.png').convert_alpha()
		self.head_left = pygame.image.load('Graphics/head_left.png').convert_alpha()
		
		self.tail_up = pygame.image.load('Graphics/tail_up.png').convert_alpha()
		self.tail_down = pygame.image.load('Graphics/tail_down.png').convert_alpha()
		self.tail_right = pygame.image.load('Graphics/tail_right.png').convert_alpha()
		self.tail_left = pygame.image.load('Graphics/tail_left.png').convert_alpha()

		self.body_vertical = pygame.image.load('Graphics/body_vertical.png').convert_alpha()
		self.body_horizontal = pygame.image.load('Graphics/body_horizontal.png').convert_alpha()

		self.body_tr = pygame.image.load('Graphics/body_tr.png').convert_alpha()
		self.body_tl = pygame.image.load('Graphics/body_tl.png').convert_alpha()
		self.body_br = pygame.image.load('Graphics/body_br.png').convert_alpha()
		self.body_bl = pygame.image.load('Graphics/body_bl.png').convert_alpha()
		self.crunch_sound = pygame.mixer.Sound('Son/minecraftcrunch.wav')

	def draw_snake(self):
		self.update_head_graphics()
		self.update_tail_graphics()

		for index,block in enumerate(self.body):
			x_pos = int(block.x * cell_size)
			y_pos = int(block.y * cell_size)
			block_rect = pygame.Rect(x_pos,y_pos,cell_size,cell_size)

			if index == 0:
				screen.blit(self.head,block_rect)
			elif index == len(self.body) - 1:
				screen.blit(self.tail,block_rect)
			else:
				previous_block = self.body[index + 1] - block
				next_block = self.body[index - 1] - block
				if previous_block.x == next_block.x:
					screen.blit(self.body_vertical,block_rect)
				elif previous_block.y == next_block.y:
					screen.blit(self.body_horizontal,block_rect)
				else:
					if previous_block.x == -1 and next_block.y == -1 or previous_block.y == -1 and next_block.x == -1:
						screen.blit(self.body_tl,block_rect)
					elif previous_block.x == -1 and next_block.y == 1 or previous_block.y == 1 and next_block.x == -1:
						screen.blit(self.body_bl,block_rect)
					elif previous_block.x == 1 and next_block.y == -1 or previous_block.y == -1 and next_block.x == 1:
						screen.blit(self.body_tr,block_rect)
					elif previous_block.x == 1 and next_block.y == 1 or previous_block.y == 1 and next_block.x == 1:
						screen.blit(self.body_br,block_rect)

	def update_head_graphics(self):
		head_relation = self.body[1] - self.body[0]
		if head_relation == Vector2(1,0): self.head = self.head_left
		elif head_relation == Vector2(-1,0): self.head = self.head_right
		elif head_relation == Vector2(0,1): self.head = self.head_up
		elif head_relation == Vector2(0,-1): self.head = self.head_down

	def update_tail_graphics(self):
		tail_relation = self.body[-2] - self.body[-1]
		if tail_relation == Vector2(1,0): self.tail = self.tail_left
		elif tail_relation == Vector2(-1,0): self.tail = self.tail_right
		elif tail_relation == Vector2(0,1): self.tail = self.tail_up
		elif tail_relation == Vector2(0,-1): self.tail = self.tail_down

	def move_snake(self):
		if self.new_block == True:
			body_copy = self.body[:]
			body_copy.insert(0,body_copy[0] + self.direction)
			self.body = body_copy[:]
			self.new_block = False
		else:
			body_copy = self.body[:-1]
			body_copy.insert(0,body_copy[0] + self.direction)
			self.body = body_copy[:]

	def add_block(self):
		self.new_block = True

	def play_crunch_sound(self):
		self.crunch_sound.play()

	def reset(self):
		self.body = [Vector2(5,10),Vector2(4,10),Vector2(3,10)]
		self.direction = Vector2(0,0)

class FRUIT:
	def __init__(self):
		self.randomize()

	def draw_fruit(self):
		fruit_rect = pygame.Rect(int(self.pos.x * cell_size),int(self.pos.y * cell_size),cell_size,cell_size)
		screen.blit(apple,fruit_rect)

	def randomize(self):
		self.x = random.randint(0,cell_number - 1)
		self.y = random.randint(0,cell_number - 1)
		self.pos = Vector2(self.x,self.y)

class MAIN:
    
	def __init__(self):
		self.snake = SNAKE()
		self.fruit = FRUIT()

	def update(self):
		self.snake.move_snake()
		self.check_collision()
		self.check_fail()

	def draw_elements(self):
		self.draw_grass()
		self.fruit.draw_fruit()
		self.snake.draw_snake()
        
	def check_collision(self):
		if self.fruit.pos == self.snake.body[0]:
			self.fruit.randomize()
			self.snake.add_block()
			self.snake.play_crunch_sound()

		for block in self.snake.body[1:]:
			if block == self.fruit.pos:
				self.fruit.randomize()

	def check_fail(self):
		if not 0 <= self.snake.body[0].x < cell_number or not 0 <= self.snake.body[0].y < cell_number:
			self.game_over()

		for block in self.snake.body[1:]:
			if block == self.snake.body[0]:
				self.game_over()
		
	def game_over(self):
		self.snake.reset()

	def draw_grass(self):
		grass_color = (167,209,61)
		for row in range(cell_number):
			if row % 2 == 0: 
				for col in range(cell_number):
					if col % 2 == 0:
						grass_rect = pygame.Rect(col * cell_size,row * cell_size,cell_size,cell_size)
						pygame.draw.rect(screen,grass_color,grass_rect)
			else:
				for col in range(cell_number):
					if col % 2 != 0:
						grass_rect = pygame.Rect(col * cell_size,row * cell_size,cell_size,cell_size)
						pygame.draw.rect(screen,grass_color,grass_rect)			


        
# Rendu du texte
def text_format(message, textFont, textSize, textColor):
    newFont=pygame.font.Font(textFont, textSize)
    newText=newFont.render(message, 0, textColor)
    return newText


pygame.mixer.pre_init(44100,-16,2,512)
pygame.init()
 
# Centrer le jeu 
os.environ['SDL_VIDEO_CENTERED'] = '1'
 
# Résolution du jeu et initialisation de variables
screen_width = 800
screen_height = 800
screen=pygame.display.set_mode((screen_width, screen_height))
game_font = "Police/VECTRO-Bold.otf"
clock = pygame.time.Clock()
apple = pygame.image.load('Graphics/pomme.png').convert_alpha()
cell_size = 40
cell_number = 20


# Main loop
menu = True
choix = 0

 
while menu:
    for event in pygame.event.get():
        if event.type==pygame.QUIT:
            menu = False
        if event.type==pygame.KEYDOWN:
            if event.key==pygame.K_LEFT and choix == 0:
                choix = 2
            elif event.key==pygame.K_LEFT and choix == 1:
                choix = 2
            elif event.key==pygame.K_LEFT and choix == 2:
                choix = 1
            elif event.key==pygame.K_RIGHT and choix == 0:
                choix = 1
            elif event.key==pygame.K_RIGHT and choix == 1:
                choix = 2
            elif event.key==pygame.K_RIGHT and choix == 2:
                choix = 1
            if event.key==pygame.K_RETURN:
                if choix == 1:
                    MAIN()
                    menu = False
                if choix == 2:
                    pygame.quit()
                    
                    
    # Main Menu UI
    screen.fill((61, 76, 65))
    title = text_format("SNAKE", game_font, 140, (255, 255, 255))
    rules = text_format("The objective of the game is to get the biggest snake.", game_font, 35, (255,255,255))
    rules1 = text_format("The more apples you eat, the longer snake you get", game_font, 35, (255,255,255))
    rules2 = text_format("and if you run into yourself, or the edges, you die!", game_font, 35, (255,255,255))
    indication = text_format("Use your arrow keys to navigate", game_font, 30, (255,255,255))
    if choix == 1 :
        text_start = text_format("START", game_font, 95, (153, 153, 153))
    else:
        text_start = text_format("START", game_font, 80, (255, 240, 255))
    if choix == 2:
        text_quit = text_format("QUIT", game_font, 95, (153, 153, 153))
    else:
        text_quit = text_format("QUIT", game_font, 80, (255, 240, 255))
        

    title_rect = title.get_rect()
    start_rect = text_start.get_rect()
    quit_rect = text_quit.get_rect()
    rules_rect = rules.get_rect()
    rules_rect1 = rules1.get_rect()
    rules_rect2 = rules2.get_rect()
    indication_rect = indication.get_rect()
    
    screen.blit(title, (screen_width/2 - (title_rect[2]/2), 60))
    screen.blit(text_start, (screen_width/2 + 225 - (start_rect[2]/2), 600))
    screen.blit(text_quit, (screen_width/2 - 225 - (quit_rect[2]/2), 600))
    screen.blit(rules, (screen_width/2 - (rules_rect[2]/2), 340))
    screen.blit(rules1, (screen_width/2 - (rules_rect1[2]/2), 390))
    screen.blit(rules2, (screen_width/2 - (rules_rect2[2]/2), 440))
    screen.blit(indication, (screen_width/2 - (indication_rect[2]/2), 760))
    
    pygame.display.update()
    clock.tick(10)
    pygame.display.set_caption("Jeu de Snake - Projet 1ère NSI")

pygame.time.set_timer(pygame.USEREVENT,150)

main_game = MAIN() 
while True:
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			pygame.quit()
			sys.exit()
		if event.type == pygame.USEREVENT:
			main_game.update()
		if event.type == pygame.KEYDOWN:
			if event.key == pygame.K_UP:
				if main_game.snake.direction.y != 1:
					main_game.snake.direction = Vector2(0,-1)
			if event.key == pygame.K_RIGHT:
				if main_game.snake.direction.x != -1:
					main_game.snake.direction = Vector2(1,0)
			if event.key == pygame.K_DOWN:
				if main_game.snake.direction.y != -1:
					main_game.snake.direction = Vector2(0,1)
			if event.key == pygame.K_LEFT:
				if main_game.snake.direction.x != 1:
					main_game.snake.direction = Vector2(-1,0)

	screen.fill((175,215,70))
	main_game.draw_elements()
	pygame.display.update()
	clock.tick(60)




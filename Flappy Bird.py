import math

import pygame as pg
from sys import exit
from random import randint

pg.init()
pg.mixer.init()

pg.display.set_caption('Flappy Bird')

WIDTH = 1200
HEIGHT = 800
screen = pg.display.set_mode((WIDTH, HEIGHT))

game_active = False

font = 'Font/PixeloidSansBold-PKnYd.ttf'

text = pg.font.Font(font, 100)
subtext = pg.font.Font(font, 50)
small_subtext = pg.font.Font(font, 20)

jump = pg.mixer.Sound('FlappyBird/Bird/Jump.mp3')
death = pg.mixer.Sound('FlappyBird/Bird/Death.mp3')
point = pg.mixer.Sound('FlappyBird/Bird/Point.mp3')
fall = pg.mixer.Sound('FlappyBird/Bird/Fall.mp3')

jump.set_volume(0.25)
death.set_volume(0.25)
point.set_volume(0.25)
fall.set_volume(0.25)

border_color = 167, 115, 37
board_color = 229, 150, 31

score = 0
hi_score = int(open('High_score', 'r').read())


class Obstacle(pg.sprite.Sprite):
	def __init__(self):
		super().__init__()
		self.times = 0
		self.cropped_pipe_bot_default = None
		self.rect_bot_default = None
		self.rect_top_default = None
		self.pipey = 0

		self.image = pg.image.load('FlappyBird/Pipe.png').convert_alpha()

		self.image_top = pg.transform.rotozoom(self.image, 0, 0.5)
		self.image_bot = pg.transform.rotozoom(self.image, 180, 0.5)

		self.rect_top = self.image_top.get_rect()
		self.rect_bot = self.image.get_rect()

		self.rect_top.center = 1200, 800
		self.rect_bot.center = 1270, 240

		self.cropped_pipe_bot = self.image_top.subsurface((0, 0), (self.rect_top.width, 700 - self.rect_top.top))
		self.pipe_list_top = []
		self.pipe_list_bot = []

	def pipe_move(self):
		self.pipey = randint(700, 1000)
		self.rect_top_default = self.image_top.get_rect()
		self.rect_bot_default = self.image_bot.get_rect()
		self.rect_top_default.center = 1300, self.pipey
		self.rect_bot_default.center = 1300, self.pipey - 900
		keys = pg.key.get_pressed()
		if keys[pg.K_SPACE] and self.times == 0:
			self.pipe_list_top.append(self.rect_top_default)
			self.pipe_list_bot.append(self.rect_bot_default)
			self.times += 1
		for rect in self.pipe_list_top:
			self.cropped_pipe_bot_default = self.image_top.subsurface((0, 0), (rect.width, 700 - rect.top))
			screen.blit(self.cropped_pipe_bot_default, rect)
			rect.x -= 4
			if rect.x == 900 or rect.x == 901 or rect.x == 902 or rect.x == 903:
				self.pipe_list_top.append(self.rect_top_default)
				self.pipe_list_bot.append(self.rect_bot_default)

			if rect.centerx < -400:
				self.pipe_list_top.remove(rect)
		for rect in self.pipe_list_bot:
			screen.blit(self.image_bot, rect)
			rect.x -= 4
			if rect.centerx < -400:
				self.pipe_list_bot.remove(rect)

	def draw(self):
		for rect in self.pipe_list_bot:
			screen.blit(self.image_bot, rect)
		for rect in self.pipe_list_top:
			self.cropped_pipe_bot_default = self.image_top.subsurface((0, 0), (rect.width, 700 - rect.top))
			screen.blit(self.cropped_pipe_bot_default, rect)

	def update(self):
		self.pipe_move()


class Background(pg.sprite.Sprite):

	def __init__(self):
		super().__init__()

		self.bground_rect_default = None
		self.ground_rect_default = None
		self.bground = pg.image.load('FlappyBird/background.png').convert()
		self.ground = pg.image.load('FlappyBird/Ground_changed.png').convert()

		self.bground_rect = self.bground.get_rect()
		self.bground_rect.topleft = 0, -300

		self.ground_rect = self.ground.get_rect()
		self.ground_rect.topleft = 0, 700

		self.bground_list = [self.bground_rect]
		self.ground_list = [self.ground_rect]

	def draw(self):
		for bg_rect in self.bground_list:
			screen.blit(self.bground, bg_rect)
		for ground_rect in self.ground_list:
			screen.blit(self.ground, ground_rect)

	def movemment(self):
		self.bground_rect_default = self.bground.get_rect()
		self.bground_rect_default.topleft = 1400, -300

		self.ground_rect_default = self.ground.get_rect()
		self.ground_rect_default.topleft = 1090, 700

		for bg_rect in self.bground_list:
			screen.blit(self.bground, bg_rect)
			bg_rect.x -= 1
			if bg_rect.right == 1500:
				self.bground_list.append(self.bground_rect_default)
			if bg_rect.right < -1000:
				self.bground_list.remove(bg_rect)

		for ground_rect in self.ground_list:
			screen.blit(self.ground, ground_rect)
			ground_rect.x -= 4
			if ground_rect.right == 1200 or ground_rect.right == 1201 or ground_rect.right == 1202 or ground_rect.right == 1203:
				self.ground_list.append(self.ground_rect_default)
			if ground_rect.right < -100:
				self.ground_list.remove(ground_rect)

	def update(self):
		self.movemment()


class Player(pg.sprite.Sprite):
	def __init__(self):
		pg.sprite.Sprite.__init__(self)
		frame1 = pg.image.load('FlappyBird/Bird/Bird_frame1-removebg.png').convert_alpha()
		frame2 = pg.image.load('FlappyBird/Bird/Bird_frame2-removebg.png').convert_alpha()
		frame3 = pg.image.load('FlappyBird/Bird/Bird_frame3-removebg.png').convert_alpha()
		frame4 = pg.image.load('FlappyBird/Bird/Bird_frame4-removebg.png').convert_alpha()
		self.png = pg.image.load('FlappyBird/PNGpic.png').convert_alpha()
		self.png = pg.transform.scale(self.png, (25, 38))
		self.animation = [frame1, frame2, frame3, frame4]
		self.player_index = 0
		self.image = self.animation[int(self.player_index)]

		self.n = 0
		self.gravity = 0
		self.image = pg.transform.rotozoom(self.image, 0, 0.25)
		self.rotate1 = 0
		self.rotate2 = 0
		self.center = 0
		self.rect = self.png.get_rect()
		self.rect.center = 330, HEIGHT / 2 + 10 * math.sin(self.n) + 10

	def movement(self):
		screen.blit(self.image, (self.rect.x - 10, self.rect.y - 10))

	def animation_run(self):
		self.center -= self.rotate1
		self.rotate2 += self.center
		if self.rotate2 < -90:
			self.rotate2 = -90

		self.player_index += 0.12
		if self.player_index >= 4:
			self.player_index = 0
		self.image = self.animation[int(self.player_index)]
		self.image = pg.transform.rotozoom(self.image, self.rotate2, 0.25)
		self.rect.centery += self.gravity
		self.gravity += 0.6
	def animation_start(self):

		if self.n > 360:
			self.n = 0
		self.n += 0.08

	def update(self):
		self.animation_run()
		self.movement()


class Scoreboard(pg.sprite.Sprite):
	def __init__(self):
		super().__init__()
		self.image = pg.surface.Surface((WIDTH / 2 - WIDTH / 4, HEIGHT - 200))
		self.image.fill(board_color)
		self.rect = self.image.get_rect()
		self.rect.center = WIDTH / 2, HEIGHT / 2 - 1000

		self.score = subtext.render('SCORE', False, 'White')
		self.score_rect = self.score.get_rect()
		self.score_rect.center = WIDTH / 2, 250

		self.hi_score_text = subtext.render('HI SCORE', False, 'White')
		self.hi_score_text_rect = self.hi_score_text.get_rect()
		self.hi_score_text_rect.center = WIDTH/2, 450

		self.borderx = 440
		self.bordery = -910

		self.score_count = subtext.render(str(score), False, 'White')
		self.score_count_rect = self.score_count.get_rect()
		self.score_count_rect.center = WIDTH / 2, 325

		self.hi_score = subtext.render(str(hi_score), False, 'White')
		self.hi_score_rect = self.hi_score.get_rect()
		self.hi_score_rect.center = WIDTH / 2, 525

		self.restart = subtext. render('Press SPACE to restart', False, 'White')
		self.restart_rect = self.restart.get_rect()
		self.restart_rect.center = WIDTH / 2, HEIGHT - 50

	def update(self):
		pg.draw.rect(screen, border_color, (self.borderx, self.bordery, WIDTH / 2 - WIDTH / 4 + 20, HEIGHT - 180))
		screen.blit(self.image, self.rect)
		if self.rect.centery != HEIGHT / 2:
			self.rect.centery += 20
			self.bordery += 20
		else:
			screen.blit(self.score, self.score_rect)
			screen.blit(self.score_count, self.score_count_rect)

			screen.blit(self.hi_score_text, self.hi_score_text_rect)
			screen.blit(self.hi_score, self.hi_score_rect)

			screen.blit(self.restart, self.restart_rect)


player = Player()
scoreboard = Scoreboard()
background = Background()
obstacle = Obstacle()

pipe_time = pg.USEREVENT + 1
pg.time.set_timer(pipe_time, 1840)
clock = pg.time.Clock()

score_surf = text.render(str(score), False, 'White')
score_rect = score_surf.get_rect()
score_rect.center = WIDTH / 2, 100

hi_score_surf = small_subtext.render(f'HIGH SCORE: {hi_score}', False,'White')
hi_score_rect = hi_score_surf.get_rect()
hi_score_rect.topleft = 20, 20

press_space = subtext.render('Press SPACE to start', False, 'White')
press_space_rect = press_space.get_rect()
press_space_rect.center = WIDTH / 2, HEIGHT / 2 + 100

time_death = 0

death_screen = False
while True:
	score_rect = score_surf.get_rect()
	score_rect.center = WIDTH / 2, 100
	for event in pg.event.get():
		if event.type == pg.QUIT:
			with open('High_score', 'w') as file:
				file.write(str(hi_score))
			pg.quit()
			exit()
		if game_active:
			if event.type == pg.KEYDOWN:
				if event.key == pg.K_SPACE and player.rect.y > -100:
					player.gravity = -10
					player.rotate2 = 20
					player.rotate1 = 0.14
					player.center = 1.3
					pg.mixer.Sound.play(jump)
		elif death_screen:
			scoreboard.score_count = subtext.render(str(score), False, 'White')
			scoreboard.score_count_rect = scoreboard.score_count.get_rect()
			scoreboard.score_count_rect.center = WIDTH / 2, 325

			scoreboard.hi_score = subtext.render(str(hi_score), False, 'White')
			scoreboard.hi_score_rect = scoreboard.hi_score.get_rect()
			scoreboard.hi_score_rect.center = WIDTH / 2, 525
			if event.type == pg.KEYDOWN and event.key == pg.K_SPACE and time_death > 130:
					time_death = 0
					death_screen = False

		else:
			score = 0
			scoreboard.rect.y = HEIGHT / 2 - 1000
			scoreboard.bordery = -610
			if event.type == pg.KEYDOWN and event.key == pg.K_SPACE:
					pg.mixer.Sound.play(jump)
					player.gravity = -10
					player.rotate2 = 20
					player.rotate1 = 0.14
					player.center = 1.3
					game_active = True
	if game_active:
		hi_score_surf = small_subtext.render(f'HIGH SCORE: {hi_score}', False, 'White')
		score_surf = text.render(str(score), True, 'White')
		background.update()
		obstacle.update()
		player.update()
		screen.blit(score_surf, score_rect)
		screen.blit(hi_score_surf, hi_score_rect)

	elif death_screen:
		time_death += 1
		if time_death == 15:
			player.gravity = 0
			background.draw()
			obstacle.draw()
			player.update()
			screen.blit(hi_score_surf, hi_score_rect)
			screen.blit(score_surf, score_rect)
		if time_death > 40:
			if time_death == 41:
				fall.play()
				player.gravity = 0
			if player.rect.centery < HEIGHT + 100:
				player.rotate1 = 0
				player.center = 0
				background.draw()
				obstacle.draw()
				player.update()
			else:
				background.draw()
				obstacle.draw()
				scoreboard.update()

	else:
		score_surf = text.render(str(score), True, 'White')
		background.draw()
		player.animation_start()
		player.update()
		screen.blit(hi_score_surf, hi_score_rect)
		screen.blit(score_surf, score_rect)
		screen.blit(press_space, press_space_rect)
		if obstacle.pipe_list_top:
			obstacle.pipe_list_top = [obstacle.rect_top_default]
			obstacle.pipe_list_bot = [obstacle.rect_bot_default]
		player.rect.centery = HEIGHT / 2 + 10 * math.sin(player.n) + 10
		player.rotate2 = 0
		player.rotate1 = 0
		player.center = 0

		player.gravity = 0

	if game_active:
		if player.rect.y > 650:
			pg.mixer.Sound.play(death)
			game_active = False
			death_screen = True
		for rect in obstacle.pipe_list_bot:
			if player.rect.colliderect(rect):
				pg.mixer.Sound.play(death)
				game_active = False
				death_screen = True
		for rect in obstacle.pipe_list_top:
			if rect.x == 290 or rect.x == 291 or rect.x == 292 or rect.x == 293:
				point.play()
				score += 1
				if hi_score < score:
					hi_score = score
			if player.rect.colliderect(rect):
				pg.mixer.Sound.play(death)
				game_active = False

	pg.display.update()

	clock.tick(65)

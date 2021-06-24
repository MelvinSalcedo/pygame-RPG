import pygame
import os
import random

pygame.init()

BG = (144, 201, 120)
RED = (255, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)

SCREEN_WIDTH = 1100
SCREEN_HEIGHT = 600
SCROLL_THRESH = 200

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Shooter')


clock = pygame.time.Clock()
FPS = 60

#gravedad del juego
GRAVITY = 0.75
rangoCamintadaIA = 120
screen_scroll = 0
#variabless para mover al personaje derecha o izquierda
mover_izquierda = False
mover_derecha = False
cast_magia = False
cast_magia_saliranimacion = False

#piso del esenario
piso = SCREEN_HEIGHT-100
font = pygame.font.SysFont('Futura', 30)


mountaña = pygame.image.load("img/background/mountain.png").convert_alpha()
pinos = pygame.image.load("img/background/pine1.png").convert_alpha()
nuves = pygame.image.load("img/background/sky_cloud.png").convert_alpha()
suelo = pygame.image.load("img/background/suelo.png").convert_alpha()
RED = (255, 0, 0)

sonidoSaltar=pygame.mixer.Sound("pj.wav")

itemVida = pygame.image.load('img/icons/health_box.png').convert_alpha()
itemMagia = pygame.image.load('img/icons/ammo_box.png').convert_alpha()
imgMagia = pygame.image.load("img/icons/magia.png").convert_alpha()

cajaItems = {
	'Health'	: itemVida,
	'magia'		: itemMagia,
}

bg_scroll = 0
widht_imagenBG=1376 #la cantidad en pixeles de la imagen de background que cargamos
LimiteFor=3
def draw_bg():
	
	for x in range(LimiteFor):
		screen.blit(nuves,(x*widht_imagenBG-bg_scroll,0))#5,0 ....150,0
		screen.blit(mountaña,(x*widht_imagenBG-bg_scroll,200))#5,0
		screen.blit(pinos,(x*widht_imagenBG-bg_scroll,270))#5,0
		screen.blit(suelo,(x*widht_imagenBG-bg_scroll,270))#5,0


def draw_text(text, font, text_col, x, y):
	img = font.render(text, True, text_col)
	screen.blit(img, (x, y))


class Player(pygame.sprite.Sprite):
	def __init__(self,tipo_personaje, x, y, scale, velocidad,cantidad_magia):
		pygame.sprite.Sprite.__init__(self)
		self.estoyVivo = True
		self.tipo_personaje =tipo_personaje
		self.velocidad = velocidad
		self.direction = 1
		self.vel_y = 0
		self.saltar = False
		self.in_air = True
		self.flip = False
		self.lista_animacion = []
		self.indice_NumeroImagen = 0
		self.accion = 0
		self.tiempoObtenido = pygame.time.get_ticks()
		
		#cargamos todas las animaciones que se nesesiten
		animation_types = ['Idle', 'Run', 'Jump','Death','atack']

		for animation in animation_types:
			#se crear una nueva lista en cada for
			temp_list = []
			#ccontanmos el numero de archivos en un folder
			num_of_frames = len(os.listdir(f'img/{self.tipo_personaje}/{animation}')) # longitud de mi carpeta
			#0,1,2,3,
			for i in range(num_of_frames):
				img = pygame.image.load(f'img/{self.tipo_personaje}/{animation}/{i}.png')
				img = pygame.transform.scale(img, (int(img.get_width() * scale), int(img.get_height() * scale)))
				temp_list.append(img)
			self.lista_animacion.append(temp_list)

		self.image = self.lista_animacion[self.accion][self.indice_NumeroImagen]
		self.rect = self.image.get_rect()
		self.rect.center = (x, y)

		self.tiempo_casteo = 0
		self.cantidad_magia = cantidad_magia
		self.health=100
		self.radius = self.rect.width/2 

		self.move_counter = 0
		self.vision = pygame.Rect(0, 0, 150, 20) # 75,10
		self.EstoyMirandoPlayer = False
		self.EstoyMirandoPlayer_counter = 0
		self.estoyAtacando=False
		self.max_health = self.health

	def update(self):
		self.actualizarAnimacion()
		self.verificarEstoyVivo()
		#uactualiamos tiempo
		if self.tiempo_casteo > 0: #20 # espera 20 ejeciccion del while principal para ejecurtarse otra vez
			self.tiempo_casteo -= 1 #0
	
	def castearMagia(self):
		if self.tiempo_casteo == 0 and self.cantidad_magia > 0:
			self.estoyAtacando=True
			self.actualizarAccion(4)


			self.tiempo_casteo = 30
			magiaFuego = MagiaFuego(self.rect.centerx + (80 * self.direction),self.rect.centery, self.direction,0.15)
			grupo_magiasDisparadas.add(magiaFuego)
			#reducimos la cantidad de magia
			self.cantidad_magia -= 1

	def verificarEstoyVivo(self):
		if self.health <= 0:
			self.health = 0
			self.velocidad = 0
			self.estoyVivo = False
			self.actualizarAccion(3)

	def mover_player(self, moving_left, moving_right):
		#reseteamos las variables de movimiento
		screen_scroll = 0
		dx = 0
		dy = 0

		#si 
		if moving_left:
			dx = -self.velocidad
			self.flip = True
			self.direction = -1
		if moving_right:
			dx = self.velocidad
			self.flip = False
			self.direction = 1

		#Accion de saltar
		if self.saltar == True and self.in_air == False:
			self.vel_y = -15
			self.saltar = False
			self.in_air = True

		#aplicamos gravedad
		self.vel_y += GRAVITY #-11+1 =-10 0 1
		
		if self.vel_y > 10:
			self.vel_y
		dy += self.vel_y # 0-10

		#verificamos la colision con el suelo
		if (self.rect.bottom-50) + dy > piso:
			dy = piso - (self.rect.bottom -50) #y  de abajo de mi imagen
			self.in_air = False

		if self.tipo_personaje == 'player':
			if self.rect.left + dx < 0 or self.rect.right + dx > SCREEN_WIDTH+400:
				dx = 0

		#actualizamos la posicion de la imagen del player
		self.rect.x += dx
		self.rect.y += dy

		if self.tipo_personaje == 'player': #
			if (self.rect.right > SCREEN_WIDTH - SCROLL_THRESH and bg_scroll <  SCREEN_WIDTH*LimiteFor-SCREEN_WIDTH)\
				or (self.rect.left < SCROLL_THRESH and bg_scroll > abs(dx)):
				self.rect.x -= dx # se hace cero
				screen_scroll -=dx  # -5
		print(bg_scroll)
		return screen_scroll

	def actualizarAnimacion(self):
		ANIMATION_COOLDOWN = 100
		self.image = self.lista_animacion[self.accion][self.indice_NumeroImagen]
		#si paso 100 milisegundos cambiamos a la sigu	einte imagen
		

		if pygame.time.get_ticks() - self.tiempoObtenido > ANIMATION_COOLDOWN:
			self.tiempoObtenido = pygame.time.get_ticks()
			self.indice_NumeroImagen += 1
		#if llego al tope del totoal de iamgenes se reiniciar la animacion desde cero
		if self.indice_NumeroImagen >= len(self.lista_animacion[self.accion]):
			if(self.accion==4):
				self.estoyAtacando=False
			if self.accion == 3:
				self.indice_NumeroImagen = len(self.lista_animacion[self.accion]) - 1

			else:
				self.indice_NumeroImagen = 0

	def actualizarAccion(self, accion):#1
		#dependiendo de la tecla que presionemos vamos a actuializar la animacion
		if accion != self.accion:
			self.accion = accion
			#actualizamos la imagen
			self.indice_NumeroImagen = 0
			self.update_time = pygame.time.get_ticks()

	def InteligenciaArtificialNormal(self):
		if self.estoyVivo :#and player.estoyVivo:
			if self.EstoyMirandoPlayer == False and random.randint(1, 200) == 1:
				#sonidoDOlor.play()
				self.actualizarAccion(0)#0: idle

				self.EstoyMirandoPlayer = True
				self.EstoyMirandoPlayer_counter = 50
			#verificamos si la AI esta cerca del personaje
			if self.vision.colliderect(player.rect):
				#detenerse y mirar al personaje
				self.actualizarAccion(4)#0: estado idle
				#estado castear magina
				self.castearMagia()
			else:
				if self.EstoyMirandoPlayer == False: # esta caminando
					if self.direction == 1:
						ai_moverDerecha = True
					else:
						ai_moverDerecha = False
					ai_moverIzquierda = not ai_moverDerecha
					self.mover_player(ai_moverIzquierda, ai_moverDerecha)
					self.actualizarAccion(1)#1: estado de caminar
					self.move_counter += 1
					#actualiamos la vision del persoje
					self.vision.center = (self.rect.centerx + 75 * self.direction, self.rect.centery)

					if self.move_counter > rangoCamintadaIA: #verifica que no sobrepase el limite de caminanata
						self.direction *= -1  # verifica la direccion de caminata
						self.move_counter *= -1
				else:
					self.EstoyMirandoPlayer_counter -= 1
					if self.EstoyMirandoPlayer_counter <= 0:
						self.EstoyMirandoPlayer = False

		self.rect.x += screen_scroll

	def InteligenciaArtificialBoss(self):
		if self.estoyVivo :#and player.estoyVivo:
			if self.EstoyMirandoPlayer == False and random.randint(1, 200) == 1:
				#sonidoDOlor.play()
				self.actualizarAccion(0)#0: idle

				self.EstoyMirandoPlayer = True
				self.EstoyMirandoPlayer_counter = 5
			#verificamos si la AI esta cerca del personaje
			if self.vision.colliderect(player.rect):
				#detenerse y mirar al personaje
				self.actualizarAccion(4)#0: estado idle
				#estado castear magina
				self.castearMagia()
			else:
				if self.EstoyMirandoPlayer == False: # esta caminando
					if self.direction == 1:
						ai_moverDerecha = True
					else:
						ai_moverDerecha = False
					ai_moverIzquierda = not ai_moverDerecha
					self.mover_player(ai_moverIzquierda, ai_moverDerecha)
					self.actualizarAccion(1)#1: estado de caminar
					self.move_counter += 1
					#actualiamos la vision del persoje
					self.vision.center = (self.rect.centerx + 75 * self.direction, self.rect.centery)

					if self.move_counter > rangoCamintadaIA: #verifica que no sobrepase el limite de caminanata
						self.direction *= -1  # verifica la direccion de caminata
						self.move_counter *= -1
				else:
					self.EstoyMirandoPlayer_counter -= 1
					if self.EstoyMirandoPlayer_counter <= 0:
						self.EstoyMirandoPlayer = False

		self.rect.x += screen_scroll


	def draw(self):
		screen.blit(pygame.transform.flip(self.image, self.flip, False), self.rect)

class MagiaFuego(pygame.sprite.Sprite):
	def __init__(self, x, y, direccion,scale):
		pygame.sprite.Sprite.__init__(self)
		self.velocidad = 10
		img = pygame.image.load("img/icons/bullet.png")
		if(direccion>0):
			img2 = pygame.transform.flip(img, False, False)
		else:
			img2 = pygame.transform.flip(img, True, False)
		self.image = pygame.transform.scale(img2, (int(img2.get_width() * scale), int(img2.get_height() * scale)))

		#self.image = self.image.flip(True,False)
		self.rect = self.image.get_rect()
		self.rect.center = (x, y)
		self.direccion = direccion

	def update(self): 
		#mover magia direccion siempre va a ser +1 -1
		self.rect.x += (self.direccion * self.velocidad)+ screen_scroll
		#verificamos si la magia a salido de la ventana de render
		if self.rect.right < 0 or self.rect.left > SCREEN_WIDTH:
			self.kill()
		self.verificarColision()
	def verificarColision(self):
		#verificamos si a colisionado con alguien
		if pygame.sprite.spritecollide(player, grupo_magiasDisparadas, False,pygame.sprite.pygame.sprite.collide_circle_ratio(.25)):
			if player.estoyVivo:
				player.health -= 5
				self.kill()
		if pygame.sprite.spritecollide(enemy, grupo_magiasDisparadas,False,pygame.sprite.pygame.sprite.collide_circle_ratio(.25)):
			if enemy.estoyVivo:
				enemy.health -= 25
				self.kill()
		if pygame.sprite.spritecollide(enemy1, grupo_magiasDisparadas,False,pygame.sprite.pygame.sprite.collide_circle_ratio(.25)):
			if enemy1.estoyVivo:
				enemy1.health -= 25
				self.kill()
		if pygame.sprite.spritecollide(enemy2, grupo_magiasDisparadas,False,pygame.sprite.pygame.sprite.collide_circle_ratio(.25)):
			if enemy2.estoyVivo:
				enemy2.health -= 25
				self.kill()

class CajaItems(pygame.sprite.Sprite):
	def __init__(self, item_type, x, y):
		pygame.sprite.Sprite.__init__(self)
		self.item_type = item_type
		self.image = cajaItems[self.item_type]
		self.rect = self.image.get_rect()
		self.rect.midtop = (x,y)

	def update(self):
		self.rect.x += screen_scroll
		#verificamos si a ahabido colision con el player
		if pygame.sprite.collide_rect(self, player):
		#if pygame.sprite.spritecollide(player, grupovidas,False,pygame.sprite.pygame.sprite.collide_circle_ratio(.25)):
			#verificamos con que objeto a colisionado
			if self.item_type == 'Health':
				player.health += 5 #98+5=103
				if player.health > player.max_health:
					player.health = player.max_health
			elif self.item_type == 'magia':
				player.cantidad_magia += 10
		
			self.kill()

class HealthBar():
	def __init__(self, x, y, health, max_health):
		self.x = x
		self.y = y
		self.health = health
		self.max_health = max_health

	def draw(self, Ehealth):

		#se acutaliza constantemente la vida segun nos agan daño
		self.health = Ehealth
		#dibujamos el borde de la vida 
		draw_text('Vida: ', font, WHITE, 20, 10)
		ratio = self.health #95/100 =0.95
		pygame.draw.rect(screen, BLACK, (self.x - 2, self.y - 2, 250+4, 24))
		pygame.draw.rect(screen, RED, (self.x, self.y, 250, 20))
		pygame.draw.rect(screen, GREEN, (self.x, self.y, ratio*2.5, 20))

player = Player("player",200, 200, .7, 5,10)
health_bar = HealthBar(90, 10, player.health, player.health)

enemy  = Player("enemy", 600, 500, .7, 2,20)
enemy1  = Player("enemy", 1200, 500, .7, 2,20)
enemy2 = Player("boss", 1800, 600, 1.1, 2,20)

grupo_magiasDisparadas = pygame.sprite.Group()
item_box_group = pygame.sprite.Group()

item_box = CajaItems('Health', 800, 450)
item_box_group.add(item_box)

item_box = CajaItems('magia', 400, 450)
item_box_group.add(item_box)


run = True

while run:
	clock.tick(FPS)
	###################EVENTOS###################
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			run = False
		if event.type == pygame.KEYDOWN: #presionanadose sin soltar
			if event.key == pygame.K_a:
				mover_izquierda = True
			if event.key == pygame.K_d:
				mover_derecha = True
			if event.key == pygame.K_w and player.estoyVivo:
				sonidoSaltar.play()
				player.saltar = True
			if event.key == pygame.K_SPACE:
				cast_magia = True
				cast_magia_saliranimacion=True
			if event.key == pygame.K_ESCAPE:
				run = False

		if event.type == pygame.KEYUP:
			if event.key == pygame.K_a:
				mover_izquierda = False
			if event.key == pygame.K_d:
				mover_derecha = False
			if event.key == pygame.K_SPACE:
				cast_magia = False

	############LOGICA DEL JUEGO ###########
	if player.estoyVivo:
		if cast_magia:
			player.castearMagia()
			#player.actualizarAccion(4)#2: saltar
		'''if cast_magia_saliranimacion :
			player.actualizarAccion(4)#2: saltar'''
		if player.in_air:
			player.actualizarAccion(2)#2: saltar
		elif mover_izquierda or mover_derecha:
			player.actualizarAccion(1)#1: correr
		elif player.estoyAtacando :
			player.actualizarAccion(4)#1: correr
		else:
			player.actualizarAccion(0)#0: quieto
		player.mover_player(mover_izquierda, mover_derecha)

	############RENDER####################
	
	draw_bg() # dibujar el fondo


	draw_text('Mana: ', font, WHITE, 10, 35)
	for x in range(player.cantidad_magia):
		screen.blit(imgMagia, (90 + (x * 12), 40))
		

	screen_scroll = player.mover_player(mover_izquierda, mover_derecha)
	bg_scroll -= screen_scroll

	item_box_group.update()
	item_box_group.draw(screen)

	player.update()
	player.draw() # dibuja al jugador

	enemy.InteligenciaArtificialNormal()
	enemy.draw()
	enemy.update()

	enemy1.InteligenciaArtificialNormal()
	enemy1.draw()
	enemy1.update()

	enemy2.InteligenciaArtificialBoss()
	enemy2.draw()
	enemy2.update()
	
	grupo_magiasDisparadas.draw(screen)
	grupo_magiasDisparadas.update()

	health_bar.draw(player.health)

	pygame.display.flip()# actualizar pantalla
pygame.quit()
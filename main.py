import pygame
import os

pygame.init()


SCREEN_WIDTH = 800
SCREEN_HEIGHT = int(SCREEN_WIDTH * 0.8)

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Shooter')


clock = pygame.time.Clock()
FPS = 60

#gravedad del juego
GRAVITY = 0.75

#variabless para mover al personaje derecha o izquierda
mover_izquierda = False
mover_derecha = False
cast_magia = False
cast_magia_saliranimacion = False

#piso del esenario
piso = SCREEN_HEIGHT-100



BG = pygame.image.load("img/background/mountain.png")
BG2 = pygame.image.load("img/background/sky_cloud.png")
BG3 = pygame.image.load("img/background/suelo.png")
BG3 = pygame.image.load("img/background/suelo.png")
RED = (255, 0, 0)

def draw_bg():
	screen.blit(BG2,(0,0))
	screen.blit(BG,(0,250))
	screen.blit(BG3,(0,300))
	screen.blit(BG3,(500,300))




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

	def update(self):
		self.actualizarAnimacion()
		self.verificarEstoyVivo()
		#update cooldown
		if self.tiempo_casteo > 0: #20 # espera 20 ejeciccion del while principal para ejecurtarse otra vez
			self.tiempo_casteo -= 1 #0
	def castearMagia(self):
		if self.tiempo_casteo == 0 and self.cantidad_magia > 0:
			self.tiempo_casteo = 20
			magiaFuego = MagiaFuego(self.rect.centerx + (80 * self.direction),self.rect.centery, self.direction,0.2)
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

		#actualizamos la posicion de la imagen del player
		self.rect.x += dx
		self.rect.y += dy

	def actualizarAnimacion(self):
		ANIMATION_COOLDOWN = 100
		self.image = self.lista_animacion[self.accion][self.indice_NumeroImagen]
		#si paso 100 milisegundos cambiamos a la sigu	einte imagen
		if pygame.time.get_ticks() - self.tiempoObtenido > ANIMATION_COOLDOWN:
			self.tiempoObtenido = pygame.time.get_ticks()
			self.indice_NumeroImagen += 1
		#if llego al tope del totoal de iamgenes se reiniciar la animacion desde cero
		if self.indice_NumeroImagen >= len(self.lista_animacion[self.accion]):
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
		self.rect.x += (self.direccion * self.velocidad)
		#verificamos si la magia a salido de la ventana de render
		if self.rect.right < 0 or self.rect.left > SCREEN_WIDTH:
			self.kill()
		self.verificarColision()
	def verificarColision(self):
		#verificamos si a colisionado con alguien
		'''if pygame.sprite.spritecollide(player, grupo_magiasDisparadas, False):
			if player.estoyVivo:
				player.health -= 5
				self.kill()'''
		if pygame.sprite.spritecollide(enemy, grupo_magiasDisparadas,False,pygame.sprite.pygame.sprite.collide_circle_ratio(.25)):
			if enemy.estoyVivo:
				enemy.health -= 25
				self.kill()

player = Player("player",200, 200, .7, 5,20)
enemy  = Player("enemy", 600, 500, .7, 5,20)

grupo_magiasDisparadas = pygame.sprite.Group()


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
		else:
			player.actualizarAccion(0)#0: quieto
		player.mover_player(mover_izquierda, mover_derecha)

	
	############RENDER####################
	
	draw_bg() # dibujar el fondo

	player.update()
	player.draw() # dibuja al jugador

	enemy.draw()
	enemy.update()
	
	grupo_magiasDisparadas.draw(screen)
	grupo_magiasDisparadas.update()

	pygame.display.flip()# actualizar pantalla
pygame.quit()
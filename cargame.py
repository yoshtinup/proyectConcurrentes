import pygame
from pygame.locals import *
import random
import threading
import time

# Parámetros de forma
tamaño = ancho, alto = (800, 800)
ancho_carretera = int(ancho / 1.6)
ancho_marca_carretera = int(ancho / 80)
# Parámetros de ubicación
carril_derecho = ancho / 2 + ancho_carretera / 4
carril_izquierdo = ancho / 2 - ancho_carretera / 4
# Parámetros de animación
velocidad = 15

# Inicializar Pygame
pygame.init()
corriendo = True

# Establecer tamaño de ventana
pantalla = pygame.display.set_mode(tamaño)
# Establecer título de ventana
pygame.display.set_caption("Juego de coches de Mariya")
# Establecer color de fondo
pantalla.fill((60, 220, 0))
# Aplicar cambios
pygame.display.update()

# Cargar vehículo del jugador
coche = pygame.image.load("car.png")
# Redimensionar imagen
# coche = pygame.transform.scale(coche, (250, 250))
ubicacion_coche = coche.get_rect()
ubicacion_coche.center = carril_derecho, alto * 0.8

# Cargar vehículo enemigo
coche_enemigo = pygame.image.load("otherCar.png")
ubicacion_coche_enemigo = coche_enemigo.get_rect()
ubicacion_coche_enemigo.center = carril_izquierdo, alto * 0.2

contador = 0

# Semáforo para controlar el acceso a la variable compartida
semáforo = threading.Semaphore()

# Barrera para sincronizar hilos
barrera = threading.Barrier(2)

# Lista de notificaciones
notificaciones = []

# Función para hilo de fondo 1 (Hilo de notificación)
def hilo_fondo1():
    global notificaciones
    while True:
        time.sleep(5)  # Dormir durante 5 segundos
        # Agregar una notificación
        semáforo.acquire()
        notificaciones.append("Notificación del Hilo 1")
        semáforo.release()

# Función para hilo de fondo 2 (Hilo de aumento de nivel)
def hilo_fondo2():
    global velocidad
    while True:
        barrera.wait()  # Esperar a que todos los hilos lleguen a este punto
        time.sleep(5)  # Dormir durante 5 segundos
        # Aumentar la velocidad del juego
        semáforo.acquire()
        velocidad += 0.15
        semáforo.release()

# Iniciar hilos de fondo
hilo1 = threading.Thread(target=hilo_fondo1)
hilo2 = threading.Thread(target=hilo_fondo2)
hilo1.daemon = True
hilo2.daemon = True
hilo1.start()
hilo2.start()

# Bucle del juego
while corriendo:
    contador += 1

    # Aumentar la dificultad del juego con el tiempo
    if contador == 5000:
        # Notificar a todos los hilos para aumentar el nivel
        barrera.wait()
        contador = 0
        print("Nivel aumentado", velocidad)

    # Animar vehículo enemigo
    ubicacion_coche_enemigo[1] += velocidad
    if ubicacion_coche_enemigo[1] > alto:
        # Seleccionar carril al azar
        if random.randint(0, 1) == 0:
            ubicacion_coche_enemigo.center = carril_derecho, -200
        else:
            ubicacion_coche_enemigo.center = carril_izquierdo, -200

    # Lógica de fin de juego
    if ubicacion_coche[0] == ubicacion_coche_enemigo[0] and ubicacion_coche_enemigo[1] > ubicacion_coche[1] - 250:
        print("¡JUEGO TERMINADO! ¡HAS PERDIDO!")
        break

    # Escuchar eventos
    for evento in pygame.event.get():
        if evento.type == QUIT:
            # Colapsar la aplicación
            corriendo = False
        if evento.type == KEYDOWN:
            # Mover el coche del jugador a la izquierda
            if evento.key in [K_a, K_LEFT]:
                ubicacion_coche = ubicacion_coche.move([-int(ancho_carretera / 2), 0])
            # Mover el coche del jugador a la derecha
            if evento.key in [K_d, K_RIGHT]:
                ubicacion_coche = ubicacion_coche.move([int(ancho_carretera / 2), 0])

    # Dibujar carretera
    pygame.draw.rect(
        pantalla,
        (50, 50, 50),
        (ancho / 2 - ancho_carretera / 2, 0, ancho_carretera, alto))
    # Dibujar línea central
    pygame.draw.rect(
        pantalla,
        (255, 240, 60),
        (ancho / 2 - ancho_marca_carretera / 2, 0, ancho_marca_carretera, alto))
    # Dibujar marca de carretera izquierda
    pygame.draw.rect(
        pantalla,
        (255, 255, 255),
        (ancho / 2 - ancho_carretera / 2 + ancho_marca_carretera * 2, 0, ancho_marca_carretera, alto))
    # Dibujar marca de carretera derecha
    pygame.draw.rect(
        pantalla,
        (255, 255, 255),
        (ancho / 2 + ancho_carretera / 2 - ancho_marca_carretera * 3, 0, ancho_marca_carretera, alto))

    # Colocar imágenes de coches en la pantalla
    pantalla.blit(coche, ubicacion_coche)
    pantalla.blit(coche_enemigo, ubicacion_coche_enemigo)
    # Aplicar cambios
    pygame.display.update()

# Colapsar la ventana de la aplicación
pygame.quit()

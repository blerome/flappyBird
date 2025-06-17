import pygame
import random
/*Dejar*/
# Inicializar PyGame
pygame.init()
pygame.joystick.init()

# Inicializar el módulo de sonido
pygame.mixer.init()

# Configuración de la pantalla
ANCHO, ALTO = 400, 600
VENTANA = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("Flappy Bird")

# Colores
BLANCO = (255, 255, 255)
ROJO = (255, 0, 0)

# Cargar imágenes y sonidos (debes tener los archivos en el directorio)
fondo = pygame.image.load("img/fondo.png") 
pajaro_imgs = [pygame.image.load("img/bird1.png"), 
               pygame.image.load("img/bird2.png"), 
               pygame.image.load("img/bird3.png")]
ground_img = pygame.image.load("img/ground.png")
tubo_img = pygame.image.load("img/tubo3.jpg")
restart_img = pygame.image.load("img/restart.png")
splash_img = pygame.image.load("img/splash.png").convert_alpha()

# Sonidos
sonido_die = pygame.mixer.Sound("sounds/die.mp3")
sonido_saltar = pygame.mixer.Sound("sounds/saltar.mp3")
sonido_hit = pygame.mixer.Sound("sounds/hit.mp3")
sonido_puntos = pygame.mixer.Sound("sounds/puntos.mp3")
pygame.mixer.music.load("sounds/music.mp3")
pygame.mixer.music.play(-1)

# Configuración del pájaro
pajaro_ancho, pajaro_alto = 40, 30
pajaro_x, pajaro_y = 50, ALTO // 2
velocidad_y = 5
gravedad = 0.9
salto = -6
pajaro_indice = 0

# Configuración de los tubos
ancho_tubo = 60
distancia_tubos = 200
velocidad_tubos = -10
altura_minima = 100
altura_maxima = ALTO - 200
nuevo_ancho_tubo = 70
nuevo_alto_tubo = 200

# Puntaje
puntaje = 0
fuente = pygame.font.SysFont(None, 36)

# Funciones
def esperar_a_tecla_o_boton(tecla=None, boton=None):
    joystick = pygame.joystick.Joystick(0) if pygame.joystick.get_count() > 0 else None
    if joystick:
        joystick.init()
    esperando = True
    while esperando:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                quit()
            if evento.type == pygame.KEYDOWN and tecla and evento.key == tecla:
                esperando = False
            if joystick and evento.type == pygame.JOYBUTTONDOWN and boton is not None:
                if joystick.get_button(boton):
                    esperando = False

def mostrar_pantalla_inicio():
    VENTANA.blit(pygame.transform.scale(fondo, (ANCHO, ALTO)), (0, 0))
    VENTANA.blit(splash_img, (ANCHO // 2 - splash_img.get_width() // 2, ALTO // 2 - splash_img.get_height() // 2))
    pygame.display.flip()
    esperar_a_tecla_o_boton(tecla=pygame.K_SPACE, boton=0)

def mostrar_game_over():
    fuente_game_over = pygame.font.SysFont(None, 48)
    texto_game_over = fuente_game_over.render("Game Over!", True, ROJO)
    VENTANA.blit(texto_game_over, (50, ALTO // 2 - 50))
    VENTANA.blit(restart_img, (ANCHO // 2 - restart_img.get_width() // 2, ALTO // 2))
    pygame.display.flip()
    esperar_a_tecla_o_boton(tecla=pygame.K_r, boton=7)
    reiniciar_juego()

def reiniciar_juego():
    global pajaro_y, velocidad_y, puntaje, tubos
    pajaro_y = ALTO // 2
    velocidad_y = 0
    puntaje = 0
    tubos = [generar_tubo()]
    mostrar_pantalla_inicio()
    juego()

def generar_tubo():
    altura = random.randint(altura_minima, altura_maxima)
    tubo_superior = pygame.Rect(ANCHO, 0, nuevo_ancho_tubo, altura)
    tubo_inferior = pygame.Rect(ANCHO, altura + distancia_tubos, nuevo_ancho_tubo, ALTO - altura - distancia_tubos)
    return tubo_superior, tubo_inferior

def mostrar_puntaje():
    texto = fuente.render(f"Puntaje: {puntaje}", True, (0, 0, 0))
    VENTANA.blit(texto, (10, 10))

def juego():
    global pajaro_y, velocidad_y, puntaje, tubos, pajaro_indice
    tubos = [generar_tubo()]
    reloj = pygame.time.Clock()
    ejecutando = True
    joystick = pygame.joystick.Joystick(0) if pygame.joystick.get_count() > 0 else None
    if joystick:
        joystick.init()

    while ejecutando:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                ejecutando = False
            if evento.type == pygame.KEYDOWN and evento.key == pygame.K_ESCAPE:
                ejecutando = False
            if evento.type == pygame.KEYDOWN and evento.key == pygame.K_SPACE:
                velocidad_y = salto
                sonido_saltar.play()
            if joystick and evento.type == pygame.JOYBUTTONDOWN:
                if joystick.get_button(0):  # Botón A
                    velocidad_y = salto
                    sonido_saltar.play()
                if joystick.get_button(6):  # Botón BACK
                    ejecutando = False

        velocidad_y += gravedad
        pajaro_y += velocidad_y
        pajaro_rect = pygame.Rect(pajaro_x, pajaro_y, pajaro_ancho, pajaro_alto)
        pajaro_indice = (pajaro_indice + 1) % len(pajaro_imgs)

        nuevos_tubos = []
        for tubo_superior, tubo_inferior in tubos:
            tubo_superior.x += velocidad_tubos
            tubo_inferior.x += velocidad_tubos
            if tubo_superior.right < 0:
                puntaje += 1
                sonido_puntos.play()
            else:
                nuevos_tubos.append((tubo_superior, tubo_inferior))

        if len(tubos) > 0 and tubos[-1][0].x < ANCHO // 2:
            nuevos_tubos.append(generar_tubo())
        tubos = nuevos_tubos

        for tubo_superior, tubo_inferior in tubos:
            if pajaro_rect.colliderect(tubo_superior) or pajaro_rect.colliderect(tubo_inferior):
                sonido_hit.play()
                mostrar_game_over()
                return

        if pajaro_y > ALTO or pajaro_y < 0:
            sonido_die.play()
            mostrar_game_over()
            return

        VENTANA.blit(pygame.transform.scale(fondo, (ANCHO, ALTO)), (0, 0))
        VENTANA.blit(pajaro_imgs[pajaro_indice], (pajaro_x, pajaro_y))
        for tubo_superior, tubo_inferior in tubos:
            tubo_img_sup = pygame.transform.scale(tubo_img, (nuevo_ancho_tubo, tubo_superior.height))
            tubo_img_inf = pygame.transform.scale(tubo_img, (nuevo_ancho_tubo, tubo_inferior.height))
            VENTANA.blit(tubo_img_sup, (tubo_superior.x, tubo_superior.y))
            VENTANA.blit(tubo_img_inf, (tubo_inferior.x, tubo_inferior.y))
        ground_redimensionado = pygame.transform.scale(ground_img, (ANCHO, 25))
        VENTANA.blit(ground_redimensionado, (0, ALTO - 25))
        mostrar_puntaje()
        pygame.display.flip()
        reloj.tick(30)

# Iniciar el juego
mostrar_pantalla_inicio()
juego()
pygame.quit()

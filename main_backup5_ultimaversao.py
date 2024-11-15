import pygame
import random

# Inicialização do Pygame
pygame.init()

# Definição das dimensões da tela
screen_width = 800
screen_height = 600
track_length = 10000  # Será ajustável no início do jogo
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Dragster')

# Cores
white = (255, 255, 255)
black = (0, 0, 0)
red = (255, 0, 0)
green = (0, 255, 0)
blue = (0, 0, 255)

# Classe Carro
class Car:
    def __init__(self, x, y, color, max_speeds, acceleration):
        self.x = x
        self.y = y
        self.color = color
        self.speed = 0
        self.gear = 1
        self.max_speeds = max_speeds
        self.acceleration = acceleration
        self.finished = False

    def draw(self, screen):
        # Chassis
        pygame.draw.rect(screen, self.color, [self.x - screen_scroll, self.y, 100, 20])
        # Traseira
        pygame.draw.rect(screen, white, [self.x - screen_scroll - 20, self.y - 10, 20, 40])
        # Dianteira
        pygame.draw.rect(screen, white, [self.x - screen_scroll + 80, self.y + 5, 20, 10])
        # Rodas traseiras
        pygame.draw.rect(screen, black, [self.x - screen_scroll - 30, self.y - 10, 10, 10])
        pygame.draw.rect(screen, black, [self.x - screen_scroll - 30, self.y + 20, 10, 10])
        # Rodas dianteiras
        pygame.draw.rect(screen, black, [self.x - screen_scroll + 90, self.y - 2, 10, 10])
        pygame.draw.rect(screen, black, [self.x - screen_scroll + 90, self.y + 12, 10, 10])

    def update(self):
        if self.gear > 0 and self.gear <= len(self.max_speeds):
            if self.speed > self.max_speeds[self.gear - 1]:
                self.speed = self.max_speeds[self.gear - 1]
            self.x += self.speed / 60  # Dividido por 60 para ajustar a velocidade à escala do jogo
            if self.x >= track_length:
                self.finished = True

# Função para exibir texto na tela
def display_text(text, font, color, x, y):
    screen_text = font.render(text, True, color)
    screen.blit(screen_text, [x, y])

# Tela de introdução
def game_intro():
    global track_length
    intro = True
    font = pygame.font.Font(None, 36)
    input_boxes = [pygame.Rect(300, 200, 140, 32)]
    colors = [white]
    active = [False]
    texts = ['']

    while intro:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                for i in range(1):
                    if input_boxes[i].collidepoint(event.pos):
                        active[i] = not active[i]
                    else:
                        active[i] = False
                colors = [blue if act else white for act in active]
            if event.type == pygame.KEYDOWN:
                for i in range(1):
                    if active[i]:
                        if event.key == pygame.K_RETURN:
                            active[i] = False
                            colors[i] = white
                        elif event.key == pygame.K_BACKSPACE:
                            texts[i] = texts[i][:-1]
                        else:
                            texts[i] += event.unicode

        screen.fill(black)
        display_text("Set Track Length (meters):", font, white, 150, 150)

        for i in range(1):
            txt_surface = font.render(texts[i], True, colors[i])
            width = max(200, txt_surface.get_width()+10)
            input_boxes[i].w = width
            screen.blit(txt_surface, (input_boxes[i].x+5, input_boxes[i].y+5))
            pygame.draw.rect(screen, colors[i], input_boxes[i], 2)

        pygame.draw.rect(screen, green, (350, 350, 100, 50))
        display_text("Start", font, black, 370, 360)

        pygame.display.flip()
        pygame.time.Clock().tick(30)

        if pygame.mouse.get_pressed()[0]:
            if 350 < pygame.mouse.get_pos()[0] < 450 and 350 < pygame.mouse.get_pos()[1] < 400:
                track_length = float(texts[0]) if texts[0] != '' else 10000
                max_speeds = [67, 134, 201, 268, 335, 400]
                acceleration = 5
                intro = False
                game_loop(max_speeds, acceleration)

# Tela de vitória
def victory_screen(winner):
    victory = True
    font = pygame.font.Font(None, 72)
    while victory:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        screen.fill(white)
        display_text(f'{winner} wins!', font, black, screen_width // 2 - 200, screen_height // 2 - 100)

        # Desenhar a bandeira quadriculada
        flag_size = 100
        for i in range(10):
            for j in range(10):
                color = black if (i + j) % 2 == 0 else white
                pygame.draw.rect(screen, color, (screen_width // 2 - flag_size // 2 + i * 10, screen_height // 2 + 50 + j * 10, 10, 10))

        pygame.display.flip()
        pygame.time.Clock().tick(30)

# Função principal do jogo
def game_loop(max_speeds, acceleration):
    global screen_scroll
    player_car = Car(50, screen_height - 150, red, max_speeds, acceleration)
    ai_car = Car(50, 150, black, max_speeds, 0.1)
    clock = pygame.time.Clock()
    running = True
    screen_scroll = 0
    font = pygame.font.Font(None, 36)

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    player_car.gear = 1
                elif event.key == pygame.K_2:
                    player_car.gear = 2
                elif event.key == pygame.K_3:
                    player_car.gear = 3
                elif event.key == pygame.K_4:
                    player_car.gear = 4
                elif event.key == pygame.K_5:
                    player_car.gear = 5
                elif event.key == pygame.K_6:
                    player_car.gear = 6

        # Controles do jogador
        keys = pygame.key.get_pressed()
        if keys[pygame.K_a]:
            player_car.speed += acceleration
            if player_car.speed > player_car.max_speeds[player_car.gear - 1]:
                player_car.speed = player_car.max_speeds[player_car.gear - 1]
        else:
            player_car.speed -= acceleration / 2
            if player_car.speed < 0:
                player_car.speed = 0

        # Lógica da IA (mais competitiva)
        if not ai_car.finished:
            if ai_car.speed < ai_car.max_speeds[ai_car.gear - 1]:
                ai_car.speed += ai_car.acceleration
            else:
                if ai_car.gear < 6 and ai_car.speed >= ai_car.max_speeds[ai_car.gear - 1] * 0.9:
                    ai_car.gear += 1
                ai_car.speed = min(ai_car.speed, ai_car.max_speeds[ai_car.gear - 1])

        # Atualização dos carros
        player_car.update()
        ai_car.update()

        # Scroll da tela baseado no carro do jogador
        screen_scroll = player_car.x - 100

        # Limpar a tela
        screen.fill(white)

        # Desenhar a pista e a linha divisória tracejada
        for i in range(0, screen_width, 40):
            pygame.draw.line(screen, black, (i, screen_height // 2), (i + 20, screen_height // 2), 2)

        # Desenhar a linha de chegada
        pygame.draw.line(screen, green, (track_length - screen_scroll, 0), (track_length - screen_scroll, screen_height), 5)

        # Desenhar os carros
        player_car.draw(screen)
        ai_car.draw(screen)

        # Exibir a marcha atual do jogador e a distância percorrida
        display_text(f'Gear: {player_car.gear}', font, black, 10, screen_height - 50)
        display_text(f'Distance: {int(player_car.x)} meters', font, black, 10, screen_height // 2 + 20)

        # Atualizar a tela
        pygame.display.flip()

        # Verificar se alguém venceu
        if player_car.finished:
            victory_screen("Player")



        # Verificar se alguém venceu
        if player_car.finished:
            victory_screen("Player")
            running = False
        if ai_car.finished:
            victory_screen("AI")
            running = False

        # Controlar a taxa de quadros
        clock.tick(60)

game_intro()
pygame.quit()

import pygame
import random

pygame.init()

screen_width = 800
screen_height = 600
track_length = 10000
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Dragster')

white = (255, 255, 255)
black = (0, 0, 0)
red = (255, 0, 0)
green = (0, 255, 0)
blue = (0, 0, 255)

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
        self.rpm = 0
        self.optimal_shift_points = [0.85, 0.88, 0.9, 0.92, 0.95]
        self.temperature = 60
        self.overheating = False

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, [self.x - screen_scroll, self.y, 100, 20])
        pygame.draw.rect(screen, white, [self.x - screen_scroll - 20, self.y - 10, 20, 40])
        pygame.draw.rect(screen, white, [self.x - screen_scroll + 80, self.y + 5, 20, 10])
        pygame.draw.rect(screen, black, [self.x - screen_scroll - 30, self.y - 10, 10, 10])
        pygame.draw.rect(screen, black, [self.x - screen_scroll - 30, self.y + 20, 10, 10])
        pygame.draw.rect(screen, black, [self.x - screen_scroll + 90, self.y - 2, 10, 10])
        pygame.draw.rect(screen, black, [self.x - screen_scroll + 90, self.y + 12, 10, 10])

    def update(self, is_ai=False, accelerating=False):
        if is_ai:
            self.ai_control()

        if self.gear > 0 and self.gear <= len(self.max_speeds):
            current_max_speed = self.max_speeds[self.gear - 1]

            if accelerating:
                self.temperature += 0.5 * (self.speed / current_max_speed)
            else:
                self.temperature = max(60, self.temperature - 0.3)

            if self.temperature > 100:
                self.overheating = True
                current_max_speed *= 0.7
                self.acceleration *= 0.8
            elif self.temperature < 90:
                self.overheating = False

            if self.speed > current_max_speed:
                self.speed = current_max_speed

            self.rpm = (self.speed / current_max_speed) * 100
            effective_speed = self.speed * (1 - (self.speed / (current_max_speed * 1.2)))
            self.x += effective_speed / 60

            if self.x >= track_length:
                self.finished = True

    def ai_control(self):
        current_max_speed = self.max_speeds[self.gear - 1]
        optimal_shift_point = self.optimal_shift_points[min(self.gear - 1, len(self.optimal_shift_points) - 1)]

        should_accelerate = True
        if self.temperature > 95:
            should_accelerate = random.random() > 0.3

        if should_accelerate and self.speed < current_max_speed:
            acceleration_factor = 1.5 if self.speed < current_max_speed * 0.3 else 1.0
            self.speed += self.acceleration * acceleration_factor
        else:
            self.speed = max(0, self.speed - self.acceleration / 2)

        if self.gear < 6 and (self.speed / current_max_speed) >= optimal_shift_point:
            next_gear_speed = self.max_speeds[self.gear] if self.gear < len(self.max_speeds) else float('inf')
            if self.speed > current_max_speed * 0.9 and self.speed < next_gear_speed:
                self.gear += 1
                self.speed *= 0.95

def display_text(text, font, color, x, y):
    screen_text = font.render(text, True, color)
    screen.blit(screen_text, [x, y])

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

        flag_size = 100
        for i in range(10):
            for j in range(10):
                color = black if (i + j) % 2 == 0 else white
                pygame.draw.rect(screen, color, (screen_width // 2 - flag_size // 2 + i * 10, screen_height // 2 + 50 + j * 10, 10, 10))

        pygame.display.flip()
        pygame.time.Clock().tick(30)

def game_loop(max_speeds, acceleration):
    global screen_scroll
    player_car = Car(50, screen_height - 150, red, max_speeds, acceleration)
    ai_car = Car(50, 150, black, max_speeds, acceleration * 1.1)
    clock = pygame.time.Clock()
    running = True
    screen_scroll = 0
    font = pygame.font.Font(None, 36)

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key in [pygame.K_1, pygame.K_2, pygame.K_3, pygame.K_4, pygame.K_5, pygame.K_6]:
                    player_car.gear = int(event.unicode)

        keys = pygame.key.get_pressed()
        accelerating = keys[pygame.K_a]
        if accelerating:
            player_car.speed += acceleration
        else:
            player_car.speed = max(0, player_car.speed - acceleration / 2)

        player_car.update(accelerating=accelerating)
        ai_car.update(is_ai=True)

        screen_scroll = player_car.x - 100
        screen.fill(white)

        for i in range(0, screen_width, 40):
            pygame.draw.line(screen, black, (i, screen_height // 2), (i + 20, screen_height // 2), 2)

        pygame.draw.line(screen, green, (track_length - screen_scroll, 0), 
                        (track_length - screen_scroll, screen_height), 5)

        player_car.draw(screen)
        ai_car.draw(screen)

        temp_color = red if player_car.temperature > 90 else black
        display_text(f'Gear: {player_car.gear}', font, black, 10, screen_height - 50)
        display_text(f'Speed: {int(player_car.speed)} km/h', font, black, 10, screen_height - 80)
        display_text(f'RPM: {int(player_car.rpm)}%', font, black, 10, screen_height - 110)
        display_text(f'Temp: {int(player_car.temperature)}°C', font, temp_color, 10, screen_height - 140)
        display_text(f'Distance: {int(player_car.x)} meters', font, black, 10, screen_height // 2 + 20)

        if player_car.overheating:
            display_text('ENGINE OVERHEATING!', font, red, screen_width // 2 - 100, 50)

        pygame.display.flip()

        if player_car.finished:
            victory_screen("Player")
            running = False
        if ai_car.finished:
            victory_screen("AI")
            running = False

        clock.tick(60)

if __name__ == "__main__":
    game_intro()
    pygame.quit()


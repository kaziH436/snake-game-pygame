import pygame
import time
import random
from enum import Enum

# Enums for direction
class Direction(Enum):
    UP = 0
    DOWN = 1
    LEFT = 2
    RIGHT = 3

# Food class
class Food:
    def __init__(self, block_size, bounds, color=(0, 255, 0)):
        self.block_size = block_size
        self.bounds = bounds
        self.color = color
        self.respawn()

    def draw(self, game, window):
        game.draw.ellipse(window, self.color, (self.x, self.y, self.block_size, self.block_size))

    def respawn(self):
        blocks_in_x = self.bounds[0] // self.block_size
        blocks_in_y = self.bounds[1] // self.block_size
        self.x = random.randint(0, blocks_in_x - 1) * self.block_size
        self.y = random.randint(0, blocks_in_y - 1) * self.block_size

# Snake class
class Snake:
    def __init__(self, block_size, bounds):
        self.block_size = block_size
        self.bounds = bounds
        self.respawn()

    def respawn(self):
        self.length = 3
        self.body = [(20, 20), (20, 40), (20, 60)]
        self.direction = Direction.DOWN
        self.color = (0, 255, 255)

    def draw(self, game, window):
        for i, segment in enumerate(self.body):
            radius = self.block_size // 2 + (i % 2) * 2 - 1
            game.draw.ellipse(window, self.color, (segment[0], segment[1], radius * 2, radius * 2))

    def move(self):
        curr_head = self.body[-1]
        if self.direction == Direction.DOWN:
            next_head = (curr_head[0], (curr_head[1] + self.block_size) % self.bounds[1])
        elif self.direction == Direction.UP:
            next_head = (curr_head[0], (curr_head[1] - self.block_size) % self.bounds[1])
        elif self.direction == Direction.RIGHT:
            next_head = ((curr_head[0] + self.block_size) % self.bounds[0], curr_head[1])
        elif self.direction == Direction.LEFT:
            next_head = ((curr_head[0] - self.block_size) % self.bounds[0], curr_head[1])

        next_head = (next_head[0] % self.bounds[0], next_head[1] % self.bounds[1])

        self.body.append(next_head)
        if self.length < len(self.body):
            self.body.pop(0)

    def steer(self, direction):
        if (self.direction == Direction.UP and direction != Direction.DOWN) or \
           (self.direction == Direction.DOWN and direction != Direction.UP) or \
           (self.direction == Direction.LEFT and direction != Direction.RIGHT) or \
           (self.direction == Direction.RIGHT and direction != Direction.LEFT):
            self.direction = direction

    def eat(self):
        self.length += 1

    def shrink(self):
        if self.length > 3:
            self.body.pop(0)
            self.length -= 1

    def check_for_food(self, food):
        head = self.body[-1]
        return head[0] == food.x and head[1] == food.y

    def check_tail_collision(self):
        head = self.body[-1]
        return head in self.body[:-1]

# Initialize Pygame
pygame.init()
bounds = (720, 480)
window = pygame.display.set_mode(bounds)
pygame.display.set_caption("Snake Game")

block_size = 20
snake = Snake(block_size, bounds)
foods = [Food(block_size, bounds, color=(0, 255, 0))]
red_food = Food(block_size, bounds, color=(255, 0, 0))
fruit_spawn_time = time.time()
score = 0

# Fonts and colors
font = pygame.font.SysFont('Comic Sans MS', 30)
button_font = pygame.font.SysFont('Arial', 24)

def display_score(score, window):
    text = font.render(f"Score: {score}", True, (255, 255, 255))
    window.blit(text, (10, 10))

def game_over():
    text = font.render("Game Over", True, (255, 0, 0))
    window.blit(text, (bounds[0] // 2 - 100, bounds[1] // 2 - 50))
    pygame.display.update()
    pygame.time.delay(2000)

def draw_button(window, text, rect, font, color, hover=False):
    if hover:
        color = (255, 100, 100)
    pygame.draw.rect(window, color, rect, border_radius=15)
    text_surface = font.render(text, True, (255, 255, 255))
    text_rect = text_surface.get_rect(center=rect.center)
    window.blit(text_surface, text_rect)

def draw_gradient_background(window):
    # Gradient from dark purple to light purple
    for i in range(bounds[1]):
        # Interpolate between dark purple (100, 0, 255) and light purple (255, 182, 193)
        r = int(100 + (255 - 100) * (i / bounds[1]))
        g = int(0 + (182 - 0) * (i / bounds[1]))
        b = int(255 + (193 - 255) * (i / bounds[1]))
        pygame.draw.line(window, (r, g, b), (0, i), (bounds[0], i))

def main_menu():
    draw_gradient_background(window)
    title_text = font.render("Welcome to Snake Game", True, (255, 255, 255))
    window.blit(title_text, (bounds[0] // 2 - 150, bounds[1] // 2 - 150))
    
    play_button_rect = pygame.Rect(bounds[0] // 2 - 100, bounds[1] // 2 - 50, 200, 50)
    quit_button_rect = pygame.Rect(bounds[0] // 2 - 100, bounds[1] // 2 + 50, 200, 50)
    
    draw_button(window, "Play", play_button_rect, button_font, (0, 128, 0))
    draw_button(window, "Quit", quit_button_rect, button_font, (128, 0, 0))
    
    pygame.display.update()
    return play_button_rect, quit_button_rect

def rules_menu():
    draw_gradient_background(window)
    rules_text = font.render("Rules: Use arrow keys to control the snake", True, (255, 255, 255))
    rules_rect = rules_text.get_rect(center=(bounds[0] // 2, bounds[1] // 2 - 100))  # Adjusted to center text
    window.blit(rules_text, rules_rect)
    
    # Adjusting button positions to move them slightly up
    play_button_rect = pygame.Rect(bounds[0] // 2 - 100, bounds[1] // 2, 200, 50)  # Moved up
    back_button_rect = pygame.Rect(bounds[0] // 2 - 100, bounds[1] // 2 + 100, 200, 50)  # Moved up
    
    draw_button(window, "Play Game", play_button_rect, button_font, (0, 128, 0))
    draw_button(window, "Back to Menu", back_button_rect, button_font, (128, 128, 0))
    
    pygame.display.update()
    return play_button_rect, back_button_rect

run = True
in_menu = True
in_rules = False
paused = False

while run:
    pygame.time.delay(100)

    if in_menu:
        play_button_rect, quit_button_rect = main_menu()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:  # Left mouse click
                if play_button_rect.collidepoint(event.pos):
                    in_menu = False
                    in_rules = True
                elif quit_button_rect.collidepoint(event.pos):
                    run = False

    elif in_rules:
        play_button_rect, back_button_rect = rules_menu()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:  # Left mouse click
                if play_button_rect.collidepoint(event.pos):
                    in_rules = False
                elif back_button_rect.collidepoint(event.pos):
                    in_rules = False
                    in_menu = True

    else:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    snake.steer(Direction.LEFT)
                elif event.key == pygame.K_RIGHT:
                    snake.steer(Direction.RIGHT)
                elif event.key == pygame.K_UP:
                    snake.steer(Direction.UP)
                elif event.key == pygame.K_DOWN:
                    snake.steer(Direction.DOWN)
                elif event.key == pygame.K_p:  # Pause game
                                    paused = not paused

        if paused:
            pause_text = font.render("Game Paused. Press P to Resume", True, (255, 255, 255))
            window.blit(pause_text, (bounds[0] // 2 - 200, bounds[1] // 2 - 20))
            pygame.display.update()
            continue

        if time.time() - fruit_spawn_time >= 5:
            foods.append(Food(block_size, bounds))
            fruit_spawn_time = time.time()

        snake.move()

        for food in foods:
            if snake.check_for_food(food):
                snake.eat()
                foods.remove(food)
                score += 1

        if snake.check_for_food(red_food):
            snake.shrink()
            red_food.respawn()

        if snake.check_tail_collision():
            game_over()
            snake.respawn()
            score = 0
            foods.clear()

        draw_gradient_background(window)
        display_score(score, window)
        for food in foods:
            food.draw(pygame, window)
        red_food.draw(pygame, window)
        snake.draw(pygame, window)
        pygame.display.update()

pygame.quit()


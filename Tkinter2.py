import pygame
import random

pygame.init()

# Ukuran layar
WIDTH = 600
HEIGHT = 500

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Colorful Block Breaker")

clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 25)

# Warna
WHITE = (255, 255, 255)
CYAN = (0, 255, 255)
YELLOW = (255, 255, 0)
RED = (255, 50, 100)
PURPLE = (180, 0, 255)
GREEN = (0, 255, 100)
ORANGE = (255, 140, 0)
BLUE = (0, 120, 255)
PINK = (255, 50, 200)

COLORS = [RED, PURPLE, GREEN, ORANGE, BLUE, PINK, YELLOW]


# Class Pemain
class Striker:
    def __init__(self):
        self.rect = pygame.Rect(250, 450, 100, 15)
        self.speed = 7

    def update(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_LEFT]:
            self.rect.x -= self.speed

        if keys[pygame.K_RIGHT]:
            self.rect.x += self.speed

        self.rect.x = max(0, min(self.rect.x, WIDTH - self.rect.width))

    def display(self):
        pygame.draw.rect(screen, CYAN, self.rect, border_radius=8)


# Class Bola
class Ball:
    def __init__(self):
        self.rect = pygame.Rect(290, 300, 15, 15)
        self.speed_x = 4
        self.speed_y = -4

    def update(self):
        self.rect.x += self.speed_x
        self.rect.y += self.speed_y

        if self.rect.left <= 0 or self.rect.right >= WIDTH:
            self.speed_x *= -1

        if self.rect.top <= 0:
            self.speed_y *= -1

    def display(self):
        pygame.draw.ellipse(screen, YELLOW, self.rect)


# Class Balok
class Block:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, 50, 20)
        self.color = random.choice(COLORS)

        # Balok merah membutuhkan 2 pukulan
        if self.color == RED:
            self.health = 2
        else:
            self.health = 1

        self.active = True

    def hit(self):
        self.health -= 1

        if self.health <= 0:
            self.active = False

    def display(self):
        if self.active:
            pygame.draw.rect(
                screen, self.color, self.rect,
                border_radius=5
            )


# Membuat objek
player = Striker()
ball = Ball()

blocks = []

for x in range(10, WIDTH, 60):
    for y in range(30, 130, 30):
        blocks.append(Block(x, y))


# Variabel permainan
score = 0
lives = 3
running = True
game_over = False


# Game Loop
while running:

    screen.fill((20, 15, 50))

    # Event
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    if not game_over:

        player.update()
        ball.update()

        # Tabrakan dengan pemain
        if ball.rect.colliderect(player.rect):
            ball.speed_y = -abs(ball.speed_y)

        # Tabrakan dengan balok
        for block in blocks:
            if block.active and ball.rect.colliderect(block.rect):

                block.hit()
                ball.speed_y *= -1

                # Skor bertambah jika balok hancur
                if not block.active:
                    score += 10

                break

        # Bola jatuh
        if ball.rect.bottom >= HEIGHT:
            lives -= 1
            ball.rect.center = (300, 300)
            ball.speed_y = -4
            ball.speed_x = 4

        # Menampilkan objek
        player.display()
        ball.display()

        for block in blocks:
            block.display()

        # Skor dan nyawa
        score_text = font.render(
            "Score: " + str(score), True, WHITE
        )

        lives_text = font.render(
            "Lives: " + str(lives), True, WHITE
        )

        screen.blit(score_text, (10, 470))
        screen.blit(lives_text, (120, 470))

        # Kondisi menang atau kalah
        if all(not block.active for block in blocks):
            game_over = True

        if lives <= 0:
            game_over = True

    else:
        text = font.render("GAME OVER!", True, RED)
        screen.blit(text, (240, 230))

        result = font.render(
            "Final Score: " + str(score), True, YELLOW
        )

        screen.blit(result, (230, 270))

    pygame.display.update()
    clock.tick(30)

pygame.quit()
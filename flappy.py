import pygame
import random

# Initialize Pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 400, 600
PIPE_WIDTH = 70
GRAVITY = 0.25
FLAP_STRENGTH = -7
FPS = 60
FONT = pygame.font.Font(None, 36)

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Game variables
score = 0
game_over = False

# Create the screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Flappy Bird")

# Load images
bird_image = pygame.image.load('bird.png').convert_alpha()
pipe_image = pygame.image.load('pipe.png').convert_alpha()

# Resize images (if needed)
bird_image = pygame.transform.scale(bird_image, (50, 50))
pipe_image = pygame.transform.scale(pipe_image, (PIPE_WIDTH, HEIGHT))

# Create Bird class
class Bird:
    def __init__(self):
        self.x = 100
        self.y = HEIGHT // 2
        self.velocity = 0

    def flap(self):
        self.velocity = FLAP_STRENGTH

    def update(self):
        self.velocity += GRAVITY
        self.y += self.velocity

    def draw(self):
        screen.blit(bird_image, (self.x, self.y))

# Create Pipe class
class Pipe:
    def __init__(self, x):
        self.x = x
        self.height = random.randint(100, HEIGHT - 200)

    def move(self):
        self.x -= 3

    def off_screen(self):
        return self.x < -PIPE_WIDTH

    def draw(self):
        screen.blit(pipe_image, (self.x, 0), (0, 0, PIPE_WIDTH, self.height))
        screen.blit(pipe_image, (self.x, self.height + 200), (0, self.height + 200, PIPE_WIDTH, HEIGHT - self.height - 200))

# Create bird and pipes
bird = Bird()
pipes = [Pipe(WIDTH + i * 200) for i in range(3)]

# Game loop
clock = pygame.time.Clock()
running = True
while running:
    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and not game_over:
                bird.flap()
            if event.key == pygame.K_SPACE and game_over:
                # Restart the game
                bird = Bird()
                pipes = [Pipe(WIDTH + i * 200) for i in range(3)]
                score = 0
                game_over = False

    # Update
    if not game_over:
        bird.update()
        for pipe in pipes:
            pipe.move()
            if pipe.x < bird.x < pipe.x + PIPE_WIDTH:
                if pipe.height > bird.y or bird.y > pipe.height + 200:
                    game_over = True
            if pipe.off_screen():
                pipes.remove(pipe)
                pipes.append(Pipe(WIDTH))
        if 0 < pipes[0].x < bird.x:
            score += 1

    # Draw
    screen.fill(BLACK)
    bird.draw()
    for pipe in pipes:
        pipe.draw()
    score_text = FONT.render(f'Score: {score}', True, WHITE)
    screen.blit(score_text, (10, 10))
    if game_over:
        game_over_text = FONT.render('Game Over! Press SPACE to play again.', True, WHITE)
        screen.blit(game_over_text, (WIDTH//2 - 200, HEIGHT//2 - 18))

    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()

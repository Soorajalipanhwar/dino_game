import pygame
import random

# Initialize pygame
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 800, 400
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Dino Game")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)

# Game variables
clock = pygame.time.Clock()
FPS = 60
GRAVITY = 0.6
ground_level = HEIGHT - 50

# Load assets
dino_image = pygame.image.load("dino.png")
cactus_image = pygame.image.load("cactus.png")
dino_image = pygame.transform.scale(dino_image, (50, 50))
cactus_image = pygame.transform.scale(cactus_image, (50, 50))

# Dino class
class Dino:
    def __init__(self):
        self.image = dino_image
        self.x = 100
        self.y = ground_level - self.image.get_height()
        self.width = self.image.get_width()
        self.height = self.image.get_height()
        self.is_jumping = False
        self.jump_speed = -15
        self.y_velocity = 0

    def update(self):
        if self.is_jumping:
            self.y_velocity += GRAVITY
            self.y += self.y_velocity
            if self.y >= ground_level - self.height:
                self.y = ground_level - self.height
                self.is_jumping = False

    def jump(self):
        if not self.is_jumping:
            self.is_jumping = True
            self.y_velocity = self.jump_speed

    def draw(self):
        SCREEN.blit(self.image, (self.x, self.y))

# Obstacle class
class Obstacle:
    def __init__(self):
        self.image = cactus_image
        self.x = WIDTH
        self.y = ground_level - self.image.get_height()
        self.width = self.image.get_width()
        self.height = self.image.get_height()

    def update(self, speed):
        self.x -= speed

    def draw(self):
        SCREEN.blit(self.image, (self.x, self.y))

# Game loop with replay option
def game_loop():
    dino = Dino()
    obstacles = []
    spawn_timer = 0
    speed = 5
    score = 0
    running = True

    while running:
        SCREEN.fill(WHITE)
        pygame.draw.rect(SCREEN, GRAY, (0, ground_level, WIDTH, 50))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                dino.jump()

        # Update dino
        dino.update()

        # Spawn obstacles
        spawn_timer += 1
        if spawn_timer > 100:
            obstacles.append(Obstacle())
            spawn_timer = 0

        # Update obstacles
        for obstacle in obstacles[:]:
            obstacle.update(speed)
            if obstacle.x + obstacle.width < 0:
                obstacles.remove(obstacle)
                score += 1

        # Check collisions
        for obstacle in obstacles:
            if (
                dino.x < obstacle.x + obstacle.width and
                dino.x + dino.width > obstacle.x and
                dino.y < obstacle.y + obstacle.height and
                dino.y + dino.height > obstacle.y
            ):
                return game_over_screen(score)

        # Draw everything
        dino.draw()
        for obstacle in obstacles:
            obstacle.draw()

        # Display score
        font = pygame.font.Font(None, 36)
        score_text = font.render(f"Score: {score}", True, BLACK)
        SCREEN.blit(score_text, (10, 10))

        pygame.display.flip()
        clock.tick(FPS)

# Game Over screen
def game_over_screen(score):
    while True:
        SCREEN.fill(WHITE)
        font = pygame.font.Font(None, 48)
        game_over_text = font.render("Game Over", True, BLACK)
        score_text = font.render(f"Your Score: {score}", True, BLACK)
        instructions_text = font.render("Press Enter to Play Again or Space to Exit", True, BLACK)

        SCREEN.blit(game_over_text, (WIDTH // 2 - game_over_text.get_width() // 2, HEIGHT // 3))
        SCREEN.blit(score_text, (WIDTH // 2 - score_text.get_width() // 2, HEIGHT // 3 + 50))
        SCREEN.blit(instructions_text, (WIDTH // 2 - instructions_text.get_width() // 2, HEIGHT // 3 + 100))

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:  # Enter key
                    return True
                if event.key == pygame.K_SPACE:  # Space key
                    return False

# Main loop
def main():
    while game_loop():
        pass
    pygame.quit()

if __name__ == "__main__":
    main()

import pygame
import random
import sys
import os

# Function to get the correct path for assets
def resource_path(relative_path):
    """Get absolute path to resource, works for dev and for PyInstaller."""
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

# Initialize Pygame
pygame.init()
pygame.mixer.init()

# Get the display surface
screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)

# Constants
WIDTH, HEIGHT = screen.get_size()
SENSITIVITY = 0.23
TARGET_RADIUS = 100
BG_COLOR = (0, 0, 0)
CURSOR_HIDDEN = True
FPS_FONT_SIZE = 24
SCORE_FONT_SIZE = 36

# Load sound using resource_path
hit_sound = pygame.mixer.Sound(resource_path("unn.mp3"))
hit_sound.set_volume(0.5)

# Load custom target image using resource_path
target_image = pygame.image.load(resource_path("unnayan.png"))
target_image = pygame.transform.scale(target_image, (2 * TARGET_RADIUS, 2 * TARGET_RADIUS))

# Game variables
score = 0
TARGET_SPEED = 2.4  # Adjust this value to control the speed

def spawn_target():
    x = random.randint(TARGET_RADIUS, WIDTH - TARGET_RADIUS)
    y = random.randint(TARGET_RADIUS, HEIGHT - TARGET_RADIUS)
    velocity = pygame.Vector2(random.uniform(-1, 1), random.uniform(-1, 1)) * TARGET_SPEED
    return {"position": pygame.Vector2(x, y), "velocity": velocity}

# Create fonts for displaying score and FPS
score_font = pygame.font.Font(None, SCORE_FONT_SIZE)
fps_font = pygame.font.Font(None, FPS_FONT_SIZE)

# Game loop
running = True
clock = pygame.time.Clock()
targets = []

fps = 200
delta_time = 1 / fps

crosshair = pygame.Surface((10, 10), pygame.SRCALPHA)
pygame.draw.line(crosshair, (255, 2, 2), (5, 0), (5, 10), 2)
pygame.draw.line(crosshair, (255, 2, 2), (0, 5), (10, 5), 2)

pygame.mouse.set_visible(not CURSOR_HIDDEN)
pygame.mouse.set_pos(WIDTH // 2, HEIGHT // 2)

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            for target in targets:
                if target["position"].distance_to(pygame.Vector2(event.pos)) <= TARGET_RADIUS:
                    targets.remove(target)
                    score += 1
                    hit_sound.play()

    # Move targets
    for target in targets:
        target["position"] += target["velocity"]

        # Bounce off the edges
        if target["position"].x < TARGET_RADIUS or target["position"].x > WIDTH - TARGET_RADIUS:
            target["velocity"].x *= -1
        if target["position"].y < TARGET_RADIUS or target["position"].y > HEIGHT - TARGET_RADIUS:
            target["velocity"].y *= -1

    if len(targets) < 4:
        targets.append(spawn_target())

    screen.fill(BG_COLOR)
    for target in targets:
        screen.blit(target_image, (target["position"].x - TARGET_RADIUS, target["position"].y - TARGET_RADIUS))

    mouse_delta = pygame.mouse.get_rel()
    crosshair_pos = (pygame.mouse.get_pos()[0] - 10 + mouse_delta[0] * SENSITIVITY,
                     pygame.mouse.get_pos()[1] - 10 + mouse_delta[1] * SENSITIVITY)

    screen.blit(crosshair, crosshair_pos)

    score_text = score_font.render("Score: " + str(score), True, (255, 255, 255))
    screen.blit(score_text, (10, 10))

    fps_text = fps_font.render("FPS: " + str(int(clock.get_fps())), True, (255, 255, 255))
    screen.blit(fps_text, (WIDTH - 100, 10))

    pygame.display.update()
    delta_time = clock.tick(fps) / 1000.0

pygame.quit()

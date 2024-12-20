import pygame
import random

# Initialize Pygame
pygame.init()
pygame.mixer.init()

# # Define your desired screen dimensions
# SCREEN_WIDTH = 1200
# SCREEN_HEIGHT = 700

# Get the display surface
# screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN) 

# Constants
WIDTH, HEIGHT = screen.get_size()
SENSITIVITY = 0.23
TARGET_RADIUS =  100 # Increase the target radius to accommodate your custom images
BG_COLOR = (0, 0, 0)
CURSOR_HIDDEN = True
FPS_FONT_SIZE = 24
SCORE_FONT_SIZE = 36


hit_sound = pygame.mixer.Sound("unn.mp3")
hit_sound.set_volume(0.5)

# Load your custom target image
target_image = pygame.image.load("unnayan.png")
# Scale the image to fit within the target radius
target_image = pygame.transform.scale(target_image, (2 * TARGET_RADIUS, 2 * TARGET_RADIUS))

# Game variables
score = 0

def spawn_target():
    x = random.randint(TARGET_RADIUS, WIDTH - TARGET_RADIUS)
    y = random.randint(TARGET_RADIUS, HEIGHT - TARGET_RADIUS)
    return pygame.Vector2(x, y)

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
pygame.draw.line(crosshair, (255, 2, 2 ), (5, 0), (5, 10), 2)
pygame.draw.line(crosshair, (255, 2, 2 ), (0, 5), (10, 5), 2)
# crosshair = pygame.Surface((20, 20), pygame.SRCALPHA)
# pygame.draw.line(crosshair, (255, 255, 255), (10, 0), (10, 20), 2)
# pygame.draw.line(crosshair, (255, 255, 255), (0, 10), (20, 10), 2)

pygame.mouse.set_visible(not CURSOR_HIDDEN)
pygame.mouse.set_pos(WIDTH // 2, HEIGHT // 2)

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            for target in targets:
                if target.distance_to(pygame.Vector2(event.pos)) <= TARGET_RADIUS:
                    targets.remove(target)
                    score += 1
                    hit_sound.play()

    if len(targets) < 20:
        targets.append(spawn_target())

    screen.fill(BG_COLOR)
    for target in targets:
        # Draw the custom image on the target position
        screen.blit(target_image, (target.x - TARGET_RADIUS, target.y - TARGET_RADIUS))

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

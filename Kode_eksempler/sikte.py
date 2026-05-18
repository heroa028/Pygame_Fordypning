import pygame
import sys
import math

pygame.init()

# Screen
WIDTH, HEIGHT = 600, 400
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Shoot with Mouse")
clock = pygame.time.Clock()

# Colors
BG = (30, 30, 30)
PLAYER_COLOR = (0, 200, 255)
BULLET_COLOR = (255, 50, 50)

# Player
player_pos = [WIDTH // 2, HEIGHT // 2]
player_radius = 20

# Bullets list
bullets = []
bullet_speed = 8
bullet_radius = 5

# Game loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        # Shoot bullet on mouse click
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # Left click
                mouse_x, mouse_y = event.pos
                dx = mouse_x - player_pos[0]
                dy = mouse_y - player_pos[1]
                distance = math.hypot(dx, dy)
                if distance == 0:
                    distance = 1
                # Normalize direction
                dx /= distance
                dy /= distance
                bullets.append({"pos": player_pos[:], "dir": (dx, dy)})

    # Move bullets
    for bullet in bullets[:]:
        bullet["pos"][0] += bullet["dir"][0] * bullet_speed
        bullet["pos"][1] += bullet["dir"][1] * bullet_speed

        # Remove bullets off-screen
        if (bullet["pos"][0] < 0 or bullet["pos"][0] > WIDTH or
            bullet["pos"][1] < 0 or bullet["pos"][1] > HEIGHT):
            bullets.remove(bullet)

    # Draw
    screen.fill(BG)

    # Player
    pygame.draw.circle(screen, PLAYER_COLOR, player_pos, player_radius)

    # Bullets
    for bullet in bullets:
        pygame.draw.circle(screen, BULLET_COLOR,
                           (int(bullet["pos"][0]), int(bullet["pos"][1])), bullet_radius)

    pygame.display.flip()
    clock.tick(60)

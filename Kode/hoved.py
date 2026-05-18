import pygame
import sys
import math


pygame.init()

# Screen
WIDTH, HEIGHT = 1440, 920
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Shoot with Mouse og beveg wasd")
clock = pygame.time.Clock()

# Colors
BG = (30, 30, 30)
PLAYER_COLOR = (0, 200, 255)
BULLET_COLOR = (255, 50, 50)
BUTTON_COLOR = (70, 130, 180)
HOVER_COLOR = (100, 170, 220)
TEXT_COLOR = (255, 255, 255)

# Font
font = pygame.font.SysFont(None, 36)



# Player
player_pos = [WIDTH // 2, HEIGHT // 2]
player_radius = 20
speed = 5
player_x = WIDTH // 2
player_y = HEIGHT // 2

player = pygame.Rect(WIDTH // 2, HEIGHT // 2, player_radius * 2 , player_radius * 2)

# Bullets list
bullets = []
bullet_speed = 8
bullet_radius = 4

# Variables
Meny = True

# Button class
class Button:
    def __init__(self, text, x, y, w, h):
        self.text = text
        self.rect = pygame.Rect(x, y, w, h)

    def draw(self, surface):
        color = HOVER_COLOR if self.rect.collidepoint(pygame.mouse.get_pos()) else BUTTON_COLOR
        pygame.draw.rect(surface, color, self.rect)
        pygame.draw.rect(surface, (0, 0, 0), self.rect, 2)

        text_surf = font.render(self.text, True, TEXT_COLOR)
        text_rect = text_surf.get_rect(center=self.rect.center)
        surface.blit(text_surf, text_rect)

    def clicked(self, event):
        return (
            event.type == pygame.MOUSEBUTTONDOWN
            and event.button == 1
            and self.rect.collidepoint(event.pos)
        )

# Create buttons
buttons = [
    Button("Play", 200, 120, 200, 50),
    Button("Options", 200, 190, 200, 50),
    Button("Quit", 200, 260, 200, 50)
]

# Game loop
while True:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if Meny == True:
            for button in buttons:
                if button.clicked(event):
                    print(f"{button.text} clicked!")

                    if button.text == "Quit":
                        pygame.quit()
                        sys.exit()
                    if button.text == "Play":
                        Meny = False
    if Meny == False:    
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


    # Keybinds
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w]:
                player_y -= speed
        if keys[pygame.K_s]:
                player_y += speed
        if keys[pygame.K_d]:
                player_x += speed
        if keys[pygame.K_a]:
                player_x -= speed
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
    if Meny:
        for button in buttons:
            button.draw(screen)

    # Player
    if Meny == False:
        pygame.draw.circle(screen, PLAYER_COLOR, player_pos, player_radius)

     # Keep square on screen
    player_x = max(0, min(WIDTH - player_radius, player_x))
    player_y = max(0, min(HEIGHT - player_radius, player_y))
    player_pos[0] = player_x
    player_pos[1] = player_y

    

    # Bullets
    for bullet in bullets:
        pygame.draw.circle(screen, BULLET_COLOR,
                           (int(bullet["pos"][0]), int(bullet["pos"][1])), bullet_radius)

    pygame.display.flip()
    clock.tick(60)
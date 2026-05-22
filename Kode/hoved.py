#Dette importerer og starter alle pygame systemer som, lys display, input etc. 
import pygame
import sys
import math
import random

#Loader inn "bibliotekene"
pygame.init()

# Screen
#Disse lager wdindowet på den satte resolusjonen, og setter caption og clock setter fpsen. 
WIDTH, HEIGHT = 1440, 920
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Leo må rapes")
clock = pygame.time.Clock()

# Colors¨
#Lagrer rgb verdier til forskjellige ting som skal ha farger
BG = (30, 30, 30)
PLAYER_COLOR = (0, 200, 255)
BULLET_COLOR = (255, 50, 50)
BUTTON_COLOR = (128, 0, 128)
HOVER_COLOR = (100, 170, 220)
TEXT_COLOR = (255, 255, 255)

# Denne loader defualt fonten i str 36

font = pygame.font.SysFont(None, 36)

#Enemies. 
enemies = []
wave = 1  # Wave setter hvilken wave man starter på. 
enemies_to_spawn = 8  # Enemies_to_spawn setter hvor mange som spawner på første wave (etter det blir det flere og flere (5+ wave nummer * 3))
spawn_timer = 0  # spawn_timer teller hvor mange frames siden siste spawn
SPAWN_INTERVAL = 60  # spawner en fiende hvert 60/60fps aka 1 sek


# Player
player_pos = [WIDTH // 2, HEIGHT // 2] #Dette er posisjonen spilleren spawner på
player_radius = 20 #Radiusen til spilleren
speed = 5 #Hvor mange piksler den beveger seg per frame
player_x = WIDTH // 2 # x posisjonen
player_y = HEIGHT // 2 # y posisjonen

player = pygame.Rect(WIDTH // 2, HEIGHT // 2, player_radius * 2 , player_radius * 2)

# Bullets list
bullets = [] 
bullet_speed = 12 # pixler hver frame
bullet_radius = 4 # radiusen på kulen

# Variables
Meny = True

# Button class
 # Lagrer tekst og lager en rect for område til MENYEN
class Button:
    def __init__(self, text, x, y, w, h): 
        self.text = text
        self.rect = pygame.Rect(x, y, w, h)

# lager knappene, gjør de lilla men blå på "Hover"
    def draw(self, surface):
        color = HOVER_COLOR if self.rect.collidepoint(pygame.mouse.get_pos()) else BUTTON_COLOR
        pygame.draw.rect(surface, color, self.rect)
        pygame.draw.rect(surface, (0, 0, 0), self.rect, 2)

        text_surf = font.render(self.text, True, TEXT_COLOR)
        text_rect = text_surf.get_rect(center=self.rect.center)
        surface.blit(text_surf, text_rect)

# Gjør den True hvis man venstre klikker mens man er over knappen
    def clicked(self, event):
        return (
            event.type == pygame.MOUSEBUTTONDOWN
            and event.button == 1
            and self.rect.collidepoint(event.pos)
        )
# Her velger den en random del av kanten til skjermen. hver fiende/enemy har x og y verdi, radius og speed. 
def spawn_enemy():
    side = random.choice(["top", "bottom", "left", "right"])
    if side == "top":    x, y = random.randint(0, WIDTH), -20
    if side == "bottom": x, y = random.randint(0, WIDTH), HEIGHT + 20
    if side == "left":   x, y = -20, random.randint(0, HEIGHT)
    if side == "right":  x, y = WIDTH + 20, random.randint(0, HEIGHT)
    # Denne kjører hver eneste frame og hvis det forsatt er noen fiender som må spawne så teller den hvor mange frames mellom hver spawn. den sjekker også om "Waven" er ferdig og hvis den er det lager den en ny kø med flere fiender for neste "wave"
def wave_update():
    global enemies_to_spawn, spawn_timer, wave
    if enemies_to_spawn > 0:
        spawn_timer += 1
        if spawn_timer >= SPAWN_INTERVAL:
            spawn_enemy()
            enemies_to_spawn -= 1
            spawn_timer = 0
    elif len(enemies) == 0:
        wave += 1
        enemies_to_spawn = 5 + wave * 3

# Flytter hver fiende mot spillerens posisjon. Denne kjører også hver eneste frame. 
def update_enemies():
    for e in enemies:
        dx = player_pos[0] - e["x"]
        dy = player_pos[1] - e["y"]
        dist = math.hypot(dx, dy)
        if dist != 0:
            e["x"] += (dx / dist) * e["speed"]
            e["y"] += (dy / dist) * e["speed"]

# Tegner hver fiende på skjermen
# Denne går gjennom alle fiender og tegner en rød sirkel på posisjonen dems. 
def draw_enemies():
    for e in enemies:
        pygame.draw.circle(screen, (220, 50, 50), (int(e["x"]), int(e["y"])), e["radius"])

# Denne lager knapper på forskjellige "Kordinater" på siden med ulik bredde og høyde. (y,x,bredde,høyde)
buttons = [
    Button("Play", 600, 120, 300, 70),
    Button("Options", 600, 220, 300, 70),
    Button("Quit", 600, 320, 300, 70)
]

# Game loop
# Her kjører alt på 60fps og alt som er under skjer hver eneste frame (60 ganger i sekundet)
while True:
# for event in pygame.event.get(): sjekker for ting som skjer i framen den sjekker. feks museknapp, keyboard, eller krysse ut vinduet. 
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
    # Sier seg selv litt men endrer x/y verdien når man klikker en viss tast 
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w]:
                player_y -= speed
        if keys[pygame.K_s]:
                player_y += speed   
        if keys[pygame.K_d]:
                player_x += speed
        if keys[pygame.K_a]:
                player_x -= speed
        if keys[pygame.K_UP]:
                player_y -= speed
        if keys[pygame.K_DOWN]:
                player_y += speed   
        if keys[pygame.K_RIGHT]:
                player_x += speed
        if keys[pygame.K_LEFT]:
                player_x -= speed
    # Move bullets
    # Denne beveger kulene i riktig retining og sletter de når de forsvinner av skjermen. 
    for bullet in bullets[:]:
        bullet["pos"][0] += bullet["dir"][0] * bullet_speed
        bullet["pos"][1] += bullet["dir"][1] * bullet_speed 

        # fjerner kulene når de forsvinner av skjermen
        if (bullet["pos"][0] < 0 or bullet["pos"][0] > WIDTH or
            bullet["pos"][1] < 0 or bullet["pos"][1] > HEIGHT):
            bullets.remove(bullet)
    
    wave_update()    # håndterer "spawningen" og "wave" systemet 
    update_enemies()  # Oppdaterer posisjonen til alle fiender

    # Draw
    screen.fill(BG) # lager bakgrunnen med fargen (BG)
    if Meny:
        for button in buttons:
            button.draw(screen) # Lager meny knappene

    # Player
    if Meny == False:
        pygame.draw.circle(screen, PLAYER_COLOR, player_pos, player_radius) # Tegner spilleren
        draw_enemies()  # Tegner alle fiender
        #Enemies
        font = pygame.font.SysFont(None, 36) # tegner teksten for hvilken wave det er / hvor mange fiender det er
        screen.blit(font.render(f"Wave {wave}  Enemies: {len(enemies)}", True, (255,255,255)), (10, 10))

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
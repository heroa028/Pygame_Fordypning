#Dette importerer og starter alle pygame systemer som, lys display, input etc. 
import pygame
import sys
import math
import random
import os  # Brukes for å lese/skrive highscore filen

#Loader inn "bibliotekene"
pygame.init()

# Screen
#Disse lager wdindowet på den satte resolusjonen, og setter caption og clock setter fpsen. 
WIDTH, HEIGHT = 1440, 920
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Z-urvival")
clock = pygame.time.Clock()

# Colors¨
#Lagrer rgb verdier til forskjellige ting som skal ha farger
BG = (30, 30, 30)
PLAYER_COLOR = (0, 200, 255)
BULLET_COLOR = (255, 50, 50)
BUTTON_COLOR = (128, 0, 128)
HOVER_COLOR = (100, 170, 220)
TEXT_COLOR = (255, 255, 255)
BG_IMAGE = pygame.image.load("Bakgrunner/Background.png").convert()

# Denne loader defualt fonten i str 36
font = pygame.font.SysFont(None, 36)
font_big = pygame.font.SysFont(None, 100)  # Stor font til Game Over teksten

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
GameOver = False  # Holder styr på om spillet er over

# Score variabler - score teller poeng denne runden, highscore er den beste noensinne
score = 0
HIGHSCORE_FILE = "highscore.txt"  # Filen highscoren lagres i

# Laster inn highscoren fra filen hvis den finnes, ellers starter den på 0
def load_highscore():
    if os.path.exists(HIGHSCORE_FILE):
        with open(HIGHSCORE_FILE, "r") as f:
            try:
                return int(f.read())
            except:
                return 0
    return 0

# Lagrer highscoren til filen hvis den nye scoren er høyere enn den gamle
def save_highscore(new_score):
    current = load_highscore()
    if new_score > current:
        with open(HIGHSCORE_FILE, "w") as f:
            f.write(str(new_score))

# Laster inn highscoren når spillet starter
high_score = load_highscore()

# Nullstiller alt til startverdier slik at man kan spille på nytt fra menyen
def reset_game():
    global enemies, bullets, wave, enemies_to_spawn, spawn_timer
    global player_x, player_y, player_pos, score, GameOver, Meny
    enemies = []
    bullets = []
    wave = 1
    enemies_to_spawn = 8
    spawn_timer = 0
    player_x = WIDTH // 2
    player_y = HEIGHT // 2
    player_pos[0] = WIDTH // 2
    player_pos[1] = HEIGHT // 2
    score = 0
    GameOver = False
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
    enemies.append({"x": x, "y": y, "radius": 15, "speed": 6})

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

# Sjekker om en kule treffer en fiende ved å måle avstanden mellom dem
# Når en fiende dør får spilleren 10 poeng, og highscoren oppdateres hvis den slås
def check_bullet_enemy_collision():
    global score, high_score
    for bullet in bullets[:]:
        for e in enemies[:]:
            dx = bullet["pos"][0] - e["x"]
            dy = bullet["pos"][1] - e["y"]
            dist = math.hypot(dx, dy)
            # Hvis avstanden er mindre enn radiusen til kule + fiende har de kollidert
            if dist < bullet_radius + e["radius"]:
                bullets.remove(bullet)
                enemies.remove(e)
                score += 10  # Spilleren får 10 poeng per drept fiende
                if score > high_score:  # Oppdaterer highscoren hvis scoren er høyere
                    high_score = score
                    save_highscore(high_score)
                break  # Kula er allerede borte, ikke sjekk flere fiender for denne kula

# Sjekker om spilleren kolliderer med en fiende ved å måle avstanden mellom dem
# Hvis de kolliderer settes GameOver til True og spillet stopper
def check_player_enemy_collision():
    global GameOver
    for e in enemies:
        dx = player_pos[0] - e["x"]
        dy = player_pos[1] - e["y"]
        dist = math.hypot(dx, dy)
        # Hvis avstanden er mindre enn spillerens radius + fiendens radius har de truffet hverandre
        if dist < player_radius + e["radius"]:
            GameOver = True

# Denne lager knapper på forskjellige "Kordinater" på siden med ulik bredde og høyde. (y,x,bredde,høyde)
buttons = [
    Button("Play", 570, 120, 300, 70),
    Button("Options", 570, 220, 300, 70),
    Button("Quit", 570, 320, 300, 70)
]

# Knapper på Game Over skjermen
gameover_buttons = [
    Button("Meny", 570, 530, 300, 70),
    Button("Quit", 570, 630, 300, 70)
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
                        score = 0  # Nullstiller scoren når man starter et nytt spill

        # Sjekker om man klikker på knappene på Game Over skjermen
        if GameOver == True:
            for button in gameover_buttons:
                if button.clicked(event):
                    if button.text == "Meny":
                        reset_game()  # Nullstiller alt og sender spilleren tilbake til menyen
                    if button.text == "Quit":
                        pygame.quit()
                        sys.exit()

        if Meny == False and GameOver == False:
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
    if Meny == False and GameOver == False:
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
        if keys[pygame.K_ESCAPE]:
                Meny = True
    # Move bullets
    # Denne beveger kulene i riktig retining og sletter de når de forsvinner av skjermen. 
    for bullet in bullets[:]:
        bullet["pos"][0] += bullet["dir"][0] * bullet_speed
        bullet["pos"][1] += bullet["dir"][1] * bullet_speed 

        # fjerner kulene når de forsvinner av skjermen
        if (bullet["pos"][0] < 0 or bullet["pos"][0] > WIDTH or
            bullet["pos"][1] < 0 or bullet["pos"][1] > HEIGHT):
            bullets.remove(bullet)
    
    # Oppdaterer kun spillet hvis man ikke er på menyen eller game over skjermen
    if Meny == False and GameOver == False:
        wave_update()    # håndterer "spawningen" og "wave" systemet 
        update_enemies()  # Oppdaterer posisjonen til alle fiender
        check_bullet_enemy_collision()  # Sjekker kollisjoner mellom kuler og fiender
        check_player_enemy_collision()  # Sjekker om spilleren er truffet av en fiende

    # Draw
    screen.fill(BG) # lager bakgrunnen med fargen (BG)
    screen.blit(BG_IMAGE, (0,0))
    if Meny:
        for button in buttons:
            button.draw(screen) # Lager meny knappene
        # Viser highscoren på menyen nederst i midten
        hs_surf = font.render(f"High Score: {high_score}", True, TEXT_COLOR)
        hs_rect = hs_surf.get_rect(center=(WIDTH // 2, 430))
        screen.blit(hs_surf, hs_rect)

    # Player
    if Meny == False and GameOver == False:
        pygame.draw.circle(screen, PLAYER_COLOR, player_pos, player_radius) # Tegner spilleren
        draw_enemies()  # Tegner alle fiender
        #Enemies
        font = pygame.font.SysFont(None, 50) # tegner teksten for hvilken wave det er / hvor mange fiender det er
        screen.blit(font.render(f"Wave {wave}  Enemies: {len(enemies)}", True, (255,255,255)), (10, 20))
        # Viser nåværende score og highscore øverst til høyre
        screen.blit(font.render(f"Score: {score}  Best: {high_score}", True, (255,255,255)), (WIDTH - 400, 20))

    # Tegner Game Over skjermen med score, highscore og knapper
    if GameOver == True:
        go_surf = font_big.render("GAME OVER", True, (220, 50, 50))
        go_rect = go_surf.get_rect(center=(WIDTH // 2, 300))
        screen.blit(go_surf, go_rect)
        screen.blit(font.render(f"Score: {score}", True, TEXT_COLOR),
                    font.render(f"Score: {score}", True, TEXT_COLOR).get_rect(center=(WIDTH // 2, 420)))
        screen.blit(font.render(f"High Score: {high_score}", True, TEXT_COLOR),
                    font.render(f"High Score: {high_score}", True, TEXT_COLOR).get_rect(center=(WIDTH // 2, 465)))
        for button in gameover_buttons:
            button.draw(screen)  # Tegner Meny og Quit knappene

     # Denne holder spilleren på skjermen
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
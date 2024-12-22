import math
import pygame
import random
from pygame import mixer
import asyncio

# pygame initializer
pygame.init()


screen = pygame.display.set_mode((800, 600))

# background
background = pygame.image.load('back.png')

mixer.music.load('lazer-grid-80s-synthwave-walking-track-227155.wav')
mixer.music.play(-1)

# title and stuff
pygame.display.set_caption("Space Shooter")
icon = pygame.image.load('iconn.png')
pygame.display.set_icon(icon)

# Player
playerImg = pygame.image.load('player.png')
playerX = 370
playerY = 470
playerX_change = 0
playerY_change = 0

# Monster
monsterImg = []
monsterX = []
monsterY = []
monsterX_change = []
monsterY_change = []
nofmonsters = 5

for i in range(nofmonsters):
    monsterImg.append(pygame.image.load('monster.png'))
    monsterX.append(random.randint(50, 600))
    monsterY.append(random.randint(10, 250))
    monsterX_change.append(0.4)
    monsterY_change.append(0.5)

# Laser
laserImg = pygame.image.load('magic.png')
laserX = 0
laserY = 480
laserX_change = 0
laserY_change = 1.5
laser_state = "ready"

# Score
score_value = 0
font = pygame.font.Font('Transformers Movie.ttf', 42)
textX = 350
textY = 60

checkpoint_played = False

# Game Over font
game_over_font = pygame.font.Font('Transformers Movie.ttf', 64)

def show_score(x, y):
    score = font.render("Score: " + str(score_value), True, (255, 124, 0))
    screen.blit(score, (x, y))

def player(x, y):
    screen.blit(playerImg, (x, y))

def monster(x, y, i):
    screen.blit(monsterImg[i], (x, y))

def fire(x, y):
    global laser_state
    laser_state = "fire"
    screen.blit(laserImg, (x + 16, y + 10))

def isCollision(obj1X, obj1Y, obj2X, obj2Y, distance_threshold):
    distance = math.sqrt((math.pow(obj1X - obj2X, 2)) + (math.pow(obj1Y - obj2Y, 2)))
    return distance < distance_threshold

def game_over_text():
    over_text = game_over_font.render("GAME OVER", True, (255, 0, 0))
    fin_text = game_over_font.render("press spacebar twice ",True,(100,245,0))
    screen.blit(over_text, (200, 250))
    screen.blit(fin_text,(30,50))
    mixer.music.load('hit.wav')
    mixer.music.play(1)

def reset_game():
    global playerX, playerY, playerX_change, playerY_change, laserX, laserY, laser_state, score_value, game_over, monsterX, monsterY, checkpoint_played

    playerX = 370
    playerY = 470
    playerX_change = 0
    playerY_change = 0
    laserX = 0
    laserY = 480
    laser_state = "ready"
    score_value = 0
    game_over = False
    checkpoint_played = False

    for i in range(nofmonsters):
        monsterX[i] = random.randint(50, 600)
        monsterY[i] = random.randint(10, 250)

game_over = False
spacebar_pressed = 0
spacebar_last_time = 0

# Game loop
running = True
while running:
    screen.fill((0, 0, 20))
    screen.blit(background, (0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                playerX_change = -1.0
            if event.key == pygame.K_RIGHT:
                playerX_change = 1.0
            if event.key == pygame.K_UP:
                playerY_change = -1.0
            if event.key == pygame.K_DOWN:
                playerY_change = 1.0
            if event.key == pygame.K_SPACE:
                laser_sound = mixer.Sound('shoot.wav')
                laser_sound.play()
                if laser_state == "ready" and not game_over:
                    laserX = playerX  # Laser starts from the player's position
                    fire(laserX, laserY)

                if game_over:
                    current_time = pygame.time.get_ticks()
                    if current_time - spacebar_last_time < 500:
                        spacebar_pressed += 1
                    else:
                        spacebar_pressed = 1

                    spacebar_last_time = current_time

                    if spacebar_pressed >= 2:
                        reset_game()

        if event.type == pygame.KEYUP:
            if event.key in [pygame.K_LEFT, pygame.K_RIGHT]:
                playerX_change = 0
            if event.key in [pygame.K_UP, pygame.K_DOWN]:
                playerY_change = 0

    if not game_over:
        # Update player position
        playerX += playerX_change
        playerY += playerY_change

        # Boundary checking to prevent the player from moving out of the screen
        playerX = max(0, min(playerX, 800 - playerImg.get_width()))
        playerY = max(0, min(playerY, 600 - playerImg.get_height()))

        # Update monster position
        for i in range(nofmonsters):
            monsterX[i] += monsterX_change[i]
            if monsterX[i] <= 0 or monsterX[i] >= 800 - monsterImg[i].get_width():
                monsterX_change[i] = -monsterX_change[i]

            monsterY[i] += monsterY_change[i]
            if monsterY[i] <= 100 or monsterY[i] >= 600 - monsterImg[i].get_width():
                monsterY_change[i] = -monsterY_change[i]

            # Collision detection with laser
            collision = isCollision(monsterX[i], monsterY[i], laserX, laserY, 27)
            if collision:
                hit_sound = mixer.Sound('hitt.wav')
                hit_sound.play()
                laserY = 480
                laser_state = "ready"
                score_value += 1

                monsterX[i] = random.randint(50, 600)
                monsterY[i] = random.randint(10, 250)

            # Collision detection with player
            if isCollision(monsterX[i], monsterY[i], playerX, playerY, 40):
                for j in range(nofmonsters):
                    monsterX[j] = 2000  # Move monsters off-screen
                game_over = True

            monster(monsterX[i], monsterY[i], i)

        # Play checkpoint sound when score is a multiple of 10
        if score_value % 10 == 0 and score_value != 0 and not checkpoint_played:
            checkpoint_sound = mixer.Sound('hit.wav')
            checkpoint_sound.play()
            checkpoint_played = True
        elif score_value % 10 != 0:
            checkpoint_played = False

        # Laser movement
        if laser_state == "fire":
            fire(laserX, laserY)
            laserY -= laserY_change

        # Reset laser when it goes off screen
        if laserY <= 0:
            laserY = playerY
            laser_state = "ready"

        # Draw the player and monster at their new positions
        player(playerX, playerY)
        show_score(textX, textY)

    else:
        # Display game over text when the game is over
        game_over_text()

    pygame.display.update()

# Quit pygame
pygame.quit()

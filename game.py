import pygame
import random
import math

pygame.init()  # Initialize pygame

screen = pygame.display.set_mode((800, 600))  # Used to create screen
crazy_mode = [4,6]
# Title and Icon and Music
pygame.display.set_caption("Space Invaders")
icon = pygame.image.load("UFO-icon.png")
pygame.display.set_icon(icon)
background = pygame.image.load("background.jpg")
background2 = pygame.image.load("background2.jpg")
# Enemy
enemyImg = []
enemyX = []
enemyY = []
enemy_X_change = []
enemy_Y_change = []
num_enemies = 6
for i in range(num_enemies):
    enemyImg.append(pygame.image.load("enemy.png"))
    enemyX.append(random.randint(0, 736))
    enemyY.append(random.randint(50, 150))
    enemy_X_change.append(crazy_mode[0])
    enemy_Y_change.append(40)
# Bullet
bulletImg = pygame.image.load("bullet.png")
bulletX = 0
bulletY = 480
bullet_X_change = 0
bullet_Y_change = 10
bullet_state = "ready"
# Player
playerImg = pygame.image.load("player.png")
playerX = 370
playerY = 480
Xchange = 0

explosion = pygame.image.load("explosion.png")

# Score Display
score = 0
font = pygame.font.Font("freesansbold.ttf", 32)
textX, textY = 10, 10


# Game Over
def game_over_text():
    text_font = pygame.font.Font("freesansbold.ttf", 64)
    text_msg = text_font.render("GAME OVER", True, (255, 255, 255))
    screen.blit(text_msg, (200, 250))


def score_display(x, y):
    score_value = font.render("Score: " + str(score), True, (255, 255, 255))
    screen.blit(score_value, (x, y))


def player(x, y):
    screen.blit(playerImg, (x, y))


def enemy(x, y, i):
    screen.blit(enemyImg[i], (x, y))


def fire_bullet(x, y):
    global bullet_state
    bullet_state = "fire"
    screen.blit(bulletImg, (x + 16, y + 10))


def isCollision(x1, y1, x2, y2):
    dist = math.sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2)
    if dist <= 27:
        return True
    else:
        return False

def crazy():
    for i in range(num_enemies):
        enemy_X_change[i] = crazy_mode[1]

def music_change(i):
    music = "music2.mp3"
    if i==1:
        music = "music2.mp3"
    else:
        music = "music.mp3"
    track = pygame.mixer.music.load(music)
    pygame.mixer.music.play(-1)
music_change(1)
background_choice = background
# Game Loop
running = True
while running:
    screen.fill((0, 0, 0))
    screen.blit(background_choice, (0, 0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        # Keyboard control
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                Xchange = -5
            if event.key == pygame.K_RIGHT:
                Xchange = 5
            if event.key == pygame.K_SPACE:
                if bullet_state is "ready":
                    bullet_sound = pygame.mixer.Sound("laser.wav")
                    bullet_sound.play()
                    bulletX = playerX
                    fire_bullet(bulletX, bulletY)
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                Xchange = 0
    playerX += Xchange
    if playerX <= 0:
        background_choice = background
        playerX = 736
        music_change(1)
    if playerX >= 800:
        background_choice = background2
        playerX = 0
        crazy()
        music_change(2)
    # Enemy Movement
    for i in range(num_enemies):
        # Game Over
        if enemyY[i] >= 440:
            for j in range(num_enemies):
                enemyY[j] = 2000
            game_over_text()
            break
        enemyX[i] += enemy_X_change[i]
        if enemyX[i] <= 0:
            enemy_X_change[i] = 4
            enemyY[i] += enemy_Y_change[i]
        elif enemyX[i] >= 736:
            enemy_X_change[i] = -4
            enemyY[i] += enemy_Y_change[i]
        # Enemy Collision Check
        collision = isCollision(enemyX[i], enemyY[i], bulletX, bulletY)
        if collision:
            explosion_sound = pygame.mixer.Sound("explosion.wav")
            explosion_sound.play()
            bulletY = 480
            bullet_state = "ready"
            score += 1
            screen.blit(explosion, (enemyX[i], enemyY[i]))
            print(score)
            enemyX[i] = random.randint(0, 736)
            enemyY[i] = random.randint(50, 150)
        enemy(enemyX[i], enemyY[i], i)
    # Bullet Movement
    if bulletY <= 0:
        bulletY = 480
        bullet_state = "ready"
    if bullet_state is "fire":
        fire_bullet(bulletX, bulletY)
        bulletY -= bullet_Y_change
    score_display(textX, textY)
    player(playerX, playerY)
    pygame.display.update()

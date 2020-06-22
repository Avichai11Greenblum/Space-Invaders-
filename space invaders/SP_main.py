import pygame, random, math
from pygame import mixer

pygame.init()

# Making the screen
screen = pygame.display.set_mode((800, 600))

# Title and icon
pygame.display.set_caption('My first game!')
my_icon = pygame.image.load('spaceship logo.png')
pygame.display.set_icon(my_icon)

# Background
bg = pygame.image.load('5311.png')

# Background sound
mixer.music.load('background.wav')
mixer.music.play(-1)

# Game over
finish_font = pygame.font.Font('freesansbold.ttf', 64)


def endgame():
    game_over = finish_font.render('GAME OVER!', True, (255, 255, 255))
    screen.blit(game_over, (200, 250))


# player
playerIMG = pygame.image.load('player logo.png')
playerX, playerY = 370, 480
playerX_change = 0


def player_show(x, y):
    screen.blit(playerIMG, (x, y))


# Score
score_value = 0
my_font = pygame.font.Font('freesansbold.ttf', 25)

textX, textY = 10, 10


def show_score(x, y):
    score = my_font.render('SCORE: ' + str(score_value), True, (255, 255, 255))
    screen.blit(score, (x, y))


# enemy
enemyIMG = []
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []
enemies_num = 13

for i in range(enemies_num):
    enemyIMG.append(pygame.image.load('ufo.png'))
    enemyX.append(random.randint(64, 736))
    enemyY.append(random.randint(80, 150))  # 20 150
    enemyX_change.append(1.75)
    enemyY_change.append(60)


def enemy_show(x, y):
    screen.blit(enemyIMG[i], (x, y))


# Bomb
bombIMG = pygame.image.load('bomb.png')
bombX, bombY = 0, 480
bombY_change = -3
fire_state = 'ready'
clash_sound = mixer.Sound('explosion.wav')


def fire(x, y):
    global fire_state
    fire_state = 'fire'
    screen.blit(bombIMG, (x + 16, y - 20))


def isCollision(enemyX, enemyY, bbX, bbY):
    distance = math.sqrt((math.pow(enemyX - bbX, 2) + 32) + (math.pow(enemyY - bbY, 2) + 32))
    if distance <= 50:
        return True
    return False


# Boom
kaboom = pygame.image.load('explosionIMG.png')

def boom(x, y):
    screen.blit(kaboom, (x, y))

    
# Game Loop
player_stop = False
run = True

while run:

    # RGB ->  red, green, blue
    screen.fill((0, 30, 80))
    screen.blit(bg, (0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

        # Making sure the spaceship will stop after we stop pressing
        playerX_change = 0

        # Checking which key is being pressed and act to it
        if event.type == pygame.KEYDOWN and player_stop is False:
            if event.key == pygame.K_LEFT:
                playerX_change -= 3
            if event.key == pygame.K_RIGHT:
                playerX_change += 3
            if event.key == pygame.K_SPACE and fire_state is 'ready':
                bomb_sound = mixer.Sound('laser.wav')
                bomb_sound.play()
                bombX = playerX
                fire(bombX, bombY)

        # Making sure when we stop pressing the spaceship stops
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                playerX_change = 0

    playerX += playerX_change

    # Making sure the spaceship cant go outside of borders
    if playerX <= 0:
        playerX = 0
    elif playerX >= 736:
        playerX = 736

    # Enemy movement
    for i in range(enemies_num):

        # checking for crash with enemy
        if math.sqrt((math.pow(enemyX[i] - playerX, 2) + 32) + (math.pow(enemyY[i] - playerY, 2) + 32)) <= 61:
            for j in range(enemies_num):
                enemyX_change[j] = 0
                player_stop = True
            endgame()
            break

        enemyX[i] += enemyX_change[i]

        if enemyX[i] <= 0:
            enemyX_change[i] = 1.75
            enemyY[i] += enemyY_change[i]
        elif enemyX[i] >= 736:
            enemyX_change[i] = -1.75
            enemyY[i] += enemyY_change[i]

        # Collision
        collision = isCollision(enemyX[i], enemyY[i], bombX, bombY)
        if collision and math.sqrt(math.pow(playerY - enemyY[i], 2)) > 20:
            clash_sound.play()
            bombY = 480
            fire_state = 'ready'
            enemyX[i], enemyY[i] = random.randint(64, 736), random.randint(20, 150)
            score_value += 1

        enemy_show(enemyX[i], enemyY[i])

    # Bomb movement
    if bombY <= 20:
        bombY = 480
        fire_state = 'ready'

    if fire_state is 'fire':
        fire(bombX, bombY)
        bombY += bombY_change

    player_show(playerX, playerY)

    show_score(textX, textY)
    pygame.display.update()

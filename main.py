# Aqil Gama Rahmansyah @ 2023

import pygame # import pygame engine
from sys import exit # to excute when exit
from random import randint # to make random number

## Initialize
pygame.init() # initialize the pygame
screenSize = (800, 400)
screen = pygame.display.set_mode((screenSize))
pygame.display.set_caption('Maxwell')
clock = pygame.time.Clock() # clocks
bgColor = (255, 255, 255)
groundColor = (0, 0, 0)
gravity = 0
gravitySpeed = 0.8
gameState = 1 # 0 = run, 1 = menu
startTime = 0
maxwellRotat = 0
fontsName = ('Assets/prstart.ttf')
lastScore = 0
highScore = 0
bgmSound = pygame.mixer.Sound('Assets/bgm.mp3')
jumpSound = pygame.mixer.Sound('Assets/jump.wav')
explodeSound = pygame.mixer.Sound('Assets/explode.mp3')
startSound = pygame.mixer.Sound('Assets/Start.mp3')
bgmSound.play(loops = -1)
captionTextSize = 20
sizeState = 0
idSize = 0

spawnTime = pygame.USEREVENT + 1
pygame.time.set_timer(spawnTime, 900)

# Icons
gameIcons = pygame.image.load('Assets/Maxwell.png')
pygame.display.set_icon(gameIcons)

# Fonts Things
scoreFonts = pygame.font.Font(fontsName, 60)
gameoverFonts = pygame.font.Font(fontsName, 65)
cprFonts = pygame.font.Font(fontsName, 16)
menuFonts = pygame.font.Font(fontsName, 24)

# Player Things
playerSpr = pygame.image.load('Assets/Maxwell.png').convert_alpha()
playerSprRect = playerSpr.get_rect(midbottom = (100, 300))

# The Object Things
objSpr = pygame.image.load('Assets/gato.png').convert_alpha()
objFlySpr = pygame.image.load('Assets/gatoB.png').convert_alpha()

def objMove(objList):
    if objList:
        for objRect in objList:
            objRect.x -= 8
            
            if objRect.bottom == 300: screen.blit(objSpr, objRect)
            else: screen.blit(objFlySpr, objRect)

        objList = [obj for obj in objList if obj.x > -150]
    
        return objList
    else: return []

def objColl(target, object):
    if object:
        for objRect in object:
            if target.colliderect(objRect): 
                explodeSound.play()
                return 1
    return 0

objRectList = []

# Texts
def score():
    curTime = int(pygame.time.get_ticks() / 1000) - startTime
    scoreText = scoreFonts.render(f'{curTime}', False, (0, 0, 0))
    scoreTextRec = scoreText.get_rect(topright = (790, 10))
    screen.blit(scoreText, scoreTextRec)
    return curTime

cprText = cprFonts.render('Kaon @2023', False, (0, 0, 0))
cprTextRec = cprText.get_rect(topleft = (10, 10))

## Loop
while True: 
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

        if gameState == 0:
            # player controls
            if event.type == pygame.KEYDOWN and event.key == pygame.K_UP and playerSprRect.bottom == 300: 
                gravity = -15
                jumpSound.play()
                
        elif gameState == 1:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_UP:
                gameState = 0
                startSound.play()
                startTime = int(pygame.time.get_ticks() / 1000)

        if event.type == spawnTime and gameState == 0:
            if randint(0, 2): objRectList.append(objSpr.get_rect(midbottom = (randint(900, 1100), 300)))
            else: objRectList.append(objFlySpr.get_rect(midbottom = (randint(900, 1100), 150)))

    if gameState == 0:
        screen.fill(bgColor)
        pygame.draw.rect(screen, groundColor, pygame.Rect(0, 300, 800, 300))

        gravity += gravitySpeed
        playerSprRect.y += gravity

        if playerSprRect.bottom <= 300: playerSpr = pygame.transform.rotate(playerSpr, maxwellRotat)

        if playerSprRect.bottom >= 300: playerSprRect.bottom = 300
    
        objRectList = objMove(objRectList)

        # draw object
        score()
        lastScore = score()
        screen.blit(playerSpr, playerSprRect)
        screen.blit(cprText, cprTextRec)

        gameState = objColl(playerSprRect, objRectList)

        if lastScore > highScore:
            highScore = lastScore

    elif gameState == 1:
        screen.fill((0, 0, 0))
        objRectList.clear()

        if lastScore == 0:
            gameoverText = gameoverFonts.render('MAXWELL', False, (255, 255, 255))
            gameoverTextRec = gameoverText.get_rect(midtop = (400, 30))
            gameoverText_A = menuFonts.render('Press Jump (UP) to restart', False, (255, 255, 255))
            gameoverTextRec_A = gameoverText_A.get_rect(midbottom = (400, 370))

            idSize += 1

            if sizeState == 0 and captionTextSize >= 16: 
                captionTextSize -= idSize
                if captionTextSize < 16 : 
                    sizeState = 1
                    idSize = 0
            if sizeState == 1 and captionTextSize <= 24: 
                captionTextSize += idSize
                if captionTextSize > 24 : 
                    sizeState = 0
                    idSize = 0

            captionsFonts = pygame.font.Font(fontsName, captionTextSize)
            captionsText = captionsFonts.render('Wtf even is this', False, (255, 0, 0))
            captionsTextRec = captionsText.get_rect(center = (400, 100))
            screen.blit(captionsText, captionsTextRec)

        else:
            gameoverText = gameoverFonts.render('GAME OVER', False, (255, 255, 255))
            gameoverTextRec = gameoverText.get_rect(midtop = (400, 30))
            gameoverText_A = menuFonts.render(f'Score: {lastScore} | High Score: {highScore}', False, (255, 255, 255))
            gameoverTextRec_A = gameoverText_A.get_rect(midbottom = (400, 370))  

        screen.blit(gameoverText, gameoverTextRec)
        screen.blit(gameoverText_A, gameoverTextRec_A)

    pygame.display.update()
    clock.tick(60) # Limit framerate
import pygame
import time
import random

pygame.init()

WidthDisplay = 800
HeightDisplay = 600
carWidth = 60
gameDisplay = pygame.display.set_mode((WidthDisplay, HeightDisplay))
pygame.display.set_caption('Racer')

clock = pygame.time.Clock()
crashed = False
carImage = pygame.image.load('Car.png')


def things_dodged(count):
    font = pygame.font.Font('17668.otf', 20)
    text = font.render("Dodged: "+str(count), True, (0, 0, 0))
    gameDisplay.blit(text,(0,0))

def things(thingX, thingY, thingW, thingH, color):
    pygame.draw.rect(gameDisplay, color, [thingX, thingY, thingW, thingH])

def car(x,y):
    gameDisplay.blit(carImage,(x,y))

def text_objects(text, font):
    textSurface = font.render(text, True, (181, 20, 20))
    return textSurface, textSurface.get_rect()

def message_display(text):
    largeText = pygame.font.Font('17666.otf',115)
    TextSurf, TextRect = text_objects(text, largeText)
    TextRect.center = ((WidthDisplay / 2),(HeightDisplay / 2))
    gameDisplay.blit(TextSurf, TextRect)

    pygame.display.update()

    time.sleep(2)

    gameLoop()

def crash():
    message_display('You crashed!')

def gameLoop():
    x = WidthDisplay * 0.45
    y = HeightDisplay * 0.8
    gameExit = False
    xChange = 0

    thing_startx = random.randrange(0, WidthDisplay)
    thing_starty = -600
    thing_speed = 7
    thing_width = 100
    thing_height = 100
    dodged = 0

    while not gameExit:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                gameExit = True
    ######################################
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    xChange = -5
                elif event.key == pygame.K_RIGHT:
                    xChange = 5
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                    xChange = 0
    ######################################
        x += xChange
    ######################################
        #there is our environment
        gameDisplay.fill((255, 255, 255))

        things(thing_startx, thing_starty, thing_width, thing_height, (0, 0, 0))
        thing_starty += thing_speed
        car(x, y)
        things_dodged(dodged)

        if x > WidthDisplay - carWidth:
            x = WidthDisplay - carWidth

        if x < 0:
            x = 0

        if thing_starty > HeightDisplay:
            thing_starty = 0 - thing_height
            thing_startx = random.randrange(0, WidthDisplay)
            dodged += 1
            thing_speed += 1
            thing_width += (dodged * 1.2)

        if y < thing_starty + thing_height:
            if x > thing_startx and x < thing_startx + thing_width or x + carWidth >= thing_startx and x + carWidth <= thing_startx + thing_width: #ERROR! FIX IT!
                crash()

        pygame.display.update()
        clock.tick(60)

gameLoop()
pygame.quit()
quit()
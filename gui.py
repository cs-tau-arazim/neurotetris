import pygame
import time
from pygame import *

pygame.init()

windowHeight = 1024
windowWidth = 768
screen = pygame.display.set_mode((windowWidth,windowHeight))
screen.fill([255,255,255])

white = (255, 255, 255)
black = (0, 0, 0)
red = (255, 0 , 0)
blue = (0, 0, 255)
colors = [white, black ,red, blue]

## Pictures:
#doodlePicture = pygame.image.load("doodleNinjaPicture.png")
#background = pygame.image.load("Picture.jpg")
#background.convert()
#backgroundRect = background.get_rect()
size = 768, 1024
screen = pygame.display.set_mode()
#screen.blit(background, backgroundRect)

while True:

    time.delay(1000)
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            quit()

    pygame.display.update()




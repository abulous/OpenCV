#skel

import pygame
from pygame.locals import *
from sys import exit
from random import choice

clock = pygame.time.Clock()

pygame.init()

# get the screen hight and width
disp_info = pygame.display.Info()
width = disp_info.current_w
height = disp_info.current_h


screen = pygame.display.set_mode((width, height), NOFRAME)
pygame.display.set_caption('abeHack')
test = 255

counter = 1
color = 0

value = choice([1, 2, 3])
value1 = choice([2, 4, 6])

radius = 225

print("width", width)
print("height", height)
print("radius", radius)
##input('press ENTER to resume script')

posW = [180, 360, 720, 1080, 1440]
posH = [45, 90, 180, 225, 450, 675, 900]


while True:
    for event in pygame.event.get():
        if event.type == KEYDOWN:
            if event.key == K_q:
                exit()	
        if event.type == QUIT:
            exit()        

    counter += 1
    if counter >= 5:
        value = choice([1, 2, 3])

    if counter >= 10:
        counter = 0
        
##    if counter > 0 and counter <= 10:

    color += 10
    if color >= 255:
        color = 0

    if test == 255:
        test = 0
    else:
        test = 255
        
    screen.fill((test, color, color/value))

    pygame.draw.circle(screen, (color/value, color, test), [choice(posW), choice(posH)], radius, 0)

    pygame.display.update()
    clock.tick(counter)



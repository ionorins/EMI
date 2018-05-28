import pygame, time

pygame.init()
pygame.mixer.init()
music = pygame.mixer.music

while True:
    a = raw_input()
    music.load("sounds/" + a +".wav")
    music.play()

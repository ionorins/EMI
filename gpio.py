import RPi.GPIO as GPIO
import pygame, time

# GPIO set up
pin = 10
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)
GPIO.setup(pin, GPIO.IN, pull_up_down = GPIO.PUD_DOWN)

# Player set up
pygame.init()
pygame.mixer.init()
player = pygame.mixer.music

# Purr set up
path = '/home/pi/Desktop/EMI/'
purr = path + 'sounds/purr.wav'
player.load(purr)
purring = 0

while True: # Run forever
    print GPIO.input(10)
    if GPIO.input(10) == GPIO.HIGH and not pygame.mixer.music.get_busy():
        player.play()
            

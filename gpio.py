import RPi.GPIO as GPIO
import pygame

GPIO.setmode(GPIO.BCM)


GPIO.setup(7, GPIO.IN)

while True:
    print GPIO.input(7)
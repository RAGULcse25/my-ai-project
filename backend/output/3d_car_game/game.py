# Import necessary libraries
import pygame
import sys
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
import numpy as np
from car_model import Car
from track import Track

# Initialize Pygame
pygame.init()

# Set up display variables
WIDTH, HEIGHT = 800, 600
display = (WIDTH, HEIGHT)

# Set up OpenGL display
pygame.display.set_mode(display, DOUBLEBUF | OPENGL)

# Set up perspective
gluPerspective(45, (display[0]/display[1]), 0.1, 50.0)

# Set up viewing position
glTranslatef(0.0, 0.0, -5)

# Create a car object
car = Car()

# Create a track object
track = Track()

# Game loop
while True:
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # Get a list of all keys currently being pressed down
    keys = pygame.key.get_pressed()

    # Move the car based on the keys being pressed
    if keys[pygame.K_w]:
        car.move_forward()
    if keys[pygame.K_s]:
        car.move_backward()
    if keys[pygame.K_a]:
        car.turn_left()
    if keys[pygame.K_d]:
        car.turn_right()

    # Clear the screen
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

    # Draw the track
    track.draw()

    # Draw the car
    car.draw()

    # Update the display
    pygame.display.flip()
    pygame.time.wait(10)
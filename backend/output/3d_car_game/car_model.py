# Import necessary libraries
import numpy as np
from OpenGL.GL import *
from OpenGL.GLU import *

# Define a class for the car model
class CarModel:
    # Initialize the car model with its properties
    def __init__(self, x, y, z, length, width, height, color):
        self.x = x
        self.y = y
        self.z = z
        self.length = length
        self.width = width
        self.height = height
        self.color = color

    # Draw the car model using OpenGL
    def draw(self):
        # Set the car's position
        glPushMatrix()
        glTranslatef(self.x, self.y, self.z)

        # Set the car's color
        glColor3f(self.color[0], self.color[1], self.color[2])

        # Draw the car's body
        glBegin(GL_QUADS)
        # Front face
        glVertex3f(-self.length/2, -self.width/2, self.height/2)
        glVertex3f(self.length/2, -self.width/2, self.height/2)
        glVertex3f(self.length/2, self.width/2, self.height/2)
        glVertex3f(-self.length/2, self.width/2, self.height/2)

        # Back face
        glVertex3f(-self.length/2, -self.width/2, -self.height/2)
        glVertex3f(self.length/2, -self.width/2, -self.height/2)
        glVertex3f(self.length/2, self.width/2, -self.height/2)
        glVertex3f(-self.length/2, self.width/2, -self.height/2)

        # Left face
        glVertex3f(-self.length/2, -self.width/2, -self.height/2)
        glVertex3f(-self.length/2, -self.width/2, self.height/2)
        glVertex3f(-self.length/2, self.width/2, self.height/2)
        glVertex3f(-self.length/2, self.width/2, -self.height/2)

        # Right face
        glVertex3f(self.length/2, -self.width/2, -self.height/2)
        glVertex3f(self.length/2, -self.width/2, self.height/2)
        glVertex3f(self.length/2, self.width/2, self.height/2)
        glVertex3f(self.length/2, self.width/2, -self.height/2)

        # Top face
        glVertex3f(-self.length/2, -self.width/2, self.height/2)
        glVertex3f(self.length/2, -self.width/2, self.height/2)
        glVertex3f(self.length/2, self.width/2, self.height/2)
        glVertex3f(-self.length/2, self.width/2, self.height/2)

        # Bottom face
        glVertex3f(-self.length/2, -self.width/2, -self.height/2)
        glVertex3f(self.length/2, -self.width/2, -self.height/2)
        glVertex3f(self.length/2, self.width/2, -self.height/2)
        glVertex3f(-self.length/2, self.width/2, -self.height/2)
        glEnd()

        # Draw the car's wheels
        self.draw_wheel(-self.length/4, self.width/2, -self.height/2)
        self.draw_wheel(self.length/4, self.width/2, -self.height/2)
        self.draw_wheel(-self.length/4, -self.width/2, -self.height/2)
        self.draw_wheel(self.length/4, -self.width/2, -self.height/2)

        glPopMatrix()

    # Draw a single wheel
    def draw_wheel(self, x, y, z):
        glPushMatrix()
        glTranslatef(x, y, z)
        glColor3f(0, 0, 0)
        gluSphere(gluNewQuadric(), 0.1, 32, 16)
        glPopMatrix()

# Example usage:
if __name__ == "__main__":
    # Create a car model
    car = CarModel(0, 0, 0, 2, 1, 1, (1, 0, 0))

    # Draw the car model
    car.draw()
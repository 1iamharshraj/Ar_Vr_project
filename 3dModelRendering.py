import cv2
from OpenGL.GL import *
from OpenGL.GLUT import *
import numpy as np
import pygame
from OpenGL.raw.GLU import gluLookAt
from pygame.locals import *



# Set up the camera
cap = cv2.VideoCapture(0)



# Function to draw a pyramid
def draw_pyramid():
    glBegin(GL_TRIANGLES)

    # Front face
    glColor3f(1, 0, 0)
    glVertex3f(0, 1, 0)
    glVertex3f(-1, -1, 1)
    glVertex3f(1, -1, 1)

    # Right face
    glColor3f(0, 1, 0)
    glVertex3f(0, 1, 0)
    glVertex3f(1, -1, 1)
    glVertex3f(1, -1, -1)

    # Back face
    glColor3f(0, 0, 1)
    glVertex3f(0, 1, 0)
    glVertex3f(1, -1, -1)
    glVertex3f(-1, -1, -1)

    # Left face
    glColor3f(1, 1, 0)
    glVertex3f(0, 1, 0)
    glVertex3f(-1, -1, -1)
    glVertex3f(-1, -1, 1)

    glEnd()



# Initialize Pygame
pygame.init()



# Main loop
while True:
    ret, frame = cap.read()

    if not ret:
        print("Error reading frame")
        break

    # Get the size of the frame
    height, width, _ = frame.shape

    # Clear the screen
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

    # Set the camera position
    gluLookAt(0, 0, 5, 0, 0, 0, 0, 1, 0)

    # Draw the pyramid at a specific location (e.g., x=0, y=0, z=-2)
    glTranslatef(0, 0, -2)  # Adjusted position
    draw_pyramid()

    # Convert the OpenGL buffer to a numpy array for OpenCV
    buffer = glReadPixels(0, 0, width, height, GL_RGB, GL_UNSIGNED_BYTE)
    image_opengl = np.frombuffer(buffer, dtype=np.uint8).reshape(height, width, 3)
    image_opengl = cv2.flip(image_opengl, 0)  # Flip the image vertically for OpenCV

    # Overlay the OpenGL rendering on the webcam feed
    result = cv2.addWeighted(frame, 0.7, image_opengl, 0.3, 0)

    # Display the result
    cv2.imshow('Webcam with 3D Overlay', result)

    # Print OpenGL errors
    while glGetError() != GL_NO_ERROR:
        pass

    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            cap.release()
            cv2.destroyAllWindows()
            exit()

    # Swap the buffers
    pygame.display.flip()

    # Break the loop when 'q' is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break



# Release the camera and close the window
cap.release()
cv2.destroyAllWindows()
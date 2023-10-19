import pygame
import sys
import json

# Initialize pygame
pygame.init()

# Set up display
width, height = 800, 600
window_size = (width, height)
window = pygame.display.set_mode(window_size)
pygame.display.set_caption("Continuous Curve Drawer")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Variables
drawing = False
points = []  # List to store points of the curve

# Set the frame rate (frames per second)
FPS = 60
clock = pygame.time.Clock()

# Main game loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            # Save points to a JSON file before exiting
            with open("curve_points.json", "w") as file:
                json.dump(points, file)
            pygame.quit()
            sys.exit()

        # Check for mouse events
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # Left mouse button pressed
                drawing = True
                points.append([])  # Start a new segment of the curve
        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:  # Left mouse button released
                drawing = False

    # Capture points every frame if drawing is True
    if drawing:
        x, y = pygame.mouse.get_pos()
        if points:  # Ensure there is at least one segment
            points[-1].append((x, y))  # Add points to the last segment of the curve

    # Draw the curve
    window.fill(WHITE)
    for segment in points:
        if len(segment) > 1:
            pygame.draw.lines(window, BLACK, False, segment, 2)

    pygame.display.flip()

    # Limit frames per second
    clock.tick(FPS)

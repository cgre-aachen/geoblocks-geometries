import pygame
import sys
import json

# Initialize pygame
pygame.init()

# Set up display
width, height = 810, 610
window_size = (width, height)
window = pygame.display.set_mode(window_size)
pygame.display.set_caption("Please draw you layer")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Variables
drawing = False
points = []  # List to store points of the curve

# Set the frame rate (frames per second)
FPS = 15
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

    window.fill(WHITE)
    # Draw grid lines
    GRID_SIZE = 40  # Size of each grid cell
    TICK_SIZE = 10  # Size of the ticks on the axes
    LABEL_FONT = pygame.font.Font(None, 24)  # Font for the tick labels

    for x in range(0, width, GRID_SIZE):
        pygame.draw.line(window, BLACK, (x, 0), (x, height))
        if x % (GRID_SIZE * 5) == 0:  # Draw longer tick marks at every 5 grid cells
            pygame.draw.line(window, BLACK, (x, -TICK_SIZE), (x, TICK_SIZE))
            label = LABEL_FONT.render(str(x), True, BLACK)  # Create label text
            window.blit(label, (x - label.get_width() // 2, TICK_SIZE))

    for y in range(0, height, GRID_SIZE):
        pygame.draw.line(window, BLACK, (0, y), (width, y))
        if y % (GRID_SIZE * 5) == 0:  # Draw longer tick marks at every 5 grid cells
            pygame.draw.line(window, BLACK, (-TICK_SIZE, y), (TICK_SIZE, y))
            label = LABEL_FONT.render(str(y), True, BLACK)  # Create label text
            window.blit(label, (TICK_SIZE, y - label.get_height() // 2))


    # Draw the curve
    for segment in points:
        if len(segment) > 1:
            pygame.draw.lines(window, BLACK, False, segment, 2)

    pygame.display.flip()

    # Limit frames per second
    clock.tick(FPS)

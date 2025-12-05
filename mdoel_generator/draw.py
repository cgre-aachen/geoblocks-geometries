import pygame
import sys
import json
import tkinter.filedialog
from PyQt5.QtWidgets import QApplication, QFileDialog



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
background_image = None


# Set the frame rate (frames per second)
FPS = 15
clock = pygame.time.Clock()

# Main game loop
while True:
    window.fill(WHITE)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            # Save points to a JSON file before exiting
            with open("curve_points.json", "w") as file:
                json.dump(points, file)
            pygame.quit()
            sys.exit()

        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # Left mouse button pressed
                if upload_button_rect.collidepoint(event.pos):
                    drawing = False
                    # Open a file dialog for image selection
                    app = QApplication(sys.argv)
                    file_dialog = QFileDialog.getOpenFileName()[0]
                    if file_dialog:  # If a file is selected
                        background_image = pygame.image.load(file_dialog)
                        background_image = pygame.transform.scale(background_image, (width, height))

                elif upload_button_rect.collidepoint(event.pos) == False:                      
                    drawing = True
                    points.append([])  # Start a new segment of the curve
        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:  # Left mouse button released
                drawing = False
    # Draw the background image if available
    if background_image:
        window.blit(background_image, (0, 0))            

    # Capture points every frame if drawing is True
    if drawing:
        x, y = pygame.mouse.get_pos()
        if points:  # Ensure there is at least one segment
            points[-1].append((x, y))  # Add points to the last segment of the curve

 


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


    # Draw the upload button
    upload_button_text = "Upload Image"
    upload_button_font = pygame.freetype.Font(None, 24)
    upload_button_surface, upload_button_rect = upload_button_font.render(upload_button_text, BLACK)
    upload_button_rect.topleft = (20, 20)
    window.blit(upload_button_surface, upload_button_rect)


    # Draw the curve
    for segment in points:
        if len(segment) > 1:
            pygame.draw.lines(window, BLACK, False, segment, 6)

    pygame.display.flip()

    # Limit frames per second
    clock.tick(FPS)

"""
Interactive drawing interface for geological boundary definition.

This module provides a pygame-based interface for drawing geological boundaries
and curves that can be used for NURBS-based geological modeling.
"""

import pygame
import pygame.freetype
import sys
import json
import os
from pathlib import Path
from typing import List, Tuple, Optional
from PyQt5.QtWidgets import QApplication, QFileDialog


class DrawingInterface:
    """Interactive drawing interface for geological curves."""
    
    # Display configuration
    DEFAULT_WIDTH = 810
    DEFAULT_HEIGHT = 610
    FPS = 15
    
    # Colors
    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)
    
    # Grid configuration
    GRID_SIZE = 40
    TICK_SIZE = 10
    
    def __init__(self, width: int = DEFAULT_WIDTH, height: int = DEFAULT_HEIGHT):
        """Initialize the drawing interface."""
        self.width = width
        self.height = height
        self.window_size = (width, height)
        self.drawing = False
        self.points: List[List[Tuple[int, int]]] = []
        self.background_image: Optional[pygame.Surface] = None
        
        # Initialize pygame
        pygame.init()
        self.window = pygame.display.set_mode(self.window_size)
        pygame.display.set_caption("Draw your geological layer")
        self.clock = pygame.time.Clock()
        
        # Initialize fonts (create once, not in loop)
        self.label_font = pygame.font.Font(None, 24)
        self.upload_button_font = pygame.freetype.Font(None, 24)
        
        # Initialize upload button
        self._setup_upload_button()
    
    def _setup_upload_button(self) -> None:
        """Initialize the upload button."""
        upload_button_text = "Upload Image"
        self.upload_button_surface, self.upload_button_rect = (
            self.upload_button_font.render(upload_button_text, self.BLACK)
        )
        self.upload_button_rect.topleft = (20, 20)
    
    def _load_background_image(self) -> None:
        """Load a background image through file dialog."""
        try:
            # Create QApplication if it doesn't exist
            app = QApplication.instance()
            if app is None:
                app = QApplication(sys.argv)
            
            file_dialog_result = QFileDialog.getOpenFileName(
                None, 
                "Select Background Image",
                "",
                "Image Files (*.png *.jpg *.jpeg *.bmp *.gif)"
            )
            
            file_path = file_dialog_result[0]
            if file_path:
                # Validate file exists and is readable
                if not os.path.isfile(file_path):
                    print(f"Error: File {file_path} not found")
                    return
                
                # Load and scale image
                try:
                    self.background_image = pygame.image.load(file_path)
                    self.background_image = pygame.transform.scale(
                        self.background_image, 
                        (self.width, self.height)
                    )
                except pygame.error as e:
                    print(f"Error loading image: {e}")
                    self.background_image = None
                    
        except Exception as e:
            print(f"Error in file dialog: {e}")
    
    def _save_points(self, filename: str = "curve_points.json") -> None:
        """Save curve points to JSON file with error handling."""
        try:
            # Ensure the directory exists
            output_path = Path(filename).resolve()
            output_path.parent.mkdir(parents=True, exist_ok=True)
            
            with open(output_path, "w") as file:
                json.dump(self.points, file, indent=2)
            print(f"Points saved to {output_path}")
            
        except (IOError, OSError) as e:
            print(f"Error saving points to {filename}: {e}")
        except Exception as e:
            print(f"Unexpected error saving points: {e}")
    
    def _handle_mouse_down(self, event: pygame.event.Event) -> None:
        """Handle mouse button down events."""
        if event.button == 1:  # Left mouse button
            if self.upload_button_rect.collidepoint(event.pos):
                self.drawing = False
                self._load_background_image()
            else:
                self.drawing = True
                self.points.append([])  # Start a new curve segment
    
    def _handle_mouse_up(self, event: pygame.event.Event) -> None:
        """Handle mouse button up events."""
        if event.button == 1:  # Left mouse button
            self.drawing = False
    
    def _capture_drawing_point(self) -> None:
        """Capture mouse position if currently drawing."""
        if self.drawing and self.points:
            x, y = pygame.mouse.get_pos()
            self.points[-1].append((x, y))
    
    def _draw_grid(self) -> None:
        """Draw grid lines and axis labels."""
        # Draw vertical lines
        for x in range(0, self.width, self.GRID_SIZE):
            pygame.draw.line(self.window, self.BLACK, (x, 0), (x, self.height))
            
            # Draw tick marks and labels at every 5th grid line
            if x % (self.GRID_SIZE * 5) == 0:
                pygame.draw.line(
                    self.window, self.BLACK, 
                    (x, -self.TICK_SIZE), (x, self.TICK_SIZE)
                )
                label = self.label_font.render(str(x), True, self.BLACK)
                self.window.blit(label, (x - label.get_width() // 2, self.TICK_SIZE))
        
        # Draw horizontal lines
        for y in range(0, self.height, self.GRID_SIZE):
            pygame.draw.line(self.window, self.BLACK, (0, y), (self.width, y))
            
            # Draw tick marks and labels at every 5th grid line
            if y % (self.GRID_SIZE * 5) == 0:
                pygame.draw.line(
                    self.window, self.BLACK, 
                    (-self.TICK_SIZE, y), (self.TICK_SIZE, y)
                )
                label = self.label_font.render(str(y), True, self.BLACK)
                self.window.blit(
                    label, (self.TICK_SIZE, y - label.get_height() // 2)
                )
    
    def _draw_curves(self) -> None:
        """Draw all curve segments."""
        for segment in self.points:
            if len(segment) > 1:
                pygame.draw.lines(self.window, self.BLACK, False, segment, 6)
    
    def _draw_background(self) -> None:
        """Draw background image if available."""
        if self.background_image:
            self.window.blit(self.background_image, (0, 0))
    
    def _draw_ui(self) -> None:
        """Draw user interface elements."""
        self.window.blit(self.upload_button_surface, self.upload_button_rect)
    
    def run(self) -> None:
        """Run the main drawing interface loop."""
        try:
            while True:
                # Fill background
                self.window.fill(self.WHITE)
                
                # Handle events
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        self._save_points()
                        return
                    elif event.type == pygame.MOUSEBUTTONDOWN:
                        self._handle_mouse_down(event)
                    elif event.type == pygame.MOUSEBUTTONUP:
                        self._handle_mouse_up(event)
                
                # Capture drawing points
                self._capture_drawing_point()
                
                # Draw everything
                self._draw_background()
                self._draw_grid()
                self._draw_curves()
                self._draw_ui()
                
                # Update display
                pygame.display.flip()
                self.clock.tick(self.FPS)
                
        except KeyboardInterrupt:
            print("Drawing interface interrupted by user")
        except Exception as e:
            print(f"Error in drawing interface: {e}")
        finally:
            pygame.quit()


def main() -> None:
    """Main entry point for the drawing interface."""
    interface = DrawingInterface()
    interface.run()


if __name__ == "__main__":
    main()
"""Background management for the asteroids game."""

import os
import pygame
import random
from typing import Optional, List

from ..game.constants import (
    SCREEN_WIDTH,
    SCREEN_HEIGHT
)

# Loading screen uses the Trifid Nebula
LOADING_BACKGROUND_PATH = os.path.join("assets", "images", "Trifid_Nebula_by_Deddy_Dayag.jpg")

# Image extensions to look for
SUPPORTED_EXTENSIONS = ('.jpg', '.jpeg', '.png', '.bmp', '.tga')

def get_available_background_images() -> List[str]:
    """
    Dynamically discover available background images, excluding the Trifid Nebula.
    
    Returns:
        List of image filenames available for game backgrounds
    """
    images_folder = os.path.join("assets", "images")
    trifid_filename = "Trifid_Nebula_by_Deddy_Dayag.jpg"
    
    available_images = []
    
    try:
        if os.path.exists(images_folder):
            for filename in os.listdir(images_folder):
                # Check if it's a supported image file
                if filename.lower().endswith(SUPPORTED_EXTENSIONS):
                    # Exclude the Trifid Nebula (reserved for loading screen)
                    if filename != trifid_filename:
                        available_images.append(filename)
            
            available_images.sort()  # Sort for consistent ordering
            print(f"Found {len(available_images)} background images: {available_images}")
        else:
            print(f"Images folder not found: {images_folder}")
    
    except Exception as e:
        print(f"Error scanning for background images: {e}")
    
    return available_images


class BackgroundManager:
    """Manages the game background image."""
    
    def __init__(self):
        """Initialize the background manager."""
        self.background_surface: Optional[pygame.Surface] = None
        self.loading_background_surface: Optional[pygame.Surface] = None
        self.background_loaded = False
        self.selected_image_path: Optional[str] = None
        self.available_images: List[str] = []
    
    def _crop_and_scale_image(self, image_path: str, target_width: int, target_height: int) -> Optional[pygame.Surface]:
        """
        Load and crop an image to fit the target dimensions without stretching.
        
        Args:
            image_path: Path to the image file
            target_width: Target width
            target_height: Target height
            
        Returns:
            Cropped and scaled pygame surface, or None if loading fails
        """
        try:
            # Load the original image
            original_image = pygame.image.load(image_path)
            orig_width, orig_height = original_image.get_size()
            
            # Calculate aspect ratios
            target_ratio = target_width / target_height
            orig_ratio = orig_width / orig_height
            
            if orig_ratio > target_ratio:
                # Image is wider than target - crop horizontally
                new_height = orig_height
                new_width = int(orig_height * target_ratio)
                crop_x = (orig_width - new_width) // 2
                crop_y = 0
            else:
                # Image is taller than target - crop vertically  
                new_width = orig_width
                new_height = int(orig_width / target_ratio)
                crop_x = 0
                crop_y = (orig_height - new_height) // 2
            
            # Create cropped surface
            cropped_rect = pygame.Rect(crop_x, crop_y, new_width, new_height)
            cropped_surface = pygame.Surface((new_width, new_height))
            cropped_surface.blit(original_image, (0, 0), cropped_rect)
            
            # Scale to target size
            scaled_surface = pygame.transform.scale(cropped_surface, (target_width, target_height))
            
            return scaled_surface
            
        except Exception as e:
            print(f"Error processing image {image_path}: {e}")
            return None
    
    def _create_fallback_background(self) -> None:
        """Create a simple fallback background if image loading fails."""
        surface = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        
        # Dark space background with subtle gradient
        for y in range(SCREEN_HEIGHT):
            color_value = max(0, 20 - (y * 20 // SCREEN_HEIGHT))
            color = (color_value, color_value, color_value + 10)
            pygame.draw.line(surface, color, (0, y), (SCREEN_WIDTH, y))
            
        # Add some stars
        random.seed(42)  # Consistent star field
        for _ in range(200):
            x = random.randint(0, SCREEN_WIDTH)
            y = random.randint(0, SCREEN_HEIGHT)
            brightness = random.randint(100, 255)
            size = random.choice([1, 1, 1, 2])  # Mostly small stars
            color = (brightness, brightness, brightness)
            
            if size == 1:
                surface.set_at((x, y), color)
            else:
                pygame.draw.circle(surface, color, (x, y), size)
        
        self.background_surface = surface
        self.background_loaded = True
        print("Created fallback background")
    
    def initialize(self) -> None:
        """Initialize the background images."""
        # Discover available background images
        self.available_images = get_available_background_images()
        
        if not self.available_images:
            print("Warning: No background images found! Using fallback background.")
        
        # Load the loading screen background (always Trifid Nebula)
        self._load_loading_background()
        
        # Randomly select and load a game background
        self._load_random_game_background()
    
    def _load_loading_background(self) -> None:
        """Load the loading screen background (Trifid Nebula, uncropped)."""
        try:
            if os.path.exists(LOADING_BACKGROUND_PATH):
                # Load and scale Trifid without cropping (preserve aspect ratio)
                original_image = pygame.image.load(LOADING_BACKGROUND_PATH)
                self.loading_background_surface = pygame.transform.scale(
                    original_image, (SCREEN_WIDTH, SCREEN_HEIGHT)
                )
                print("Loading screen background loaded successfully (uncropped)")
            else:
                print(f"Loading background not found at {LOADING_BACKGROUND_PATH}")
        except Exception as e:
            print(f"Error loading loading background: {e}")
    
    def _load_random_game_background(self) -> None:
        """Randomly select and load a game background."""
        if not self.available_images:
            print("No background images available, using fallback")
            self._create_fallback_background()
            return
            
        # Randomly select an image from the available ones
        selected_image = random.choice(self.available_images)
        self.selected_image_path = os.path.join("assets", "images", selected_image)
        
        print(f"Randomly selected background: {selected_image}")
        
        try:
            if os.path.exists(self.selected_image_path):
                # Load and crop the image properly
                self.background_surface = self._crop_and_scale_image(
                    self.selected_image_path, SCREEN_WIDTH, SCREEN_HEIGHT
                )
                
                if self.background_surface:
                    self.background_loaded = True
                    print("Game background loaded and cropped successfully")
                else:
                    raise Exception("Failed to process image")
            else:
                print(f"Selected background not found at {self.selected_image_path}")
                self._create_fallback_background()
        except Exception as e:
            print(f"Error loading game background: {e}")
            self._create_fallback_background()
    
    def render(self, screen: pygame.Surface) -> None:
        """Render the background to the screen."""
        if self.background_surface:
            screen.blit(self.background_surface, (0, 0))
        else:
            # Emergency fallback - just fill with black
            screen.fill((0, 0, 0))
    
    def is_background_ready(self) -> bool:
        """Check if the background is ready to use."""
        return self.background_loaded
    
    def get_loading_background(self) -> Optional[pygame.Surface]:
        """Get the loading screen background surface."""
        return self.loading_background_surface
    
    def regenerate_background(self) -> None:
        """Select and load a new random background."""
        print("Regenerating background...")
        self._load_random_game_background()

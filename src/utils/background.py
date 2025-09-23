"""Background management for the asteroids game."""

import os
import pygame
import subprocess
import sys
import threading
import time
from typing import Optional

from ..game.constants import (
    BACKGROUND_IMAGE_PATH,
    BACKGROUND_CACHE_PATH, 
    GENERATE_BACKGROUND_ON_STARTUP,
    BACKGROUND_SEED,
    FORCE_REGENERATE_BACKGROUND,
    NEBULA_THEME,
    BACKGROUND_GENERATION_TIMEOUT,
    SCREEN_WIDTH,
    SCREEN_HEIGHT
)


class BackgroundManager:
    """Manages the game background image with loading screen support."""
    
    def __init__(self):
        """Initialize the background manager."""
        self.background_surface: Optional[pygame.Surface] = None
        self.loading_surface: Optional[pygame.Surface] = None
        self.background_loaded = False
        self.is_generating = False
        self.generation_complete = False
        self.generation_thread = None
        
    def _create_loading_screen(self) -> pygame.Surface:
        """Create a loading screen with title and previous background."""
        loading_surface = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        
        # Try to load previous background as loading screen
        if os.path.exists(BACKGROUND_CACHE_PATH):
            try:
                bg_img = pygame.image.load(BACKGROUND_CACHE_PATH)
                bg_scaled = pygame.transform.scale(bg_img, (SCREEN_WIDTH, SCREEN_HEIGHT))
                loading_surface.blit(bg_scaled, (0, 0))
            except:
                # Fallback to simple gradient
                self._create_fallback_background_on_surface(loading_surface)
        else:
            # No previous background, use simple gradient
            self._create_fallback_background_on_surface(loading_surface)
        
        # Add dark overlay for text readability
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        overlay.set_alpha(100)
        overlay.fill((0, 0, 0))
        loading_surface.blit(overlay, (0, 0))
        
        # Add title text
        try:
            title_font = pygame.font.Font(None, 120)
            subtitle_font = pygame.font.Font(None, 48)
            
            # Main title
            title_text = title_font.render("ASTEROIDS", True, (255, 255, 255))
            title_rect = title_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 50))
            loading_surface.blit(title_text, title_rect)
            
            # Loading subtitle
            loading_text = subtitle_font.render("Generating nebula...", True, (200, 200, 255))
            loading_rect = loading_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 50))
            loading_surface.blit(loading_text, loading_rect)
            
        except:
            # Fallback if font loading fails
            pass
        
        return loading_surface
    
    def _create_fallback_background_on_surface(self, surface: pygame.Surface) -> None:
        """Create a simple fallback background directly on a surface."""
        # Dark space background with subtle gradient
        for y in range(SCREEN_HEIGHT):
            color_value = max(0, 15 - (y * 15 // SCREEN_HEIGHT))
            color = (color_value, color_value, color_value + 5)
            pygame.draw.line(surface, color, (0, y), (SCREEN_WIDTH, y))
    
    def _generate_background_threaded(self) -> None:
        """Generate background in a separate thread."""
        try:
            success = self._generate_background()
            if success:
                # Cache the new background for next time
                if os.path.exists(BACKGROUND_IMAGE_PATH):
                    # Copy current background to cache
                    import shutil
                    shutil.copy2(BACKGROUND_IMAGE_PATH, BACKGROUND_CACHE_PATH)
                
                # Load the new background
                if self._load_background_image():
                    self.generation_complete = True
        except Exception as e:
            print(f"Background generation failed: {e}")
        finally:
            self.is_generating = False
    
    def _generate_background(self) -> bool:
        """
        Generate a new nebula background using the image generation tool.
        
        Returns:
            True if generation was successful, False otherwise.
        """
        try:
            # Path to the nebula generator
            generator_path = os.path.join("tools", "image_generation", "create_nebula.py")
            
            if not os.path.exists(generator_path):
                print(f"Warning: Nebula generator not found at {generator_path}")
                return False
            
            # Build command
            cmd = [
                sys.executable, generator_path,
                "--width", str(SCREEN_WIDTH),
                "--height", str(SCREEN_HEIGHT),
                "--output", BACKGROUND_IMAGE_PATH
            ]
            
            # Add seed if specified
            if BACKGROUND_SEED is not None:
                cmd.extend(["--seed", str(BACKGROUND_SEED)])
            
            # Add theme
            if NEBULA_THEME is not None:
                cmd.extend(["--theme", NEBULA_THEME])
                print(f"Generating {NEBULA_THEME} themed nebula background...")
            else:
                # Random theme selection
                import random
                themes = ['default', 'fire', 'ice', 'alien', 'sunset']
                chosen_theme = random.choice(themes)
                cmd.extend(["--theme", chosen_theme])
                print(f"Generating random {chosen_theme} themed nebula background...")
            
            # Run the generator with timeout
            result = subprocess.run(
                cmd, 
                capture_output=True, 
                text=True, 
                cwd=".",
                timeout=BACKGROUND_GENERATION_TIMEOUT
            )
            
            if result.returncode == 0:
                print("Nebula background generated successfully!")
                return True
            else:
                print(f"Error generating background: {result.stderr}")
                return False
                
        except subprocess.TimeoutExpired:
            print(f"Background generation timed out after {BACKGROUND_GENERATION_TIMEOUT} seconds")
            return False
        except Exception as e:
            print(f"Failed to generate background: {e}")
            return False
    
    def _load_background_image(self) -> bool:
        """
        Load the background image from file.
        
        Returns:
            True if loading was successful, False otherwise.
        """
        try:
            if not os.path.exists(BACKGROUND_IMAGE_PATH):
                print(f"Background image not found at {BACKGROUND_IMAGE_PATH}")
                return False
            
            # Load and scale the image
            background_img = pygame.image.load(BACKGROUND_IMAGE_PATH)
            self.background_surface = pygame.transform.scale(
                background_img, 
                (SCREEN_WIDTH, SCREEN_HEIGHT)
            )
            
            print("Background image loaded successfully!")
            return True
            
        except Exception as e:
            print(f"Error loading background image: {e}")
            return False
    
    def _create_fallback_background(self) -> None:
        """Create a simple fallback background if image generation fails."""
        print("Creating fallback background...")
        
        # Create a simple gradient background
        self.background_surface = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        self._create_fallback_background_on_surface(self.background_surface)
    
    def initialize(self) -> None:
        """Initialize the background system."""
        # Ensure assets directory exists
        os.makedirs(os.path.dirname(BACKGROUND_IMAGE_PATH), exist_ok=True)
        
        # Try to load existing background for immediate display
        if os.path.exists(BACKGROUND_IMAGE_PATH):
            if self._load_background_image():
                self.background_loaded = True
                print("Background image loaded successfully!")
        
        # If no background exists, create fallback
        if not self.background_loaded:
            self._create_fallback_background()
            self.background_loaded = True
        
        # Start background generation in thread if needed
        should_generate = (GENERATE_BACKGROUND_ON_STARTUP and 
                          (FORCE_REGENERATE_BACKGROUND or 
                           BACKGROUND_SEED is None))
        
        if should_generate:
            print("Starting background generation in thread...")
            self.is_generating = True
            self.generation_thread = threading.Thread(target=self._generate_background_threaded)
            self.generation_thread.daemon = True
            self.generation_thread.start()
    
    def render(self, screen: pygame.Surface) -> None:
        """
        Render the appropriate background to the screen.
        
        Args:
            screen: The pygame surface to render to.
        """
        if self.generation_complete and self.background_surface:
            # Switch to new background when generation is complete
            screen.blit(self.background_surface, (0, 0))
            # Mark as no longer generating
            if self.is_generating:
                self.is_generating = False
                print("New background loaded!")
        elif self.background_surface and self.background_loaded:
            # Show current background
            screen.blit(self.background_surface, (0, 0))
        else:
            # Emergency fallback - fill with black
            screen.fill((0, 0, 0))
    
    def is_background_generating(self) -> bool:
        """Check if background is currently being generated."""
        return self.is_generating
    
    def is_generation_complete(self) -> bool:
        """Check if new background generation is complete."""
        return self.generation_complete
    
    def get_generation_status(self) -> str:
        """Get a human-readable generation status."""
        if self.is_generating:
            return "Generating new nebula..."
        elif self.generation_complete:
            return "New background ready!"
        else:
            return "Background ready"
    
    def is_generation_complete(self) -> bool:
        """Check if background generation is complete."""
        return not getattr(self, 'is_generating', False)
    
    def use_fallback(self) -> None:
        """Force use of fallback background and stop generation."""
        if hasattr(self, 'is_generating'):
            self.is_generating = False
        if not self.background_loaded:
            self._create_fallback_background()
            self.background_loaded = True
    
    def regenerate_background(self, new_seed: Optional[int] = None) -> bool:
        """
        Regenerate the background with a new seed.
        
        Args:
            new_seed: Optional seed for reproducible generation.
            
        Returns:
            True if regeneration was successful.
        """
        # Temporarily override the seed by modifying the constants module
        from ..game import constants
        original_seed = constants.BACKGROUND_SEED
        
        if new_seed is not None:
            constants.BACKGROUND_SEED = new_seed
        
        try:
            success = self._generate_background() and self._load_background_image()
            return success
        finally:
            # Restore original seed
            if new_seed is not None:
                constants.BACKGROUND_SEED = original_seed

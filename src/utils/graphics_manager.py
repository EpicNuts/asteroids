"""Graphics mode management system for switching visual styles during gameplay."""

from enum import Enum
import pygame
from typing import Optional


class GraphicsMode(Enum):
    """Different graphics modes available in the game."""
    BASIC = "basic"           # Original simple shapes (circles, triangles)
    SPRITES = "sprites"       # High-quality sprite-based graphics
    MINIMAL = "minimal"       # Minimal wireframe style


class GraphicsManager:
    """Manages graphics mode switching and visual style consistency."""
    
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(GraphicsManager, cls).__new__(cls)
        return cls._instance
    
    def __init__(self):
        if hasattr(self, 'initialized'):
            return
        
        self.initialized = True
        self._current_mode = GraphicsMode.SPRITES  # Start with sprites
        self._ship_sprite = None
        self._ship_sprite_loaded = False
        
        # Visual style definitions
        self.styles = {
            GraphicsMode.BASIC: {
                'ship_color': (150, 150, 255),
                'ship_outline': 'white',
                'asteroid_color': (150, 100, 80),
                'asteroid_outline': (100, 70, 50),
                'shot_color': (255, 255, 100),
                'background': 'black',
                'use_sprites': False,
                'show_background_image': False,
                'wireframe_only': False
            },
            GraphicsMode.SPRITES: {
                'ship_color': (150, 150, 255),  # Fallback color
                'ship_outline': 'white',
                'asteroid_color': (150, 100, 80),  # Fallback color
                'asteroid_outline': (100, 70, 50),
                'shot_color': (255, 255, 100),
                'background': 'space_image',
                'use_sprites': True,
                'show_background_image': True,
                'wireframe_only': False
            },
            GraphicsMode.MINIMAL: {
                'ship_color': (100, 255, 100),    # Green wireframe
                'ship_outline': (100, 255, 100),  # Same color for consistency
                'asteroid_color': (255, 100, 100), # Red wireframe
                'asteroid_outline': (255, 100, 100), # Same color for consistency
                'shot_color': (255, 255, 100),    # Yellow wireframe
                'background': 'black',
                'use_sprites': False,
                'show_background_image': False,
                'wireframe_only': True  # Key difference - wireframes only
            }
        }
        
        # Load ship sprite after pygame is initialized
        # self._load_ship_sprite()  # Will be called later via initialize()
    
    def initialize(self):
        """Initialize graphics manager after pygame is ready."""
        if not self._ship_sprite_loaded:
            self._load_ship_sprite()
    
    def _load_ship_sprite(self):
        """Load the ship sprite image."""
        try:
            ship_path = "assets/ships/yct20hubfk061.png"
            self._ship_sprite = pygame.image.load(ship_path).convert_alpha()
            self._ship_sprite_loaded = True
            print(f"Ship sprite loaded: {ship_path}")
        except Exception as e:
            print(f"Could not load ship sprite: {e}")
            self._ship_sprite_loaded = False
    
    def get_current_mode(self) -> GraphicsMode:
        """Get the current graphics mode."""
        return self._current_mode
    
    def set_mode(self, mode: GraphicsMode):
        """Set the graphics mode."""
        if mode in GraphicsMode:
            self._current_mode = mode
            print(f"Graphics mode changed to: {mode.value}")
    
    def cycle_mode(self):
        """Cycle to the next graphics mode."""
        modes = list(GraphicsMode)
        current_index = modes.index(self._current_mode)
        next_index = (current_index + 1) % len(modes)
        self.set_mode(modes[next_index])
    
    def should_use_sprites(self) -> bool:
        """Check if current mode should use sprite-based rendering."""
        return self.styles[self._current_mode]['use_sprites']
    
    def should_show_background_image(self) -> bool:
        """Check if current mode should show background images."""
        return self.styles[self._current_mode]['show_background_image']
    
    def is_wireframe_only(self) -> bool:
        """Check if current mode should only draw wireframes (no fills)."""
        return self.styles[self._current_mode].get('wireframe_only', False)
    
    def get_ship_sprite(self) -> Optional[pygame.Surface]:
        """Get the ship sprite if available and mode supports it."""
        if self.should_use_sprites() and self._ship_sprite_loaded:
            return self._ship_sprite
        return None
    
    def get_style(self, element: str):
        """Get style property for current mode."""
        return self.styles[self._current_mode].get(element)
    
    def get_ship_color(self) -> tuple:
        """Get ship color for current graphics mode."""
        return self.get_style('ship_color')
    
    def get_ship_outline_color(self):
        """Get ship outline color for current graphics mode."""
        return self.get_style('ship_outline')
    
    def get_asteroid_color(self) -> tuple:
        """Get asteroid color for current graphics mode."""
        return self.get_style('asteroid_color')
    
    def get_asteroid_outline_color(self) -> tuple:
        """Get asteroid outline color for current graphics mode."""
        return self.get_style('asteroid_outline')
    
    def get_shot_color(self) -> tuple:
        """Get shot color for current graphics mode."""
        return self.get_style('shot_color')
    
    def get_background_color(self) -> tuple:
        """Get background color for current graphics mode."""
        bg = self.get_style('background')
        if bg == 'black':
            return (0, 0, 0)
        elif bg == 'space_image':
            return (5, 5, 15)  # Deep space fallback
        return (0, 0, 0)


# Global instance
graphics_manager = GraphicsManager()

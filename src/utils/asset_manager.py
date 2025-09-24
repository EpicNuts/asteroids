"""Asset management system for efficient loading and caching of game resources."""

import os
import pygame
import threading
from typing import Dict, List, Optional, Tuple
import time


class AssetManager:
    """Centralized asset management system with preloading and caching."""
    
    _instance = None
    _lock = threading.Lock()
    
    def __new__(cls):
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = super(AssetManager, cls).__new__(cls)
        return cls._instance
    
    def __init__(self):
        if hasattr(self, 'initialized'):
            return
        
        self.initialized = True
        self._sprite_cache: Dict[str, List[pygame.Surface]] = {}
        self._loading_complete = False
        self._loading_progress = 0
        self._total_assets = 0
        self._loaded_assets = 0
        
        # Asset definitions
        self.asteroid_variants = {
            "large": ["a1", "a3", "b1", "b3", "c1", "c3", "c4"],
            "medium": ["a1", "a3", "a4", "b4", "c1", "c3", "c4", "d1", "d3", "d4"],
            "small": ["a1", "a3", "a4", "b1", "b3", "b4"]
        }
        
        # Pre-calculate total assets for progress tracking
        for size_variants in self.asteroid_variants.values():
            self._total_assets += len(size_variants)
    
    def preload_assets_async(self):
        """Start asynchronous preloading of all game assets."""
        def load_worker():
            self._preload_asteroid_sprites()
            self._loading_complete = True
        
        thread = threading.Thread(target=load_worker, daemon=True)
        thread.start()
        return thread
    
    def _preload_asteroid_sprites(self):
        """Preload all asteroid sprite animations."""
        start_time = time.time()
        
        for size, variants in self.asteroid_variants.items():
            for variant in variants:
                self._load_asteroid_variant(size, variant)
                self._loaded_assets += 1
                self._loading_progress = self._loaded_assets / self._total_assets
        
        load_time = time.time() - start_time
        print(f"Asteroid sprites preloaded in {load_time:.2f}s")
    
    def _load_asteroid_variant(self, size: str, variant: str):
        """Load a specific asteroid variant's animation frames."""
        cache_key = f"{size}_{variant}"
        
        if cache_key in self._sprite_cache:
            return
        
        frames = []
        base_path = os.path.join("assets", "asteroids", size)
        
        # Quick existence check first
        first_frame = os.path.join(base_path, f"{variant}0000.png")
        if not os.path.exists(first_frame):
            print(f"Warning: Variant {variant} not found in {size} asteroids")
            return
        
        # Load all 16 frames
        for i in range(16):
            filename = f"{variant}{i:04d}.png"
            filepath = os.path.join(base_path, filename)
            
            try:
                if os.path.exists(filepath):
                    # Load and convert immediately for performance
                    surface = pygame.image.load(filepath).convert_alpha()
                    frames.append(surface)
                else:
                    print(f"Warning: Frame {i} missing for {cache_key}")
                    break
            except Exception as e:
                print(f"Error loading {filepath}: {e}")
                break
        
        if frames:
            self._sprite_cache[cache_key] = frames
        else:
            # Create fallback frames
            radius = self._get_size_radius(size)
            fallback_frames = self._create_fallback_frames(radius)
            self._sprite_cache[cache_key] = fallback_frames
    
    def _get_size_radius(self, size: str) -> int:
        """Get radius for asteroid size."""
        size_map = {
            "large": 40,
            "medium": 25,
            "small": 15
        }
        return size_map.get(size, 40)
    
    def _create_fallback_frames(self, radius: int) -> List[pygame.Surface]:
        """Create fallback animation frames for missing sprites."""
        frames = []
        colors = [
            (150, 100, 80),  # Brown
            (120, 80, 60),   # Dark brown
            (180, 120, 100), # Light brown
            (100, 70, 50)    # Very dark brown
        ]
        
        for i in range(16):
            surface = pygame.Surface((radius * 2, radius * 2), pygame.SRCALPHA)
            color = colors[i % len(colors)]
            pygame.draw.circle(surface, color, (radius, radius), radius)
            
            # Add some texture variation
            for j in range(3):
                offset_x = (i + j * 5) % (radius // 2)
                offset_y = (i * 2 + j) % (radius // 2)
                small_radius = radius // 4
                pygame.draw.circle(surface, 
                                 tuple(max(0, c - 30) for c in color),
                                 (radius + offset_x - radius//4, radius + offset_y - radius//4),
                                 small_radius)
            
            frames.append(surface)
        
        return frames
    
    def get_asteroid_frames(self, size: str, variant: str) -> List[pygame.Surface]:
        """Get cached asteroid animation frames."""
        cache_key = f"{size}_{variant}"
        
        if cache_key in self._sprite_cache:
            return self._sprite_cache[cache_key]
        
        # If not cached, create simple fallback immediately
        print(f"Warning: {cache_key} not preloaded, creating fallback")
        radius = self._get_size_radius(size)
        fallback_frames = self._create_fallback_frames(radius)
        self._sprite_cache[cache_key] = fallback_frames
        return fallback_frames
    
    def is_loading_complete(self) -> bool:
        """Check if asset preloading is complete."""
        return self._loading_complete
    
    def get_loading_progress(self) -> float:
        """Get loading progress (0.0 to 1.0)."""
        return self._loading_progress
    
    def get_available_variants(self, size: str) -> List[str]:
        """Get available variants for an asteroid size."""
        return self.asteroid_variants.get(size, [])


# Global instance
asset_manager = AssetManager()

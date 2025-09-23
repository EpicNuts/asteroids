#!/usr/bin/env python3
"""
Procedural nebula background generator for the asteroids game.

This tool creates eerie, space-like nebula backgrounds using:
- Perlin noise-like patterns
- Multiple color layers
- Gradient blending
- Random star fields

Usage:
    python create_nebula.py --width 800 --height 600 --output nebula.png
"""

import argparse
import math
import random
from typing import Tuple, List
from PIL import Image, ImageDraw, ImageFilter
import numpy as np


class NebulaGenerator:
    """Generates procedural nebula background images."""
    
    def __init__(self, width: int = 800, height: int = 600, seed: int = None):
        """
        Initialize the nebula generator.
        
        Args:
            width: Image width in pixels
            height: Image height in pixels
            seed: Random seed for reproducible results
        """
        self.width = width
        self.height = height
        if seed is not None:
            random.seed(seed)
            np.random.seed(seed)
    
    def _noise_2d(self, x: float, y: float, scale: float = 1.0) -> float:
        """
        Generate 2D noise using a simple hash-based approach.
        This creates organic, cloud-like patterns.
        """
        # Simple hash-based noise
        x_scaled = x * scale
        y_scaled = y * scale
        
        # Hash the coordinates
        hash_val = hash((int(x_scaled * 12.9898), int(y_scaled * 78.233))) % 2**32
        return (hash_val / 2**32) * 2 - 1
    
    def _turbulence(self, x: float, y: float, size: float) -> float:
        """
        Generate turbulence using multiple octaves of noise.
        Creates swirling, flowing patterns like real gas dynamics.
        """
        value = 0.0
        initial_size = size
        
        while size >= 1:
            value += abs(self._noise_2d(x / size, y / size)) * size
            size /= 2.0
            
        return value / initial_size
    
    def _create_flow_field(self, scale: float = 32.0) -> np.ndarray:
        """Create a flow field that simulates gas movement and turbulence."""
        flow_x = np.zeros((self.height, self.width))
        flow_y = np.zeros((self.height, self.width))
        
        for y in range(self.height):
            for x in range(self.width):
                # Generate angle based on noise
                angle = self._turbulence(x, y, scale) * 2 * math.pi
                flow_x[y, x] = math.cos(angle)
                flow_y[y, x] = math.sin(angle)
        
        return flow_x, flow_y
    
    def _create_density_field(self, num_seeds: int = 3) -> np.ndarray:
        """
        Create a density field with flowing, organic structures.
        Optimized for performance with larger images.
        """
        density = np.zeros((self.height, self.width))
        
        # Create flow field for gas movement (lower resolution for speed)
        flow_scale = max(32.0, min(self.width, self.height) / 20)
        flow_x, flow_y = self._create_flow_field(flow_scale)
        
        # Place seed points for gas concentration
        seeds = []
        for _ in range(num_seeds):
            seed_x = random.randint(int(self.width * 0.1), int(self.width * 0.9))
            seed_y = random.randint(int(self.height * 0.1), int(self.height * 0.9))
            intensity = random.uniform(0.8, 1.0)
            seeds.append((seed_x, seed_y, intensity))
        
        # Reduce particle count for larger images
        particles_per_seed = max(200, 1000 - (self.width * self.height // 1000))
        max_steps = max(50, 150 - (self.width * self.height // 5000))
        
        # Flow particles from seeds to create organic structures
        for seed_x, seed_y, intensity in seeds:
            for _ in range(particles_per_seed):
                x, y = float(seed_x), float(seed_y)
                current_intensity = intensity
                
                # Follow the flow field
                for step in range(max_steps):
                    if 0 <= int(x) < self.width and 0 <= int(y) < self.height:
                        # Add density at current position (simplified)
                        ix, iy = int(x), int(y)
                        density[iy, ix] += current_intensity * 0.05
                        
                        # Move along flow field
                        flow_strength = 3.0
                        x += flow_x[iy, ix] * flow_strength
                        y += flow_y[iy, ix] * flow_strength
                        
                        # Add some turbulence
                        x += (random.random() - 0.5) * 1.0
                        y += (random.random() - 0.5) * 1.0
                        
                        # Decay intensity faster
                        current_intensity *= 0.95
                        if current_intensity < 0.02:
                            break
                    else:
                        break
        
        # Simple smoothing (much faster than full convolution)
        if self.width * self.height < 500000:  # Only smooth for smaller images
            smoothed = np.zeros_like(density)
            for y in range(1, self.height - 1):
                for x in range(1, self.width - 1):
                    smoothed[y, x] = (
                        density[y-1, x] + density[y+1, x] + 
                        density[y, x-1] + density[y, x+1] + 
                        density[y, x] * 2
                    ) / 6.0
            return smoothed
        else:
            return density
    
    def _create_nebula_layer(self, 
                           color: Tuple[int, int, int],
                           opacity: float = 0.8,
                           density_field: np.ndarray = None) -> Image.Image:
        """
        Create a single colored nebula layer using density field for realistic gas flow.
        
        Args:
            color: RGB color tuple
            opacity: Layer opacity (0.0 to 1.0)
            density_field: Pre-computed density field
        """
        if density_field is None:
            density_field = self._create_density_field()
        
        # Normalize density field
        max_density = np.max(density_field)
        if max_density > 0:
            density_field = density_field / max_density
        
        # Create image array
        img_array = np.zeros((self.height, self.width, 4), dtype=np.uint8)
        
        for y in range(self.height):
            for x in range(self.width):
                density = density_field[y, x]
                
                if density > 0.05:  # Only show areas with significant density
                    # Apply power curve for more dramatic contrast
                    alpha_factor = density ** 0.5  # Square root for softer falloff
                    
                    # Add some brightness variation based on density
                    brightness_factor = 0.7 + (density * 0.6)  # 0.7 to 1.3 range
                    
                    # Calculate final color
                    final_color = [
                        min(255, int(color[0] * brightness_factor)),
                        min(255, int(color[1] * brightness_factor)),
                        min(255, int(color[2] * brightness_factor))
                    ]
                    
                    alpha = min(255, int(alpha_factor * 255 * opacity))
                    img_array[y, x] = [final_color[0], final_color[1], final_color[2], alpha]
        
        return Image.fromarray(img_array, 'RGBA')
    
    def _create_star_field(self, num_stars: int = 200) -> Image.Image:
        """Create a random star field background."""
        img = Image.new('RGBA', (self.width, self.height), (0, 0, 0, 0))
        draw = ImageDraw.Draw(img)
        
        for _ in range(num_stars):
            x = random.randint(0, self.width - 1)
            y = random.randint(0, self.height - 1)
            
            # Random star brightness and size
            brightness = random.randint(100, 255)
            size = random.choice([1, 1, 1, 2])  # Mostly small stars
            
            if size == 1:
                draw.point((x, y), fill=(brightness, brightness, brightness, 255))
            else:
                draw.ellipse([x-1, y-1, x+1, y+1], fill=(brightness, brightness, brightness, 255))
        
        return img
    
    def _create_gradient_base(self) -> Image.Image:
        """Create a deep space background with subtle color variation."""
        img_array = np.zeros((self.height, self.width, 3), dtype=np.uint8)
        
        # Create a subtle radial gradient from center with deep space colors
        center_x, center_y = self.width // 2, self.height // 2
        max_distance = math.sqrt(center_x**2 + center_y**2)
        
        for y in range(self.height):
            for x in range(self.width):
                # Distance from center
                distance = math.sqrt((x - center_x)**2 + (y - center_y)**2)
                gradient_factor = 1.0 - (distance / max_distance)
                
                # Deep space colors with subtle purple/blue tint
                base_r = int(gradient_factor * 8 + 2)   # Very dark red
                base_g = int(gradient_factor * 5 + 1)   # Very dark green  
                base_b = int(gradient_factor * 12 + 4)  # Slightly more blue
                
                img_array[y, x] = [base_r, base_g, base_b]
        
        return Image.fromarray(img_array, 'RGB')
    
    def generate_nebula(self, 
                       colors: List[Tuple[int, int, int]] = None,
                       num_stars: int = 120,
                       theme: str = 'default') -> Image.Image:
        """
        Generate a complete nebula background image with flowing gas structures.
        
        Args:
            colors: List of RGB color tuples for nebula layers
            num_stars: Number of stars to add
            theme: Color theme ('default', 'fire', 'ice', 'alien', 'sunset')
            
        Returns:
            PIL Image of the generated nebula
        """
        if colors is None:
            # Choose colors based on theme - much more vibrant
            if theme == 'fire':
                colors = [
                    (255, 120, 20),   # Bright orange-red
                    (255, 180, 40),   # Golden orange
                    (255, 60, 10),    # Deep red-orange
                    (255, 220, 80),   # Bright yellow
                ]
            elif theme == 'ice':
                colors = [
                    (80, 180, 255),   # Bright blue
                    (120, 220, 255),  # Light blue
                    (40, 140, 255),   # Deep blue
                    (180, 240, 255),  # Pale cyan
                ]
            elif theme == 'alien':
                colors = [
                    (40, 255, 80),    # Bright green
                    (120, 255, 40),   # Yellow-green
                    (80, 255, 180),   # Cyan-green
                    (20, 200, 60),    # Forest green
                ]
            elif theme == 'sunset':
                colors = [
                    (255, 80, 120),   # Hot pink
                    (255, 140, 60),   # Orange
                    (180, 40, 180),   # Purple
                    (255, 180, 80),   # Peach
                ]
            else:  # default - dramatic space colors
                colors = [
                    (255, 120, 40),   # Bright orange (hydrogen)
                    (160, 40, 255),   # Bright purple (ionized gas)
                    (40, 255, 140),   # Bright cyan (oxygen)
                    (255, 200, 40),   # Bright yellow (sulfur)
                ]
        
        # Start with deep space gradient base
        result = self._create_gradient_base()
        result = result.convert('RGBA')
        
        # Add star field first (behind the gas)
        stars = self._create_star_field(num_stars)
        result = Image.alpha_composite(result, stars)
        
        # Create different density fields for each gas type
        print("Creating gas flow structures...")
        for i, color in enumerate(colors):
            # Each layer gets its own unique flow pattern
            density_field = self._create_density_field(num_seeds=2 + i)
            
            # Create the gas layer
            layer = self._create_nebula_layer(
                color=color,
                opacity=0.5 + (i * 0.1),  # Vary opacity slightly
                density_field=density_field
            )
            
            # Apply moderate blur for realistic gas diffusion
            blur_radius = 2 if self.width * self.height > 500000 else 4
            layer = layer.filter(ImageFilter.GaussianBlur(radius=blur_radius))
            result = Image.alpha_composite(result, layer)
        
        # Add fewer bright core regions for performance
        print("Adding bright emission cores...")
        for _ in range(1):
            core_density = self._create_density_field(num_seeds=1)
            core_color = random.choice(colors)
            
            # Make cores much brighter
            bright_color = tuple(min(255, int(c * 1.3)) for c in core_color)
            
            core_layer = self._create_nebula_layer(
                color=bright_color,
                opacity=0.3,
                density_field=core_density
            )
            
            # Less blur for sharper cores
            core_layer = core_layer.filter(ImageFilter.GaussianBlur(radius=1))
            result = Image.alpha_composite(result, core_layer)
        
        return result.convert('RGB')


def main():
    """Command line interface for nebula generation."""
    parser = argparse.ArgumentParser(description='Generate procedural nebula backgrounds')
    parser.add_argument('--width', type=int, default=800, help='Image width')
    parser.add_argument('--height', type=int, default=600, help='Image height')
    parser.add_argument('--output', type=str, default='nebula.png', help='Output filename')
    parser.add_argument('--seed', type=int, help='Random seed for reproducible results')
    parser.add_argument('--stars', type=int, default=150, help='Number of stars')
    parser.add_argument('--theme', type=str, choices=['default', 'fire', 'ice', 'alien', 'sunset'], 
                       default='default', help='Color theme')
    
    args = parser.parse_args()
    
    print(f"Generating {args.width}x{args.height} {args.theme} nebula background...")
    
    generator = NebulaGenerator(args.width, args.height, args.seed)
    nebula = generator.generate_nebula(num_stars=args.stars, theme=args.theme)
    
    nebula.save(args.output)
    print(f"Nebula saved as {args.output}")


if __name__ == '__main__':
    main()

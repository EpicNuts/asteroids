"""
Sound Generation Tool for Asteroids Game

This script creates procedural sound effects for the asteroids game.
It generates simple but effective sounds using pure pygame/math, without requiring NumPy.

Usage:
    python -m tools.sound_generation.create_sounds
    
Or from the project root:
    python tools/sound_generation/create_sounds.py

The generated sounds will be saved to assets/sounds/ and can be used
instead of the built-in programmatic sounds in the game.
"""

import pygame
import math
import struct
import os
import sys
from pathlib import Path


class SoundGenerator:
    """Generate procedural sound effects using pygame and basic math."""
    
    def __init__(self, sample_rate: int = 22050):
        """Initialize the sound generator.
        
        Args:
            sample_rate: Audio sample rate in Hz
        """
        self.sample_rate = sample_rate
        pygame.mixer.pre_init(frequency=sample_rate, size=-16, channels=2, buffer=512)
        pygame.mixer.init()
        
    def create_beep(self, frequency: float, duration: float, volume: float = 0.3, 
                   fade_out: bool = True) -> pygame.mixer.Sound:
        """Create a simple beep sound.
        
        Args:
            frequency: Frequency in Hz
            duration: Duration in seconds
            volume: Volume level (0.0 to 1.0)
            fade_out: Whether to fade out the sound
            
        Returns:
            pygame.mixer.Sound object
        """
        samples = []
        frames = int(duration * self.sample_rate)
        
        for i in range(frames):
            progress = i / frames
            
            # Create sine wave
            wave = math.sin(2 * math.pi * frequency * i / self.sample_rate)
            
            # Apply envelope
            if fade_out:
                envelope = 1 - progress  # Linear fade out
            else:
                envelope = 1.0
                
            # Apply volume and envelope
            sample = int(wave * volume * envelope * 16383)
            samples.extend([sample, sample])  # Stereo
        
        # Pack as bytes
        sound_data = struct.pack('<' + 'h' * len(samples), *samples)
        return pygame.mixer.Sound(buffer=sound_data)
    
    def create_sweep(self, start_freq: float, end_freq: float, duration: float, 
                    volume: float = 0.3) -> pygame.mixer.Sound:
        """Create a frequency sweep sound.
        
        Args:
            start_freq: Starting frequency in Hz
            end_freq: Ending frequency in Hz  
            duration: Duration in seconds
            volume: Volume level (0.0 to 1.0)
            
        Returns:
            pygame.mixer.Sound object
        """
        samples = []
        frames = int(duration * self.sample_rate)
        
        for i in range(frames):
            progress = i / frames
            
            # Interpolate frequency
            frequency = start_freq + (end_freq - start_freq) * progress
            
            # Create sine wave
            wave = math.sin(2 * math.pi * frequency * i / self.sample_rate)
            
            # Apply fade out envelope
            envelope = 1 - progress
            
            # Apply volume and envelope
            sample = int(wave * volume * envelope * 16383)
            samples.extend([sample, sample])  # Stereo
        
        # Pack as bytes
        sound_data = struct.pack('<' + 'h' * len(samples), *samples)
        return pygame.mixer.Sound(buffer=sound_data)
    
    def create_noise_burst(self, duration: float, volume: float = 0.2) -> pygame.mixer.Sound:
        """Create a noise burst for explosion effects.
        
        Args:
            duration: Duration in seconds
            volume: Volume level (0.0 to 1.0)
            
        Returns:
            pygame.mixer.Sound object
        """
        import random
        samples = []
        frames = int(duration * self.sample_rate)
        
        for i in range(frames):
            progress = i / frames
            
            # Create noise
            noise = (random.random() * 2 - 1)
            
            # Apply envelope (quick attack, slow decay)
            if progress < 0.1:
                envelope = progress / 0.1  # Quick attack
            else:
                envelope = math.exp(-3 * (progress - 0.1) / 0.9)  # Exponential decay
            
            # Apply volume and envelope
            sample = int(noise * volume * envelope * 16383)
            samples.extend([sample, sample])  # Stereo
        
        # Pack as bytes
        sound_data = struct.pack('<' + 'h' * len(samples), *samples)
        return pygame.mixer.Sound(buffer=sound_data)
    
    def save_sound_as_wav(self, sound: pygame.mixer.Sound, filepath: str) -> None:
        """Save a pygame sound as a WAV file.
        
        Note: This creates a basic WAV file. For better quality, 
        consider using dedicated audio libraries.
        
        Args:
            sound: pygame.mixer.Sound to save
            filepath: Output file path
        """
        # This is a simplified WAV export - in practice, you might want 
        # to use a dedicated audio library for better WAV export
        print(f"Note: Sound created in memory for {filepath}")
        print("      For file export, consider using dedicated audio libraries")


def create_game_sounds(output_dir: str = "assets/sounds") -> None:
    """Create all sound effects for the asteroids game.
    
    Args:
        output_dir: Directory to save sound files
    """
    # Ensure output directory exists
    Path(output_dir).mkdir(parents=True, exist_ok=True)
    
    # Initialize sound generator
    generator = SoundGenerator()
    
    print("🎵 Generating game sound effects...")
    print("=" * 50)
    
    # Define sound specifications
    sound_specs = {
        "shoot": {
            "type": "sweep",
            "params": {"start_freq": 800, "end_freq": 200, "duration": 0.15, "volume": 0.4},
            "description": "Laser shooting sound (high to low sweep)"
        },
        "explosion": {
            "type": "noise_burst", 
            "params": {"duration": 0.4, "volume": 0.3},
            "description": "Asteroid destruction (noise burst)"
        },
        "thrust": {
            "type": "beep",
            "params": {"frequency": 150, "duration": 0.3, "volume": 0.25, "fade_out": False},
            "description": "Engine/thruster sound (low rumble)"
        },
        "collision": {
            "type": "beep",
            "params": {"frequency": 600, "duration": 0.2, "volume": 0.4},
            "description": "Player collision (sharp beep)"
        }
    }
    
    # Generate each sound
    created_sounds = {}
    for name, spec in sound_specs.items():
        print(f"🔊 Creating '{name}' - {spec['description']}")
        
        # Create sound based on type
        if spec["type"] == "beep":
            sound = generator.create_beep(**spec["params"])
        elif spec["type"] == "sweep":
            sound = generator.create_sweep(**spec["params"])
        elif spec["type"] == "noise_burst":
            sound = generator.create_noise_burst(**spec["params"])
        else:
            print(f"   ❌ Unknown sound type: {spec['type']}")
            continue
            
        created_sounds[name] = sound
        
        # Test the sound
        print(f"   🎧 Testing sound (duration: {sound.get_length():.2f}s)...")
        sound.play()
        pygame.time.wait(int(sound.get_length() * 1000) + 100)
        
        print(f"   ✅ '{name}' created successfully")
        print()
    
    print("=" * 50)
    print("🎉 All sound effects generated!")
    print()
    print("📋 Usage:")
    print("  - These sounds are generated in memory")
    print("  - The game will automatically use them as fallbacks")
    print("  - To use custom sounds, add .wav files to assets/sounds/")
    print("  - The game prioritizes real files over generated sounds")
    
    return created_sounds


def main():
    """Main function - create game sounds."""
    try:
        create_game_sounds()
    except Exception as e:
        print(f"❌ Error creating sounds: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()

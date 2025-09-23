"""Sound management utilities."""

import pygame
import os
import struct
import math
import random
from typing import Dict, Optional


class SoundManager:
    """Manages game sound effects and music."""
    
    def __init__(self, master_volume: float = 0.7):
        """Initialize the sound manager.
        
        Args:
            master_volume: Master volume level (0.0 to 1.0)
        """
        # Initialize pygame mixer
        pygame.mixer.pre_init(frequency=22050, size=-16, channels=2, buffer=512)
        pygame.mixer.init()
        
        self.master_volume = master_volume
        self.sounds: Dict[str, pygame.mixer.Sound] = {}
        self.sound_volumes: Dict[str, float] = {}
        
    def _create_beep_sound(self, frequency: float, duration: float, volume: float = 0.3) -> pygame.mixer.Sound:
        """Create a simple beep sound programmatically."""
        sample_rate = 22050
        samples = []
        
        for i in range(int(duration * sample_rate)):
            # Sine wave with fade out
            progress = i / (duration * sample_rate)
            envelope = (1 - progress) if progress > 0.8 else 1.0  # Fade out in last 20%
            
            value = math.sin(2 * math.pi * frequency * i / sample_rate) * volume * envelope
            sample = int(value * 16383)
            samples.extend([sample, sample])  # Stereo
        
        sound_data = struct.pack('<' + 'h' * len(samples), *samples)
        return pygame.mixer.Sound(buffer=sound_data)
    
    def _create_noise_burst(self, duration: float, volume: float = 0.2) -> pygame.mixer.Sound:
        """Create a noise burst for explosion effects."""
        sample_rate = 22050
        samples = []
        
        for i in range(int(duration * sample_rate)):
            progress = i / (duration * sample_rate)
            
            # Envelope: quick attack, slow decay
            if progress < 0.1:
                envelope = progress / 0.1
            else:
                envelope = math.exp(-3 * (progress - 0.1) / 0.9)
            
            # Random noise
            value = (random.random() * 2 - 1) * volume * envelope
            sample = int(value * 16383)
            samples.extend([sample, sample])  # Stereo
        
        sound_data = struct.pack('<' + 'h' * len(samples), *samples)
        return pygame.mixer.Sound(buffer=sound_data)
    
    def create_default_sounds(self) -> None:
        """Create default sound effects programmatically."""
        print("Creating default sound effects...")
        
        # Create basic sound effects
        default_sounds = {
            "shoot": self._create_beep_sound(800, 0.15, 0.4),      # High pitched short beep
            "explosion": self._create_noise_burst(0.4, 0.3),       # Noise burst  
            "thrust": self._create_beep_sound(150, 0.3, 0.25),     # Low rumble
            "collision": self._create_beep_sound(600, 0.2, 0.4)    # Medium pitched beep
        }
        
        for name, sound in default_sounds.items():
            sound.set_volume(self.sound_volumes.get(name, 1.0) * self.master_volume)
            self.sounds[name] = sound
            print(f"Created sound: {name}")

    def load_sound(self, name: str, filepath: str, volume: float = 1.0) -> bool:
        """Load a sound effect from file, or create default if file doesn't exist.
        
        Args:
            name: Internal name for the sound
            filepath: Path to the sound file
            volume: Volume level for this specific sound (0.0 to 1.0)
            
        Returns:
            True if sound loaded successfully, False otherwise
        """
        self.sound_volumes[name] = volume
        
        try:
            if os.path.exists(filepath):
                sound = pygame.mixer.Sound(filepath)
                sound.set_volume(volume * self.master_volume)
                self.sounds[name] = sound
                print(f"Loaded sound from file: {name}")
                return True
            else:
                print(f"Sound file not found: {filepath}, creating default sound")
                # Create default sound effect
                if name == "shoot":
                    sound = self._create_beep_sound(800, 0.15, 0.4)
                elif name == "explosion":
                    sound = self._create_noise_burst(0.4, 0.3)
                elif name == "thrust":
                    sound = self._create_beep_sound(150, 0.3, 0.25)
                elif name == "collision":
                    sound = self._create_beep_sound(600, 0.2, 0.4)
                else:
                    # Generic beep for unknown sounds
                    sound = self._create_beep_sound(440, 0.2, 0.3)
                
                sound.set_volume(volume * self.master_volume)
                self.sounds[name] = sound
                print(f"Created default sound: {name}")
                return True
                
        except Exception as e:
            print(f"Error loading sound {name}: {e}")
            self.sounds[name] = None
            return False
    
    def play_sound(self, name: str) -> None:
        """Play a sound effect.
        
        Args:
            name: Name of the sound to play
        """
        if name in self.sounds and self.sounds[name] is not None:
            self.sounds[name].play()
    
    def set_master_volume(self, volume: float) -> None:
        """Set the master volume for all sounds.
        
        Args:
            volume: Master volume level (0.0 to 1.0)
        """
        self.master_volume = max(0.0, min(1.0, volume))
        
        # Update all loaded sounds
        for name, sound in self.sounds.items():
            if sound is not None:
                original_volume = self.sound_volumes.get(name, 1.0)
                sound.set_volume(original_volume * self.master_volume)
    
    def stop_all_sounds(self) -> None:
        """Stop all currently playing sounds."""
        pygame.mixer.stop()


# Global sound manager instance
sound_manager: Optional[SoundManager] = None


def get_sound_manager() -> SoundManager:
    """Get the global sound manager instance."""
    global sound_manager
    if sound_manager is None:
        sound_manager = SoundManager()
    return sound_manager


def play_sound(name: str) -> None:
    """Convenience function to play a sound."""
    get_sound_manager().play_sound(name)

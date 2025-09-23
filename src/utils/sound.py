"""Sound management utilities."""

import pygame
import os
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
        
    def load_sound(self, name: str, filepath: str, volume: float = 1.0) -> bool:
        """Load a sound effect.
        
        Args:
            name: Internal name for the sound
            filepath: Path to the sound file
            volume: Volume level for this specific sound (0.0 to 1.0)
            
        Returns:
            True if sound loaded successfully, False otherwise
        """
        try:
            if os.path.exists(filepath):
                sound = pygame.mixer.Sound(filepath)
                sound.set_volume(volume * self.master_volume)
                self.sounds[name] = sound
                self.sound_volumes[name] = volume
                print(f"Loaded sound: {name}")
                return True
            else:
                print(f"Sound file not found: {filepath}")
                # Create a silent dummy sound as fallback
                self.sounds[name] = None
                return False
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

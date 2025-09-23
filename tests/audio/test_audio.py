"""
Audio System Test Suite

This script tests the pygame audio system and creates test sounds.
Run this to verify that audio is working properly on your system.

Usage:
    python tests/audio/test_audio.py
"""

import pygame
import sys
import os

# Add project root to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))


def test_audio_system():
    """Test if the audio system is working."""
    print("Testing audio system...")
    
    # Initialize pygame
    pygame.init()
    pygame.mixer.init(frequency=22050, size=-16, channels=2, buffer=512)
    
    print(f"Mixer initialized: {pygame.mixer.get_init()}")
    print(f"Number of mixer channels: {pygame.mixer.get_num_channels()}")
    
    # Create a simple beep using pygame's built-in capabilities
    try:
        # Test with a simple frequency generator (if available)
        print("Testing basic audio...")
        
        # Create a very simple test sound using a basic method
        duration = 0.5  # seconds
        sample_rate = 22050
        
        # Try to make a simple sound buffer
        # This is a very basic approach without numpy
        import struct
        
        # Generate a simple sine wave manually
        import math
        samples = []
        frequency = 440  # A note
        
        for i in range(int(duration * sample_rate)):
            # Simple sine wave
            value = math.sin(2 * math.pi * frequency * i / sample_rate)
            # Convert to 16-bit signed integer
            sample = int(value * 16383)  # Half volume to be safe
            # Stereo: same sample for both channels
            samples.extend([sample, sample])
        
        # Pack as bytes
        sound_data = struct.pack('<' + 'h' * len(samples), *samples)
        
        # Create pygame sound from raw data
        test_sound = pygame.mixer.Sound(buffer=sound_data)
        
        print("Playing test beep...")
        test_sound.play()
        
        # Wait for sound to finish
        pygame.time.wait(600)
        
        print("Audio system is working!")
        return True
        
    except Exception as e:
        print(f"Error testing audio: {e}")
        return False


def create_simple_beep_sounds():
    """Create simple beep sounds without numpy."""
    import struct
    import math
    import os
    
    os.makedirs("assets/sounds", exist_ok=True)
    
    pygame.mixer.init(frequency=22050, size=-16, channels=2, buffer=512)
    
    def make_beep(frequency, duration, volume=0.3):
        """Make a simple beep sound."""
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
    
    def make_noise_burst(duration, volume=0.2):
        """Make a noise burst for explosion."""
        import random
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
    
    # Create sounds
    sounds = {
        "shoot": make_beep(800, 0.15, 0.4),        # High pitched short beep
        "explosion": make_noise_burst(0.4, 0.3),   # Noise burst
        "thrust": make_beep(150, 0.3, 0.25),       # Low rumble
        "collision": make_beep(600, 0.2, 0.4)      # Medium pitched beep
    }
    
    print("Created sound effects:")
    for name, sound in sounds.items():
        print(f"  - {name}: {sound.get_length():.2f}s")
        
        # Test each sound
        print(f"    Testing {name}...")
        sound.play()
        pygame.time.wait(int(sound.get_length() * 1000) + 100)
    
    return sounds


if __name__ == "__main__":
    if test_audio_system():
        print("\n" + "="*50)
        print("Creating game sound effects...")
        sounds = create_simple_beep_sounds()
        print("Sound effects created successfully!")
        print("\nNow try running the game - you should hear sounds!")
    else:
        print("Audio system test failed. Check your audio settings.")
        sys.exit(1)

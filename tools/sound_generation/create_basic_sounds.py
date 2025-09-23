"""Simple sound file generator using pygame only."""

import pygame
import os


def create_basic_sound_files():
    """Create basic sound files using pygame's capabilities."""
    # Ensure assets/sounds directory exists
    os.makedirs("assets/sounds", exist_ok=True)
    
    pygame.mixer.pre_init(frequency=22050, size=-16, channels=2, buffer=512)
    pygame.mixer.init()
    
    # Create simple beep sounds with different frequencies
    # These are very basic - you'll want to replace with real sound files
    
    sounds_info = [
        ("shoot", 800, 0.1),      # High pitch, short
        ("explosion", 200, 0.3),   # Low pitch, longer  
        ("thrust", 150, 0.2),      # Very low pitch, medium
        ("collision", 600, 0.15)   # Medium pitch, short
    ]
    
    for name, frequency, duration in sounds_info:
        # Create a simple sine wave tone
        sample_rate = 22050
        frames = int(duration * sample_rate)
        
        # Create sound array (very basic sine wave)
        sound_data = []
        for i in range(frames):
            # Simple sine wave with fade out
            amplitude = 0.3 * (1 - i / frames)  # Fade out
            sample = int(amplitude * 32767 * 
                        (1 if (i * frequency * 2 // sample_rate) % 2 == 0 else -1))
            sound_data.extend([sample, sample])  # Stereo
        
        # Convert to bytes
        sound_bytes = b''.join(sample.to_bytes(2, 'little', signed=True) for sample in sound_data)
        
        # Create pygame sound
        try:
            sound = pygame.mixer.Sound(buffer=sound_bytes)
            filepath = f"assets/sounds/{name}.wav"
            
            # Unfortunately pygame can't easily save sounds to file
            # So we'll create an empty file as a placeholder
            with open(filepath, 'wb') as f:
                # Write minimal WAV header for a very short silent sound
                f.write(b'RIFF')
                f.write((36).to_bytes(4, 'little'))
                f.write(b'WAVE')
                f.write(b'fmt ')
                f.write((16).to_bytes(4, 'little'))
                f.write((1).to_bytes(2, 'little'))  # PCM
                f.write((2).to_bytes(2, 'little'))  # Stereo
                f.write((22050).to_bytes(4, 'little'))  # Sample rate
                f.write((88200).to_bytes(4, 'little'))  # Byte rate
                f.write((4).to_bytes(2, 'little'))  # Block align
                f.write((16).to_bytes(2, 'little'))  # Bits per sample
                f.write(b'data')
                f.write((0).to_bytes(4, 'little'))  # Data size (empty)
            
            print(f"Created placeholder sound file: {filepath}")
            
        except Exception as e:
            print(f"Error creating sound {name}: {e}")


if __name__ == "__main__":
    create_basic_sound_files()

"""Create audible sound effects using pygame's audio capabilities."""

import pygame
import math
import array


def create_audible_sounds():
    """Create simple but audible sound effects."""
    # Ensure assets/sounds directory exists
    import os
    os.makedirs("assets/sounds", exist_ok=True)
    
    # Initialize pygame mixer
    pygame.mixer.pre_init(frequency=22050, size=-16, channels=1, buffer=512)
    pygame.mixer.init()
    
    # Sample rate
    sample_rate = 22050
    
    def create_tone(frequency, duration, volume=0.5, fade_out=True):
        """Create a simple tone."""
        frames = int(duration * sample_rate)
        arr = array.array('h')
        
        for i in range(frames):
            # Calculate the sample
            time_frac = i / sample_rate
            wave = math.sin(2 * math.pi * frequency * time_frac)
            
            # Apply fade out envelope if requested
            if fade_out:
                envelope = 1 - (i / frames)  # Linear fade out
                wave *= envelope
            
            # Apply volume and convert to 16-bit integer
            sample = int(wave * volume * 32767)
            arr.append(sample)
        
        return pygame.sndarray.make_sound(arr)
    
    def create_sweep(start_freq, end_freq, duration, volume=0.5):
        """Create a frequency sweep."""
        frames = int(duration * sample_rate)
        arr = array.array('h')
        
        for i in range(frames):
            time_frac = i / sample_rate
            progress = i / frames
            
            # Interpolate frequency
            frequency = start_freq + (end_freq - start_freq) * progress
            wave = math.sin(2 * math.pi * frequency * time_frac)
            
            # Apply envelope
            envelope = 1 - progress  # Fade out
            wave *= envelope
            
            # Apply volume and convert to 16-bit integer
            sample = int(wave * volume * 32767)
            arr.append(sample)
        
        return pygame.sndarray.make_sound(arr)
    
    def create_noise_burst(duration, volume=0.3):
        """Create a noise burst for explosion."""
        frames = int(duration * sample_rate)
        arr = array.array('h')
        
        import random
        for i in range(frames):
            progress = i / frames
            
            # Random noise
            noise = (random.random() * 2 - 1)
            
            # Apply envelope (quick attack, slow decay)
            if progress < 0.1:
                envelope = progress / 0.1
            else:
                envelope = math.exp(-3 * (progress - 0.1) / 0.9)
            
            wave = noise * envelope
            
            # Apply volume and convert to 16-bit integer
            sample = int(wave * volume * 32767)
            arr.append(sample)
        
        return pygame.sndarray.make_sound(arr)
    
    # Create the sounds
    sounds = {
        "shoot": create_sweep(800, 200, 0.15, 0.4),      # High to low sweep
        "explosion": create_noise_burst(0.5, 0.6),        # Noise burst
        "thrust": create_tone(120, 0.3, 0.3, False),      # Low rumble
        "collision": create_tone(600, 0.2, 0.5, True)     # Sharp tone
    }
    
    # Test each sound and save if possible
    for name, sound in sounds.items():
        print(f"Created {name} sound - testing...")
        
        # Test play the sound
        sound.play()
        pygame.time.wait(int(sound.get_length() * 1000) + 100)  # Wait for sound to finish
        
        # Try to save (this might not work on all systems, but the sound will still be loaded)
        try:
            # Save as a simple raw format that can be loaded later
            filepath = f"assets/sounds/{name}.wav"
            
            # Create a minimal WAV file
            # Note: pygame doesn't easily export sounds, so we'll use the sounds directly
            print(f"Sound {name} ready for use")
            
        except Exception as e:
            print(f"Note: Could not save {name} to file ({e}), but sound is loaded in memory")
    
    return sounds


if __name__ == "__main__":
    print("Creating audible sound effects...")
    sounds = create_audible_sounds()
    print("Done! Sound effects created.")
    print("Note: These are basic procedural sounds. For better quality,")
    print("consider downloading professional sound effects from freesound.org")

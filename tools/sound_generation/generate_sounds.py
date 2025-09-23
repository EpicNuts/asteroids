"""Generate basic sound effects for testing."""

import pygame
import numpy as np
import os


def generate_sine_wave(frequency: float, duration: float, sample_rate: int = 22050, amplitude: float = 0.3) -> np.ndarray:
    """Generate a sine wave."""
    frames = int(duration * sample_rate)
    arr = np.zeros(frames)
    
    for i in range(frames):
        arr[i] = amplitude * np.sin(2 * np.pi * frequency * i / sample_rate)
    
    return arr


def generate_noise(duration: float, sample_rate: int = 22050, amplitude: float = 0.1) -> np.ndarray:
    """Generate white noise."""
    frames = int(duration * sample_rate)
    return amplitude * (2 * np.random.random(frames) - 1)


def generate_shoot_sound() -> np.ndarray:
    """Generate a laser shoot sound effect."""
    duration = 0.2
    sample_rate = 22050
    
    # High pitched descending tone
    frames = int(duration * sample_rate)
    arr = np.zeros(frames)
    
    for i in range(frames):
        # Frequency descends from 800Hz to 200Hz
        progress = i / frames
        frequency = 800 - (600 * progress)
        envelope = (1 - progress) * 0.3  # Fade out
        arr[i] = envelope * np.sin(2 * np.pi * frequency * i / sample_rate)
    
    return arr


def generate_explosion_sound() -> np.ndarray:
    """Generate an explosion sound effect."""
    duration = 0.5
    sample_rate = 22050
    
    # Mix of noise and low frequency rumble
    noise = generate_noise(duration, sample_rate, 0.4)
    rumble = generate_sine_wave(60, duration, sample_rate, 0.2)
    
    # Apply envelope
    frames = len(noise)
    envelope = np.zeros(frames)
    
    # Quick attack, slow decay
    attack_frames = int(0.1 * sample_rate)
    for i in range(frames):
        if i < attack_frames:
            envelope[i] = i / attack_frames
        else:
            envelope[i] = np.exp(-3 * (i - attack_frames) / (frames - attack_frames))
    
    return (noise + rumble) * envelope


def generate_thrust_sound() -> np.ndarray:
    """Generate a thrust/engine sound effect."""
    duration = 0.3
    sample_rate = 22050
    
    # Low frequency rumble with some noise
    base_freq = 120
    noise_component = generate_noise(duration, sample_rate, 0.1)
    tone_component = generate_sine_wave(base_freq, duration, sample_rate, 0.2)
    
    return noise_component + tone_component


def generate_collision_sound() -> np.ndarray:
    """Generate a collision sound effect."""
    duration = 0.3
    sample_rate = 22050
    
    # Sharp metallic clang
    frames = int(duration * sample_rate)
    arr = np.zeros(frames)
    
    frequencies = [800, 1200, 1600]  # Metallic harmonics
    
    for i in range(frames):
        progress = i / frames
        envelope = np.exp(-5 * progress)  # Quick decay
        
        sample = 0
        for freq in frequencies:
            sample += envelope * 0.15 * np.sin(2 * np.pi * freq * i / sample_rate)
        
        arr[i] = sample
    
    return arr


def create_sound_files():
    """Create basic sound files for testing."""
    # Ensure assets/sounds directory exists
    os.makedirs("assets/sounds", exist_ok=True)
    
    pygame.mixer.pre_init(frequency=22050, size=-16, channels=2, buffer=512)
    pygame.mixer.init()
    
    sounds = {
        "shoot": generate_shoot_sound(),
        "explosion": generate_explosion_sound(), 
        "thrust": generate_thrust_sound(),
        "collision": generate_collision_sound()
    }
    
    for name, sound_data in sounds.items():
        # Convert to 16-bit integers
        sound_data = (sound_data * 32767).astype(np.int16)
        
        # Create pygame sound and save
        sound = pygame.sndarray.make_sound(sound_data)
        filepath = f"assets/sounds/{name}.wav"
        
        # Save as WAV file
        # Note: pygame doesn't have direct wav export, so we'll use numpy
        import wave
        with wave.open(filepath, 'w') as wav_file:
            wav_file.setnchannels(1)  # Mono
            wav_file.setsampwidth(2)  # 16-bit
            wav_file.setframerate(22050)
            wav_file.writeframes(sound_data.tobytes())
        
        print(f"Created sound file: {filepath}")


if __name__ == "__main__":
    try:
        import numpy as np
        create_sound_files()
    except ImportError:
        print("NumPy not available, cannot generate sound files.")
        print("You can add your own .wav files to assets/sounds/ instead.")

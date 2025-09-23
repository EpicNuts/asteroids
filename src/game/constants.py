"""Game constants and configuration."""

# Screen settings
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720

# Asteroid settings
ASTEROID_MIN_RADIUS = 20
ASTEROID_KINDS = 3
ASTEROID_SPAWN_RATE = 0.8  # seconds
ASTEROID_MAX_RADIUS = ASTEROID_MIN_RADIUS * ASTEROID_KINDS

# Player settings
PLAYER_RADIUS = 20
PLAYER_TURN_SPEED = 300
PLAYER_ACCELERATION = 800  # Increased for more noticeable acceleration
PLAYER_SPEED = 200
PLAYER_MAX_SPEED = 600     # More reasonable max speed
PLAYER_DRAG = 0.98         # Reduced drag so acceleration is more effective
PLAYER_SHOOT_SPEED = 500
PLAYER_SHOOT_COOLDOWN = 0.3  # seconds

# Shot settings
SHOT_RADIUS = 5

# Game settings
PLAYER_LIVES = 3

# Loading screen settings
SHOW_LOADING_SCREEN = True
LOADING_SCREEN_TIMEOUT = 30  # Maximum time to wait for background generation

# Sound settings
MASTER_VOLUME = 0.7
SOUND_VOLUME_SHOOT = 0.5
SOUND_VOLUME_EXPLOSION = 0.8
SOUND_VOLUME_THRUST = 0.3
SOUND_VOLUME_COLLISION = 0.6

# Background settings
BACKGROUND_IMAGE_PATH = "assets/images/nebula_background.png"
BACKGROUND_CACHE_PATH = "assets/images/nebula_cache.png"
GENERATE_BACKGROUND_ON_STARTUP = True
BACKGROUND_SEED = None  # None for random each time, or set an integer for reproducible background
FORCE_REGENERATE_BACKGROUND = False  # Set to True to always generate new background
NEBULA_THEME = None  # None for random theme, or choose: 'default', 'fire', 'ice', 'alien', 'sunset'
BACKGROUND_GENERATION_TIMEOUT = 30  # Maximum seconds to wait for background generation
FAST_BACKGROUND_MODE = True  # Generate smaller images and scale up for faster startup

# Sound file paths
SOUND_PATH_SHOOT = "assets/sounds/shoot.wav"
SOUND_PATH_EXPLOSION = "assets/sounds/explosion.wav" 
SOUND_PATH_THRUST = "assets/sounds/thrust.wav"
SOUND_PATH_COLLISION = "assets/sounds/collision.wav"

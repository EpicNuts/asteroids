# Development Tools

This directory contains development tools and utilities for the Asteroids game.

## Sound Generation

The `sound_generation/` directory contains tools for creating procedural sound effects:

### `create_sounds.py`
Generate all game sound effects programmatically.

**Usage:**
```bash
# From project root
python tools/sound_generation/create_sounds.py

# Or as a module
python -m tools.sound_generation.create_sounds
```

**Features:**
- Creates all 4 game sound effects (shoot, explosion, thrust, collision)
- Tests each sound as it's created
- Uses only pygame and standard library (no NumPy required)
- Generates sounds in memory for immediate use

### Legacy Files
- `generate_sounds.py` - Advanced sound generation (requires NumPy)
- `create_audible_sounds.py` - Alternative sound creation method
- `create_basic_sounds.py` - Simple sound file creation

## Future Tools

This directory is ready for additional development tools such as:
- Sprite generation utilities
- Level editors
- Asset optimization scripts
- Build tools

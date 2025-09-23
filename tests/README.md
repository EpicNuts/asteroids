# Tests

This directory contains all test files for the Asteroids game.

## Directory Structure

### `audio/`
Audio system tests and utilities.

**Files:**
- `test_audio.py` - Comprehensive audio system testing
  - Tests pygame mixer initialization
  - Creates and tests sound generation
  - Verifies audio playback functionality

### `game/` 
Game logic and mechanics tests (ready for future tests).

**Future test categories:**
- Entity behavior tests (Player, Asteroid, Shot)
- Collision detection tests
- Game state management tests
- Physics and movement tests

## Running Tests

### Audio Tests
```bash
# Test audio system
python tests/audio/test_audio.py
```

### Future Integration
This structure is ready for pytest or unittest integration:

```bash
# Future usage (when tests are added)
pytest tests/
python -m unittest discover tests/
```

## Test Guidelines

When adding new tests:
1. Place audio-related tests in `tests/audio/`
2. Place game logic tests in `tests/game/`
3. Use descriptive filenames (e.g., `test_collision_detection.py`)
4. Include docstrings explaining what each test covers

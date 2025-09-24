# Asteroids Game

Yet another take on the classic Asteroids arcade game, built with Python and Pygame. Features animated sprites, multiple graphics modes, and a professional asset management system. Initiated as part of the [Boot.dev Python Development Course](https://www.boot.dev/courses/build-asteroids-python), and expanded upon.

## Features

- **Three Graphics Modes**: Switch between different visual styles on-the-fly
  - **Sprites Mode**: Full animated asteroids with 16-frame sprite animations and custom ship sprite
  - **Basic Mode**: Enhanced geometric shapes with chevron ship design and irregular polygon asteroids
  - **Minimal Mode**: Clean wireframe graphics for classic arcade feel

- **Performance Optimized**: Threaded asset preloading system eliminates frame drops
- **Dynamic Audio**: Procedural sound generation with fallback audio system
- **Professional Structure**: Modular codebase with proper separation of concerns
- **Beautiful Backgrounds**: Randomly selected space imagery for immersive gameplay

## Controls

- **Arrow Keys / WASD**: Move and rotate ship
- **Spacebar**: Shoot
- **G**: Cycle through graphics modes (Sprites → Basic → Minimal)
- **B**: Cycle through background images

## Graphics Modes

### Sprites Mode
- Animated asteroids with 16-frame rotation cycles
- Custom ship sprite with proper scaling and rotation
- Full visual effects and engine glow

### Basic Mode
- Chevron-shaped ship design
- Irregular 5-7 sided polygon asteroids
- Filled shapes with colored outlines

### Minimal Mode
- Simple wireframe triangle ship
- Circle wireframe asteroids
- Clean, classic arcade aesthetic

## Installation

1. Ensure you have Python 3.12+ installed
2. Install uv package manager if not already installed
3. Clone this repository
4. Run the game:

```bash
uv run python main.py
```

## Project Structure

```
asteroids/
├── main.py                 # Main game loop and entry point
├── src/                    # Source code modules
│   ├── entities/           # Game entities (Player, Asteroid, Shot)
│   ├── game/              # Game logic and constants
│   └── utils/             # Utilities (Asset Manager, Graphics Manager, etc.)
├── assets/                # Game assets
│   ├── asteroids/         # Sprite animations
│   ├── images/           # Background images
│   ├── ships/            # Ship sprites
│   └── sounds/           # Audio files
├── tests/                # Test files
└── tools/               # Development tools
```

## Art Assets Attribution

This project uses various art assets from different sources:

### Background Images

- **Trifid Nebula** (`Trifid_Nebula_by_Deddy_Dayag.jpg`): 
  - Created by Deddy Dayag
  - Source: Wikipedia
  - License: Creative Commons

- **Hubble Space Telescope Images** (files starting with `heic`):
  - `heic0411a.jpg`, `heic0910e.jpg`, `heic1105a.jpg`, `heic1819a.jpg`
  - Source: NASA Hubble Space Telescope
  - Credit: NASA/ESA
  - Public Domain

- **AI Generated Space Scenes** (files starting with `StockCake`):
  - `StockCake-Celestial Aurora Majesty_1758665862.jpg`
  - `StockCake-Celestial World Discovered_1758665899.jpg`
  - `StockCake-Cosmic Asteroid Field_1758665834.jpg`
  - `StockCake-Cosmic Debris Field_1758665951.jpg`
  - `StockCake-Cosmic Rocks Adrift_1758665959.jpg`
  - Source: StockCake.com
  - AI Generated Images
  - License: Public Domain

### Sprite Assets

- **Asteroid Sprites**: 
  - Source: http://zimnox.com, via Reddit
  - Various asteroid animations in large, medium, and small sizes
  - Multiple variants (a1, a3, b1 series)

### Ship Assets

- **Ship Sprite** (`yct20hubfk061.png`):
  - Source: Thunder246, via Reddit
  - Used in sprites graphics mode

## Technical Features

### Asset Management System
- Threaded preloading of all sprite animations
- Progress tracking with loading screen
- Intelligent caching to prevent runtime file I/O
- Support for multiple sprite variants and sizes

### Graphics Management
- Runtime switching between three distinct visual modes
- Mode-specific rendering pipelines
- Optimized drawing routines for each graphics style
- Proper sprite scaling and rotation handling

### Audio System
- Procedural sound generation for missing audio files
- Dynamic sound loading and caching
- Support for shoot, explosion, thrust, and collision sounds

## Development

The project uses a modern Python development setup:
- **uv** for package management and virtual environments
- **pygame 2.6.1** for graphics and input handling
- **Modular architecture** for maintainability
- **Professional project structure** following Python best practices

## License

This project is open source. Please respect the individual licenses of the art assets as listed above.

## Acknowledgments

Special thanks to:
- Boot.dev for the base project
- Deddy Dayag for the beautiful Trifid Nebula image
- NASA/ESA Hubble Space Telescope team for the space imagery
- StockCake.com for the AI-generated cosmic scenes
- Zimnox.com for the asteroid sprite animations
- The Pygame community for the excellent game development framework

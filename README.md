# GenAnim

**GenAnim** is a HooRii Agent Character Animation Generation System - a comprehensive framework for creating and managing AI character agents with state-based animations, emotion responses, and multi-device switching capabilities.

## Overview

This project implements the complete workflow for creating a virtual AI character agent (like the cat-eared girl "HooRii" example) with:

- **Character Setup**: Define character attributes, personality, and appearance
- **Character Image Generation**: Create character visuals using AI image generation
- **State Management**: Manage character states (idle, listening, speaking, emotions)
- **Emotion System**: Respond to user input with 9 different emotion states
- **Multi-Device Switching**: Seamlessly switch character presence between devices
- **Video Generation**: Interface for AI video generation models

## Features

### Character States

- **Default State**: Character idle, not engaged with user
- **Listening State**: Character actively listening to user
- **Speaking State**: Character speaking with lip sync
- **Emotion States**: 9 emotions (happy, shy, surprised, smug, angry, confused, sad, sleepy, neutral)
- **Device Transitions**: Enter/leave animations for device switching

### State Machine

- Validates state transitions
- Manages first/last frame control for seamless video transitions
- Handles state history and callbacks
- Ensures smooth animation flow

### Multi-Device Support

- Character can only be active on ONE device at a time
- Seamless switching between hardware, mobile, desktop, and web devices
- Synchronized state and conversation history across devices
- "Leave" and "Enter" animations for device transitions

## Project Structure

```
GenAnim/
├── config/                      # Configuration files
│   ├── character_config.json   # Character attributes and appearance
│   ├── video_params.json       # Video generation parameters
│   └── emotion_keywords.json   # Emotion trigger keywords
├── src/                        # Source code
│   ├── character/             # Character management
│   │   ├── character.py       # Main character class
│   │   └── profile.py         # Character profile
│   ├── state/                 # State management
│   │   ├── states.py          # State definitions
│   │   ├── state_machine.py   # State machine logic
│   │   └── transitions.py     # Transition management
│   ├── video/                 # Video generation
│   │   ├── generator.py       # Video generator interface
│   │   ├── prompts.py         # Prompt generation
│   │   └── processor.py       # Video post-processing
│   ├── device/                # Device management
│   │   ├── device_manager.py  # Multi-device management
│   │   └── sync.py            # Device synchronization
│   └── utils/                 # Utilities
│       ├── logger.py          # Logging
│       └── validator.py       # Configuration validation
├── prompts/                    # Prompt templates
│   ├── emotions/              # Emotion prompts
│   └── transitions/           # Transition prompts
├── examples/                   # Example scripts
├── tests/                      # Unit tests
└── docs/                       # Documentation

```

## Installation

```bash
# Clone the repository
git clone https://github.com/yourusername/GenAnim.git
cd GenAnim

# Install dependencies
pip install -r requirements.txt

# Install the package
pip install -e .
```

## Quick Start

### Generate ALL Animations from Config (Main Usage)

The primary way to use GenAnim is to provide a character configuration JSON and automatically generate all required animations:

```bash
# Generate all 17 required video animations
python src/animation_pipeline.py --character-config config/character_config.json --output-dir output/videos

# Or run the complete example
python examples/complete_generation.py
```

This will automatically generate:
- 3 base state videos (default, listening, speaking)
- 2 transition videos (default↔listening)
- 9 emotion videos (happy, shy, surprised, smug, angry, confused, sad, sleepy, neutral)
- 3 device transition videos (enter, 2x leave)

**Total: 17 videos + 1 reference image**

### Manual Configuration

### 1. Configure Your Character

Edit `config/character_config.json` to define your character:

```json
{
  "character": {
    "nickname": "HooRii",
    "gender": "female",
    "age": 24,
    "personality": {
      "traits": ["tsundere", "mischievous", "cute", "clever"]
    }
  }
}
```

### 2. Initialize Character

```python
from src.character import Character, CharacterProfile
from src.state import StateMachine

# Load character profile
profile = CharacterProfile("config/character_config.json")

# Create character
character = Character(
    character_id="hoorii_001",
    profile=profile
)

# Initialize state machine
state_machine = StateMachine()
```

### 3. Manage States

```python
from src.state import StateType, EmotionType

# Transition to listening state
success, error = state_machine.transition_to(StateType.LISTENING)

# Trigger emotion
success, error = state_machine.transition_to(
    StateType.EMOTION,
    emotion=EmotionType.HAPPY
)
```

### 4. Generate All Animations with Pipeline

```python
from src.animation_pipeline import AnimationPipeline

# Create pipeline
pipeline = AnimationPipeline(
    character_config_path="config/character_config.json",
    video_config_path="config/video_params.json",
    output_dir="output/videos"
)

# Generate ALL required animations
videos = pipeline.generate_all_animations()
# Returns dict of 17 videos: {'default': 'output/videos/default.mp4', ...}
```

### 5. Multi-Device Management

```python
from src.device import DeviceManager, DeviceType

# Initialize device manager
device_mgr = DeviceManager(user_id="user123")

# Register devices
device_mgr.register_device("device1", DeviceType.HARDWARE, "Desktop Hardware")
device_mgr.register_device("device2", DeviceType.MOBILE, "iPhone")

# Switch character between devices
success, error = device_mgr.switch_device(
    from_device_id="device1",
    to_device_id="device2"
)
```

## Character Creation Workflow

### Phase 1: Character Setup
Define character attributes, personality, background, and special features.

### Phase 2: Character Image Generation
1. Create character image prompts combining setup + appearance
2. Generate images using AI models (text-to-image or image-to-image)
3. Refine using models like Seedream V4, Gemini Nano Banana
4. Post-process: remove background, upscale, adjust colors

### Phase 3: Character State Switching (Key Phase)
Generate video cuts for different states:
- **Default state**: 5s idle animation
- **Listening state**: 5s listening animation
- **Speaking state**: 4s with lip movement
- **9 Emotion states**: 5s each (happy, shy, surprised, etc.)
- **Transition videos**: Default↔Listening, Leave, Enter

Key principle: Use **first/last frame control** to ensure seamless transitions

### Phase 4: Multi-Device Switching
Generate device transition animations:
- **Leave animation**: Character runs out of frame
- **Enter animation**: Character enters frame
- **Empty state**: Display when character is on another device

## Video Generation Parameters

All videos follow these specifications:
- **Aspect Ratio**: 9:16
- **Resolution**: 1080p (1088x1920)
- **Frame Rate**: 24fps
- **Codec**: H.264
- **Format**: MP4
- **Color Space**: Rec.709 SDR

## Emotion Trigger System

The system detects emotions from user input using keyword matching:

```python
# Emotion keywords are configured in config/emotion_keywords.json
{
  "happy": ["开心", "高兴", "快乐", "happy", "great"],
  "angry": ["生气", "烦", "angry", "annoyed"],
  "surprised": ["惊讶", "wow", "omg"]
}
```

## Configuration

### Character Configuration (`config/character_config.json`)
- Basic info: nickname, gender, age
- Personality traits and background
- Appearance: art style, clothing, face, hairstyle
- Special features and accessories

### Video Parameters (`config/video_params.json`)
- Video specifications (resolution, FPS, codec)
- Generation settings (model, platform)
- State durations
- Post-processing options

### Emotion Keywords (`config/emotion_keywords.json`)
- Keywords that trigger each emotion
- Priority ordering for emotion detection
- Weight and description for each emotion

## Development

### Running Tests

```bash
pytest tests/
```

### Validation

```bash
python -c "from src.utils import ConfigValidator; \
    results = ConfigValidator.validate_all_configs('config'); \
    print(results)"
```

### Generate Prompt Files

```python
from src.video import PromptGenerator
from src.character import CharacterProfile

profile = CharacterProfile("config/character_config.json")
prompt_gen = PromptGenerator(profile)
prompt_gen.save_prompts_to_file("prompts")
```

## API Reference

See [docs/API.md](docs/API.md) for detailed API documentation.

## Video Delivery Checklist

When delivering character videos, ensure all these are included:

- [ ] Default state (1 video)
- [ ] Default→Listening transition (1 video)
- [ ] Listening state (2 videos - with and without speaking)
- [ ] Listening→Default transition (1 video)
- [ ] 9 Emotion states (9 videos)
- [ ] Leave animations (2 videos - from listening and default)
- [ ] Enter animation (1 video)

**Total: 17 video files**

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License.

## Acknowledgments

Based on the HooRii Agent character creation workflow specification, implementing a complete system for AI character animation generation with state management and multi-device support.

## Contact

For questions or support, please open an issue on GitHub.

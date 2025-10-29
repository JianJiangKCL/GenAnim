# GenAnim API Documentation

## Character Module

### CharacterProfile

```python
class CharacterProfile:
    def __init__(self, config_path: Optional[str] = None)
    def load_from_file(self, file_path: str) -> None
    def get_character_info(self) -> Dict[str, Any]
    def get_appearance_info(self) -> Dict[str, Any]
    def get_image_prompt(self) -> str

    @property
    def nickname(self) -> str
    @property
    def personality_traits(self) -> list
    @property
    def art_style(self) -> str
```

### Character

```python
class Character:
    def __init__(
        self,
        character_id: str,
        profile: CharacterProfile,
        initial_state: StateType = StateType.DEFAULT
    )

    def get_state(self) -> Optional[CharacterState]
    def get_state_type(self) -> Optional[StateType]
    def set_online(self, online: bool = True) -> None
    def connect(self) -> bool
    def disconnect(self) -> None
    def set_device(self, device_id: str) -> None
    def get_status(self) -> Dict[str, Any]
```

## State Module

### StateType (Enum)

```python
class StateType(Enum):
    DEFAULT = "default"       # Idle state
    LISTENING = "listening"   # Listening to user
    SPEAKING = "speaking"     # Speaking
    EMOTION = "emotion"       # Emotion state
    LEAVING = "leaving"       # Leaving device
    ENTERING = "entering"     # Entering device
    EMPTY = "empty"          # Not present
```

### EmotionType (Enum)

```python
class EmotionType(Enum):
    NEUTRAL = "neutral"
    HAPPY = "happy"
    SHY = "shy"
    SURPRISED = "surprised"
    SMUG = "smug"
    ANGRY = "angry"
    CONFUSED = "confused"
    SAD = "sad"
    SLEEPY = "sleepy"
```

### CharacterState

```python
@dataclass
class CharacterState:
    state_type: StateType
    emotion: Optional[EmotionType] = None
    duration: float = 5.0
    loop: bool = False

    def get_video_name(self) -> str
    def is_interactive(self) -> bool
    def can_trigger_emotion(self) -> bool
```

### StateMachine

```python
class StateMachine:
    def __init__(self)

    def transition_to(
        self,
        target_state: StateType,
        emotion: Optional[EmotionType] = None
    ) -> tuple[bool, Optional[str]]

    def register_callback(self, state_type: StateType, callback: Callable) -> None
    def get_current_state(self) -> Optional[CharacterState]
    def get_previous_state(self) -> Optional[CharacterState]
    def get_state_history(self, limit: int = 10) -> List[CharacterState]
    def can_transition_to(self, target_state: StateType) -> bool
    def reset(self) -> None
```

### TransitionManager

```python
class TransitionManager:
    def __init__(self)

    def get_transition(
        self,
        from_state: StateType,
        to_state: StateType,
        emotion: Optional[EmotionType] = None
    ) -> Optional[Transition]

    def requires_transition_video(
        self,
        from_state: StateType,
        to_state: StateType
    ) -> bool

    def get_all_transitions(self) -> list[Transition]
```

## Video Module

### PromptGenerator

```python
class PromptGenerator:
    def __init__(self, character_profile: CharacterProfile)

    def generate_state_prompt(
        self,
        state: CharacterState,
        include_technical: bool = True
    ) -> str

    def generate_transition_prompt(
        self,
        from_state: StateType,
        to_state: StateType
    ) -> str

    def generate_image_prompt(self, with_background: bool = False) -> str
    def save_prompts_to_file(self, output_dir: str) -> None
```

### VideoGenerator

```python
class VideoGenerator:
    def __init__(self, config_path: Optional[str] = None)

    def generate_video(
        self,
        request: VideoGenerationRequest,
        output_path: str
    ) -> Dict[str, Any]

    def generate_with_frame_control(
        self,
        prompt: str,
        first_frame_path: str,
        last_frame_path: str,
        output_path: str,
        duration: float = 5.0
    ) -> Dict[str, Any]

    def get_supported_models(self) -> list[str]
    def validate_request(self, request: VideoGenerationRequest) -> tuple[bool, Optional[str]]
```

### VideoProcessor

```python
class VideoProcessor:
    def __init__(self)

    def remove_watermark(self, video_path: str, output_path: str) -> Dict[str, Any]
    def remove_background(self, video_path: str, output_path: str, background_color: str = "white") -> Dict[str, Any]
    def upscale(self, video_path: str, output_path: str, target_resolution: str = "1080p") -> Dict[str, Any]
    def extract_frame(self, video_path: str, frame_position: str, output_path: str) -> Dict[str, Any]
    def concatenate_videos(self, video_paths: list[str], output_path: str, transition_duration: float = 0.0) -> Dict[str, Any]
    def check_video_consistency(self, video_paths: list[str]) -> Dict[str, Any]
    def adjust_color(self, video_path: str, output_path: str, brightness: float = 0.0, contrast: float = 0.0) -> Dict[str, Any]
    def crop_video(self, video_path: str, output_path: str, aspect_ratio: str = "9:16") -> Dict[str, Any]
    def validate_video(self, video_path: str) -> Dict[str, Any]
```

## Device Module

### DeviceType (Enum)

```python
class DeviceType(Enum):
    HARDWARE = "hardware"
    MOBILE = "mobile"
    DESKTOP = "desktop"
    WEB = "web"
```

### DeviceManager

```python
class DeviceManager:
    def __init__(self, user_id: str)

    def register_device(self, device_id: str, device_type: DeviceType, name: str) -> Device
    def get_device(self, device_id: str) -> Optional[Device]
    def get_active_device(self) -> Optional[Device]

    def switch_device(
        self,
        from_device_id: Optional[str],
        to_device_id: str
    ) -> tuple[bool, Optional[str]]

    def character_leave_device(self, device_id: str) -> tuple[bool, Optional[str]]
    def character_enter_device(self, device_id: str) -> tuple[bool, Optional[str]]
    def get_all_devices(self) -> List[Device]
    def is_character_online(self) -> bool
    def get_status(self) -> Dict
```

### DeviceSyncManager

```python
class DeviceSyncManager:
    def __init__(self)

    def sync_character_state(self, character_id: str, state: CharacterState, device_id: str) -> None
    def get_character_state(self, character_id: str) -> Optional[Dict[str, Any]]
    def sync_conversation_history(self, character_id: str, messages: list, device_id: str) -> None
    def get_conversation_history(self, character_id: str) -> list
    def sync_character_memory(self, character_id: str, memory_data: Dict[str, Any], device_id: str) -> None
    def get_character_memory(self, character_id: str) -> Dict[str, Any]
    def sync_device_switch(self, character_id: str, from_device: Optional[str], to_device: str) -> None
    def get_sync_status(self) -> Dict[str, Any]
    def clear_sync_data(self, character_id: Optional[str] = None) -> None
```

## Utils Module

### Logger

```python
def setup_logger(
    name: str = "genanim",
    level: int = logging.INFO,
    log_file: Optional[str] = None
) -> logging.Logger
```

### ConfigValidator

```python
class ConfigValidator:
    @staticmethod
    def validate_character_config(config: Dict[str, Any]) -> tuple[bool, Optional[str]]

    @staticmethod
    def validate_video_params(config: Dict[str, Any]) -> tuple[bool, Optional[str]]

    @staticmethod
    def validate_emotion_keywords(config: Dict[str, Any]) -> tuple[bool, Optional[str]]

    @staticmethod
    def validate_json_file(file_path: str) -> tuple[bool, Optional[str]]

    @staticmethod
    def validate_all_configs(config_dir: str) -> Dict[str, Any]
```

## Usage Examples

### Complete Character Setup

```python
from src.character import Character, CharacterProfile
from src.state import StateMachine, StateType, EmotionType
from src.video import PromptGenerator, VideoGenerator
from src.device import DeviceManager, DeviceType

# 1. Load character
profile = CharacterProfile("config/character_config.json")
character = Character("char_001", profile)

# 2. Setup state machine
state_machine = StateMachine()

# 3. Setup devices
device_mgr = DeviceManager("user_123")
device_mgr.register_device("hw1", DeviceType.HARDWARE, "Desktop")
device_mgr.register_device("mobile1", DeviceType.MOBILE, "iPhone")

# 4. Character goes online on hardware device
character.set_online()
device_mgr.character_enter_device("hw1")
state_machine.transition_to(StateType.DEFAULT)

# 5. User connects
character.connect()
state_machine.transition_to(StateType.LISTENING)

# 6. Trigger emotion
state_machine.transition_to(StateType.EMOTION, emotion=EmotionType.HAPPY)

# 7. Switch to mobile
device_mgr.switch_device("hw1", "mobile1")
state_machine.transition_to(StateType.LEAVING)
state_machine.transition_to(StateType.EMPTY)
state_machine.transition_to(StateType.ENTERING)
state_machine.transition_to(StateType.LISTENING)
```

### Generate Video Prompts

```python
from src.video import PromptGenerator
from src.character import CharacterProfile
from src.state import CharacterState, StateType, EmotionType

profile = CharacterProfile("config/character_config.json")
prompt_gen = PromptGenerator(profile)

# Generate for different states
listening = CharacterState(StateType.LISTENING)
print(prompt_gen.generate_state_prompt(listening))

happy = CharacterState(StateType.EMOTION, emotion=EmotionType.HAPPY)
print(prompt_gen.generate_state_prompt(happy))

# Generate transition prompt
print(prompt_gen.generate_transition_prompt(
    StateType.DEFAULT,
    StateType.LISTENING
))
```

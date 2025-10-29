"""
State Definitions
Defines all possible character states and emotions
"""

from enum import Enum
from typing import Optional
from dataclasses import dataclass


class StateType(Enum):
    """Main character states"""
    DEFAULT = "default"  # Idle/waiting state (online + not connected)
    LISTENING = "listening"  # Listening state (online + connected)
    SPEAKING = "speaking"  # Speaking state (with lip sync)
    EMOTION = "emotion"  # Emotion state (triggered by keywords)
    LEAVING = "leaving"  # Character leaving device
    ENTERING = "entering"  # Character entering device
    EMPTY = "empty"  # Character not present on device


class EmotionType(Enum):
    """Emotion states based on Expression Sheet"""
    NEUTRAL = "neutral"  # Neutral (same as listening)
    HAPPY = "happy"  # Happy
    SHY = "shy"  # Shy/embarrassed
    SURPRISED = "surprised"  # Surprised
    SMUG = "smug"  # Confident/smug
    ANGRY = "angry"  # Angry
    CONFUSED = "confused"  # Confused
    SAD = "sad"  # Sad
    SLEEPY = "sleepy"  # Sleepy/tired


class TransitionType(Enum):
    """Transition types between states"""
    DEFAULT_TO_LISTENING = "default2listening"
    LISTENING_TO_DEFAULT = "listening2default"
    LISTENING_TO_SPEAKING = "listening2speaking"
    SPEAKING_TO_LISTENING = "speaking2listening"
    LISTENING_TO_EMOTION = "listening2emotion"
    EMOTION_TO_LISTENING = "emotion2listening"
    LISTENING_TO_LEAVING = "listening2leave"
    DEFAULT_TO_LEAVING = "default2leave"
    EMPTY_TO_ENTERING = "empty2enter"
    ENTERING_TO_LISTENING = "enter2listening"


@dataclass
class CharacterState:
    """
    Represents a character state with optional emotion

    Attributes:
        state_type: The main state type
        emotion: Optional emotion if in emotion state
        duration: Duration of the state in seconds
        loop: Whether the state should loop
    """
    state_type: StateType
    emotion: Optional[EmotionType] = None
    duration: float = 5.0
    loop: bool = False

    def __post_init__(self):
        """Validate state after initialization"""
        if self.state_type == StateType.EMOTION and self.emotion is None:
            self.emotion = EmotionType.NEUTRAL

    def get_video_name(self) -> str:
        """
        Get the video file name for this state

        Returns:
            Video file name (without extension)
        """
        if self.state_type == StateType.EMOTION and self.emotion:
            return self.emotion.value
        return self.state_type.value

    def is_interactive(self) -> bool:
        """Check if state allows user interaction"""
        return self.state_type in [StateType.LISTENING, StateType.SPEAKING, StateType.EMOTION]

    def can_trigger_emotion(self) -> bool:
        """Check if emotion can be triggered from this state"""
        return self.state_type == StateType.LISTENING

    def __repr__(self) -> str:
        if self.emotion:
            return f"CharacterState({self.state_type.value}, emotion={self.emotion.value})"
        return f"CharacterState({self.state_type.value})"


def get_state_config(state_type: StateType, emotion: Optional[EmotionType] = None) -> dict:
    """
    Get configuration for a specific state

    Args:
        state_type: Type of state
        emotion: Optional emotion type

    Returns:
        Dictionary with state configuration
    """
    configs = {
        StateType.DEFAULT: {
            "duration": 5.0,
            "loop": True,
            "description": "Character looking away, not engaging with user"
        },
        StateType.LISTENING: {
            "duration": 5.0,
            "loop": True,
            "description": "Character facing camera, neutral expression, ready to interact"
        },
        StateType.SPEAKING: {
            "duration": 4.0,
            "loop": False,
            "description": "Character speaking with lip sync animation"
        },
        StateType.LEAVING: {
            "duration": 5.0,
            "loop": False,
            "description": "Character runs out of frame to the right"
        },
        StateType.ENTERING: {
            "duration": 5.0,
            "loop": False,
            "description": "Character enters frame from the left"
        },
        StateType.EMPTY: {
            "duration": 0,
            "loop": True,
            "description": "Empty state with 'Call her back' button"
        }
    }

    if state_type == StateType.EMOTION and emotion:
        emotion_configs = {
            EmotionType.NEUTRAL: {"duration": 5.0, "description": "Same as listening"},
            EmotionType.HAPPY: {"duration": 5.0, "description": "Happy smile, blushing, tilting head"},
            EmotionType.SHY: {"duration": 10.0, "description": "Looking down shyly, blushing"},
            EmotionType.SURPRISED: {"duration": 5.0, "description": "Surprised expression, body recoils"},
            EmotionType.SMUG: {"duration": 5.0, "description": "Confident, arms crossed"},
            EmotionType.ANGRY: {"duration": 5.0, "description": "Angry, clenched teeth, frowning"},
            EmotionType.CONFUSED: {"duration": 5.0, "description": "Confused, hand on chin, thinking"},
            EmotionType.SAD: {"duration": 5.0, "description": "Sad, sighing, head down"},
            EmotionType.SLEEPY: {"duration": 5.0, "description": "Sleepy, eyes closing, head dropping"}
        }
        return emotion_configs.get(emotion, {})

    return configs.get(state_type, {})

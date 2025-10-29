"""
Unit tests for state machine
"""

import pytest
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from src.state import StateMachine, StateType, EmotionType, CharacterState


class TestStateMachine:
    """Test state machine functionality"""

    def setup_method(self):
        """Setup test fixtures"""
        self.state_machine = StateMachine()

    def test_initialization(self):
        """Test state machine initializes correctly"""
        assert self.state_machine.current_state is not None
        assert self.state_machine.current_state.state_type == StateType.EMPTY

    def test_valid_transition(self):
        """Test valid state transitions"""
        # Empty -> Entering
        success, error = self.state_machine.transition_to(StateType.ENTERING)
        assert success is True
        assert error is None
        assert self.state_machine.current_state.state_type == StateType.ENTERING

        # Entering -> Listening
        success, error = self.state_machine.transition_to(StateType.LISTENING)
        assert success is True
        assert self.state_machine.current_state.state_type == StateType.LISTENING

    def test_invalid_transition(self):
        """Test invalid state transitions are rejected"""
        # Can't go from EMPTY to LISTENING directly
        success, error = self.state_machine.transition_to(StateType.LISTENING)
        assert success is False
        assert error is not None

    def test_emotion_transition(self):
        """Test emotion state transitions"""
        # Setup: go to listening state
        self.state_machine.transition_to(StateType.ENTERING)
        self.state_machine.transition_to(StateType.LISTENING)

        # Trigger emotion
        success, error = self.state_machine.transition_to(
            StateType.EMOTION,
            emotion=EmotionType.HAPPY
        )
        assert success is True
        assert self.state_machine.current_state.emotion == EmotionType.HAPPY

        # Return to listening
        success, error = self.state_machine.transition_to(StateType.LISTENING)
        assert success is True

    def test_emotion_requires_emotion_type(self):
        """Test emotion state requires emotion type"""
        self.state_machine.transition_to(StateType.ENTERING)
        self.state_machine.transition_to(StateType.LISTENING)

        # Try to transition to emotion without emotion type
        success, error = self.state_machine.transition_to(StateType.EMOTION)
        assert success is False

    def test_state_history(self):
        """Test state history tracking"""
        # Perform several transitions
        self.state_machine.transition_to(StateType.ENTERING)
        self.state_machine.transition_to(StateType.LISTENING)
        self.state_machine.transition_to(StateType.EMOTION, EmotionType.HAPPY)

        history = self.state_machine.get_state_history()
        assert len(history) >= 3

    def test_can_transition_to(self):
        """Test checking if transition is possible"""
        # From EMPTY, can go to ENTERING
        assert self.state_machine.can_transition_to(StateType.ENTERING) is True

        # From EMPTY, cannot go to LISTENING
        assert self.state_machine.can_transition_to(StateType.LISTENING) is False

    def test_reset(self):
        """Test state machine reset"""
        self.state_machine.transition_to(StateType.ENTERING)
        self.state_machine.transition_to(StateType.LISTENING)

        self.state_machine.reset()

        assert self.state_machine.current_state.state_type == StateType.EMPTY
        assert len(self.state_machine.state_history) == 0


class TestCharacterState:
    """Test character state class"""

    def test_state_creation(self):
        """Test creating character states"""
        state = CharacterState(StateType.LISTENING)
        assert state.state_type == StateType.LISTENING
        assert state.duration == 5.0

    def test_emotion_state(self):
        """Test emotion state creation"""
        state = CharacterState(StateType.EMOTION, emotion=EmotionType.HAPPY)
        assert state.emotion == EmotionType.HAPPY

    def test_video_name(self):
        """Test getting video name from state"""
        listening = CharacterState(StateType.LISTENING)
        assert listening.get_video_name() == "listening"

        happy = CharacterState(StateType.EMOTION, emotion=EmotionType.HAPPY)
        assert happy.get_video_name() == "happy"

    def test_is_interactive(self):
        """Test checking if state is interactive"""
        listening = CharacterState(StateType.LISTENING)
        assert listening.is_interactive() is True

        empty = CharacterState(StateType.EMPTY)
        assert empty.is_interactive() is False

    def test_can_trigger_emotion(self):
        """Test checking if emotion can be triggered"""
        listening = CharacterState(StateType.LISTENING)
        assert listening.can_trigger_emotion() is True

        default = CharacterState(StateType.DEFAULT)
        assert default.can_trigger_emotion() is False


if __name__ == "__main__":
    pytest.main([__file__, "-v"])

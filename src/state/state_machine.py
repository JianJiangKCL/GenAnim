"""
State Machine
Manages character state transitions and validates state changes
"""

from typing import Optional, Callable, Dict, List
from .states import CharacterState, StateType, EmotionType, TransitionType
from .transitions import TransitionManager


class StateMachine:
    """
    State machine for managing character state transitions

    Handles state validation, transition logic, and state history
    """

    def __init__(self):
        """Initialize state machine"""
        self.current_state: Optional[CharacterState] = None
        self.previous_state: Optional[CharacterState] = None
        self.state_history: List[CharacterState] = []
        self.transition_manager = TransitionManager()
        self.state_callbacks: Dict[StateType, List[Callable]] = {}

        # Initialize with empty state
        self.current_state = CharacterState(StateType.EMPTY)

    def transition_to(
        self,
        target_state: StateType,
        emotion: Optional[EmotionType] = None
    ) -> tuple[bool, Optional[str]]:
        """
        Attempt to transition to a new state

        Args:
            target_state: Target state type
            emotion: Optional emotion if transitioning to emotion state

        Returns:
            Tuple of (success: bool, error_message: Optional[str])
        """
        if not self.current_state:
            return False, "No current state set"

        # Validate transition
        is_valid, error_msg = self._validate_transition(target_state, emotion)
        if not is_valid:
            return False, error_msg

        # Get transition video if needed
        transition = self.transition_manager.get_transition(
            self.current_state.state_type,
            target_state,
            emotion
        )

        # Create new state
        new_state = CharacterState(
            state_type=target_state,
            emotion=emotion,
            loop=(target_state in [StateType.DEFAULT, StateType.LISTENING, StateType.EMPTY])
        )

        # Update states
        self.previous_state = self.current_state
        self.current_state = new_state
        self.state_history.append(new_state)

        # Trigger callbacks
        self._trigger_callbacks(target_state)

        return True, None

    def _validate_transition(
        self,
        target_state: StateType,
        emotion: Optional[EmotionType]
    ) -> tuple[bool, Optional[str]]:
        """
        Validate if transition is allowed

        Args:
            target_state: Target state
            emotion: Optional emotion

        Returns:
            Tuple of (is_valid: bool, error_message: Optional[str])
        """
        current = self.current_state.state_type

        # Define valid transitions
        valid_transitions = {
            StateType.EMPTY: [StateType.ENTERING],
            StateType.ENTERING: [StateType.LISTENING],
            StateType.DEFAULT: [StateType.LISTENING, StateType.LEAVING],
            StateType.LISTENING: [
                StateType.DEFAULT,
                StateType.SPEAKING,
                StateType.EMOTION,
                StateType.LEAVING
            ],
            StateType.SPEAKING: [StateType.LISTENING],
            StateType.EMOTION: [StateType.LISTENING],
            StateType.LEAVING: [StateType.EMPTY],
        }

        # Check if transition is valid
        allowed = valid_transitions.get(current, [])
        if target_state not in allowed:
            return False, f"Invalid transition from {current.value} to {target_state.value}"

        # Validate emotion state
        if target_state == StateType.EMOTION and emotion is None:
            return False, "Emotion type required for emotion state"

        # Cannot trigger emotion from non-interactive states
        if target_state == StateType.EMOTION and not self.current_state.can_trigger_emotion():
            return False, "Cannot trigger emotion from current state"

        return True, None

    def register_callback(self, state_type: StateType, callback: Callable) -> None:
        """
        Register a callback to be called when entering a state

        Args:
            state_type: State type to register callback for
            callback: Callback function
        """
        if state_type not in self.state_callbacks:
            self.state_callbacks[state_type] = []
        self.state_callbacks[state_type].append(callback)

    def _trigger_callbacks(self, state_type: StateType) -> None:
        """
        Trigger callbacks for a state

        Args:
            state_type: State type that was entered
        """
        callbacks = self.state_callbacks.get(state_type, [])
        for callback in callbacks:
            try:
                callback(self.current_state)
            except Exception as e:
                print(f"Error in state callback: {e}")

    def get_current_state(self) -> Optional[CharacterState]:
        """Get current state"""
        return self.current_state

    def get_previous_state(self) -> Optional[CharacterState]:
        """Get previous state"""
        return self.previous_state

    def get_state_history(self, limit: int = 10) -> List[CharacterState]:
        """
        Get recent state history

        Args:
            limit: Maximum number of states to return

        Returns:
            List of recent states
        """
        return self.state_history[-limit:]

    def reset(self) -> None:
        """Reset state machine to empty state"""
        self.current_state = CharacterState(StateType.EMPTY)
        self.previous_state = None
        self.state_history.clear()

    def can_transition_to(self, target_state: StateType) -> bool:
        """
        Check if transition to target state is possible

        Args:
            target_state: Target state to check

        Returns:
            True if transition is possible
        """
        is_valid, _ = self._validate_transition(target_state, None)
        return is_valid

    def __repr__(self) -> str:
        current = self.current_state.state_type.value if self.current_state else "None"
        previous = self.previous_state.state_type.value if self.previous_state else "None"
        return f"StateMachine(current={current}, previous={previous})"

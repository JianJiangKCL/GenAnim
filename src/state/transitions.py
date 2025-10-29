"""
Transition Manager
Handles smooth transitions between character states using first/last frame control
"""

from typing import Optional, Dict, Tuple
from .states import StateType, EmotionType, TransitionType


class Transition:
    """Represents a transition between two states"""

    def __init__(
        self,
        from_state: StateType,
        to_state: StateType,
        transition_type: TransitionType,
        video_name: str,
        duration: float = 5.0,
        description: str = ""
    ):
        """
        Initialize transition

        Args:
            from_state: Source state
            to_state: Target state
            transition_type: Type of transition
            video_name: Name of transition video file
            duration: Duration in seconds
            description: Description of the transition
        """
        self.from_state = from_state
        self.to_state = to_state
        self.transition_type = transition_type
        self.video_name = video_name
        self.duration = duration
        self.description = description

    def __repr__(self) -> str:
        return f"Transition({self.from_state.value} -> {self.to_state.value})"


class TransitionManager:
    """
    Manages transitions between character states

    Key principle: Use first/last frame control to ensure seamless transitions
    """

    def __init__(self):
        """Initialize transition manager with predefined transitions"""
        self.transitions: Dict[Tuple[StateType, StateType], Transition] = {}
        self._initialize_transitions()

    def _initialize_transitions(self) -> None:
        """Initialize all valid transitions"""

        # Default <-> Listening transitions
        self.add_transition(
            StateType.DEFAULT,
            StateType.LISTENING,
            TransitionType.DEFAULT_TO_LISTENING,
            "default2listening",
            5.0,
            "Character turns from side view to face camera"
        )

        self.add_transition(
            StateType.LISTENING,
            StateType.DEFAULT,
            TransitionType.LISTENING_TO_DEFAULT,
            "listening2default",
            5.0,
            "Character turns from facing camera to side view"
        )

        # Listening <-> Speaking (direct transition, no video needed)
        # Speaking is just listening with lip sync overlay

        # Leaving transitions
        self.add_transition(
            StateType.LISTENING,
            StateType.LEAVING,
            TransitionType.LISTENING_TO_LEAVING,
            "listening2leave",
            5.0,
            "Character runs out of frame from right side"
        )

        self.add_transition(
            StateType.DEFAULT,
            StateType.LEAVING,
            TransitionType.DEFAULT_TO_LEAVING,
            "default2leave",
            5.0,
            "Character runs out of frame from right side"
        )

        # Entering transition
        self.add_transition(
            StateType.EMPTY,
            StateType.ENTERING,
            TransitionType.EMPTY_TO_ENTERING,
            "enter",
            5.0,
            "Character peeks from left edge and enters frame"
        )

        # Note: Listening <-> Emotion transitions don't need separate videos
        # They use direct cuts since first/last frames are consistent

    def add_transition(
        self,
        from_state: StateType,
        to_state: StateType,
        transition_type: TransitionType,
        video_name: str,
        duration: float,
        description: str = ""
    ) -> None:
        """
        Add a transition

        Args:
            from_state: Source state
            to_state: Target state
            transition_type: Transition type
            video_name: Video file name
            duration: Duration in seconds
            description: Description
        """
        key = (from_state, to_state)
        self.transitions[key] = Transition(
            from_state,
            to_state,
            transition_type,
            video_name,
            duration,
            description
        )

    def get_transition(
        self,
        from_state: StateType,
        to_state: StateType,
        emotion: Optional[EmotionType] = None
    ) -> Optional[Transition]:
        """
        Get transition between two states

        Args:
            from_state: Source state
            to_state: Target state
            emotion: Optional emotion for emotion state

        Returns:
            Transition object or None if direct cut
        """
        # Emotion transitions are direct cuts (first/last frame matching)
        if to_state == StateType.EMOTION or from_state == StateType.EMOTION:
            return None

        # Speaking transitions are direct overlays
        if to_state == StateType.SPEAKING or from_state == StateType.SPEAKING:
            return None

        key = (from_state, to_state)
        return self.transitions.get(key)

    def requires_transition_video(
        self,
        from_state: StateType,
        to_state: StateType
    ) -> bool:
        """
        Check if transition requires a transition video

        Args:
            from_state: Source state
            to_state: Target state

        Returns:
            True if transition video is needed
        """
        transition = self.get_transition(from_state, to_state)
        return transition is not None

    def get_all_transitions(self) -> list[Transition]:
        """Get all registered transitions"""
        return list(self.transitions.values())

    def get_transitions_from(self, state: StateType) -> list[Transition]:
        """
        Get all transitions from a specific state

        Args:
            state: Source state

        Returns:
            List of transitions from this state
        """
        return [
            trans for (from_st, _), trans in self.transitions.items()
            if from_st == state
        ]

    def get_transitions_to(self, state: StateType) -> list[Transition]:
        """
        Get all transitions to a specific state

        Args:
            state: Target state

        Returns:
            List of transitions to this state
        """
        return [
            trans for (_, to_st), trans in self.transitions.items()
            if to_st == state
        ]

    def __repr__(self) -> str:
        return f"TransitionManager({len(self.transitions)} transitions)"

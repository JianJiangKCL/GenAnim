"""
Character Class
Main character entity that manages profile, state, and behavior
"""

from typing import Optional, Dict, Any
from .profile import CharacterProfile
from ..state.states import CharacterState, StateType


class Character:
    """
    Main character entity for HooRii Agent system
    Manages character profile, current state, and interactions
    """

    def __init__(
        self,
        character_id: str,
        profile: CharacterProfile,
        initial_state: StateType = StateType.DEFAULT
    ):
        """
        Initialize character

        Args:
            character_id: Unique character identifier
            profile: Character profile with appearance and personality
            initial_state: Initial state of the character
        """
        self.character_id = character_id
        self.profile = profile
        self.current_state: Optional[CharacterState] = None
        self.previous_state: Optional[CharacterState] = None
        self.is_online = False
        self.is_connected = False
        self.current_device: Optional[str] = None

        # Initialize with default state
        self._set_state(CharacterState(initial_state))

    def _set_state(self, new_state: CharacterState) -> None:
        """
        Internal method to set character state

        Args:
            new_state: New state to set
        """
        self.previous_state = self.current_state
        self.current_state = new_state

    def get_state(self) -> Optional[CharacterState]:
        """Get current character state"""
        return self.current_state

    def get_state_type(self) -> Optional[StateType]:
        """Get current state type"""
        return self.current_state.state_type if self.current_state else None

    def set_online(self, online: bool = True) -> None:
        """
        Set character online status

        Args:
            online: Whether character is online
        """
        self.is_online = online
        if not online:
            self.is_connected = False

    def connect(self) -> bool:
        """
        Connect to character (start interaction)

        Returns:
            True if connection successful
        """
        if not self.is_online:
            return False

        self.is_connected = True
        return True

    def disconnect(self) -> None:
        """Disconnect from character (end interaction)"""
        self.is_connected = False

    def set_device(self, device_id: str) -> None:
        """
        Set current device where character is active

        Args:
            device_id: Device identifier
        """
        self.current_device = device_id

    def get_status(self) -> Dict[str, Any]:
        """
        Get complete character status

        Returns:
            Dictionary with character status information
        """
        return {
            'character_id': self.character_id,
            'nickname': self.profile.nickname,
            'is_online': self.is_online,
            'is_connected': self.is_connected,
            'current_state': self.get_state_type().value if self.current_state else None,
            'current_device': self.current_device,
            'previous_state': self.previous_state.state_type.value if self.previous_state else None
        }

    def __repr__(self) -> str:
        state = self.get_state_type().value if self.current_state else 'None'
        return (f"Character(id='{self.character_id}', "
                f"nickname='{self.profile.nickname}', "
                f"state='{state}', "
                f"online={self.is_online}, "
                f"connected={self.is_connected})")

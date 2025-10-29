"""
Device Sync Manager
Handles synchronization of character state and memory across devices
"""

from typing import Dict, Any, Optional
from datetime import datetime
from ..state.states import CharacterState, StateType


class DeviceSyncManager:
    """
    Manages synchronization of character data across devices

    Ensures character maintains consistent memory and interaction history
    when switching between devices
    """

    def __init__(self):
        """Initialize sync manager"""
        self.character_data: Dict[str, Any] = {}
        self.last_sync: Optional[datetime] = None
        self.sync_history: list = []

    def sync_character_state(
        self,
        character_id: str,
        state: CharacterState,
        device_id: str
    ) -> None:
        """
        Sync character state to cloud/storage

        Args:
            character_id: Character identifier
            state: Current character state
            device_id: Device where state changed
        """
        sync_data = {
            'character_id': character_id,
            'state': state.state_type.value,
            'emotion': state.emotion.value if state.emotion else None,
            'device_id': device_id,
            'timestamp': datetime.now().isoformat()
        }

        self.character_data[character_id] = sync_data
        self.last_sync = datetime.now()
        self.sync_history.append(sync_data)

        print(f"[Sync] Character state synced: {sync_data}")

    def get_character_state(self, character_id: str) -> Optional[Dict[str, Any]]:
        """
        Get synced character state

        Args:
            character_id: Character identifier

        Returns:
            Character state data or None
        """
        return self.character_data.get(character_id)

    def sync_conversation_history(
        self,
        character_id: str,
        messages: list,
        device_id: str
    ) -> None:
        """
        Sync conversation history

        Args:
            character_id: Character identifier
            messages: List of conversation messages
            device_id: Device where conversation happened
        """
        sync_data = {
            'character_id': character_id,
            'messages': messages,
            'device_id': device_id,
            'timestamp': datetime.now().isoformat()
        }

        key = f"{character_id}_history"
        self.character_data[key] = sync_data
        self.last_sync = datetime.now()

        print(f"[Sync] Conversation history synced: {len(messages)} messages")

    def get_conversation_history(self, character_id: str) -> list:
        """
        Get synced conversation history

        Args:
            character_id: Character identifier

        Returns:
            List of conversation messages
        """
        key = f"{character_id}_history"
        data = self.character_data.get(key, {})
        return data.get('messages', [])

    def sync_character_memory(
        self,
        character_id: str,
        memory_data: Dict[str, Any],
        device_id: str
    ) -> None:
        """
        Sync character memory/context

        Args:
            character_id: Character identifier
            memory_data: Memory data to sync
            device_id: Device where memory was updated
        """
        sync_data = {
            'character_id': character_id,
            'memory': memory_data,
            'device_id': device_id,
            'timestamp': datetime.now().isoformat()
        }

        key = f"{character_id}_memory"
        self.character_data[key] = sync_data
        self.last_sync = datetime.now()

        print(f"[Sync] Character memory synced")

    def get_character_memory(self, character_id: str) -> Dict[str, Any]:
        """
        Get synced character memory

        Args:
            character_id: Character identifier

        Returns:
            Memory data dictionary
        """
        key = f"{character_id}_memory"
        data = self.character_data.get(key, {})
        return data.get('memory', {})

    def sync_device_switch(
        self,
        character_id: str,
        from_device: Optional[str],
        to_device: str
    ) -> None:
        """
        Record device switch event

        Args:
            character_id: Character identifier
            from_device: Previous device ID
            to_device: New device ID
        """
        switch_data = {
            'character_id': character_id,
            'from_device': from_device,
            'to_device': to_device,
            'timestamp': datetime.now().isoformat()
        }

        self.sync_history.append(switch_data)
        print(f"[Sync] Device switch recorded: {from_device} -> {to_device}")

    def get_sync_status(self) -> Dict[str, Any]:
        """
        Get synchronization status

        Returns:
            Dictionary with sync status
        """
        return {
            'last_sync': self.last_sync.isoformat() if self.last_sync else None,
            'synced_characters': len([k for k in self.character_data.keys() if not k.endswith('_history') and not k.endswith('_memory')]),
            'sync_history_count': len(self.sync_history),
            'total_data_keys': len(self.character_data)
        }

    def clear_sync_data(self, character_id: Optional[str] = None) -> None:
        """
        Clear sync data

        Args:
            character_id: Specific character to clear, or None to clear all
        """
        if character_id:
            # Clear specific character data
            keys_to_remove = [
                k for k in self.character_data.keys()
                if k.startswith(character_id)
            ]
            for key in keys_to_remove:
                del self.character_data[key]
            print(f"[Sync] Cleared data for character: {character_id}")
        else:
            # Clear all data
            self.character_data.clear()
            self.sync_history.clear()
            print("[Sync] Cleared all sync data")

    def get_recent_sync_history(self, limit: int = 10) -> list:
        """
        Get recent sync history

        Args:
            limit: Maximum number of records to return

        Returns:
            List of recent sync events
        """
        return self.sync_history[-limit:]

    def __repr__(self) -> str:
        return f"DeviceSyncManager(synced={len(self.character_data)}, last_sync={self.last_sync})"

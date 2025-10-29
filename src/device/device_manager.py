"""
Device Manager
Manages character presence across multiple devices
"""

from enum import Enum
from typing import Optional, Dict, List
from dataclasses import dataclass
from datetime import datetime


class DeviceType(Enum):
    """Types of devices"""
    HARDWARE = "hardware"  # Desktop hardware device
    MOBILE = "mobile"  # Mobile app
    DESKTOP = "desktop"  # Desktop app
    WEB = "web"  # Web browser


@dataclass
class Device:
    """Represents a device in the system"""
    device_id: str
    device_type: DeviceType
    name: str
    is_active: bool = False
    last_active: Optional[datetime] = None

    def activate(self) -> None:
        """Activate this device"""
        self.is_active = True
        self.last_active = datetime.now()

    def deactivate(self) -> None:
        """Deactivate this device"""
        self.is_active = False

    def __repr__(self) -> str:
        return f"Device(id='{self.device_id}', type={self.device_type.value}, active={self.is_active})"


class DeviceManager:
    """
    Manages character presence across multiple devices

    Key principle: Character can only be active on ONE device at a time.
    When switching devices, character "leaves" current device and "enters" new device.
    """

    def __init__(self, user_id: str):
        """
        Initialize device manager for a user

        Args:
            user_id: User identifier
        """
        self.user_id = user_id
        self.devices: Dict[str, Device] = {}
        self.active_device: Optional[Device] = None

    def register_device(
        self,
        device_id: str,
        device_type: DeviceType,
        name: str
    ) -> Device:
        """
        Register a new device

        Args:
            device_id: Unique device identifier
            device_type: Type of device
            name: Device name

        Returns:
            Created device
        """
        device = Device(
            device_id=device_id,
            device_type=device_type,
            name=name,
            is_active=False
        )
        self.devices[device_id] = device
        return device

    def get_device(self, device_id: str) -> Optional[Device]:
        """
        Get device by ID

        Args:
            device_id: Device identifier

        Returns:
            Device or None if not found
        """
        return self.devices.get(device_id)

    def get_active_device(self) -> Optional[Device]:
        """Get currently active device"""
        return self.active_device

    def switch_device(
        self,
        from_device_id: Optional[str],
        to_device_id: str
    ) -> tuple[bool, Optional[str]]:
        """
        Switch character from one device to another

        This triggers:
        1. Character leaves current device (play leave animation)
        2. Current device shows empty state
        3. Target device shows enter animation
        4. Character enters listening state on target device

        Args:
            from_device_id: Current device ID (None if character is offline)
            to_device_id: Target device ID

        Returns:
            Tuple of (success, error_message)
        """
        # Validate target device exists
        to_device = self.devices.get(to_device_id)
        if not to_device:
            return False, f"Target device not found: {to_device_id}"

        # If there's an active device, deactivate it
        if from_device_id:
            from_device = self.devices.get(from_device_id)
            if from_device:
                from_device.deactivate()

        # Deactivate current active device if different
        if self.active_device and self.active_device.device_id != to_device_id:
            self.active_device.deactivate()

        # Activate target device
        to_device.activate()
        self.active_device = to_device

        return True, None

    def character_leave_device(self, device_id: str) -> tuple[bool, Optional[str]]:
        """
        Character leaves a device

        Args:
            device_id: Device to leave

        Returns:
            Tuple of (success, error_message)
        """
        device = self.devices.get(device_id)
        if not device:
            return False, f"Device not found: {device_id}"

        device.deactivate()

        if self.active_device and self.active_device.device_id == device_id:
            self.active_device = None

        return True, None

    def character_enter_device(self, device_id: str) -> tuple[bool, Optional[str]]:
        """
        Character enters a device

        Args:
            device_id: Device to enter

        Returns:
            Tuple of (success, error_message)
        """
        device = self.devices.get(device_id)
        if not device:
            return False, f"Device not found: {device_id}"

        # Deactivate any currently active device
        if self.active_device:
            self.active_device.deactivate()

        # Activate target device
        device.activate()
        self.active_device = device

        return True, None

    def get_all_devices(self) -> List[Device]:
        """Get all registered devices"""
        return list(self.devices.values())

    def get_devices_by_type(self, device_type: DeviceType) -> List[Device]:
        """
        Get all devices of a specific type

        Args:
            device_type: Device type to filter

        Returns:
            List of matching devices
        """
        return [
            device for device in self.devices.values()
            if device.device_type == device_type
        ]

    def is_character_online(self) -> bool:
        """Check if character is online on any device"""
        return self.active_device is not None

    def get_status(self) -> Dict:
        """
        Get complete device status

        Returns:
            Dictionary with device manager status
        """
        return {
            'user_id': self.user_id,
            'total_devices': len(self.devices),
            'active_device': self.active_device.device_id if self.active_device else None,
            'character_online': self.is_character_online(),
            'devices': [
                {
                    'id': d.device_id,
                    'type': d.device_type.value,
                    'name': d.name,
                    'active': d.is_active
                }
                for d in self.devices.values()
            ]
        }

    def __repr__(self) -> str:
        active = self.active_device.device_id if self.active_device else "None"
        return f"DeviceManager(user='{self.user_id}', devices={len(self.devices)}, active='{active}')"

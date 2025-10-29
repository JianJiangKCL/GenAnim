"""Device management module for multi-device character switching"""

from .device_manager import DeviceManager, Device, DeviceType
from .sync import DeviceSyncManager

__all__ = ["DeviceManager", "Device", "DeviceType", "DeviceSyncManager"]

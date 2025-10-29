"""
Device Switching Example
Demonstrates multi-device character switching
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from src.character import Character, CharacterProfile
from src.state import StateMachine, StateType
from src.device import DeviceManager, DeviceType, DeviceSyncManager


def main():
    print("=== Multi-Device Switching Example ===\n")

    # 1. Setup character
    profile = CharacterProfile("config/character_config.json")
    character = Character("char_001", profile)
    state_machine = StateMachine()

    # 2. Setup device manager
    print("1. Setting up devices...")
    device_mgr = DeviceManager(user_id="user_123")

    # Register devices
    device_mgr.register_device("hw1", DeviceType.HARDWARE, "Desktop Hardware")
    device_mgr.register_device("mobile1", DeviceType.MOBILE, "iPhone 15")
    device_mgr.register_device("desktop1", DeviceType.DESKTOP, "MacBook Pro")

    print(f"   Registered {len(device_mgr.get_all_devices())} devices")
    for device in device_mgr.get_all_devices():
        print(f"   - {device.name} ({device.device_type.value})")
    print()

    # 3. Setup sync manager
    sync_mgr = DeviceSyncManager()

    # 4. Character enters hardware device
    print("2. Character entering hardware device...")
    character.set_online(True)
    device_mgr.character_enter_device("hw1")
    state_machine.transition_to(StateType.ENTERING)
    state_machine.transition_to(StateType.LISTENING)

    print(f"   Character on: {device_mgr.get_active_device().name}")
    print(f"   State: {state_machine.get_current_state()}\n")

    # Sync state
    sync_mgr.sync_character_state(
        character.character_id,
        state_machine.get_current_state(),
        "hw1"
    )

    # 5. Switch to mobile
    print("3. Switching to mobile device...")
    print("   → Character leaving hardware...")
    state_machine.transition_to(StateType.LEAVING)
    state_machine.transition_to(StateType.EMPTY)

    success, error = device_mgr.switch_device("hw1", "mobile1")
    if success:
        print(f"   ✓ Switched to: {device_mgr.get_active_device().name}")
    else:
        print(f"   ✗ Switch failed: {error}")

    print("   → Character entering mobile...")
    state_machine.transition_to(StateType.ENTERING)
    state_machine.transition_to(StateType.LISTENING)

    # Sync device switch
    sync_mgr.sync_device_switch(character.character_id, "hw1", "mobile1")
    sync_mgr.sync_character_state(
        character.character_id,
        state_machine.get_current_state(),
        "mobile1"
    )
    print()

    # 6. Switch to desktop
    print("4. Switching to desktop device...")
    print("   → Character leaving mobile...")
    state_machine.transition_to(StateType.LEAVING)
    state_machine.transition_to(StateType.EMPTY)

    success, error = device_mgr.switch_device("mobile1", "desktop1")
    if success:
        print(f"   ✓ Switched to: {device_mgr.get_active_device().name}")

    print("   → Character entering desktop...")
    state_machine.transition_to(StateType.ENTERING)
    state_machine.transition_to(StateType.LISTENING)

    sync_mgr.sync_device_switch(character.character_id, "mobile1", "desktop1")
    print()

    # 7. Show sync status
    print("5. Synchronization status:")
    status = sync_mgr.get_sync_status()
    for key, value in status.items():
        print(f"   {key}: {value}")

    print("\n6. Recent sync history:")
    for event in sync_mgr.get_recent_sync_history(3):
        if 'from_device' in event:
            print(f"   Switch: {event['from_device']} → {event['to_device']}")

    print("\n7. Final device status:")
    print(f"   Active device: {device_mgr.get_active_device().name}")
    print(f"   Character online: {device_mgr.is_character_online()}")
    print(f"   Current state: {state_machine.get_current_state()}")

    print("\n=== Example Complete ===")


if __name__ == "__main__":
    main()

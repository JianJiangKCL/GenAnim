"""
Basic Usage Example
Demonstrates basic character creation and state management
"""

import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.character import Character, CharacterProfile
from src.state import StateMachine, StateType, EmotionType


def main():
    print("=== GenAnim Basic Usage Example ===\n")

    # 1. Load character profile
    print("1. Loading character profile...")
    profile = CharacterProfile("config/character_config.json")
    print(f"   Loaded character: {profile.nickname}")
    print(f"   Traits: {', '.join(profile.personality_traits)}\n")

    # 2. Create character
    print("2. Creating character...")
    character = Character(
        character_id="hoorii_001",
        profile=profile
    )
    print(f"   Character created: {character}\n")

    # 3. Initialize state machine
    print("3. Initializing state machine...")
    state_machine = StateMachine()
    print(f"   Initial state: {state_machine.get_current_state()}\n")

    # 4. Character goes online
    print("4. Character going online...")
    character.set_online(True)
    state_machine.transition_to(StateType.ENTERING)
    state_machine.transition_to(StateType.LISTENING)
    print(f"   Current state: {state_machine.get_current_state()}\n")

    # 5. User connects
    print("5. User connecting...")
    character.connect()
    print(f"   Character status: {character.get_status()}\n")

    # 6. Trigger emotions
    print("6. Triggering emotions...")
    emotions_to_test = [
        EmotionType.HAPPY,
        EmotionType.SURPRISED,
        EmotionType.CONFUSED
    ]

    for emotion in emotions_to_test:
        success, error = state_machine.transition_to(
            StateType.EMOTION,
            emotion=emotion
        )
        if success:
            print(f"   ✓ Triggered emotion: {emotion.value}")
            # Return to listening
            state_machine.transition_to(StateType.LISTENING)
        else:
            print(f"   ✗ Failed to trigger {emotion.value}: {error}")

    print("\n7. Character state history:")
    history = state_machine.get_state_history(5)
    for i, state in enumerate(history[-5:], 1):
        print(f"   {i}. {state}")

    print("\n=== Example Complete ===")


if __name__ == "__main__":
    main()

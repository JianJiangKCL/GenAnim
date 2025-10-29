"""
Prompt Generation Example
Demonstrates video prompt generation for different states
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from src.character import CharacterProfile
from src.video import PromptGenerator
from src.state import CharacterState, StateType, EmotionType


def main():
    print("=== Video Prompt Generation Example ===\n")

    # 1. Load character profile
    profile = CharacterProfile("config/character_config.json")
    print(f"Character: {profile.nickname}\n")

    # 2. Create prompt generator
    prompt_gen = PromptGenerator(profile)

    # 3. Generate character image prompt
    print("1. Character Image Prompt:")
    print("-" * 60)
    image_prompt = prompt_gen.generate_image_prompt(with_background=True)
    print(image_prompt)
    print()

    # 4. Generate state prompts
    print("2. State Prompts:")
    print("-" * 60)

    states = [
        CharacterState(StateType.DEFAULT),
        CharacterState(StateType.LISTENING),
        CharacterState(StateType.SPEAKING),
    ]

    for state in states:
        print(f"\n{state.state_type.value.upper()}:")
        prompt = prompt_gen.generate_state_prompt(state)
        print(prompt)

    # 5. Generate emotion prompts
    print("\n3. Emotion Prompts:")
    print("-" * 60)

    emotions = [
        EmotionType.HAPPY,
        EmotionType.SURPRISED,
        EmotionType.ANGRY,
        EmotionType.SAD
    ]

    for emotion in emotions:
        state = CharacterState(StateType.EMOTION, emotion=emotion)
        print(f"\n{emotion.value.upper()}:")
        prompt = prompt_gen.generate_state_prompt(state)
        print(prompt)

    # 6. Generate transition prompts
    print("\n4. Transition Prompts:")
    print("-" * 60)

    transitions = [
        (StateType.DEFAULT, StateType.LISTENING),
        (StateType.LISTENING, StateType.DEFAULT),
    ]

    for from_state, to_state in transitions:
        print(f"\n{from_state.value} → {to_state.value}:")
        prompt = prompt_gen.generate_transition_prompt(from_state, to_state)
        if prompt:
            print(prompt)
        else:
            print("(No transition video needed - direct cut)")

    # 7. Save all prompts to files
    print("\n\n5. Saving prompts to files...")
    prompt_gen.save_prompts_to_file("prompts")
    print("   ✓ Prompts saved to 'prompts/' directory")

    print("\n=== Example Complete ===")


if __name__ == "__main__":
    main()

"""
Prompt Generator
Generates prompts for AI video generation based on character state
"""

from typing import Dict, Optional
from pathlib import Path
from ..state.states import StateType, EmotionType, CharacterState
from ..character.profile import CharacterProfile


class PromptGenerator:
    """
    Generates prompts for video generation based on character states

    Combines character appearance, state requirements, and technical parameters
    """

    def __init__(self, character_profile: CharacterProfile):
        """
        Initialize prompt generator

        Args:
            character_profile: Character profile with appearance info
        """
        self.profile = character_profile
        self.base_appearance = self._get_base_appearance()

    def _get_base_appearance(self) -> str:
        """Get base appearance description from character profile"""
        appearance = self.profile.get_appearance_info()
        return (
            f"{appearance.get('art_style', '')}, "
            f"{appearance.get('clothing', '')}, "
            f"{appearance.get('face', '')}, "
            f"{appearance.get('hairstyle', '')}"
        )

    def generate_state_prompt(
        self,
        state: CharacterState,
        include_technical: bool = True
    ) -> str:
        """
        Generate complete prompt for a character state

        Args:
            state: Character state to generate prompt for
            include_technical: Include technical parameters

        Returns:
            Complete prompt string
        """
        # Get state-specific action/pose
        action = self._get_state_action(state)

        # Build prompt parts
        prompt_parts = [
            self.base_appearance,
            action,
            "white background" if state.state_type != StateType.DEFAULT else "",
            "camera fixed, no camera movement",
            "smooth animation, no distortion, no frame skipping"
        ]

        if include_technical:
            prompt_parts.extend([
                "9:16 aspect ratio",
                "high quality, 2K resolution",
                "24fps",
                "clear face details"
            ])

        # Filter empty parts and join
        prompt = ", ".join(filter(None, prompt_parts))
        return prompt

    def _get_state_action(self, state: CharacterState) -> str:
        """
        Get action/pose description for a state

        Args:
            state: Character state

        Returns:
            Action description string
        """
        actions = {
            StateType.DEFAULT: (
                "girl looking to the left side, facing left, "
                "two arms behind back, body still, "
                "occasionally blinks, hair gently blown by wind"
            ),
            StateType.LISTENING: (
                "create a 5s video, girl's hair naturally blown by wind, "
                "blinks occasionally"
            ),
            StateType.SPEAKING: (
                "girl is speaking, hair naturally blown by wind, "
                "occasionally blinks, head can naturally tilt slightly, "
                "very small movements"
            ),
            StateType.LEAVING: (
                "girl quickly leaves the frame, runs out from the right side, "
                "only pure white background left, smooth natural motion, "
                "no distortion, smooth running pose"
            ),
            StateType.ENTERING: (
                "create a 5s video, first frame has no person, "
                "only pure white background, then person peeks from left edge, "
                "then walks into frame, facing camera, "
                "throughout process person's frame proportion unchanged, "
                "person details remain consistent"
            ),
        }

        # Handle emotion states
        if state.state_type == StateType.EMOTION and state.emotion:
            emotion_actions = {
                EmotionType.NEUTRAL: actions[StateType.LISTENING],
                EmotionType.HAPPY: (
                    "create a 5s video, girl happily smiles, blushing, "
                    "tilts head, camera fixed"
                ),
                EmotionType.SHY: (
                    "Shot 1: girl hears something and looks down shyly, blushing. "
                    "Shot 2: girl returns from shy to calm state"
                ),
                EmotionType.SURPRISED: (
                    "girl looks like she was frightened by something, "
                    "surprised expression, body jolts, steps back two steps, "
                    "shoulders raised, looks around nervously"
                ),
                EmotionType.SMUG: (
                    "girl crosses arms in front of chest, "
                    "confident and proud look, then lowers arms"
                ),
                EmotionType.ANGRY: (
                    "girl is angry, teeth clenched, frowning, "
                    "then returns to calm"
                ),
                EmotionType.CONFUSED: (
                    "girl frowns, serious expression, very confused look, "
                    "one hand on chin, as if thinking about something, "
                    "camera fixed"
                ),
                EmotionType.SAD: (
                    "girl frowns, takes a deep breath, "
                    "slightly lowers head, eyes looking down"
                ),
                EmotionType.SLEEPY: (
                    "girl looks very tired, eyes about to close, "
                    "head drooping down, body slightly swaying"
                ),
            }
            return emotion_actions.get(state.emotion, "")

        return actions.get(state.state_type, "")

    def generate_transition_prompt(
        self,
        from_state: StateType,
        to_state: StateType
    ) -> str:
        """
        Generate prompt for state transition

        Args:
            from_state: Source state
            to_state: Target state

        Returns:
            Transition prompt string
        """
        transition_prompts = {
            (StateType.DEFAULT, StateType.LISTENING): (
                f"{self.base_appearance}, "
                "girl turns from left side to front, looking at camera, "
                "hands at body sides, smooth natural motion, "
                "no distortion, no frame skipping"
            ),
            (StateType.LISTENING, StateType.DEFAULT): (
                f"{self.base_appearance}, "
                "girl turns from front to left side, hands behind back, "
                "smooth natural motion, no distortion, no frame skipping"
            ),
        }

        key = (from_state, to_state)
        return transition_prompts.get(key, "")

    def generate_image_prompt(self, with_background: bool = False) -> str:
        """
        Generate prompt for character image generation

        Args:
            with_background: Include scene background

        Returns:
            Image generation prompt
        """
        appearance = self.profile.get_appearance_info()
        character = self.profile.get_character_info()

        parts = [
            appearance.get('art_style', ''),
            appearance.get('clothing', ''),
            appearance.get('face', ''),
            appearance.get('hairstyle', ''),
        ]

        if with_background:
            parts.extend([
                appearance.get('pose', ''),
                appearance.get('scene', ''),
                appearance.get('atmosphere', '')
            ])
        else:
            parts.append("standing facing camera, half/full body")
            parts.append("white background")

        parts.extend([
            "9:16 aspect ratio",
            "high quality",
            "face high definition",
            "detailed"
        ])

        return ", ".join(filter(None, parts))

    def save_prompts_to_file(self, output_dir: str) -> None:
        """
        Save all prompts to text files

        Args:
            output_dir: Directory to save prompt files
        """
        output_path = Path(output_dir)
        output_path.mkdir(parents=True, exist_ok=True)

        # Save image prompt
        with open(output_path / "character_image.txt", 'w', encoding='utf-8') as f:
            f.write(self.generate_image_prompt(with_background=True))

        # Save state prompts
        for state_type in StateType:
            state = CharacterState(state_type)
            prompt = self.generate_state_prompt(state)
            filename = f"{state_type.value}_state.txt"
            with open(output_path / filename, 'w', encoding='utf-8') as f:
                f.write(prompt)

        # Save emotion prompts
        emotions_dir = output_path / "emotions"
        emotions_dir.mkdir(exist_ok=True)
        for emotion in EmotionType:
            state = CharacterState(StateType.EMOTION, emotion=emotion)
            prompt = self.generate_state_prompt(state)
            filename = f"{emotion.value}.txt"
            with open(emotions_dir / filename, 'w', encoding='utf-8') as f:
                f.write(prompt)

    def __repr__(self) -> str:
        return f"PromptGenerator(character='{self.profile.nickname}')"

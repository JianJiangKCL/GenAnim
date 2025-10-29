"""
Character Profile Management
Handles loading and managing character configuration data
"""

import json
from typing import Dict, Any, Optional
from pathlib import Path


class CharacterProfile:
    """Manages character profile information including appearance and personality"""

    def __init__(self, config_path: Optional[str] = None):
        """
        Initialize character profile from configuration file

        Args:
            config_path: Path to character configuration JSON file
        """
        self.config_path = config_path
        self.data: Dict[str, Any] = {}

        if config_path:
            self.load_from_file(config_path)

    def load_from_file(self, file_path: str) -> None:
        """
        Load character configuration from JSON file

        Args:
            file_path: Path to configuration file
        """
        path = Path(file_path)
        if not path.exists():
            raise FileNotFoundError(f"Character config file not found: {file_path}")

        with open(path, 'r', encoding='utf-8') as f:
            self.data = json.load(f)

    def get_character_info(self) -> Dict[str, Any]:
        """Get basic character information"""
        return self.data.get('character', {})

    def get_appearance_info(self) -> Dict[str, Any]:
        """Get character appearance information"""
        return self.data.get('appearance', {})

    @property
    def nickname(self) -> str:
        """Get character nickname"""
        return self.get_character_info().get('nickname', 'Unknown')

    @property
    def personality_traits(self) -> list:
        """Get character personality traits"""
        personality = self.get_character_info().get('personality', {})
        return personality.get('traits', [])

    @property
    def art_style(self) -> str:
        """Get character art style"""
        return self.get_appearance_info().get('art_style', '')

    def get_image_prompt(self) -> str:
        """
        Generate complete image generation prompt from character configuration

        Returns:
            Complete prompt string for image generation
        """
        appearance = self.get_appearance_info()
        character = self.get_character_info()

        prompt_parts = [
            f"Art style: {appearance.get('art_style', '')}",
            f"Clothing: {appearance.get('clothing', '')}",
            f"Face: {appearance.get('face', '')}",
            f"Hairstyle: {appearance.get('hairstyle', '')}",
            f"Pose: {appearance.get('pose', '')}",
            f"Scene: {appearance.get('scene', '')}",
            f"Atmosphere: {appearance.get('atmosphere', '')}",
            f"Personality: {', '.join(character.get('personality', {}).get('traits', []))}",
        ]

        image_settings = appearance.get('image_settings', {})
        prompt_parts.append(
            f"Image settings: {image_settings.get('aspect_ratio', '9:16')}, "
            f"high quality, face high definition, detailed"
        )

        return ". ".join(filter(None, prompt_parts))

    def to_dict(self) -> Dict[str, Any]:
        """Convert profile to dictionary"""
        return self.data

    def __repr__(self) -> str:
        return f"CharacterProfile(nickname='{self.nickname}')"

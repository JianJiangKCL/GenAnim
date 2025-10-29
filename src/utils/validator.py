"""
Configuration Validator
Validates configuration files and data
"""

from typing import Dict, Any, List, Optional
import json
from pathlib import Path


class ValidationError(Exception):
    """Validation error exception"""
    pass


class ConfigValidator:
    """Validates configuration files and data"""

    @staticmethod
    def validate_character_config(config: Dict[str, Any]) -> tuple[bool, Optional[str]]:
        """
        Validate character configuration

        Args:
            config: Character configuration dictionary

        Returns:
            Tuple of (is_valid, error_message)
        """
        required_fields = {
            'character': ['nickname', 'gender', 'age', 'personality'],
            'appearance': ['art_style', 'clothing', 'face', 'hairstyle']
        }

        try:
            # Check top-level keys
            for key in required_fields.keys():
                if key not in config:
                    return False, f"Missing required section: {key}"

            # Check character fields
            character = config.get('character', {})
            for field in required_fields['character']:
                if field not in character:
                    return False, f"Missing character field: {field}"

            # Check appearance fields
            appearance = config.get('appearance', {})
            for field in required_fields['appearance']:
                if field not in appearance:
                    return False, f"Missing appearance field: {field}"

            # Validate age is positive
            age = character.get('age')
            if not isinstance(age, int) or age <= 0:
                return False, "Age must be a positive integer"

            return True, None

        except Exception as e:
            return False, str(e)

    @staticmethod
    def validate_video_params(config: Dict[str, Any]) -> tuple[bool, Optional[str]]:
        """
        Validate video parameters configuration

        Args:
            config: Video parameters dictionary

        Returns:
            Tuple of (is_valid, error_message)
        """
        try:
            video_params = config.get('video_parameters', {})

            # Check required fields
            required = ['aspect_ratio', 'resolution', 'frame_rate', 'format']
            for field in required:
                if field not in video_params:
                    return False, f"Missing video parameter: {field}"

            # Validate frame rate
            fps = video_params.get('frame_rate')
            if not isinstance(fps, int) or fps <= 0:
                return False, "Frame rate must be a positive integer"

            # Validate aspect ratio format
            aspect = video_params.get('aspect_ratio', '')
            if ':' not in aspect:
                return False, "Invalid aspect ratio format (should be like 9:16)"

            return True, None

        except Exception as e:
            return False, str(e)

    @staticmethod
    def validate_emotion_keywords(config: Dict[str, Any]) -> tuple[bool, Optional[str]]:
        """
        Validate emotion keywords configuration

        Args:
            config: Emotion keywords dictionary

        Returns:
            Tuple of (is_valid, error_message)
        """
        try:
            triggers = config.get('emotion_triggers', {})

            if not triggers:
                return False, "No emotion triggers defined"

            # Check each emotion has required fields
            for emotion, data in triggers.items():
                if 'keywords' not in data:
                    return False, f"Emotion '{emotion}' missing keywords field"

                if 'description' not in data:
                    return False, f"Emotion '{emotion}' missing description field"

                if not isinstance(data['keywords'], list):
                    return False, f"Emotion '{emotion}' keywords must be a list"

            return True, None

        except Exception as e:
            return False, str(e)

    @staticmethod
    def validate_json_file(file_path: str) -> tuple[bool, Optional[str]]:
        """
        Validate JSON file can be loaded

        Args:
            file_path: Path to JSON file

        Returns:
            Tuple of (is_valid, error_message)
        """
        try:
            path = Path(file_path)

            if not path.exists():
                return False, f"File does not exist: {file_path}"

            with open(path, 'r', encoding='utf-8') as f:
                json.load(f)

            return True, None

        except json.JSONDecodeError as e:
            return False, f"Invalid JSON: {str(e)}"
        except Exception as e:
            return False, str(e)

    @staticmethod
    def validate_all_configs(config_dir: str) -> Dict[str, Any]:
        """
        Validate all configuration files in directory

        Args:
            config_dir: Configuration directory path

        Returns:
            Dictionary with validation results
        """
        config_path = Path(config_dir)
        results = {}

        # Validate character config
        char_config = config_path / "character_config.json"
        if char_config.exists():
            with open(char_config, 'r', encoding='utf-8') as f:
                config = json.load(f)
                is_valid, error = ConfigValidator.validate_character_config(config)
                results['character_config'] = {
                    'valid': is_valid,
                    'error': error
                }

        # Validate video params
        video_config = config_path / "video_params.json"
        if video_config.exists():
            with open(video_config, 'r', encoding='utf-8') as f:
                config = json.load(f)
                is_valid, error = ConfigValidator.validate_video_params(config)
                results['video_params'] = {
                    'valid': is_valid,
                    'error': error
                }

        # Validate emotion keywords
        emotion_config = config_path / "emotion_keywords.json"
        if emotion_config.exists():
            with open(emotion_config, 'r', encoding='utf-8') as f:
                config = json.load(f)
                is_valid, error = ConfigValidator.validate_emotion_keywords(config)
                results['emotion_keywords'] = {
                    'valid': is_valid,
                    'error': error
                }

        return results

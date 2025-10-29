"""
Video Generator
Interface for AI video generation models
"""

from typing import Optional, Dict, Any
from pathlib import Path
import json
from ..state.states import CharacterState
from .prompts import PromptGenerator


class VideoGenerationRequest:
    """Represents a video generation request"""

    def __init__(
        self,
        prompt: str,
        state: CharacterState,
        reference_image: Optional[str] = None,
        first_frame: Optional[str] = None,
        last_frame: Optional[str] = None,
        duration: float = 5.0,
        model: str = "Seedream V4"
    ):
        """
        Initialize video generation request

        Args:
            prompt: Text prompt for generation
            state: Character state
            reference_image: Reference image path for image-to-video
            first_frame: First frame image path for frame control
            last_frame: Last frame image path for frame control
            duration: Video duration in seconds
            model: AI model to use
        """
        self.prompt = prompt
        self.state = state
        self.reference_image = reference_image
        self.first_frame = first_frame
        self.last_frame = last_frame
        self.duration = duration
        self.model = model

    def to_dict(self) -> Dict[str, Any]:
        """Convert request to dictionary"""
        return {
            'prompt': self.prompt,
            'state': str(self.state),
            'reference_image': self.reference_image,
            'first_frame': self.first_frame,
            'last_frame': self.last_frame,
            'duration': self.duration,
            'model': self.model
        }


class VideoGenerator:
    """
    Video generator interface for AI models

    This is an interface class. Actual generation would integrate with
    real AI video generation services like Seedream V4, Gemini Nano Banana, etc.
    """

    def __init__(self, config_path: Optional[str] = None):
        """
        Initialize video generator

        Args:
            config_path: Path to video parameters config
        """
        self.config = {}
        if config_path:
            self.load_config(config_path)

        self.default_model = self.config.get('generation_settings', {}).get(
            'model', 'Seedream V4'
        )

    def load_config(self, config_path: str) -> None:
        """
        Load video generation configuration

        Args:
            config_path: Path to config JSON file
        """
        with open(config_path, 'r', encoding='utf-8') as f:
            self.config = json.load(f)

    def generate_video(
        self,
        request: VideoGenerationRequest,
        output_path: str
    ) -> Dict[str, Any]:
        """
        Generate video based on request

        This is a placeholder method. In production, this would:
        1. Call the actual AI video generation API
        2. Handle frame control (first/last frame)
        3. Process the generated video
        4. Save to output path

        Args:
            request: Video generation request
            output_path: Where to save generated video

        Returns:
            Dictionary with generation result info
        """
        print(f"[VideoGenerator] Generating video for state: {request.state}")
        print(f"[VideoGenerator] Model: {request.model}")
        print(f"[VideoGenerator] Prompt: {request.prompt[:100]}...")
        print(f"[VideoGenerator] Output: {output_path}")

        # In production, this would call actual API
        # For now, return mock result
        return {
            'success': True,
            'output_path': output_path,
            'duration': request.duration,
            'model_used': request.model,
            'message': 'Video generation request prepared (mock mode)'
        }

    def generate_with_frame_control(
        self,
        prompt: str,
        first_frame_path: str,
        last_frame_path: str,
        output_path: str,
        duration: float = 5.0
    ) -> Dict[str, Any]:
        """
        Generate video with first/last frame control

        This ensures seamless transitions between video clips

        Args:
            prompt: Generation prompt
            first_frame_path: Path to first frame image
            last_frame_path: Path to last frame image
            output_path: Output video path
            duration: Video duration

        Returns:
            Generation result
        """
        print(f"[VideoGenerator] Frame-controlled generation")
        print(f"[VideoGenerator] First frame: {first_frame_path}")
        print(f"[VideoGenerator] Last frame: {last_frame_path}")

        # In production, this would use the AI model's frame control feature
        return {
            'success': True,
            'output_path': output_path,
            'first_frame': first_frame_path,
            'last_frame': last_frame_path,
            'message': 'Frame-controlled generation prepared (mock mode)'
        }

    def get_video_parameters(self) -> Dict[str, Any]:
        """Get video generation parameters"""
        return self.config.get('video_parameters', {})

    def get_supported_models(self) -> list[str]:
        """Get list of supported models"""
        return [
            "Seedream V4",
            "Gemini Nano Banana",
            "Lovart",
        ]

    def validate_request(self, request: VideoGenerationRequest) -> tuple[bool, Optional[str]]:
        """
        Validate video generation request

        Args:
            request: Request to validate

        Returns:
            Tuple of (is_valid, error_message)
        """
        if not request.prompt:
            return False, "Prompt is required"

        if request.duration <= 0:
            return False, "Duration must be positive"

        if request.model not in self.get_supported_models():
            return False, f"Unsupported model: {request.model}"

        return True, None

    def __repr__(self) -> str:
        return f"VideoGenerator(model='{self.default_model}')"

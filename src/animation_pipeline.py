"""
Animation Pipeline
Main orchestrator that generates all required character animations from config
"""

import json
from pathlib import Path
from typing import Dict, List, Optional
import sys

sys.path.insert(0, str(Path(__file__).parent.parent))

from src.character import CharacterProfile
from src.video import PromptGenerator, VideoGenerator, VideoGenerationRequest, VideoProcessor
from src.state import CharacterState, StateType, EmotionType


class AnimationPipeline:
    """
    Complete pipeline to generate all character animations from config

    Takes a character config JSON and generates all 17 required video files:
    - 1 Default state
    - 1 Default→Listening transition
    - 2 Listening states (normal + speaking)
    - 1 Listening→Default transition
    - 9 Emotion states
    - 2 Leave animations (from listening and default)
    - 1 Enter animation
    """

    def __init__(
        self,
        character_config_path: str,
        video_config_path: str,
        output_dir: str = "output/videos"
    ):
        """
        Initialize animation pipeline

        Args:
            character_config_path: Path to character config JSON
            video_config_path: Path to video parameters config
            output_dir: Directory to save generated videos
        """
        self.character_config_path = character_config_path
        self.video_config_path = video_config_path
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)

        # Load configurations
        self.profile = CharacterProfile(character_config_path)
        self.prompt_gen = PromptGenerator(self.profile)
        self.video_gen = VideoGenerator(video_config_path)
        self.video_processor = VideoProcessor()

        # Track generated videos
        self.generated_videos: Dict[str, str] = {}
        self.generation_log: List[Dict] = []

    def generate_all_animations(self) -> Dict[str, str]:
        """
        Generate all required character animations

        Returns:
            Dictionary mapping video name to file path
        """
        print(f"=== Generating All Animations for {self.profile.nickname} ===\n")

        # Step 1: Generate character reference image
        print("Step 1: Generating character reference image...")
        reference_image = self._generate_reference_image()
        print(f"✓ Reference image: {reference_image}\n")

        # Step 2: Generate base state videos
        print("Step 2: Generating base state videos...")
        self._generate_base_states(reference_image)

        # Step 3: Generate transition videos
        print("\nStep 3: Generating transition videos...")
        self._generate_transitions(reference_image)

        # Step 4: Generate emotion videos
        print("\nStep 4: Generating emotion videos...")
        self._generate_emotions(reference_image)

        # Step 5: Generate device transition videos
        print("\nStep 5: Generating device transition videos...")
        self._generate_device_transitions(reference_image)

        # Step 6: Post-process all videos
        print("\nStep 6: Post-processing videos...")
        self._post_process_videos()

        # Step 7: Generate summary
        print("\nStep 7: Generating summary...")
        self._generate_summary()

        print(f"\n=== Complete! Generated {len(self.generated_videos)} videos ===")
        return self.generated_videos

    def _generate_reference_image(self) -> str:
        """Generate character reference image"""
        prompt = self.prompt_gen.generate_image_prompt(with_background=False)
        output_path = str(self.output_dir / "reference_image.png")

        print(f"   Prompt: {prompt[:100]}...")
        print(f"   → Output: {output_path}")

        # In production: call actual image generation API
        # For now: return mock path
        self.generation_log.append({
            'type': 'image',
            'name': 'reference_image',
            'prompt': prompt,
            'output': output_path
        })

        return output_path

    def _generate_base_states(self, reference_image: str) -> None:
        """Generate base state videos (default, listening, speaking)"""

        states_to_generate = [
            (StateType.DEFAULT, "default", 5.0),
            (StateType.LISTENING, "listening", 5.0),
            (StateType.SPEAKING, "speaking", 4.0),
        ]

        for state_type, name, duration in states_to_generate:
            state = CharacterState(state_type, duration=duration)
            prompt = self.prompt_gen.generate_state_prompt(state)
            output_path = str(self.output_dir / f"{name}.mp4")

            print(f"   Generating {name}...")

            request = VideoGenerationRequest(
                prompt=prompt,
                state=state,
                reference_image=reference_image,
                duration=duration
            )

            result = self.video_gen.generate_video(request, output_path)

            if result['success']:
                self.generated_videos[name] = output_path
                self.generation_log.append({
                    'type': 'video',
                    'name': name,
                    'state': state_type.value,
                    'prompt': prompt,
                    'output': output_path
                })
                print(f"   ✓ {name}.mp4")

    def _generate_transitions(self, reference_image: str) -> None:
        """Generate state transition videos"""

        transitions = [
            (StateType.DEFAULT, StateType.LISTENING, "default2listening", 5.0),
            (StateType.LISTENING, StateType.DEFAULT, "listening2default", 5.0),
        ]

        for from_state, to_state, name, duration in transitions:
            prompt = self.prompt_gen.generate_transition_prompt(from_state, to_state)

            if not prompt:  # Skip if no transition video needed
                continue

            output_path = str(self.output_dir / f"{name}.mp4")

            print(f"   Generating {name}...")

            # Get first/last frames for seamless transition
            first_frame = self._get_state_last_frame(from_state)
            last_frame = self._get_state_first_frame(to_state)

            result = self.video_gen.generate_with_frame_control(
                prompt=prompt,
                first_frame_path=first_frame,
                last_frame_path=last_frame,
                output_path=output_path,
                duration=duration
            )

            if result['success']:
                self.generated_videos[name] = output_path
                self.generation_log.append({
                    'type': 'transition',
                    'name': name,
                    'from': from_state.value,
                    'to': to_state.value,
                    'prompt': prompt,
                    'output': output_path
                })
                print(f"   ✓ {name}.mp4")

    def _generate_emotions(self, reference_image: str) -> None:
        """Generate all emotion state videos"""

        emotions = [
            EmotionType.NEUTRAL,
            EmotionType.HAPPY,
            EmotionType.SHY,
            EmotionType.SURPRISED,
            EmotionType.SMUG,
            EmotionType.ANGRY,
            EmotionType.CONFUSED,
            EmotionType.SAD,
            EmotionType.SLEEPY,
        ]

        for emotion in emotions:
            state = CharacterState(StateType.EMOTION, emotion=emotion)
            prompt = self.prompt_gen.generate_state_prompt(state)
            name = emotion.value
            output_path = str(self.output_dir / f"emotion_{name}.mp4")

            print(f"   Generating emotion: {name}...")

            # Get listening state frames for seamless transition
            first_frame = self._get_state_first_frame(StateType.LISTENING)
            last_frame = self._get_state_last_frame(StateType.LISTENING)

            duration = 10.0 if emotion == EmotionType.SHY else 5.0

            result = self.video_gen.generate_with_frame_control(
                prompt=prompt,
                first_frame_path=first_frame,
                last_frame_path=last_frame,
                output_path=output_path,
                duration=duration
            )

            if result['success']:
                self.generated_videos[f"emotion_{name}"] = output_path
                self.generation_log.append({
                    'type': 'emotion',
                    'name': name,
                    'emotion': emotion.value,
                    'prompt': prompt,
                    'output': output_path
                })
                print(f"   ✓ emotion_{name}.mp4")

    def _generate_device_transitions(self, reference_image: str) -> None:
        """Generate device transition videos (leave, enter)"""

        # Leave animations (from listening and default)
        leave_sources = [
            (StateType.LISTENING, "listening2leave"),
            (StateType.DEFAULT, "default2leave"),
        ]

        for source_state, name in leave_sources:
            state = CharacterState(StateType.LEAVING)
            prompt = self.prompt_gen.generate_state_prompt(state)
            output_path = str(self.output_dir / f"{name}.mp4")

            print(f"   Generating {name}...")

            first_frame = self._get_state_last_frame(source_state)

            request = VideoGenerationRequest(
                prompt=prompt,
                state=state,
                first_frame=first_frame,
                duration=5.0
            )

            result = self.video_gen.generate_video(request, output_path)

            if result['success']:
                self.generated_videos[name] = output_path
                self.generation_log.append({
                    'type': 'device_transition',
                    'name': name,
                    'action': 'leave',
                    'prompt': prompt,
                    'output': output_path
                })
                print(f"   ✓ {name}.mp4")

        # Enter animation
        state = CharacterState(StateType.ENTERING)
        prompt = self.prompt_gen.generate_state_prompt(state)
        output_path = str(self.output_dir / "enter.mp4")

        print(f"   Generating enter...")

        last_frame = self._get_state_first_frame(StateType.LISTENING)

        request = VideoGenerationRequest(
            prompt=prompt,
            state=state,
            last_frame=last_frame,
            duration=5.0
        )

        result = self.video_gen.generate_video(request, output_path)

        if result['success']:
            self.generated_videos["enter"] = output_path
            self.generation_log.append({
                'type': 'device_transition',
                'name': 'enter',
                'action': 'enter',
                'prompt': prompt,
                'output': output_path
            })
            print(f"   ✓ enter.mp4")

    def _get_state_first_frame(self, state_type: StateType) -> str:
        """Get first frame of a state video"""
        # In production: extract from generated video
        # For now: return mock path
        return str(self.output_dir / f"{state_type.value}_first_frame.png")

    def _get_state_last_frame(self, state_type: StateType) -> str:
        """Get last frame of a state video"""
        # In production: extract from generated video
        # For now: return mock path
        return str(self.output_dir / f"{state_type.value}_last_frame.png")

    def _post_process_videos(self) -> None:
        """Post-process all generated videos"""

        for name, video_path in self.generated_videos.items():
            print(f"   Processing {name}...")

            # Remove watermark
            temp_path = str(Path(video_path).parent / f"temp_{Path(video_path).name}")
            self.video_processor.remove_watermark(video_path, temp_path)

            # Check consistency
            self.video_processor.validate_video(video_path)

            print(f"   ✓ {name} processed")

    def _generate_summary(self) -> None:
        """Generate summary report"""
        summary_path = self.output_dir / "generation_summary.json"

        summary = {
            'character': {
                'nickname': self.profile.nickname,
                'config': self.character_config_path
            },
            'total_videos': len(self.generated_videos),
            'videos': self.generated_videos,
            'generation_log': self.generation_log
        }

        with open(summary_path, 'w', encoding='utf-8') as f:
            json.dump(summary, f, indent=2, ensure_ascii=False)

        print(f"   Summary saved to: {summary_path}")

        # Print checklist
        print("\n   Video Delivery Checklist:")
        checklist = {
            'Default state': 'default' in self.generated_videos,
            'Default→Listening': 'default2listening' in self.generated_videos,
            'Listening state': 'listening' in self.generated_videos,
            'Speaking state': 'speaking' in self.generated_videos,
            'Listening→Default': 'listening2default' in self.generated_videos,
            '9 Emotion states': sum(1 for k in self.generated_videos if k.startswith('emotion_')),
            'Leave animations': sum(1 for k in self.generated_videos if 'leave' in k),
            'Enter animation': 'enter' in self.generated_videos,
        }

        for item, status in checklist.items():
            if isinstance(status, bool):
                symbol = "✓" if status else "✗"
                print(f"   {symbol} {item}")
            else:
                print(f"   {status}/9 {item}")

    def export_prompts(self, output_dir: str = "output/prompts") -> None:
        """Export all prompts to text files"""
        self.prompt_gen.save_prompts_to_file(output_dir)
        print(f"Prompts exported to: {output_dir}")


def main():
    """Main entry point for animation generation"""
    import argparse

    parser = argparse.ArgumentParser(
        description="Generate all character animations from config"
    )
    parser.add_argument(
        "--character-config",
        default="config/character_config.json",
        help="Path to character configuration JSON"
    )
    parser.add_argument(
        "--video-config",
        default="config/video_params.json",
        help="Path to video parameters configuration JSON"
    )
    parser.add_argument(
        "--output-dir",
        default="output/videos",
        help="Directory to save generated videos"
    )
    parser.add_argument(
        "--export-prompts-only",
        action="store_true",
        help="Only export prompts without generating videos"
    )

    args = parser.parse_args()

    # Create pipeline
    pipeline = AnimationPipeline(
        character_config_path=args.character_config,
        video_config_path=args.video_config,
        output_dir=args.output_dir
    )

    if args.export_prompts_only:
        print("Exporting prompts only...")
        pipeline.export_prompts("output/prompts")
    else:
        # Generate all animations
        videos = pipeline.generate_all_animations()

        print(f"\nGenerated videos saved to: {args.output_dir}")
        print(f"Total videos: {len(videos)}")


if __name__ == "__main__":
    main()

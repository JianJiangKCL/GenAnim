"""
Complete Animation Generation Example
Shows end-to-end workflow: config → all animations
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from src.animation_pipeline import AnimationPipeline


def main():
    print("=== Complete Animation Generation Example ===\n")
    print("This example shows how to generate ALL required animations")
    print("from a single character configuration JSON file.\n")

    # Create pipeline with configuration
    pipeline = AnimationPipeline(
        character_config_path="config/character_config.json",
        video_config_path="config/video_params.json",
        output_dir="output/videos"
    )

    print("Configuration loaded:")
    print(f"  Character: {pipeline.profile.nickname}")
    print(f"  Personality: {', '.join(pipeline.profile.personality_traits)}")
    print(f"  Art style: {pipeline.profile.art_style}\n")

    # Generate ALL animations
    print("Starting animation generation...\n")
    videos = pipeline.generate_all_animations()

    print("\n" + "="*60)
    print("GENERATION COMPLETE!")
    print("="*60)
    print(f"\nTotal videos generated: {len(videos)}")
    print("\nGenerated files:")
    for name, path in sorted(videos.items()):
        print(f"  • {name}: {path}")

    print(f"\nAll videos saved to: {pipeline.output_dir}")
    print(f"Summary report: {pipeline.output_dir}/generation_summary.json")

    print("\n" + "="*60)
    print("USAGE INSTRUCTIONS")
    print("="*60)
    print("""
The generated videos should be delivered to backend for integration:

1. Base States (3 videos):
   - default.mp4: Character idle state
   - listening.mp4: Character listening to user
   - speaking.mp4: Character speaking (with lip sync)

2. Transitions (2 videos):
   - default2listening.mp4: Idle → Listening
   - listening2default.mp4: Listening → Idle

3. Emotions (9 videos):
   - emotion_neutral.mp4, emotion_happy.mp4, emotion_shy.mp4
   - emotion_surprised.mp4, emotion_smug.mp4, emotion_angry.mp4
   - emotion_confused.mp4, emotion_sad.mp4, emotion_sleepy.mp4

4. Device Transitions (3 videos):
   - listening2leave.mp4: Leave from listening state
   - default2leave.mp4: Leave from default state
   - enter.mp4: Enter new device

TOTAL: 17 video files

To integrate with actual AI video generation:
1. Replace VideoGenerator mock implementation with real API calls
2. Add API keys for Seedream V4 / Gemini Nano Banana / Lovart
3. Implement frame extraction for first/last frame control
4. Add video post-processing (watermark removal, upscale, etc.)
    """)


if __name__ == "__main__":
    main()

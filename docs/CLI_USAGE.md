# GenAnim Command Line Usage

## Main Command: Generate All Animations

Generate all required character animations from a configuration file:

```bash
python src/animation_pipeline.py \
  --character-config config/character_config.json \
  --video-config config/video_params.json \
  --output-dir output/videos
```

### Arguments

- `--character-config`: Path to character configuration JSON (default: `config/character_config.json`)
- `--video-config`: Path to video parameters JSON (default: `config/video_params.json`)
- `--output-dir`: Directory to save generated videos (default: `output/videos`)
- `--export-prompts-only`: Only export text prompts without generating videos

### What Gets Generated

Running this command will automatically create:

#### 1. Reference Image (1 file)
- `reference_image.png` - Base character image used as reference

#### 2. Base State Videos (3 files)
- `default.mp4` (5s) - Character in idle state
- `listening.mp4` (5s) - Character listening to user
- `speaking.mp4` (4s) - Character speaking with lip movement

#### 3. State Transition Videos (2 files)
- `default2listening.mp4` (5s) - Transition from idle to listening
- `listening2default.mp4` (5s) - Transition from listening to idle

#### 4. Emotion Videos (9 files)
- `emotion_neutral.mp4` (5s) - Neutral expression
- `emotion_happy.mp4` (5s) - Happy, smiling, blushing
- `emotion_shy.mp4` (10s) - Looking down shyly, blushing
- `emotion_surprised.mp4` (5s) - Surprised, startled reaction
- `emotion_smug.mp4` (5s) - Confident, arms crossed
- `emotion_angry.mp4` (5s) - Angry, frowning
- `emotion_confused.mp4` (5s) - Confused, thinking
- `emotion_sad.mp4` (5s) - Sad, sighing
- `emotion_sleepy.mp4` (5s) - Tired, drowsy

#### 5. Device Transition Videos (3 files)
- `listening2leave.mp4` (5s) - Character leaving device from listening state
- `default2leave.mp4` (5s) - Character leaving device from default state
- `enter.mp4` (5s) - Character entering device

#### Total Output
- **17 video files** in MP4 format (9:16, 1080p, 24fps, H.264)
- **1 reference image** in PNG format
- **1 summary JSON** with generation details

## Export Prompts Only

If you just want to generate the text prompts for manual use with AI models:

```bash
python src/animation_pipeline.py --export-prompts-only
```

This creates text files in `output/prompts/` with prompts for each animation.

## Examples

### Run Complete Generation Example

```bash
python examples/complete_generation.py
```

This runs the full pipeline and shows detailed progress and results.

### Generate with Custom Config

```bash
# Create your own character config
cp config/character_config.json config/my_character.json
# Edit my_character.json with your character details

# Generate animations
python src/animation_pipeline.py \
  --character-config config/my_character.json \
  --output-dir output/my_character
```

### Check Output

After generation, check the output directory:

```bash
ls -lh output/videos/
# Should show 17 MP4 files + reference image + summary.json

cat output/videos/generation_summary.json
# View detailed generation report
```

## Integration with AI Video Generation

Currently, the video generation is in **mock mode**. To integrate with real AI models:

### Option 1: Seedream V4 (Recommended)
1. Get API access to Seedream V4 at 即梦AI platform
2. Update `src/video/generator.py` with API integration
3. Implement actual video generation calls

### Option 2: Other Models
The system supports:
- **Gemini Nano Banana** - Good for refinement and character consistency
- **Lovart** - For post-processing (Remove bg, Upscale, etc.)

Update the generator to call your preferred model's API.

## Workflow

```
Character Config (JSON)
    ↓
Animation Pipeline
    ├─→ Generate Reference Image
    ├─→ Generate Base States (3 videos)
    ├─→ Generate Transitions (2 videos)
    ├─→ Generate Emotions (9 videos)
    ├─→ Generate Device Transitions (3 videos)
    ├─→ Post-Process (watermark removal, etc.)
    └─→ Generate Summary Report
    ↓
17 MP4 Videos Ready for Backend Integration
```

## Notes

- **First/Last Frame Control**: The system automatically manages frame consistency for seamless transitions
- **Video Parameters**: All videos follow strict parameters (9:16, 1080p, 24fps, H.264, Rec.709 SDR)
- **Batch Processing**: All videos are generated in a single run
- **Quality Assurance**: Automatic validation ensures video consistency

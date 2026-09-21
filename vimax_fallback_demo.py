import asyncio
import os
from pathlib import Path
import sys

VIMAX_ROOT = Path(os.environ.get("VIMAX_ROOT", "/home/ubuntu/ViMax"))
sys.path.insert(0, str(VIMAX_ROOT))

from tools.image_generator_nanobanana_google_api import ImageGeneratorNanobananaGoogleAPI

PROMPT = (
    "Wide 16:9 cinematic documentary keyframe of a small solar-powered community workshop at sunrise, "
    "warm golden light passing through trees, a technician in a blue work shirt checking a clean rooftop "
    "solar panel, realistic photography, high detail, natural colors, gentle hopeful mood, no text, no logo, "
    "no watermark."
)

async def main() -> None:
    key = os.environ.get("GEMINI_API_KEY")
    if not key:
        raise RuntimeError("GEMINI_API_KEY is not available")
    out_dir = Path(__file__).parent / "assets" / "vimax"
    out_dir.mkdir(parents=True, exist_ok=True)
    image_path = out_dir / "rtm_vimax_keyframe.png"
    video_path = out_dir / "rtm_vimax_demo.mp4"
    generator = ImageGeneratorNanobananaGoogleAPI(api_key=key)
    result = await generator.generate_single_image(PROMPT, aspect_ratio="16:9")
    result.save(str(image_path))
    print(f"keyframe={image_path}")
    os.system(
        "ffmpeg -y -loop 1 -i " + str(image_path) +
        " -vf \"scale=1920:1080:force_original_aspect_ratio=increase,crop=1920:1080," 
        "zoompan=z='min(zoom+0.0008,1.08)':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':d=192:s=1920x1080:fps=24,format=yuv420p\" "
        "-t 8 -an -c:v libx264 -preset medium -crf 20 " + str(video_path)
    )
    print(f"video={video_path}")
    print(f"bytes={video_path.stat().st_size}")

if __name__ == "__main__":
    asyncio.run(main())

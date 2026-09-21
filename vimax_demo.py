import asyncio
import os
from pathlib import Path
import sys

# Load the official ViMax source tree without copying or rewriting its providers.
VIMAX_ROOT = Path(os.environ.get("VIMAX_ROOT", "/home/ubuntu/ViMax"))
sys.path.insert(0, str(VIMAX_ROOT))

from tools.video_generator_veo_google_api import VideoGeneratorVeoGoogleAPI


PROMPT = (
    "Cinematic documentary shot of a small solar-powered community workshop at sunrise, "
    "warm golden light passing through trees, a technician in a blue work shirt gently "
    "checking a clean rooftop solar panel, subtle breeze moving nearby leaves, realistic "
    "motion, stable composition, natural colors, no text, no logos, no watermark."
)


async def main() -> None:
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        raise RuntimeError("GEMINI_API_KEY is not available in the environment")

    output_dir = Path(__file__).parent / "assets" / "vimax"
    output_dir.mkdir(parents=True, exist_ok=True)
    output_path = output_dir / "rtm_vimax_demo.mp4"

    generator = VideoGeneratorVeoGoogleAPI(
        api_key=api_key,
        t2v_model="veo-3.1-generate-preview",
        ff2v_model="veo-3.1-generate-preview",
    )
    result = await generator.generate_single_video(
        prompt=PROMPT,
        reference_image_paths=[],
        resolution="720p",
        aspect_ratio="16:9",
        duration=8,
    )
    result.save(str(output_path))
    print(output_path)
    print(f"bytes={output_path.stat().st_size}")


if __name__ == "__main__":
    asyncio.run(main())

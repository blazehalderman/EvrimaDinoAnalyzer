# etl/extract/extract_doqi_transcripts.py
# Source 3 extractor — Doqi Ultimate Guide YouTube playlist
# Method: youtube-transcript-api (preferred) with yt-dlp fallback
# Output: data/youtube_doqi_guide/

import os
from youtube_transcript_api import YouTubeTranscriptApi

OUTPUT_DIR = os.path.join(os.path.dirname(__file__), "..", "..", "data", "youtube_doqi_guide")

# Doqi Ultimate Guide playlist entries — populated during Phase 2
DOQI_VIDEO_IDS: list[str] = []


def get_transcript(video_id: str) -> list[dict]:
    """Fetch the auto-generated or manual transcript for a YouTube video.

    Returns a list of segment dicts: [{"text": str, "start": float, "duration": float}, ...]
    Falls back to yt-dlp subtitle extraction if the Transcript API returns nothing.
    """
    return YouTubeTranscriptApi.get_transcript(video_id)


def save_transcript(video_id: str, transcript: list[dict], title: str) -> str:
    """Write a transcript to data/youtube_doqi_guide/<title>.txt and return the path."""
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    safe_title = "".join(c for c in title if c.isalnum() or c in " _-").strip()
    out_path = os.path.join(OUTPUT_DIR, f"{safe_title}.txt")
    with open(out_path, "w", encoding="utf-8") as f:
        for segment in transcript:
            f.write(segment["text"] + "\n")
    return out_path


def run():
    """Entry point for Phase 2 ETL: extract all Doqi transcripts."""
    raise NotImplementedError("Phase 2")


if __name__ == "__main__":
    run()

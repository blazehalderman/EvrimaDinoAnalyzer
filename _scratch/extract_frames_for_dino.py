"""
extract_frames_for_dino.py
Usage: python extract_frames_for_dino.py <youtube_url> <out_folder> [timestamp1 timestamp2 ...]
If timestamps are provided, extract exactly those seconds.
Otherwise, auto-uses chapter midpoints.
"""
import os, sys
os.environ["OPENCV_LOG_LEVEL"] = "SILENT"
os.environ["OPENCV_FFMPEG_LOGLEVEL"] = "-8"
import cv2, yt_dlp

url        = sys.argv[1]
out_dir    = sys.argv[2]
timestamps = [float(x) for x in sys.argv[3:]] if len(sys.argv) > 3 else None

os.makedirs(out_dir, exist_ok=True)

ydl_opts = {"format": "best[ext=mp4]", "quiet": True, "no_warnings": True}
with yt_dlp.YoutubeDL(ydl_opts) as ydl:
    info = ydl.extract_info(url, download=False)
    stream_url = info["url"]
    duration   = float(info.get("duration") or 0)
    chapters   = info.get("chapters") or []

SKIP_CHAPTERS = {"calls", "patterns", "colors", "night vision", "colour", "colours"}

if timestamps is None:
    if chapters:
        timestamps = []
        skipped = []
        kept_chapters = []
        for i, ch in enumerate(chapters):
            title_lower = ch["title"].strip().lower()
            if title_lower in SKIP_CHAPTERS:
                skipped.append(ch["title"])
                continue
            start = float(ch["start_time"])
            end   = float(chapters[i+1]["start_time"]) if i+1 < len(chapters) else duration
            mid   = start + (end - start) * 0.6
            timestamps.append(round(mid, 1))
            kept_chapters.append(ch)
        print(f"Auto-generated {len(timestamps)} timestamps ({len(skipped)} cosmetic chapters skipped: {skipped})")
        for ch, t in zip(kept_chapters, timestamps):
            print(f"  {ch['title']:<30s} start={ch['start_time']:>5.0f}s  sample@{t:.0f}s")
    else:
        print("No chapters and no timestamps given.")
        sys.exit(1)

cap = cv2.VideoCapture(stream_url)
fps = cap.get(cv2.CAP_PROP_FPS) or 30.0

for t in sorted(timestamps):
    cap.set(cv2.CAP_PROP_POS_FRAMES, int(t * fps))
    ret, frame = cap.read()
    if not ret:
        print(f"  t={t:.0f}s  FAILED")
        continue
    gray  = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    brite = float(gray.mean())
    path  = os.path.join(out_dir, f"t{int(t):04d}.jpg")
    cv2.imwrite(path, frame, [cv2.IMWRITE_JPEG_QUALITY, 85])
    print(f"  t={t:6.1f}s  brightness={brite:.1f}  → {path}")

cap.release()
print("Done.")

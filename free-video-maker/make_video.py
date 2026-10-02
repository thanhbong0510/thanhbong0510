#!/usr/bin/env python3
"""Free 2D story-video maker for a US micro-history channel.

Turns a scenes.json file into a finished 1080p MP4:
  voice (Edge TTS or Kokoro, free)  ->  2D images (Pollinations, free, no key)
  -> Ken Burns zoom/pan motion (ffmpeg)  ->  subtitles + optional music.

Usage:
  python make_video.py scenes.json                 # full run
  python make_video.py scenes.json --mock          # offline test: placeholder images + silent audio
  python make_video.py scenes.json --tts kokoro    # use Kokoro (open-source, safe for monetized videos)
"""

import argparse
import asyncio
import json
import re
import subprocess
import sys
import time
import urllib.parse
import urllib.request
from pathlib import Path

W, H, FPS = 1920, 1080, 30
PAD = 0.4  # seconds of breathing room after each line
FADE = 0.3
DEFAULT_VOICE = "en-US-AndrewNeural"
DEFAULT_KOKORO_VOICE = "am_michael"


def run(cmd):
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        sys.exit(f"Command failed: {' '.join(cmd)}\n{result.stderr[-2000:]}")
    return result.stdout


def audio_duration(path):
    out = run(["ffprobe", "-v", "error", "-show_entries", "format=duration",
               "-of", "default=nw=1:nk=1", str(path)])
    return float(out.strip())


# ---------- voice ----------

def tts_edge(text, voice, rate, out):
    import edge_tts
    asyncio.run(edge_tts.Communicate(text, voice, rate=rate).save(str(out)))


_kokoro = None


def tts_kokoro(text, voice, out):
    global _kokoro
    import numpy as np
    import soundfile as sf
    from kokoro import KPipeline
    if _kokoro is None:
        _kokoro = KPipeline(lang_code="a")  # American English
    chunks = [audio for _, _, audio in _kokoro(text, voice=voice)]
    wav = out.with_suffix(".wav")
    sf.write(wav, np.concatenate(chunks), 24000)
    run(["ffmpeg", "-y", "-v", "error", "-i", str(wav), str(out)])


def tts_mock(text, out):
    seconds = max(2.0, len(text.split()) / 2.5)  # ~150 words per minute
    run(["ffmpeg", "-y", "-v", "error", "-f", "lavfi", "-i", "anullsrc=r=24000:cl=mono",
         "-t", f"{seconds:.2f}", str(out)])


# ---------- images ----------

def image_pollinations(prompt, seed, out):
    url = ("https://image.pollinations.ai/prompt/" + urllib.parse.quote(prompt)
           + f"?width={W}&height={H}&seed={seed}&nologo=true")
    for attempt in range(4):
        try:
            req = urllib.request.Request(url, headers={"User-Agent": "free-video-maker"})
            with urllib.request.urlopen(req, timeout=180) as resp:
                out.write_bytes(resp.read())
            return
        except Exception as exc:
            wait = 2 ** (attempt + 1)
            print(f"    image failed ({exc}), retrying in {wait}s")
            time.sleep(wait)
    sys.exit(f"Could not download image for: {prompt}")


def image_mock(index, out):
    run(["ffmpeg", "-y", "-v", "error", "-f", "lavfi",
         "-i", f"gradients=s={W}x{H}:seed={index + 1}", "-frames:v", "1", str(out)])


# ---------- motion ----------

def motion_filter(motion, frames):
    n = max(frames - 1, 1)
    center_x, center_y = "iw/2-(iw/zoom/2)", "ih/2-(ih/zoom/2)"
    moves = {
        "zoom_in":   (f"1+0.15*on/{n}", center_x, center_y),
        "zoom_out":  (f"1.15-0.15*on/{n}", center_x, center_y),
        "pan_right": ("1.15", f"(iw-iw/zoom)*on/{n}", center_y),
        "pan_left":  ("1.15", f"(iw-iw/zoom)*(1-on/{n})", center_y),
        "pan_up":    ("1.15", center_x, f"(ih-ih/zoom)*(1-on/{n})"),
        "pan_down":  ("1.15", center_x, f"(ih-ih/zoom)*on/{n}"),
    }
    if motion not in moves:
        sys.exit(f"Unknown motion '{motion}'. Use one of: {', '.join(moves)}")
    z, x, y = moves[motion]
    # Upscale first so the slow zoom doesn't jitter.
    return (f"scale={W * 2}:{H * 2}:force_original_aspect_ratio=increase,crop={W * 2}:{H * 2},"
            f"zoompan=z='{z}':x='{x}':y='{y}':d={frames}:s={W}x{H}:fps={FPS}")


def render_clip(image, audio, motion, out):
    duration = audio_duration(audio) + PAD
    frames = int(duration * FPS)
    vf = (motion_filter(motion, frames)
          + f",fade=t=in:st=0:d={FADE},fade=t=out:st={duration - FADE:.2f}:d={FADE},format=yuv420p")
    run(["ffmpeg", "-y", "-v", "error", "-i", str(image), "-i", str(audio),
         "-filter_complex", f"[0:v]{vf}[v];[1:a]apad=pad_dur={PAD}[a]",
         "-map", "[v]", "-map", "[a]", "-t", f"{duration:.3f}",
         "-c:v", "libx264", "-preset", "medium", "-crf", "20", "-r", str(FPS),
         "-c:a", "aac", "-ar", "48000", "-ac", "2", "-b:a", "192k", str(out)])
    return duration


# ---------- subtitles ----------

def srt_time(t):
    ms = int(round(t * 1000))
    return f"{ms // 3600000:02}:{ms // 60000 % 60:02}:{ms // 1000 % 60:02},{ms % 1000:03}"


def write_srt(scenes, durations, out, words_per_line=7):
    lines, start, idx = [], 0.0, 1
    for scene, duration in zip(scenes, durations):
        words = scene["text"].split()
        speech = duration - PAD
        groups = [words[i:i + words_per_line] for i in range(0, len(words), words_per_line)]
        t = start
        for group in groups:
            length = speech * len(group) / len(words)
            lines.append(f"{idx}\n{srt_time(t)} --> {srt_time(t + length)}\n{' '.join(group)}\n")
            idx, t = idx + 1, t + length
        start += duration
    out.write_text("\n".join(lines), encoding="utf-8")


# ---------- main ----------

def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("scenes", type=Path)
    parser.add_argument("--out", type=Path, default=Path("output.mp4"))
    parser.add_argument("--tts", choices=["edge", "kokoro"], default="edge")
    parser.add_argument("--music", type=Path, help="background music file (mp3/wav)")
    parser.add_argument("--music-volume", type=float, default=0.12)
    parser.add_argument("--no-subs", action="store_true")
    parser.add_argument("--mock", action="store_true", help="offline test, no network")
    args = parser.parse_args()

    project = json.loads(args.scenes.read_text(encoding="utf-8"))
    style = project.get("style", "")
    scenes = project["scenes"]
    base = args.scenes.parent
    work = base / "work"
    work.mkdir(exist_ok=True)

    clips, durations = [], []
    for i, scene in enumerate(scenes):
        print(f"[{i + 1}/{len(scenes)}] {scene['text'][:60]}")
        audio = work / f"scene_{i:03}.mp3"
        image = work / f"scene_{i:03}.jpg"
        clip = work / f"scene_{i:03}.mp4"

        if args.mock:
            tts_mock(scene["text"], audio)
        elif not audio.exists():
            if args.tts == "kokoro":
                tts_kokoro(scene["text"], project.get("kokoro_voice", DEFAULT_KOKORO_VOICE), audio)
            else:
                tts_edge(scene["text"], project.get("voice", DEFAULT_VOICE), project.get("rate", "-5%"), audio)

        if scene.get("image_file"):
            image = base / scene["image_file"]
        elif args.mock:
            image_mock(i, image)
        elif not image.exists():
            prompt = f"{style}, {scene['image']}" if style else scene["image"]
            image_pollinations(prompt, project.get("seed", 42) + i, image)

        durations.append(render_clip(image, audio, scene.get("motion", "zoom_in"), clip))
        clips.append(clip)

    concat_list = work / "clips.txt"
    concat_list.write_text("".join(f"file '{c.name}'\n" for c in clips))
    joined = work / "joined.mp4"
    run(["ffmpeg", "-y", "-v", "error", "-f", "concat", "-safe", "0", "-i", str(concat_list),
         "-c", "copy", str(joined)])

    inputs, graph, video_map = ["-i", str(joined)], [], "0:v"
    if not args.no_subs:
        srt = work / "subs.srt"
        write_srt(scenes, durations, srt)
        style_sub = "FontName=Arial,FontSize=13,Bold=1,Outline=2,Shadow=0,MarginV=40"
        srt_path = re.sub(r"([\\:'])", r"\\\1", str(srt.resolve()))
        graph.append(f"[0:v]subtitles='{srt_path}':force_style='{style_sub}'[v]")
        video_map = "[v]"
    if args.music:
        inputs += ["-stream_loop", "-1", "-i", str(args.music)]
        graph.append(f"[1:a]volume={args.music_volume}[m];"
                     "[0:a][m]amix=inputs=2:duration=first:dropout_transition=0:normalize=0[a]")
        audio_map = "[a]"
    else:
        audio_map = "0:a"

    cmd = ["ffmpeg", "-y", "-v", "error", *inputs]
    if graph:
        cmd += ["-filter_complex", ";".join(graph)]
    cmd += ["-map", video_map, "-map", audio_map]
    cmd += ["-c:v", "libx264", "-crf", "20", "-preset", "medium"] if video_map == "[v]" else ["-c:v", "copy"]
    cmd += ["-c:a", "aac", "-b:a", "192k"] if audio_map == "[a]" else ["-c:a", "copy"]
    cmd += ["-shortest", str(args.out)]
    run(cmd)
    print(f"\nDone: {args.out}  ({sum(durations):.1f}s, {len(scenes)} scenes)")


if __name__ == "__main__":
    main()

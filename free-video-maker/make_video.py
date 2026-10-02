#!/usr/bin/env python3
"""Free 2D story-video maker for a US micro-history channel.

Turns a scenes.json file into a finished 1080p MP4:
  voice (Edge TTS or Kokoro)  ->  2D images (local Stable Diffusion or Pollinations)
  -> motion: 2.5D depth parallax or Ken Burns zoom/pan  ->  subtitles + optional music.

Usage:
  python make_video.py scenes.json                            # Edge TTS + Pollinations
  python make_video.py scenes.json --tts kokoro --images sd   # everything local, unlimited
  python make_video.py scenes.json --mock                     # offline test, no network/GPU
"""

import argparse
import asyncio
import json
import math
import os
import re
import subprocess
import sys
import time
import urllib.parse
import urllib.request
from pathlib import Path

# Windows can't make the symlinks Hugging Face's cache prefers; the fallback works fine, so hide the noise.
os.environ.setdefault("HF_HUB_DISABLE_SYMLINKS_WARNING", "1")

W, H, FPS = 1920, 1080, 30
PAD = 0.4  # seconds of breathing room after each line
FADE = 0.3
DEFAULT_VOICE = "en-US-AndrewNeural"
DEFAULT_KOKORO_VOICE = "am_michael"
DEFAULT_NEGATIVE = ("text, letters, words, watermark, signature, logo, blurry, deformed hands, "
                    "extra fingers, photo, photorealistic, 3d render")
# Used for scenes that don't set "motion", so consecutive scenes always move differently.
MOTION_CYCLE = ["parallax_in", "pan_right", "parallax_left", "zoom_out",
                "parallax_right", "zoom_in", "parallax_up", "pan_left"]


def run(cmd, **kwargs):
    result = subprocess.run(cmd, capture_output=True, text=True, **kwargs)
    if result.returncode != 0:
        sys.exit(f"Command failed: {' '.join(map(str, cmd))}\n{result.stderr[-2000:]}")
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

POLLINATIONS_GAP = 20  # seconds between requests; the anonymous free tier rate-limits bursts
_last_pollinations = 0.0


def image_pollinations(prompt, seed, out, token=""):
    global _last_pollinations
    import urllib.error
    url = ("https://image.pollinations.ai/prompt/" + urllib.parse.quote(prompt)
           + f"?width={W}&height={H}&seed={seed}&nologo=true")
    headers = {"User-Agent": "free-video-maker"}
    if token:
        headers["Authorization"] = f"Bearer {token}"
    for wait in (30, 60, 120, 240, None):
        time.sleep(max(0.0, _last_pollinations + POLLINATIONS_GAP - time.time()))
        _last_pollinations = time.time()
        try:
            with urllib.request.urlopen(urllib.request.Request(url, headers=headers), timeout=180) as resp:
                out.write_bytes(resp.read())
            return
        except Exception as exc:
            limited = isinstance(exc, urllib.error.HTTPError) and exc.code in (402, 429)
            if wait is None:
                break
            reason = "rate limited by Pollinations free tier" if limited else str(exc)
            print(f"    image failed ({reason}), retrying in {wait}s")
            time.sleep(wait)
    sys.exit("\n[LOI] Pollinations tu choi tao anh (gioi han ban mien phi).\n"
             "Cach sua: chay lai lenh sau 10-15 phut (anh da tao duoc giu nguyen),\n"
             "hoac tao anh tren may: them --images sd vao lenh.")


_sd = None


def load_sd(project):
    import torch
    from diffusers import AutoencoderKL, StableDiffusionPipeline, StableDiffusionXLPipeline

    sd_type = project.get("sd_type", "sdxl")
    model = project.get("sd_model") or ("stabilityai/stable-diffusion-xl-base-1.0" if sd_type == "sdxl"
                                        else "stable-diffusion-v1-5/stable-diffusion-v1-5")
    cuda = torch.cuda.is_available()
    if not cuda:
        print("    WARNING: no CUDA GPU found, Stable Diffusion will be very slow on CPU")
    dtype = torch.float16 if cuda else torch.float32
    pipe_cls = StableDiffusionXLPipeline if sd_type == "sdxl" else StableDiffusionPipeline
    extra = {"torch_dtype": dtype}
    if sd_type == "sdxl":
        # The stock SDXL VAE produces black images in fp16; this one doesn't.
        extra["vae"] = AutoencoderKL.from_pretrained("madebyollin/sdxl-vae-fp16-fix", torch_dtype=dtype)
    else:
        extra["safety_checker"] = None

    if model.endswith((".safetensors", ".ckpt")):
        pipe = pipe_cls.from_single_file(model, **extra)
    else:
        pipe = pipe_cls.from_pretrained(model, use_safetensors=True, **extra)

    if project.get("sd_lora"):
        pipe.load_lora_weights(project["sd_lora"])
        pipe.fuse_lora(lora_scale=project.get("sd_lora_scale", 0.8))

    if cuda and sd_type == "sdxl":
        pipe.enable_model_cpu_offload()  # SDXL doesn't fit in 8 GB VRAM; spill to system RAM
    elif cuda:
        pipe.to("cuda")
    pipe.enable_attention_slicing()
    pipe.enable_vae_tiling()
    size = (1344, 768) if sd_type == "sdxl" else (912, 512)
    return pipe, size


def image_sd(prompt, seed, out, project):
    global _sd
    import torch
    if _sd is None:
        print("    loading Stable Diffusion (first time downloads several GB)...")
        _sd = load_sd(project)
    pipe, (width, height) = _sd
    image = pipe(prompt=prompt,
                 negative_prompt=project.get("negative", DEFAULT_NEGATIVE),
                 width=width, height=height,
                 num_inference_steps=project.get("sd_steps", 28),
                 guidance_scale=project.get("sd_cfg", 6.5),
                 generator=torch.Generator("cpu").manual_seed(seed)).images[0]
    image.save(out)


def image_mock(index, out):
    run(["ffmpeg", "-y", "-v", "error", "-f", "lavfi",
         "-i", f"gradients=s={W}x{H}:seed={index + 1}", "-frames:v", "1", str(out)])


# ---------- depth (for 2.5D parallax) ----------

_depth = None


def depth_map(img, mock):
    """Relative depth in [0, 1], 1 = nearest to the camera."""
    import cv2
    import numpy as np
    h, w = img.shape[:2]
    if mock:
        ys, xs = np.mgrid[0:h, 0:w].astype(np.float32)
        depth = 0.7 * ys / h + 0.3 * np.exp(-(((xs - w / 2) / (w / 4)) ** 2 + ((ys - h * 0.6) / (h / 4)) ** 2))
    else:
        global _depth
        from PIL import Image
        from transformers import pipeline
        if _depth is None:
            import torch
            _depth = pipeline("depth-estimation", model="depth-anything/Depth-Anything-V2-Small-hf",
                              device=0 if torch.cuda.is_available() else -1)
        result = _depth(Image.fromarray(cv2.cvtColor(img, cv2.COLOR_BGR2RGB)))
        depth = cv2.resize(np.asarray(result["depth"], dtype=np.float32), (w, h))
    depth = cv2.GaussianBlur(depth, (0, 0), 6)  # soften edges to avoid tearing
    return (depth - depth.min()) / max(float(depth.max() - depth.min()), 1e-6)


# ---------- motion ----------

def cover_resize(img):
    import cv2
    h, w = img.shape[:2]
    scale = max(W / w, H / h)
    img = cv2.resize(img, (math.ceil(w * scale), math.ceil(h * scale)), interpolation=cv2.INTER_LANCZOS4)
    top, left = (img.shape[0] - H) // 2, (img.shape[1] - W) // 2
    return img[top:top + H, left:left + W]


def zoompan_filter(motion, frames):
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
    z, x, y = moves[motion]
    # Upscale first so the slow zoom doesn't jitter.
    return (f"scale={W * 2}:{H * 2}:force_original_aspect_ratio=increase,crop={W * 2}:{H * 2},"
            f"zoompan=z='{z}':x='{x}':y='{y}':d={frames}:s={W}x{H}:fps={FPS}")


def parallax_frames(img, depth, motion, frames):
    """Fake camera move: near pixels (high depth) shift and zoom more than far ones."""
    import cv2
    import numpy as np
    ys, xs = np.mgrid[0:H, 0:W].astype(np.float32)
    cx, cy = W / 2, H / 2
    base_zoom, shift = 1.08, 0.035 * W
    for i in range(frames):
        t = i / max(frames - 1, 1)
        e = 0.5 - 0.5 * math.cos(math.pi * t)  # ease in-out
        zoom, sx, sy = base_zoom, 0.0, 0.0
        if motion == "parallax_in":
            zoom = base_zoom + 0.12 * e * (0.3 + 0.7 * depth)
        elif motion == "parallax_left":
            sx = shift * (1 - 2 * e)
        elif motion == "parallax_right":
            sx = shift * (2 * e - 1)
        elif motion == "parallax_up":
            sy = shift * 0.6 * (2 * e - 1)
        map_x = cx + (xs - cx) / zoom + sx * depth
        map_y = cy + (ys - cy) / zoom + sy * depth
        yield cv2.remap(img, map_x.astype(np.float32), map_y.astype(np.float32),
                        cv2.INTER_LINEAR, borderMode=cv2.BORDER_REPLICATE)


ENCODE = ["-c:v", "libx264", "-preset", "medium", "-crf", "20", "-r", str(FPS), "-pix_fmt", "yuv420p",
          "-c:a", "aac", "-ar", "48000", "-ac", "2", "-b:a", "192k"]


def render_clip(image, audio, motion, out, mock):
    duration = audio_duration(audio) + PAD
    frames = int(duration * FPS)
    fades = f"fade=t=in:st=0:d={FADE},fade=t=out:st={duration - FADE:.2f}:d={FADE}"
    audio_filter = f"[1:a]apad=pad_dur={PAD}[a]"

    if motion.startswith("parallax"):
        import cv2
        img = cv2.imread(str(image))
        if img is None:
            sys.exit(f"Cannot read image {image}")
        img = cover_resize(img)
        depth = depth_map(img, mock)
        proc = subprocess.Popen(
            ["ffmpeg", "-y", "-v", "error", "-f", "rawvideo", "-pix_fmt", "bgr24", "-s", f"{W}x{H}",
             "-r", str(FPS), "-i", "-", "-i", str(audio),
             "-filter_complex", f"[0:v]{fades}[v];{audio_filter}",
             "-map", "[v]", "-map", "[a]", "-t", f"{duration:.3f}", *ENCODE, str(out)],
            stdin=subprocess.PIPE, stderr=subprocess.PIPE)
        for frame in parallax_frames(img, depth, motion, frames):
            proc.stdin.write(frame.tobytes())
        proc.stdin.close()
        if proc.wait() != 0:
            sys.exit(f"ffmpeg failed on {out}:\n{proc.stderr.read().decode()[-2000:]}")
    else:
        vf = f"{zoompan_filter(motion, frames)},{fades}"
        run(["ffmpeg", "-y", "-v", "error", "-i", str(image), "-i", str(audio),
             "-filter_complex", f"[0:v]{vf}[v];{audio_filter}",
             "-map", "[v]", "-map", "[a]", "-t", f"{duration:.3f}", *ENCODE, str(out)])
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


def ffmpeg_filter_path(path):
    # ffmpeg filter args need forward slashes and an escaped drive colon on Windows.
    return re.sub(r"([:'])", r"\\\1", str(path.resolve()).replace("\\", "/"))


# ---------- main ----------

VALID_MOTIONS = set(MOTION_CYCLE) | {"pan_up", "pan_down"}


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("scenes", type=Path)
    parser.add_argument("--out", type=Path, default=Path("output.mp4"))
    parser.add_argument("--tts", choices=["edge", "kokoro"], help="default: 'tts' in scenes.json, else edge")
    parser.add_argument("--images", choices=["pollinations", "sd"],
                        help="default: 'images' in scenes.json, else pollinations")
    parser.add_argument("--music", type=Path, help="background music file (mp3/wav)")
    parser.add_argument("--music-volume", type=float, default=0.12)
    parser.add_argument("--no-subs", action="store_true")
    parser.add_argument("--mock", action="store_true", help="offline test, no network or GPU")
    args = parser.parse_args()

    project = json.loads(args.scenes.read_text(encoding="utf-8"))
    tts = args.tts or project.get("tts", "edge")
    images = args.images or project.get("images", "pollinations")
    style = project.get("style", "")
    scenes = project["scenes"]
    base = args.scenes.parent
    work = base / "work"
    work.mkdir(exist_ok=True)

    for i, scene in enumerate(scenes):
        scene.setdefault("motion", MOTION_CYCLE[i % len(MOTION_CYCLE)])
        if scene["motion"] not in VALID_MOTIONS:
            sys.exit(f"Scene {i + 1}: unknown motion '{scene['motion']}'. "
                     f"Use one of: {', '.join(sorted(VALID_MOTIONS))}")

    clips, durations = [], []
    for i, scene in enumerate(scenes):
        print(f"[{i + 1}/{len(scenes)}] {scene['motion']:<15} {scene['text'][:55]}")
        audio = work / f"scene_{i:03}.mp3"
        image = work / f"scene_{i:03}.png"
        clip = work / f"scene_{i:03}.mp4"
        seed = project.get("seed", 42) + i

        if args.mock:
            tts_mock(scene["text"], audio)
        elif not audio.exists():
            if tts == "kokoro":
                tts_kokoro(scene["text"], project.get("kokoro_voice", DEFAULT_KOKORO_VOICE), audio)
            else:
                tts_edge(scene["text"], project.get("voice", DEFAULT_VOICE), project.get("rate", "-5%"), audio)

        if scene.get("image_file"):
            image = base / scene["image_file"]
        elif args.mock:
            image_mock(i, image)
        elif not image.exists():
            if images == "sd":
                # CLIP reads only ~75 tokens, so the scene goes first and the style after.
                image_sd(f"{scene['image']}, {project.get('sd_style', style)}", seed, image, project)
            else:
                image_pollinations(f"{style}, {scene['image']}" if style else scene["image"], seed, image,
                                   project.get("pollinations_token", ""))

        durations.append(render_clip(image, audio, scene["motion"], clip, args.mock))
        clips.append(clip)

    concat_list = work / "clips.txt"
    concat_list.write_text("".join(f"file '{c.name}'\n" for c in clips))
    joined = work / "joined.mp4"
    run(["ffmpeg", "-y", "-v", "error", "-f", "concat", "-safe", "0", "-i", str(concat_list),
         "-c", "copy", str(joined)])

    inputs, graph, video_map, audio_map = ["-i", str(joined)], [], "0:v", "0:a"
    if not args.no_subs:
        srt = work / "subs.srt"
        write_srt(scenes, durations, srt)
        style_sub = "FontName=Arial,FontSize=13,Bold=1,Outline=2,Shadow=0,MarginV=40"
        graph.append(f"[0:v]subtitles='{ffmpeg_filter_path(srt)}':force_style='{style_sub}'[v]")
        video_map = "[v]"
    if args.music:
        inputs += ["-stream_loop", "-1", "-i", str(args.music)]
        graph.append(f"[1:a]volume={args.music_volume}[m];"
                     "[0:a][m]amix=inputs=2:duration=first:dropout_transition=0:normalize=0[a]")
        audio_map = "[a]"

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

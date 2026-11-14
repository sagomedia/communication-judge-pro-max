#!/usr/bin/env python3
"""Fail-closed Step 0 preflight check for Communicator Judge Pro Max (v2).

Verifies host tooling (ffprobe, ffmpeg, Chrome/Chromium), validates that the
target video contains both a real video stream and an audio stream, computes
its SHA-256 and chunking plan, and optionally extracts a tiny MP4 probe clip so
the running agent/harness can verify native video + voice understanding BEFORE
attempting any evaluation.
"""

import argparse
import hashlib
import json
from pathlib import Path
import shutil
import subprocess
import sys


MAX_DIRECT_SECONDS = 240.0
MAX_DIRECT_MB = 25.0


def sha256_file(path: Path) -> str:
    """Compute hex SHA-256 digest of a file in 1 MB chunks."""
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def detect_tools() -> dict[str, str | None]:
    """Locate required CLI dependencies in PATH."""
    browser = (
        shutil.which("google-chrome")
        or shutil.which("chromium")
        or shutil.which("chromium-browser")
    )
    return {
        "ffprobe": shutil.which("ffprobe"),
        "ffmpeg": shutil.which("ffmpeg"),
        "browser": browser,
    }


def probe_media(video_path: Path, ffprobe_bin: str) -> dict:
    """Inspect video/audio streams and duration via ffprobe."""
    cmd = [
        ffprobe_bin,
        "-v",
        "quiet",
        "-print_format",
        "json",
        "-show_format",
        "-show_streams",
        str(video_path),
    ]
    proc = subprocess.run(cmd, check=True, capture_output=True, text=True)
    info = json.loads(proc.stdout)
    streams = info.get("streams", [])
    fmt = info.get("format", {})

    video_streams = [
        s
        for s in streams
        if s.get("codec_type") == "video"
        and (s.get("disposition") or {}).get("attached_pic", 0) == 0
        and int(s.get("width") or 0) > 0
        and int(s.get("height") or 0) > 0
    ]
    audio_streams = [
        s
        for s in streams
        if s.get("codec_type") == "audio" and int(s.get("channels") or 0) > 0
    ]

    duration_raw = fmt.get("duration")
    if duration_raw is None and video_streams:
        duration_raw = video_streams[0].get("duration")
    duration_seconds = round(float(duration_raw or 0.0), 2)

    primary_v = video_streams[0] if video_streams else None
    primary_a = audio_streams[0] if audio_streams else None
    size_bytes = video_path.stat().st_size
    size_mb = round(size_bytes / (1024 * 1024), 2)

    return {
        "path": str(video_path),
        "size_bytes": size_bytes,
        "size_mb": size_mb,
        "duration_seconds": duration_seconds,
        "has_video_stream": primary_v is not None,
        "has_audio_stream": primary_a is not None,
        "video_codec": primary_v.get("codec_name") if primary_v else None,
        "width": int(primary_v["width"]) if primary_v else None,
        "height": int(primary_v["height"]) if primary_v else None,
        "audio_codec": primary_a.get("codec_name") if primary_a else None,
        "audio_channels": int(primary_a["channels"]) if primary_a else None,
        "take_status_hint": (
            "Complete (>= 120s)"
            if duration_seconds >= 120.0
            else "Incomplete Take (< 120s)"
        ),
    }


def extract_probe_clip(
    video_path: Path,
    probe_out: Path,
    duration_seconds: float,
    probe_duration: float,
    ffmpeg_bin: str,
) -> dict:
    """Create a lightweight compressed 720p MP4 clip for harness+model testing."""
    probe_out.parent.mkdir(parents=True, exist_ok=True)
    clip_len = min(probe_duration, max(duration_seconds, 1.0)) if duration_seconds > 0 else probe_duration
    start_sec = 0.0
    if duration_seconds > clip_len + 8.0:
        start_sec = min(10.0, round(duration_seconds * 0.15, 2))

    cmd = [
        ffmpeg_bin,
        "-y",
        "-ss",
        f"{start_sec:.2f}",
        "-i",
        str(video_path),
        "-t",
        f"{clip_len:.2f}",
        "-vf",
        "scale='min(1280,iw)':-2",
        "-c:v",
        "libx264",
        "-preset",
        "veryfast",
        "-crf",
        "28",
        "-c:a",
        "aac",
        "-b:a",
        "64k",
        "-movflags",
        "+faststart",
        str(probe_out),
    ]
    subprocess.run(cmd, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    probe_mb = round(probe_out.stat().st_size / (1024 * 1024), 3)
    return {
        "probe_clip_path": str(probe_out),
        "start_seconds": start_sec,
        "clip_seconds": round(clip_len, 2),
        "size_mb": probe_mb,
    }


def build_inspection_plan(
    media_summary: dict,
    max_chunk_seconds: float,
    max_chunk_mb: float,
    probe_info: dict | None,
) -> dict:
    """Recommend direct read vs chunked 720p proxy inspection."""
    needs_chunking = (
        media_summary["duration_seconds"] > max_chunk_seconds
        or media_summary["size_mb"] > max_chunk_mb
    )
    plan = {
        "recommended_mode": "chunked_720p_proxy" if needs_chunking else "direct_single_file",
        "safe_read_limits": {
            "max_chunk_seconds": max_chunk_seconds,
            "max_chunk_mb": max_chunk_mb,
            "reason": (
                "Large or long MP4 files can silently fail or exceed multimodal harness "
                "budgets; keep each inspected MP4 segment <= 4 min and <= 25 MB."
            ),
        },
        "cleanup_required": needs_chunking or (probe_info is not None),
    }
    if needs_chunking:
        plan["suggested_proxy_command"] = (
            "ffmpeg -y -i \"<video_path>\" -vf \"scale='min(1280,iw)':-2,fps=24\" "
            "-c:v libx264 -preset veryfast -crf 28 -c:a aac -b:a 64k "
            f"-f segment -segment_time {int(max_chunk_seconds)} -reset_timestamps 1 "
            "\"/tmp/cj_proxy_part_%03d.mp4\""
        )
    if probe_info is not None:
        plan["probe_clip"] = probe_info
    return plan


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "video",
        nargs="?",
        type=Path,
        default=None,
        help="Path to input video file (omit only when using --tools-only).",
    )
    parser.add_argument(
        "--tools-only",
        action="store_true",
        help="Check host CLI dependencies only without inspecting a video.",
    )
    parser.add_argument(
        "--probe-clip",
        type=Path,
        default=None,
        help="Optional output path for a temporary ~10s MP4 probe clip to test harness+model perception.",
    )
    parser.add_argument(
        "--probe-duration",
        type=float,
        default=10.0,
        help="Duration in seconds for --probe-clip (default: 10.0).",
    )
    parser.add_argument(
        "--max-chunk-seconds",
        type=float,
        default=MAX_DIRECT_SECONDS,
        help=f"Threshold above which chunking is recommended (default: {int(MAX_DIRECT_SECONDS)}s).",
    )
    parser.add_argument(
        "--max-chunk-mb",
        type=float,
        default=MAX_DIRECT_MB,
        help=f"File size MB threshold above which proxy/chunking is recommended (default: {MAX_DIRECT_MB}).",
    )
    args = parser.parse_args()

    if not args.tools_only and args.video is None:
        parser.error("Provide a <video> path or pass --tools-only.")

    tools = detect_tools()
    blockers: list[str] = []
    if not tools["ffprobe"]:
        blockers.append("MISSING_FFPROBE: Install ffmpeg/ffprobe to inspect audio/video streams.")
    if not tools["ffmpeg"]:
        blockers.append("MISSING_FFMPEG: Install ffmpeg to extract probes and compress/chunk >25 MB videos.")
    if not tools["browser"]:
        blockers.append("MISSING_BROWSER: Install google-chrome or chromium to render 3-page PDF reports.")

    environment_ok = len(blockers) == 0
    result: dict = {
        "environment_ok": environment_ok,
        "media_ok": None if args.tools_only else False,
        "blockers": blockers,
        "tools": tools,
        "agent_capability_gate": {
            "required_capabilities": [
                "harness_accepts_mp4_video_audio",
                "model_native_voice_audio_understanding",
                "model_native_video_visual_understanding",
            ],
            "forbidden_workarounds": [
                "external_asr_or_whisper_instead_of_native_voice_listening",
                "extracted_static_frames_without_hearing_audio",
                "text_only_or_ffprobe_metadata_guessing",
            ],
            "fail_closed_rule": (
                "Before Step 1, inspect the probe clip (or direct <=25MB/<=240s video) with the "
                "harness media tool. Verify you can directly hear spoken words + vocal tone AND "
                "see continuous facial/body motion. If any capability is missing, delete temporary "
                "files, report UNSUPPORTED_ENVIRONMENT, and STOP."
            ),
        },
    }

    exit_code = 0 if environment_ok else 3

    if not args.tools_only and args.video is not None:
        video_path = args.video
        if not video_path.exists() or not video_path.is_file():
            blockers.append(f"FILE_NOT_FOUND: Target video does not exist: {video_path}")
            result["media_ok"] = False
            print(json.dumps(result, indent=2, ensure_ascii=False))
            return 2

        if not tools["ffprobe"]:
            result["media_ok"] = False
            print(json.dumps(result, indent=2, ensure_ascii=False))
            return 3

        try:
            media_summary = probe_media(video_path, tools["ffprobe"])
        except (OSError, subprocess.CalledProcessError, json.JSONDecodeError) as exc:
            blockers.append(f"UNREADABLE_MEDIA: ffprobe failed on {video_path}: {exc}")
            result["media_ok"] = False
            print(json.dumps(result, indent=2, ensure_ascii=False))
            return 2

        media_summary["media_sha256"] = sha256_file(video_path)
        result["media_summary"] = media_summary

        if not media_summary["has_video_stream"]:
            blockers.append("MISSING_VIDEO_STREAM: Input file has no valid video frames (cannot judge Body Language).")
        if not media_summary["has_audio_stream"]:
            blockers.append("MISSING_AUDIO_STREAM: Input file has no audio track (cannot judge Fluency, Communication, or Tonality).")
        if media_summary["duration_seconds"] <= 0:
            blockers.append("ZERO_DURATION_MEDIA: Input file reports 0s duration.")

        media_ok = (
            media_summary["has_video_stream"]
            and media_summary["has_audio_stream"]
            and media_summary["duration_seconds"] > 0
        )
        result["media_ok"] = media_ok

        probe_info = None
        if args.probe_clip is not None and media_ok:
            if not tools["ffmpeg"]:
                blockers.append("MISSING_FFMPEG_FOR_PROBE: Cannot create --probe-clip without ffmpeg.")
                exit_code = 3
            else:
                try:
                    probe_info = extract_probe_clip(
                        video_path=video_path,
                        probe_out=args.probe_clip,
                        duration_seconds=media_summary["duration_seconds"],
                        probe_duration=args.probe_duration,
                        ffmpeg_bin=tools["ffmpeg"],
                    )
                except (OSError, subprocess.CalledProcessError) as exc:
                    blockers.append(f"PROBE_EXTRACTION_FAILED: {exc}")
                    exit_code = 2

        result["inspection_plan"] = build_inspection_plan(
            media_summary=media_summary,
            max_chunk_seconds=args.max_chunk_seconds,
            max_chunk_mb=args.max_chunk_mb,
            probe_info=probe_info,
        )

        if not media_ok and exit_code == 0:
            exit_code = 2

    print(json.dumps(result, indent=2, ensure_ascii=False))
    return exit_code


if __name__ == "__main__":
    raise SystemExit(main())

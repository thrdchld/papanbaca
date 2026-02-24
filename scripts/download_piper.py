#!/usr/bin/env python3
"""
Unduh Piper TTS (Windows amd64) dan suara Indonesia (id_ID) untuk build offline.
Tidak memerlukan token Hugging Face (repo publik).
Menempatkan:
  - piper/piper.exe (Windows)
  - piper/id_ID-news_tts-medium.onnx + .onnx.json
"""
import os
import sys
import zipfile
import urllib.request
import json

# Direktori repo (parent dari scripts/)
REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT_DIR = os.path.join(REPO_ROOT, "piper")
# Cerminan SourceForge jika aset GitHub tidak ada
PIPER_WIN_URL = "https://sourceforge.net/projects/piper-tts.mirror/files/2023.11.14-2/piper_windows_amd64.zip/download"
# Suara Indonesia dari Hugging Face (public)
HF_VOICE_BASE = "https://huggingface.co/rhasspy/piper-voices/resolve/main/id/id_ID/news_tts/medium"
VOICE_FILES = [
    "id_ID-news_tts-medium.onnx",
    "id_ID-news_tts-medium.onnx.json",
]


def download_file(url: str, dest: str) -> None:
    print(f"Download {url} -> {dest}")
    os.makedirs(os.path.dirname(dest) or ".", exist_ok=True)
    urllib.request.urlretrieve(url, dest)


def main():
    os.makedirs(OUT_DIR, exist_ok=True)

    # 1. Piper Windows binary
    zip_path = os.path.join(OUT_DIR, "piper_windows_amd64.zip")
    if not os.path.isfile(os.path.join(OUT_DIR, "piper.exe")):
        if not os.path.isfile(zip_path):
            download_file(PIPER_WIN_URL, zip_path)
        with zipfile.ZipFile(zip_path, "r") as z:
            z.extractall(OUT_DIR)
        print("Piper binary ready:", OUT_DIR)
    else:
        print("Piper binary already present")

    # 2. Voice id_ID
    for fname in VOICE_FILES:
        dest = os.path.join(OUT_DIR, fname)
        if os.path.isfile(dest):
            print("Voice file already present:", fname)
            continue
        url = f"{HF_VOICE_BASE}/{fname}"
        download_file(url, dest)

    print("Done. Piper + id_ID voice in", OUT_DIR)
    return 0


if __name__ == "__main__":
    sys.exit(main() or 0)

#!/usr/bin/env python3
"""
Minimal offline TTS CLI using Coqui TTS.

Usage:
  python tts_app.py --text "Halo" --out out.wav

Environment:
  MODEL_ID: optional model repo id (e.g., tts_models/id/...) to force a specific model.
  HF_TOKEN: (optional) Hugging Face token to download private models.

This script will try to auto-detect an Indonesian model from Coqui TTS model list
if `MODEL_ID` is not provided. For reproducible offline usage, set `MODEL_ID`
and ensure the model files are available (the workflow will attempt to download them).
"""
import os
import sys
import argparse

from TTS.api import TTS
from huggingface_hub import HfApi


def choose_model():
    model_id = os.environ.get("MODEL_ID")
    if model_id:
        return model_id

    # Try to discover Indonesian TTS models via Hugging Face API
    try:
        api = HfApi()
        hf_models = api.list_models()
        candidates = []
        for m in hf_models:
            mid = getattr(m, "modelId", "") or getattr(m, "modelId", "")
            tags = getattr(m, "tags", []) or []
            # prefer Coqui-style model ids
            if "tts_models/id" in mid:
                candidates.insert(0, mid)
                continue

            text = (mid + " " + " ".join(tags)).lower()
            if "indones" in text or "bahasa" in text or "id-id" in text or "indonesia" in text:
                candidates.append(mid)

        if candidates:
            return candidates[0]
    except Exception:
        pass

    # As a last resort, try Coqui TTS helper (may raise)
    try:
        models = TTS.list_models()
        for m in models:
            if isinstance(m, str) and ("/id/" in m or m.startswith("tts_models/id") or "indones" in m.lower()):
                return m
    except Exception:
        pass

    return None


def synthesize(text, out_file):
    model_id = choose_model()
    if not model_id:
        print("ERROR: No Indonesian model detected. Set MODEL_ID environment variable to a Coqui/HF model id.", file=sys.stderr)
        print("You can also set HF_TOKEN and MODEL_ID as repository secrets for Actions.", file=sys.stderr)
        sys.exit(2)

    print(f"Using model: {model_id}")
    try:
        tts = TTS(model_name=model_id, progress_bar=True, gpu=False)
        tts.tts_to_file(text=text, file_path=out_file)
        print("Saved:", out_file)
    except Exception as e:
        print("Synthesis failed:", e, file=sys.stderr)
        sys.exit(3)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--text", "-t", required=True, help="Text to synthesize")
    parser.add_argument("--out", "-o", default="out.wav", help="Output WAV file path")
    parser.add_argument("--demo", action="store_true", help="Run demo mode: generate a few sample Indonesian phrases")
    args = parser.parse_args()

    if args.demo:
        samples = [
            "Halo dunia",
            "Ayo belajar membaca",
            "Ini adalah demo suara Bahasa Indonesia",
        ]
        base = os.path.splitext(args.out)[0]
        for i, s in enumerate(samples, start=1):
            outp = f"{base}_demo_{i}.wav"
            print(f"Synthesizing demo {i}: '{s}' -> {outp}")
            synthesize(s, outp)
        print("Demo finished")
    else:
        synthesize(args.text, args.out)


if __name__ == '__main__':
    main()

# Offline Indonesian TTS (Coqui TTS)

This folder contains a minimal CLI wrapper around Coqui `TTS` intended for
offline usage. The GitHub Actions workflow in the repository will build a
standalone Windows executable using `PyInstaller`.

Usage (after building or installing dependencies):

```bash
MODEL_ID=grandhigh/Chatterbox-TTS-Indonesian HF_TOKEN=... python tts/tts_app.py --text "Halo dunia" --out halo.wav
```

Recommended model (first choice)
- `grandhigh/Chatterbox-TTS-Indonesian` — community Indonesian TTS model available on Hugging Face. This is the suggested starting point for offline use; it provides Indonesian-only voice(s) and has working inference examples on HF. Depending on model size it may be slower on CPU.

Notes:
- Set `MODEL_ID` to a HuggingFace model id that targets Bahasa Indonesia. If you prefer a different model, replace `MODEL_ID` above.
-- If the repository contains large model files, add `hf_token` as a repository secret so CI can download them and bundle into the Windows EXE (create secret name `hf_token`).
- Building a bundled EXE that includes the full model ensures the app works offline immediately after installation.


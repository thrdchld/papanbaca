RELEASE NOTES
===============

This repository's GitHub Actions workflow builds a standalone Windows executable
and creates a release automatically when pushing to `main`/`master`.

Required repository secrets (set in Settings → Secrets):
- `GITHUB_TOKEN` (provided automatically by Actions) — used to create the release and upload assets.
- `MODEL_ID` (optional but recommended) — the Hugging Face model id to bundle (example: `grandhigh/Chatterbox-TTS-Indonesian`). If left empty the app will try to auto-discover a model at runtime.
-- `hf_token` (optional) — Hugging Face token needed if the model repo is private or to avoid rate limits for large downloads. Create the secret with the name `hf_token` in repository Secrets.

What the workflow does
- Installs Python dependencies from `requirements.txt`.
- Optionally downloads the HF model into `models/<MODEL_ID_safe>` when both `MODEL_ID` and `HF_TOKEN` are present.
- Builds a single-file Windows EXE (`papanbaca.exe`) including `web/` and `models/` if present.
- Compresses the EXE into `papanbaca-windows.zip` and creates a GitHub Release `v1.0.<run_number>`, attaching the zip as a release asset.

Important notes
- Model size: many TTS models are large (100s of MB to multiple GB). Bundling a full model will increase the EXE package size accordingly. Prefer a smaller model for CPU-only builds.
- If you do not bundle a model via CI, the app will attempt to download/resolve a model at runtime (requires network on first run and may fail on some machines).
- PyInstaller builds on Windows; building for macOS/Linux requires separate CI runners and packaging steps (not included).

How to trigger a build
- Push to `main` or `master` or create a commit on those branches. The workflow will run automatically.

How to test locally
1. Create and activate a virtual environment:

```powershell
python -m venv .venv
.\.venv\Scripts\activate
```

2. Install dependencies:

```powershell
pip install -r requirements.txt
```

3. Run the app (set `MODEL_ID` if you want a specific model):

```powershell
$env:MODEL_ID = 'grandhigh/Chatterbox-TTS-Indonesian'
python app.py
```

4. To build locally (PyInstaller):

```powershell
pip install pyinstaller
pyinstaller --onefile --add-data "web;web" app.py --name papanbaca
```

Where to find the release
- Releases → the latest release created by CI. The asset name is `papanbaca-windows.zip`.

If you need different release naming, draft releases, or additional artifacts, update `.github/workflows/windows-build.yml` accordingly.

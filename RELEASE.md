# Build & Release

**Semua build hanya di GitHub Actions. Tidak perlu install atau build di local.**

## Workflow

| Workflow | Trigger | Hasil |
|----------|---------|--------|
| **Build Windows EXE** | Push ke `main`/`master` atau workflow_dispatch | Artifact: `papanbaca-windows` (zip berisi EXE) |
| **Build Android APK** | Push ke `main`/`master` atau workflow_dispatch | Artifact: `papanbaca-android-apk` (APK debug) |

## Sumber UI

- **`index.html`** = grand design (preview cepat + sumber untuk build).
- Di CI, `index.html` disalin ke `web/index.html` sebelum build sehingga Windows dan Android memakai UI yang sama.

## Windows (`.github/workflows/windows-build.yml`)

- Runner: `windows-latest`
- Python 3.10, `pip install -r requirements.txt`, PyInstaller
- Bundle: `web/` + (opsional) `models/` jika ada
- **Secret opsional:** `MODEL_ID` + `hf_token` untuk unduh model TTS dari Hugging Face. Tanpa ini, build tetap jalan; app coba pakai/resolve model saat jalan (butuh jaringan di first run).

## Android (`.github/workflows/android-build.yml`)

- Runner: `ubuntu-latest`
- Node 20, `npm install`, Capacitor, `cap add android`, Gradle `assembleDebug`
- Folder `android/` dibuat di CI (tidak di-commit). APK debug (unsigned) untuk uji pasang.

## Mengambil hasil build

1. Buka repo → **Actions** → pilih run workflow yang selesai
2. Di bagian **Artifacts** unduh:
   - **papanbaca-windows** → unzip, jalankan `papanbaca.exe`
   - **papanbaca-android-apk** → pasang `app-debug.apk` di perangkat/emulator

## Tanpa install local

- `node_modules/`, `android/`, `dist/`, `package-lock.json` di-ignore; tidak perlu di-commit.
- Preview: buka `index.html` di browser.
- Untuk develop local (opsional): Python venv + `pip install -r requirements.txt` lalu `python app.py`; untuk Android bisa `npm install` dan `npx cap run android` (perlu Android SDK local).

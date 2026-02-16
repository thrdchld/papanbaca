# PapanBaca — Belajar Membaca Anak

Aplikasi desktop untuk anak-anak belajar membaca huruf dan suku kata Bahasa Indonesia.

## ✨ Fitur

- **Papan huruf interaktif** — drag & drop huruf untuk menyusun kata
- **Text-to-Speech** — baca huruf dan kata dengan suara Bahasa Indonesia
- **Mode Suku Kata** — 4 zona untuk latihan suku kata
- **Keyboard berwarna** — vokal (kuning) dan konsonan (biru) dibedakan
- **Confetti celebration** — efek perayaan saat membaca kata
- **Portable** — satu file `.exe`, tanpa instalasi

## 🚀 Cara Pakai

### Download

Download file `.exe` dari [Releases](../../releases). Langsung jalankan, tidak perlu install.

### Development (lokal)

```bash
npm install
npx electron .
```

### Build Portable EXE

```bash
npm install
npx electron-builder --win --x64 --publish never
```

Hasil build ada di folder `dist/`.

## 🔧 CI/CD

Build otomatis via GitHub Actions:

1. **Push tag** `v*` (contoh: `v0.2.0`) → otomatis build dan buat Release
2. **Manual trigger** → workflow_dispatch di tab Actions

## 📁 Struktur

```
├── index.html          # Aplikasi utama (HTML + CSS + JS)
├── main.js             # Electron main process
├── package.json        # Config & dependencies
├── build/
│   └── icon.svg        # App icon (dikonversi ke PNG saat build)
├── assets/
│   ├── icon-192.svg    # PWA icon
│   ├── icon-512.svg    # PWA icon
│   ├── fonts/          # (opsional) font offline
│   └── sounds/         # (opsional) audio offline
├── manifest.json       # PWA manifest
├── service-worker.js   # PWA service worker
└── .github/workflows/
    └── windows-only.yml  # GitHub Actions build
```

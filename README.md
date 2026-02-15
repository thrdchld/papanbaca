**PapanBaca — build & run**

- **Run locally (dev):**

```
npm install
npx electron .
```

- **Build desktop installers (Windows/Linux, 32 & 64-bit):**

```
npm install
npx electron-builder --linux --win
```

This uses `electron-builder` targets: Windows NSIS (ia32, x64) and Linux AppImage (ia32, x64).

- **Android / Mobile options:**

- Option A — Install as PWA: open the app in a browser (or serve via simple HTTP) and install to Android homescreen. The app includes `manifest.json` and `service-worker.js` for offline install.

- Option B — Native wrapper: use Capacitor to wrap the `www`/project folder:

```
npx cap init
npx cap add android
npx cap copy
npx cap open android
```

Requirements: Node.js, npm, Java JDK, Android SDK (for building native Android apk).

Offline notes — making the app fully standalone:

- Place local font files in `assets/fonts/` as `ComicNeue-Regular.woff2` and `ComicNeue-Bold.woff2` so the app doesn't rely on Google Fonts.
- Add per-letter and phrase audio files to `assets/sounds/` named `a.mp3`, `b.mp3`, ..., `bersih.mp3`, `kosong.mp3`. The app will automatically fallback to these files when `speechSynthesis` isn't available.
- Optional: replace PWA icons in `manifest.json` with your own images (placed in `assets/`).
- The service worker caches app files for offline use; after first load (online) the PWA can be installed and run offline. Electron builds are fully local.

If you want, I can add example audio files and bundle the Comic Neue font into the repo — tell me and I'll add them.

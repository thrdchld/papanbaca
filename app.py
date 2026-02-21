import os
import sys
import threading
import tempfile
import time

import webview

from TTS.api import TTS
from huggingface_hub import HfApi

try:
    import simpleaudio as sa
except Exception:
    sa = None


def choose_model():
    model_id = os.environ.get("MODEL_ID")
    if model_id:
        # allow local bundled model path under ./models/<safe-name>
        local_dir = os.path.join(os.path.dirname(__file__), 'models', model_id.replace('/', '_'))
        if os.path.isdir(local_dir):
            return local_dir
        return model_id

    try:
        api = HfApi()
        hf_models = api.list_models()
        candidates = []
        for m in hf_models:
            mid = getattr(m, "modelId", "")
            tags = getattr(m, "tags", []) or []
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

    try:
        models = TTS.list_models()
        for m in models:
            if isinstance(m, str) and ("/id/" in m or m.startswith("tts_models/id") or "indones" in m.lower()):
                return m
    except Exception:
        pass

    return None


def play_wav(path):
    if sa is None:
        # fallback: try to use platform default via winsound (Windows)
        if sys.platform.startswith('win'):
            import winsound
            winsound.PlaySound(path, winsound.SND_FILENAME)
        else:
            # best-effort: try ffplay if available
            os.system(f"ffplay -nodisp -autoexit \"{path}\" >/dev/null 2>&1")
        return

    try:
        wave_obj = sa.WaveObject.from_wave_file(path)
        play_obj = wave_obj.play()
        play_obj.wait_done()
    except Exception:
        pass


class Api:
    def __init__(self):
        self.tts = None
        self.model = None

    def ensure_model(self):
        if self.tts is not None:
            return
        model_id = choose_model()
        if not model_id:
            raise RuntimeError("No Indonesian TTS model found. Set MODEL_ID env var or add HF_TOKEN and set MODEL_ID.")
        print("Loading TTS model:", model_id)
        self.model = model_id
        # If model_id is a local path, TTS will load from it; otherwise it's a HF id
        self.tts = TTS(model_name=model_id, progress_bar=False, gpu=False)

    def speak(self, text: str):
        # called from JS; run synthesis and play in background thread
        def job(txt):
            try:
                self.ensure_model()
            except Exception as e:
                print("TTS model error:", e)
                return False

            fd, path = tempfile.mkstemp(suffix='.wav')
            os.close(fd)
            try:
                self.tts.tts_to_file(text=txt, file_path=path)
                play_wav(path)
            except Exception as e:
                print("Synthesis/playback error:", e)
            finally:
                try:
                    os.remove(path)
                except Exception:
                    pass
            return True

        threading.Thread(target=job, args=(text,), daemon=True).start()
        return True


def resource_path(relative):
    # get path when bundled by PyInstaller
    base = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base, relative)


def main():
    api = Api()

    index_path = resource_path(os.path.join('web', 'index.html'))
    url = f'file:///{index_path.replace("\\", "/")}'

    window = webview.create_window('Papan Pintar Belajar Membaca', url, js_api=api, width=1100, height=800)
    webview.start()


if __name__ == '__main__':
    main()

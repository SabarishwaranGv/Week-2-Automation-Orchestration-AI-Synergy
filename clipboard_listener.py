import keyboard
import pyperclip
import threading

class ClipboardListener:
    def __init__(self, trigger_key="alt+m", callback=None):
        self.trigger_key = trigger_key
        self.callback = callback

    def start(self):
        def listen():
            keyboard.add_hotkey(self.trigger_key, self._on_trigger)
            keyboard.wait()  # Keeps the listener alive

        thread = threading.Thread(target=listen, daemon=True)
        thread.start()

    def _on_trigger(self):
        try:
            text = pyperclip.paste()
            if text and self.callback:
                self.callback(text)
        except Exception as e:
            print(f"[ClipboardListener] Error: {e}")

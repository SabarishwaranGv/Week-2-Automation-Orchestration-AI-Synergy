import pyautogui
import pygetwindow as gw
import pyperclip
import time

def paste_to_whatsapp(text: str):
    try:
        whatsapp_window = next((w for w in gw.getWindowsWithTitle("WhatsApp") if w.isActive), None)
        if not whatsapp_window:
            print("[OutputHandler] WhatsApp Desktop is not open or not focused.")
            return

        pyperclip.copy(text)
        time.sleep(0.5)  # Ensure clipboard is ready
        pyautogui.hotkey("ctrl", "v")
        print("[OutputHandler] Response pasted into WhatsApp.")
    except Exception as e:
        print(f"[OutputHandler] Error: {e}")

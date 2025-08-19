import sys
import traceback
from modules.clipboard_listener import ClipboardListener
from modules.langchain_pipeline import get_ai_response
from modules.output_handler import paste_to_whatsapp

# Global error handler to catch unexpected exceptions
def global_exception_handler(exc_type, exc_value, exc_traceback):
    print("❌ Unhandled exception:")
    print("".join(traceback.format_exception(exc_type, exc_value, exc_traceback)))

sys.excepthook = global_exception_handler

# Debug print to confirm script is running
print("[Debug] main.py is running...")

# Callback function triggered when Alt+M is pressed
def handle_clipboard_text(text):
    print(f"[Main] Received clipboard text:\n{text}\n")
    response = get_ai_response(text)
    print(f"[Main] AI Response:\n{response}\n")
    paste_to_whatsapp(response)

# Main function to start the listener
def main():
    print("🎼 AI Orchestra is running. Press Alt+M to process clipboard text.")
    listener = ClipboardListener(callback=handle_clipboard_text)
    listener.start()

    # Keep the script alive
    try:
        while True:
            pass
    except KeyboardInterrupt:
        print("\n[Main] Exiting AI Orchestra.")

# Entry point
if __name__ == "__main__":
    main()

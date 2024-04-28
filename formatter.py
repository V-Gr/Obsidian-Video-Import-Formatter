import os
import time
import pyperclip
import win32clipboard
import win32con
import threading

def get_clipboard_file():
    win32clipboard.OpenClipboard()
    filePath = None
    try:
        if win32clipboard.IsClipboardFormatAvailable(win32con.CF_HDROP):
            files = win32clipboard.GetClipboardData(win32con.CF_HDROP)
            filePath = files[0] if files else None
    except Exception as e:
        print(f"Error opening clipboard: {e}")
    finally:
        win32clipboard.CloseClipboard()
    return filePath

def monitor_clipboard():
    PreviousPath = None
    loopContinue = True
    while loopContinue:
        time.sleep(0.5)
        try:
            filePath = get_clipboard_file()
            if filePath and filePath != PreviousPath and filePath.lower().endswith(('.mp4', '.mkv')): # Add file Extension here
                fileWithExtension = os.path.basename(filePath)
                fileWithoutExtension = os.path.splitext(fileWithExtension)[0]
                formatted_text = f"{fileWithoutExtension} ![[{fileWithExtension}]]"
                pyperclip.copy(formatted_text)
                print(f"Clipboard copy detected: {filePath}")
                print(f"Version ready to be pasted: {formatted_text}")
                PreviousPath = filePath
        except Exception as e:
            print(f"Error : {e}")
        if not threading.main_thread().is_alive():
            loopContinue = False

if __name__ == "__main__":
    try:
        monitor_clipboard()
    except KeyboardInterrupt:
        print("Process Interrupted")

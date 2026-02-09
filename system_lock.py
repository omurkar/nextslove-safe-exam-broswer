import ctypes
import keyboard
import time
from ctypes import wintypes

# Windows API Constants
SW_HIDE = 0
SW_SHOW = 5


class SystemLocker:
    def __init__(self):
        self.user32 = ctypes.windll.user32
        self.taskbar_hwnd = self.user32.FindWindowW(u"Shell_TrayWnd", None)
        self.start_button_hwnd = self.user32.FindWindowW(u"Button", u"Start")

    def hide_taskbar(self):
        """Hides the Windows Taskbar and Start Button."""
        if self.taskbar_hwnd:
            self.user32.ShowWindow(self.taskbar_hwnd, SW_HIDE)
        if self.start_button_hwnd:
            self.user32.ShowWindow(self.start_button_hwnd, SW_HIDE)

    def show_taskbar(self):
        """Restores the Windows Taskbar and Start Button."""
        if self.taskbar_hwnd:
            self.user32.ShowWindow(self.taskbar_hwnd, SW_SHOW)
        if self.start_button_hwnd:
            self.user32.ShowWindow(self.start_button_hwnd, SW_SHOW)

    def block_keys(self, config):
        """Blocks keys based on the configuration dictionary."""
        keys_config = config.get('keys', {})

        if keys_config.get('block_alt_tab'):
            # Blocking Alt+Tab is tricky; we block the 'alt' modifier generally for switching
            keyboard.block_key('alt')
            # Note: This is aggressive. It blocks ALT menu in apps too.

        if keys_config.get('block_win'):
            keyboard.block_key('windows')
            keyboard.block_key('left windows')
            keyboard.block_key('right windows')

        if keys_config.get('block_esc'):
            keyboard.block_key('esc')

        # Function Keys (F1-F12)
        # We can add a loop here if you want to block all F-keys
        # for i in range(1, 13): keyboard.block_key(f'f{i}')

    def unblock_all(self):
        """Releases all blocked keys and shows taskbar."""
        try:
            keyboard.unhook_all()
        except:
            pass
        self.show_taskbar()


# Helper for direct testing
if __name__ == "__main__":
    locker = SystemLocker()
    print("Locking system for 5 seconds...")
    locker.hide_taskbar()
    # locker.block_keys({'keys': {'block_win': True}})
    time.sleep(5)
    locker.unblock_all()
    print("System unlocked.")
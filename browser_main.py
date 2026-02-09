import sys
import json
import hashlib
import subprocess
import time
import ctypes
from ctypes import wintypes
import os

from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout,
                             QHBoxLayout, QPushButton, QLabel, QFrame,
                             QInputDialog, QMessageBox, QTabWidget, QLineEdit, QMenu)
from PyQt6.QtCore import Qt, QTimer, QUrl, QTime, QProcess, QObject
from PyQt6.QtGui import QAction
from PyQt6.QtWebEngineWidgets import QWebEngineView
from cryptography.fernet import Fernet

# --- IMPORT SYSTEM LOCK ---
# Ensure system_lock.py is in the same folder or properly imported
try:
    from system_lock import SystemLocker
except ImportError:
    from utils.system_lock import SystemLocker

# --- CONFIGURATION ---
VALID_KEY = b'Z7wQ_0pZ9G9yJ_c8_k1_s2_u3_v4_w5_x6_y7_z8_A9='

# --- WINDOWS API SETUP ---
user32 = ctypes.windll.user32
HWND = wintypes.HWND
DWORD = wintypes.DWORD
BOOL = wintypes.BOOL


def get_window_pid(hwnd):
    pid = DWORD()
    user32.GetWindowThreadProcessId(hwnd, ctypes.byref(pid))
    return pid.value


class AppLauncher(QObject):
    """
    Helper class to launch ONE app and embed it into a specific container.
    We need a class for this so we can have multiple independent timers for multiple apps.
    """

    def __init__(self, path, container, parent=None):
        super().__init__(parent)
        self.path = path
        self.container = container
        self.proc = None
        self.embed_retries = 0
        self.external_hwnd = None

        # Start the launch process
        self.start_app()

    def start_app(self):
        if not os.path.exists(self.path):
            print(f"App path not found: {self.path}")
            return

        try:
            self.proc = subprocess.Popen(self.path)

            # Start looking for the window
            self.embed_timer = QTimer(self)
            self.embed_timer.timeout.connect(self.find_and_embed_window)
            self.embed_timer.start(500)  # Check every 0.5s
        except Exception as e:
            print(f"Failed to launch {self.path}: {e}")

    def find_and_embed_window(self):
        self.embed_retries += 1
        if self.embed_retries > 20:  # Timeout after 10s
            self.embed_timer.stop()
            return

        target_hwnd = None

        def enum_callback(hwnd, lParam):
            nonlocal target_hwnd
            if user32.IsWindowVisible(hwnd):
                window_pid = get_window_pid(hwnd)
                if window_pid == self.proc.pid:
                    target_hwnd = hwnd
                    return False
            return True

        WNDENUMPROC = ctypes.WINFUNCTYPE(BOOL, HWND, ctypes.POINTER(ctypes.c_int))
        user32.EnumWindows(WNDENUMPROC(enum_callback), 0)

        if target_hwnd:
            self.embed_timer.stop()
            self.embed_window(target_hwnd)

    def embed_window(self, hwnd):
        self.external_hwnd = hwnd
        container_hwnd = int(self.container.winId())

        # Windows API Magic
        user32.SetParent(hwnd, container_hwnd)

        # Strip Title Bar
        style = user32.GetWindowLongW(hwnd, -16)
        style = style & ~0x00C00000  # WS_CAPTION
        style = style & ~0x00040000  # WS_THICKFRAME
        user32.SetWindowLongW(hwnd, -16, style | 0x40000000)  # WS_CHILD

        user32.ShowWindow(hwnd, 3)  # Maximize

        # Setup Resize Event
        self.container.resizeEvent = self.on_container_resize
        # Trigger initial resize
        self.on_container_resize(None)

    def on_container_resize(self, event):
        if self.external_hwnd:
            user32.MoveWindow(self.external_hwnd, 0, 0,
                              self.container.width(),
                              self.container.height(), True)

    def kill(self):
        if self.proc:
            self.proc.kill()


class ExamBrowser(QMainWindow):
    def __init__(self):
        super().__init__()

        self.config = self.load_config()
        if not self.config:
            sys.exit(1)

        # --- SYSTEM LOCK ---
        self.locker = SystemLocker()
        self.locker.hide_taskbar()
        self.locker.block_keys(self.config)

        # --- UI SETUP ---
        if self.config['ui']['fullscreen']:
            self.showFullScreen()
        else:
            self.showMaximized()

        self.setWindowFlags(Qt.WindowType.WindowStaysOnTopHint | Qt.WindowType.FramelessWindowHint)

        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        self.main_layout = QVBoxLayout(central_widget)
        self.main_layout.setContentsMargins(0, 0, 0, 0)

        # --- TABS ---
        self.tabs = QTabWidget()
        self.tabs.setStyleSheet("""
            QTabBar::tab { height: 40px; min-width: 120px; font-size: 14px; font-weight: bold; }
            QTabWidget::pane { border: 0; }
        """)
        self.main_layout.addWidget(self.tabs)

        # 1. BROWSER TAB
        self.init_browser_tab()

        # 2. APP TABS (DYNAMIC)
        self.app_launchers = []  # Store launcher instances
        self.init_app_tabs()

        # --- TASKBAR ---
        self.init_taskbar()

    def load_config(self):
        try:
            if not os.path.exists("exam_config.seb"):
                QMessageBox.critical(self, "Error", "Config file not found!")
                return None
            with open("exam_config.seb", "rb") as f:
                data = f.read()
            return json.loads(Fernet(VALID_KEY).decrypt(data))
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Config Load Error: {e}")
            return None

    def init_browser_tab(self):
        self.browser = QWebEngineView()

        # Support old config (single url) and new config (url list)
        start_url = self.config['network'].get('start_url', '')

        # If start_url is empty but allowed_urls exists, take the first one
        if not start_url and self.config['network'].get('allowed_urls'):
            start_url = self.config['network']['allowed_urls'][0]

        if start_url:
            self.browser.setUrl(QUrl(start_url if start_url.startswith("http") else "https://" + start_url))

        self.tabs.addTab(self.browser, "Exam Portal")

    def init_app_tabs(self):
        # Support old config (single path) and new config (list of paths)
        app_paths = self.config['app'].get('paths', [])

        # Fallback for old config structure
        if not app_paths and self.config['app'].get('path'):
            app_paths = [self.config['app']['path']]

        for i, path in enumerate(app_paths):
            if not path: continue

            # Create a name for the tab (e.g., "App 1" or file name)
            app_name = os.path.basename(path).replace(".exe", "")

            # Create Container
            container = QWidget()
            container.setStyleSheet("background-color: #2D2D30;")
            self.tabs.addTab(container, app_name)

            # Launch and Embed
            launcher = AppLauncher(path, container, self)
            self.app_launchers.append(launcher)

    def init_taskbar(self):
        self.taskbar = QFrame()
        self.taskbar.setFixedHeight(50)
        self.taskbar.setStyleSheet("background-color: #2D2D30; color: white;")
        tb_layout = QHBoxLayout(self.taskbar)

        lbl = QLabel("NextSolves SEB")
        lbl.setStyleSheet("font-weight: bold;")
        tb_layout.addWidget(lbl)

        # --- BOOKMARKS MENU (If multiple URLs exist) ---
        allowed_urls = self.config['network'].get('allowed_urls', [])
        if len(allowed_urls) > 1:
            btn_links = QPushButton("Exam Links")
            btn_links.setStyleSheet("background-color: #0078D7; border: none; padding: 5px 10px;")
            menu = QMenu(self)
            for url in allowed_urls:
                action = QAction(url, self)
                # Capture variable 'url' in lambda
                action.triggered.connect(
                    lambda checked, u=url: self.browser.setUrl(QUrl(u if u.startswith("http") else "https://" + u)))
                menu.addAction(action)
            btn_links.setMenu(menu)
            tb_layout.addWidget(btn_links)

        tb_layout.addStretch()

        # Standard Controls
        if self.config['taskbar']['reload']:
            btn_reload = QPushButton("Reload")
            btn_reload.clicked.connect(self.browser.reload)
            btn_reload.setStyleSheet("background-color: #555; border: none; padding: 5px;")
            tb_layout.addWidget(btn_reload)

        btn_quit = QPushButton("EXIT EXAM")
        btn_quit.setStyleSheet("background-color: #D32F2F; font-weight: bold; padding: 5px 15px;")
        btn_quit.clicked.connect(self.attempt_quit)
        tb_layout.addWidget(btn_quit)

        self.main_layout.addWidget(self.taskbar)

    def attempt_quit(self):
        password, ok = QInputDialog.getText(self, "Unlock", "Enter Password:", QLineEdit.EchoMode.Password)
        if ok and password:
            h = hashlib.sha256(password.encode()).hexdigest()
            if h == self.config['security']['quit_hash'] or h == self.config['security']['admin_hash']:
                self.locker.unblock_all()
                # Kill all launched apps
                for launcher in self.app_launchers:
                    launcher.kill()
                QApplication.quit()
            else:
                QMessageBox.warning(self, "Error", "Incorrect Password")

    def closeEvent(self, event):
        event.ignore()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ExamBrowser()
    window.show()
    sys.exit(app.exec())
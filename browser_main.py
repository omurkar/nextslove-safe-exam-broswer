# # import sys
# # import json
# # import hashlib
# # import subprocess
# # import time
# # import ctypes
# # from ctypes import wintypes
# # import os
# #
# # from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout,
# #                              QHBoxLayout, QPushButton, QLabel, QFrame,
# #                              QInputDialog, QMessageBox, QTabWidget, QLineEdit, QMenu, QFileDialog)
# # from PyQt6.QtCore import Qt, QTimer, QUrl, QTime, QProcess, QObject
# # from PyQt6.QtGui import QAction
# # from PyQt6.QtWebEngineWidgets import QWebEngineView
# # from PyQt6.QtWebEngineCore import QWebEnginePage, QWebEngineProfile, QWebEngineSettings
# # from cryptography.fernet import Fernet
# #
# # # --- IMPORT SYSTEM LOCK ---
# # try:
# #     from system_lock import SystemLocker
# # except ImportError:
# #     try:
# #         from utils.system_lock import SystemLocker
# #     except ImportError:
# #         print("CRITICAL ERROR: system_lock.py not found!")
# #         sys.exit(1)
# #
# # # --- CONFIGURATION ---
# # VALID_KEY = b'Z7wQ_0pZ9G9yJ_c8_k1_s2_u3_v4_w5_x6_y7_z8_A9='
# # DEFAULT_DIR = r"C:\Dev\nextsloves seb"
# #
# # # --- WINDOWS API ---
# # user32 = ctypes.windll.user32
# # HWND = wintypes.HWND
# # DWORD = wintypes.DWORD
# # BOOL = wintypes.BOOL
# #
# #
# # def get_window_pid(hwnd):
# #     pid = DWORD()
# #     user32.GetWindowThreadProcessId(hwnd, ctypes.byref(pid))
# #     return pid.value
# #
# #
# # # --- LAUNCHER CLASS ---
# # class AppLauncher(QObject):
# #     def __init__(self, path, container, parent=None):
# #         super().__init__(parent)
# #         self.path = path
# #         self.container = container
# #         self.proc = None
# #         self.embed_retries = 0
# #         self.external_hwnd = None
# #         self.start_app()
# #
# #     def start_app(self):
# #         if not os.path.exists(self.path):
# #             return
# #         try:
# #             self.proc = subprocess.Popen(self.path)
# #             self.embed_timer = QTimer(self)
# #             self.embed_timer.timeout.connect(self.find_and_embed_window)
# #             self.embed_timer.start(500)
# #         except Exception as e:
# #             print(f"Failed to launch {self.path}: {e}")
# #
# #     def find_and_embed_window(self):
# #         self.embed_retries += 1
# #         if self.embed_retries > 20:
# #             self.embed_timer.stop()
# #             return
# #
# #         target_hwnd = None
# #
# #         def enum_callback(hwnd, lParam):
# #             nonlocal target_hwnd
# #             if user32.IsWindowVisible(hwnd):
# #                 window_pid = get_window_pid(hwnd)
# #                 if window_pid == self.proc.pid:
# #                     target_hwnd = hwnd
# #                     return False
# #             return True
# #
# #         WNDENUMPROC = ctypes.WINFUNCTYPE(BOOL, HWND, ctypes.POINTER(ctypes.c_int))
# #         user32.EnumWindows(WNDENUMPROC(enum_callback), 0)
# #
# #         if target_hwnd:
# #             self.embed_timer.stop()
# #             self.embed_window(target_hwnd)
# #
# #     def embed_window(self, hwnd):
# #         self.external_hwnd = hwnd
# #         container_hwnd = int(self.container.winId())
# #         user32.SetParent(hwnd, container_hwnd)
# #         style = user32.GetWindowLongW(hwnd, -16)
# #         style = style & ~0x00C00000
# #         style = style & ~0x00040000
# #         user32.SetWindowLongW(hwnd, -16, style | 0x40000000)
# #         user32.ShowWindow(hwnd, 3)
# #         self.container.resizeEvent = self.on_container_resize
# #         self.on_container_resize(None)
# #
# #     def on_container_resize(self, event):
# #         if self.external_hwnd:
# #             user32.MoveWindow(self.external_hwnd, 0, 0,
# #                               self.container.width(),
# #                               self.container.height(), True)
# #
# #     def kill(self):
# #         if self.proc:
# #             self.proc.kill()
# #
# #
# # # --- WEB PAGE CLASS ---
# # class ExamWebPage(QWebEnginePage):
# #     def __init__(self, config, parent=None):
# #         super().__init__(parent)
# #         self.config = config
# #
# #     def chooseFiles(self, mode, oldFiles, acceptedMimeTypes):
# #         allow_upload = self.config.get('down_uploads', {}).get('allow_upload', True)
# #         if not allow_upload:
# #             return []
# #         return super().chooseFiles(mode, oldFiles, acceptedMimeTypes)
# #
# #
# # # --- MAIN BROWSER CLASS ---
# # class ExamBrowser(QMainWindow):
# #     def __init__(self, config_path):
# #         super().__init__()
# #
# #         self.config_path = config_path
# #         self.config = self.load_config()
# #         if not self.config:
# #             sys.exit(1)
# #
# #         # 1. SYSTEM LOCK (Start Immediately)
# #         self.locker = SystemLocker()
# #         self.locker.hide_taskbar()
# #         self.locker.block_keys(self.config)
# #
# #         # 2. UI Setup
# #         if self.config['ui']['fullscreen']:
# #             self.showFullScreen()
# #         else:
# #             self.showMaximized()
# #
# #         self.setWindowFlags(Qt.WindowType.WindowStaysOnTopHint | Qt.WindowType.FramelessWindowHint)
# #
# #         central_widget = QWidget()
# #         self.setCentralWidget(central_widget)
# #         self.main_layout = QVBoxLayout(central_widget)
# #         self.main_layout.setContentsMargins(0, 0, 0, 0)
# #
# #         self.tabs = QTabWidget()
# #         self.tabs.setStyleSheet("""
# #             QTabBar::tab { height: 40px; min-width: 120px; font-size: 14px; font-weight: bold; }
# #             QTabWidget::pane { border: 0; }
# #         """)
# #         self.main_layout.addWidget(self.tabs)
# #
# #         self.init_browser_tab()
# #
# #         if self.config.get('exam', {}).get('clear_session_start', False):
# #             self.clear_browser_session()
# #
# #         self.app_launchers = []
# #         self.init_app_tabs()
# #         self.init_taskbar()
# #
# #     def load_config(self):
# #         try:
# #             if not os.path.exists(self.config_path):
# #                 QMessageBox.critical(self, "Error", "Selected config file not found!")
# #                 return None
# #             with open(self.config_path, "rb") as f:
# #                 data = f.read()
# #             return json.loads(Fernet(VALID_KEY).decrypt(data))
# #         except Exception as e:
# #             QMessageBox.critical(self, "Error", f"Config Load Error: {e}")
# #             return None
# #
# #     def init_browser_tab(self):
# #         self.browser = QWebEngineView()
# #         self.page = ExamWebPage(self.config, self.browser)
# #         self.browser.setPage(self.page)
# #         self.browser.page().profile().downloadRequested.connect(self.on_download_requested)
# #
# #         start_url = self.config['network'].get('start_url', '')
# #         if not start_url and self.config['network'].get('allowed_urls'):
# #             start_url = self.config['network']['allowed_urls'][0]
# #
# #         if start_url:
# #             self.browser.setUrl(QUrl(start_url if start_url.startswith("http") else "https://" + start_url))
# #
# #         self.tabs.addTab(self.browser, "Exam Portal")
# #
# #     def on_download_requested(self, download_item):
# #         down_config = self.config.get('down_uploads', {})
# #         if not down_config.get('allow_download', True):
# #             download_item.cancel()
# #             return
# #         target_dir = down_config.get('directory', '')
# #         use_custom = down_config.get('allow_custom_dir', False)
# #
# #         if target_dir and not use_custom and os.path.isdir(target_dir):
# #             original_name = download_item.downloadFileName()
# #             download_item.setDownloadDirectory(target_dir)
# #             download_item.setDownloadFileName(original_name)
# #             download_item.accept()
# #         else:
# #             download_item.accept()
# #
# #     def clear_browser_session(self):
# #         profile = self.browser.page().profile()
# #         profile.clearHttpCache()
# #         profile.clearAllVisitedLinks()
# #         profile.cookieStore().deleteAllCookies()
# #         print("Session cleared.")
# #
# #     def init_app_tabs(self):
# #         app_paths = self.config['app'].get('paths', [])
# #         if not app_paths and self.config['app'].get('path'):
# #             app_paths = [self.config['app']['path']]
# #
# #         for path in app_paths:
# #             if not path: continue
# #             app_name = os.path.basename(path).replace(".exe", "")
# #             container = QWidget()
# #             container.setStyleSheet("background-color: #2D2D30;")
# #             self.tabs.addTab(container, app_name)
# #             launcher = AppLauncher(path, container, self)
# #             self.app_launchers.append(launcher)
# #
# #     def init_taskbar(self):
# #         self.taskbar = QFrame()
# #         self.taskbar.setFixedHeight(50)
# #         self.taskbar.setStyleSheet("background-color: #2D2D30; color: white;")
# #         tb_layout = QHBoxLayout(self.taskbar)
# #
# #         lbl = QLabel("NextSolves SEB")
# #         lbl.setStyleSheet("font-weight: bold;")
# #         tb_layout.addWidget(lbl)
# #
# #         allowed_urls = self.config['network'].get('allowed_urls', [])
# #         if len(allowed_urls) > 1:
# #             btn_links = QPushButton("Exam Links")
# #             btn_links.setStyleSheet("background-color: #0078D7; border: none; padding: 5px 10px;")
# #             menu = QMenu(self)
# #             for url in allowed_urls:
# #                 action = QAction(url, self)
# #                 action.triggered.connect(
# #                     lambda checked, u=url: self.browser.setUrl(QUrl(u if u.startswith("http") else "https://" + u)))
# #                 menu.addAction(action)
# #             btn_links.setMenu(menu)
# #             tb_layout.addWidget(btn_links)
# #
# #         tb_layout.addStretch()
# #
# #         if self.config['taskbar']['reload']:
# #             btn_reload = QPushButton("Reload")
# #             btn_reload.clicked.connect(self.browser.reload)
# #             btn_reload.setStyleSheet("background-color: #555; border: none; padding: 5px;")
# #             tb_layout.addWidget(btn_reload)
# #
# #         btn_quit = QPushButton("EXIT EXAM")
# #         btn_quit.setStyleSheet("background-color: #D32F2F; font-weight: bold; padding: 5px 15px;")
# #         btn_quit.clicked.connect(self.attempt_quit)
# #         tb_layout.addWidget(btn_quit)
# #
# #         self.main_layout.addWidget(self.taskbar)
# #
# #     def attempt_quit(self):
# #         password, ok = QInputDialog.getText(self, "Unlock", "Enter Password:", QLineEdit.EchoMode.Password)
# #         if ok and password:
# #             h = hashlib.sha256(password.encode()).hexdigest()
# #             if h == self.config['security']['quit_hash'] or h == self.config['security']['admin_hash']:
# #
# #                 # --- EXIT SEQUENCE ---
# #                 print("Exiting...")
# #
# #                 # 1. Unlock System
# #                 self.locker.unblock_all()
# #
# #                 # 2. Clear Session (if needed)
# #                 if self.config.get('exam', {}).get('clear_session_end', False):
# #                     self.clear_browser_session()
# #
# #                 # 3. Kill Apps
# #                 for launcher in self.app_launchers:
# #                     launcher.kill()
# #
# #                 # 4. FORCE CLOSE
# #                 QApplication.instance().quit()
# #                 sys.exit(0)  # Forces Python to terminate
# #             else:
# #                 QMessageBox.warning(self, "Error", "Incorrect Password")
# #
# #     def closeEvent(self, event):
# #         event.ignore()
# #
# #
# # if __name__ == "__main__":
# #     app = QApplication(sys.argv)
# #
# #     # --- SELECT CONFIG FILE ON STARTUP ---
# #     # Ensures the folder exists just in case
# #     if not os.path.exists(DEFAULT_DIR):
# #         os.makedirs(DEFAULT_DIR)
# #
# #     filename, _ = QFileDialog.getOpenFileName(None, "Select Exam Configuration", DEFAULT_DIR, "SEB Config (*.seb)")
# #
# #     if not filename:
# #         sys.exit(0)  # Exit if user cancelled selection
# #
# #     window = ExamBrowser(filename)
# #     window.show()
# #     sys.exit(app.exec())
#
#
# import sys
# import json
# import hashlib
# import subprocess
# import time
# import ctypes
# from ctypes import wintypes
# import os
#
# from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout,
#                              QHBoxLayout, QPushButton, QLabel, QFrame,
#                              QInputDialog, QMessageBox, QMenu, QFileDialog)
# from PyQt6.QtCore import Qt, QTimer, QUrl, QTime, QProcess, QObject, QRect
# from PyQt6.QtGui import QAction, QScreen, QIcon, QAction
# from PyQt6.QtWebEngineWidgets import QWebEngineView
# from PyQt6.QtWebEngineCore import QWebEnginePage
# from cryptography.fernet import Fernet
#
# # --- IMPORT SYSTEM LOCK ---
# try:
#     from system_lock import SystemLocker
# except ImportError:
#     try:
#         from utils.system_lock import SystemLocker
#     except ImportError:
#         # Fallback to prevent crash, though lock won't work
#         class SystemLocker:
#             def hide_taskbar(self): pass
#
#             def show_taskbar(self): pass
#
#             def block_keys(self, cfg): pass
#
#             def unblock_all(self): pass
#
# # --- CONFIGURATION ---
# VALID_KEY = b'Z7wQ_0pZ9G9yJ_c8_k1_s2_u3_v4_w5_x6_y7_z8_A9='
# DEFAULT_DIR = r"C:\Dev\nextsloves seb"
#
# # --- WINDOWS API SETUP ---
# user32 = ctypes.windll.user32
# kernel32 = ctypes.windll.kernel32
#
# HWND = wintypes.HWND
# DWORD = wintypes.DWORD
# BOOL = wintypes.BOOL
#
# user32.GetWindowThreadProcessId.argtypes = [HWND, ctypes.POINTER(DWORD)]
# user32.GetWindowThreadProcessId.restype = DWORD
# user32.SetForegroundWindow.argtypes = [HWND]
# user32.ShowWindow.argtypes = [HWND, ctypes.c_int]
# user32.IsIconic.argtypes = [HWND]
# user32.IsIconic.restype = BOOL
#
# SW_RESTORE = 9
#
#
# def get_window_thread_process_id(hwnd):
#     pid = DWORD()
#     tid = user32.GetWindowThreadProcessId(hwnd, ctypes.byref(pid))
#     return tid, pid.value
#
#
# # --- STYLESHEET (White/Blue/Orange Theme) ---
# STYLESHEET = """
# /* TASKBAR WINDOW */
# QMainWindow {
#     background-color: #0078d7; /* Main Blue */
# }
# QWidget {
#     font-family: 'Segoe UI', sans-serif;
# }
#
# /* APP BUTTONS ON TASKBAR */
# QPushButton {
#     background-color: transparent;
#     border: none;
#     color: white;
#     font-size: 13px;
#     font-weight: bold;
#     padding: 5px 15px;
#     border-radius: 4px;
#     min-width: 80px;
#     text-align: center;
# }
# QPushButton:hover {
#     background-color: rgba(255, 255, 255, 0.15);
# }
# QPushButton:checked { /* Active App */
#     background-color: rgba(255, 255, 255, 0.3);
#     border-bottom: 3px solid #ff9800; /* Orange Highlight */
# }
#
# /* SPECIAL BUTTONS */
# QPushButton#StartBtn {
#     background-color: #ff9800; /* Orange */
#     font-weight: 800;
#     font-size: 14px;
#     border-radius: 4px;
# }
# QPushButton#StartBtn:hover {
#     background-color: #f57c00;
# }
#
# QPushButton#QuitBtn {
#     background-color: #d32f2f;
#     color: white;
# }
# QPushButton#QuitBtn:hover {
#     background-color: #b71c1c;
# }
#
# /* LABELS */
# QLabel {
#     color: white;
#     font-weight: bold;
# }
# """
#
#
# # --- WEB PAGE CLASS ---
# class ExamWebPage(QWebEnginePage):
#     def __init__(self, config, parent=None):
#         super().__init__(parent)
#         self.config = config
#
#     def chooseFiles(self, mode, oldFiles, acceptedMimeTypes):
#         allow_upload = self.config.get('down_uploads', {}).get('allow_upload', True)
#         if not allow_upload:
#             return []
#         return super().chooseFiles(mode, oldFiles, acceptedMimeTypes)
#
#
# # --- BROWSER WINDOW (THE DESKTOP LAYER) ---
# class BrowserWindow(QMainWindow):
#     """
#     This window acts as the 'Desktop'. It sits behind everything else.
#     """
#
#     def __init__(self, config, taskbar_ref):
#         super().__init__()
#         self.config = config
#         self.taskbar = taskbar_ref
#         self.setWindowFlags(Qt.WindowType.FramelessWindowHint)
#         self.setStyleSheet("background-color: #f0f0f0;")
#
#         # Web View
#         self.browser = QWebEngineView()
#         self.page = ExamWebPage(self.config, self.browser)
#         self.browser.setPage(self.page)
#         self.browser.page().profile().downloadRequested.connect(self.on_download_requested)
#
#         self.setCentralWidget(self.browser)
#
#         # Load URL
#         start_url = self.config['network'].get('start_url', '')
#         if not start_url and self.config['network'].get('allowed_urls'):
#             start_url = self.config['network']['allowed_urls'][0]
#         if start_url:
#             self.browser.setUrl(QUrl(start_url if start_url.startswith("http") else "https://" + start_url))
#
#     def on_download_requested(self, download_item):
#         down_config = self.config.get('down_uploads', {})
#         if not down_config.get('allow_download', True):
#             download_item.cancel()
#             return
#         target_dir = down_config.get('directory', '')
#         if target_dir and os.path.isdir(target_dir) and not down_config.get('allow_custom_dir', False):
#             download_item.setDownloadDirectory(target_dir)
#             download_item.setDownloadFileName(download_item.downloadFileName())
#             download_item.accept()
#         else:
#             download_item.accept()
#
#
# # --- APP LAUNCHER & TRACKER ---
# class AppTracker(QObject):
#     """
#     Launches an app and finds its Window Handle (HWND) so we can activate it.
#     """
#
#     def __init__(self, name, path, taskbar_callback):
#         super().__init__()
#         self.name = name
#         self.path = path
#         self.callback = taskbar_callback  # Function to call when window found
#         self.process = None
#         self.hwnd = None
#
#         self.launch()
#
#     def launch(self):
#         if not os.path.exists(self.path):
#             return
#         try:
#             self.process = subprocess.Popen(self.path)
#             # Poll to find the window
#             self.timer = QTimer(self)
#             self.timer.timeout.connect(self.find_window)
#             self.timer.start(500)
#         except Exception as e:
#             print(f"Error launching {self.name}: {e}")
#
#     def find_window(self):
#         if not self.process: return
#
#         target_hwnd = None
#
#         def enum_callback(hwnd, lParam):
#             nonlocal target_hwnd
#             if user32.IsWindowVisible(hwnd):
#                 _, pid = get_window_thread_process_id(hwnd)
#                 if pid == self.process.pid:
#                     # Found it!
#                     target_hwnd = hwnd
#                     return False
#             return True
#
#         WNDENUMPROC = ctypes.WINFUNCTYPE(BOOL, HWND, ctypes.POINTER(ctypes.c_int))
#         user32.EnumWindows(WNDENUMPROC(enum_callback), 0)
#
#         if target_hwnd:
#             self.hwnd = target_hwnd
#             self.timer.stop()
#             # Notify Taskbar to create button
#             self.callback(self.name, self.hwnd)
#
#     def activate(self):
#         if self.hwnd:
#             if user32.IsIconic(self.hwnd):
#                 user32.ShowWindow(self.hwnd, SW_RESTORE)
#             user32.SetForegroundWindow(self.hwnd)
#
#     def kill(self):
#         if self.process:
#             self.process.kill()
#
#
# # --- MAIN CONTROLLER (THE CUSTOM TASKBAR) ---
# class SebTaskbar(QMainWindow):
#     def __init__(self, config_path):
#         super().__init__()
#
#         # 1. Load Config
#         self.config_path = config_path
#         self.config = self.load_config()
#         if not self.config:
#             sys.exit(1)
#
#         # 2. Lock System
#         self.locker = SystemLocker()
#         self.locker.hide_taskbar()
#         self.locker.block_keys(self.config)
#
#         # 3. Setup Taskbar Window (The Controller)
#         self.setWindowFlags(Qt.WindowType.FramelessWindowHint | Qt.WindowType.WindowStaysOnTopHint | Qt.WindowType.Tool)
#         self.setStyleSheet(STYLESHEET)
#
#         # Geometry: Bottom 50px of screen
#         screen_geo = QApplication.primaryScreen().geometry()
#         self.taskbar_height = 50
#         self.setGeometry(0, screen_geo.height() - self.taskbar_height, screen_geo.width(), self.taskbar_height)
#
#         # 4. Setup Browser Window (The "Desktop")
#         self.browser_win = BrowserWindow(self.config, self)
#         # Browser fills space ABOVE taskbar
#         self.browser_win.setGeometry(0, 0, screen_geo.width(), screen_geo.height() - self.taskbar_height)
#         self.browser_win.show()
#
#         # 5. UI Layout
#         central = QWidget()
#         self.setCentralWidget(central)
#         self.layout = QHBoxLayout(central)
#         self.layout.setContentsMargins(10, 5, 10, 5)
#         self.layout.setSpacing(10)
#
#         # Start / Browser Button
#         self.btn_browser = QPushButton("Exam Portal")
#         self.btn_browser.setObjectName("StartBtn")
#         self.btn_browser.clicked.connect(self.activate_browser)
#         self.layout.addWidget(self.btn_browser)
#
#         # Divider
#         line = QFrame()
#         line.setFrameShape(QFrame.Shape.VLine)
#         line.setStyleSheet("color: rgba(255,255,255,0.3);")
#         self.layout.addWidget(line)
#
#         # App Buttons Container
#         self.app_buttons = {}
#         self.app_trackers = []
#
#         # Right Side Controls
#         self.layout.addStretch()
#
#         if self.config['taskbar'].get('time', True):
#             self.lbl_clock = QLabel()
#             self.layout.addWidget(self.lbl_clock)
#             self.timer = QTimer(self)
#             self.timer.timeout.connect(self.update_clock)
#             self.timer.start(1000)
#             self.update_clock()
#
#         self.btn_quit = QPushButton("Exit Exam")
#         self.btn_quit.setObjectName("QuitBtn")
#         self.btn_quit.clicked.connect(self.attempt_quit)
#         self.layout.addWidget(self.btn_quit)
#
#         # 6. Launch External Apps
#         self.launch_apps()
#
#     def load_config(self):
#         try:
#             if not os.path.exists(self.config_path):
#                 return None
#             with open(self.config_path, "rb") as f:
#                 data = f.read()
#             return json.loads(Fernet(VALID_KEY).decrypt(data))
#         except:
#             return None
#
#     def launch_apps(self):
#         app_paths = self.config['app'].get('paths', [])
#         # Fallback for old config
#         if not app_paths and self.config['app'].get('path'):
#             app_paths = [self.config['app']['path']]
#
#         for path in app_paths:
#             if not path: continue
#             name = os.path.basename(path).replace(".exe", "")
#             # Tracker launches the app and calls 'add_app_button' when window is found
#             tracker = AppTracker(name, path, self.add_app_button)
#             self.app_trackers.append(tracker)
#
#     def add_app_button(self, name, hwnd):
#         """Called by AppTracker when an external window is found."""
#         btn = QPushButton(name)
#         btn.setCheckable(True)
#         # Python closure trick to capture hwnd
#         btn.clicked.connect(lambda checked, h=hwnd: self.activate_external_app(h))
#
#         # Insert before the stretch (index = count - 3 roughly, but layout logic varies)
#         # We insert after the divider (index 2)
#         count = self.layout.count()
#         # Find position before stretch
#         insert_idx = 2 + len(self.app_buttons)
#         self.layout.insertWidget(insert_idx, btn)
#         self.app_buttons[hwnd] = btn
#
#     def activate_browser(self):
#         """Brings the Browser window to front."""
#         self.browser_win.setWindowState(
#             self.browser_win.windowState() & ~Qt.WindowState.WindowMinimized | Qt.WindowState.WindowActive)
#         self.browser_win.activateWindow()
#         self.browser_win.raise_()
#
#         # Reset button styles
#         for btn in self.app_buttons.values():
#             btn.setChecked(False)
#
#     def activate_external_app(self, hwnd):
#         """Brings an external window to front."""
#         if user32.IsIconic(hwnd):
#             user32.ShowWindow(hwnd, SW_RESTORE)
#         user32.SetForegroundWindow(hwnd)
#
#         # Update UI: Highlight this button, uncheck others
#         for h, btn in self.app_buttons.items():
#             btn.setChecked(h == hwnd)
#
#     def update_clock(self):
#         self.lbl_clock.setText(QTime.currentTime().toString("hh:mm AP"))
#
#     def attempt_quit(self):
#         password, ok = QInputDialog.getText(self, "Unlock", "Enter Password:", QLineEdit.EchoMode.Password)
#         if ok and password:
#             h = hashlib.sha256(password.encode()).hexdigest()
#             if h == self.config['security']['quit_hash'] or h == self.config['security']['admin_hash']:
#                 # 1. Unlock
#                 self.locker.unblock_all()
#                 # 2. Kill External Apps
#                 for tracker in self.app_trackers:
#                     tracker.kill()
#                 # 3. Clear Session
#                 if self.config.get('exam', {}).get('clear_session_end', False):
#                     self.browser_win.browser.page().profile().cookieStore().deleteAllCookies()
#
#                 QApplication.quit()
#                 sys.exit(0)
#             else:
#                 QMessageBox.warning(self, "Error", "Incorrect Password")
#
#     def closeEvent(self, event):
#         event.ignore()  # Prevent Alt+F4 on taskbar
#
#
# if __name__ == "__main__":
#     app = QApplication(sys.argv)
#
#     if not os.path.exists(DEFAULT_DIR):
#         os.makedirs(DEFAULT_DIR)
#
#     filename, _ = QFileDialog.getOpenFileName(None, "Select Exam Configuration", DEFAULT_DIR, "SEB Config (*.seb)")
#
#     if filename:
#         taskbar = SebTaskbar(filename)
#         taskbar.show()  # Shows the bottom bar
#         # Browser window is shown inside SebTaskbar __init__
#         sys.exit(app.exec())


import sys
import json
import hashlib
import subprocess
import time
import ctypes
from ctypes import wintypes
import os

# Try to import keyboard for key blocking
try:
    import keyboard
except ImportError:
    print("WARNING: 'keyboard' library not found. Key blocking will be disabled.")
    keyboard = None

from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout,
                             QHBoxLayout, QPushButton, QLabel, QFrame,
                             QInputDialog, QMessageBox, QMenu, QFileDialog, QLineEdit)
from PyQt6.QtCore import Qt, QTimer, QUrl, QTime, QProcess, QObject, QRect
from PyQt6.QtGui import QAction, QScreen, QIcon, QAction
from PyQt6.QtWebEngineWidgets import QWebEngineView
from PyQt6.QtWebEngineCore import QWebEnginePage
from cryptography.fernet import Fernet

# --- CONFIGURATION ---
VALID_KEY = b'Z7wQ_0pZ9G9yJ_c8_k1_s2_u3_v4_w5_x6_y7_z8_A9='
DEFAULT_DIR = r"C:\Dev\nextsloves seb"

# --- WINDOWS API SETUP ---
user32 = ctypes.windll.user32
kernel32 = ctypes.windll.kernel32

HWND = wintypes.HWND
DWORD = wintypes.DWORD
BOOL = wintypes.BOOL

# API Signatures
user32.GetWindowThreadProcessId.argtypes = [HWND, ctypes.POINTER(DWORD)]
user32.GetWindowThreadProcessId.restype = DWORD
user32.SetForegroundWindow.argtypes = [HWND]
user32.ShowWindow.argtypes = [HWND, ctypes.c_int]
user32.IsIconic.argtypes = [HWND]
user32.IsIconic.restype = BOOL
user32.FindWindowW.argtypes = [ctypes.c_wchar_p, ctypes.c_wchar_p]
user32.FindWindowW.restype = HWND
user32.AttachThreadInput.argtypes = [DWORD, DWORD, BOOL]
user32.AttachThreadInput.restype = BOOL
user32.SetFocus.argtypes = [HWND]

SW_HIDE = 0
SW_SHOW = 5
SW_RESTORE = 9


def get_window_thread_process_id(hwnd):
    pid = DWORD()
    tid = user32.GetWindowThreadProcessId(hwnd, ctypes.byref(pid))
    return tid, pid.value


# --- STYLESHEET (White/Blue/Orange Theme) ---
STYLESHEET = """
QMainWindow {
    background-color: #0078d7; /* Main Blue */
}
QWidget {
    font-family: 'Segoe UI', sans-serif;
}
QPushButton {
    background-color: transparent;
    border: none;
    color: white;
    font-size: 13px;
    font-weight: bold;
    padding: 5px 15px;
    border-radius: 4px;
    min-width: 80px;
    text-align: center;
}
QPushButton:hover {
    background-color: rgba(255, 255, 255, 0.15);
}
QPushButton:checked {
    background-color: rgba(255, 255, 255, 0.3);
    border-bottom: 3px solid #ff9800;
}
QPushButton#StartBtn {
    background-color: #ff9800;
    font-weight: 800;
    font-size: 14px;
    border-radius: 4px;
}
QPushButton#StartBtn:hover {
    background-color: #f57c00;
}
QPushButton#QuitBtn {
    background-color: #d32f2f;
    color: white;
}
QPushButton#QuitBtn:hover {
    background-color: #b71c1c;
}
QLabel {
    color: white;
    font-weight: bold;
}
"""


# ==========================================
#      CORE 1: SYSTEM LOCKER (INTEGRATED)
# ==========================================
class SystemLocker:
    def __init__(self):
        self.user32 = ctypes.windll.user32
        self.taskbar_hwnd = self.user32.FindWindowW(u"Shell_TrayWnd", None)
        self.start_button_hwnd = self.user32.FindWindowW(u"Button", u"Start")
        self.blocked_keys = []

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
        """Blocks keys based on config using 'keyboard' library."""
        if not keyboard: return  # Safety check

        keys_config = config.get('keys', {})
        self.unblock_keys()  # Reset first

        # 1. Block Alt+Tab / Alt
        if keys_config.get('block_alt_tab'):
            try:
                keyboard.block_key('alt')
                self.blocked_keys.append('alt')
            except:
                pass

        # 2. Block Windows Key
        if keys_config.get('block_win'):
            try:
                keyboard.block_key('windows')
                keyboard.block_key('left windows')
                keyboard.block_key('right windows')
                self.blocked_keys.extend(['windows', 'left windows', 'right windows'])
            except:
                pass

        # 3. Block Escape
        if keys_config.get('block_esc'):
            try:
                keyboard.block_key('esc')
                self.blocked_keys.append('esc')
            except:
                pass

        # 4. Block F-Keys
        if keys_config.get('block_f_keys'):
            for i in range(1, 13):
                key = f'f{i}'
                try:
                    keyboard.block_key(key)
                    self.blocked_keys.append(key)
                except:
                    pass

    def unblock_keys(self):
        if not keyboard: return
        try:
            keyboard.unhook_all()
            self.blocked_keys = []
        except:
            pass

    def unblock_all(self):
        self.unblock_keys()
        self.show_taskbar()


# ==========================================
#      CORE 2: BROWSER & UPLOAD BLOCKER
# ==========================================
class ExamWebPage(QWebEnginePage):
    def __init__(self, config, parent=None):
        super().__init__(parent)
        self.config = config

    def chooseFiles(self, mode, oldFiles, acceptedMimeTypes):
        # Block uploads if config says so
        allow_upload = self.config.get('down_uploads', {}).get('allow_upload', True)
        if not allow_upload:
            return []
        return super().chooseFiles(mode, oldFiles, acceptedMimeTypes)


class BrowserWindow(QMainWindow):
    def __init__(self, config):
        super().__init__()
        self.config = config
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint)
        self.setStyleSheet("background-color: #f0f0f0;")

        self.browser = QWebEngineView()
        self.page = ExamWebPage(self.config, self.browser)
        self.browser.setPage(self.page)
        self.browser.page().profile().downloadRequested.connect(self.on_download_requested)

        self.setCentralWidget(self.browser)

        # Load Start URL
        start_url = self.config['network'].get('start_url', '')
        if not start_url and self.config['network'].get('allowed_urls'):
            start_url = self.config['network']['allowed_urls'][0]
        if start_url:
            self.load_url(start_url)

    def load_url(self, url):
        self.browser.setUrl(QUrl(url if url.startswith("http") else "https://" + url))

    def on_download_requested(self, download_item):
        down_config = self.config.get('down_uploads', {})
        if not down_config.get('allow_download', True):
            download_item.cancel()
            return
        target_dir = down_config.get('directory', '')
        if target_dir and os.path.isdir(target_dir) and not down_config.get('allow_custom_dir', False):
            download_item.setDownloadDirectory(target_dir)
            download_item.setDownloadFileName(download_item.downloadFileName())
            download_item.accept()
        else:
            download_item.accept()


# ==========================================
#      CORE 3: APP TRACKER & FOCUS FIX
# ==========================================
class AppTracker(QObject):
    def __init__(self, name, path, taskbar_callback):
        super().__init__()
        self.name = name
        self.path = path
        self.callback = taskbar_callback
        self.process = None
        self.hwnd = None
        self.launch()

    def launch(self):
        if not os.path.exists(self.path): return
        try:
            self.process = subprocess.Popen(self.path)
            self.timer = QTimer(self)
            self.timer.timeout.connect(self.find_window)
            self.timer.start(500)
        except Exception as e:
            print(f"Error launching {self.name}: {e}")

    def find_window(self):
        if not self.process: return
        target_hwnd = None

        def enum_callback(hwnd, lParam):
            nonlocal target_hwnd
            if user32.IsWindowVisible(hwnd):
                _, pid = get_window_thread_process_id(hwnd)
                if pid == self.process.pid:
                    target_hwnd = hwnd
                    return False
            return True

        WNDENUMPROC = ctypes.WINFUNCTYPE(BOOL, HWND, ctypes.POINTER(ctypes.c_int))
        user32.EnumWindows(WNDENUMPROC(enum_callback), 0)

        if target_hwnd:
            self.hwnd = target_hwnd
            self.timer.stop()
            self.callback(self.name, self.hwnd)

    def activate(self):
        """Bring app to front and FORCE focus so you can type."""
        if self.hwnd:
            if user32.IsIconic(self.hwnd):
                user32.ShowWindow(self.hwnd, SW_RESTORE)

            # 1. Attach Input Threads
            fg_thread = kernel32.GetCurrentThreadId()
            target_thread, _ = get_window_thread_process_id(self.hwnd)
            if fg_thread != target_thread:
                user32.AttachThreadInput(fg_thread, target_thread, True)

            # 2. Force Foreground & Focus
            user32.SetForegroundWindow(self.hwnd)
            user32.SetFocus(self.hwnd)

            # 3. Detach
            if fg_thread != target_thread:
                user32.AttachThreadInput(fg_thread, target_thread, False)

    def kill(self):
        if self.process:
            # Force kill the process tree to fix the "application not closing" issue
            subprocess.run(f"taskkill /F /T /PID {self.process.pid}", shell=True)


# ==========================================
#      CORE 4: TASKBAR CONTROLLER
# ==========================================
class SebTaskbar(QMainWindow):
    def __init__(self, config_path):
        super().__init__()

        self.config_path = config_path
        self.config = self.load_config()
        if not self.config: sys.exit(1)

        # 1. LOCK SYSTEM IMMEDIATELY
        self.locker = SystemLocker()
        self.locker.hide_taskbar()
        self.locker.block_keys(self.config)

        # 2. Setup Taskbar UI
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint | Qt.WindowType.WindowStaysOnTopHint | Qt.WindowType.Tool)
        self.setStyleSheet(STYLESHEET)

        screen_geo = QApplication.primaryScreen().geometry()
        self.taskbar_height = 50
        self.setGeometry(0, screen_geo.height() - self.taskbar_height, screen_geo.width(), self.taskbar_height)

        # 3. Setup Browser Desktop
        self.browser_win = BrowserWindow(self.config)
        self.browser_win.setGeometry(0, 0, screen_geo.width(), screen_geo.height() - self.taskbar_height)
        self.browser_win.show()

        # Handle Session Clear Start
        if self.config.get('exam', {}).get('clear_session_start', False):
            self.browser_win.browser.page().profile().cookieStore().deleteAllCookies()

        # 4. Layout
        central = QWidget()
        self.setCentralWidget(central)
        self.layout = QHBoxLayout(central)
        self.layout.setContentsMargins(10, 5, 10, 5)
        self.layout.setSpacing(10)

        # Start Button
        self.btn_browser = QPushButton("Exam Portal")
        self.btn_browser.setObjectName("StartBtn")
        self.btn_browser.setCheckable(True)
        self.btn_browser.setChecked(True)
        self.btn_browser.clicked.connect(self.activate_browser)
        self.layout.addWidget(self.btn_browser)

        # Divider
        line = QFrame()
        line.setFrameShape(QFrame.Shape.VLine)
        line.setStyleSheet("color: rgba(255,255,255,0.3);")
        self.layout.addWidget(line)

        # App Management
        self.app_buttons = {}
        self.app_trackers = []

        self.layout.addStretch()

        # Exam Links
        allowed_urls = self.config['network'].get('allowed_urls', [])
        if allowed_urls and len(allowed_urls) > 0:
            btn_links = QPushButton("Exam Links")
            btn_links.setStyleSheet("background-color: #ff9800; color: white; border-radius: 4px;")
            menu = QMenu(self)
            for url in allowed_urls:
                action = QAction(url, self)
                action.triggered.connect(lambda checked, u=url: self.browser_win.load_url(u))
                menu.addAction(action)
            btn_links.setMenu(menu)
            self.layout.addWidget(btn_links)

        # Indicators
        if self.config['taskbar'].get('wifi', False):
            self.layout.addWidget(QPushButton("Wi-Fi"))
        if self.config['taskbar'].get('keyboard', False):
            self.layout.addWidget(QPushButton("EN-US"))
        if self.config['taskbar'].get('time', True):
            self.lbl_clock = QLabel()
            self.layout.addWidget(self.lbl_clock)
            self.timer = QTimer(self)
            self.timer.timeout.connect(self.update_clock)
            self.timer.start(1000)
            self.update_clock()
        if self.config['taskbar'].get('reload', False):
            btn_reload = QPushButton("Reload")
            btn_reload.clicked.connect(self.browser_win.browser.reload)
            self.layout.addWidget(btn_reload)

        self.btn_quit = QPushButton("Exit Exam")
        self.btn_quit.setObjectName("QuitBtn")
        self.btn_quit.clicked.connect(self.attempt_quit)
        self.layout.addWidget(self.btn_quit)

        # 5. Launch Apps
        self.launch_apps()

    def load_config(self):
        try:
            if not os.path.exists(self.config_path): return None
            with open(self.config_path, "rb") as f:
                data = f.read()
            return json.loads(Fernet(VALID_KEY).decrypt(data))
        except:
            return None

    def launch_apps(self):
        app_paths = self.config['app'].get('paths', [])
        if not app_paths and self.config['app'].get('path'):
            app_paths = [self.config['app']['path']]

        for path in app_paths:
            if not path: continue
            name = os.path.basename(path).replace(".exe", "")
            tracker = AppTracker(name, path, self.add_app_button)
            self.app_trackers.append(tracker)

    def add_app_button(self, name, hwnd):
        btn = QPushButton(name)
        btn.setCheckable(True)
        btn.clicked.connect(lambda checked, h=hwnd: self.activate_external_app(h))
        insert_idx = 2 + len(self.app_buttons)
        self.layout.insertWidget(insert_idx, btn)
        self.app_buttons[hwnd] = btn

    def activate_browser(self):
        self.browser_win.setWindowState(
            self.browser_win.windowState() & ~Qt.WindowState.WindowMinimized | Qt.WindowState.WindowActive)
        self.browser_win.activateWindow()
        self.browser_win.raise_()
        self.browser_win.browser.setFocus()
        self.btn_browser.setChecked(True)
        for btn in self.app_buttons.values(): btn.setChecked(False)

    def activate_external_app(self, hwnd):
        for tracker in self.app_trackers:
            if tracker.hwnd == hwnd:
                tracker.activate()
                break
        self.btn_browser.setChecked(False)
        for h, btn in self.app_buttons.items(): btn.setChecked(h == hwnd)

    def update_clock(self):
        self.lbl_clock.setText(QTime.currentTime().toString("hh:mm AP"))

    def attempt_quit(self):
        # Create a custom Dialog to ensure it shows ON TOP of the kiosk window
        dialog = QInputDialog(self)
        dialog.setWindowTitle("Unlock")
        dialog.setLabelText("Enter Password:")
        dialog.setTextEchoMode(QLineEdit.EchoMode.Password)
        dialog.setWindowFlags(Qt.WindowType.Dialog | Qt.WindowType.WindowStaysOnTopHint)

        if dialog.exec():
            password = dialog.textValue()
            h = hashlib.sha256(password.encode()).hexdigest()
            if h == self.config['security']['quit_hash'] or h == self.config['security']['admin_hash']:
                # 1. Unlock System
                self.locker.unblock_all()

                # 2. Force Kill External Apps (Fixes apps not closing)
                for tracker in self.app_trackers:
                    tracker.kill()

                # 3. Clear Session
                if self.config.get('exam', {}).get('clear_session_end', False):
                    self.browser_win.browser.page().profile().cookieStore().deleteAllCookies()

                # 4. Exit Application
                QApplication.quit()
                sys.exit(0)
            else:
                # Show error on top
                msg = QMessageBox(self)
                msg.setIcon(QMessageBox.Icon.Warning)
                msg.setWindowTitle("Error")
                msg.setText("Incorrect Password")
                msg.setWindowFlags(Qt.WindowType.Dialog | Qt.WindowType.WindowStaysOnTopHint)
                msg.exec()

    def closeEvent(self, event):
        event.ignore()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    if not os.path.exists(DEFAULT_DIR): os.makedirs(DEFAULT_DIR)
    filename, _ = QFileDialog.getOpenFileName(None, "Select Exam Configuration", DEFAULT_DIR, "SEB Config (*.seb)")
    if filename:
        taskbar = SebTaskbar(filename)
        taskbar.show()
        sys.exit(app.exec())
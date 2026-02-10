# import sys
# import json
# import hashlib
# import os  # <--- NEW: For path handling
# from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout,
#                              QHBoxLayout, QTabWidget, QLabel, QLineEdit,
#                              QCheckBox, QPushButton, QFileDialog, QMessageBox,
#                              QGroupBox, QListWidget, QComboBox)
# from cryptography.fernet import Fernet
#
# # --- SECURITY KEY (MUST MATCH BROWSER APP) ---
# VALID_KEY = b'Z7wQ_0pZ9G9yJ_c8_k1_s2_u3_v4_w5_x6_y7_z8_A9='
#
# # --- FIXED SAVE PATH ---
# SAVE_DIR = r"C:\Dev\nextsloves seb"
#
#
# class ConflictTool(QMainWindow):
#     def __init__(self):
#         super().__init__()
#
#         self.setWindowTitle("NextSolves - SEB Config Tool")
#         self.setGeometry(100, 100, 650, 750)
#
#         # Main Layout
#         central_widget = QWidget()
#         self.setCentralWidget(central_widget)
#         layout = QVBoxLayout(central_widget)
#
#         # Tabs
#         self.tabs = QTabWidget()
#         layout.addWidget(self.tabs)
#
#         # Initialize Tabs
#         self.init_general_tab()
#         self.init_ui_tab()
#         self.init_network_tab()
#         self.init_down_upload_tab()
#         self.init_exam_tab()
#         self.init_taskbar_tab()
#         self.init_hockey_tab()
#         self.init_application_tab()
#
#         # Save Button
#         self.btn_save = QPushButton("Save Configuration & Encrypt")
#         self.btn_save.setFixedHeight(50)
#         self.btn_save.setStyleSheet("background-color: #0078D7; color: white; font-weight: bold; font-size: 14px;")
#         self.btn_save.clicked.connect(self.save_configuration)
#         layout.addWidget(self.btn_save)
#
#     def init_general_tab(self):
#         tab = QWidget()
#         layout = QVBoxLayout()
#
#         # --- SECTION 1: ADMIN PASSWORD ---
#         group_admin = QGroupBox("Administrator Access")
#         vbox_admin = QVBoxLayout()
#
#         vbox_admin.addWidget(QLabel("Set Administrator Password:"))
#         self.input_admin_pass = QLineEdit()
#         self.input_admin_pass.setEchoMode(QLineEdit.EchoMode.Password)
#         vbox_admin.addWidget(self.input_admin_pass)
#
#         vbox_admin.addWidget(QLabel("Confirm Administrator Password:"))
#         self.input_admin_conf = QLineEdit()
#         self.input_admin_conf.setEchoMode(QLineEdit.EchoMode.Password)
#         vbox_admin.addWidget(self.input_admin_conf)
#
#         group_admin.setLayout(vbox_admin)
#         layout.addWidget(group_admin)
#
#         # --- SECTION 2: QUIT PASSWORD ---
#         group_quit = QGroupBox("Exit / Unlock Settings")
#         vbox_quit = QVBoxLayout()
#
#         self.chk_allow_quit = QCheckBox("Allow User to Quit SEB")
#         self.chk_allow_quit.setChecked(True)
#         vbox_quit.addWidget(self.chk_allow_quit)
#
#         vbox_quit.addWidget(QLabel("Set Quit/Unlock Password:"))
#         self.input_quit_pass = QLineEdit()
#         self.input_quit_pass.setEchoMode(QLineEdit.EchoMode.Password)
#         vbox_quit.addWidget(self.input_quit_pass)
#
#         vbox_quit.addWidget(QLabel("Confirm Quit/Unlock Password:"))
#         self.input_quit_conf = QLineEdit()
#         self.input_quit_conf.setEchoMode(QLineEdit.EchoMode.Password)
#         vbox_quit.addWidget(self.input_quit_conf)
#
#         group_quit.setLayout(vbox_quit)
#         layout.addWidget(group_quit)
#
#         layout.addStretch()
#         tab.setLayout(layout)
#         self.tabs.addTab(tab, "General")
#
#     def init_ui_tab(self):
#         tab = QWidget()
#         layout = QVBoxLayout()
#
#         group_browser = QGroupBox("Browser View Mode")
#         vbox = QVBoxLayout()
#
#         self.chk_fullscreen = QCheckBox("Full Screen Mode")
#         self.chk_fullscreen.setChecked(True)
#
#         self.chk_touch = QCheckBox("Touch Optimized Interface")
#
#         vbox.addWidget(self.chk_fullscreen)
#         vbox.addWidget(self.chk_touch)
#         group_browser.setLayout(vbox)
#         layout.addWidget(group_browser)
#
#         group_win = QGroupBox("Main Window Size/Position")
#         vbox2 = QVBoxLayout()
#         vbox2.addWidget(QLabel("Width/Height: 100% (Forced)"))
#         vbox2.addWidget(QLabel("Position: Central"))
#         group_win.setLayout(vbox2)
#         layout.addWidget(group_win)
#
#         self.chk_zoom = QCheckBox("Enable Page Zoom")
#         layout.addWidget(self.chk_zoom)
#
#         self.chk_spell = QCheckBox("Enable Spell Checker (English Only)")
#         layout.addWidget(self.chk_spell)
#
#         layout.addStretch()
#         tab.setLayout(layout)
#         self.tabs.addTab(tab, "User Interface")
#
#     def init_network_tab(self):
#         tab = QWidget()
#         layout = QVBoxLayout()
#
#         group_net = QGroupBox("Exam URLs")
#         vbox = QVBoxLayout()
#
#         vbox.addWidget(QLabel("Enter URL (First URL is Start Page):"))
#
#         hbox = QHBoxLayout()
#         self.input_url = QLineEdit()
#         self.input_url.setPlaceholderText("https://www.example.com/exam")
#         self.btn_add_url = QPushButton("Add URL")
#         self.btn_add_url.clicked.connect(self.add_url_to_list)
#
#         hbox.addWidget(self.input_url)
#         hbox.addWidget(self.btn_add_url)
#         vbox.addLayout(hbox)
#
#         vbox.addWidget(QLabel("Allowed URLs List:"))
#         self.list_urls = QListWidget()
#         vbox.addWidget(self.list_urls)
#
#         self.btn_remove_url = QPushButton("Remove Selected URL")
#         self.btn_remove_url.clicked.connect(self.remove_url_from_list)
#         vbox.addWidget(self.btn_remove_url)
#
#         group_net.setLayout(vbox)
#         layout.addWidget(group_net)
#
#         layout.addStretch()
#         tab.setLayout(layout)
#         self.tabs.addTab(tab, "Network")
#
#     def add_url_to_list(self):
#         url = self.input_url.text().strip()
#         if url:
#             if not url.startswith("http"):
#                 url = "https://" + url
#             self.list_urls.addItem(url)
#             self.input_url.clear()
#
#     def remove_url_from_list(self):
#         row = self.list_urls.currentRow()
#         if row >= 0:
#             self.list_urls.takeItem(row)
#
#     def init_down_upload_tab(self):
#         tab = QWidget()
#         layout = QVBoxLayout()
#
#         # Group 1: Downloads
#         group_down = QGroupBox("Downloading")
#         vbox_down = QVBoxLayout()
#
#         self.chk_allow_down = QCheckBox("Allow downloading files")
#         vbox_down.addWidget(self.chk_allow_down)
#
#         # Download Directory Selection
#         hbox_dir = QHBoxLayout()
#         self.input_down_dir = QLineEdit()
#         self.input_down_dir.setPlaceholderText("Standard Download Directory")
#         self.btn_choose_dir = QPushButton("Choose Directory...")
#         self.btn_choose_dir.clicked.connect(self.choose_download_directory)
#         hbox_dir.addWidget(self.input_down_dir)
#         hbox_dir.addWidget(self.btn_choose_dir)
#         vbox_down.addLayout(hbox_dir)
#
#         # Mac Directory
#         hbox_mac = QHBoxLayout()
#         hbox_mac.addWidget(QLabel("Download directory on Mac:"))
#         self.input_mac_dir = QLineEdit()
#         self.input_mac_dir.setPlaceholderText("~/Downloads")
#         hbox_mac.addWidget(self.input_mac_dir)
#         vbox_down.addLayout(hbox_mac)
#
#         self.chk_custom_dir = QCheckBox("Allow user to select custom download / upload directory")
#         self.chk_temp_dir = QCheckBox("Use temporary download / upload directory")
#         self.chk_show_fs_path = QCheckBox("Show path of file system elements (Win)")
#
#         vbox_down.addWidget(self.chk_custom_dir)
#         vbox_down.addWidget(self.chk_temp_dir)
#         vbox_down.addWidget(self.chk_show_fs_path)
#
#         group_down.setLayout(vbox_down)
#         layout.addWidget(group_down)
#
#         # Group 2: Uploads
#         group_up = QGroupBox("Uploading")
#         vbox_up = QVBoxLayout()
#
#         self.chk_allow_up = QCheckBox("Allow uploading files")
#         vbox_up.addWidget(self.chk_allow_up)
#
#         vbox_up.addWidget(QLabel("Choose file to upload... (Policy):"))
#         self.combo_upload_policy = QComboBox()
#         self.combo_upload_policy.addItems([
#             "manually with file requester",
#             "by attempting to upload the same file downloaded before",
#             "by only allowing to upload the same file downloaded before"
#         ])
#         vbox_up.addWidget(self.combo_upload_policy)
#
#         group_up.setLayout(vbox_up)
#         layout.addWidget(group_up)
#
#         # Group 3: File Handling
#         group_files = QGroupBox("File Handling")
#         vbox_files = QVBoxLayout()
#
#         self.chk_down_pdf = QCheckBox("Download PDF files instead of displaying them inline")
#         self.chk_acrobat = QCheckBox("Allow using Acrobat Reader PDF plugin")
#         self.chk_open_seb = QCheckBox("Download and open SEB Config Files")
#
#         vbox_files.addWidget(self.chk_down_pdf)
#         vbox_files.addWidget(self.chk_acrobat)
#         vbox_files.addWidget(self.chk_open_seb)
#
#         group_files.setLayout(vbox_files)
#         layout.addWidget(group_files)
#
#         layout.addStretch()
#         tab.setLayout(layout)
#         self.tabs.addTab(tab, "Down/Uploads")
#
#     def choose_download_directory(self):
#         directory = QFileDialog.getExistingDirectory(self, "Select Download Directory")
#         if directory:
#             self.input_down_dir.setText(directory)
#
#     def init_exam_tab(self):
#         tab = QWidget()
#         layout = QVBoxLayout()
#
#         group_session = QGroupBox("Session Handling")
#         vbox = QVBoxLayout()
#
#         lbl_info = QLabel("Use the following parameters to control whether a browser session is persisted on disk.")
#         lbl_info.setWordWrap(True)
#         vbox.addWidget(lbl_info)
#
#         self.chk_clear_session_start = QCheckBox("Clear browser session when starting an exam or starting SEB")
#         self.chk_clear_session_end = QCheckBox("Clear browser session when ending an exam or terminating SEB")
#         self.chk_clear_session_end.setToolTip("Prevents deletion of browser cache if deactivated!")
#
#         vbox.addWidget(self.chk_clear_session_start)
#         vbox.addWidget(self.chk_clear_session_end)
#
#         group_session.setLayout(vbox)
#         layout.addWidget(group_session)
#
#         layout.addStretch()
#         tab.setLayout(layout)
#         self.tabs.addTab(tab, "Exam")
#
#     def init_taskbar_tab(self):
#         tab = QWidget()
#         layout = QVBoxLayout()
#
#         layout.addWidget(QLabel("Select elements to show on the custom taskbar:"))
#
#         self.chk_show_wifi = QCheckBox("Show Wi-Fi Control")
#         self.chk_show_time = QCheckBox("Show Time")
#         self.chk_show_reload = QCheckBox("Show Reload Button")
#         self.chk_show_keyboard = QCheckBox("Show Keyboard Layout")
#
#         layout.addWidget(self.chk_show_wifi)
#         layout.addWidget(self.chk_show_time)
#         layout.addWidget(self.chk_show_reload)
#         layout.addWidget(self.chk_show_keyboard)
#
#         layout.addStretch()
#         tab.setLayout(layout)
#         self.tabs.addTab(tab, "Taskbar")
#
#     def init_hockey_tab(self):
#         tab = QWidget()
#         layout = QVBoxLayout()
#
#         layout.addWidget(QLabel("<b>Special Keys Blocking:</b>"))
#         layout.addWidget(QLabel("Check to ENABLE blocking (Disable the key)"))
#
#         self.chk_block_esc = QCheckBox("Block Escape (Esc)")
#         self.chk_block_ctrl_esc = QCheckBox("Block Ctrl+Esc (Start Menu)")
#         self.chk_block_alt_esc = QCheckBox("Block Alt+Esc")
#         self.chk_block_alt_tab = QCheckBox("Block Alt+Tab (App Switcher)")
#         self.chk_block_f_keys = QCheckBox("Block Function Keys (F1-F12)")
#         self.chk_block_right_click = QCheckBox("Block Mouse Right Click")
#
#         layout.addWidget(self.chk_block_esc)
#         layout.addWidget(self.chk_block_ctrl_esc)
#         layout.addWidget(self.chk_block_alt_esc)
#         layout.addWidget(self.chk_block_alt_tab)
#         layout.addWidget(self.chk_block_f_keys)
#         layout.addWidget(self.chk_block_right_click)
#
#         layout.addStretch()
#         tab.setLayout(layout)
#         self.tabs.addTab(tab, "Hockey (Keys)")
#
#     def init_application_tab(self):
#         tab = QWidget()
#         layout = QVBoxLayout()
#
#         group_apps = QGroupBox("Allowed Applications")
#         vbox = QVBoxLayout()
#
#         vbox.addWidget(QLabel("Select Application Path (.exe):"))
#
#         hbox_browse = QHBoxLayout()
#         self.input_app_path = QLineEdit()
#         self.btn_browse = QPushButton("Browse")
#         self.btn_browse.clicked.connect(self.browse_file)
#         hbox_browse.addWidget(self.input_app_path)
#         hbox_browse.addWidget(self.btn_browse)
#         vbox.addLayout(hbox_browse)
#
#         self.btn_add_app = QPushButton("Add Application to List")
#         self.btn_add_app.clicked.connect(self.add_app_to_list)
#         vbox.addWidget(self.btn_add_app)
#
#         vbox.addWidget(QLabel("Applications to Launch:"))
#         self.list_apps = QListWidget()
#         vbox.addWidget(self.list_apps)
#
#         self.btn_remove_app = QPushButton("Remove Selected Application")
#         self.btn_remove_app.clicked.connect(self.remove_app_from_list)
#         vbox.addWidget(self.btn_remove_app)
#
#         group_apps.setLayout(vbox)
#         layout.addWidget(group_apps)
#
#         layout.addStretch()
#         tab.setLayout(layout)
#         self.tabs.addTab(tab, "Applications")
#
#     def browse_file(self):
#         fname, _ = QFileDialog.getOpenFileName(self, 'Open File', 'c:\\', "Executables (*.exe)")
#         if fname:
#             self.input_app_path.setText(fname)
#
#     def add_app_to_list(self):
#         path = self.input_app_path.text().strip()
#         if path:
#             self.list_apps.addItem(path)
#             self.input_app_path.clear()
#
#     def remove_app_from_list(self):
#         row = self.list_apps.currentRow()
#         if row >= 0:
#             self.list_apps.takeItem(row)
#
#     def save_configuration(self):
#         # 1. Validation
#         if self.input_admin_pass.text() != self.input_admin_conf.text():
#             QMessageBox.critical(self, "Error", "Administrator passwords do not match!")
#             return
#
#         if self.input_quit_pass.text() != self.input_quit_conf.text():
#             QMessageBox.critical(self, "Error", "Quit/Unlock passwords do not match!")
#             return
#
#         # Get URLs and Apps
#         url_list = []
#         for i in range(self.list_urls.count()):
#             url_list.append(self.list_urls.item(i).text())
#
#         app_list = []
#         for i in range(self.list_apps.count()):
#             app_list.append(self.list_apps.item(i).text())
#
#         if not url_list and not app_list:
#             QMessageBox.warning(self, "Warning", "Please add at least one URL or Application path.")
#             return
#
#         # 2. Prepare Data
#         admin_hash = hashlib.sha256(self.input_admin_pass.text().encode()).hexdigest()
#         quit_hash = hashlib.sha256(self.input_quit_pass.text().encode()).hexdigest()
#
#         start_url = url_list[0] if url_list else ""
#
#         config_data = {
#             "security": {
#                 "admin_hash": admin_hash,
#                 "quit_hash": quit_hash,
#                 "allow_quit": self.chk_allow_quit.isChecked()
#             },
#             "ui": {
#                 "fullscreen": self.chk_fullscreen.isChecked(),
#                 "touch_mode": self.chk_touch.isChecked(),
#                 "zoom_enabled": self.chk_zoom.isChecked(),
#                 "spell_check": self.chk_spell.isChecked()
#             },
#             "down_uploads": {
#                 "allow_download": self.chk_allow_down.isChecked(),
#                 "directory": self.input_down_dir.text(),
#                 "mac_directory": self.input_mac_dir.text(),
#                 "allow_custom_dir": self.chk_custom_dir.isChecked(),
#                 "use_temp_dir": self.chk_temp_dir.isChecked(),
#                 "show_fs_path": self.chk_show_fs_path.isChecked(),
#                 "allow_upload": self.chk_allow_up.isChecked(),
#                 "upload_policy": self.combo_upload_policy.currentText(),
#                 "download_pdf": self.chk_down_pdf.isChecked(),
#                 "allow_acrobat": self.chk_acrobat.isChecked(),
#                 "open_seb_config": self.chk_open_seb.isChecked()
#             },
#             "exam": {
#                 "clear_session_start": self.chk_clear_session_start.isChecked(),
#                 "clear_session_end": self.chk_clear_session_end.isChecked()
#             },
#             "taskbar": {
#                 "wifi": self.chk_show_wifi.isChecked(),
#                 "time": self.chk_show_time.isChecked(),
#                 "reload": self.chk_show_reload.isChecked()
#             },
#             "keys": {
#                 "block_alt_tab": self.chk_block_alt_tab.isChecked(),
#                 "block_win": self.chk_block_ctrl_esc.isChecked(),
#                 "block_esc": self.chk_block_esc.isChecked(),
#                 "block_right_click": self.chk_block_right_click.isChecked()
#             },
#             "network": {
#                 "start_url": start_url,
#                 "allowed_urls": url_list
#             },
#             "app": {
#                 "paths": app_list
#             }
#         }
#
#         # 3. Encrypt & Save to FIXED PATH
#         try:
#             # Ensure Directory Exists
#             if not os.path.exists(SAVE_DIR):
#                 os.makedirs(SAVE_DIR)
#
#             full_path = os.path.join(SAVE_DIR, "exam_config.seb")
#
#             json_str = json.dumps(config_data)
#             cipher_suite = Fernet(VALID_KEY)
#             encrypted_data = cipher_suite.encrypt(json_str.encode())
#
#             with open(full_path, "wb") as f:
#                 f.write(encrypted_data)
#
#             QMessageBox.information(self, "Success", f"Configuration saved to:\n{full_path}")
#
#         except Exception as e:
#             QMessageBox.critical(self, "Error", f"Failed to save: {str(e)}")
#
#
# if __name__ == "__main__":
#     app = QApplication(sys.argv)
#     window = ConflictTool()
#     window.show()
#     sys.exit(app.exec())

import sys
import json
import hashlib
import os
from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout,
                             QHBoxLayout, QTabWidget, QLabel, QLineEdit,
                             QCheckBox, QPushButton, QFileDialog, QMessageBox,
                             QGroupBox, QListWidget, QComboBox)
from PyQt6.QtCore import Qt
from cryptography.fernet import Fernet

# --- SECURITY KEY (MUST MATCH BROWSER APP) ---
VALID_KEY = b'Z7wQ_0pZ9G9yJ_c8_k1_s2_u3_v4_w5_x6_y7_z8_A9='

# --- FIXED SAVE PATH ---
SAVE_DIR = r"C:\Dev\nextsloves seb"

# --- NEW "WHITE/BLUE/ORANGE" STYLESHEET ---
STYLESHEET = """
QMainWindow {
    background-color: #ffffff;
}
QWidget {
    color: #333333;
    font-family: 'Segoe UI', sans-serif;
    font-size: 14px;
}
/* TABS */
QTabWidget::pane {
    border: 1px solid #d0d0d0;
    background: #fdfdfd;
    border-radius: 4px;
}
QTabBar::tab {
    background: #e0e0e0;
    color: #555555;
    padding: 10px 20px;
    border-top-left-radius: 4px;
    border-top-right-radius: 4px;
    margin-right: 2px;
}
QTabBar::tab:selected {
    background: #ffffff;
    color: #0078d7; /* Blue Text */
    border-top: 3px solid #ff9800; /* Orange Accent Line */
    font-weight: bold;
}

/* GROUP BOXES */
QGroupBox {
    border: 1px solid #cccccc;
    border-radius: 6px;
    margin-top: 20px;
    font-weight: bold;
    color: #005a9e; /* Strong Blue Title */
}
QGroupBox::title {
    subcontrol-origin: margin;
    subcontrol-position: top left;
    padding: 0 5px;
    left: 10px;
}

/* INPUTS */
QLineEdit {
    background-color: #ffffff;
    border: 1px solid #cccccc;
    border-radius: 4px;
    padding: 6px;
    color: #333333;
}
QLineEdit:focus {
    border: 2px solid #ff9800; /* Orange Focus Border */
}
QComboBox {
    background-color: #ffffff;
    border: 1px solid #cccccc;
    border-radius: 4px;
    padding: 5px;
}

/* BUTTONS */
QPushButton {
    background-color: #0078d7; /* Standard Blue */
    color: white;
    border: none;
    padding: 8px 16px;
    border-radius: 4px;
    font-weight: bold;
}
QPushButton:hover {
    background-color: #005a9e; /* Darker Blue */
}
QPushButton:pressed {
    background-color: #004578;
}

/* SPECIAL BUTTONS */
QPushButton#SaveBtn {
    background-color: #ff9800; /* Orange for Save */
    font-size: 15px;
}
QPushButton#SaveBtn:hover {
    background-color: #f57c00;
}
QPushButton#RemoveBtn {
    background-color: #ffffff;
    color: #d32f2f;
    border: 1px solid #d32f2f;
}
QPushButton#RemoveBtn:hover {
    background-color: #ffebee;
}

/* LISTS & CHECKBOXES */
QListWidget {
    background-color: #ffffff;
    border: 1px solid #cccccc;
    border-radius: 4px;
}
QCheckBox {
    spacing: 8px;
}
QCheckBox::indicator {
    width: 18px;
    height: 18px;
    background: #ffffff;
    border: 1px solid #999999;
    border-radius: 3px;
}
QCheckBox::indicator:checked {
    background: #0078d7;
    border: 1px solid #0078d7;
    image: url(data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHdpZHRoPSIyNCIgaGVpZ2h0PSIyNCIgdmlld0JveD0iMCAwIDI0IDI0IiBmaWxsPSJub25lIiBzdHJva2U9IndoaXRlIiBzdHJva2Utd2lkdGg9IjMiIHN0cm9rZS1saW5lY2FwPSJyb3VuZCIgc3Ryb2tlLWxpbmVqb2luPSJyb3VuZCI+PHBvbHlsaW5lIHBvaW50cz0iMjAgNiA5IDE3IDQgMTIiPjwvcG9seWxpbmU+PC9zdmc+);
}
"""


class ConflictTool(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("NextSolves - SEB Config Tool")
        self.setGeometry(100, 100, 800, 750)
        self.setStyleSheet(STYLESHEET)  # Apply New Theme

        # Main Layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(15)

        # Header
        lbl_header = QLabel("Exam Configuration")
        lbl_header.setStyleSheet("font-size: 26px; font-weight: bold; color: #0078d7; margin-bottom: 5px;")
        layout.addWidget(lbl_header)

        # Tabs
        self.tabs = QTabWidget()
        layout.addWidget(self.tabs)

        # Initialize Tabs
        self.init_general_tab()
        self.init_ui_tab()
        self.init_network_tab()
        self.init_down_upload_tab()
        self.init_exam_tab()
        self.init_taskbar_tab()
        self.init_hockey_tab()
        self.init_application_tab()

        # Save Button Container
        btn_layout = QHBoxLayout()
        btn_layout.addStretch()

        self.btn_save = QPushButton("Save Configuration & Encrypt")
        self.btn_save.setObjectName("SaveBtn")  # Apply Orange Style
        self.btn_save.setMinimumWidth(250)
        self.btn_save.setMinimumHeight(45)
        self.btn_save.clicked.connect(self.save_configuration)

        btn_layout.addWidget(self.btn_save)
        btn_layout.addStretch()
        layout.addLayout(btn_layout)

    def init_general_tab(self):
        tab = QWidget()
        layout = QVBoxLayout()
        layout.setSpacing(15)

        # --- SECTION 1: ADMIN PASSWORD ---
        group_admin = QGroupBox("Administrator Access")
        vbox_admin = QVBoxLayout()
        vbox_admin.setSpacing(10)

        vbox_admin.addWidget(QLabel("Set Administrator Password:"))
        self.input_admin_pass = QLineEdit()
        self.input_admin_pass.setEchoMode(QLineEdit.EchoMode.Password)
        vbox_admin.addWidget(self.input_admin_pass)

        vbox_admin.addWidget(QLabel("Confirm Administrator Password:"))
        self.input_admin_conf = QLineEdit()
        self.input_admin_conf.setEchoMode(QLineEdit.EchoMode.Password)
        vbox_admin.addWidget(self.input_admin_conf)

        group_admin.setLayout(vbox_admin)
        layout.addWidget(group_admin)

        # --- SECTION 2: QUIT PASSWORD ---
        group_quit = QGroupBox("Exit / Unlock Settings")
        vbox_quit = QVBoxLayout()
        vbox_quit.setSpacing(10)

        self.chk_allow_quit = QCheckBox("Allow User to Quit SEB")
        self.chk_allow_quit.setChecked(True)
        vbox_quit.addWidget(self.chk_allow_quit)

        vbox_quit.addWidget(QLabel("Set Quit/Unlock Password:"))
        self.input_quit_pass = QLineEdit()
        self.input_quit_pass.setEchoMode(QLineEdit.EchoMode.Password)
        vbox_quit.addWidget(self.input_quit_pass)

        vbox_quit.addWidget(QLabel("Confirm Quit/Unlock Password:"))
        self.input_quit_conf = QLineEdit()
        self.input_quit_conf.setEchoMode(QLineEdit.EchoMode.Password)
        vbox_quit.addWidget(self.input_quit_conf)

        group_quit.setLayout(vbox_quit)
        layout.addWidget(group_quit)

        layout.addStretch()
        tab.setLayout(layout)
        self.tabs.addTab(tab, "General")

    def init_ui_tab(self):
        tab = QWidget()
        layout = QVBoxLayout()

        group_browser = QGroupBox("Browser View Mode")
        vbox = QVBoxLayout()
        self.chk_fullscreen = QCheckBox("Full Screen Mode")
        self.chk_fullscreen.setChecked(True)
        self.chk_touch = QCheckBox("Touch Optimized Interface")
        vbox.addWidget(self.chk_fullscreen)
        vbox.addWidget(self.chk_touch)
        group_browser.setLayout(vbox)
        layout.addWidget(group_browser)

        group_win = QGroupBox("Main Window Settings")
        vbox2 = QVBoxLayout()
        self.chk_zoom = QCheckBox("Enable Page Zoom")
        self.chk_spell = QCheckBox("Enable Spell Checker (English Only)")
        vbox2.addWidget(self.chk_zoom)
        vbox2.addWidget(self.chk_spell)
        group_win.setLayout(vbox2)
        layout.addWidget(group_win)

        layout.addStretch()
        tab.setLayout(layout)
        self.tabs.addTab(tab, "User Interface")

    def init_network_tab(self):
        tab = QWidget()
        layout = QVBoxLayout()

        group_net = QGroupBox("Exam URLs")
        vbox = QVBoxLayout()

        vbox.addWidget(QLabel("Enter URL (First URL is Start Page):"))

        hbox = QHBoxLayout()
        self.input_url = QLineEdit()
        self.input_url.setPlaceholderText("https://www.example.com/exam")
        self.btn_add_url = QPushButton("Add URL")
        self.btn_add_url.clicked.connect(self.add_url_to_list)

        hbox.addWidget(self.input_url)
        hbox.addWidget(self.btn_add_url)
        vbox.addLayout(hbox)

        vbox.addWidget(QLabel("Allowed URLs List:"))
        self.list_urls = QListWidget()
        vbox.addWidget(self.list_urls)

        self.btn_remove_url = QPushButton("Remove Selected URL")
        self.btn_remove_url.setObjectName("RemoveBtn")  # Red/White style
        self.btn_remove_url.clicked.connect(self.remove_url_from_list)
        vbox.addWidget(self.btn_remove_url)

        group_net.setLayout(vbox)
        layout.addWidget(group_net)

        layout.addStretch()
        tab.setLayout(layout)
        self.tabs.addTab(tab, "Network")

    def add_url_to_list(self):
        url = self.input_url.text().strip()
        if url:
            if not url.startswith("http"):
                url = "https://" + url
            self.list_urls.addItem(url)
            self.input_url.clear()

    def remove_url_from_list(self):
        row = self.list_urls.currentRow()
        if row >= 0:
            self.list_urls.takeItem(row)

    def init_down_upload_tab(self):
        tab = QWidget()
        layout = QVBoxLayout()

        group_down = QGroupBox("Downloading")
        vbox_down = QVBoxLayout()
        self.chk_allow_down = QCheckBox("Allow downloading files")
        vbox_down.addWidget(self.chk_allow_down)

        hbox_dir = QHBoxLayout()
        self.input_down_dir = QLineEdit()
        self.input_down_dir.setPlaceholderText("Standard Download Directory")
        self.btn_choose_dir = QPushButton("Choose...")
        self.btn_choose_dir.clicked.connect(self.choose_download_directory)
        hbox_dir.addWidget(self.input_down_dir)
        hbox_dir.addWidget(self.btn_choose_dir)
        vbox_down.addLayout(hbox_dir)

        hbox_mac = QHBoxLayout()
        hbox_mac.addWidget(QLabel("Mac Directory:"))
        self.input_mac_dir = QLineEdit()
        self.input_mac_dir.setPlaceholderText("~/Downloads")
        hbox_mac.addWidget(self.input_mac_dir)
        vbox_down.addLayout(hbox_mac)

        self.chk_custom_dir = QCheckBox("Allow user to select custom download directory")
        self.chk_temp_dir = QCheckBox("Use temporary download directory")
        self.chk_show_fs_path = QCheckBox("Show path of file system elements (Win)")
        vbox_down.addWidget(self.chk_custom_dir)
        vbox_down.addWidget(self.chk_temp_dir)
        vbox_down.addWidget(self.chk_show_fs_path)
        group_down.setLayout(vbox_down)
        layout.addWidget(group_down)

        group_up = QGroupBox("Uploading")
        vbox_up = QVBoxLayout()
        self.chk_allow_up = QCheckBox("Allow uploading files")
        vbox_up.addWidget(self.chk_allow_up)
        vbox_up.addWidget(QLabel("Upload Policy:"))
        self.combo_upload_policy = QComboBox()
        self.combo_upload_policy.addItems([
            "manually with file requester",
            "by attempting to upload the same file downloaded before",
            "by only allowing to upload the same file downloaded before"
        ])
        vbox_up.addWidget(self.combo_upload_policy)
        group_up.setLayout(vbox_up)
        layout.addWidget(group_up)

        group_files = QGroupBox("File Handling")
        vbox_files = QVBoxLayout()
        self.chk_down_pdf = QCheckBox("Download PDF files instead of displaying them inline")
        self.chk_acrobat = QCheckBox("Allow using Acrobat Reader PDF plugin")
        self.chk_open_seb = QCheckBox("Download and open SEB Config Files")
        vbox_files.addWidget(self.chk_down_pdf)
        vbox_files.addWidget(self.chk_acrobat)
        vbox_files.addWidget(self.chk_open_seb)
        group_files.setLayout(vbox_files)
        layout.addWidget(group_files)

        layout.addStretch()
        tab.setLayout(layout)
        self.tabs.addTab(tab, "Down/Uploads")

    def choose_download_directory(self):
        directory = QFileDialog.getExistingDirectory(self, "Select Download Directory")
        if directory:
            self.input_down_dir.setText(directory)

    def init_exam_tab(self):
        tab = QWidget()
        layout = QVBoxLayout()

        group_session = QGroupBox("Session Handling")
        vbox = QVBoxLayout()
        lbl_info = QLabel("Control whether browser session (cookies/cache) is persisted.")
        lbl_info.setStyleSheet("color: #777777; font-style: italic;")
        vbox.addWidget(lbl_info)

        self.chk_clear_session_start = QCheckBox("Clear browser session when starting an exam")
        self.chk_clear_session_end = QCheckBox("Clear browser session when ending an exam")
        vbox.addWidget(self.chk_clear_session_start)
        vbox.addWidget(self.chk_clear_session_end)
        group_session.setLayout(vbox)
        layout.addWidget(group_session)

        layout.addStretch()
        tab.setLayout(layout)
        self.tabs.addTab(tab, "Exam")

    def init_taskbar_tab(self):
        tab = QWidget()
        layout = QVBoxLayout()

        group_task = QGroupBox("Custom Taskbar Elements")
        vbox = QVBoxLayout()
        self.chk_show_wifi = QCheckBox("Show Wi-Fi Control")
        self.chk_show_time = QCheckBox("Show Time")
        self.chk_show_reload = QCheckBox("Show Reload Button")
        self.chk_show_keyboard = QCheckBox("Show Keyboard Layout")
        vbox.addWidget(self.chk_show_wifi)
        vbox.addWidget(self.chk_show_time)
        vbox.addWidget(self.chk_show_reload)
        vbox.addWidget(self.chk_show_keyboard)
        group_task.setLayout(vbox)
        layout.addWidget(group_task)

        layout.addStretch()
        tab.setLayout(layout)
        self.tabs.addTab(tab, "Taskbar")

    def init_hockey_tab(self):
        tab = QWidget()
        layout = QVBoxLayout()

        group_keys = QGroupBox("Lockdown Keys")
        vbox = QVBoxLayout()
        self.chk_block_esc = QCheckBox("Block Escape (Esc)")
        self.chk_block_ctrl_esc = QCheckBox("Block Ctrl+Esc (Start Menu)")
        self.chk_block_alt_esc = QCheckBox("Block Alt+Esc")
        self.chk_block_alt_tab = QCheckBox("Block Alt+Tab (App Switcher)")
        self.chk_block_f_keys = QCheckBox("Block Function Keys (F1-F12)")
        self.chk_block_right_click = QCheckBox("Block Mouse Right Click")

        vbox.addWidget(self.chk_block_esc)
        vbox.addWidget(self.chk_block_ctrl_esc)
        vbox.addWidget(self.chk_block_alt_esc)
        vbox.addWidget(self.chk_block_alt_tab)
        vbox.addWidget(self.chk_block_f_keys)
        vbox.addWidget(self.chk_block_right_click)
        group_keys.setLayout(vbox)
        layout.addWidget(group_keys)

        layout.addStretch()
        tab.setLayout(layout)
        self.tabs.addTab(tab, "Hooked Keys")

    def init_application_tab(self):
        tab = QWidget()
        layout = QVBoxLayout()

        group_apps = QGroupBox("Allowed Applications")
        vbox = QVBoxLayout()

        hbox_browse = QHBoxLayout()
        self.input_app_path = QLineEdit()
        self.input_app_path.setPlaceholderText("Path to .exe")
        self.btn_browse = QPushButton("Browse")
        self.btn_browse.clicked.connect(self.browse_file)
        hbox_browse.addWidget(self.input_app_path)
        hbox_browse.addWidget(self.btn_browse)
        vbox.addLayout(hbox_browse)

        self.btn_add_app = QPushButton("Add Application to List")
        self.btn_add_app.clicked.connect(self.add_app_to_list)
        vbox.addWidget(self.btn_add_app)

        vbox.addWidget(QLabel("Applications List:"))
        self.list_apps = QListWidget()
        vbox.addWidget(self.list_apps)

        self.btn_remove_app = QPushButton("Remove Selected Application")
        self.btn_remove_app.setObjectName("RemoveBtn")  # Apply Red Style
        self.btn_remove_app.clicked.connect(self.remove_app_from_list)
        vbox.addWidget(self.btn_remove_app)

        group_apps.setLayout(vbox)
        layout.addWidget(group_apps)

        layout.addStretch()
        tab.setLayout(layout)
        self.tabs.addTab(tab, "Applications")

    def browse_file(self):
        fname, _ = QFileDialog.getOpenFileName(self, 'Open File', 'c:\\', "Executables (*.exe)")
        if fname:
            self.input_app_path.setText(fname)

    def add_app_to_list(self):
        path = self.input_app_path.text().strip()
        if path:
            self.list_apps.addItem(path)
            self.input_app_path.clear()

    def remove_app_from_list(self):
        row = self.list_apps.currentRow()
        if row >= 0:
            self.list_apps.takeItem(row)

    def save_configuration(self):
        # 1. Validation
        if self.input_admin_pass.text() != self.input_admin_conf.text():
            QMessageBox.critical(self, "Error", "Administrator passwords do not match!")
            return
        if self.input_quit_pass.text() != self.input_quit_conf.text():
            QMessageBox.critical(self, "Error", "Quit/Unlock passwords do not match!")
            return

        url_list = [self.list_urls.item(i).text() for i in range(self.list_urls.count())]
        app_list = [self.list_apps.item(i).text() for i in range(self.list_apps.count())]

        if not url_list and not app_list:
            QMessageBox.warning(self, "Warning", "Please add at least one URL or Application path.")
            return

        # 2. Prepare Data
        admin_hash = hashlib.sha256(self.input_admin_pass.text().encode()).hexdigest()
        quit_hash = hashlib.sha256(self.input_quit_pass.text().encode()).hexdigest()
        start_url = url_list[0] if url_list else ""

        config_data = {
            "security": {"admin_hash": admin_hash, "quit_hash": quit_hash,
                         "allow_quit": self.chk_allow_quit.isChecked()},
            "ui": {"fullscreen": self.chk_fullscreen.isChecked(), "touch_mode": self.chk_touch.isChecked(),
                   "zoom_enabled": self.chk_zoom.isChecked(), "spell_check": self.chk_spell.isChecked()},
            "down_uploads": {
                "allow_download": self.chk_allow_down.isChecked(), "directory": self.input_down_dir.text(),
                "mac_directory": self.input_mac_dir.text(),  # Added Mac dir to JSON
                "allow_custom_dir": self.chk_custom_dir.isChecked(), "use_temp_dir": self.chk_temp_dir.isChecked(),
                "show_fs_path": self.chk_show_fs_path.isChecked(), "allow_upload": self.chk_allow_up.isChecked(),
                "upload_policy": self.combo_upload_policy.currentText(),
                "download_pdf": self.chk_down_pdf.isChecked(), "allow_acrobat": self.chk_acrobat.isChecked(),
                "open_seb_config": self.chk_open_seb.isChecked()
            },
            "exam": {"clear_session_start": self.chk_clear_session_start.isChecked(),
                     "clear_session_end": self.chk_clear_session_end.isChecked()},
            "taskbar": {"wifi": self.chk_show_wifi.isChecked(), "time": self.chk_show_time.isChecked(),
                        "reload": self.chk_show_reload.isChecked()},
            "keys": {"block_alt_tab": self.chk_block_alt_tab.isChecked(),
                     "block_win": self.chk_block_ctrl_esc.isChecked(), "block_esc": self.chk_block_esc.isChecked(),
                     "block_right_click": self.chk_block_right_click.isChecked()},
            "network": {"start_url": start_url, "allowed_urls": url_list},
            "app": {"paths": app_list}
        }

        # 3. Encrypt & Save to FIXED PATH
        try:
            if not os.path.exists(SAVE_DIR):
                os.makedirs(SAVE_DIR)
            full_path = os.path.join(SAVE_DIR, "exam_config.seb")

            cipher_suite = Fernet(VALID_KEY)
            encrypted_data = cipher_suite.encrypt(json.dumps(config_data).encode())

            with open(full_path, "wb") as f:
                f.write(encrypted_data)

            QMessageBox.information(self, "Success", f"Configuration saved to:\n{full_path}")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to save: {str(e)}")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ConflictTool()
    window.show()
    sys.exit(app.exec())
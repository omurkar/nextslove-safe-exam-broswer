import sys
import json
import hashlib
from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout,
                             QHBoxLayout, QTabWidget, QLabel, QLineEdit,
                             QCheckBox, QPushButton, QFileDialog, QMessageBox,
                             QGroupBox, QListWidget)
from cryptography.fernet import Fernet

# --- SECURITY KEY (MUST MATCH BROWSER APP) ---
VALID_KEY = b'Z7wQ_0pZ9G9yJ_c8_k1_s2_u3_v4_w5_x6_y7_z8_A9='


class ConflictTool(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("NextSolves - SEB Config Tool")
        self.setGeometry(100, 100, 600, 700)

        # Main Layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)

        # Tabs
        self.tabs = QTabWidget()
        layout.addWidget(self.tabs)

        # Initialize Tabs
        self.init_general_tab()
        self.init_ui_tab()
        self.init_network_tab()
        self.init_taskbar_tab()
        self.init_hockey_tab()
        self.init_application_tab()  # <--- Updated to support multiple apps

        # Save Button
        self.btn_save = QPushButton("Save Configuration & Encrypt")
        self.btn_save.setFixedHeight(50)
        self.btn_save.setStyleSheet("background-color: #0078D7; color: white; font-weight: bold; font-size: 14px;")
        self.btn_save.clicked.connect(self.save_configuration)
        layout.addWidget(self.btn_save)

    def init_general_tab(self):
        tab = QWidget()
        layout = QVBoxLayout()

        # --- SECTION 1: ADMIN PASSWORD ---
        group_admin = QGroupBox("Administrator Access")
        vbox_admin = QVBoxLayout()

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

        group_win = QGroupBox("Main Window Size/Position")
        vbox2 = QVBoxLayout()
        vbox2.addWidget(QLabel("Width/Height: 100% (Forced)"))
        vbox2.addWidget(QLabel("Position: Central"))
        group_win.setLayout(vbox2)
        layout.addWidget(group_win)

        self.chk_zoom = QCheckBox("Enable Page Zoom")
        layout.addWidget(self.chk_zoom)

        self.chk_spell = QCheckBox("Enable Spell Checker (English Only)")
        layout.addWidget(self.chk_spell)

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

    def init_taskbar_tab(self):
        tab = QWidget()
        layout = QVBoxLayout()

        layout.addWidget(QLabel("Select elements to show on the custom taskbar:"))

        self.chk_show_wifi = QCheckBox("Show Wi-Fi Control")
        self.chk_show_time = QCheckBox("Show Time")
        self.chk_show_reload = QCheckBox("Show Reload Button")
        self.chk_show_keyboard = QCheckBox("Show Keyboard Layout")

        layout.addWidget(self.chk_show_wifi)
        layout.addWidget(self.chk_show_time)
        layout.addWidget(self.chk_show_reload)
        layout.addWidget(self.chk_show_keyboard)

        layout.addStretch()
        tab.setLayout(layout)
        self.tabs.addTab(tab, "Taskbar")

    def init_hockey_tab(self):
        tab = QWidget()
        layout = QVBoxLayout()

        layout.addWidget(QLabel("<b>Special Keys Blocking:</b>"))
        layout.addWidget(QLabel("Check to ENABLE blocking (Disable the key)"))

        self.chk_block_esc = QCheckBox("Block Escape (Esc)")
        self.chk_block_ctrl_esc = QCheckBox("Block Ctrl+Esc (Start Menu)")
        self.chk_block_alt_esc = QCheckBox("Block Alt+Esc")
        self.chk_block_alt_tab = QCheckBox("Block Alt+Tab (App Switcher)")
        self.chk_block_f_keys = QCheckBox("Block Function Keys (F1-F12)")
        self.chk_block_right_click = QCheckBox("Block Mouse Right Click")

        layout.addWidget(self.chk_block_esc)
        layout.addWidget(self.chk_block_ctrl_esc)
        layout.addWidget(self.chk_block_alt_esc)
        layout.addWidget(self.chk_block_alt_tab)
        layout.addWidget(self.chk_block_f_keys)
        layout.addWidget(self.chk_block_right_click)

        layout.addStretch()
        tab.setLayout(layout)
        self.tabs.addTab(tab, "Hockey (Keys)")

    def init_application_tab(self):
        tab = QWidget()
        layout = QVBoxLayout()

        group_apps = QGroupBox("Allowed Applications")
        vbox = QVBoxLayout()

        vbox.addWidget(QLabel("Select Application Path (.exe):"))

        # Row 1: Input + Browse
        hbox_browse = QHBoxLayout()
        self.input_app_path = QLineEdit()
        self.btn_browse = QPushButton("Browse")
        self.btn_browse.clicked.connect(self.browse_file)
        hbox_browse.addWidget(self.input_app_path)
        hbox_browse.addWidget(self.btn_browse)
        vbox.addLayout(hbox_browse)

        # Row 2: Add Button
        self.btn_add_app = QPushButton("Add Application to List")
        self.btn_add_app.clicked.connect(self.add_app_to_list)
        vbox.addWidget(self.btn_add_app)

        # Row 3: List of Apps
        vbox.addWidget(QLabel("Applications to Launch:"))
        self.list_apps = QListWidget()
        vbox.addWidget(self.list_apps)

        # Row 4: Remove Button
        self.btn_remove_app = QPushButton("Remove Selected Application")
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

        # Get URLs
        url_list = []
        for i in range(self.list_urls.count()):
            url_list.append(self.list_urls.item(i).text())

        # Get Apps
        app_list = []
        for i in range(self.list_apps.count()):
            app_list.append(self.list_apps.item(i).text())

        # Ensure minimal config
        if not url_list and not app_list:
            QMessageBox.warning(self, "Warning", "Please add at least one URL or Application path.")
            return

        # 2. Prepare Data
        admin_hash = hashlib.sha256(self.input_admin_pass.text().encode()).hexdigest()
        quit_hash = hashlib.sha256(self.input_quit_pass.text().encode()).hexdigest()

        start_url = url_list[0] if url_list else ""

        config_data = {
            "security": {
                "admin_hash": admin_hash,
                "quit_hash": quit_hash,
                "allow_quit": self.chk_allow_quit.isChecked()
            },
            "ui": {
                "fullscreen": self.chk_fullscreen.isChecked(),
                "touch_mode": self.chk_touch.isChecked(),
                "zoom_enabled": self.chk_zoom.isChecked(),
                "spell_check": self.chk_spell.isChecked()
            },
            "taskbar": {
                "wifi": self.chk_show_wifi.isChecked(),
                "time": self.chk_show_time.isChecked(),
                "reload": self.chk_show_reload.isChecked()
            },
            "keys": {
                "block_alt_tab": self.chk_block_alt_tab.isChecked(),
                "block_win": self.chk_block_ctrl_esc.isChecked(),
                "block_esc": self.chk_block_esc.isChecked(),
                "block_right_click": self.chk_block_right_click.isChecked()
            },
            "network": {
                "start_url": start_url,
                "allowed_urls": url_list
            },
            "app": {
                "paths": app_list  # Changed from single "path" to list "paths"
            }
        }

        # 3. Encrypt & Save
        try:
            json_str = json.dumps(config_data)
            cipher_suite = Fernet(VALID_KEY)
            encrypted_data = cipher_suite.encrypt(json_str.encode())

            with open("exam_config.seb", "wb") as f:
                f.write(encrypted_data)

            QMessageBox.information(self, "Success", "Configuration saved as 'exam_config.seb' (Encrypted)")

        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to save: {str(e)}")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ConflictTool()
    window.show()
    sys.exit(app.exec())
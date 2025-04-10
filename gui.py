import os
from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QPushButton, QFileDialog, QLabel,
    QMessageBox, QLineEdit, QGroupBox, QApplication, QProgressDialog
)
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt, QTimer
from encryption_utils import encrypt_file, decrypt_file, is_valid_file_type
import sys
import pyperclip
import qdarkstyle


class EncryptionApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("🔐 Secure File Encryptor")
        self.setGeometry(100, 100, 500, 350)

        font_title = QFont("Arial", 12, QFont.Bold)

        layout = QVBoxLayout()

        # file selection
        file_group = QGroupBox("First, Select a File")
        file_layout = QVBoxLayout()
        self.label = QLabel("No file selected")
        self.label.setStyleSheet("color: gray")
        self.browse_button = QPushButton("📁 Browse")
        self.browse_button.clicked.connect(self.browse_file)
        file_layout.addWidget(self.label)
        file_layout.addWidget(self.browse_button)
        file_group.setLayout(file_layout)

        # encryption
        encrypt_group = QGroupBox("Second, Encrypt the File")
        encrypt_layout = QVBoxLayout()
        self.encrypt_button = QPushButton("🔒 Encrypt")
        self.encrypt_button.clicked.connect(self.encrypt_file)
        encrypt_layout.addWidget(self.encrypt_button)
        encrypt_group.setLayout(encrypt_layout)

        # decryption
        decrypt_group = QGroupBox("Last of All, Decrypt the File")
        decrypt_layout = QVBoxLayout()
        self.key_input = QLineEdit()
        self.key_input.setPlaceholderText("Enter decryption key")
        self.decrypt_button = QPushButton("🔓 Decrypt")
        self.decrypt_button.clicked.connect(self.decrypt_file)
        decrypt_layout.addWidget(self.key_input)
        decrypt_layout.addWidget(self.decrypt_button)
        decrypt_group.setLayout(decrypt_layout)

        # status Bar
        self.status_label = QLabel("Ready")
        self.status_label.setStyleSheet("color: lightgray; font-style: italic;")
        self.status_label.setAlignment(Qt.AlignCenter)

        # Add groups to main layout
        layout.addWidget(file_group)
        layout.addWidget(encrypt_group)
        layout.addWidget(decrypt_group)
        layout.addWidget(self.status_label)

        self.setLayout(layout)
        self.selected_file = None

    def update_status(self, message, duration=3000):
        self.status_label.setText(message)
        QTimer.singleShot(duration, lambda: self.status_label.setText("Ready"))

    def show_progress_dialog(self, title, label_text):
        progress = QProgressDialog(label_text, None, 0, 0, self)
        progress.setWindowTitle(title)
        progress.setCancelButton(None)
        progress.setWindowModality(Qt.ApplicationModal)
        progress.setMinimumDuration(0)
        progress.show()
        return progress

    def browse_file(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Select File")
        if file_path:
            self.selected_file = file_path
            filename = os.path.basename(file_path)
            file_size = os.path.getsize(file_path)
            size_kb = round(file_size / 1024, 2)
            self.label.setText(f"✅ Selected: {filename} ({size_kb} KB)")
            self.label.setStyleSheet("color: green")
            self.update_status(f"Selected {filename} ({size_kb} KB)")

    def encrypt_file(self):
        if not self.selected_file:
            QMessageBox.warning(self, "Missing File", "Please select a file first.")
            return

        try:
            if not is_valid_file_type(self.selected_file):
                raise ValueError("Invalid file type selected.")

            progress = self.show_progress_dialog("Encrypting", "Encrypting the file securely...")
            key = encrypt_file(self.selected_file)
            progress.close()

            pyperclip.copy(key.decode())
            QMessageBox.information(
                self,
                "Encrypted!",
                f"The file was encrypted successfully.\n\n🔑 KEY (copied to clipboard):\n{key.decode()}"
            )
            self.update_status("Encryption complete!")
        except Exception as e:
            QMessageBox.critical(self, "Encryption Failed", str(e))
            self.update_status("Encryption failed!")

    def decrypt_file(self):
        if not self.selected_file:
            QMessageBox.warning(self, "Missing File", "Please select a file.")
            return

        key = self.key_input.text().strip()
        if not key:
            QMessageBox.warning(self, "Missing Key", "Please enter the decryption key.")
            return

        try:
            progress = self.show_progress_dialog("Decrypting", "Restoring original file...")
            decrypt_file(self.selected_file, key.encode())
            progress.close()

            QMessageBox.information(self, "Decryption Successful", "File decrypted successfully.")
            self.update_status("Decryption complete!")
        except Exception as e:
            QMessageBox.critical(self, "Decryption Failed", str(e))
            self.update_status("Decryption failed!")


def run_app():
    app = QApplication(sys.argv)
    app.setStyleSheet(qdarkstyle.load_stylesheet_pyqt5())
    window = EncryptionApp()
    window.show()
    sys.exit(app.exec_())

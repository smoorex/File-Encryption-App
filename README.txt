# 🔐 File Encryption App — Cybersecurity & Ethical Hacking Project

This project is a Python-based GUI application for encrypting and decrypting files of any type. It was developed as part of the **Cybersecurity and Ethical Hacking** module at Griffith College (BSCH Year 4).

---

## 📌 Features

- 🔒 Encrypts **any file type** in-place (e.g., `.txt`, `.jpg`, `.pdf`, etc.)
- 🔑 Generates a **random encryption key** for each session
- 🧠 Key is shown **once only** after encryption
- 🔓 Requires **user-entered key** to decrypt
- 📁 Simple **file picker** interface
- 🚫 Prevents encryption of unsupported file types
- 📋 Logs encrypted file paths without exposing keys
- 🌙 Stylish dark mode interface using `qdarkstyle`
- 💻 Built-in **status updates** and **progress dialogs**
- 📦 Compiled into a standalone `.exe` (for Windows)

---

## 🛠️ Built With

- Python 3
- PyQt5 – GUI Framework
- Cryptography – Encryption (`Fernet`/AES)
- Pyperclip – Auto-copy encryption key
- QDarkStyle – Dark theme styling
- PyInstaller – Packaged into a `.exe` file for Windows

---

## 🚀 Running the App Locally

### 1. Clone the Repository

```bash
git clone https://github.com/smoorex/File-Encryption-App.git
cd File-Encryption-App

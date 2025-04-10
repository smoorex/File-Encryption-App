from cryptography.fernet import Fernet
import os
import logging

# Set up the log file
LOG_DIR = "logs"
os.makedirs(LOG_DIR, exist_ok=True)
LOG_FILE = os.path.join(LOG_DIR, "encryption.log")

logging.basicConfig(
    filename=LOG_FILE,
    level=logging.INFO,
    format='%(asctime)s - %(message)s'
)

# supported file extensions
VALID_FILE_TYPES = ['.txt', '.pdf', '.docx', '.png', '.jpg', '.jpeg', '.mp3', '.mp4', '.csv', '.xlsx']

def is_valid_file_type(filepath):
    _, ext = os.path.splitext(filepath)
    return ext.lower() in VALID_FILE_TYPES

def generate_key():
    """generates a random encryption key."""
    return Fernet.generate_key()

def encrypt_file(filepath):
    """
    encrypts the given file in-place.
    returns the encryption key if successful.
    """
    if not is_valid_file_type(filepath):
        raise ValueError("Invalid file type selected for encryption.")

    key = generate_key()
    cipher = Fernet(key)

    with open(filepath, 'rb') as file:
        original_data = file.read()

    encrypted_data = cipher.encrypt(original_data)

    with open(filepath, 'wb') as file:
        file.write(encrypted_data)

    log_encryption(filepath)
    return key  # key will be displayed once

def decrypt_file(filepath, key):
    """
    decrypts the given file in-place using the provided key.
    """
    cipher = Fernet(key)

    with open(filepath, 'rb') as file:
        encrypted_data = file.read()

    decrypted_data = cipher.decrypt(encrypted_data)

    with open(filepath, 'wb') as file:
        file.write(decrypted_data)

def log_encryption(filepath):
    """
    logs the encrypted file path and timestamp, the key doesn't get logged .
    """
    logging.info(f"Encrypted file: {filepath}")

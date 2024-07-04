from pathlib import Path
from os import urandom
import base64

from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend

def derive_key(master_password, salt):
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=100000,
        backend=default_backend()
    )
    key = kdf.derive(master_password.encode())
    return key

def decrypt_message(key, encrypted_message):
    encrypted_message_bytes = base64.urlsafe_b64decode(encrypted_message.encode('utf-8'))
    iv = encrypted_message_bytes[:16]
    cipher = Cipher(algorithms.AES(key), modes.CFB(iv), backend=default_backend())
    decryptor = cipher.decryptor()
    decrypted_message = decryptor.update(encrypted_message_bytes[16:]) + decryptor.finalize()
    return decrypted_message.decode('utf-8')

def encrypt_message(key, message):
    iv = urandom(16)
    cipher = Cipher(algorithms.AES(key), modes.CFB(iv), backend=default_backend())
    encryptor = cipher.encryptor()
    encrypted_message = encryptor.update(message.encode()) + encryptor.finalize()
    return base64.urlsafe_b64encode(iv + encrypted_message).decode('utf-8')

def get_credstore_path(filename):
    home = Path.home()
    yacs_dir = home / ".yacs"
    yacs_dir.mkdir(exist_ok=True)  # Create directory if it doesn't exist
    credstore_path = yacs_dir / filename
    return credstore_path
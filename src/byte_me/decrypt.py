import os
import stat
from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad
from byte_me.utils import log_action

def decrypt_files(key: bytes, folder: str = ".byte_me"):
    if not os.path.isdir(folder):
        print(f"Folder '{folder}' not found.")
        return

    for root, _, files in os.walk(folder):
        for name in files:
            path = os.path.join(root, name)
            _decrypt_file(path, key)

def _decrypt_file(path: str, key: bytes):
    CHUNK_SIZE = 10 * 1024
    SIGNATURE = b"BME1"

    with open(path, "rb") as f:
        data = f.read()

    if not data.startswith(SIGNATURE):
        print(f"🟡 Skipping file (no signature): {path}")
        return

    iv = data[4:20]
    encrypted_header = data[20:20 + ((CHUNK_SIZE + AES.block_size - 1) // AES.block_size) * AES.block_size]
    tail = data[20 + len(encrypted_header):]

    try:
        cipher = AES.new(key, AES.MODE_CBC, iv)
        header = unpad(cipher.decrypt(encrypted_header), AES.block_size)
    except Exception as e:
        print(f"❌ Decryption failed for {path}: {str(e)}")
        log_action(f"❌ Decryption failed for {path}: {str(e)}")
        return

    with open(path, "wb") as f:
        f.write(header + tail)

    log_action(f"✅ Decrypted file: {path}")

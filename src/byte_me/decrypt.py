import os
from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad
from byte_me.utils import log_action

def decrypt_files(key: bytes, folder: str = ".byte_me"):
    """
    מפענח את 1–10KB הראשונים של כל קובץ תחת התיקייה folder באמצעות AES-CBC.
    :param key: מפתח AES באורך 32 בתים (256-bit).
    :param folder: תיקיית היעד לפענוח (ברירת מחדל: .byte_me).
    """
    if not os.path.isdir(folder):
        print(f"Folder '{folder}' not found.")
        return

    for root, _, files in os.walk(folder):
        for name in files:
            path = os.path.join(root, name)
            _decrypt_file(path, key)

def _decrypt_file(path: str, key: bytes):
    """
    מפענח את חלקו הראשון (עד 10KB + IV) של הקובץ ב-path עם AES-CBC.
    מניח שהקובץ התחיל ב–IV (16 בתים) ואחריו הנתונים המוצפנים (מושטלים לגודל בלוקים).
    :param path: נתיב הקובץ לפענוח.
    :param key: מפתח AES.
    """
    CHUNK_SIZE = 10 * 1024  # 10KB

    with open(path, "rb") as f:
        data = f.read()

    # קריאה ופרישה של ה-IV, החלק המוצפן והשארית
    iv = data[:16]
    # מחשבים את אורך החלק המוצפן (מעוגל עד לגודל בלוק)
    enc_len = ((CHUNK_SIZE + AES.block_size - 1) // AES.block_size) * AES.block_size
    encrypted_header = data[16:16 + enc_len]
    tail = data[16 + enc_len:]

    # יצירת מופע AES ופענוח + הסרת padding
    cipher = AES.new(key, AES.MODE_CBC, iv)
    try:
        header = unpad(cipher.decrypt(encrypted_header), AES.block_size)
    except ValueError:
        print(f"Decryption failed for {path}: wrong key or corrupted data.")
        return

    # כתיבה מחדש של הקובץ עם החלק המפוענח והשארית
    with open(path, "wb") as f:
        f.write(header + tail)

    log_action(f"Decrypted file: {path}")

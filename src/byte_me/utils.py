import os
import logging
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
from Crypto.Random import get_random_bytes

# הגדרת נתיב לוגים
LOG_DIR  = os.path.join(os.getcwd(), "logs")
LOG_FILE = os.path.join(LOG_DIR, "byte_me.log")

# יצירת תיקיית לוגים אם לא קיימת
if not os.path.isdir(LOG_DIR):
    os.makedirs(LOG_DIR)

# הגדרת logging
logging.basicConfig(
    filename=LOG_FILE,
    level=logging.INFO,
    format="%(asctime)s - %(message)s",
)

def log_action(message: str):
    """
    כותב הודעה ל־byte_me.log עם חותמת זמן.
    """
    logging.info(message)

def generate_aes_key() -> bytes:
    """
    יוצר מפתח AES-256 אקראי.
    """
    return get_random_bytes(32)

def encrypt_key_rsa(
    key: bytes,
    public_key_path: str = os.path.join("keys", "public.pem"),
    output_path: str = "encrypted_key.bin"
):
    """
    מצפין את מפתח ה-AES עם מפתח RSA ציבורי ושומר לקובץ.
    :param key: מפתח AES.
    :param public_key_path: נתיב לקובץ public.pem.
    :param output_path: שם קובץ הפלט למפתח המוצפן.
    """
    # קריאה של המפתח הציבורי
    with open(public_key_path, "rb") as f:
        pub_key = RSA.import_key(f.read())
    cipher = PKCS1_OAEP.new(pub_key)

    # הצפנת המפתח
    enc_key = cipher.encrypt(key)

    # שמירה לקובץ
    with open(output_path, "wb") as f:
        f.write(enc_key)

    log_action(f"AES key encrypted to {output_path}")

def decrypt_key_rsa(
    enc_key_path: str = "encrypted_key.bin",
    private_key_path: str = os.path.join("keys", "private.pem")
) -> bytes:
    """
    מפענח את מפתח ה-AES מתוך קובץ מוצפן בעזרת מפתח RSA פרטי.
    :param enc_key_path: נתיב לקובץ המפתח המוצפן.
    :param private_key_path: נתיב לקובץ private.pem.
    :return: המפתח המפוענח (bytes).
    """
    # קריאה של המפתח הפרטי
    with open(private_key_path, "rb") as f:
        priv_key = RSA.import_key(f.read())
    cipher = PKCS1_OAEP.new(priv_key)

    # קריאה של המפתח המוצפן
    with open(enc_key_path, "rb") as f:
        enc_key = f.read()

    # פענוח
    key = cipher.decrypt(enc_key)
    log_action(f"AES key decrypted from {enc_key_path}")
    return key

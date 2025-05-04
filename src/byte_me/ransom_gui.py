import os

import tkinter as tk
from tkinter import scrolledtext
from byte_me.utils import log_action

def show_ransom_note() -> str:
    """
    מציג חלון Tkinter עם הודעת דרישת כופר ושדה להזנת מפתח.
    מחזיר את המחרוזת שהוזנה על ידי המשתמש.
    """
    # 1. קריאת טקסט דרישת הכופר מקובץ
    note_path = os.path.join("resources", "ransom_note.txt")
    try:
        with open(note_path, "r", encoding="utf-8") as f:
            note = f.read()
    except FileNotFoundError:
        note = "Your files have been encrypted!\nEnter the decryption key below."

    # 2. יצירת חלון ראשי והגדרות בסיסיות
    root = tk.Tk()
    root.title("ByteMe Ransomware Simulator")
    root.geometry("600x400")
    root.resizable(False, False)

    # 3. תיבת טקסט לקריאת ההודעה (readonly)
    text_widget = scrolledtext.ScrolledText(root, wrap=tk.WORD, height=10, width=70)
    text_widget.insert(tk.END, note)
    text_widget.configure(state="disabled")
    text_widget.pack(padx=10, pady=10)

    # 4. תווית ושדה להזנת המפתח
    tk.Label(root, text="Enter decryption key:").pack(padx=10, pady=(5, 0))
    entry = tk.Entry(root, width=70)
    entry.pack(padx=10, pady=(0, 10))
    entry.focus()

    # 5. משתנה לשמירת הקלט
    user_input = {"value": None}

    def on_submit():
        user_input["value"] = entry.get().strip()
        log_action("User entered key in GUI")
        root.destroy()

    # 6. כפתור לשליחה
    tk.Button(root, text="Submit", command=on_submit).pack(pady=(0, 10))

    # 7. הפעלת לולאת ה-GUI (עד ש־root.destroy נקרא)
    root.mainloop()

    # 8. החזרת הקלט (או מחרוזת ריקה אם לא הוזן דבר)
    return user_input["value"] or ""

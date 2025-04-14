import os
import base64
from tkinter import Tk, filedialog, simpledialog, messagebox, Button, Label
from cryptography.fernet import Fernet
import hashlib
import subprocess

# Derive a Fernet key from a password
def password_to_key(password):
    digest = hashlib.sha256(password.encode()).digest()
    return base64.urlsafe_b64encode(digest)

# Encrypt a PDF file
def encrypt_pdf(file_path, password):
    key = password_to_key(password)
    fernet = Fernet(key)

    with open(file_path, 'rb') as file:
        original = file.read()

    encrypted = fernet.encrypt(original)

    output_file = file_path.replace(".pdf", "_encrypted.pdf")
    with open(output_file, 'wb') as enc_file:
        enc_file.write(encrypted)

    messagebox.showinfo("Success", f"File encrypted as:\n{output_file}")

# Decrypt a PDF file
def decrypt_pdf(file_path, password):
    key = password_to_key(password)
    fernet = Fernet(key)

    try:
        with open(file_path, 'rb') as enc_file:
            encrypted = enc_file.read()

        decrypted = fernet.decrypt(encrypted)

        output_file = file_path.replace("_encrypted.pdf", "_decrypted.pdf")
        with open(output_file, 'wb') as dec_file:
            dec_file.write(decrypted)

        messagebox.showinfo("Success", f"Decryption successful!\nOpening {output_file}")
        open_pdf(output_file)

    except Exception as e:
        messagebox.showerror("Decryption Failed", f"Incorrect password or corrupt file.\n{str(e)}")

# Open file using system's default PDF viewer
def open_pdf(path):
    if os.name == 'nt':
        os.startfile(path)
    elif os.name == 'posix':
        subprocess.call(['xdg-open', path])

# GUI logic
def select_encrypt():
    file_path = filedialog.askopenfilename(filetypes=[("PDF Files", "*.pdf")])
    if file_path:
        password = simpledialog.askstring("Password", "Enter password to encrypt:", show="*")
        if password:
            encrypt_pdf(file_path, password)

def select_decrypt():
    file_path = filedialog.askopenfilename(filetypes=[("Encrypted PDF Files", "*.pdf")])
    if file_path:
        password = simpledialog.askstring("Password", "Enter password to decrypt:", show="*")
        if password:
            decrypt_pdf(file_path, password)

# GUI window
def run_gui():
    root = Tk()
    root.title("PDF Encryptor / Decryptor")

    label = Label(root, text="Select an option", font=("Arial", 14))
    label.pack(pady=10)

    Button(root, text="Encrypt PDF", command=select_encrypt, width=20, height=2).pack(pady=10)
    Button(root, text="Decrypt PDF", command=select_decrypt, width=20, height=2).pack(pady=10)

    root.mainloop()

if __name__ == "__main__":
    run_gui()

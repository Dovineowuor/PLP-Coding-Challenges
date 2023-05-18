import tkinter as tk
from tkinter import messagebox
import hashlib
import string
import random
import csv
import os

PASSWORDS_FILE = os.path.expanduser("~/Documents/GitHub/PLP-Coding-Challenges/password.csv")


class PasswordModel:
    def __init__(self):
        self.passwords = []
        self.load_passwords()

    def load_passwords(self):
        if os.path.exists(PASSWORDS_FILE):
            with open(PASSWORDS_FILE, "r", newline="") as file:
                reader = csv.DictReader(file)
                self.passwords = list(reader)

    def save_passwords(self):
        with open(PASSWORDS_FILE, "w", newline="") as file:
            fieldnames = ["ID", "Name", "Hashed Password"]
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(self.passwords)

    def add_password(self, name, password):
        id = self.generate_id()
        hashed_password = hash_password(password)
        self.passwords.append({"ID": id, "Name": name, "Hashed Password": hashed_password})
        self.save_passwords()

    def delete_password(self, id):
        self.passwords = [password for password in self.passwords if password["ID"] != id]
        self.save_passwords()

    def get_all_passwords(self):
        return self.passwords

    def generate_id(self):
        ids = [int(password.get("ID", 0)) for password in self.passwords]
        new_id = max(ids) + 1 if ids else 1
        return str(new_id)


class PasswordView:
    def __init__(self, root):
        self.root = root
        self.root.geometry("720x720")
        self.root.title("Password Generator")

        self.label = tk.Label(root, text="Password Generator")
        self.label.pack()

        self.name_label = tk.Label(root, text="Name:")
        self.name_label.pack()
        self.name_entry = tk.Entry(root)
        self.name_entry.pack()

        self.generate_button = tk.Button(root, text="Generate Password", command=self.generate_password)
        self.generate_button.pack()

        self.password_model = PasswordModel()

        self.menu_bar = tk.Menu(self.root)
        self.menu_bar.add_command(label="View Passwords", command=self.show_passwords)
        self.root.config(menu=self.menu_bar)

        self.root.bind("<Configure>", self.hide_password_window)

    def generate_password(self):
        name = self.name_entry.get().strip()
        if not name:
            messagebox.showerror("Error", "Name cannot be empty.")
            return

        password = generate_password()
        self.password_model.add_password(name, password)
        messagebox.showinfo("Password Generated", f"Generated Password: {password}")

    def show_passwords(self):
        self.display_passwords()
        self.password_window.deiconify()

    def display_passwords(self):
        passwords = self.password_model.get_all_passwords()
        self.password_text.delete("1.0", tk.END)
        for password in passwords[:10]:
            self.password_text.insert(tk.END, f"ID: {password['ID']}\tName: {password['Name']}\tHashed Password: {password['Hashed Password']}\n")
        if len(passwords) > 10:
            self.password_text.insert(tk.END, "\n...More")

    def hide_password_window(self, event):
        self.password_window.withdraw()


def hash_password(password):
    salt = _salt(length=16)
    hashed_password = hashlib.pbkdf2_hmac('sha256', password.encode(), salt, 100000)
    return hashed_password.hex()


def _salt(length=16):
    characters = string.ascii_letters + string.digits + string.punctuation
    salt = ''.join(random.choice(characters) for _ in range(length))
    return salt.encode()


def generate_password(length=12):
    characters = string.ascii_letters + string.digits + string.punctuation
    password = ''.join(random.choice(characters) for _ in range(length))
    return password


def main():
    root = tk.Tk()
    view = PasswordView(root)
    root.mainloop()


if __name__ == "__main__":
    main()


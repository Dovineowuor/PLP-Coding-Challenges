import tkinter as tk
from tkinter import messagebox
import csv
import hashlib
import random
import string
from window import Window


class PasswordModel:
    def __init__(self):
        self.passwords = []
        self.load_passwords()

    def load_passwords(self):
        try:
            with open("passwords.csv", "r") as file:
                reader = csv.DictReader(file)
                self.passwords = list(reader)
        except FileNotFoundError:
            self.passwords = []

    def save_passwords(self):
        with open("passwords.csv", "w", newline="") as file:
            fieldnames = ["ID", "Name", "Hashed Password"]
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(self.passwords)

    def get_all_passwords(self):
        return self.passwords

    def add_password(self, name, password):
        new_id = self.generate_id()
        hashed_password = hash_password(password)
        self.passwords.append({"ID": new_id, "Name": name, "Hashed Password": hashed_password})
        self.save_passwords()

    def delete_password(self, id):
        self.passwords = [password for password in self.passwords if password["ID"] != id]
        self.save_passwords()

    def update_password(self, id, name, password):
        for pwd in self.passwords:
            if pwd["ID"] == id:
                pwd["Name"] = name
                pwd["Hashed Password"] = hash_password(password)
                break
        self.save_passwords()

    def generate_id(self):
        ids = [int(password.get("ID", 0)) for password in self.passwords]
        new_id = max(ids) + 1 if ids else 1
        return str(new_id)


class PasswordView:
    def __init__(self, root):
        self.root = root

        self.label = tk.Label(root.main_frame, text="Password Generator")
        self.label.pack()

        self.name_label = tk.Label(root.main_frame, text="Name:")
        self.name_label.pack()
        self.name_entry = tk.Entry(root.main_frame)
        self.name_entry.pack()

        self.generate_button = tk.Button(root.main_frame, text="Generate Password", command=self.generate_password)
        self.generate_button.pack()

        self.password_label = tk.Label(root.main_frame, text="Generated Password:")
        self.password_label.pack()
        self.password_entry = tk.Entry(root.main_frame, state="readonly")
        self.password_entry.pack()

        self.save_button = tk.Button(root.main_frame, text="Save Password", command=self.save_password)
        self.save_button.pack()

        self.show_passwords_button = tk.Button(root.main_frame, text="Show Passwords", command=self.show_passwords)
        self.show_passwords_button.pack()

        self.password_model = PasswordModel()

    def generate_password(self):
        password = generate_password()
        self.password_entry.configure(state="normal")
        self.password_entry.delete(0, tk.END)
        self.password_entry.insert(0, password)
        self.password_entry.configure(state="readonly")

    def save_password(self):
        name = self.name_entry.get().strip()
        password = self.password_entry.get().strip()
        if name and password:
            self.password_model.add_password(name, password)
            messagebox.showinfo("Success", "Password saved successfully.")
            self.name_entry.delete(0, tk.END)
            self.password_entry.delete(0, tk.END)
        else:
            messagebox.showerror("Error", "Please enter a name and password.")

    def show_passwords(self):
        passwords = self.password_model.get_all_passwords()
        if not passwords:
            messagebox.showinfo("Info", "No passwords saved.")
        else:
            messagebox.showinfo("Info", "\n".join([f"ID: {password['ID']}\tName: {password['Name']}" for password in passwords]))


def hash_password(password):
    salt = _salt()
    return hashlib.pbkdf2_hmac('sha256', password.encode(), salt.encode(), 100000).hex()


def generate_password(length=10):
    characters = string.ascii_letters + string.digits + string.punctuation
    return ''.join(random.choice(characters) for _ in range(length))


def _salt(length=32):
    characters = string.ascii_letters + string.digits + string.punctuation
    return ''.join(random.choice(characters) for _ in range(length))


if __name__ == '__main__':
    window = Window()
    app = PasswordView(window)
    window.run()


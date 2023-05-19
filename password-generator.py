import tkinter as tk
from tkinter import messagebox
import csv
import hashlib
import random
import string
from window import Window
from tkinter import Tk
from side_bar_conditioner import SideBarConditioner


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
        hashed_password = self.hash_password(password)
        self.passwords.append({"ID": new_id, "Name": name, "Hashed Password": hashed_password})
        self.save_passwords()

    def delete_password(self, id):
        self.passwords = [password for password in self.passwords if password["ID"] != id]
        self.save_passwords()

    def update_password(self, id, name, password):
        for pwd in self.passwords:
            if pwd["ID"] == id:
                pwd["Name"] = name
                pwd["Hashed Password"] = self.hash_password(password)
                break
        self.save_passwords()

    def generate_id(self):
        ids = [int(password.get("ID", 0)) for password in self.passwords]
        new_id = max(ids) + 1 if ids else 1
        return str(new_id)

    def hash_password(self, password):
        return hashlib.sha256(password.encode()).hexdigest()


class PasswordView:
    def __init__(self, root, sidebar_conditioner):
        self.root = root
        self.sidebar_conditioner = sidebar_conditioner

        self.label = tk.Label(root.main_frame, text="Password Generator")
        self.label.pack()

        self.name_label = tk.Label(root.main_frame, text="Name:")
        self.name_label.pack()
        self.name_entry = tk.Entry(root.main_frame)
        self.name_entry.pack()

        self.generate_button = tk.Button(root.sidebar_frame, text="Generate New Password", command=self.generate_password)
        self.generate_button.pack(anchor="w", padx=10)

        self.password_label = tk.Label(root.main_frame, text="Generated Password:")
        self.password_label.pack()
        self.password_entry = tk.Entry(root.main_frame, state="readonly")
        self.password_entry.pack()

        self.save_button = tk.Button(root.sidebar_frame, text="Save Password", command=self.save_password)
        self.save_button.pack(anchor="w", padx=10)

        self.show_passwords_button = tk.Button(root.sidebar_frame, text="Show Passwords", command=self.show_passwords)
        self.show_passwords_button.pack(anchor="w", padx=10)

        self.delete_button = tk.Button(root.sidebar_frame, text="Delete Password", command=self.delete_password)
        self.delete_button.pack(anchor="w", padx=10)

        self.update_button = tk.Button(root.sidebar_frame, text="Update Password", command=self.update_password)
        self.update_button.pack(anchor="w", padx=10)

        self.about_button = tk.Button(root.sidebar_frame, text="About", command=self.show_about)
        self.about_button.pack(anchor="w", padx=10)

        self.password_model = PasswordModel()

    def generate_password(self):
        length = 12
        chars = string.ascii_letters + string.digits + string.punctuation
        password = "".join(random.choice(chars) for _ in range(length))
        self.password_entry.config(state="normal")
        self.password_entry.delete(0, tk.END)
        self.password_entry.insert(0, password)
        self.password_entry.config(state="readonly")

    def save_password(self):
        name = self.name_entry.get()
        password = self.password_entry.get()

        if not name or not password:
            messagebox.showerror("Error", "Please enter a name and password.")
            return

        self.password_model.add_password(name, password)
        self.clear_entries()
        messagebox.showinfo("Success", "Password saved successfully.")

    def show_passwords(self):
        passwords = self.password_model.get_all_passwords()
        if not passwords:
            messagebox.showinfo("No Passwords", "No passwords found.")
            return

        password_list = []
        for password in passwords:
            name = password.get("Name", "")
            hashed_password = password.get("Hashed Password", "")
            password_list.append(f"Name: {name}, Hashed Password: {hashed_password}")

        messagebox.showinfo("Passwords", "\n".join(password_list))

    def delete_password(self):
        id = self.get_selected_password_id()
        if not id:
            messagebox.showerror("Error", "Please select a password to delete.")
            return

        if messagebox.askyesno("Confirm Delete", "Are you sure you want to delete this password?"):
            self.password_model.delete_password(id)
            messagebox.showinfo("Success", "Password deleted successfully.")
            self.clear_entries()

    def update_password(self):
        id = self.get_selected_password_id()
        if not id:
            messagebox.showerror("Error", "Please select a password to update.")
            return

        name = self.name_entry.get()
        password = self.password_entry.get()

        if not name or not password:
            messagebox.showerror("Error", "Please enter a name and password.")
            return

        self.password_model.update_password(id, name, password)
        messagebox.showinfo("Success", "Password updated successfully.")
        self.clear_entries()

    def get_selected_password_id(self):
        selection = messagebox.askyesno("Confirm Selection", "Please select a password.")
        if selection:
            passwords = self.password_model.get_all_passwords()
            if passwords:
                selected_password = random.choice(passwords)
                self.name_entry.delete(0, tk.END)
                self.name_entry.insert(0, selected_password.get("Name", ""))
                self.password_entry.delete(0, tk.END)
                self.password_entry.insert(0, selected_password.get("Hashed Password", ""))
                return selected_password.get("ID", "")

        return None

    def clear_entries(self):
        self.name_entry.delete(0, tk.END)
        self.password_entry.config(state="normal")
        self.password_entry.delete(0, tk.END)
        self.password_entry.config(state="readonly")

    def show_about(self):
        about_text = """
        Password Generator v1.0
        Created by Your Name
        
        This application generates random passwords and allows you to save, update, and delete them.
        """
        messagebox.showinfo("About", about_text)


if __name__ == '__main__':
    root = Tk()
    window = Window(root)

    sidebar_conditioner = SideBarConditioner(
        root,
        window.sidebar_frame,
        window.hamburger_button,
        window.generate_button,
        window.save_button,
        window.show_passwords_button,
        window.delete_button,
        window.update_button,
        window.about_button
    )

    view = PasswordView(window, sidebar_conditioner)
    root.mainloop()

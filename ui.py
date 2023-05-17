import tkinter as tk
from tkinter import messagebox
import re
from models import PasswordManager


class PasswordGeneratorUI:
    def __init__(self):
        # Create instance of PasswordManager
        self.password_manager = PasswordManager()

        # Create main window
        self.window = tk.Tk()
        self.window.title("Password Generator App")
        self.window.geometry("400x400")

        # Create widgets
        self.password_length_label = tk.Label(
            self.window, text="Password Length (6-50):"
        )
        self.password_length_entry = tk.Entry(self.window, width=10)
        self.generate_password_button = tk.Button(
            self.window, text="Generate Password", command=self.generate_password
        )
        self.password_label = tk.Label(self.window, text="Generated Password:")
        self.password_entry = tk.Entry(self.window, show="*", width=25)
        self.save_password_button = tk.Button(
            self.window, text="Save Password", command=self.save_password
        )
        self.keywords_label = tk.Label(self.window, text="Keywords:")
        self.keywords_entry = tk.Entry(self.window, width=25)
        self.search_button = tk.Button(
            self.window, text="Search Password", command=self.search_password
        )
        self.delete_button = tk.Button(
            self.window, text="Delete Password", command=self.delete_password
        )
        self.update_button = tk.Button(
            self.window, text="Update Password", command=self.update_password
        )

        # Create layout
        self.password_length_label.pack()
        self.password_length_entry.pack()
        self.generate_password_button.pack()
        self.password_label.pack()
        self.password_entry.pack()
        self.save_password_button.pack()
        self.keywords_label.pack()
        self.keywords_entry.pack()
        self.search_button.pack()
        self.delete_button.pack()
        self.update_button.pack()

        # Start the main event loop
        self.window.mainloop()

    def generate_password(self):
        """Generate a random password based on the password length and display it."""
        password_length = self.password_length_entry.get()

        # Validate password length input
        if not password_length.isnumeric():
            messagebox.showerror("Error", "Password length must be a number.")
            return
        password_length = int(password_length)
        if not 6 <= password_length <= 50:
            messagebox.showerror(
                "Error", "Password length must be between 6 and 50 characters."
            )
            return

        # Generate a random password
        password = self.password_manager.generate_password(password_length)

        # Display the generated password
        self.password_entry.delete(0, tk.END)
        self.password_entry.insert(0, password)

    def password_strength_check(self, password):
        """Check the strength of the password."""
        if len(password) < 8:
            return False
        if not re.search("[a-z]", password):
            return False
        if not re.search("[A-Z]", password):
            return False
        if not re.search("[0-9]", password):
            return False
        if not re.search("[!@#$%^&*(),.?\":{}|<>]", password):
            return False
        return True

    def save_password(self):
        """Save the generated password with the provided keywords."""
        keywords = self.keywords_entry.get()
        password = self.password_entry.get()

        # Validate keywords input
        if not keywords:
            messagebox.showerror("Error", "Keywords cannot be empty.")
            return

	"""
        # Check if the password already exists
        # existing_password =
	In the `save_password()` function, after validating the keywords input, the code checks if the password already exists in the password manager by calling the `search_password()` method of the `PasswordManager` class. If the password already exists, the user is prompted with a message box asking if they want to update the password. If the user selects "Yes", the `update_password()` method is called. If the user selects "No", nothing happens.
	If the password does not already exist, the code checks the strength of the password by calling the `password_strength_check()` function. If the password is strong enough, the password and keywords are saved to the password manager using the `add_password()` method of the `PasswordManager` class. If the password is not strong enough, the user is prompted with a message box informing them that the password is weak and asking if they still want to save it. If the user selects "Yes", the password and keywords are saved to the password manager. If the user selects "No", nothing happens.
	Here's the updated `save_password()` function:
	"""
	def save_password(self):
        	"""Save the generated password with the provided keywords."""
        	keywords = self.keywords_entry.get()
        	password = self.password_entry.get()

	        # Validate keywords input
	        if not keywords:
	            messagebox.showerror("Error", "Keywords cannot be empty.")
	            return

	        # Check if the password already exists
	        existing_password = self.password_manager.search_password(keywords)
	        if existing_password:
	            answer = messagebox.askyesno(
	                "Password Already Exists",
	                "A password already exists for these keywords. Do you want to update it?",
	            )
	            if answer:
                self.update_password()
            return

        # Check the strength of the password
        if not self.password_strength_check(password):
            answer = messagebox.askyesno(
                "Weak Password",
                "The password is weak. Do you still want to save it?",
            )
            if not answer:
                return

        # Add the password to the password manager
        self.password_manager.add_password(keywords, password)

        # Clear the keywords and password entry fields
        self.keywords_entry.delete(0, tk.END)
        self.password_entry.delete(0, tk.END)


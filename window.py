import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import csv
import hashlib
import random
import string
from tkinter import filedialog
import os


class Window:
    def __init__(self, root):
        self.root = root
        self.root.title("Password Generator")
        self.root.geometry("600x400")

        # Set default profile picture
        self.profile_icon = self.get_profile_picture()

        # Create Main Frame
        self.main_frame = ttk.Frame(self.root)
        self.main_frame.pack(side="left", fill="both", expand=True)

        # Create profile frame
        self.profile_frame = ttk.Frame(self.root)
        self.profile_frame.pack(side="top", fill="both", padx=10, pady=10)

        # Create profile icon
        self.profile_label = ttk.Label(self.profile_frame, image=self.profile_icon)
        self.profile_label.pack(side="left")

        # Create profile details frame
        self.profile_details_frame = ttk.Frame(self.profile_frame)
        self.profile_details_frame.pack(side="left", padx=10)

        # Create name label
        self.name_label = ttk.Label(self.profile_details_frame, text="Name:")
        self.name_label.pack()

        # Create name entry
        self.name_entry = ttk.Entry(self.profile_details_frame)
        self.name_entry.pack()

        # Create sidebar frame
        self.sidebar_frame = ttk.Frame(self.root)
        self.sidebar_frame.pack(side="left", fill="y")

        # Create sidebar buttons
        self.sidebar_buttons = []
        sidebar_button_texts = ["Home", "Generate Password", "Save Password", "Show Passwords", "Delete Password",
                                "Update Password", "About"]
        for text in sidebar_button_texts:
            button = ttk.Button(self.sidebar_frame, text=text)
            button.pack(fill="x", padx=10, pady=5)
            self.sidebar_buttons.append(button)

        # Create hamburger button
        self.hamburger_button = ttk.Button(self.profile_details_frame, text="☰")
        self.hamburger_button.pack(side="right")

        # Create content frame
        self.content_frame = ttk.Frame(self.root)
        self.content_frame.pack(side="left", fill="both", expand=True)

        # Create generate button
        self.generate_button = ttk.Button(self.content_frame, text="Generate")
        self.generate_button.pack()

        # Create save button
        self.save_button = ttk.Button(self.content_frame, text="Save")
        self.save_button.pack()

        # Create show passwords button
        self.show_passwords_button = ttk.Button(self.content_frame, text="Show Passwords")
        self.show_passwords_button.pack()

        # Create delete button
        self.delete_button = ttk.Button(self.content_frame, text="Delete")
        self.delete_button.pack()

        # Create update button
        self.update_button = ttk.Button(self.content_frame, text="Update")
        self.update_button.pack()

        # Create about button
        self.about_button = ttk.Button(self.content_frame, text="About")
        self.about_button.pack()

        # Set initial content
        self.set_content("Home")

    def set_content(self, content):
        # TODO: Implement logic to change content based on selected sidebar button
        pass

    def get_profile_picture(self):
        profile_pictures_dir = "profile_pictures"  # Directory where the profile pictures are stored

        try:
            profile_pictures = os.listdir(profile_pictures_dir)
        except FileNotFoundError:
            return None

        if len(profile_pictures) == 0:
            return None

        random_picture = random.choice(profile_pictures)
        picture_path = os.path.join(profile_pictures_dir, random_picture)

        profile_icon = tk.PhotoImage(file=picture_path)
        return profile_icon


if __name__ == "__main__":
    root = tk.Tk()
    window = Window(root)
    root.mainloop()

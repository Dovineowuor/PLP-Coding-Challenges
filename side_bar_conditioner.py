import tkinter as tk


class SideBarConditioner:
    def __init__(self, root, sidebar_frame, hamburger_button, *content_buttons):
        self.root = root
        self.sidebar_frame = sidebar_frame
        self.hamburger_button = hamburger_button
        self.content_buttons = content_buttons

        self.sidebar_width = self.sidebar_frame.winfo_width()
        self.sidebar_hidden = False

        self.hamburger_button.configure(command=self.toggle_sidebar)

        self.root.bind("<Configure>", self.update_sidebar_width)

    def toggle_sidebar(self):
        if self.sidebar_hidden:
            self.sidebar_frame.pack(side="left", fill="y")
            self.sidebar_hidden = False
        else:
            self.sidebar_frame.pack_forget()
            self.sidebar_hidden = True

    def update_sidebar_width(self, event):
        self.sidebar_width = self.sidebar_frame.winfo_width()

        # Adjust the position of the hamburger button based on sidebar width
        if self.sidebar_hidden:
            self.hamburger_button.place(x=0, y=0)
        else:
            self.hamburger_button.place(x=self.sidebar_width, y=0)

        # Adjust the position of content buttons based on sidebar width
        for button in self.content_buttons:
            if self.sidebar_hidden:
                button.place(x=0, y=button.winfo_y())
            else:
                button.place(x=self.sidebar_width, y=button.winfo_y())

import tkinter as tk
import customtkinter as ctk
from PIL import Image, ImageTk
from tkinter.font import Font

class AlgorithmDashboard:
    def __init__(self, root, logout_callback,username):
        self.username = username
        self.root = root
        self.logout_callback = logout_callback
        self.background_image = Image.open("background3.png")
        self.bg_image = ImageTk.PhotoImage(self.background_image.resize((1000, 600)))
        self.canvas = tk.Canvas(self.root, highlightthickness=0)
        self.canvas.pack(fill="both", expand=True)

        self.button_style = {
            "width": 200,
            "height": 150,
            "fg_color": "#F40307",
            "border_width": 0,
            "text_color": "white",
            "font": ("Inter Regular", 20),
            "corner_radius": 0,
            "bg_color": "transparent"
        }

        self.startX = 70
        self.startY = 140
        self.col_spacing = 20 + 200
        self.row_spacing = 20 + 150

    def create_layout(self):
        self.canvas.create_image(0, 0, image=self.bg_image, anchor="nw")
        self.create_buttons()
        self.create_text_labels()

    def create_buttons(self):
        algorithms = [
            "Caesar", "Play Fair", "Rail Fence", "ROT13",
            "Vigenere", "Substitution", "Affine", "RSA"
        ]

        # First row
        ctk.CTkButton(master=self.canvas, text="Ceaser Cipher", command=lambda: self.open_encryption_page(algorithms[0]), **self.button_style).place(
            x=self.startX, y=self.startY)
        ctk.CTkButton(master=self.canvas, text="Play Fair",command=lambda: self.open_encryption_page(algorithms[1]), **self.button_style).place(
            x=self.startX + self.col_spacing, y=self.startY)
        ctk.CTkButton(master=self.canvas, text="Reil Fence",command=lambda:self.open_encryption_page(algorithms[2]), **self.button_style).place(
            x=self.startX + self.col_spacing * 2, y=self.startY)
        ctk.CTkButton(master=self.canvas, text="Rot 13",command=lambda: self.open_encryption_page(algorithms[3]), **self.button_style).place(
            x=self.startX + self.col_spacing * 3, y=self.startY)

        # Second row
        ctk.CTkButton(master=self.canvas, text="Vigenere",command=lambda: self.open_encryption_page(algorithms[4]), **self.button_style).place(
            x=self.startX, y=self.startY + self.row_spacing)
        ctk.CTkButton(master=self.canvas, text="Substitution",command=lambda: self.open_encryption_page(algorithms[5]), **self.button_style).place(
            x=self.startX + self.col_spacing, y=self.startY + self.row_spacing)
        ctk.CTkButton(master=self.canvas, text="Affine",command=lambda: self.open_encryption_page(algorithms[6]), **self.button_style).place(
            x=self.startX + self.col_spacing * 2, y=self.startY + self.row_spacing)
        ctk.CTkButton(master=self.canvas, text="RSA",command=lambda: self.open_encryption_page(algorithms[7]), **self.button_style).place(
            x=self.startX + self.col_spacing * 3, y=self.startY + self.row_spacing)

    def create_text_labels(self):
        label_font = ("Inter Regular", 14)


        self.canvas.create_text(self.startX, self.startY - 20,
                                text=f"Welcome, {self.username}",
                                fill="white", font=label_font, anchor="w")

        self.canvas.create_text(375, self.startY + self.row_spacing + 150 + 40,
                                text="Choose your Algorithm Carefully!",
                                fill="white", font=(*label_font, "bold"), anchor="w")

        self.canvas.create_text(920, 30, text="Log Out",
                                fill="#F40307", font=(*("Inter Regular", 14), "underline"),
                                anchor="w", tags=("logout_link",))
        self.canvas.tag_bind("logout_link", "<Button-1>", self.logout)
        self.canvas.tag_bind("logout_link", "<Enter>", lambda e: self.canvas.config(cursor="hand2"))
        self.canvas.tag_bind("logout_link", "<Leave>", lambda e: self.canvas.config(cursor=""))

    def logout(self, event):
        self.canvas.destroy()
        self.logout_callback()

    def open_encryption_page(self, algorithm):
        saved_geometry = self.root.geometry()  # <-- Add this line
        self.root.withdraw()  # Hide dashboard
        encryption_window = tk.Toplevel(self.root)
        from EncryptionPage import EncryptionPage
        EncryptionPage(encryption_window, algorithm, self, self.logout_callback)

    def recreate_dashboard(self):
        # Clear existing widgets
        for widget in self.root.winfo_children():
            widget.destroy()
        # Rebuild UI components
        self.canvas = tk.Canvas(self.root, highlightthickness=0)
        self.canvas.pack(fill="both", expand=True)
        self.create_layout()
        # Restore saved geometry (position/size)
        if hasattr(self, 'saved_geometry'):
            self.root.geometry(self.saved_geometry)
        # Ensure the window is visible
        self.root.deiconify()

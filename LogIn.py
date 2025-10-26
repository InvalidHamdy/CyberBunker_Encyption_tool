import tkinter as tk
from PIL import Image, ImageTk
from tkinter.font import Font
import customtkinter as ctk
from SignUp import SignUpApp
from ForgotPassword import ForgotPasswordApp
from services.LoginHandler import LoginHandler

class LoginApp:
    def __init__(self):
        self.password_entry = None
        self.root = tk.Tk()
        self.root.title("CyberSecurity")
        self.root.geometry("1000x600")
        self.root.minsize(800, 500)
        self.root.resizable(False, False)
        self.BASE_WIDTH = 1000
        self.BASE_HEIGHT = 600
        self.elements = {}

        # Initialize images
        self.original_image = Image.open("Frame 1.png")
        self.logo_image = Image.open("logo.png")

        # Setup canvas
        self.canvas = tk.Canvas(self.root, highlightthickness=0)
        self.canvas.pack(fill="both", expand=True)

        # Configure appearance
        ctk.set_appearance_mode("System")
        ctk.set_default_color_theme("blue")

        # Bind resize event
        self.canvas.bind("<Configure>", self.on_resize)

    @staticmethod
    def on_entry_click(event, entry, default_text):
        if entry.get() == default_text:
            entry.delete(0, tk.END)
            entry.config(show="*" if default_text == "Password" else "")

    @staticmethod
    def on_focusout(event, entry, default_text):
        if not entry.get():
            entry.insert(0, default_text)
            entry.config(show="" if default_text == "admin" else "")

    def create_layout(self, width, height):
        scale_x = width / self.BASE_WIDTH
        scale_y = height / self.BASE_HEIGHT
        scale = min(scale_x, scale_y)

        # Clear previous elements
        for item in self.elements.values():
            self.canvas.delete(item)
        self.elements.clear()

        # Background
        resized_bg = self.original_image.resize((width, height), Image.Resampling.LANCZOS)
        self.bg_tk = ImageTk.PhotoImage(resized_bg)
        self.elements['bg'] = self.canvas.create_image(0, 0, anchor="nw", image=self.bg_tk)

        try:
            # Logo
            logo_width = int(280 * scale)
            logo_height = int(280 * scale)
            logo_x = width // 2
            logo_y = int(64 * scale) + 87

            logo_img = self.logo_image.resize((logo_width, logo_height), Image.Resampling.LANCZOS)
            self.logo_tk = ImageTk.PhotoImage(logo_img)
            self.elements['logo'] = self.canvas.create_image(logo_x, logo_y, image=self.logo_tk)

            # Title text
            text_y = int(230 * scale)
            title_font = Font(family="Inter Bold", size=36)

            cyber_width = title_font.measure("Cyber ")
            bunker_width = title_font.measure("Bunker")
            start_x = (width - (cyber_width + bunker_width)) // 2

            self.elements['cyber'] = self.canvas.create_text(
                start_x + cyber_width // 2, text_y,
                text="Cyber", fill="#F40303", font=title_font, anchor="center"
            )
            self.elements['bunker'] = self.canvas.create_text(
                start_x + cyber_width + bunker_width // 2, text_y,
                text="Bunker", fill="white", font=title_font, anchor="center"
            )

            # Form elements
            button_font = Font(family="Inter Bold", size=20)
            entry_width = int(325 * scale)
            entry_height = int(35 * scale)

            # Username
            self.username_entry = tk.Entry(self.root, font=button_font)
            self.username_entry.insert(0, "admin")
            self.username_entry.bind('<FocusIn>', lambda e: self.on_entry_click(e, self.username_entry, "admin"))
            self.username_entry.bind('<FocusOut>', lambda e: self.on_focusout(e, self.username_entry, "admin"))
            self.elements['username'] = self.canvas.create_window(
                width // 2, int(286 * scale),
                window=self.username_entry, anchor="center",
                width=entry_width, height=entry_height
            )

            # Password
            self.password_entry = tk.Entry(self.root, font=button_font)
            self.password_entry.insert(0, "Password")
            self.password_entry.bind('<FocusIn>', lambda e: self.on_entry_click(e, self.password_entry, "Password"))
            self.password_entry.bind('<FocusOut>', lambda e: self.on_focusout(e, self.password_entry, "Password"))
            self.elements['password'] = self.canvas.create_window(
                width // 2, int(341 * scale),
                window=self.password_entry, anchor="center",
                width=entry_width, height=entry_height
            )

            # Sign In Button
            signin_btn = tk.Button(
                self.root, text="Sign In", font=button_font,
                bg="#098dca", fg="white", relief="flat", command=self.attempt_login
            )
            self.elements['signin'] = self.canvas.create_window(
                width // 2, int(396 * scale),
                window=signin_btn, anchor="center",
                width=int(109 * scale), height=int(35 * scale)
            )

            # Additional text elements
            castfont = ("Inter Regular", 12)
            self.elements['forgot'] = self.canvas.create_text(
                width // 2, int(450 * scale),
                text="Forgot Password", font=castfont,
                fill="red", anchor="center", tags=("forgot_link",)
            )

            # Sign Up text
            text_part1 = "Don't have an account? "
            text_part2 = "Sign Up"
            part1_width = Font(family="Inter Regular", size=12).measure(text_part1)
            start_x = (width - (part1_width + Font().measure(text_part2))) // 2

            self.elements['acc_text1'] = self.canvas.create_text(
                start_x + part1_width // 2, int(486 * scale),
                text=text_part1, font=castfont,
                fill="white", anchor="center"
            )
            self.elements['acc_text2'] = self.canvas.create_text(
                start_x + part1_width + Font().measure(text_part2) // 2, int(486 * scale),
                text=text_part2, font=castfont,
                fill="#008FCE", anchor="center",
                tags=("signup_link",)
            )

            # Add click bindings
            self.canvas.tag_bind("signup_link", "<Button-1>", self.show_signup)
            self.canvas.tag_bind("forgot_link", "<Button-1>", self.show_forgot_password)
        except Exception as e:
            print(f"Layout error: {e}")
    def attempt_login(self):
        email = self.username_entry.get()
        password = self.password_entry.get()

        with LoginHandler() as handler:
            if handler.validate_user(email, password):
                self.root.resizable(False, False)
                self.canvas.destroy()
                from AlgorithmDashBoard import AlgorithmDashboard
                username = handler.getUserName(email)
                dashboard = AlgorithmDashboard(self.root, self.recreate_login_layout,username)
                dashboard.create_layout()
            else:
                self.canvas.create_text(1000 // 2, 523,
                                        text="**Invalid Credential**", font=("Inter Regular", 12),
                                        fill="red", anchor="center")

    def show_forgot_password(self, event):
        self.canvas.destroy()
        ForgotPasswordApp(self.root, self.recreate_login_layout)

    def recreate_login_layout(self):
        for widget in self.root.winfo_children():
            widget.destroy()

        self.root.resizable(False, False)
        self.canvas = tk.Canvas(self.root, highlightthickness=0)
        self.canvas.pack(fill="both", expand=True)
        self.create_layout(self.BASE_WIDTH, self.BASE_HEIGHT)
        self.canvas.bind("<Configure>", self.on_resize)

    def show_signup(self, event):
        self.canvas.destroy()
        SignUpApp(self.root, self.recreate_login_layout).show_signup()

    def on_resize(self, event):
        self.create_layout(event.width, event.height)

    def show_login(self):
        self.create_layout(self.BASE_WIDTH, self.BASE_HEIGHT)
        self.root.mainloop()
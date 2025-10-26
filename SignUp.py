import tkinter as tk
import customtkinter as ctk
from PIL import Image, ImageTk
from tkinter.font import Font
import webbrowser
from services.SignUpHandler import  SignUpHandler
import services.OTP_Sender
import services.OTP_Gen
class SignUpApp:
    def __init__(self, root, back_callback):
        self.root = root
        self.back_callback = back_callback
        self.root.title("CyberSecurity - Sign Up")
        self.root.geometry("1000x600")
        self.root.resizable(False, False)
        self.signup_handler = SignUpHandler()
        self.email_entry = None
        self.password_entry = None
        self.confirm_password_entry = None
        self.first_name_entry = None
        self.last_name_entry = None
        self.otp_entry = None

        # Configure CustomTkinter
        ctk.set_appearance_mode("system")
        ctk.set_default_color_theme("blue")

        # Load images
        self.background_image = Image.open("Frame 1.png")
        self.bg_image = ImageTk.PhotoImage(self.background_image.resize((1000, 600)))

        # Create canvas
        self.canvas = tk.Canvas(self.root, highlightthickness=0)
        self.canvas.pack(fill="both", expand=True)

        # Style configurations (preserve original values)
        self.entry_style = {
            "width": 200,
            "height": 35,
            "border_width": 0,
            "corner_radius": 8,
            "fg_color": "white",
            "border_color": "#CCCCCC",
            "text_color": "black",
            "font": ("Inter Regular", 20)
        }

        self.button_style = {
            "width": 90,
            "height": 35,
            "fg_color": "#008FCE",
            "border_width": 0,
            "text_color": "white",
            "font": ("Inter Regular", 20),
            "corner_radius": 0,
            "bg_color": "transparent"
        }

        # Positions configuration (original values)
        self.start_x = 280
        self.start_y = 150
        self.col_spacing = 49 + 200
        self.row_spacing = 55 + 35
        self.textGap = 15

    def create_layout(self):
        # Background image
        self.canvas.create_image(0, 0, image=self.bg_image, anchor="nw")

        # Title text
        self.canvas.create_text(500, 70, text="Sign Up",
                                font=("Inter Bold", 30), fill="white")

        # First Column Elements
        self._create_first_column()
        # Second Column Elements
        self._create_second_column()
        # OTP Field
        self._create_otp_field()
        # Buttons
        self._create_buttons()
        # Terms of Service
        self._create_terms_text()
        # Exit text
        self.canvas.create_text(920, 30, text="Exit",
                                fill="#F40307", font=(*("Inter Regular", 14), "underline"),
                                anchor="w")
        self.canvas.create_text(20, 30, text="Back",
                                fill="white", font=(*("Inter Regular", 14), "underline"),
                                anchor="w", tags=("back_link",))
        self.canvas.tag_bind("back_link", "<Button-1>", self.go_back)
        self.canvas.tag_bind("back_link", "<Enter>", lambda e: self.canvas.config(cursor="hand2"))
        self.canvas.tag_bind("back_link", "<Leave>", lambda e: self.canvas.config(cursor=""))
    def _create_first_column(self):
        # First Name
        self.canvas.create_text(self.start_x, self.start_y - self.textGap,
                                text="First Name", fill="white",
                                font=("Inter Regular", 14), anchor="w")
        self.first_name_entry = ctk.CTkEntry(master=self.canvas, **self.entry_style)
        self.first_name_entry .place(x=self.start_x, y=self.start_y)

        # Email
        self.canvas.create_text(self.start_x, self.start_y + self.row_spacing - self.textGap,
                                text="Email", fill="white",
                                font=("Inter Regular", 14), anchor="w")
        self.email_entry = ctk.CTkEntry(master=self.canvas, **self.entry_style)
        self.email_entry.place(x=self.start_x, y=self.start_y + self.row_spacing)

        # Password
        self.canvas.create_text(self.start_x, self.start_y + self.row_spacing * 2 - self.textGap,
                                text="Password", fill="white",
                                font=("Inter Regular", 14), anchor="w")
        self.password_entry = ctk.CTkEntry(master=self.canvas,show="•", **self.entry_style)
        self.password_entry.place(x=self.start_x, y=self.start_y + self.row_spacing * 2)

    def _create_second_column(self):
        # Last Name
        self.canvas.create_text(self.start_x + self.col_spacing, self.start_y - self.textGap,
                                text="Last Name", fill="white",
                                font=("Inter Regular", 14), anchor="w")
        self.last_name_entry = ctk.CTkEntry(master=self.canvas, **self.entry_style)
        self.last_name_entry.place(x=self.start_x + self.col_spacing, y=self.start_y)

        # Username
        self.canvas.create_text(self.start_x + self.col_spacing, self.start_y + self.row_spacing - self.textGap,
                                text="Username", fill="white",
                                font=("Inter Regular", 14), anchor="w")
        self.username_entry = ctk.CTkEntry(master=self.canvas,  **self.entry_style)
        self.username_entry.place(x=self.start_x + self.col_spacing, y=self.start_y + self.row_spacing)

        # Confirm Password
        self.canvas.create_text(self.start_x + self.col_spacing, self.start_y + self.row_spacing * 2 - self.textGap,
                                text="Confirm Password", fill="white",
                                font=("Inter Regular", 14), anchor="w")
        self.confirm_password_entry = ctk.CTkEntry(master=self.canvas, show="•", **self.entry_style)
        self.confirm_password_entry.place(x=self.start_x + self.col_spacing, y=self.start_y + self.row_spacing * 2)

    def _create_otp_field(self):
        self.canvas.create_text(self.start_x, self.start_y + self.row_spacing * 3 - self.textGap,
                                text="OTP", fill="white",
                                font=("Inter Regular", 14), anchor="w")
        self.otp_entry = ctk.CTkEntry(master=self.canvas, **self.entry_style)
        self.otp_entry.place(x=self.start_x, y=self.start_y + self.row_spacing * 3)

    def _create_buttons(self):
        send_otp_btn = ctk.CTkButton(master=self.canvas, text="Send OTP", command=self.send_otp, **self.button_style)
        signup_btn = ctk.CTkButton(master=self.canvas, text="Sign Up", command=self.sign_up, **self.button_style)

        send_otp_btn.place(x=self.start_x + self.col_spacing, y=self.start_y + self.row_spacing * 3)
        signup_btn.place(x=self.start_x + self.col_spacing + 90 + 20,
                         y=self.start_y + self.row_spacing * 3)

    def _create_terms_text(self):
        text_y = 550
        text_part1 = "By creating an account, you agree to the "
        terms_text = "Terms Of Service"
        centerGap = 65

        # First text segment
        self.canvas.create_text(self.start_x + centerGap, text_y,
                                anchor="nw", text=text_part1,
                                fill="white", font=("Inter Regular", 10))

        # Clickable Terms text
        regular_font = Font(family="Inter Regular", size=10)
        terms_link = self.canvas.create_text(
            self.start_x + centerGap + regular_font.measure(text_part1), text_y,
            anchor="nw", text=terms_text,
            fill="#008FCE", font=(*("Inter Regular", 10), "underline"),
            tags="terms_link"
        )

        # Bind events
        self.canvas.tag_bind("terms_link", "<Button-1>", self.open_terms)
        self.canvas.tag_bind("terms_link", "<Enter>", lambda e: self.canvas.config(cursor="hand2"))
        self.canvas.tag_bind("terms_link", "<Leave>", lambda e: self.canvas.config(cursor=""))

        # Hover effects
        self.canvas.tag_bind("terms_link", "<Enter>",
                             lambda e: self.canvas.itemconfig(terms_link, fill="#006699"))
        self.canvas.tag_bind("terms_link", "<Leave>",
                             lambda e: self.canvas.itemconfig(terms_link, fill="#008FCE"))

    def send_otp(self):
        email = self.email_entry.get()
        if not email:
            self.canvas.create_text(self.start_x, self.start_y + self.row_spacing + 50,
                                    text="**Make sure to enter an Email", font=("Inter Regular", 12),
                                    fill="red", anchor="center")
            return
        if self.signup_handler.email_exists(email):
            self.canvas.create_text(self.start_x, self.start_y + self.row_spacing + 50,
                                    text="**Try another Email", font=("Inter Regular", 12),
                                    fill="red", anchor="center")
            return
        self.signup_handler.otp_sender.send_otp_email(email)

    def sign_up(self):
        from services.ForgotPasswordHandler import ForgotPasswordHandler as FHP
        if not FHP.validate_password_constraints(self.password_entry.get(),self.confirm_password_entry.get()):
            self.canvas.create_text(self.start_x + self.col_spacing, self.start_y + self.row_spacing * 4,
                                    text="Password must be at least 8 characters long", font=("Inter Regular", 12),
                                    fill="red", anchor="center")
            self.canvas.create_text(self.start_x + self.col_spacing, self.start_y + self.row_spacing * 4+20,
                                    text="and include at least 1 digit and 1 special character (e.g., !@#$%^&*).and include at least 1 digit and 1 special character.",
                                    font=("Inter Regular", 12),
                                    fill="red", anchor="center")
            return
        data = {
            'first_name': self.first_name_entry.get(),
            'last_name': self.last_name_entry.get(),
            'username':self.username_entry.get(),
            'email': self.email_entry.get(),
            'password': self.password_entry.get(),
            'confirm_password': self.confirm_password_entry.get(),
            'otp': self.otp_entry.get()
        }

        success, message = self.signup_handler.process_signup(**data)
        if success:
            self.canvas.create_text(self.start_x + self.col_spacing, self.start_y + self.row_spacing * 4 + 40,
                                    text="**Regrestiration Failed.",
                                    font=("Inter Regular", 12),
                                    fill="red", anchor="center")
            self.go_back(None)
        else:
            print(f"Error: {message}")
    def open_terms(self, event):
        webbrowser.open("https://example.com/terms")

    def show_signup(self):
        self.create_layout()
    def go_back(self, event):
        self.canvas.destroy()
        self.back_callback()

# Usage example
if __name__ == "__main__":
    app = SignUpApp()
    app.show_signup()
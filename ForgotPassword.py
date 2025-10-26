import tkinter as tk
import customtkinter as ctk
from PIL import Image, ImageTk
from tkinter.font import Font
import webbrowser
from services.ForgotPasswordHandler import ForgotPasswordHandler
from services.SignUpHandler import SignUpHandler
class ForgotPasswordApp:
    def __init__(self, root, back_callback):
        self.root = root
        self.back_callback = back_callback
        self.root.title("CyberSecurity - Forgot Password")
        self.root.geometry("1000x600")
        self.root.resizable(False, False)
        self.ForgotPasswordHandler = ForgotPasswordHandler()
        # Load background image
        self.background_image = Image.open("Frame 1.png")
        self.bg_image = ImageTk.PhotoImage(self.background_image.resize((1000, 600)))

        # Create canvas
        self.canvas = tk.Canvas(self.root, highlightthickness=0)
        self.canvas.pack(fill="both", expand=True)
        self.canvas.create_image(0, 0, image=self.bg_image, anchor="nw")

        # Style configurations (preserve original values)
        self.entry_style = {
            "width": 325,
            "height": 35,
            "border_width": 0,
            "corner_radius": 0,
            "fg_color": "white",
            "border_color": "#CCCCCC",
            "text_color": "black",
            "font": ("Inter Regular", 20)
        }

        self.otp_style = {
            "width": 162,
            "height": 35,
            "border_width": 0,
            "corner_radius": 0,
            "fg_color": "white",
            "border_color": "#CCCCCC",
            "text_color": "black",
            "font": ("Inter Regular", 20)
        }

        self.button_style = {
            "width": 150,
            "height": 35,
            "fg_color": "#008FCE",
            "border_width": 0,
            "text_color": "white",
            "font": ("Inter Regular", 20),
            "corner_radius": 0,
            "bg_color": "transparent"
        }

        # Position configurations (original values)
        self.startX = 336
        self.startY = 135
        self.textGap = 15
        self.col_spacing = 173  # 13 + 160
        self.row_spacing = 75   # 40 + 35

        # Create all UI elements
        self.create_widgets()
        self.bind_events()

    def create_widgets(self):
        # Email Field
        self.canvas.create_text(self.startX, self.startY-self.textGap,
                              text="Email", fill="white",
                              font=("Inter Regular", 14), anchor="w")
        self.email_entry = ctk.CTkEntry(master=self.canvas, **self.entry_style)
        self.email_entry.place(x=self.startX, y=self.startY)

        # OTP Field
        self.canvas.create_text(self.startX, self.startY+self.row_spacing-self.textGap,
                              text="OTP", fill="white",
                              font=("Inter Regular", 14), anchor="w")
        self.otp_entry = ctk.CTkEntry(master=self.canvas, **self.otp_style)
        self.otp_entry.place(x=self.startX, y=self.startY+self.row_spacing)

        # Send OTP Button
        self.send_otp_btn = ctk.CTkButton(master=self.canvas,
                                        text="Send OTP", **self.button_style,command=self.sendOtp)
        self.send_otp_btn.place(x=self.startX+self.col_spacing,
                              y=self.startY+self.row_spacing)

        # New Password Field
        self.canvas.create_text(self.startX, self.startY+self.row_spacing*2-self.textGap,
                              text="New Password", fill="white",
                              font=("Inter Regular", 14), anchor="w")
        self.password_entry = ctk.CTkEntry(master=self.canvas, show="•",**self.entry_style)
        self.password_entry.place(x=self.startX, y=self.startY+self.row_spacing*2)

        # Confirm Password Field
        self.canvas.create_text(self.startX, self.startY+self.row_spacing*3-self.textGap,
                              text="Confirm Password", fill="#FF0000",
                              font=("Inter Regular", 14), anchor="w")
        self.confirm_password_entry = ctk.CTkEntry(master=self.canvas, show="•",**self.entry_style)
        self.confirm_password_entry.place(x=self.startX, y=self.startY+self.row_spacing*3)

        # Confirm Button
        self.confirm_btn = ctk.CTkButton(master=self.canvas,
                                       text="Confirm",
                                         command=self.hande_passwordUpdate,
                                         **self.button_style)
        self.confirm_btn.place(x=self.startX+89, y=self.startY+self.row_spacing*4)

        # Back Link
        self.canvas.create_text(20, 30, text="Back",
                              fill="white", font=(*("Inter Regular", 14), "underline"),
                              anchor="w", tags=("back_link",))
    def hande_passwordUpdate(self):
        if not self.ForgotPasswordHandler.validate_password_constraints(self.password_entry.get()):
            self.canvas.create_text(1000//2,  self.startY+self.row_spacing*5, text="Password must be at least 8 characters long", font=("Inter Regular", 12),fill="red", anchor="center")
            self.canvas.create_text(1000 // 2, self.startY + self.row_spacing * 5+20,
                                    text="and include at least 1 digit and 1 special character (e.g., !@#$%^&*).and include at least 1 digit and 1 special character.", font=("Inter Regular", 12),
                                    fill="red", anchor="center")
            return
        if not self.ForgotPasswordHandler.validateMatchingPassword(self.password_entry.get(), self.confirm_password_entry.get()):
            self.canvas.create_text(1000//2, self.startY+self.row_spacing*5, text="Password Does not Match", font=("Inter Regular", 12),fill="red", anchor="center")
            return
        isUpdated = self.ForgotPasswordHandler.updatePassword(
            self.otp_entry.get(),
            self.email_entry.get(),
            self.password_entry.get(),
            self.confirm_password_entry.get(),
         )
        if isUpdated:
            self.canvas.create_text( 1000//2, self.startY+self.row_spacing*5 ,text="Password Updated", font=("Inter Regular", 12),
                                        fill="#008FCE", anchor="center")

    def sendOtp(self):
        email = self.email_entry.get()
        if not email:
            self.canvas.create_text(self.startX, self.startY+10,text="Please enter VALID email first", font=("Inter Regular", 12),fill="red", anchor="center")
            return
        signup_handler = SignUpHandler()
        if not signup_handler.email_exists(email):
            self.canvas.create_text(self.startX, self.startY+10,text="Please enter VALID email first", font=("Inter Regular", 12),fill="red", anchor="center")
            return
        isSent =self.ForgotPasswordHandler.otp_sender.send_otp_email(email)
        if isSent:
            self.canvas.create_text(self.startX+self.col_spacing+25, self.startY+self.row_spacing+45,text="OTP sent", font=("Inter Regular", 12),fill="#008FCE", anchor="center")
    def bind_events(self):
        self.canvas.tag_bind("back_link", "<Button-1>", self.go_back)
        self.canvas.tag_bind("back_link", "<Enter>", lambda e: self.canvas.config(cursor="hand2"))
        self.canvas.tag_bind("back_link", "<Leave>", lambda e: self.canvas.config(cursor=""))

    def go_back(self, event):
        self.canvas.destroy()
        self.back_callback()
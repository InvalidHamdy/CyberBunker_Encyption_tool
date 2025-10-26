from tkinter import messagebox, filedialog

import CeaserCipher
import tkinter as tk
from PIL import Image, ImageTk
from tkinter.font import Font
from algorithms.CeaserCipher import CaesarCipher
from algorithms.PlayFairCipher import PlayfairCipher
from algorithms.Vagenere import VigenereCipher
from algorithms.RailFenceCipher import RailFenceCipher
from algorithms.ROT13 import ROT13 as ROT13Cipher
from algorithms.AFFINE import AffineCipher
from algorithms.RSACipher import RSACipher
from algorithms.Substitution import Substitiotion

class EncryptionPage:
    def __init__(self, root, algorithm, dashboard_instance, logout_callback):
        self.root = root
        self.root.title("CyberSecurity")
        self.root.geometry("1000x600")
        self.algorithm = algorithm
        self.current_filepath = None
        self.dashboard_instance = dashboard_instance
        self.logout_callback = logout_callback
        self.setup_canvas()
        self.load_background()
        self.create_fonts()
        self.create_interface_elements()
        self.setup_bindings()
        self.logout_callback = logout_callback
        self.RSA_cipher = RSACipher()
    def setup_canvas(self):
        self.canvas = tk.Canvas(self.root, highlightthickness=0)
        self.canvas.pack(fill="both", expand=True)
        self.root.update_idletasks()  # Force window dimension calculation

    def load_background(self):
        self.original_image = Image.open("background3.png")
        initial_width = self.canvas.winfo_width()
        initial_height = self.canvas.winfo_height()
        resized_image = self.original_image.resize((initial_width, initial_height), Image.Resampling.LANCZOS)
        self.image_tk = ImageTk.PhotoImage(resized_image)
        self.image_item = self.canvas.create_image(0, 0, anchor="nw", image=self.image_tk)

    def create_fonts(self):
        self.button_font = Font(family="Inter Bold", size=20)

    def create_interface_elements(self):
        # Text labels
        self.canvas.create_text(20, 30, text="Back", fill="white",
                                font=(*("Inter Regular", 14), "underline"), anchor="w",tags=("back_link",))
        self.canvas.tag_bind("back_link", "<Button-1>", self.go_back)
        self.canvas.create_text(950, 30, text="Exit", fill="#F40307",
                                font=(*("Inter Regular", 14), "underline"), anchor="w",tags=("logout_link",))
        self.canvas.tag_bind("logout_link", "<Button-1>", self.logout)
        self.canvas.tag_bind("logout_link", "<Enter>", lambda e: self.canvas.config(cursor="hand2"))
        self.canvas.tag_bind("logout_link", "<Leave>", lambda e: self.canvas.config(cursor=""))

        # Entry fields
        self.entry1 = tk.Entry(self.root, font=self.button_font)
        self.entry2 = tk.Entry(self.root, font=self.button_font)
        self.entry3 = tk.Entry(self.root, font=self.button_font)
        if self.algorithm == "RSA":
            self.entry4 = tk.Entry(self.root, font=self.button_font)
            self.canvas.create_window(202, 382, window=self.entry4, anchor="nw", width=324, height=35)

        # Entry placements
        self.canvas.create_window(202, 232, window=self.entry1, anchor="nw", width=324, height=35)
        self.canvas.create_window(202, 282, window=self.entry2, anchor="nw", width=324, height=35)
        self.canvas.create_window(202, 332, window=self.entry3, anchor="nw", width=324, height=35)
        if self.algorithm == "ROT13":
            self.entry3.insert(0, "13")
            self.entry3.configure(state="disabled")

        self.canvas.create_text(500 ,150,text=self.algorithm,
                                    font=("Inter bold", 32),
                                    fill="red", anchor="center" )



        # Text labels
        text_height = self.button_font.metrics("ascent") + self.button_font.metrics("descent")
        y_start, gap = 235, 21
        if self.algorithm == "RSA":
            y_positions = [y_start, y_start + text_height + gap, y_start + 2 * (text_height + gap),y_start + 3* (text_height + gap)]
        else :
            y_positions = [y_start, y_start + text_height + gap, y_start + 2 * (text_height + gap)]

        if self.algorithm == "RSA":
            labels = ["Plain Text", "Cipher Text", "Public Key","Private Key"]
        else:
            labels = ["Plain Text", "Cipher Text", "Key"]

        for i, (y, text) in enumerate(zip(y_positions, labels)):
            self.canvas.create_text(47, y, anchor="nw", text=text,
                                    font=self.button_font, fill="white")

        # Buttons
        self.create_button(584, 232, 'Upload', self.on_upload_click)
        self.create_button(584, 282, 'Encrypt', self.on_encrypt_click)
        self.create_button(584, 332, 'Decrypt', self.on_decrypt_click)
        if self.algorithm == "RSA":
            self.create_button(584,382,"Genereate Keys",self.forRsa)

    def create_button(self, x, y, text, command):
        tag = f"button_{text}"
        rect = self.canvas.create_rectangle(x, y, x + 324, y + 35, fill='#F40303', outline='')
        text_id = self.canvas.create_text(x + 162, y + 17.5, text=text, anchor='center',
                                          fill='white', font=self.button_font)
        self.canvas.addtag_withtag(tag, rect)
        self.canvas.addtag_withtag(tag, text_id)
        self.canvas.tag_bind(tag, '<Button-1>', command)

    def setup_bindings(self):
        self.canvas.bind("<Configure>", self.resize_image)
    def forRsa(self,event):
        self.publicKey,self.privateKey = self.RSA_cipher.generate_rsa_keys()
        self.entry3.delete(0, "end")
        self.entry3.insert(0, f"{self.publicKey}")
        self.entry4.delete(0, "end")
        self.entry4.insert(0, f"{self.privateKey}")


    def resize_image(self, event):
        new_width = self.canvas.winfo_width()
        new_height = self.canvas.winfo_height()
        resized_img = self.original_image.resize((new_width, new_height), Image.Resampling.LANCZOS)
        self.image_tk = ImageTk.PhotoImage(resized_img)
        self.canvas.itemconfig(self.image_item, image=self.image_tk)
        self.canvas.image = self.image_tk

    # Event handlers
    def on_upload_click(self, event):
        filepath = filedialog.askopenfilename(filetypes=[("Text files", "*.txt")])
        if not filepath:
            self.canvas.create_text(1000//2,235 + 3* ( self.button_font.metrics("ascent") + self.button_font.metrics("descent")+ 21)+20,text="Choose Vaild FIle and Try again", font=("Inter Regular", 12),fill="red", anchor="center")
            return

        try:
            with open(filepath, 'r') as file:
                content = file.read()
                self.entry1.delete(0, tk.END)
                self.entry1.insert(0, content)
                self.current_filepath = filepath
                self.canvas.create_text(1000//2,235 + 3* ( self.button_font.metrics("ascent") + self.button_font.metrics("descent")+ 21)+50,text="File is loaded", font=("Inter Regular", 12),fill="#008FCE", anchor="center")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to read file:\n{str(e)}")
        print("Upload button clicked")


    def on_encrypt_click(self, event):
        text = self.entry1.get()
        key = self.entry3.get()

        try:
            if self.algorithm == "Caesar":
                cipher = CaesarCipher(int(key))
                result = cipher.encrypt(text)

            elif self.algorithm == "Vigenere":
                vigenere_cipher = VigenereCipher(key)
                result = vigenere_cipher.encrypt(text)

            elif self.algorithm == "Rail Fence":
                rail_fence_cipher = RailFenceCipher()
                result = rail_fence_cipher.encrypt(text,int(key))

            elif self.algorithm == "ROT13":

                rot_cipher = ROT13Cipher()
                result = rot_cipher.encrypt(text)

            elif self.algorithm == "Affine":
                a, b = map(int, key.split(','))
                affine_cipher = AffineCipher(a, b)
                result = affine_cipher.encrypt(text)

            elif self.algorithm == "Play Fair":
                playfair_cipher = PlayfairCipher(key)
                result = playfair_cipher.encrypt(text)

            elif self.algorithm == "RSA":
                 result = self.RSA_cipher.rsa_encrypt(text,self.publicKey)
            elif self.algorithm == "Substitution":
                substitution_cipher = Substitiotion(key)
                result = substitution_cipher.encrypt(text)

            # Add other algorithms similarly
            self.entry2.delete(0, tk.END)
            self.entry2.insert(0, result)
        except Exception as e:
            print("Error:", e)
        else:
            if self.current_filepath:
                try:
                    with open(self.current_filepath, 'w') as file:
                        file.write(result)
                        self.canvas.create_text(1000 // 2, 235 + 3 * (
                                self.button_font.metrics("ascent") + self.button_font.metrics("descent") + 21) + 80,
                                                text="File is OverWritten!", font=("Inter Regular", 12), fill="#008FCE",
                                                anchor="center")
                except Exception as e:
                    messagebox.showerror("Error", f"Failed to write to file:\n{str(e)}")


    def on_decrypt_click(self, event):
        text = self.entry2.get()
        key = self.entry3.get()
        if self.algorithm == "RSA":
            self.privateKey = self.entry4.get()
        try:
            if self.algorithm == "Caesar":
                cipher = CaesarCipher(int(key))
                result = cipher.decrypt(text)

            elif self.algorithm == "Vigenere":
                vigenere_cipher = VigenereCipher(key)
                result = vigenere_cipher.decrypt(text)

            elif self.algorithm == "Rail Fence":
                rail_fence_cipher = RailFenceCipher()
                result = rail_fence_cipher.decrypt(text,key)

            elif self.algorithm == "ROT13":
                rot_cipher = ROT13Cipher()
                result = rot_cipher.decrypt(text)

            elif self.algorithm == "Affine":
                a, b = map(int, key.split(','))
                affine_cipher = AffineCipher(a, b)
                result = affine_cipher.decrypt(text)

            elif self.algorithm == "Play Fair":
                playfair_cipher = PlayfairCipher(key)
                result = playfair_cipher.decrypt(text) # Unpack tuple, use only ciphertext


            elif self.algorithm == "RSA":
                result = self.RSA_cipher.rsa_decrypt(text,self.privateKey)

            elif self.algorithm == "Substitution":
                substitution_cipher = Substitiotion(key)
                result = substitution_cipher.decrypt(text)

            self.entry1.delete(0, tk.END)
            self.entry1.insert(0, result)
        except Exception as e:
            print("Error:", e)
        else:
            if self.current_filepath:
                try:
                    with open(self.current_filepath, 'w') as file:
                        file.write(result)
                    self.canvas.create_text(1000 // 2, 235 + 3 * (
                                self.button_font.metrics("ascent") + self.button_font.metrics("descent") + 21) + 80,
                                            text="File is OverWritten!", font=("Inter Regular", 12), fill="#008FCE",
                                            anchor="center")
                except Exception as e:
                    messagebox.showerror("Error", f"Failed to write to file:\n{str(e)}")

    def logout(self, event):
        self.root.destroy()
        self.logout_callback()

    def go_back(self, event):
        self.root.destroy()  # Close encryption window
        self.dashboard_instance.recreate_dashboard() # Force-show the dashboard
def run(self):
        self.root.mainloop()


# if __name__ == "__main__":
#     app = EncryptionPage()
#     app.run()
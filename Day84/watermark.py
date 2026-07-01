import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageDraw, ImageFont, ImageTk
import os

import sys

os.environ['TCL_LIBRARY'] = os.path.join(sys.base_prefix, "tcl", "tcl8.6")
os.environ['TK_LIBRARY'] = os.path.join(sys.base_prefix, "tcl", "tk8.6")


class WatermarkApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Python Auto-Watermarker")
        self.root.geometry("600x700")

        self.image_path = None
        self.tk_preview = None  # To keep a reference to the image

        # --- UI Elements ---
        tk.Label(root, text="Step 1: Choose your Image", font=("Arial", 12, "bold")).pack(pady=10)

        # Frame to hold the image and the 'X' button
        self.image_frame = tk.Frame(root, width=400, height=300, bg="lightgrey")
        self.image_frame.pack_propagate(False)  # Prevents frame from shrinking
        self.image_frame.pack(pady=5)

        self.preview_label = tk.Label(self.image_frame, bg="lightgrey")
        self.preview_label.place(relx=0.5, rely=0.5, anchor="center")

        # The 'X' button (hidden initially)
        self.remove_btn = tk.Button(self.image_frame, text=" X ", bg="red", fg="white",
                                    font=("Arial", 8, "bold"), command=self.remove_image)

        self.upload_btn = tk.Button(root, text="Upload Image", command=self.upload_image)
        self.upload_btn.pack()

        tk.Label(root, text="Step 2: Enter Watermark Text", font=("Arial", 12, "bold")).pack(pady=15)
        self.watermark_entry = tk.Entry(root, width=35, font=("Arial", 10))
        self.watermark_entry.insert(0, "© MyWebsite.com")
        self.watermark_entry.pack()

        tk.Button(root, text="Apply & Save Watermark", command=self.apply_watermark,
                  bg="#2ecc71", fg="white", font=("Arial", 11, "bold"), height=2).pack(pady=30)

    def upload_image(self):
        file_types = [("Image files", "*.jpg *.jpeg *.png *.bmp")]
        path = filedialog.askopenfilename(filetypes=file_types)

        if path:
            self.image_path = path
            self.show_preview(path)
            self.upload_btn.config(state="disabled")  # Disable upload until current is removed
            self.remove_btn.place(x=370, y=5)  # Show the X button

    def show_preview(self, path):
        # Open and resize for the GUI preview
        img = Image.open(path)
        img.thumbnail((380, 280))  # Resize to fit the frame while keeping aspect ratio

        self.tk_preview = ImageTk.PhotoImage(img)
        self.preview_label.config(image=self.tk_preview)

    def remove_image(self):
        # Reset everything
        self.image_path = None
        self.tk_preview = None
        self.preview_label.config(image='')
        self.upload_btn.config(state="normal")
        self.remove_btn.place_forget()  # Hide the X button

    def apply_watermark(self):
        if not self.image_path:
            messagebox.showerror("Error", "Please upload an image first!")
            return

        text = self.watermark_entry.get()

        try:
            with Image.open(self.image_path).convert("RGBA") as base_image:
                txt_layer = Image.new("RGBA", base_image.size, (255, 255, 255, 0))

                # Dynamic font sizing
                try:
                    font = ImageFont.truetype("arial.ttf", int(base_image.width / 20))
                except:
                    font = ImageFont.load_default()

                d = ImageDraw.Draw(txt_layer)
                bbox = d.textbbox((0, 0), text, font=font)
                textwidth, textheight = bbox[2] - bbox[0], bbox[3] - bbox[1]

                x = base_image.width - textwidth - 30
                y = base_image.height - textheight - 30

                d.text((x, y), text, font=font, fill=(255, 255, 255, 128))
                out = Image.alpha_composite(base_image, txt_layer)

                save_path = filedialog.asksaveasfilename(defaultextension=".png")
                if save_path:
                    out.convert("RGB").save(save_path)
                    messagebox.showinfo("Success", "Watermarked image saved!")

        except Exception as e:
            messagebox.showerror("Error", f"Failed to process image: {e}")


if __name__ == "__main__":
    root = tk.Tk()
    app = WatermarkApp(root)
    root.mainloop()
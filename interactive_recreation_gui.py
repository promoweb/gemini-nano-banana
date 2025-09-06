#!/usr/bin/env python3

# ======================================================
# Gemini Interactive Image Recreation Tool (GUI Version)
# ======================================================

import os
import base64
import json
import datetime
import sys
import threading
import subprocess
from pathlib import Path
import customtkinter as ctk
from tkinter import filedialog, messagebox, Scrollbar
from PIL import Image, ImageTk

try:
    import requests
except ImportError:
    messagebox.showerror("Errore", "La libreria 'requests' non è installata. Installala con: pip install requests")
    sys.exit(1)

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("dark-blue")

class GeminiRecreationGUI:
    def __init__(self):
        self.root = ctk.CTk()
        self.root.title("Gemini Image Recreation Tool")
        self.root.geometry("900x700")
        self.root.resizable(True, True)

        # Variables
        self.api_key = ""
        self.input_path = ""
        self.ref_paths = []
        self.output_path = ""
        self.custom_prompt = ""
        self.is_processing = False

        # Image data
        self.input_image = None
        self.result_image = None

        self.setup_ui()
        self.center_window()

    def center_window(self):
        self.root.update_idletasks()
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f'{width}x{height}+{x}+{y}')

    def setup_ui(self):
        # Main container
        main_frame = ctk.CTkScrollableFrame(self.root)
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)

        # Title
        title_label = ctk.CTkLabel(main_frame, text="Gemini Image Recreation Tool", font=ctk.CTkFont(size=24, weight="bold"))
        title_label.pack(pady=(0, 20))

        # API Key section
        api_frame = ctk.CTkFrame(main_frame)
        api_frame.pack(fill="x", pady=(0, 10))
        ctk.CTkLabel(api_frame, text="🔑 API Key", font=ctk.CTkFont(weight="bold")).pack(anchor="w", padx=10, pady=(10, 0))

        api_input_frame = ctk.CTkFrame(api_frame, fg_color="transparent")
        api_input_frame.pack(fill="x", padx=10, pady=(0, 10))
        self.api_entry = ctk.CTkEntry(api_input_frame, placeholder_text="Enter your Gemini API key", show="*")
        self.api_entry.pack(side="left", fill="x", expand=True)
        self.api_entry.insert(0, os.getenv("GEMINI_API_KEY", ""))

        # Input Image section
        input_frame = ctk.CTkFrame(main_frame)
        input_frame.pack(fill="x", pady=(0, 10))

        ctk.CTkLabel(input_frame, text="📸 Input Image", font=ctk.CTkFont(weight="bold")).pack(anchor="w", padx=10, pady=(10, 0))

        input_btn_frame = ctk.CTkFrame(input_frame, fg_color="transparent")
        input_btn_frame.pack(fill="x", padx=10, pady=(0, 10))

        self.select_input_btn = ctk.CTkButton(input_btn_frame, text="Select Input Image", command=self.select_input_image)
        self.select_input_btn.pack(side="left")

        self.input_path_label = ctk.CTkLabel(input_btn_frame, text="No file selected", fg_color="transparent")
        self.input_path_label.pack(side="left", padx=(20, 0))

        # Preview frame
        self.preview_frame = ctk.CTkFrame(main_frame)
        self.preview_frame.pack(fill="x", pady=(0, 10))

        ctk.CTkLabel(self.preview_frame, text="👁️ Image Preview", font=ctk.CTkFont(weight="bold")).pack(anchor="w", padx=10, pady=(10, 0))

        preview_container = ctk.CTkFrame(self.preview_frame, fg_color="transparent")
        preview_container.pack(fill="x", padx=10, pady=(0, 10))

        # Input image
        self.input_image_label = ctk.CTkLabel(preview_container, text="Input Image: No image loaded", image=None, compound="top")
        self.input_image_label.pack(side="left", padx=(0, 20))

        # Result image
        self.result_image_label = ctk.CTkLabel(preview_container, text="Result Image: Not generated yet", image=None, compound="top")
        self.result_image_label.pack(side="left")

        # Reference Images section
        ref_frame = ctk.CTkFrame(main_frame)
        ref_frame.pack(fill="x", pady=(0, 10))

        ctk.CTkLabel(ref_frame, text="📚 Reference Images (Optional)", font=ctk.CTkFont(weight="bold")).pack(anchor="w", padx=10, pady=(10, 0))

        ref_btn_frame = ctk.CTkFrame(ref_frame, fg_color="transparent")
        ref_btn_frame.pack(fill="x", padx=10, pady=(0, 5))

        self.add_ref_btn = ctk.CTkButton(ref_btn_frame, text="Add Reference", command=self.add_reference_image)
        self.add_ref_btn.pack(side="left")

        self.clear_ref_btn = ctk.CTkButton(ref_btn_frame, text="Clear All", command=self.clear_references, fg_color="transparent")
        self.clear_ref_btn.pack(side="left", padx=(10, 0))

        self.ref_listbox_frame = ctk.CTkScrollableFrame(ref_frame, height=80)
        self.ref_listbox_frame.pack(fill="x", padx=10, pady=(0, 10))

        # Output section
        output_frame = ctk.CTkFrame(main_frame)
        output_frame.pack(fill="x", pady=(0, 10))

        ctk.CTkLabel(output_frame, text="💾 Output Configuration", font=ctk.CTkFont(weight="bold")).pack(anchor="w", padx=10, pady=(10, 0))

        output_radio_frame = ctk.CTkFrame(output_frame, fg_color="transparent")
        output_radio_frame.pack(fill="x", padx=10, pady=(0, 10))

        self.output_var = ctk.StringVar(value="auto_same")
        ctk.CTkRadioButton(output_radio_frame, text="Auto-generate in same directory", variable=self.output_var, value="auto_same").pack(anchor="w")
        ctk.CTkRadioButton(output_radio_frame, text="Auto-generate in current directory", variable=self.output_var, value="auto_current").pack(anchor="w")
        ctk.CTkRadioButton(output_radio_frame, text="Custom path", variable=self.output_var, value="custom").pack(anchor="w")

        self.custom_output_entry = ctk.CTkEntry(output_radio_frame, placeholder_text="Enter custom output path...")
        self.custom_output_entry.pack(fill="x", pady=(10, 0))
        self.custom_output_entry.configure(state="disabled")

        self.output_var.trace("w", self.on_output_radio_change)

        # Prompt section
        prompt_frame = ctk.CTkFrame(main_frame)
        prompt_frame.pack(fill="x", pady=(0, 10))

        ctk.CTkLabel(prompt_frame, text="📝 Generation Prompt", font=ctk.CTkFont(weight="bold")).pack(anchor="w", padx=10, pady=(10, 0))

        prompt_radio_frame = ctk.CTkFrame(prompt_frame, fg_color="transparent")
        prompt_radio_frame.pack(fill="x", padx=10, pady=(0, 10))

        self.prompt_var = ctk.StringVar(value="default")
        ctk.CTkRadioButton(prompt_radio_frame, text="Use default prompt", variable=self.prompt_var, value="default").pack(anchor="w")
        ctk.CTkRadioButton(prompt_radio_frame, text="Custom prompt", variable=self.prompt_var, value="custom").pack(anchor="w")

        self.prompt_textbox = ctk.CTkTextbox(prompt_radio_frame, height=80, wrap="word")
        self.prompt_textbox.pack(fill="x", pady=(10, 0))
        self.prompt_textbox.configure(state="disabled")
        self.prompt_textbox.insert("0.0", "Recreate a new very realistic, sharp and defined color image, high resolution, with current quality standards. As if it was taken by a digital reflex camera.")

        self.prompt_var.trace("w", self.on_prompt_radio_change)

        # Progress and Control
        control_frame = ctk.CTkFrame(main_frame)
        control_frame.pack(fill="x", pady=(0, 10))

        self.progress_bar = ctk.CTkProgressBar(control_frame)
        self.progress_bar.pack(fill="x", padx=10, pady=(10, 0))
        self.progress_bar.set(0)

        self.status_label = ctk.CTkLabel(control_frame, text="Ready", fg_color="transparent")
        self.status_label.pack(pady=(5, 0))

        button_frame = ctk.CTkFrame(control_frame, fg_color="transparent")
        button_frame.pack(fill="x", padx=10, pady=(0, 10))

        self.start_btn = ctk.CTkButton(button_frame, text="🚀 Start Generation", command=self.start_generation, height=40)
        self.start_btn.pack(side="left", expand=True, fill="x", padx=(0, 10))

        self.cancel_btn = ctk.CTkButton(button_frame, text="❌ Cancel", command=self.cancel_generation, fg_color="transparent",
                                       state="disabled", height=40)
        self.cancel_btn.pack(side="left", expand=True, fill="x")

    def on_output_radio_change(self, *args):
        if self.output_var.get() == "custom":
            self.custom_output_entry.configure(state="normal")
        else:
            self.custom_output_entry.configure(state="disabled")

    def on_prompt_radio_change(self, *args):
        if self.prompt_var.get() == "custom":
            self.prompt_textbox.configure(state="normal")
        else:
            self.prompt_textbox.configure(state="disabled")

    def select_input_image(self):
        file_path = filedialog.askopenfilename(
            title="Select Input Image",
            filetypes=[("Image files", "*.jpg *.jpeg *.png *.gif *.bmp *.webp")]
        )
        if file_path:
            self.input_path = file_path
            filename = os.path.basename(file_path)
            self.input_path_label.configure(text=f"Selected: {filename}")
            self.load_input_preview()

    def load_input_preview(self):
        try:
            img = Image.open(self.input_path)
            img.thumbnail((200, 200))
            self.input_image = ImageTk.PhotoImage(img)
            self.input_image_label.configure(image=self.input_image, text="Input Image")
        except Exception as e:
            messagebox.showerror("Error", f"Could not load image preview: {e}")

    def add_reference_image(self):
        file_path = filedialog.askopenfilename(
            title="Select Reference Image",
            filetypes=[("Image files", "*.jpg *.jpeg *.png *.gif *.bmp *.webp")]
        )
        if file_path:
            self.ref_paths.append(file_path)
            self.update_ref_list()

    def clear_references(self):
        self.ref_paths.clear()
        for widget in self.ref_listbox_frame.winfo_children():
            widget.destroy()
        self.ref_listbox_frame._parent_canvas.yview_moveto(0)

    def update_ref_list(self):
        for widget in self.ref_listbox_frame.winfo_children():
            widget.destroy()

        for i, path in enumerate(self.ref_paths):
            frame = ctk.CTkFrame(self.ref_listbox_frame)
            frame.pack(fill="x", pady=(0, 5))

            label = ctk.CTkLabel(frame, text=f"Ref {i+1}: {os.path.basename(path)}", anchor="w")
            label.pack(side="left", fill="x", expand=True)

            remove_btn = ctk.CTkButton(frame, text="Remove", width=80,
                                      command=lambda idx=i: self.remove_reference(idx))
            remove_btn.pack(side="right")

    def remove_reference(self, index):
        if 0 <= index < len(self.ref_paths):
            del self.ref_paths[index]
            self.update_ref_list()

    def cancel_generation(self):
        self.is_processing = False
        self.status_label.configure(text="Cancelled", text_color="orange")
        self.start_btn.configure(state="normal")
        self.cancel_btn.configure(state="disabled")
        self.progress_bar.set(0)

    def start_generation(self):
        # Validate inputs
        self.api_key = self.api_entry.get().strip()
        if not self.api_key:
            messagebox.showwarning("Warning", "Please enter your Gemini API key")
            return

        if not self.input_path:
            messagebox.showwarning("Warning", "Please select an input image")
            return

        if not os.path.isfile(self.input_path):
            messagebox.showerror("Error", "Input image file does not exist")
            return

        # Validate reference images
        for ref in self.ref_paths:
            if not os.path.isfile(ref):
                messagebox.showerror("Error", f"Reference image file does not exist: {ref}")
                return

        # Set output path
        if self.output_var.get() == "auto_same":
            input_dir = os.path.dirname(self.input_path)
            timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
            input_name = Path(self.input_path).stem
            self.output_path = os.path.join(input_dir, f"{input_name}_recreated_{timestamp}.jpg")
        elif self.output_var.get() == "auto_current":
            timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
            input_name = Path(self.input_path).stem
            self.output_path = os.path.join('.', f"{input_name}_recreated_{timestamp}.jpg")
        else:
            custom_path = self.custom_output_entry.get().strip()
            if not custom_path:
                messagebox.showwarning("Warning", "Please enter a custom output path")
                return
            if not custom_path.lower().endswith(('.jpg', '.jpeg')):
                custom_path += ".jpg"
            self.output_path = custom_path

        # Set prompt
        if self.prompt_var.get() == "default":
            self.custom_prompt = "Recreate a new very realistic, sharp and defined color image, high resolution, with current quality standards. As if it was taken by a digital reflex camera."
        else:
            self.custom_prompt = self.prompt_textbox.get("1.0", "end-1c").strip()
            if not self.custom_prompt:
                messagebox.showwarning("Warning", "Please enter a custom prompt")
                return

        # Start processing
        self.is_processing = True
        self.start_btn.configure(state="disabled")
        self.cancel_btn.configure(state="normal")
        self.progress_bar.set(0)
        self.status_label.configure(text="Starting generation...", text_color="blue")

        # Run in separate thread
        threading.Thread(target=self.process_generation, daemon=True).start()

    def process_generation(self):
        try:
            self.status_label.configure(text="Encoding images...")
            self.progress_bar.set(0.2)

            # Encode input image
            img_base64 = self.encode_image_to_base64(self.input_path)
            if not img_base64:
                raise Exception("Failed to encode input image")

            # Encode reference images
            ref_base64_list = []
            for ref_path in self.ref_paths:
                ref_base64 = self.encode_image_to_base64(ref_path)
                if not ref_base64:
                    raise Exception(f"Failed to encode reference image: {ref_path}")
                ref_base64_list.append(ref_base64)

            if self.is_processing:
                self.status_label.configure(text="Sending to Gemini API...")
                self.progress_bar.set(0.5)

                # API call
                payload = self.build_payload(self.custom_prompt, img_base64, ref_base64_list)
                response = requests.post(
                    "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash-image-preview:generateContent",
                    headers={"x-goog-api-key": self.api_key, "Content-Type": "application/json"},
                    json=payload
                )
                response.raise_for_status()

                self.status_label.configure(text="Processing response...")
                self.progress_bar.set(0.7)

                # Extract and save image
                self.save_result_image(response.json(), self.output_path)

                self.status_label.configure(text="Loading result...")
                self.progress_bar.set(0.9)

                # Load result preview
                self.load_result_preview()

                self.progress_bar.set(1.0)
                self.status_label.configure(text="✅ Generation completed!", text_color="green")

                # Open file
                self.open_output_file()

        except Exception as e:
            self.root.after(0, lambda: messagebox.showerror("Error", f"Generation failed: {str(e)}"))
            self.status_label.configure(text=f"❌ Error: {str(e)[:50]}...", text_color="red")
        finally:
            self.is_processing = False
            self.root.after(0, lambda: self.start_btn.configure(state="normal"))
            self.root.after(0, lambda: self.cancel_btn.configure(state="disabled"))

    def encode_image_to_base64(self, file_path):
        try:
            with open(file_path, "rb") as image_file:
                return base64.b64encode(image_file.read()).decode('utf-8')
        except IOError as e:
            return None

    def build_payload(self, prompt, img_base64, ref_base64_list):
        parts = [{"text": prompt}, {"inlineData": {"mimeType": "image/jpeg", "data": img_base64}}]
        for ref_b64 in ref_base64_list:
            parts.append({"inlineData": {"mimeType": "image/jpeg", "data": ref_b64}})
        return {"contents": [{"parts": parts}]}

    def save_result_image(self, response_data, output_path):
        candidate = response_data['candidates'][0]
        content = candidate['content']

        img_data_b64 = None
        for part in content['parts']:
            if 'inlineData' in part:
                img_data_b64 = part['inlineData']['data']
                break

        if not img_data_b64:
            raise Exception("No image data found in response")

        decoded_img = base64.b64decode(img_data_b64)
        with open(output_path, "wb") as f:
            f.write(decoded_img)

    def load_result_preview(self):
        try:
            img = Image.open(self.output_path)
            img.thumbnail((200, 200))
            self.result_image = ImageTk.PhotoImage(img)
            self.result_image_label.configure(image=self.result_image, text="Result Image")
        except Exception as e:
            pass  # Silently fail for preview

    def open_output_file(self):
        try:
            if sys.platform == "win32":
                os.startfile(self.output_path)
            elif sys.platform == "darwin":
                subprocess.run(["open", self.output_path])
            else:
                subprocess.run(["xdg-open", self.output_path])
        except FileNotFoundError:
            pass  # Silently fail if no default opener

    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    app = GeminiRecreationGUI()
    app.run()

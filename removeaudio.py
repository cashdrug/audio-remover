from tkinterdnd2 import DND_FILES, TkinterDnD
import customtkinter as ctk
from tkinter import filedialog, messagebox
from moviepy import VideoFileClip
import sys
import os

# Setup
OUTPUT_DIR = "output-videos"
os.makedirs(OUTPUT_DIR, exist_ok=True)

ctk.set_appearance_mode("System")
ctk.set_default_color_theme("blue")

def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS 
    except AttributeError:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

class App(TkinterDnD.Tk):
    def __init__(self):
        super().__init__()
        self.title("Remove Audio from Video")
        self.geometry("500x400")
        self.resizable(False, False)
        self.iconbitmap(resource_path("icon.ico"))

        self.ctk_frame = ctk.CTkFrame(self)
        self.ctk_frame.pack(fill="both", expand=True)

        self.init_ui()

    def init_ui(self):
        global progress_label, open_button

        title_label = ctk.CTkLabel(self.ctk_frame, text="Remove Audio from a Video", font=ctk.CTkFont(size=18, weight="bold"))
        title_label.pack(pady=20)

        drag_label = ctk.CTkLabel(self.ctk_frame, text="\U0001F4C2 Select video files here", text_color="gray")
        drag_label.pack(pady=5)
        drag_label.drop_target_register(DND_FILES)
        drag_label.dnd_bind("<<Drop>>", self.handle_drop)

        select_button = ctk.CTkButton(self.ctk_frame, text="\U0001F3A5 Select Video", command=self.browse_file, width=220)
        select_button.pack(pady=10)

        progress_label = ctk.CTkLabel(self.ctk_frame, text="", text_color="gray")
        progress_label.pack(pady=5)

        open_button = ctk.CTkButton(self.ctk_frame, text="Open Output Video", command=lambda: None, state="disabled")
        open_button.pack(pady=20)

    def handle_drop(self, event):
        try:
            files = self.tk.splitlist(event.data)
            valid_files = [f for f in files if os.path.isfile(f)]
            if valid_files:
                open_button.configure(state="disabled")
                process_files(valid_files)
        except Exception as e:
            messagebox.showerror("Error", f"Drag-and-drop failed: {e}")

    def browse_file(self):
        try:
            filetypes = [("Video files", "*.mp4 *.mov *.mkv *.avi"), ("All files", "*.*")]
            filepaths = filedialog.askopenfilenames(title="Choose video files", filetypes=filetypes)
            if filepaths:
                open_button.configure(state="disabled")
                process_files(filepaths)
        except Exception as e:
            messagebox.showerror("Error", f"File dialog failed: {e}")

def process_files(filepaths):
    try:
        for filepath in filepaths:
            filename = os.path.basename(filepath)
            name, ext = os.path.splitext(filename)
            output_path = os.path.join(OUTPUT_DIR, f"{name}_no_audio{ext}")

            progress_label.configure(text=f"Processing: {filename}")
            app.update()

            clip = VideoFileClip(filepath)
            clip_no_audio = clip.without_audio()
            clip_no_audio.write_videofile(output_path, codec="libx264", audio=False)

        progress_label.configure(text="All done ✅")
        open_button.configure(state="normal", command=lambda: os.startfile(OUTPUT_DIR))
        messagebox.showinfo("Done", f"All videos processed.\nSaved to: {OUTPUT_DIR}")

    except Exception as e:
        messagebox.showerror("Error", f"Processing failed: {e}")
        progress_label.configure(text="")

if __name__ == "__main__":
    try:
        app = App()
        app.mainloop()
    except Exception as e:
        messagebox.showerror("Fatal Error", str(e))
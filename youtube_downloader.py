import tkinter as tk
from tkinter import ttk, filedialog
import subprocess
import os

class YouTubeDownloaderGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("YouTube Audio Downloader")
        self.root.geometry("600x300")
        
        # URL Input
        url_frame = ttk.LabelFrame(root, text="YouTube URL", padding="10")
        url_frame.pack(fill="x", padx=10, pady=5)
        
        self.url_entry = ttk.Entry(url_frame, width=50)
        self.url_entry.pack(fill="x", padx=5)
        
        # Audio Codec Selection
        codec_frame = ttk.LabelFrame(root, text="Audio Codec", padding="10")
        codec_frame.pack(fill="x", padx=10, pady=5)
        
        self.codec_var = tk.StringVar(value="mp3")
        codecs = ["mp3", "m4a", "wav", "aac"]
        
        for codec in codecs:
            ttk.Radiobutton(codec_frame, text=codec, value=codec,
                           variable=self.codec_var).pack(side="left", padx=10)
        
        # Convert Button
        self.convert_btn = ttk.Button(root, text="Convert", command=self.convert)
        self.convert_btn.pack(pady=20)
        
        # Progress Label
        self.status_label = ttk.Label(root, text="")
        self.status_label.pack(pady=10)

    def convert(self):
        url = self.url_entry.get().strip()
        if not url:
            self.status_label.config(text="Please enter a valid URL")
            return
            
        codec = self.codec_var.get()
        
        # Ask user where to save the file
        save_path = filedialog.asksaveasfilename(
            defaultextension=f".{codec}",
            filetypes=[(f"{codec.upper()} files", f"*.{codec}")]
        )
        
        if not save_path:
            return
            
        self.status_label.config(text="Downloading and converting...")
        self.root.update()
        
        try:
            # Prepare yt-dlp command
            command = [
                "yt-dlp",
                "-x",  # Extract audio
                f"--audio-format={codec}",
                "-o", save_path,
                url
            ]
            
            # Execute command
            process = subprocess.Popen(
                command,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                universal_newlines=True
            )
            
            stdout, stderr = process.communicate()
            
            if process.returncode == 0:
                self.status_label.config(text="Conversion completed successfully!")
            else:
                self.status_label.config(text=f"Error: {stderr}")
                
        except Exception as e:
            self.status_label.config(text=f"Error: {str(e)}")

if __name__ == "__main__":
    root = tk.Tk()
    app = YouTubeDownloaderGUI(root)
    root.mainloop()
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import yt_dlp
import threading

# Theme
BG_COLOR = "#ffe6f0"
BTN_COLOR = "#ffb6c1"
BTN_TEXT = "#ffffff"
TEXT_COLOR = "#5a2a3a"
ENTRY_BG = "#fff0f6"

# Functions
def browse_folder():
    folder = filedialog.askdirectory()
    if folder:
        path_var.set(folder)

def progress_hook(d):
    if d['status'] == 'downloading':
        total = d.get('total_bytes') or d.get('total_bytes_estimate')
        downloaded = d.get('downloaded_bytes', 0)
        if total:
            percent = int(downloaded / total * 100)
            progress_bar["value"] = percent
            progress_var.set(f"{percent}%")
    elif d['status'] == 'finished':
        progress_bar["value"] = 100
        progress_var.set("Processing...")

def download():
    url = url_entry.get()
    mode = mode_var.get()
    path = path_var.get()
    quality = quality_var.get()

    if not url or not path:
        messagebox.showerror("Ruby says…", "URL dan folder tujuan harus diisi yaa 🥺")
        return

    status_label.config(text="⏳ Ruby lagi downloadin buat kamu…")
    progress_bar["value"] = 0
    progress_var.set("0%")

# Video / Audio download di thread yang berbeda
    def run():
        try:
            if mode == "video":
                if quality == "Best":
                    fmt = "bestvideo+bestaudio/best"
                elif quality == "720p":
                    fmt = "bestvideo[height<=720]+bestaudio/best"
                else:
                    fmt = "bestvideo[height<=480]+bestaudio/best"

                ydl_opts = {
                    'outtmpl': f'{path}/%(title)s.%(ext)s',
                    'format': fmt,
                    'merge_output_format': 'mp4',
                    'progress_hooks': [progress_hook],
                    'restrictfilenames': True,
                }

            else:
                if quality == "Best":
                    bitrate = "192"
                elif quality == "192kbps":
                    bitrate = "192"
                else:
                    bitrate = "128"

                ydl_opts = {
                    'outtmpl': f'{path}/%(title)s.%(ext)s',
                    'format': 'bestaudio/best',
                    'postprocessors': [{
                        'key': 'FFmpegExtractAudio',
                        'preferredcodec': 'mp3',
                        'preferredquality': bitrate,
                    }],
                    'progress_hooks': [progress_hook],
                    'restrictfilenames': True,
                }

            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([url])

# Selesai
            progress_bar["value"] = 0
            progress_var.set("Download selesai")
            status_label.config(text="✅ Download selesai")

        except Exception as e:
            status_label.config(text="❌ Gagal…")
            messagebox.showerror("Ruby sedih…", str(e))

    threading.Thread(target=run).start()

def update_quality_options(*args):
    menu = quality_menu["menu"]
    menu.delete(0, "end")

    if mode_var.get() == "video":
        options = ["Best", "720p", "480p"]
    else:
        options = ["Best", "192kbps", "128kbps"]

    for opt in options:
        menu.add_command(label=opt, command=lambda v=opt: quality_var.set(v))

    quality_var.set(options[0])

# Tampilan GUI
root = tk.Tk()
root.title("Ruby Downloader 💎")
root.geometry("500x420")
root.resizable(False, False)
root.configure(bg=BG_COLOR)

# Title
title = tk.Label(root, text="🌸 Ruby Downloader 🌸",
                 font=("Comic Sans MS", 14, "bold"), bg=BG_COLOR, fg=TEXT_COLOR)
title.pack(pady=10)

# URL
tk.Label(root, text="YouTube / Instagram / TikTok URL:", bg=BG_COLOR, fg=TEXT_COLOR).pack()
url_entry = tk.Entry(root, width=55, bg=ENTRY_BG, relief="flat")
url_entry.pack(pady=5)

# Mode
mode_var = tk.StringVar(value="video")
mode_var.trace("w", update_quality_options)

tk.Label(root, text="Mode:", bg=BG_COLOR, fg=TEXT_COLOR).pack(pady=5)
frame_mode = tk.Frame(root, bg=BG_COLOR)
frame_mode.pack()

tk.Radiobutton(frame_mode, text="🎥 Video", variable=mode_var, value="video",
               bg=BG_COLOR, fg=TEXT_COLOR, selectcolor=BG_COLOR).grid(row=0, column=0, padx=15)
tk.Radiobutton(frame_mode, text="🎧 Audio", variable=mode_var, value="audio",
               bg=BG_COLOR, fg=TEXT_COLOR, selectcolor=BG_COLOR).grid(row=0, column=1, padx=15)

# Quality
quality_var = tk.StringVar(value="Best")
tk.Label(root, text="Quality:", bg=BG_COLOR, fg=TEXT_COLOR).pack(pady=5)

quality_menu = tk.OptionMenu(root, quality_var, "Best", "720p", "480p")
quality_menu.config(bg=BTN_COLOR, fg=BTN_TEXT, relief="flat", width=12)
quality_menu.pack()

# Path
path_var = tk.StringVar()
tk.Label(root, text="Save To Folder:", bg=BG_COLOR, fg=TEXT_COLOR).pack(pady=5)
frame_path = tk.Frame(root, bg=BG_COLOR)
frame_path.pack()

tk.Entry(frame_path, textvariable=path_var, width=38, bg=ENTRY_BG, relief="flat").grid(row=0, column=0, padx=5)
tk.Button(frame_path, text="Browse", command=browse_folder,
          bg=BTN_COLOR, fg=BTN_TEXT, relief="flat", width=10).grid(row=0, column=1)

# Progress Bar
progress_bar = ttk.Progressbar(root, length=380, mode="determinate")
progress_bar.pack(pady=12)

progress_var = tk.StringVar(value="0%")
tk.Label(root, textvariable=progress_var, bg=BG_COLOR, fg=TEXT_COLOR).pack()

# Download Button
tk.Button(root, text="⬇ Download with Ruby", command=download,
          bg=BTN_COLOR, fg=BTN_TEXT, relief="flat",
          font=("Arial", 11, "bold"),
          width=30, height=2).pack(pady=15)

# Status
status_label = tk.Label(root, text="", bg=BG_COLOR, fg=TEXT_COLOR)
status_label.pack()

root.mainloop()

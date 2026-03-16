# 🛠️ Scripts

Personal collection of bash and python scripts to automate daily tasks on Linux.

---

## 📁 Structure

```
scripts/
├── colors           # Color definitions (sourced by other scripts)
├── clean            # System cleanup
├── sys-update       # System and package updater
├── my-wifi          # Show WiFi password
├── ip-check         # Show local and public IP
├── laptop-info      # Show battery and CPU info
├── organize         # Organize Downloads folder
├── new-project      # Create a new dev project
├── pdf-split        # Split a PDF by page range (bash wrapper)
├── ytdl             # Download YouTube audio as MP3 (bash wrapper)
├── .gitignore
└── Python/
    ├── pdf-separator.py
    └── descargar_youtube.py
```

---

## 📜 Scripts

### `colors`
Defines color variables used by all other scripts. It's sourced at the beginning of each script, not executed directly.

```bash
source ~/scripts/colors
```

---

### `clean`
Clears RAM cache, swap, APT packages, thumbnail cache and empties the trash. Shows memory usage at the end.

```bash
clean
```

---

### `sys-update`
Updates system packages via APT and global NPM packages.

```bash
sys-update
```

---

### `my-wifi`
Shows the current WiFi network password using `nmcli`.

```bash
my-wifi
```

---

### `ip-check`
Shows your local IP (via `hostname`) and your public IP (via `ifconfig.me`).

```bash
ip-check
```

---

### `laptop-info`
Shows battery status (charge, health) and CPU usage and temperature via `upower` and `sensors`.

```bash
laptop-info
```

> **Requirements:** `upower`, `lm-sensors` (`sudo apt install lm-sensors`)

---

### `organize`
Organizes files in `~/Downloads` into subfolders by type:

| Folder | File types |
|---|---|
| Documents | pdf, docx, doc, pptx, pages |
| Excel, csv | xlsx, xls, csv |
| Music | mp3, wav, m4a |
| Images | jpg, jpeg, png, gif, webp, svg |
| Videos | mp4, mkv, avi, mov |
| Development | html, har, json, log |
| Compressed | zip, tar, gz, rar, 7z |
| Programs | deb, iso, sh, exe, apk |

```bash
organize
```

---

### `new-project`
Interactive script to create a new development project. It asks for a name, a context (UNI / Work / Personal) and a language/framework, then sets up the folder structure, initializes git and opens VSCode.

**Supported types:** `c`, `python`, `react`, `node`, `html`

```bash
new-project my-app
```

---

### `pdf-split` + `Python/pdf-separator.py`
Splits a PDF file by a page range and saves it as a new file. The bash script calls the Python script using a virtual environment.

```bash
pdf-split
```

The Python script will interactively ask for:
- Path to the original PDF
- Start and end page
- Output file name (optional, auto-generated if left blank)

> **Requirements:** `pip install PyPDF2` inside the `.venv`

---

### `ytdl` + `Python/descargar_youtube.py`
Downloads the audio from a YouTube video and converts it to MP3. Shows a progress bar during the download. Files are saved to `~/Downloads/YoutubeMusic/`.

```bash
ytdl <youtube-url>
ytdl <youtube-url> -c 320   # specify quality in kbps (default: 192)
```

> **Requirements:** `pip install yt-dlp` and `ffmpeg` (`sudo apt install ffmpeg`) inside the `.venv`

---

## ⚙️ Setup

### 1. Clone the repo
```bash
git clone https://github.com/your-username/scripts.git ~/scripts
```

### 2. Make scripts executable
```bash
chmod +x ~/scripts/*
```

### 3. Add to PATH (add this to your `~/.bashrc` or `~/.zshrc`)
```bash
export PATH="$HOME/scripts:$PATH"
```

### 4. Set up Python virtual environment (for pdf-split and ytdl)
```bash
cd ~/scripts/Python
python3 -m venv .venv
source .venv/bin/activate
pip install PyPDF2 yt-dlp
deactivate
```

---

## 🖥️ OS
Tested on **Linux Mint** (Ubuntu-based). Most scripts should work on any Debian/Ubuntu distro.
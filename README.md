<br />
<div align="center">
  <a href="https://github.com/oshriagronov/local-chat">
    <img src="assets/app_icon.png" alt="Logo" width="200" height="200">
  </a>

<h3 align="center">LocalChat</h3>
  <p align="center">
    Simple chat interface designed to interact with open language models.
  </p>
</div>

## About

The goal of this project is to make open language models accessible to end users who do not want to deal with command-line interfaces or coding. It provides a clean, easy-to-use GUI for chatting with models locally.

### Key Features

- **Normal mode**
  → Chat with the 1B model for lightweight usage(Gemma3:1b).
- **Expert mode**
  → Chat with the more powerful 4B model(Gemma3:4b).
- **Web Search (Expert mode only)**
  → Allows the model to fetch answers from the web.
- **Multi-language support**
  → Models support a wide range of languages.
- **Local usage**
  → Run the models locally without sending data to any external service.

## Hardware Recommendations

- **Normal mode (1B model):** Requires at least 8GB of RAM, can work without GPU.
- **Expert mode (4B model):** Recommended 16GB of RAM and decent GPU(I will say 2GB Vram at the very lest) for optimal performance.

## Planned Upgrades

- Conversation history support
- PDF file reading capability
- Modern UI redesign
- Easier installation process

## Technologies Used

- `custometkinter`
- `tkinter`
- `llm-axe`
- `PIL`

## Tools Utilized

- `ollama`

## Media

  <img src="/example.jpg" alt="example of the chat interface">

## Getting Started

To get a local copy up and running follow these simple steps.

## Download Executable (No Python Needed)

Prebuilt executables are published on GitHub Releases for Windows, macOS, and Linux.
Download the file for your OS from the latest release and run it.

Notes:
- You still need Ollama installed and the Gemma3 models pulled (see steps 4-5 below).
- On macOS, you may need to right-click the app/executable and choose **Open** the first time.

### Prerequisites

- Linux, MacOS or Windows
- ollama
- Python 3.11 or 3.12 (recommended)
- tkinter

### Installation

---

1. **Clone and enter the Magnetron repository:**

   ```bash
   git clone https://github.com/oshriagronov/local-chat && cd local-chat
   ```

2. **Create and activate a virtual environment:**

   ```bash
   python3 -m venv .venv && source .venv/bin/activate
   ```

3. **Install LocalChat**  
   _(Make sure tkinter installed – see [Prerequisites](#prerequisites)):_

   ```bash
   pip install -r requirements.txt
   ```

4. **install Ollama**
   through this link: https://ollama.com/download

5. **install Gemma3 models**
  <br/>The smaller model:
    ```bash
      ollama run gemma3:1b
    ```
    _The "expert" model:_
    ```bash
    ollama run gemma3:4b-it-qat
    ```

6. **Run the app:**
    ```bash
    python3 main.py
    ```

---

## Build Executable Locally

Use the helper script (recommended):

```bash
bash scripts/build_local.sh
```

What it does:
- Uses Python 3.12 (or 3.11 if 3.12 is unavailable)
- Creates `.venv`
- Installs dependencies and PyInstaller
- Builds `dist/LocalChat.app` on macOS
- Builds `dist/LocalChat-linux-x86_64.AppImage` on Linux
- Builds `dist/LocalChat.exe` on Windows (when run under Windows shell)

Optional target override:

```bash
bash scripts/build_local.sh mac
bash scripts/build_local.sh linux-appimage
bash scripts/build_local.sh windows
```

Note for macOS:
- The selected Python must include `tkinter` (`_tkinter`).
- If Finder blocks opening, use right-click `LocalChat.app` -> `Open` on first launch.

Manual PyInstaller command (if needed):

```bash
python3 -m pip install --upgrade pip
pip install --only-binary=:all: -r requirements.txt
pip install pyinstaller
pyinstaller --noconfirm --clean --windowed --onefile --name LocalChat --collect-data llm_axe --add-data "assets:assets" main.py
```

On Windows, replace the `--add-data` separator with `;`:

```bash
pyinstaller --noconfirm --clean --windowed --onefile --name LocalChat --collect-data llm_axe --add-data "assets;assets" main.py
```

The executable will be in `dist/`.

On macOS, if you want a double-clickable `.app` bundle, remove `--onefile`:

```bash
pyinstaller --noconfirm --clean --windowed --name LocalChat --collect-data llm_axe --add-data "assets:assets" main.py
```

## Build Executables Automatically on GitHub Releases

This repo includes a GitHub Actions workflow at:
`.github/workflows/build-release.yml`

It builds Windows, macOS, and Linux executables when:
- You push a tag like `v1.0.0`

Quick publish flow:

```bash
git tag v1.0.0
git push origin v1.0.0
```

After the workflow finishes, your release gets:
- `LocalChat-windows.exe`
- `LocalChat-macOS.zip` (contains `LocalChat.app`)
- `LocalChat-linux-x86_64.AppImage`

Feel free to chat with me about anything. I hope you enjoy my project!

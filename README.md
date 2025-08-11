<br />
<div align="center">
  <a href="https://github.com/oshriagronov/local-chat">
    <img src="assets/app_icon.png" alt="Logo" width="200" height="200">
  </a>

<h3 align="center">LocalChat</h3>
  <p align="center">
    simple and user-friendly chat interface designed to interact with open language models, specifically the Gemma3 models in 1B and 4B sizes.
  </p>
</div>

## Features

- **Two Modes:**
  - **Normal mode:** Chat with the 1B model for lightweight usage(Gemma3:1b).
  - **Expert mode:** Chat with the more powerful 4B model(Gemma3:4b).
- **Web Search (Expert mode only):** Allows the model to fetch answers from the web.
- **Multi-language support:** Models support a wide range of languages.
- **Local usage:** Run the models locally without sending data to any external service.

## Hardware Recommendations

- **Normal mode (1B model):** Requires at least 8GB of RAM, can work without GPU.
- **Expert mode (4B model):** Recommended 16GB of RAM and decent GPU(I will say 2GB Vram at the very lest) for optimal performance.

## Purpose

The goal of this project is to make open language models accessible to end users who do not want to deal with command-line interfaces or coding. It provides a clean, easy-to-use GUI for chatting with models locally.

## Planned Upgrades

- Conversation history support
- PDF file reading capability
- Modern UI redesign

## Technologies Used

- `custometkinter`
- `tkinter`
- `llm-axe`
- `PIL` (Python Imaging Library)

## Tools Utilized

- `ollama`

## Installation Guide

Follow these steps to set up the project on your local machine:

### 1. Install Python (if not installed)

Make sure Python 3.8+ is installed on your system. You can download it from [python.org](https://www.python.org/downloads/).

### 2. Install pip (if not installed)

Check if pip is installed:

```bash
pip --version
```

If not installed, try the following commands:

```bash
pip --version
```

---

Feel free to contribute or open issues if you have suggestions or encounter any problems!

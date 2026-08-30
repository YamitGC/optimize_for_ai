# DOCX → AI-Optimized Markdown/Text Converter

> 🌐 **Language:** [English](README.md) | [Español](README.es.md)

A small Python utility that takes a `.docx` file, strips out repetitive headers/footers (which waste tokens when feeding documents to an LLM), and converts it into two AI-friendly formats:

- **`.md`** — Markdown, preserving heading hierarchy and tables.
- **`.txt`** — Plain text, minimal token footprint.

---

## Table of Contents

- [How It Works](#how-it-works)
- [Requirements](#requirements)
- [Installation](#installation)
  - [🪟 Windows](#-windows)
  - [🐧 Linux](#-linux)
    - [Ubuntu / Debian / Pop!_OS](#ubuntu--debian--pop_os)
    - [Linux Mint](#linux-mint)
    - [Fedora](#fedora)
    - [Arch Linux / Manjaro](#arch-linux--manjaro)
- [Usage](#usage)
- [Output Example](#output-example)
- [Troubleshooting](#troubleshooting)
- [Project Structure](#project-structure)
- [License](#license)

---

## How It Works

The script (`optimize_for_ai.py`) does the following:

1. Resolves the input path (expands `~` and turns it into an absolute path). If the given filename doesn't exist in the current directory, it automatically also looks for it in `~/Documents` and `~/Downloads` — so you can run the script from anywhere and just pass the file name, without typing the full path, as long as the file lives in one of those two folders.
2. Opens the resolved `.docx` with `python-docx`.
3. Clears the text of every header and footer in every section (these usually contain page numbers, logos, or repeated boilerplate that adds no value for an AI).
4. Saves a temporary cleaned copy.
5. Converts that copy using `markitdown` into structured Markdown text.
6. Writes the **`.md`** file with the full Markdown structure intact — headings, tables, bold text, links, etc. Use this when the AI needs to understand hierarchy or table relationships.
7. Strips all Markdown syntax (`#`, `**`, `|`, list markers, link URLs, horizontal rules, blockquote markers, extra blank lines...) and writes the result as **`.txt`** — real plain text with only the informational content, no formatting overhead. This is the cheapest format in tokens; use it when only the content matters, not the structure.
8. Deletes the temporary file and prints a character-count comparison between `.md` and `.txt` so you can see the actual token savings.

> 💡 **Tip:** If your file isn't in the current folder, `Documents`, or `Downloads`, just pass the full path instead of only the filename, e.g. `python optimize_for_ai.py C:\Users\me\Desktop\report.docx` (Windows) or `python3 optimize_for_ai.py ~/Desktop/report.docx` (Linux).

---

## Requirements

- **Python 3.9 or newer** (3.10+ recommended).
- **pip** (Python package manager).
- Internet access the first time you install dependencies.
- The two Python packages listed in [`requirements.txt`](requirements.txt):
  - [`python-docx`](https://pypi.org/project/python-docx/)
  - [`markitdown`](https://pypi.org/project/markitdown/)

> 💡 `markitdown` can optionally handle more file types (PDF, PPTX, images with OCR, audio transcription, etc.) if you install it with extras: `pip install "markitdown[all]"`. For this script, the base install is enough since we only need `.docx` support.

---

## Installation

Clone or download this repository first:

```bash
git clone https://github.com/YamitGC/optimize_for_ai.git
cd optimize_for_ai
```

### 🪟 Windows

1. **Install Python**
   - Download the installer from [python.org/downloads](https://www.python.org/downloads/).
   - Run it and **check the box "Add python.exe to PATH"** before clicking *Install Now*. This is the #1 cause of "python is not recognized" errors.

2. **Verify the installation** (open *PowerShell* or *CMD*):
   ```powershell
   python --version
   pip --version
   ```
   If `python` is not recognized, close and reopen the terminal, or reinstall Python making sure to tick the PATH checkbox.

3. **(Recommended) Create a virtual environment**
   ```powershell
   python -m venv venv
   venv\Scripts\activate
   ```
   You should now see `(venv)` at the start of your prompt.

   > If PowerShell blocks the activation script with an "execution policy" error, run PowerShell **as Administrator** once and execute:
   > ```powershell
   > Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
   > ```
   > Then try activating again.

4. **Install dependencies**
   ```powershell
   pip install -r requirements.txt
   ```

5. **Run the script**
   ```powershell
   python optimize_for_ai.py mi_documento.docx
   ```

6. **(Optional) Deactivate the virtual environment when done**
   ```powershell
   deactivate
   ```

---

### 🐧 Linux

General notes for all distributions:
- Use `python3` and `pip3` explicitly (some distros don't alias `python`/`pip` to Python 3).
- It's strongly recommended to use a **virtual environment** to avoid conflicts with system-managed Python packages (especially on modern Debian/Ubuntu, which block global `pip install` by default — see [Troubleshooting](#troubleshooting)).

#### Ubuntu / Debian / Pop!_OS

```bash
sudo apt update
sudo apt install -y python3 python3-pip python3-venv

python3 -m venv venv
source venv/bin/activate

pip install -r requirements.txt
python3 optimize_for_ai.py mi_documento.docx
```

#### Linux Mint

Mint is Ubuntu/Debian-based, so the same commands apply:

```bash
sudo apt update
sudo apt install -y python3 python3-pip python3-venv

python3 -m venv venv
source venv/bin/activate

pip install -r requirements.txt
python3 optimize_for_ai.py mi_documento.docx
```

#### Fedora

Fedora uses `dnf` and generally ships `python3`/`pip3` already, but `venv` support may need an explicit package:

```bash
sudo dnf install -y python3 python3-pip python3-virtualenv

python3 -m venv venv
source venv/bin/activate

pip install -r requirements.txt
python3 optimize_for_ai.py mi_documento.docx
```

#### Arch Linux / Manjaro

Arch ships a very recent Python via `pacman`, and `python-pip` includes `venv` support already:

```bash
sudo pacman -Syu --needed python python-pip

python -m venv venv
source venv/bin/activate

pip install -r requirements.txt
python optimize_for_ai.py mi_documento.docx
```

> ⚠️ Arch is a rolling-release distro with very new Python versions. If `markitdown` or `python-docx` throws a compatibility error, check the [Troubleshooting](#troubleshooting) section for the `--break-system-packages` note or pin dependency versions in `requirements.txt`.

---

## Usage

Once dependencies are installed (and your virtual environment is activated, if you created one):

```bash
python optimize_for_ai.py path/to/document.docx
```

You can also just pass the filename (no path) if the file is in your current folder, `Documents`, or `Downloads` — the script will find it automatically:

```bash
python optimize_for_ai.py my_report.docx
```

This generates, in the same folder where the input file was found:

- `document.md`
- `document.txt`

---

## Output Example

```
Procesando: /home/user/Documents/document.docx
Limpiando el documento...
Convirtiendo a formatos para IA...

¡Listo! Archivos generados en /home/user/Documents:
 - document.md  (19,000 caracteres, con formato Markdown)
 - document.txt  (16,800 caracteres, texto plano)
   Reducción de caracteres del .txt frente al .md: 11.6%
```

> Note: console messages are printed in Spanish regardless of your system language, since that's how the script was written. Actual percentages vary depending on how much Markdown formatting (tables, headings, bold text, links) the source document contains.

---

## Troubleshooting

| Problem | Cause | Fix |
|---|---|---|
| `python: command not found` (Linux) or `'python' is not recognized` (Windows) | Python not installed or not in PATH | Reinstall Python and make sure PATH is configured (see OS-specific steps above), or use `python3` on Linux |
| `error: externally-managed-environment` when running `pip install` | Modern Debian/Ubuntu/Mint (PEP 668) blocks global pip installs | Use a virtual environment (`python3 -m venv venv && source venv/bin/activate`) — **do not** use `--break-system-packages` unless you fully understand the risk |
| `ModuleNotFoundError: No module named 'docx'` | `python-docx` not installed, or installed in a different environment than the one running the script | Activate your virtual environment before installing/running, or reinstall with `pip install -r requirements.txt` |
| `ModuleNotFoundError: No module named 'markitdown'` | Same as above, applied to `markitdown` | Same fix |
| Script runs but produces an empty or broken `.md` | Corrupted or password-protected `.docx` file | Open and re-save the file in Word/LibreOffice first, and remove any password protection |
| `PermissionError` when saving output files | The `.docx` (or the output folder) is open in Word or is read-only | Close the file in any other program and check folder write permissions |
| PowerShell won't run `venv\Scripts\activate` | Execution policy restriction | Run `Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser` in an elevated PowerShell |
| `pip` installs succeed but script still fails on Fedora/Arch after a system update | System Python got upgraded and broke the venv | Delete the `venv` folder and recreate it (`rm -rf venv && python3 -m venv venv`) |
| `Error: No se encontró '<file>' en el directorio actual, ni en Documents ni en Downloads` | You typed a filename that isn't in the current folder, `~/Documents`, or `~/Downloads` | Double-check the spelling/extension, move the file into one of those folders, or pass the full path instead (e.g. `~/Desktop/file.docx`) |

---

## Project Structure

```
.
├── optimize_for_ai.py     # Main conversion script
├── requirements.txt       # Python dependencies
├── README.md               # This file (English)
├── README.es.md            # Spanish version
├── LICENSE.md               # License (English)
└── LICENSE.es.md            # License (Spanish, informational)
```

---

## License

This project is distributed under the [MIT License](LICENSE.md). See [`LICENSE.md`](LICENSE.md) for the full text (or [`LICENSE.es.md`](LICENSE.es.md) for a Spanish informational translation).

#!/usr/bin/env bash
set -euo pipefail

# Always run from the repository root, regardless of caller cwd.
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
cd "$REPO_ROOT"

if [[ ! -f "requirements.txt" || ! -f "main.py" || ! -d "assets" ]]; then
  echo "Project files not found in $REPO_ROOT"
  exit 1
fi

TARGET="${1:-auto}"

if [[ "$TARGET" == "-h" || "$TARGET" == "--help" ]]; then
  echo "Usage: bash scripts/build_local.sh [auto|mac|windows|linux-appimage]"
  exit 0
fi

choose_python() {
  local candidate v
  for candidate in python3.12 python3.11; do
    if command -v "$candidate" >/dev/null 2>&1; then
      v="$("$candidate" -c 'import sys; print(f"{sys.version_info.major}.{sys.version_info.minor}")' 2>/dev/null || true)"
      if [[ "$v" == "3.12" || "$v" == "3.11" ]]; then
        if "$candidate" -c 'import tkinter' >/dev/null 2>&1; then
          echo "$candidate"
          return 0
        fi
      fi
    fi
  done

  if command -v python3 >/dev/null 2>&1; then
    v="$(python3 -c 'import sys; print(f"{sys.version_info.major}.{sys.version_info.minor}")')"
    if [[ "$v" == "3.12" || "$v" == "3.11" ]]; then
      if python3 -c 'import tkinter' >/dev/null 2>&1; then
        echo "python3"
        return 0
      fi
    fi
  fi

  echo ""
}

PYTHON_BIN="${PYTHON_BIN:-$(choose_python)}"

if [[ -z "$PYTHON_BIN" ]]; then
  echo "Python 3.11/3.12 with tkinter support was not found."
  echo "LocalChat needs tkinter; your current Python build does not include _tkinter."
  echo "macOS option 1: install Python 3.12 from python.org (includes tkinter)."
  echo "macOS option 2 (Homebrew): brew install python@3.12 python-tk@3.12"
  exit 1
fi

echo "Using $PYTHON_BIN"
echo "Project root: $REPO_ROOT"
"$PYTHON_BIN" -V

rm -rf .venv
"$PYTHON_BIN" -m venv .venv
# shellcheck disable=SC1091
source .venv/bin/activate

python -m pip install --upgrade pip
pip install --only-binary=:all: -r requirements.txt
pip install pyinstaller

OS_NAME="$(uname -s)"

if [[ "$TARGET" == "auto" ]]; then
  if [[ "$OS_NAME" == "Darwin" ]]; then
    TARGET="mac"
  elif [[ "$OS_NAME" == "Linux" ]]; then
    TARGET="linux-appimage"
  elif [[ "$OS_NAME" == MINGW* || "$OS_NAME" == MSYS* || "$OS_NAME" == CYGWIN* ]]; then
    TARGET="windows"
  else
    echo "Unsupported OS for auto target: $OS_NAME"
    exit 1
  fi
fi

echo "Build target: $TARGET"

if [[ "$TARGET" == "mac" ]]; then
  if [[ "$OS_NAME" != "Darwin" ]]; then
    echo "mac target can only be built on macOS."
    exit 1
  fi
  pyinstaller --noconfirm --clean --windowed --name LocalChat --collect-data llm_axe --add-data "assets:assets" main.py

  # Improve double-click behavior for local builds on macOS.
  codesign --force --deep --sign - dist/LocalChat.app >/dev/null 2>&1 || true
  xattr -dr com.apple.quarantine dist/LocalChat.app >/dev/null 2>&1 || true

  echo "Build complete: dist/LocalChat.app"
  echo "If Finder still blocks launch: right-click LocalChat.app > Open (first launch only)."
elif [[ "$TARGET" == "windows" ]]; then
  if [[ "$OS_NAME" != MINGW* && "$OS_NAME" != MSYS* && "$OS_NAME" != CYGWIN* ]]; then
    echo "windows target must be built on Windows."
    echo "Use GitHub release workflow to build cross-platform artifacts."
    exit 1
  fi
  pyinstaller --noconfirm --clean --windowed --onefile --name LocalChat --collect-data llm_axe --add-data "assets;assets" main.py
  echo "Build complete: dist/LocalChat.exe"
elif [[ "$TARGET" == "linux-appimage" ]]; then
  if [[ "$OS_NAME" != "Linux" ]]; then
    echo "linux-appimage target must be built on Linux."
    echo "Use GitHub release workflow to build cross-platform artifacts."
    exit 1
  fi
  pyinstaller --noconfirm --clean --windowed --name LocalChat --collect-data llm_axe --add-data "assets:assets" main.py

  rm -rf AppDir
  mkdir -p AppDir/usr/bin
  cp -R dist/LocalChat/* AppDir/usr/bin/

  cat > AppDir/AppRun <<'EOF'
#!/bin/sh
HERE="$(dirname "$(readlink -f "$0")")"
exec "$HERE/usr/bin/LocalChat" "$@"
EOF
  chmod +x AppDir/AppRun

  cat > AppDir/LocalChat.desktop <<'EOF'
[Desktop Entry]
Type=Application
Name=LocalChat
Exec=LocalChat
Icon=LocalChat
Categories=Utility;
Terminal=false
EOF

  cp assets/app_icon.png AppDir/LocalChat.png

  APPIMAGETOOL="./appimagetool-x86_64.AppImage"
  if [[ ! -f "$APPIMAGETOOL" ]]; then
    curl -L -o "$APPIMAGETOOL" "https://github.com/AppImage/AppImageKit/releases/download/continuous/appimagetool-x86_64.AppImage"
    chmod +x "$APPIMAGETOOL"
  fi

  APPIMAGE_EXTRACT_AND_RUN=1 ARCH=x86_64 "$APPIMAGETOOL" AppDir dist/LocalChat-linux-x86_64.AppImage
  echo "Build complete: dist/LocalChat-linux-x86_64.AppImage"
else
  echo "Unknown target: $TARGET"
  echo "Usage: bash scripts/build_local.sh [auto|mac|windows|linux-appimage]"
  exit 1
fi

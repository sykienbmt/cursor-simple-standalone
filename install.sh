#!/bin/bash
#
# Cursor Simple - Installation Script
# For Linux and macOS
#

set -e

echo "╔═══════════════════════════════════════════════════════════╗"
echo "║                                                           ║"
echo "║           🚀 Cursor Simple - Installer 🚀                ║"
echo "║                                                           ║"
echo "╚═══════════════════════════════════════════════════════════╝"
echo ""

# Detect OS
OS="$(uname -s)"
case "${OS}" in
    Linux*)     OS_NAME="Linux";;
    Darwin*)    OS_NAME="macOS";;
    *)          OS_NAME="Unknown";;
esac

echo "Detected OS: ${OS_NAME}"
echo ""

# Check Python
if command -v python3 &> /dev/null; then
    PYTHON_CMD="python3"
    PIP_CMD="pip3"
elif command -v python &> /dev/null; then
    PYTHON_CMD="python"
    PIP_CMD="pip"
else
    echo "❌ Error: Python 3 is not installed"
    echo "Please install Python 3.7+ first"
    exit 1
fi

PYTHON_VERSION=$($PYTHON_CMD --version 2>&1 | awk '{print $2}')
echo "✅ Found Python: $PYTHON_VERSION"
echo ""

# Install dependencies
echo "📦 Installing dependencies..."
if $PIP_CMD install -r requirements.txt --quiet 2>/dev/null; then
    echo "✅ Dependencies installed successfully"
else
    echo "⚠️  Using fallback installation..."
    $PIP_CMD install colorama requests --quiet 2>/dev/null || true
fi
echo ""

# Make executable
if [ -f "cursor_simple.py" ]; then
    chmod +x cursor_simple.py
    echo "✅ Made cursor_simple.py executable"
else
    echo "⚠️  cursor_simple.py not found in current directory"
fi
echo ""

# Installation complete
echo "╔═══════════════════════════════════════════════════════════╗"
echo "║                                                           ║"
echo "║                  ✅ Installation Complete!               ║"
echo "║                                                           ║"
echo "╚═══════════════════════════════════════════════════════════╝"
echo ""
echo "To run:"
echo "  $PYTHON_CMD cursor_simple.py"
echo ""
echo "Or:"
echo "  ./cursor_simple.py"
echo ""


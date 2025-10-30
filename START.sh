#!/bin/bash
#
# Cursor Simple - Quick Start for Linux/macOS
# Just run: ./START.sh
#

set -e

echo "╔═══════════════════════════════════════════════════════════╗"
echo "║                                                           ║"
echo "║           🚀 Cursor Simple - Quick Start 🚀              ║"
echo "║                                                           ║"
echo "╚═══════════════════════════════════════════════════════════╝"
echo ""

# Detect Python command
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

# Check if dependencies are installed
if ! $PYTHON_CMD -c "import colorama, requests" &> /dev/null; then
    echo "📦 First time setup - installing dependencies..."
    echo ""
    
    if $PIP_CMD install -r requirements.txt --quiet 2>/dev/null; then
        echo "✅ Dependencies installed!"
    else
        echo "⚠️  Using fallback installation..."
        $PIP_CMD install colorama requests --quiet 2>/dev/null || true
    fi
    echo ""
fi

# Make executable if not already
if [ -f "cursor_simple.py" ] && [ ! -x "cursor_simple.py" ]; then
    chmod +x cursor_simple.py
fi

# Run the tool
echo "🚀 Starting Cursor Simple..."
echo ""
$PYTHON_CMD cursor_simple.py

echo ""
echo "╔═══════════════════════════════════════════════════════════╗"
echo "║                      Finished!                            ║"
echo "╚═══════════════════════════════════════════════════════════╝"


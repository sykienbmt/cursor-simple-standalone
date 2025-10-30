#!/bin/bash
#
# Cursor Simple - Quick Start
# Usage: curl -fsSL https://raw.githubusercontent.com/sykienbmt/cursor-simple-standalone/HEAD/scripts/start.sh | bash
#

set -e

# Configuration
REPO_URL="https://raw.githubusercontent.com/sykienbmt/cursor-simple-standalone/HEAD"
TEMP_DIR="/tmp/cursor-simple-temp"

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

print_success() {
    echo -e "${GREEN}✅ $1${NC}"
}

print_info() {
    echo -e "${CYAN}ℹ️  $1${NC}"
}

print_error() {
    echo -e "${RED}❌ $1${NC}"
}

# Cleanup on exit
cleanup() {
    if [ -d "$TEMP_DIR" ]; then
        rm -rf "$TEMP_DIR"
    fi
}
trap cleanup EXIT

# Header
echo ""
echo -e "${GREEN}╔═══════════════════════════════════════════════════════════╗${NC}"
echo -e "${GREEN}║                                                           ║${NC}"
echo -e "${GREEN}║           🚀 Cursor Simple - Quick Start 🚀              ║${NC}"
echo -e "${GREEN}║                                                           ║${NC}"
echo -e "${GREEN}╚═══════════════════════════════════════════════════════════╝${NC}"
echo ""

# Check Python
print_info "Checking Python..."

if command -v python3 &> /dev/null; then
    PYTHON_CMD="python3"
    PIP_CMD="pip3"
elif command -v python &> /dev/null; then
    PYTHON_CMD="python"
    PIP_CMD="pip"
else
    print_error "Python not installed!"
    print_info "Install with: curl -fsSL https://raw.githubusercontent.com/sykienbmt/cursor-simple-standalone/HEAD/scripts/install.sh | bash"
    exit 1
fi

PYTHON_VERSION=$($PYTHON_CMD --version 2>&1 | awk '{print $2}')
print_success "Found Python: $PYTHON_VERSION"

# Create temp directory
rm -rf "$TEMP_DIR"
mkdir -p "$TEMP_DIR"

# Download files
print_info "Downloading Cursor Simple..."
curl -fsSL "$REPO_URL/cursor_simple.py" -o "$TEMP_DIR/cursor_simple.py"
curl -fsSL "$REPO_URL/requirements.txt" -o "$TEMP_DIR/requirements.txt"

print_success "Downloaded!"

# Install dependencies
print_info "Checking dependencies..."
$PIP_CMD install -q -r "$TEMP_DIR/requirements.txt" 2>/dev/null || true

# Make executable
chmod +x "$TEMP_DIR/cursor_simple.py"

# Run
echo ""
echo -e "${CYAN}🚀 Starting Cursor Simple...${NC}"
echo ""

cd "$TEMP_DIR"
$PYTHON_CMD cursor_simple.py < /dev/tty


#!/bin/bash
#
# Cursor Simple Standalone - One-Click Installer
# Usage: curl -fsSL https://raw.githubusercontent.com/sykienbmt/cursor-simple-standalone/HEAD/scripts/install.sh | bash
#

set -e

# Configuration
REPO_URL="https://raw.githubusercontent.com/sykienbmt/cursor-simple-standalone/HEAD"
INSTALL_DIR="$HOME/cursor-simple-standalone"
FILES=(
    "cursor_simple.py"
    "requirements.txt"
    "START.sh"
    "START.bat"
    "install.sh"
    "install.bat"
    "README.md"
    "QUICKSTART.md"
    "LICENSE"
)

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

# Helper functions
print_header() {
    echo ""
    echo -e "${GREEN}╔═══════════════════════════════════════════════════════════╗${NC}"
    echo -e "${GREEN}║                                                           ║${NC}"
    echo -e "${GREEN}║        🚀 Cursor Simple - One-Click Installer 🚀         ║${NC}"
    echo -e "${GREEN}║                                                           ║${NC}"
    echo -e "${GREEN}╚═══════════════════════════════════════════════════════════╝${NC}"
    echo ""
}

print_success() {
    echo -e "${GREEN}✅ $1${NC}"
}

print_info() {
    echo -e "${CYAN}ℹ️  $1${NC}"
}

print_error() {
    echo -e "${RED}❌ $1${NC}"
}

print_warning() {
    echo -e "${YELLOW}⚠️  $1${NC}"
}

# Detect OS
detect_os() {
    OS="$(uname -s)"
    case "${OS}" in
        Linux*)     OS_NAME="Linux";;
        Darwin*)    OS_NAME="macOS";;
        *)          OS_NAME="Unknown";;
    esac
    print_info "Detected OS: ${OS_NAME}"
}

# Check Python
check_python() {
    print_info "Step 1/4: Checking Python..."
    
    if command -v python3 &> /dev/null; then
        PYTHON_CMD="python3"
        PIP_CMD="pip3"
    elif command -v python &> /dev/null; then
        PYTHON_CMD="python"
        PIP_CMD="pip"
    else
        print_error "Python 3 is not installed"
        print_info "Please install Python 3.7+ first:"
        
        if [ "$OS_NAME" = "macOS" ]; then
            print_info "  brew install python3"
        elif [ "$OS_NAME" = "Linux" ]; then
            print_info "  sudo apt install python3 python3-pip  # Debian/Ubuntu"
            print_info "  sudo yum install python3 python3-pip  # CentOS/RHEL"
        fi
        
        exit 1
    fi
    
    PYTHON_VERSION=$($PYTHON_CMD --version 2>&1 | awk '{print $2}')
    print_success "Found Python: $PYTHON_VERSION"
}

# Create installation directory
setup_directory() {
    print_info "Step 2/4: Setting up installation directory..."
    
    if [ -d "$INSTALL_DIR" ]; then
        print_warning "Directory exists: $INSTALL_DIR"
        print_info "Cleaning old installation..."
        rm -rf "$INSTALL_DIR"
    fi
    
    mkdir -p "$INSTALL_DIR"
    print_success "Created: $INSTALL_DIR"
}

# Download files
download_files() {
    print_info "Step 3/4: Downloading files from GitHub..."
    
    for file in "${FILES[@]}"; do
        url="$REPO_URL/$file"
        dest="$INSTALL_DIR/$file"
        
        print_info "  Downloading: $file"
        if curl -fsSL "$url" -o "$dest"; then
            print_success "  ✓ $file"
        else
            print_warning "  ⚠️  Failed to download $file (optional)"
        fi
    done
    
    # Make scripts executable
    if [ -f "$INSTALL_DIR/cursor_simple.py" ]; then
        chmod +x "$INSTALL_DIR/cursor_simple.py"
    fi
    if [ -f "$INSTALL_DIR/START.sh" ]; then
        chmod +x "$INSTALL_DIR/START.sh"
    fi
    if [ -f "$INSTALL_DIR/install.sh" ]; then
        chmod +x "$INSTALL_DIR/install.sh"
    fi
}

# Install dependencies
install_dependencies() {
    print_info "Step 4/4: Installing Python dependencies..."
    
    if [ -f "$INSTALL_DIR/requirements.txt" ]; then
        if $PIP_CMD install -q -r "$INSTALL_DIR/requirements.txt" 2>/dev/null; then
            print_success "Dependencies installed!"
        else
            print_warning "Dependency installation failed, but tool may still work"
            # Fallback: install directly
            $PIP_CMD install -q colorama requests 2>/dev/null || true
        fi
    else
        # Fallback: install directly
        if $PIP_CMD install -q colorama requests 2>/dev/null; then
            print_success "Dependencies installed!"
        else
            print_warning "Could not install dependencies, but tool may still work"
        fi
    fi
}

# Main installation
main() {
    print_header
    
    detect_os
    echo ""
    
    check_python
    echo ""
    
    setup_directory
    echo ""
    
    download_files
    echo ""
    
    install_dependencies
    echo ""
    
    # Installation complete
    echo ""
    echo -e "${GREEN}╔═══════════════════════════════════════════════════════════╗${NC}"
    echo -e "${GREEN}║                                                           ║${NC}"
    echo -e "${GREEN}║              ✅ Installation Complete! ✅                 ║${NC}"
    echo -e "${GREEN}║                                                           ║${NC}"
    echo -e "${GREEN}╚═══════════════════════════════════════════════════════════╝${NC}"
    echo ""
    
    print_info "Installation directory: $INSTALL_DIR"
    echo ""
    echo -e "${CYAN}To run Cursor Simple:${NC}"
    echo ""
    echo -e "${YELLOW}  cd \"$INSTALL_DIR\"${NC}"
    echo -e "${YELLOW}  $PYTHON_CMD cursor_simple.py${NC}"
    echo ""
    echo -e "${YELLOW}Or:${NC}"
    echo -e "${YELLOW}  $INSTALL_DIR/START.sh${NC}"
    echo ""
    
    # Ask to run now
    echo ""
    read -p "Do you want to run Cursor Simple now? (Y/n) " -n 1 -r
    echo ""
    if [[ $REPLY =~ ^[Yy]$ ]] || [[ -z $REPLY ]]; then
        print_info "Starting Cursor Simple..."
        echo ""
        cd "$INSTALL_DIR"
        $PYTHON_CMD cursor_simple.py
    fi
}

# Run main function
main


#
# Cursor Simple Standalone - One-Click Installer (PowerShell)
# Usage: irm https://raw.githubusercontent.com/sykienbmt/cursor-simple-standalone/HEAD/scripts/install.ps1 | iex
#

$ErrorActionPreference = "Stop"

# Configuration
$REPO_URL = "https://raw.githubusercontent.com/sykienbmt/cursor-simple-standalone/HEAD"
$INSTALL_DIR = "$env:USERPROFILE\cursor-simple-standalone"
$FILES = @(
    "cursor_simple.py",
    "requirements.txt",
    "START.bat",
    "START.sh",
    "install.bat",
    "install.sh",
    "README.md",
    "QUICKSTART.md",
    "LICENSE"
)

# Colors
function Write-ColorOutput($ForegroundColor) {
    $fc = $host.UI.RawUI.ForegroundColor
    $host.UI.RawUI.ForegroundColor = $ForegroundColor
    if ($args) {
        Write-Output $args
    }
    $host.UI.RawUI.ForegroundColor = $fc
}

function Write-Header {
    Write-Host ""
    Write-ColorOutput Green "╔═══════════════════════════════════════════════════════════╗"
    Write-ColorOutput Green "║                                                           ║"
    Write-ColorOutput Green "║        🚀 Cursor Simple - One-Click Installer 🚀         ║"
    Write-ColorOutput Green "║                                                           ║"
    Write-ColorOutput Green "╚═══════════════════════════════════════════════════════════╝"
    Write-Host ""
}

function Write-Success {
    param($Message)
    Write-ColorOutput Green "✅ $Message"
}

function Write-Info {
    param($Message)
    Write-ColorOutput Cyan "ℹ️  $Message"
}

function Write-Error {
    param($Message)
    Write-ColorOutput Red "❌ $Message"
}

function Write-Warning {
    param($Message)
    Write-ColorOutput Yellow "⚠️  $Message"
}

# Main Installation
try {
    Write-Header
    
    # Step 1: Check/Install Python
    Write-Info "Step 1/4: Checking Python..."
    
    $pythonCmd = $null
    foreach ($cmd in @("py", "python", "python3")) {
        try {
            $version = & $cmd --version 2>&1
            if ($LASTEXITCODE -eq 0) {
                $pythonCmd = $cmd
                Write-Success "Found Python: $version"
                break
            }
        } catch {
            continue
        }
    }
    
    if (-not $pythonCmd) {
        Write-Warning "Python not found! Attempting auto-install..."
        
        # Try winget (Windows 10/11)
        if (Get-Command winget -ErrorAction SilentlyContinue) {
            Write-Info "Installing Python via winget..."
            try {
                winget install -e --id Python.Python.3.11 --silent --accept-package-agreements --accept-source-agreements
                Write-Success "Python installed! Please restart PowerShell and run the installer again."
                Write-Info "Or run manually: cd $INSTALL_DIR && python cursor_simple.py"
                exit 0
            } catch {
                Write-Warning "Winget installation failed."
            }
        }
        
        # Fallback: Open download page
        Write-Error "Please install Python manually:"
        Write-Info "Opening Python download page..."
        Start-Process "https://www.python.org/downloads/"
        Write-Info "After installation, run this script again."
        exit 1
    }
    
    # Step 2: Create installation directory
    Write-Info "Step 2/4: Setting up installation directory..."
    
    if (Test-Path $INSTALL_DIR) {
        Write-Warning "Directory exists: $INSTALL_DIR"
        Write-Info "Cleaning old installation..."
        Remove-Item -Path $INSTALL_DIR -Recurse -Force
    }
    
    New-Item -ItemType Directory -Path $INSTALL_DIR -Force | Out-Null
    Write-Success "Created: $INSTALL_DIR"
    
    # Step 3: Download files
    Write-Info "Step 3/4: Downloading files from GitHub..."
    
    foreach ($file in $FILES) {
        $url = "$REPO_URL/$file"
        $dest = Join-Path $INSTALL_DIR $file
        
        try {
            Write-Info "  Downloading: $file"
            Invoke-WebRequest -Uri $url -OutFile $dest -UseBasicParsing
            Write-Success "  ✓ $file"
        } catch {
            Write-Warning "  ⚠️  Failed to download $file (optional)"
        }
    }
    
    # Step 4: Install dependencies
    Write-Info "Step 4/4: Installing Python dependencies..."
    
    $requirementsPath = Join-Path $INSTALL_DIR "requirements.txt"
    if (Test-Path $requirementsPath) {
        try {
            & $pythonCmd -m pip install -q --upgrade pip 2>&1 | Out-Null
            & $pythonCmd -m pip install -q -r $requirementsPath
            Write-Success "Dependencies installed!"
        } catch {
            Write-Warning "Dependency installation failed, but tool may still work"
        }
    } else {
        # Fallback: install directly
        try {
            & $pythonCmd -m pip install -q colorama requests
            Write-Success "Dependencies installed!"
        } catch {
            Write-Warning "Could not install dependencies, but tool may still work"
        }
    }
    
    # Installation complete
    Write-Host ""
    Write-ColorOutput Green "╔═══════════════════════════════════════════════════════════╗"
    Write-ColorOutput Green "║                                                           ║"
    Write-ColorOutput Green "║              ✅ Installation Complete! ✅                 ║"
    Write-ColorOutput Green "║                                                           ║"
    Write-ColorOutput Green "╚═══════════════════════════════════════════════════════════╝"
    Write-Host ""
    
    Write-Info "Installation directory: $INSTALL_DIR"
    Write-Host ""
    Write-ColorOutput Cyan "To run Cursor Simple:"
    Write-Host ""
    Write-ColorOutput Yellow "  cd `"$INSTALL_DIR`""
    Write-ColorOutput Yellow "  $pythonCmd cursor_simple.py"
    Write-Host ""
    Write-ColorOutput Yellow "Or double-click: $INSTALL_DIR\START.bat"
    Write-Host ""
    
    # Ask to run now
    Write-Host ""
    $response = Read-Host "Do you want to run Cursor Simple now? (Y/n)"
    if ($response -eq "" -or $response -eq "Y" -or $response -eq "y") {
        Write-Info "Starting Cursor Simple..."
        Write-Host ""
        Set-Location $INSTALL_DIR
        & $pythonCmd cursor_simple.py
    }
    
} catch {
    Write-Host ""
    Write-Error "Installation failed: $_"
    Write-Info "Please try manual installation:"
    Write-Info "  1. Download files from GitHub"
    Write-Info "  2. Run: pip install colorama requests"
    Write-Info "  3. Run: python cursor_simple.py"
    exit 1
}


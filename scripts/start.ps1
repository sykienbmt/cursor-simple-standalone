#
# Cursor Simple - Quick Start (PowerShell)
# Usage: irm https://raw.githubusercontent.com/sykienbmt/cursor-simple-standalone/HEAD/scripts/start.ps1 | iex
#

$ErrorActionPreference = "Stop"

# Configuration
$REPO_URL = "https://raw.githubusercontent.com/sykienbmt/cursor-simple-standalone/HEAD"
$TEMP_DIR = "$env:TEMP\cursor-simple-temp"

# Colors
function Write-ColorOutput($ForegroundColor) {
    $fc = $host.UI.RawUI.ForegroundColor
    $host.UI.RawUI.ForegroundColor = $ForegroundColor
    if ($args) {
        Write-Output $args
    }
    $host.UI.RawUI.ForegroundColor = $fc
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

try {
    Write-Host ""
    Write-ColorOutput Green "╔═══════════════════════════════════════════════════════════╗"
    Write-ColorOutput Green "║                                                           ║"
    Write-ColorOutput Green "║           🚀 Cursor Simple - Quick Start 🚀              ║"
    Write-ColorOutput Green "║                                                           ║"
    Write-ColorOutput Green "╚═══════════════════════════════════════════════════════════╝"
    Write-Host ""
    
    # Check Python
    Write-Info "Checking Python..."
    
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
        Write-Error "Python not installed!"
        Write-Info "Install with: irm https://raw.githubusercontent.com/sykienbmt/cursor-simple-standalone/HEAD/scripts/install.ps1 | iex"
        exit 1
    }
    
    # Create temp directory
    if (Test-Path $TEMP_DIR) {
        Remove-Item -Path $TEMP_DIR -Recurse -Force
    }
    New-Item -ItemType Directory -Path $TEMP_DIR -Force | Out-Null
    
    # Download main script
    Write-Info "Downloading Cursor Simple..."
    $scriptPath = Join-Path $TEMP_DIR "cursor_simple.py"
    $requirementsPath = Join-Path $TEMP_DIR "requirements.txt"
    
    Invoke-WebRequest -Uri "$REPO_URL/cursor_simple.py" -OutFile $scriptPath -UseBasicParsing
    Invoke-WebRequest -Uri "$REPO_URL/requirements.txt" -OutFile $requirementsPath -UseBasicParsing
    
    Write-Success "Downloaded!"
    
    # Install dependencies quietly
    Write-Info "Checking dependencies..."
    & $pythonCmd -m pip install -q -r $requirementsPath 2>&1 | Out-Null
    
    # Run the tool
    Write-Host ""
    Write-ColorOutput Cyan "🚀 Starting Cursor Simple..."
    Write-Host ""
    
    Set-Location $TEMP_DIR
    & $pythonCmd cursor_simple.py
    
} catch {
    Write-Host ""
    Write-Error "Failed to start: $_"
    exit 1
} finally {
    # Cleanup
    if (Test-Path $TEMP_DIR) {
        Remove-Item -Path $TEMP_DIR -Recurse -Force -ErrorAction SilentlyContinue
    }
}


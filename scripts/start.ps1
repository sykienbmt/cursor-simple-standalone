#
# Cursor Simple - Quick Start (PowerShell)
# Usage: irm https://raw.githubusercontent.com/sykienbmt/cursor-simple-standalone/HEAD/scripts/start.ps1 | iex
#

$ErrorActionPreference = "Stop"

# Configuration
$REPO_URL = "https://raw.githubusercontent.com/sykienbmt/simple-standalone/HEAD"
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

function Write-Warning {
    param($Message)
    Write-ColorOutput Yellow "⚠️  $Message"
}

# Function to check if command exists
function Test-Command {
    param([string]$Command)
    return [bool](Get-Command $Command -ErrorAction SilentlyContinue)
}

# Function to install Python automatically
function Install-Python {
    Write-Warning "Python not installed. Installing automatically..."
    
    # Check winget
    if (Test-Command "winget") {
        Write-Info "Installing Python via winget..."
        try {
            winget install -e --id Python.Python.3.12 --silent --accept-package-agreements --accept-source-agreements
            # Refresh PATH
            $env:Path = [System.Environment]::GetEnvironmentVariable("Path","Machine") + ";" + [System.Environment]::GetEnvironmentVariable("Path","User")
            Write-Success "Python installed successfully!"
            return $true
        } catch {
            Write-Warning "Could not install via winget, trying another method..."
        }
    }
    
    # If winget not available, download and install Python manually
    Write-Info "Downloading Python installer..."
    $pythonUrl = "https://www.python.org/ftp/python/3.12.0/python-3.12.0-amd64.exe"
    $pythonInstaller = "$env:TEMP\python-installer.exe"
    
    try {
        # Download Python installer
        Invoke-WebRequest -Uri $pythonUrl -OutFile $pythonInstaller -UseBasicParsing
        
        Write-Info "Installing Python (may take a few minutes)..."
        # Install Python with pip and add to PATH
        Start-Process -FilePath $pythonInstaller -ArgumentList "/quiet", "InstallAllUsers=0", "PrependPath=1", "Include_pip=1" -Wait
        
        # Refresh PATH
        $env:Path = [System.Environment]::GetEnvironmentVariable("Path","Machine") + ";" + [System.Environment]::GetEnvironmentVariable("Path","User")
        
        # Clean up installer
        Remove-Item $pythonInstaller -Force
        
        Write-Success "Python installed successfully!"
        return $true
    } catch {
        Write-Error "Could not install Python automatically: $_"
        Write-Info "Please install Python manually from: https://www.python.org/downloads/"
        Write-Warning "Note: Make sure to check 'Add Python to PATH' during installation!"
        exit 1
    }
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
        Write-Warning "Python not found!"
        Install-Python
        Start-Sleep -Seconds 2
        
        # Check again after installation
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
        
        # If still not found
        if (-not $pythonCmd) {
            Write-Error "Python installation failed or not ready!"
            Write-Info "Please restart PowerShell and try again, or install manually from: https://www.python.org/downloads/"
            exit 1
        }
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
    
    # Install dependencies with better error handling
    Write-Info "Checking dependencies..."
    try {
        # Try to upgrade pip first
        & $pythonCmd -m pip install --upgrade pip --quiet 2>&1 | Out-Null
        
        # Install from requirements.txt with retry logic
        $retryCount = 0
        $maxRetries = 3
        $success = $false
        
        while ($retryCount -lt $maxRetries -and -not $success) {
            try {
                $output = & $pythonCmd -m pip install -r $requirementsPath --no-cache-dir 2>&1
                $exitCode = $LASTEXITCODE
                
                if ($exitCode -eq 0) {
                    $success = $true
                    Write-Success "Dependencies installed successfully!"
                } else {
                    throw "pip install failed with exit code: $exitCode"
                }
            } catch {
                $retryCount++
                if ($retryCount -lt $maxRetries) {
                    Write-Warning "Retrying... (attempt $retryCount/$maxRetries)"
                    Start-Sleep -Seconds 2
                }
            }
        }
        
        # Try with --user flag if standard install failed
        if (-not $success) {
            Write-Warning "Trying with --user flag..."
            $output = & $pythonCmd -m pip install --user -r $requirementsPath --no-cache-dir 2>&1
            if ($LASTEXITCODE -eq 0) {
                Write-Success "Dependencies installed successfully!"
                $success = $true
            }
        }
        
        if (-not $success) {
            throw "Could not install dependencies after $maxRetries attempts"
        }
    } catch {
        Write-Error "Failed to install dependencies: $_"
        Write-Info "You can try manually: cd $TEMP_DIR ; pip install -r requirements.txt"
        exit 1
    }
    
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


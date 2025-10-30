@echo off
REM Cursor Simple - Installation Script
REM For Windows

REM Change to script directory
cd /d "%~dp0"

echo ================================================================
echo.
echo            Cursor Simple - Installer
echo.
echo ================================================================
echo.

REM === Check Python Installation ===
set PYTHON_CMD=

REM Try py launcher first (recommended for Windows)
py --version >nul 2>&1
if %errorlevel% equ 0 (
    set PYTHON_CMD=py
    goto :python_found
)

REM Try python command
python --version >nul 2>&1
if %errorlevel% equ 0 (
    set PYTHON_CMD=python
    goto :python_found
)

REM Try python3 command
python3 --version >nul 2>&1
if %errorlevel% equ 0 (
    set PYTHON_CMD=python3
    goto :python_found
)

REM Python not found - Try to install automatically
echo ================================================================
echo.
echo    ⚠️  Python not found! Attempting auto-install...
echo.
echo ================================================================
echo.

REM Try winget first (Windows 10/11)
echo Checking for winget...
winget --version >nul 2>&1
if %errorlevel% equ 0 (
    echo ✓ Found winget! Installing Python automatically...
    echo.
    echo This may take a few minutes...
    winget install -e --id Python.Python.3.11 --silent --accept-package-agreements --accept-source-agreements
    
    if %errorlevel% equ 0 (
        echo.
        echo ================================================================
        echo.
        echo    ✅ Python installed successfully via winget!
        echo.
        echo ================================================================
        echo.
        echo Restarting script to apply changes...
        timeout /t 3 /nobreak >nul
        
        REM Restart this script in a new command prompt
        start "" "%~f0"
        exit /b 0
    ) else (
        echo.
        echo ⚠️  Auto-install failed. Trying direct download...
        echo.
    )
)

REM Winget not available - Try direct download and install
echo Winget not available. Downloading Python installer...
echo.

REM Create temp directory
set TEMP_DIR=%TEMP%\cursor_python_install
if not exist "%TEMP_DIR%" mkdir "%TEMP_DIR%"

REM Download Python installer using PowerShell
echo Downloading Python 3.11.9 (this may take a few minutes)...
powershell -Command "& {[Net.ServicePointManager]::SecurityProtocol = [Net.SecurityProtocolType]::Tls12; Invoke-WebRequest -Uri 'https://www.python.org/ftp/python/3.11.9/python-3.11.9-amd64.exe' -OutFile '%TEMP_DIR%\python-installer.exe'}"

if exist "%TEMP_DIR%\python-installer.exe" (
    echo.
    echo ✓ Download complete! Installing Python...
    echo.
    echo This will install Python with:
    echo   - Add to PATH automatically (PrependPath=1)
    echo   - Install pip automatically
    echo   - For all users
    echo.
    
    REM Run installer silently with all necessary options
    echo Installing... (this may take 1-2 minutes)
    "%TEMP_DIR%\python-installer.exe" /quiet InstallAllUsers=1 PrependPath=1 Include_pip=1
    
    REM Wait for installation to complete
    timeout /t 5 /nobreak >nul
    
    echo.
    echo ================================================================
    echo.
    echo    ✅ Python installation completed!
    echo    ✅ Python added to PATH automatically
    echo.
    echo ================================================================
    echo.
    echo Cleaning up and restarting script...
    
    REM Cleanup
    del "%TEMP_DIR%\python-installer.exe" 2>nul
    rmdir "%TEMP_DIR%" 2>nul
    
    timeout /t 2 /nobreak >nul
    
    REM Restart this script in a new command prompt (will have new PATH)
    start "" "%~f0"
    exit /b 0
) else (
    echo.
    echo ❌ Download failed! Opening browser for manual download...
    start https://www.python.org/downloads/
    echo.
    echo ================================================================
    echo.
    echo    📥 Please install Python manually:
    echo.
    echo    1. Download from the opened browser page
    echo    2. Run the installer
    echo    3. ✅ CHECK "Add Python to PATH" (Important!)
    echo    4. Complete installation
    echo    5. Close this window and run install.bat again
    echo.
    echo    Minimum version: Python 3.7+
    echo.
    echo ================================================================
    echo.
    pause
    exit /b 1
)

:python_found
echo Found Python:
%PYTHON_CMD% --version
echo.

REM === Check and upgrade pip ===
%PYTHON_CMD% -m pip --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ================================================================
    echo.
    echo    ⚠️  WARNING: pip is not installed!
    echo.
    echo ================================================================
    echo.
    echo Installing pip...
    %PYTHON_CMD% -m ensurepip --default-pip
    echo.
) else (
    REM Upgrade pip silently to avoid warnings
    echo Upgrading pip...
    %PYTHON_CMD% -m pip install --upgrade pip --quiet --no-warn-script-location >nul 2>&1
    echo.
)

REM === Install dependencies ===
echo Installing dependencies...
%PYTHON_CMD% -m pip install -r requirements.txt --no-warn-script-location >nul 2>&1
if %errorlevel% equ 0 (
    echo ✓ Dependencies installed successfully
) else (
    echo ! Using fallback installation...
    %PYTHON_CMD% -m pip install colorama requests --no-warn-script-location >nul 2>&1
    if %errorlevel% equ 0 (
        echo ✓ Dependencies installed successfully
    ) else (
        echo ❌ Failed to install dependencies!
        echo.
        echo Please try manually:
        echo    %PYTHON_CMD% -m pip install colorama requests
        echo.
        pause
        exit /b 1
    )
)
echo.

REM === Installation complete ===
echo ================================================================
echo.
echo                Installation Complete!
echo.
echo ================================================================
echo.
echo To run:
echo   START.bat  (recommended)
echo   or
echo   %PYTHON_CMD% cursor_simple.py
echo.
pause


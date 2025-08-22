@echo off
setlocal enabledelayedexpansion

echo 🚀 Starting Flask app packaging...
echo Current directory: %CD%
echo.

REM Check if conda is available
echo Checking conda availability...
where conda >nul 2>nul
if errorlevel 1 (
    echo ❌ Conda not found in PATH
    echo Please ensure conda is installed and in your PATH
    pause
    exit /b 1
)
echo ✅ Conda found

REM Check if environment exists
echo Checking if py_flask_trade environment exists...
conda env list | findstr "py_flask_trade" >nul
if errorlevel 1 (
    echo ❌ Environment 'py_flask_trade' not found
    echo Please run setup_conda.sh first
    pause
    exit /b 1
)
echo ✅ Environment py_flask_trade found

REM Get conda base path
for /f "tokens=*" %%i in ('conda info --base') do set CONDA_BASE=%%i
echo Conda base path: %CONDA_BASE%

REM Check if PyInstaller is installed in the environment
echo Checking PyInstaller installation...
call "%CONDA_BASE%\Scripts\activate.bat" py_flask_trade
python -c "import PyInstaller" 2>nul
if errorlevel 1 (
    echo ❌ PyInstaller not installed in py_flask_trade environment
    echo Installing PyInstaller...
    python -m pip install pyinstaller
    if errorlevel 1 (
        echo ❌ Failed to install PyInstaller
        pause
        exit /b 1
    )
    echo ✅ PyInstaller installed successfully
) else (
    echo ✅ PyInstaller already installed
)

REM Create necessary directories
echo Creating necessary directories...
if not exist "logs" (
    mkdir logs
    echo ✅ Created logs directory
)
if not exist "data" (
    mkdir data
    echo ✅ Created data directory
)

REM Create local config file if not exists
if not exist ".env" (
    echo ⚙️ Creating local environment config...
    (
        echo SQLALCHEMY_DATABASE_URI = 'sqlite:///./lincms_local.db'
        echo SECRET_KEY = 'local_development_secret_key_2024'
        echo REDIS_URL = "redis://:iphone5C,.@115.159.204.224:6020/2"
        echo REDIS_SUB = "diff_buy,diff_sell,diff_cancel,diff_search"
        echo ENV = "local"
        echo DEBUG = True
        echo FLASK_APP = "starter:app"
        echo FLASK_ENV = "local"
        echo FLASK_DEBUG = True
    ) > .env
    echo ✅ Created .env file
)

REM Check if spec file exists
if not exist "pyinstaller_config.spec" (
    echo ❌ pyinstaller_config.spec not found
    echo Please ensure you're in the project root directory
    echo Current directory: %CD%
    pause
    exit /b 1
)
echo ✅ Found pyinstaller_config.spec

REM Clean previous builds
echo 🧹 Cleaning previous build files...
if exist "build" (
    rmdir /s /q build
    echo ✅ Removed build directory
)
if exist "dist" (
    rmdir /s /q dist
    echo ✅ Removed dist directory
)
if exist "__pycache__" (
    rmdir /s /q __pycache__
    echo ✅ Removed __pycache__ directory
)

REM Start packaging using activated environment
echo.
echo 📦 Starting packaging...
echo This may take several minutes...
echo.

REM Ensure we're still in the correct environment
call "%CONDA_BASE%\Scripts\activate.bat" py_flask_trade
python -m PyInstaller pyinstaller_config.spec
set PACKAGE_RESULT=%errorlevel%

if %PACKAGE_RESULT% neq 0 (
    echo.
    echo ❌ Packaging failed with error code: %PACKAGE_RESULT%
    echo Please check the error messages above
    pause
    exit /b 1
)

REM Check packaging result
echo.
echo Checking packaging result...
if exist "dist\flask_cms_app.exe" (
    echo ✅ Packaging successful!
    echo 📍 Executable location: dist\flask_cms_app.exe
    echo 📁 File size: 
    dir "dist\flask_cms_app.exe" | findstr "flask_cms_app.exe"
    echo.
    echo 🔧 Usage:
    echo 1. Go to dist directory: cd dist
    echo 2. Run program: flask_cms_app.exe
    echo 3. Access URL: http://127.0.0.1:5000
    echo.
    echo 🎉 Build completed successfully!
) else (
    echo ❌ Packaging failed - executable not found
    echo Please check error messages above
    echo.
    echo Checking dist directory contents:
    if exist "dist" (
        dir dist
    ) else (
        echo dist directory does not exist
    )
    pause
    exit /b 1
)

echo.
echo Press any key to exit...
pause >nul 
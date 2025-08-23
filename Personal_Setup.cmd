@echo off
echo =========================================
echo    One-Click Personal Windows Setup
echo =========================================

:: ========================
:: 1. Steam (winget silent)
:: ========================
echo Installing Steam...
winget install --id Valve.Steam --exact --silent

:: ========================
:: 2. Floorp (winget silent)
:: ========================
echo Installing Floorp...
winget install --id=Ablaze.Floorp -e --silent

:: ========================
:: 3. GitHub Desktop (MSI silent)
:: ========================
echo Downloading GitHub Desktop...
powershell -Command "Invoke-WebRequest -Uri 'https://central.github.com/deployments/desktop/desktop/latest/win32?format=msi' -OutFile '%USERPROFILE%\Downloads\GitHubDesktop.msi'"
echo Installing GitHub Desktop silently...
msiexec /i "%USERPROFILE%\Downloads\GitHubDesktop.msi" /quiet /norestart

:: ========================
:: 4. Discord (winget silent)
:: ========================
echo Downloading Discord...
winget install --id=Discord.Discord -e --silent

:: ========================
:: 5. Bloxstrap (winget silent)
:: ========================
echo Installing Bloxstrap...
winget install --id=pizzaboxer.Bloxstrap -e --silent

:: ========================
:: 6. PrismLauncher (winget silent)
:: ========================
echo Installing PrismLauncher...
winget install --id=PrismLauncher.PrismLauncher -e --silent

:: ========================
:: Optional: Clean up downloaded installers
:: ========================
echo Cleaning up downloaded installers...
del "%USERPROFILE%\Downloads\GitHubDesktop.msi" /f /q

echo =========================================
echo All apps installed successfully!
echo =========================================
pause

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
:: 3. GitHub Desktop (winget silent)
:: ========================
echo Installing GitHub Desktop...
winget install --id=GitHub.GitHubDesktop -e --silent

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

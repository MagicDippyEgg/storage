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
:: 7. SVG Thumbnail Extension (winget silent)
:: ========================
echo Installing PrismLauncher...
winget install ThioJoe.SvgThumbnailExtension --silent

:: ========================
:: 8. Clean up downloaded installers
:: ========================
echo Cleaning up downloaded installers...
del "%USERPROFILE%\Downloads\GitHubDesktop.msi" /f /q

echo =========================================
echo All apps installed successfully!
echo =========================================

:: ========================
:: Change Personalization
:: ========================
echo Enabling Dark Mode
reg add "HKCU\Software\Microsoft\Windows\CurrentVersion\Themes\Personalize" /v AppsUseLightTheme /t REG_DWORD /d 0 /f
reg add "HKCU\Software\Microsoft\Windows\CurrentVersion\Themes\Personalize" /v SystemUsesLightTheme /t REG_DWORD /d 0 /f
echo Restarting explorer.exe
taskkill /f /im explorer.exe
start explorer.exe

echo =========================================
echo Personalization changed successfully!
echo =========================================

pause

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
echo Moving Task Bar
reg add "HKCU\Software\Microsoft\Windows\CurrentVersion\Explorer\StuckRects3" /v Settings /t REG_BINARY /d 2800000001000000010000000000000003000000000000000000000000000000 /f

echo =========================================
echo Personalization changed successfully!
echo =========================================

pause

@echo off
echo =========================================
echo    One-Click Personal Windows Setup
echo =========================================

:: ========================
:: 1. Steam (manual installer)
:: ========================
echo Downloading Steam...
powershell -Command "Invoke-WebRequest -Uri 'https://cdn.akamai.steamstatic.com/client/installer/SteamSetup.exe' -OutFile '%USERPROFILE%\Downloads\SteamSetup.exe'"
echo Running Steam installer (manual)...
start "" "%USERPROFILE%\Downloads\SteamSetup.exe"

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
:: 4. Discord (EXE silent)
:: ========================
echo Downloading Discord...
powershell -Command "Invoke-WebRequest -Uri 'https://discord.com/api/downloads/distributions/app/installers/latest?channel=stable&platform=win&arch=x64' -OutFile '%USERPROFILE%\Downloads\DiscordSetup.exe'"
echo Installing Discord silently...
start /wait "" "%USERPROFILE%\Downloads\DiscordSetup.exe" /S

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
del "%USERPROFILE%\Downloads\SteamSetup.exe" /f /q
del "%USERPROFILE%\Downloads\GitHubDesktop.msi" /f /q
del "%USERPROFILE%\Downloads\DiscordSetup.exe" /f /q

echo =========================================
echo All apps installed successfully!
echo =========================================
pause

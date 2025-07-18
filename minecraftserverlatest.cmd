@echo off
setlocal EnableDelayedExpansion
echo Checking for Minecraft server updates...

:: Download version manifest
curl -s -o manifest.json https://piston-meta.mojang.com/mc/game/version_manifest_v2.json

:: Get latest version ID
for /f "usebackq tokens=*" %%i in (`powershell -NoProfile -Command ^
  "(Get-Content 'manifest.json' | ConvertFrom-Json).latest.release"`) do set LATEST_VERSION=%%i

echo Latest version: %LATEST_VERSION%

:: Get version JSON URL
for /f "usebackq tokens=*" %%i in (`powershell -NoProfile -Command ^
  "(Get-Content 'manifest.json' | ConvertFrom-Json).versions | Where-Object { $_.id -eq '%LATEST_VERSION%' } | Select-Object -ExpandProperty url"`) do set VERSION_URL=%%i

:: Download version metadata
curl -s -o version.json %VERSION_URL%

:: Get download URL
for /f "usebackq tokens=*" %%i in (`powershell -NoProfile -Command ^
  "$v = Get-Content 'version.json' | ConvertFrom-Json; $v.downloads.server.url"`) do set SERVER_JAR_URL=%%i

:: Get SHA1 from Mojang
for /f "usebackq tokens=*" %%i in (`powershell -NoProfile -Command ^
  "((Get-Content 'version.json' | ConvertFrom-Json).downloads.server.sha1).ToUpper()"`) do set SERVER_JAR_SHA1=%%i

echo Mojang SHA1: %SERVER_JAR_SHA1%

:: Check local SHA1
set NEED_UPDATE=true
if exist server.jar (
    set "LOCAL_SHA1="
    for /f %%h in ('certutil -hashfile server.jar SHA1 ^| findstr /R "^[0-9A-Fa-f]*$"') do (
        set "LOCAL_SHA1=%%h"
    )

    :: Now convert and compare using delayed expansion
    for /f "usebackq tokens=*" %%i in (`powershell -NoProfile -Command ^
      "\"!LOCAL_SHA1!\".ToUpper()"`) do set LOCAL_SHA1_UPPER=%%i

    echo Local SHA1 : !LOCAL_SHA1_UPPER!

    if "!LOCAL_SHA1_UPPER!"=="%SERVER_JAR_SHA1%" (
        echo server.jar is already up to date.
        set NEED_UPDATE=false
    ) else (
        echo Local server.jar differs from latest release.
    )
) else (
    echo No server.jar found.
)

:: Download if needed
if "%NEED_UPDATE%"=="true" (
    echo Downloading updated server.jar...
    curl -o server.jar %SERVER_JAR_URL%
    echo server.jar updated to version %LATEST_VERSION%
)

:: Cleanup
del manifest.json
del version.json

echo Running server.jar
java -Xmx1024M -Xms1024M -jar server.jar
exit
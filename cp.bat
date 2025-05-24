@echo off
setlocal enabledelayedexpansion

:: Set the serial port and source folder
set PORT=COM5
set SOURCE_DIR=esp32_client

echo Connecting to %PORT% and copying files from %SOURCE_DIR%...

:: Loop through all files in the folder
for %%F in (%SOURCE_DIR%\*) do (
    echo Copying %%F...
    mpremote connect %PORT% cp "%%F" :
)

echo All files copied successfully.
pause

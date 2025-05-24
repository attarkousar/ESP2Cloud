@echo off

echo Remove connections of esp32. Make sure GPIO are not connected to anything
timeout /t 5 /nobreak > nul

setlocal

:: Configuration
set PORT=COM5
set BAUD=460800
set FIRMWARE=ESP32_GENERIC-20250415-v1.25.0.bin

echo Erasing flash on %PORT%...
esptool --port %PORT% erase_flash

echo Writing firmware to %PORT% at %BAUD% baud...
esptool --baud %BAUD% --port %PORT% write_flash 0x1000 %FIRMWARE%

echo Flash complete. Waiting for ESP32 to reboot...
timeout /t 5 /nobreak > nul

echo Done.
pause

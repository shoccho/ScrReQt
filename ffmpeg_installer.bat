@echo off
setlocal enabledelayedexpansion

set "ffmpeg_url=https://github.com/BtbN/FFmpeg-Builds/releases/download/latest/ffmpeg-master-latest-win64-gpl.zip"
set "download_folder=%~dp0ffmpeg"

echo Downloading FFmpeg...
mkdir "!download_folder!" 2>nul

powershell -command "Start-BitsTransfer -Source '!ffmpeg_url!' -Destination '!download_folder!'"

echo Installing FFmpeg...
powershell -command "Expand-Archive '!download_folder!\ffmpeg-master-latest-win64-gpl.zip' '!download_folder!'"

powershell -command "Move-Item -Path '!download_folder!\ffmpeg-master-latest-win64-gpl\bin\ffmpeg.exe' -Destination '!download_folder!'"

echo Cleaning up
powershell -command "Remove-Item -Path '!download_folder!\ffmpeg-master-latest-win64-gpl*' -Recurse"
echo FFmpeg installation complete.
pause

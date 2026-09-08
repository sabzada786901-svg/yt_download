1. Install required Python package
pip install pytubefix

2. Install FFmpeg
winget install Gyan.FFmpeg

3. check ffmpeg version
ffmpeg --version

4. if ffmpeg is not recognized like this type error
'ffmpeg' is not recognized as an internal or external command

5. so use this
dir "C:\Users\%USERNAME%\AppData\Local\Microsoft\WinGet\Packages" /s /b | findstr /i "ffmpeg.exe"

6. Run the downloader
python yt_download.py

from pytubefix import YouTube
import subprocess
import os

# FFmpeg ka exact path
FFMPEG = r"C:\Users\1\AppData\Local\Microsoft\WinGet\Packages\Gyan.FFmpeg_Microsoft.Winget.Source_8wekyb3d8bbwe\ffmpeg-9.0.1-full_build\bin\ffmpeg.exe"

# YouTube URL
link = input("Enter your video URL: ")

try:
    yt = YouTube(link)

    print("\nTitle:", yt.title)
    print("Downloading 720p video...")

    # 720p video stream
    video = (
        yt.streams
        .filter(adaptive=True, file_extension="mp4", res="720p")
        .first()
    )

    # Best MP4 audio
    audio = (
        yt.streams
        .filter(adaptive=True, mime_type="audio/mp4")
        .order_by("abr")
        .desc()
        .first()
    )

    # Agar 720p available na ho to 480p
    if not video:
        print("720p available nahi hai, 480p try kar raha hoon...")

        video = (
            yt.streams
            .filter(adaptive=True, file_extension="mp4", res="480p")
            .first()
        )

    if not video:
        print("❌ Video stream nahi mili.")
        exit()

    if not audio:
        print("❌ Audio stream nahi mili.")
        exit()

    print("Video:", video.resolution)
    print("Audio:", audio.abr)

    video_file = "video.mp4"
    audio_file = "audio.mp4"
    output_file = "youtube_video.mp4"

    # Download video
    print("\nDownloading video...")
    video.download(filename=video_file)

    # Download audio
    print("Downloading audio...")
    audio.download(filename=audio_file)

    # Merge
    print("Merging video + audio...")

    subprocess.run([
        FFMPEG,
        "-y",
        "-i", video_file,
        "-i", audio_file,
        "-c:v", "copy",
        "-c:a", "aac",
        output_file
    ], check=True)

    # Temporary files delete
    if os.path.exists(video_file):
        os.remove(video_file)

    if os.path.exists(audio_file):
        os.remove(audio_file)

    print("\n✅ Download complete!")
    print("Saved as:", output_file)

except Exception as e:
    print("\n❌ Error:", e)
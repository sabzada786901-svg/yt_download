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

    # Quality options
    print("\nAvailable Quality Options:")
    print("1. 360p")
    print("2. 480p")
    print("3. 720p")
    print("4. 1080p")

    choice = input("\nSelect quality (1-4): ")

    quality_map = {
        "1": "360p",
        "2": "480p",
        "3": "720p",
        "4": "1080p"
    }

    selected_quality = quality_map.get(choice)

    if not selected_quality:
        print("❌ Invalid choice!")
        exit()

    print(f"\nSelected Quality: {selected_quality}")
    print("Searching video stream...")

    # Requested quality
    video = (
        yt.streams
        .filter(
            adaptive=True,
            file_extension="mp4",
            res=selected_quality
        )
        .first()
    )

    # Agar selected quality available nahi hai
    if not video:

        print(f"⚠️ {selected_quality} available nahi hai.")

        # Available resolutions check karo
        available = []

        for stream in yt.streams:
            if (
                stream.type == "video"
                and stream.mime_type == "video/mp4"
                and stream.resolution
            ):
                if stream.resolution not in available:
                    available.append(stream.resolution)

        # Quality order
        quality_order = ["1080p", "720p", "480p", "360p"]

        # Lower available quality find karo
        selected_index = quality_order.index(selected_quality)

        for quality in quality_order[selected_index + 1:]:
            if quality in available:
                video = (
                    yt.streams
                    .filter(
                        adaptive=True,
                        file_extension="mp4",
                        res=quality
                    )
                    .first()
                )

                if video:
                    print(f"✅ {quality} available hai, ye download hogi.")
                    break

    if not video:
        print("❌ Suitable video stream nahi mili.")
        exit()

    # Best MP4 audio
    audio = (
        yt.streams
        .filter(
            adaptive=True,
            mime_type="audio/mp4"
        )
        .order_by("abr")
        .desc()
        .first()
    )

    if not audio:
        print("❌ Audio stream nahi mili.")
        exit()

    print("\nVideo:", video.resolution)
    print("Audio:", audio.abr)

    # Temporary files
    video_file = "video.mp4"
    audio_file = "audio.mp4"
    output_file = "youtube_video.mp4"

    # Download video
    print("\n📥 Downloading video...")
    video.download(filename=video_file)

    # Download audio
    print("📥 Downloading audio...")
    audio.download(filename=audio_file)

    # Merge video + audio
    print("\n🔄 Merging video + audio...")

    subprocess.run(
        [
            FFMPEG,
            "-y",
            "-i", video_file,
            "-i", audio_file,
            "-c:v", "copy",
            "-c:a", "aac",
            output_file
        ],
        check=True
    )

    # Temporary files delete
    if os.path.exists(video_file):
        os.remove(video_file)

    if os.path.exists(audio_file):
        os.remove(audio_file)

    print("\n✅ Download complete!")
    print("Saved as:", output_file)

except Exception as e:
    print("\n❌ Error:", e)
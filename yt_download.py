# ============================================================
# 🎬 YouTube Video Downloader
# ============================================================
#
# 📦 REQUIRED INSTALLATION
#
# Is program ko chalane se pehle VS Code Terminal mein
# ye commands run karein:
#
# 1️⃣ pytubefix install karein:
#    pip install pytubefix
#
# 2️⃣ FFmpeg install karein:
#    winget install Gyan.FFmpeg
#
# ⚠️ Agar FFmpeg already installed hai to dobara install
# karne ki zaroorat nahi.
#
# for checking
# 3️⃣ FFmpeg --version

# ager ffmpeg install ho giya hai or zip file hai to yeh use karo:
#dir "C:\Users\1\AppData\Local\Microsoft\WinGet\Packages" /s /b | findstr /i "ffmpeg.exe"
# ============================================================


from pytubefix import YouTube
import subprocess
import os


# ============================================================
# ⚙️ FFMPEG PATH
# ============================================================
#
# Ye path aapke computer par FFmpeg ka path hai.
#
# Agar kisi doosre computer par ye program use karna ho,
# to FFmpeg install karne ke baad us computer ka FFmpeg
# path yahan set karna hoga.
#
# ============================================================

FFMPEG = r"C:\Users\1\AppData\Local\Microsoft\WinGet\Packages\Gyan.FFmpeg_Microsoft.Winget.Source_8wekyb3d8bbwe\ffmpeg-9.0.1-full_build\bin\ffmpeg.exe"


# ============================================================
# 🔗 YOUTUBE VIDEO URL
# ============================================================

link = input("Enter your video URL: ")


try:

    # YouTube video information
    yt = YouTube(link)

    print("\nTitle:", yt.title)


    # ========================================================
    # 🎥 QUALITY OPTIONS
    # ========================================================

    print("\nAvailable Quality Options:")

    print("1. 360p")
    print("2. 480p")
    print("3. 720p")
    print("4. 1080p")


    choice = input("\nSelect quality (1-4): ")


    # User choice ko actual resolution mein convert karna
    quality_map = {

        "1": "360p",
        "2": "480p",
        "3": "720p",
        "4": "1080p"

    }


    selected_quality = quality_map.get(choice)


    # Agar user ne wrong option select ki
    if not selected_quality:

        print("❌ Invalid choice!")
        exit()


    print(f"\nSelected Quality: {selected_quality}")
    print("Searching video stream...")


    # ========================================================
    # 📹 REQUESTED VIDEO QUALITY
    # ========================================================

    video = (
        yt.streams
        .filter(
            adaptive=True,
            file_extension="mp4",
            res=selected_quality
        )
        .first()
    )


    # ========================================================
    # 🔄 AGAR SELECTED QUALITY AVAILABLE NA HO
    # ========================================================

    if not video:

        print(
            f"⚠️ {selected_quality} available nahi hai."
        )


        # Available resolutions check karna
        available = []


        for stream in yt.streams:

            if (
                stream.type == "video"
                and stream.mime_type == "video/mp4"
                and stream.resolution
            ):

                if stream.resolution not in available:

                    available.append(stream.resolution)


        # Quality priority
        quality_order = [
            "1080p",
            "720p",
            "480p",
            "360p"
        ]


        selected_index = quality_order.index(
            selected_quality
        )


        # Lower quality automatically find karna
        for quality in quality_order[
            selected_index + 1:
        ]:

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

                    print(
                        f"✅ {quality} available hai, "
                        "ye download hogi."
                    )

                    break


    # Agar koi video stream na mile
    if not video:

        print("❌ Suitable video stream nahi mili.")
        exit()


    # ========================================================
    # 🔊 BEST MP4 AUDIO
    # ========================================================

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


    # Agar audio stream na mile
    if not audio:

        print("❌ Audio stream nahi mili.")
        exit()


    print("\nVideo:", video.resolution)
    print("Audio:", audio.abr)


    # ========================================================
    # 📁 TEMPORARY FILES
    # ========================================================

    video_file = "video.mp4"
    audio_file = "audio.mp4"
    output_file = "youtube_video.mp4"


    # ========================================================
    # 📥 DOWNLOAD VIDEO
    # ========================================================

    print("\n📥 Downloading video...")

    video.download(
        filename=video_file
    )


    # ========================================================
    # 🔊 DOWNLOAD AUDIO
    # ========================================================

    print("📥 Downloading audio...")

    audio.download(
        filename=audio_file
    )


    # ========================================================
    # 🔄 MERGE VIDEO + AUDIO USING FFMPEG
    # ========================================================

    print("\n🔄 Merging video + audio...")


    subprocess.run(
        [
            FFMPEG,

            "-y",

            "-i",
            video_file,

            "-i",
            audio_file,

            "-c:v",
            "copy",

            "-c:a",
            "aac",

            output_file
        ],

        check=True
    )


    # ========================================================
    # 🗑️ TEMPORARY FILES DELETE
    # ========================================================

    if os.path.exists(video_file):

        os.remove(video_file)


    if os.path.exists(audio_file):

        os.remove(audio_file)


    # ========================================================
    # ✅ DOWNLOAD COMPLETE
    # ========================================================

    print("\n✅ Download complete!")

    print(
        "Saved as:",
        output_file
    )


# ============================================================
# ❌ ERROR HANDLING
# ============================================================

except Exception as e:

    print("\n❌ Error:", e)

# Run the code and enjoy for download video without IDM
# py yt_download.py
# and enter youtube video URL
# wait some time and see the video
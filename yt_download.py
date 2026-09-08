# ============================================================
# 🎬 YouTube Video Downloader
# ============================================================
#
# 📦 INSTALLATION
#
# VS Code Terminal mein ye commands run karein:
#
# pip install pytubefix
#
# FFmpeg install karne ke liye:
#
# winget install Gyan.FFmpeg
#
# FFmpeg check karne ke liye:
#
# ffmpeg -version
#
# Agar "ffmpeg is not recognized" aaye to:
#
# winget install Gyan.FFmpeg
#
# ============================================================


from pytubefix import YouTube
import subprocess
import os
import shutil
import re


# ============================================================
# ⚙️ DOWNLOAD FOLDER
# ============================================================
#
# Video automatically Windows ke Downloads folder mein jayegi.
#
# Example:
# C:\Users\YourName\Downloads
#
# ============================================================

DOWNLOAD_FOLDER = os.path.join(
    os.path.expanduser("~"),
    "Downloads"
)

# Agar Downloads folder nahi hai to create kar do
os.makedirs(DOWNLOAD_FOLDER, exist_ok=True)


# ============================================================
# ⚙️ FIND FFMPEG AUTOMATICALLY
# ============================================================

FFMPEG = shutil.which("ffmpeg")


# Agar PATH mein FFmpeg nahi milta
if not FFMPEG:

    # Common WinGet location
    winget_folder = os.path.join(
        os.path.expanduser("~"),
        "AppData",
        "Local",
        "Microsoft",
        "WinGet",
        "Packages"
    )

    # FFmpeg executable search karna
    for root, dirs, files in os.walk(winget_folder):

        if "ffmpeg.exe" in files:

            FFMPEG = os.path.join(
                root,
                "ffmpeg.exe"
            )

            break


# ============================================================
# ❌ FFMPEG CHECK
# ============================================================

if not FFMPEG:

    print("\n❌ FFmpeg nahi mila!")

    print("\nTerminal mein ye command run karein:")

    print("winget install Gyan.FFmpeg")

    print("\nPhir VS Code restart karke program dobara run karein.")

    input("\nPress Enter to exit...")

    exit()


# ============================================================
# 🧹 SAFE FILE NAME
# ============================================================

def safe_filename(filename):

    # Windows ke invalid characters remove karna
    filename = re.sub(
        r'[<>:"/\\|?*]',
        '',
        filename
    )

    # Extra spaces remove
    filename = filename.strip()

    # Filename bohat long na ho
    return filename[:150]


# ============================================================
# 🎥 DOWNLOAD FUNCTION
# ============================================================

def download_video():

    # YouTube URL
    link = input(
        "\n🔗 Enter YouTube URL "
        "(exit likh kar program band karein): "
    )

    # Program exit
    if link.lower() == "exit":

        print("\n👋 Program closed. Goodbye!")

        return False


    try:

        # ====================================================
        # YouTube video information
        # ====================================================

        print("\n🔍 Getting video information...")

        yt = YouTube(link)

        print("\n🎬 Title:")
        print(yt.title)


        # ====================================================
        # QUALITY OPTIONS
        # ====================================================

        print("\n🎥 Available Quality Options:")

        print("1. 360p")
        print("2. 480p")
        print("3. 720p")
        print("4. 1080p")


        choice = input(
            "\nSelect quality (1-4): "
        )


        quality_map = {

            "1": "360p",
            "2": "480p",
            "3": "720p",
            "4": "1080p"

        }


        selected_quality = quality_map.get(
            choice
        )


        # Wrong choice
        if not selected_quality:

            print("\n❌ Invalid quality choice!")

            return True


        print(
            f"\n✅ Selected Quality: "
            f"{selected_quality}"
        )


        # ====================================================
        # FIND VIDEO STREAM
        # ====================================================

        print("\n🔍 Searching video stream...")


        video = (
            yt.streams
            .filter(
                adaptive=True,
                file_extension="mp4",
                res=selected_quality
            )
            .first()
        )


        # ====================================================
        # FALLBACK QUALITY
        # ====================================================

        if not video:

            print(
                f"\n⚠️ {selected_quality} "
                "available nahi hai."
            )

            available = []


            for stream in yt.streams:

                if (
                    stream.type == "video"
                    and stream.mime_type == "video/mp4"
                    and stream.resolution
                ):

                    if stream.resolution not in available:

                        available.append(
                            stream.resolution
                        )


            quality_order = [
                "1080p",
                "720p",
                "480p",
                "360p"
            ]


            selected_index = quality_order.index(
                selected_quality
            )


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
                            f"\n✅ {quality} available hai."
                        )

                        print(
                            f"📥 {quality} download hogi."
                        )

                        break


        # No video found
        if not video:

            print(
                "\n❌ Suitable video stream nahi mili."
            )

            return True


        # ====================================================
        # BEST AUDIO
        # ====================================================

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

            print(
                "\n❌ Audio stream nahi mili."
            )

            return True


        print(
            "\n📹 Video:",
            video.resolution
        )

        print(
            "🔊 Audio:",
            audio.abr
        )


        # ====================================================
        # SAFE VIDEO TITLE
        # ====================================================

        title = safe_filename(
            yt.title
        )


        # ====================================================
        # TEMPORARY FILES
        # ====================================================

        video_file = os.path.join(
            DOWNLOAD_FOLDER,
            "_temp_video.mp4"
        )

        audio_file = os.path.join(
            DOWNLOAD_FOLDER,
            "_temp_audio.mp4"
        )

        output_file = os.path.join(
            DOWNLOAD_FOLDER,
            title + ".mp4"
        )


        # ====================================================
        # DOWNLOAD VIDEO
        # ====================================================

        print(
            "\n📥 Downloading video..."
        )


        video.download(
            output_path=DOWNLOAD_FOLDER,
            filename="_temp_video.mp4"
        )


        # ====================================================
        # DOWNLOAD AUDIO
        # ====================================================

        print(
            "🔊 Downloading audio..."
        )


        audio.download(
            output_path=DOWNLOAD_FOLDER,
            filename="_temp_audio.mp4"
        )


        # ====================================================
        # MERGE VIDEO + AUDIO
        # ====================================================

        print(
            "\n🔄 Merging video + audio..."
        )


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


        # ====================================================
        # DELETE TEMP FILES
        # ====================================================

        if os.path.exists(video_file):

            os.remove(video_file)


        if os.path.exists(audio_file):

            os.remove(audio_file)


        # ====================================================
        # SUCCESS
        # ====================================================

        print(
            "\n========================================"
        )

        print(
            "✅ DOWNLOAD COMPLETE!"
        )

        print(
            "========================================"
        )

        print(
            "\n🎬 Video:",
            title + ".mp4"
        )

        print(
            "\n📁 Saved in:"
        )

        print(
            DOWNLOAD_FOLDER
        )


        print(
            "\n🔁 Aap next video ka URL enter kar sakte hain."
        )


        return True


    # ========================================================
    # ERROR HANDLING
    # ========================================================

    except Exception as e:

        print(
            "\n❌ Error:",
            e
        )


        # Temporary files cleanup
        if os.path.exists(video_file):

            try:
                os.remove(video_file)
            except:
                pass


        if os.path.exists(audio_file):

            try:
                os.remove(audio_file)
            except:
                pass


        return True


# ============================================================
# 🚀 MAIN PROGRAM
# ============================================================

print(
    "\n=============================================="
)

print(
    "🎬 YOUTUBE VIDEO DOWNLOADER"
)

print(
    "=============================================="
)

print(
    "\n📁 Videos will be saved in:"
)

print(
    DOWNLOAD_FOLDER
)

print(
    "\n💡 Multiple videos download karne ke liye"
)

print(
    "   program ko baar-baar run karne ki zaroorat nahi."
)

print(
    "\n💡 Program band karne ke liye URL ki jagah"
)

print(
    "   'exit' type karein."
)


# ============================================================
# 🔁 CONTINUOUS DOWNLOAD LOOP
# ============================================================

while True:

    keep_running = download_video()

    if not keep_running:

        break
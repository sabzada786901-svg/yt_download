import streamlit as st
import subprocess
import sys
import os
import time


# ============================================================
# 🎬 PAGE SETTINGS
# ============================================================

st.set_page_config(
    page_title="YouTube Downloader",
    page_icon="🎬",
    layout="centered"
)


# ============================================================
# 🎨 CUSTOM DESIGN
# ============================================================

st.markdown("""
<style>

.main-title {
    text-align: center;
    font-size: 42px;
    font-weight: 700;
    margin-bottom: 5px;
}

.subtitle {
    text-align: center;
    font-size: 18px;
    margin-bottom: 30px;
}

.download-button {
    width: 100%;
}

</style>
""", unsafe_allow_html=True)


# ============================================================
# 🏠 HEADER
# ============================================================

st.markdown(
    '<div class="main-title">🎬 YouTube Downloader</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">Fast & Simple YouTube Video Downloader</div>',
    unsafe_allow_html=True
)


# ============================================================
# 📁 FIND yt_download.py
# ============================================================

BASE_DIR = os.path.dirname(
    os.path.abspath(__file__)
)

DOWNLOADER_FILE = os.path.join(
    BASE_DIR,
    "yt_download.py"
)


if not os.path.exists(DOWNLOADER_FILE):

    st.error(
        "❌ yt_download.py nahi mili!"
    )

    st.info(
        "app.py aur yt_download.py ko same folder mein rakhein."
    )

    st.stop()


# ============================================================
# 🔗 URL INPUT
# ============================================================

st.subheader("🔗 YouTube Video")

url = st.text_input(
    "YouTube URL",
    placeholder="https://www.youtube.com/watch?v=..."
)


# ============================================================
# 🎥 QUALITY
# ============================================================

st.subheader("🎥 Select Quality")

quality = st.selectbox(
    "Video Quality",
    [
        "360p",
        "480p",
        "720p",
        "1080p"
    ]
)


quality_map = {
    "360p": "1",
    "480p": "2",
    "720p": "3",
    "1080p": "4"
}


# ============================================================
# 📥 DOWNLOAD BUTTON
# ============================================================

download = st.button(
    "⬇️ Download Video",
    use_container_width=True
)


# ============================================================
# 🚀 DOWNLOAD
# ============================================================

if download:

    # --------------------------------------------------------
    # URL CHECK
    # --------------------------------------------------------

    if not url.strip():

        st.warning(
            "⚠️ Pehle YouTube URL enter karein."
        )

        st.stop()


    # --------------------------------------------------------
    # YOUTUBE URL CHECK
    # --------------------------------------------------------

    if (
        "youtube.com" not in url.lower()
        and
        "youtu.be" not in url.lower()
    ):

        st.error(
            "❌ Invalid YouTube URL."
        )

        st.stop()


    # --------------------------------------------------------
    # QUALITY
    # --------------------------------------------------------

    selected_quality = quality_map[quality]


    st.info(
        f"🎥 Selected quality: {quality}"
    )


    # ========================================================
    # START EXISTING DOWNLOADER
    # ========================================================

    try:

        process = subprocess.Popen(
            [
                sys.executable,

                # Force Python UTF-8 mode
                "-X",
                "utf8",

                DOWNLOADER_FILE
            ],

            stdin=subprocess.PIPE,

            stdout=subprocess.PIPE,

            stderr=subprocess.STDOUT,

            text=True,

            encoding="utf-8",

            errors="replace",

            bufsize=1
        )


        # ====================================================
        # SEND INPUT TO yt_download.py
        # ====================================================

        process.stdin.write(
            url.strip() + "\n"
        )

        process.stdin.write(
            selected_quality + "\n"
        )

        process.stdin.write(
            "exit\n"
        )

        process.stdin.flush()

        process.stdin.close()


        # ====================================================
        # PROGRESS
        # ====================================================

        progress = st.progress(0)

        status = st.empty()

        output_box = st.empty()

        output = ""


        # ====================================================
        # READ DOWNLOADER OUTPUT
        # ====================================================

        while True:

            line = process.stdout.readline()


            if line:

                output += line

                # Show output without crashing
                output_box.code(
                    output[-5000:]
                )


                # --------------------------------------------
                # STATUS
                # --------------------------------------------

                lower_line = line.lower()


                if "getting video information" in lower_line:

                    status.info(
                        "🔍 Getting video information..."
                    )

                    progress.progress(10)


                elif "searching video stream" in lower_line:

                    status.info(
                        "🔎 Searching video stream..."
                    )

                    progress.progress(20)


                elif "downloading video" in lower_line:

                    status.info(
                        "📥 Downloading video..."
                    )

                    progress.progress(40)


                elif "downloading audio" in lower_line:

                    status.info(
                        "🔊 Downloading audio..."
                    )

                    progress.progress(65)


                elif "merging video" in lower_line:

                    status.info(
                        "🔄 Merging video + audio..."
                    )

                    progress.progress(85)


                elif "download complete" in lower_line:

                    status.success(
                        "✅ Download Complete!"
                    )

                    progress.progress(100)


            else:

                if process.poll() is not None:

                    break

                time.sleep(0.1)


        # ====================================================
        # PROCESS COMPLETE
        # ====================================================

        return_code = process.wait()


        # ====================================================
        # SUCCESS
        # ====================================================

        if return_code == 0:

            progress.progress(100)

            status.success(
                "🎉 Video successfully downloaded!"
            )


            # Windows Downloads folder
            download_folder = os.path.join(
                os.path.expanduser("~"),
                "Downloads"
            )


            st.success(
                "📁 Video Downloads folder mein save ho gayi."
            )


            st.code(
                download_folder
            )


            st.info(
                "🔄 Next video ke liye upar naya URL enter karein."
            )


        else:

            st.error(
                "❌ Downloader process mein error aaya."
            )

            st.code(
                output
            )


    except Exception as e:

        st.error(
            "❌ Application Error"
        )

        st.exception(e)


# ============================================================
# 📌 FOOTER
# ============================================================

st.markdown("---")

st.caption(
    "🎬 YouTube Downloader | Python + Streamlit"
)

st.caption(
    "Use this tool only for content you have permission to download."
)
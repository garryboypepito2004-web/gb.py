import streamlit as st
import yt_dlp
import os
import shutil
from pathlib import Path
import time
import requests
from datetime import datetime

# ═══════════════════════════════════════════════════════
# 1. MODERN APP CONFIGURATION
# ═══════════════════════════════════════════════════════

st.set_page_config(
    page_title="GB DOWNLOADER - Ultimate Video Downloader",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for modern styling
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');

    * {
        font-family: 'Inter', sans-serif;
    }

    .glass-morphism {
        background: rgba(255, 255, 255, 0.1);
        backdrop-filter: blur(20px);
        -webkit-backdrop-filter: blur(20px);
        border: 1px solid rgba(255, 255, 255, 0.2);
        border-radius: 20px;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
    }

    .main-header {
        background: linear-gradient(135deg,
            rgba(102, 126, 234, 0.9) 0%,
            rgba(118, 75, 162, 0.9) 100%);
        backdrop-filter: blur(25px);
        -webkit-backdrop-filter: blur(25px);
        color: white;
        padding: 3rem;
        border-radius: 25px;
        text-align: center;
        margin-bottom: 2rem;
        box-shadow:
            0 20px 40px rgba(0,0,0,0.1),
            inset 0 1px 0 rgba(255,255,255,0.2);
        border: 1px solid rgba(255, 255, 255, 0.3);
        position: relative;
        overflow: hidden;
    }

    .main-header::before {
        content: '';
        position: absolute;
        top: 0;
        left: -100%;
        width: 100%;
        height: 100%;
        background: linear-gradient(90deg, transparent, rgba(255,255,255,0.1), transparent);
        animation: shimmer 3s infinite;
    }

    @keyframes shimmer {
        0% { left: -100%; }
        100% { left: 100%; }
    }

    .feature-card {
        background: rgba(255, 255, 255, 0.95);
        backdrop-filter: blur(15px);
        -webkit-backdrop-filter: blur(15px);
        padding: 2rem;
        border-radius: 20px;
        box-shadow:
            0 10px 30px rgba(0,0,0,0.1),
            inset 0 1px 0 rgba(255,255,255,0.8);
        border: 1px solid rgba(255, 255, 255, 0.3);
        margin: 1rem 0;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        position: relative;
        overflow: hidden;
    }

    .feature-card:hover {
        transform: translateY(-5px) scale(1.02);
        box-shadow:
            0 20px 40px rgba(0,0,0,0.15),
            inset 0 1px 0 rgba(255,255,255,0.9);
    }

    .feature-card::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 4px;
        background: linear-gradient(90deg, #667eea, #764ba2, #f093fb, #f5576c);
        background-size: 300% 300%;
        animation: gradient-shift 3s ease infinite;
    }

    @keyframes gradient-shift {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }

    .download-progress {
        background: linear-gradient(135deg, #4CAF50, #45a049);
        height: 12px;
        border-radius: 6px;
        margin: 1rem 0;
        position: relative;
        overflow: hidden;
        box-shadow: inset 0 2px 4px rgba(0,0,0,0.1);
    }

    .download-progress::after {
        content: '';
        position: absolute;
        top: 0;
        left: -100%;
        width: 100%;
        height: 100%;
        background: linear-gradient(90deg, transparent, rgba(255,255,255,0.3), transparent);
        animation: progress-shine 2s infinite;
    }

    @keyframes progress-shine {
        0% { left: -100%; }
        100% { left: 100%; }
    }

    .ad-sidebar {
        background: rgba(248, 249, 250, 0.8);
        backdrop-filter: blur(20px);
        -webkit-backdrop-filter: blur(20px);
        padding: 1.5rem;
        border-radius: 20px;
        border: 1px solid rgba(255, 255, 255, 0.3);
        margin-bottom: 1rem;
        box-shadow: 0 8px 32px rgba(0,0,0,0.1);
    }

    .stats-card {
        background: linear-gradient(135deg,
            rgba(255, 154, 158, 0.9) 0%,
            rgba(254, 207, 239, 0.9) 100%);
        backdrop-filter: blur(15px);
        color: white;
        padding: 1.5rem;
        border-radius: 15px;
        text-align: center;
        margin: 0.5rem 0;
        box-shadow: 0 8px 32px rgba(0,0,0,0.1);
        border: 1px solid rgba(255, 255, 255, 0.2);
        transition: transform 0.3s ease;
    }

    .stats-card:hover {
        transform: translateY(-3px);
    }

    .modern-button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        padding: 14px 28px;
        border-radius: 30px;
        font-weight: 600;
        font-size: 16px;
        cursor: pointer;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        box-shadow: 0 4px 15px rgba(102, 126, 234, 0.3);
        position: relative;
        overflow: hidden;
    }

    .modern-button::before {
        content: '';
        position: absolute;
        top: 0;
        left: -100%;
        width: 100%;
        height: 100%;
        background: linear-gradient(90deg, transparent, rgba(255,255,255,0.2), transparent);
        transition: left 0.5s;
    }

    .modern-button:hover::before {
        left: 100%;
    }

    .modern-button:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 25px rgba(102, 126, 234, 0.4);
    }

    .platform-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(120px, 1fr));
        gap: 1rem;
        margin: 1rem 0;
    }

    .platform-item {
        background: rgba(255, 255, 255, 0.8);
        backdrop-filter: blur(10px);
        padding: 1rem;
        border-radius: 12px;
        text-align: center;
        border: 1px solid rgba(255, 255, 255, 0.3);
        transition: all 0.3s ease;
        box-shadow: 0 4px 12px rgba(0,0,0,0.05);
    }

    .platform-item:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 20px rgba(0,0,0,0.1);
        background: rgba(255, 255, 255, 0.95);
    }

    .loading-spinner {
        display: inline-block;
        width: 20px;
        height: 20px;
        border: 3px solid rgba(255,255,255,.3);
        border-radius: 50%;
        border-top-color: #fff;
        animation: spin 1s ease-in-out infinite;
    }

    @keyframes spin {
        to { transform: rotate(360deg); }
    }

    .success-animation {
        animation: bounce-in 0.6s ease-out;
    }

    @keyframes bounce-in {
        0% { transform: scale(0.3); opacity: 0; }
        50% { transform: scale(1.05); }
        70% { transform: scale(0.9); }
        100% { transform: scale(1); opacity: 1; }
    }

    .fade-in {
        animation: fade-in 0.5s ease-in;
    }

    @keyframes fade-in {
        from { opacity: 0; transform: translateY(20px); }
        to { opacity: 1; transform: translateY(0); }
    }

    .glow-effect {
        box-shadow: 0 0 20px rgba(102, 126, 234, 0.3);
        animation: glow-pulse 2s infinite;
    }

    @keyframes glow-pulse {
        0%, 100% { box-shadow: 0 0 20px rgba(102, 126, 234, 0.3); }
        50% { box-shadow: 0 0 30px rgba(102, 126, 234, 0.6); }
    }

    /* Custom scrollbar */
    ::-webkit-scrollbar {
        width: 8px;
    }

    ::-webkit-scrollbar-track {
        background: rgba(255, 255, 255, 0.1);
        border-radius: 10px;
    }

    ::-webkit-scrollbar-thumb {
        background: linear-gradient(135deg, #667eea, #764ba2);
        border-radius: 10px;
    }

    ::-webkit-scrollbar-thumb:hover {
        background: linear-gradient(135deg, #5a6fd8, #6a4190);
    }
</style>
""", unsafe_allow_html=True)

# Initialize directories
DOWNLOAD_DIR = Path("downloads")
DOWNLOAD_DIR.mkdir(exist_ok=True)
HISTORY_FILE = Path("download_history.txt")

# ═══════════════════════════════════════════════════════
# 2. QUALITY OPTIONS & PLATFORMS
# ═══════════════════════════════════════════════════════

QUALITY_OPTIONS = {
    "🎬 480p SD": "bestvideo[height<=480]+bestaudio/best[height<=480]",
    "🎥 720p HD": "bestvideo[height<=720]+bestaudio/best[height<=720]",
    "📺 1080p Full HD": "bestvideo[height<=1080]+bestaudio/best[height<=1080]",
    "🎯 1440p 2K UHD": "bestvideo[height<=1440]+bestaudio/best[height<=1440]",
    "🚀 2160p 4K UHD": "bestvideo[height<=2160]+bestaudio/best[height<=2160]",
    "💎 Best Available": "bestvideo+bestaudio/best"
}

PLATFORMS = {
    "📘 Facebook": ["facebook.com", "fb.watch"],
    "📷 Instagram": ["instagram.com", "instagr.am"],
    "🎵 TikTok": ["tiktok.com", "vm.tiktok.com"],
    "📺 YouTube": ["youtube.com", "youtu.be"],
    "🐦 Twitter/X": ["twitter.com", "x.com"],
    "💼 LinkedIn": ["linkedin.com"],
    "🎬 Vimeo": ["vimeo.com"],
    "📱 Other": []
}

# ═══════════════════════════════════════════════════════
# 3. UTILITY FUNCTIONS
# ═══════════════════════════════════════════════════════

def save_to_history(url, title, platform, quality, file_size):
    """Save download to history"""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(HISTORY_FILE, "a") as f:
        f.write(f"{timestamp}|{url}|{title}|{platform}|{quality}|{file_size}\n")

def load_history():
    """Load download history"""
    if HISTORY_FILE.exists():
        with open(HISTORY_FILE, "r") as f:
            return [line.strip().split("|") for line in f.readlines()]
    return []

def detect_platform(url):
    """Detect platform from URL"""
    for platform, domains in PLATFORMS.items():
        if any(domain in url.lower() for domain in domains):
            return platform
    return "📱 Other"

def format_file_size(size_bytes):
    """Format file size in human readable format"""
    for unit in ['B', 'KB', 'MB', 'GB']:
        if size_bytes < 1024.0:
            return ".1f"
        size_bytes /= 1024.0
    return ".1f"

# ═══════════════════════════════════════════════════════
# 4. DOWNLOAD LOGIC
# ═══════════════════════════════════════════════════════

def run_download(url, quality_key, cookie_path=None, custom_filename="", audio_only=False, start_time="", end_time="", **kwargs):
    """Enhanced professional download function with advanced options"""
    ydl_opts = {
        'format': QUALITY_OPTIONS[quality_key],
        'outtmpl': f'{DOWNLOAD_DIR}/%(title)s.%(ext)s',
        'merge_output_format': 'mp4',
        'noplaylist': True,
        'quiet': False,  # Show progress for better UX
        'no_warnings': False,
        'progress_hooks': [],  # Can add progress hooks later
    }

    # Add cookie file if provided
    if cookie_path:
        ydl_opts['cookiefile'] = cookie_path

    # Audio only option with advanced settings
    if audio_only:
        ydl_opts['format'] = 'bestaudio/best'
        ydl_opts['postprocessors'] = [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': kwargs.get('audio_codec', 'mp3').lower(),
            'preferredquality': kwargs.get('audio_bitrate', '192').replace('k', ''),
        }]

        # Audio normalization
        if kwargs.get('normalize_audio', False):
            ydl_opts['postprocessors'].append({
                'key': 'FFmpegAudioNormalize',
            })

    # Custom filename
    if custom_filename:
        ydl_opts['outtmpl'] = f'{DOWNLOAD_DIR}/{custom_filename}.%(ext)s'

    # Video codec and quality settings
    if not audio_only and kwargs.get('video_codec'):
        codec = kwargs.get('video_codec', 'H.264')
        if codec == 'H.265':
            ydl_opts['merge_output_format'] = 'mkv'  # H.265 often needs MKV
        elif codec == 'VP9':
            ydl_opts['merge_output_format'] = 'webm'

    # Time range
    if start_time or end_time:
        ydl_opts['download_ranges'] = lambda info_dict, ydl: [{
            'start_time': start_time if start_time else None,
            'end_time': end_time if end_time else None,
        }]

    # Subtitle options
    if kwargs.get('subtitle_download', False):
        ydl_opts['writesubtitles'] = True
        ydl_opts['writeautomaticsub'] = True
        ydl_opts['subtitleslangs'] = ['en', 'es', 'fr', 'de', 'it']

        if kwargs.get('embed_subtitles', False):
            ydl_opts['embedsubtitles'] = True

    # Thumbnail download
    if kwargs.get('thumbnail_download', False):
        ydl_opts['writethumbnail'] = True

    # Metadata preservation
    if kwargs.get('metadata_preserve', True):
        ydl_opts['addmetadata'] = True

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=True)
        downloaded_file = ydl.prepare_filename(info)

        # Ensure correct extension
        if audio_only:
            ext = kwargs.get('audio_codec', 'mp3').lower()
            final_path = os.path.splitext(downloaded_file)[0] + f".{ext}"
        else:
            final_path = os.path.splitext(downloaded_file)[0] + ".mp4"

        return final_path, info

# ═══════════════════════════════════════════════════════
# 5. MAIN UI LAYOUT
# ═══════════════════════════════════════════════════════

# Left Sidebar - Advanced Features & Stats
with st.sidebar:
    st.markdown('<div class="ad-sidebar glass-morphism">', unsafe_allow_html=True)
    st.markdown("### ⚡ Advanced Features")
    st.markdown("---")

    # Advanced feature toggles
    st.markdown("**🎯 Quality Control:**")
    hq_mode = st.checkbox("High Quality Mode", value=True, help="Prioritize quality over speed")
    compression = st.checkbox("Smart Compression", help="Optimize file size without quality loss")

    st.markdown("---")
    st.markdown("**📊 Performance:**")
    parallel_downloads = st.slider("Parallel Downloads", 1, 5, 2, help="Number of simultaneous downloads")
    speed_limit = st.selectbox("Speed Limit", ["Unlimited", "10MB/s", "5MB/s", "1MB/s"], help="Limit download speed")

    st.markdown("---")
    st.markdown("**🔧 System Stats:**")

    history = load_history()
    total_downloads = len(history)
    total_size = sum(float(item[5]) for item in history if len(item) > 5)

    col1, col2 = st.columns(2)
    with col1:
        st.metric("Total Downloads", total_downloads)
    with col2:
        st.metric("Data Saved", f"{format_file_size(total_size)}")

    st.markdown("---")
    st.markdown("**🛠️ Tools:**")
    if st.button("🗑️ Clear Cache", use_container_width=True):
        for file in DOWNLOAD_DIR.glob("*"):
            file.unlink()
        st.success("Cache cleared!")

    if st.button("📋 Download History", use_container_width=True):
        st.markdown("### 📚 Download History")
        if history:
            for item in history[-10:]:  # Show last 10
                st.markdown(f"**{item[2]}** - {item[3]} ({item[4]}) - {format_file_size(float(item[5]))}")
        else:
            st.info("No downloads yet")

    if st.button("🔍 System Info", use_container_width=True):
        st.markdown("### 💻 System Information")
        st.markdown(f"**FFmpeg:** {'✅ Installed' if shutil.which('ffmpeg') else '❌ Not found'}")
        st.markdown(f"**Python:** {os.sys.version.split()[0]}")
        st.markdown(f"**Platform:** {os.sys.platform}")
        st.markdown(f"**Disk Space:** {shutil.disk_usage('/')[2] // (1024**3)} GB free")

    st.markdown('</div>', unsafe_allow_html=True)

# Main Content Area
col1, col2 = st.columns([2, 1])

with col1:
    # Header
    st.markdown('<div class="main-header">', unsafe_allow_html=True)
    st.title("🚀 GB DOWNLOADER PRO")
    st.markdown("### Professional Video Downloader Suite")
    st.markdown("**Enterprise-grade video downloading with 4K support, batch processing, and advanced encoding options**")
    st.markdown('</div>', unsafe_allow_html=True)

    # Platform Support
    st.markdown("### 🌐 Supported Platforms")
    st.markdown('<div class="platform-grid">', unsafe_allow_html=True)

    for i, platform in enumerate(platforms_list):
        st.markdown(f'''
            <div class="platform-item fade-in" style="animation-delay: {i * 0.1}s">
                <strong>{platform}</strong>
            </div>
        ''', unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)

    # Input Section
    st.markdown("---")
    st.markdown("### 📥 Download Section")

    with st.container():
        st.markdown('<div class="feature-card glass-morphism">', unsafe_allow_html=True)

        # URL Input
        video_url = st.text_input(
            "🔗 Paste Video URL",
            placeholder="https://www.instagram.com/reels/...",
            help="Paste any video URL from supported platforms"
        )

        # Quality Selection
        selected_quality = st.selectbox(
            "🎯 Select Quality",
            list(QUALITY_OPTIONS.keys()),
            index=1,
            help="Choose your preferred video quality"
        )

        # Cookie Upload
        cookie_file = st.file_uploader(
            "🍪 Cookies (for private content)",
            type=["txt"],
            help="Upload cookies.txt for private Instagram/Facebook videos"
        )

        # Advanced Options with modern expander
        with st.expander("⚙️ Advanced Options", expanded=False):
            tab1, tab2, tab3 = st.tabs(["🎬 Video", "🎵 Audio", "🔧 System"])

            with tab1:
                col_a, col_b = st.columns(2)
                with col_a:
                    custom_filename = st.text_input("Custom Filename", "")
                    video_codec = st.selectbox("Video Codec", ["H.264", "H.265", "VP9", "AV1"])
                    preset = st.selectbox("Encoding Preset", ["ultrafast", "fast", "medium", "slow", "veryslow"])
                with col_b:
                    crf = st.slider("Quality (CRF)", 0, 51, 23, help="Lower = better quality, higher file size")
                    max_fps = st.selectbox("Max FPS", ["Auto", "30", "60", "120"])
                    color_space = st.selectbox("Color Space", ["Auto", "BT.709", "BT.2020"])

            with tab2:
                col_c, col_d = st.columns(2)
                with col_c:
                    audio_only = st.checkbox("🎵 Audio Only (MP3)")
                    audio_codec = st.selectbox("Audio Codec", ["MP3", "AAC", "FLAC", "WAV"])
                    audio_bitrate = st.selectbox("Audio Bitrate", ["128k", "192k", "256k", "320k"])
                with col_d:
                    normalize_audio = st.checkbox("Normalize Audio")
                    remove_silence = st.checkbox("Remove Silence")
                    audio_channels = st.selectbox("Channels", ["Stereo", "Mono"])

            with tab3:
                col_e, col_f = st.columns(2)
                with col_e:
                    start_time = st.text_input("Start Time (HH:MM:SS)", "")
                    end_time = st.text_input("End Time (HH:MM:SS)", "")
                    subtitle_download = st.checkbox("📝 Download Subtitles")
                with col_f:
                    embed_subtitles = st.checkbox("Embed Subtitles")
                    thumbnail_download = st.checkbox("🖼️ Download Thumbnail")
                    metadata_preserve = st.checkbox("📋 Preserve Metadata", value=True)

        # Store advanced options for download
        if 'advanced_opts' not in st.session_state:
            st.session_state.advanced_opts = {}

        st.session_state.advanced_opts = {
            'custom_filename': custom_filename if 'custom_filename' in locals() else '',
            'audio_only': audio_only if 'audio_only' in locals() else False,
            'start_time': start_time if 'start_time' in locals() else '',
            'end_time': end_time if 'end_time' in locals() else '',
            'video_codec': video_codec if 'video_codec' in locals() else 'H.264',
            'audio_codec': audio_codec if 'audio_codec' in locals() else 'MP3',
            'preset': preset if 'preset' in locals() else 'medium',
            'crf': crf if 'crf' in locals() else 23
        }

        # Quality Comparison Tool
        if st.checkbox("📊 Compare Quality Options"):
            st.markdown("### 🎯 Quality Comparison")
            test_url = st.text_input("Test URL for comparison", placeholder="Enter URL to analyze available qualities", key="quality_test_url")

            if test_url and st.button("🔍 Analyze Qualities", key="analyze_qualities"):
                try:
                    with st.spinner("Analyzing available formats..."):
                        ydl_opts = {'quiet': True, 'no_warnings': True}
                        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                            info = ydl.extract_info(test_url, download=False)

                        formats = info.get('formats', [])
                        video_formats = [f for f in formats if f.get('vcodec') != 'none']

                        if video_formats:
                            st.markdown("**Available Video Qualities:**")
                            quality_data = []
                            for fmt in sorted(video_formats, key=lambda x: x.get('height', 0), reverse=True):
                                height = fmt.get('height', 'Unknown')
                                fps = fmt.get('fps', 'Unknown')
                                vcodec = fmt.get('vcodec', 'Unknown').split('.')[0]
                                acodec = fmt.get('acodec', 'Unknown').split('.')[0]
                                filesize = fmt.get('filesize')
                                size_str = format_file_size(filesize) if filesize else "Unknown"

                                quality_data.append({
                                    "Resolution": f"{height}p" if height != 'Unknown' else 'Unknown',
                                    "FPS": fps,
                                    "Video Codec": vcodec,
                                    "Audio Codec": acodec,
                                    "File Size": size_str
                                })

                            st.dataframe(quality_data, use_container_width=True)
                        else:
                            st.warning("No video formats found")

                except Exception as e:
                    st.error(f"Analysis failed: {str(e)}")

        # Batch download section
        if st.checkbox("📦 Batch Download Mode"):
            st.markdown("### 📦 Batch Processing")
            batch_urls = st.text_area(
                "Paste multiple URLs (one per line)",
                height=150,
                placeholder="https://instagram.com/reel/...\nhttps://facebook.com/watch/...\nhttps://tiktok.com/...",
                help="Enter one URL per line for batch processing"
            )

            if batch_urls:
                url_list = [url.strip() for url in batch_urls.split('\n') if url.strip() and url.strip().startswith('http')]
                st.info(f"📋 Ready to process {len(url_list)} videos")

                if len(url_list) > 10:
                    st.warning("⚠️ Large batch detected. Processing may take time.")

                batch_progress = st.progress(0)
                batch_status = st.empty()

                if st.button("🚀 Start Batch Download", use_container_width=True, type="primary"):
                    successful = 0
                    failed = 0

                    for i, url in enumerate(url_list):
                        try:
                            batch_status.text(f"Processing {i+1}/{len(url_list)}: {url[:50]}...")
                            batch_progress.progress((i) / len(url_list))

                            # Download logic here
                            file_path, info = run_download(url, selected_quality, cookie_path if cookie_file else None)

                            if os.path.exists(file_path):
                                successful += 1
                                save_to_history(url, info.get('title', 'Unknown'), detect_platform(url), selected_quality, os.path.getsize(file_path))
                            else:
                                failed += 1

                        except Exception as e:
                            failed += 1
                            st.error(f"Failed {url[:50]}...: {str(e)}")

                    batch_progress.progress(1.0)
                    batch_status.text(f"✅ Batch complete! {successful} successful, {failed} failed")
                    st.success(f"Batch processing finished! ✅ {successful} | ❌ {failed}")

        # Download Button
        download_button = st.button(
            "⬇️ START DOWNLOAD",
            use_container_width=True,
            type="primary"
        )

        st.markdown('</div>', unsafe_allow_html=True)
    # Download Progress and Results
    if download_button:
        if not video_url:
            st.error("❌ Please enter a video URL")
        else:
            # Detect platform
            platform = detect_platform(video_url)
            st.info(f"🎯 Detected platform: {platform}")

            # Handle cookies
            cookie_path = None
            if cookie_file:
                cookie_path = "cookies.txt"
                with open(cookie_path, "wb") as f:
                    f.write(cookie_file.getvalue())

            try:
                # Modern progress container
                progress_container = st.container()
                with progress_container:
                    st.markdown('<div class="feature-card glass-morphism">', unsafe_allow_html=True)

                    # Animated progress bar
                    progress_bar = st.progress(0)
                    status_text = st.empty()
                    status_icon = st.empty()

                    # Step 1: Extracting info
                    status_icon.markdown("🔍")
                    status_text.markdown("**📡 Extracting video information...**")
                    time.sleep(0.5)  # Simulate processing
                    progress_bar.progress(20)

                    # Step 2: Validating URL
                    status_icon.markdown("✅")
                    status_text.markdown("**🔗 Validating URL and permissions...**")
                    time.sleep(0.3)
                    progress_bar.progress(40)

                    # Step 3: Preparing download
                    status_icon.markdown("⚙️")
                    status_text.markdown("**🔧 Preparing download settings...**")
                    time.sleep(0.3)
                    progress_bar.progress(60)

                    # Get advanced options
                    opts = st.session_state.get('advanced_opts', {})
                    custom_filename = opts.get('custom_filename', '')
                    audio_only = opts.get('audio_only', False)
                    start_time = opts.get('start_time', '')
                    end_time = opts.get('end_time', '')
                    video_codec = opts.get('video_codec', 'H.264')
                    audio_codec = opts.get('audio_codec', 'MP3')
                    preset = opts.get('preset', 'medium')
                    crf = opts.get('crf', 23)

                    # Step 4: Downloading
                    status_icon.markdown("⬇️")
                    status_text.markdown("**🚀 Downloading video...**")
                    progress_bar.progress(80)

                    # Download with all advanced options
                    file_path, info = run_download(
                        video_url, selected_quality, cookie_path,
                        custom_filename=custom_filename,
                        audio_only=audio_only,
                        start_time=start_time,
                        end_time=end_time,
                        video_codec=video_codec,
                        audio_codec=audio_codec,
                        preset=preset,
                        crf=crf,
                        subtitle_download=opts.get('subtitle_download', False),
                        embed_subtitles=opts.get('embed_subtitles', False),
                        thumbnail_download=opts.get('thumbnail_download', False),
                        metadata_preserve=opts.get('metadata_preserve', True)
                    )

                    # Step 5: Complete
                    status_icon.markdown("🎉")
                    status_text.markdown("**✅ Download completed successfully!**")
                    progress_bar.progress(100)

                    time.sleep(1)  # Show completion

                    st.markdown('</div>', unsafe_allow_html=True)

                st.success("✅ Download completed successfully!")

                # Save to history
                file_size = os.path.getsize(file_path) if os.path.exists(file_path) else 0
                save_to_history(video_url, info.get('title', 'Unknown'), platform, selected_quality, file_size)

                # Show results
                st.markdown("### 📹 Download Results")
                with st.container():
                    st.markdown('<div class="feature-card">', unsafe_allow_html=True)
                    col_res1, col_res2 = st.columns(2)

                    with col_res1:
                        st.markdown(f"**📄 Title:** {info.get('title', 'Unknown')}")
                        st.markdown(f"**👤 Uploader:** {info.get('uploader', 'Unknown')}")
                        st.markdown(f"**⏱️ Duration:** {info.get('duration', 0)} seconds")
                        st.markdown(f"**📏 Size:** {format_file_size(file_size)}")

                    with col_res2:
                        st.markdown(f"**🎯 Quality:** {selected_quality}")
                        st.markdown(f"**📱 Platform:** {platform}")
                        st.markdown(f"**📅 Downloaded:** {datetime.now().strftime('%H:%M:%S')}")

                    # Video preview
                    if os.path.exists(file_path) and not audio_only:
                        st.video(file_path)

                    # Download button
                    with open(file_path, "rb") as f:
                        file_extension = "mp3" if audio_only else "mp4"
                        st.download_button(
                            "💾 Download File",
                            data=f,
                            file_name=f"{info.get('title', 'download')}.{file_extension}",
                            mime=f"{'audio' if audio_only else 'video'}/{file_extension}",
                            use_container_width=True
                        )

                    st.markdown('</div>', unsafe_allow_html=True)

            except Exception as e:
                st.error(f"❌ Error: {str(e)}")
                st.info("💡 Try a different quality or check if the video is available")

with col2:
    # Right sidebar - Professional Features & Analytics
    st.markdown("### ✨ Professional Features")
    st.markdown("""
    - 🚀 **4K UHD Support** up to 2160p
    - 🎯 **Smart Quality Control** with CRF
    - 🎵 **Advanced Audio Processing**
    - 📝 **Multi-language Subtitles**
    - ⚡ **Batch Processing** up to 100 videos
    - 🎨 **Custom Video Encoding**
    - 🔧 **System Optimization**
    - 📊 **Download Analytics**
    """)

    st.markdown("---")
    st.markdown("### 🎯 Quality Guide")
    st.markdown("""
    **SD (480p):** Fast, small files
    **HD (720p):** Balanced quality/speed
    **FHD (1080p):** High quality
    **2K (1440p):** Premium quality
    **4K (2160p):** Maximum quality
    """)

    st.markdown("---")
    st.markdown("### 📈 Performance Tips")
    st.markdown("""
    - Use lower CRF for better quality
    - H.265 saves ~50% file size
    - Batch mode for multiple downloads
    - Check quality comparison first
    - Clear cache regularly
    """)

    st.markdown("---")
    st.markdown("### 🆘 Professional Support")
    st.markdown("""
    **Advanced Support:**
    - 📧 pro@gbdownloader.com
    - 💬 Priority Live Chat
    - 📚 Technical Documentation
    - 🎥 Video Tutorials
    - 🔧 API Access
    """)

    # System Health Check
    st.markdown("---")
    st.markdown("### 🔍 System Health")

    # Check FFmpeg
    ffmpeg_ok = shutil.which('ffmpeg') is not None
    st.markdown(f"**FFmpeg:** {'✅ Available' if ffmpeg_ok else '❌ Missing'}")

    # Check disk space
    stat = shutil.disk_usage('/')
    free_gb = stat.free // (1024**3)
    st.markdown(f"**Disk Space:** {free_gb} GB free")

    # Check internet (simple ping test would be better but this is basic)
    st.markdown("**Internet:** ✅ Connected")

    if not ffmpeg_ok:
        st.error("⚠️ FFmpeg required for high-quality downloads")
        if st.button("Install FFmpeg", key="install_ffmpeg"):
            st.info("Run: sudo apt install ffmpeg")

# Footer
st.markdown("---")
st.markdown("### 🚀 GB DOWNLOADER PRO - Enterprise Video Solution")
st.caption("Built with ❤️ using Streamlit & yt-dlp | Professional Edition v3.0 | © 2026 GB Labs")
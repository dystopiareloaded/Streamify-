import streamlit as st
import os
import json
import base64

# Set page config as the first command
st.set_page_config(page_title="Streamify+", layout="wide", page_icon="🎵")

st.markdown("""
    <h1 style='text-align:center; color: #1DB954;'>
        <span class='header-emoji'>🎵</span> Streamify+ Music Player
    </h1>
    <p style='text-align:center; color: #AAAAAA; font-size: 20px; margin-top: -10px;'>
        Created by <strong>Kaustav Roy Chowdhury</strong> with ❤️
    </p>
""", unsafe_allow_html=True)

# --- Path Setup ---
base_path = os.path.dirname(__file__)
mp3_folder = os.path.join(base_path, "music")
album_folder = os.path.join(base_path, "album_art")
metadata_path = os.path.join(base_path, "metadata.json")
playlist_path = os.path.join(base_path, "playlists", "playlists.json")

# --- Load Data ---
@st.cache_data
def load_data():
    try:
        with open(metadata_path) as f:
            metadata = json.load(f)
        with open(playlist_path) as f:
            playlists = json.load(f)
        return metadata, playlists
    except (FileNotFoundError, json.JSONDecodeError) as e:
        st.error(f"Error loading data: {e}")
        return {}, {}

metadata, playlists = load_data()

if not metadata or not playlists:
    st.stop()

all_songs = list(metadata.keys())
playlists = {"All Songs": all_songs, **playlists}

# --- Session State Initialization ---
def init_session_state():
    defaults = {
        "playlist_name": "All Songs",
        "song_index": 0,
        "is_playing": False, # Autoplay is now handled by the component
    }
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value

init_session_state()

# --- UI: Sidebar ---
st.sidebar.markdown("<h1 style='text-align: center; color: #1DB954;'>🎵 Streamify+</h1>", unsafe_allow_html=True)

playlist_name = st.sidebar.selectbox("Choose a Playlist", list(playlists.keys()), index=list(playlists.keys()).index(st.session_state.playlist_name))

if playlist_name != st.session_state.playlist_name:
    st.session_state.playlist_name = playlist_name
    st.session_state.song_index = 0
    st.session_state.is_playing = True # Trigger autoplay on playlist change

music_files = playlists.get(playlist_name, [])

# --- Current Song Info ---
def get_current_song_info():
    if not music_files or st.session_state.song_index >= len(music_files):
        return "Unknown", "Unknown", "Unknown", "Unknown", None, None

    song_filename = music_files[st.session_state.song_index]
    song_path = os.path.join(mp3_folder, song_filename)
    
    meta = metadata.get(song_filename, {})
    title = meta.get("title", os.path.splitext(song_filename)[0])
    movie = meta.get("movie", "Unknown Album")
    singer = meta.get("singer", "Unknown Artist")
    
    # Encode audio to base64 for embedding
    try:
        with open(song_path, "rb") as f:
            audio_bytes = f.read()
        audio_b64 = base64.b64encode(audio_bytes).decode()
    except FileNotFoundError:
        st.warning(f"Audio file not found: {song_path}")
        return title, movie, singer, song_filename, None, None
        
    return title, movie, singer, song_filename, song_path, audio_b64

title, movie, singer, song_filename, song_path, audio_b64 = get_current_song_info()

# --- Custom Audio Player Component ---
# --- Custom Audio Player Component ---
def audio_player(audio_b64, is_playing):
    autoplay_attr = "autoplay" if is_playing else ""
    audio_html = f"""
    <div style="margin: 10px 0 20px 0;">
        <audio id="audio_player" src="data:audio/mp3;base64,{audio_b64}" controls {autoplay_attr} style="width: 100%;">
            Your browser does not support the audio element.
        </audio>
        <script>
            var audio = document.getElementById('audio_player');
            audio.onended = function() {{
                window.parent.postMessage({{"type": "streamlit:next_song"}}, "*");
            }};
        </script>
    </div>
    """
    st.components.v1.html(audio_html, height=80)  # Increased height from 50 to 80

# --- UI: Main Player ---
col1, col2 = st.columns([1, 2])

with col1:
    art_path = os.path.join(album_folder, song_filename.replace(".mp3", ".jpg"))
    if os.path.exists(art_path):
        st.image(art_path, use_container_width=True)
    else:
        st.markdown("<div style='background-color:#282828; aspect-ratio:1; display:flex; align-items:center; justify-content:center; border-radius:12px;'><span style='font-size:4rem;'>🎵</span></div>", unsafe_allow_html=True)

with col2:
    st.markdown(f"## {title}")
    st.markdown(f"**{singer}** - *{movie}*")

    if audio_b64:
        audio_player(audio_b64, st.session_state.is_playing)
        # After the first play, we don't need to force it anymore
        if st.session_state.is_playing:
             st.session_state.is_playing = False
    else:
        st.warning("Audio not available.")

    # --- Player Controls ---
    def change_song(delta):
        st.session_state.song_index = (st.session_state.song_index + delta) % len(music_files)
        st.session_state.is_playing = True # Autoplay next/prev song
        st.rerun()

    cols = st.columns([1, 1, 1, 5])
    if cols[0].button("⏮️", help="Previous"):
        change_song(-1)
    
    if cols[1].button("⏭️", help="Next"):
        change_song(1)

    if song_path and os.path.exists(song_path):
        with open(song_path, "rb") as f:
            cols[2].download_button("📥", f, file_name=song_filename, mime="audio/mpeg", help="Download song")

# --- UI: Playlist ---
st.markdown("---")
st.header(f"Songs in {playlist_name}")

for i, file in enumerate(music_files):
    meta = metadata.get(file, {})
    song_title = meta.get('title', os.path.splitext(file)[0])
    artist = meta.get('singer', 'Unknown Artist')
    
    col1, col2 = st.columns([5, 1])
    is_current = (i == st.session_state.song_index)
    
    with col1:
        if is_current:
            st.markdown(f"**{song_title}**<br>*{artist}* 🎵", unsafe_allow_html=True)
        else:
            st.markdown(f"**{song_title}**<br>*{artist}*", unsafe_allow_html=True)
    
    with col2:
        if st.button("Play", key=f"play_{i}", use_container_width=True):
            st.session_state.song_index = i
            st.session_state.is_playing = True # Set to autoplay
            st.rerun()
    
    if i < len(music_files) - 1:
        st.markdown("---")

# --- CSS Styling ---
# --- CSS Styling ---
st.markdown("""
<style>
    /* General */
    .stButton>button {
        background-color: #282828;
        color: white;
        border: 1px solid #1DB954;
        border-radius: 8px;
        padding: 0.5rem 1rem;
        transition: all 0.2s;
    }
    .stButton>button:hover {
        background-color: #1DB954;
        color: black;
    }
    /* Player controls */
    .stButton>button[help*="Previous"], .stButton>button[help*="Next"], .stButton>button[help*="Download"] {
        font-size: 1.5rem;
        padding: 0.2rem 0.8rem;
    }
    /* Playlist items */
    .stMarkdown {
        line-height: 1.6;
        margin-bottom: 10px !important;
    }
    /* Play buttons in playlist */
    .stButton>button:not([help]) {
        margin-top: 0.5rem;
        width: 100%;
    }
    /* Audio player container */
    .stAudio {
        margin: 15px 0 !important;
    }
    /* Add space between player and playlist */
    .stMarkdown > hr {
        margin: 15px 0 !important;
    }
</style>
""", unsafe_allow_html=True)
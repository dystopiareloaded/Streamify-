# 🎵 Streamify+ Music Player

!(streamify-logo.jog)

A modern, clean, and minimal **MP3 music player web app** built using **Streamlit**.  
Upload your own songs, browse playlists, display album art, and enjoy a smooth audio player experience — all in your browser.

---

## ✨ Features

- 🎧 Playlist Selection (Predefined or All Songs)
- 🖼️ Album Art Display
- ⏮️⏭️ Previous/Next Song Controls
- 📥 Download Songs
- Responsive UI with custom CSS styling

---

## 📸 App Screenshots

| Home View                       | Playlist View                      | Album Art & Player                |
|---------------------------------|------------------------------------|-----------------------------------|
| ![](assets/screenshot-1.png)    | ![](assets/screenshot-2.png)       | ![](assets/screenshot-3.png)      |

---

## 🚀 How to Run Locally

### 1️⃣ Prerequisites:
- Python 3.8+
- Streamlit installed:  
  ```bash
  pip install streamlit

# 2️⃣ Project Structure:

streamify/
│
├── streamlit_app.py      # Main Streamlit app file
├── music/                # MP3 files folder
├── album_art/            # Album art images (.jpg)
├── playlists/            # Playlists JSON folder
│   └── playlists.json
├── metadata.json         # Metadata for all songs
├── assets/               # Screenshots for README and branding
└── requirements.txt      # Python dependencies

# 3️⃣ Launch App:


# 🛠️ Project Setup Details

- Framework: Streamlit

- Frontend Customization:

- HTML Markup using st.markdown()

- CSS for button styling and layout

- Audio Handling:

- st.audio() component using local MP3 files

- State Management:

- st.session_state for tracking song index, play status, etc.

# ❤️ Author
- Created with love by Kaustav Roy Chowdhury

- 💡 "Turning raw numbers into real business stories."




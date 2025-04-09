# 🎵 Lofi Music Generator 🎵

Transform your favorite songs into dreamy lofi versions with reverb, rain effects, pitch shift, and more — all through a sleek and easy-to-use web app built with Flask.

![UI Preview](ui_preview.jpg)

---

## 🚀 Features

🎶 Upload any `.mp3` file  
🎛️ Control:
- Playback Speed
- Pitch Shift
- Reverb

🔊 Add Extra Effects:
- Echo  
- Bass Boost  
- Distortion  

🌧️ Add Rain FX with volume control  
🎤 Karaoke Remover (Vocal remover)  
🎼 Preset Selection (Chill, Vintage, Deepnight)

---

## 🖥️ Technologies Used

- Python 3.7+
- Flask (for the web framework)
- Pydub (for audio processing)
- FFMPEG (required by Pydub to process audio)

---

## 📂 Project Structure

`lofi-music-generator/ ├── app.py ├── requirements.txt ├── ui_preview.jpg ← Your UI screenshot here ├── static/ │ ├── uploads/ ← Uploaded audio files │ ├── processed/ ← Output after processing │ └── rain.mp3 ← Optional rain background sound ├── templates/ │ └── index.html ← HTML UI └── README.md`

---

## ⚙️ Installation

### 1. Clone the repository

```bash
git clone https://github.com/your-username/lofi-music-generator.git
cd lofi-music-generator

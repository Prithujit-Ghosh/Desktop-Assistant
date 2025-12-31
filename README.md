# Jarvis – Voice Controlled AI Assistant 🎙️🤖

Jarvis is a Python-based voice assistant that can recognize speech, respond with text-to-speech, fetch real-time information (weather, news, AI answers), and launch applications on your computer. It integrates multiple APIs and libraries to provide a hands-free, interactive experience.

---

## ✨ Features
- **Voice Recognition**: Uses `speech_recognition` to capture and understand spoken commands.
- **Text-to-Speech**: Speaks responses using `pyttsx3`.
- **AI Responses**: Connects to Google Gemini API for conversational replies.
- **Weather Updates**: Fetches live weather data from OpenWeatherMap.
- **News Headlines**: Retrieves top headlines from NewsAPI.
- **System Control**: Opens apps like Calculator, Notepad, Paint, File Explorer, Command Prompt, PowerShell, Edge, Photos, Clock, Recycle Bin.
- **Music Playback**: Plays songs from a custom `musicLibrary`.
- **Screenshots**: Captures and saves screenshots automatically.
- **Date & Time**: Announces current time and date.

---

## 🛠️ Tech Stack
- **Python 3.9+**
- Libraries:
  - `speech_recognition`
  - `pyttsx3`
  - `webbrowser`
  - `requests`
  - `re`
  - `os`
  - `pyautogui`
  - `datetime`
  - `time`
  - `python-dotenv`

---

## 🔑 API Keys
Jarvis uses external APIs for AI, weather, and news:
- **Gemini API** (Google Generative Language)
- **OpenWeatherMap API**
- **NewsAPI**
---
## 🧩 Project Structure

```
Repo
├── main.py          # Main assistant script
├── musicLibrary.py    # Custom music links
├── requirements.txt   # Dependencies
└── README.md          # Documentation
```

---
## 📌 **Notes**
- Works best on Windows (uses os.system("start ...") for app launching).
- Requires a working microphone for speech recognition.
- Internet connection needed for API calls (Gemini, Weather, News).

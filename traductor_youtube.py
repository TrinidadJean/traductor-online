import yt_dlp
import whisper
import ffmpeg
from deep_translator import GoogleTranslator
from gtts import gTTS
import pygame
import os

# URL del video de YouTube
video_url = "https://m.youtube.com/watch?v=W8AspkUCnkg"

# Descargar solo el audio
ydl_opts = {
    'format': 'bestaudio/best',
    'cookiefile': 'cookies.txt',
    'postprocessors': [{
        'key': 'FFmpegExtractAudio',
        'preferredcodec': 'mp3',
        'preferredquality': '192',
    }],
    'outtmpl': 'audio.mp3'
}

with yt_dlp.YoutubeDL(ydl_opts) as ydl:
    ydl.download([video_url])

# Cargar modelo de Whisper
model = whisper.load_model("small")

# Transcribir audio
result = model.transcribe("audio.mp3")
original_text = result["text"]

# Traducir al español
translated_text = GoogleTranslator(source="auto", target="es").translate(original_text)

# Convertir a voz en español
tts = gTTS(translated_text, lang="es")
tts.save("audio_es.mp3")

# Silenciar el audio original (opcional)
os.system("ffmpeg -i audio.mp3 -af volume=0 audio_muted.mp3 -y")

# Reproducir la traducción
pygame.mixer.init()
pygame.mixer.music.load("audio_es.mp3")
pygame.mixer.music.play()

while pygame.mixer.music.get_busy():
    continue

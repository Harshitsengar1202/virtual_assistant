import pyaudio
import wave
import librosa
import numpy as np
from shazamio import Shazam
import os
from pydub import AudioSegment
from pydub.utils import make_chunks
import asyncio
import pyttsx3

def SpeakText(command):
    """Initializes the text-to-speech engine and speaks the given command."""
    engine = pyttsx3.init()
    voices = engine.getProperty('voices')
    engine.setProperty('voice', voices[1].id)  # Use a different voice if desired
    engine.say(command)
    engine.runAndWait()

# Step 1: Record Audio
def record_audio(filename, duration=10, rate=44100, channels=1):
    """Records audio from the microphone and saves it as a .wav file."""
    chunk = 1024  # Buffer size
    format = pyaudio.paInt16  # 16-bit resolution
    audio = pyaudio.PyAudio()

    print("Recording...")
    SpeakText("Recording audio. Please speak.")
    stream = audio.open(format=format, channels=channels,
                        rate=rate, input=True,
                        frames_per_buffer=chunk)
    frames = []

    for _ in range(0, int(rate / chunk * duration)):
        data = stream.read(chunk)
        frames.append(data)

    print("Recording complete.")
    SpeakText("Recording Complete.")

    stream.stop_stream()
    stream.close()
    audio.terminate()

    # Save the recorded audio to a file
    with wave.open(filename, 'wb') as wf:
        wf.setnchannels(channels)
        wf.setsampwidth(audio.get_sample_size(format))
        wf.setframerate(rate)
        wf.writeframes(b''.join(frames))

# Step 2: Analyze Audio
def analyze_audio(filename):
    """Extracts features from the audio file using librosa."""
    print("Analyzing audio...")
    SpeakText("Analyzing audio. One moment.")
    y, sr = librosa.load(filename, sr=None)  # Load the audio file

    # Extract features
    pitch_contour = librosa.yin(y, fmin=librosa.note_to_hz('C2'), fmax=librosa.note_to_hz('C7'))
    tempo, _ = librosa.beat.beat_track(y=y, sr=sr)
    mfccs = librosa.feature.mfcc(y=y, sr=sr)

    print(f"Pitch contour extracted: {pitch_contour[:10]}")  # Print first 10 values for brevity
    print(f"Tempo: {tempo}")
    print(f"MFCCs shape: {mfccs.shape}")

    return {
        "pitch_contour": pitch_contour,
        "tempo": tempo,
        "mfccs": mfccs
    }

# Step 3: Search for a Match Using ShazamIO
async def search_song(filename):
    """Searches for a song match using ShazamIO."""

    print("Searching for a match...")
    #SpeakText("Searching Shazam...")
    shazam = Shazam()

    try:
        ffmpeg_path = "C:\\Users\\Harshit\\AppData\\Local\\Microsoft\\WinGet\\Links"  # Your actual path
        os.environ["PATH"] += os.pathsep + ffmpeg_path  # Add to path

        AudioSegment.converter = os.path.join(ffmpeg_path, "ffmpeg.exe")
        AudioSegment.ffprobe = os.path.join(ffmpeg_path, "ffprobe.exe")
        os.environ["TFLITE_GPU_INFERENCE"] = "0"
        os.environ["TFLITE_CPU_ONLY"] = "1"
        
        out = await shazam.recognize(filename)  # Use 'recognize' instead of 'recognize_song'

        if "track" in out:
            track_info = out["track"]
            print(f"Song Found: {track_info['title']} by {track_info['subtitle']}")
            SpeakText(f"Song Found: {track_info['title']} by {track_info['subtitle']}")
            return track_info
        else:
            print("No match found.")
            SpeakText("No song found, Sorry!")
            return None

    except Exception as e:
        print(f"Error during song recognition: {e}")
        SpeakText("Sorry, there was an error identifying the song.")
        return None

async def process_audio(audio_file):
    """Processes the audio file, analyzes it, and searches for a match."""
    # Step 2: Analyze the recorded audio
    features = analyze_audio(audio_file)

    # Step 3: Search for a match using ShazamIO
    track_info = await search_song(audio_file)
    
    return track_info

def main():
    """Main function to coordinate audio recording, analysis, and song search."""
    import asyncio

    # Step 1: Record audio and save it as a .wav file
    audio_file = "recorded_audio.wav"
    record_audio(audio_file, duration=10)

    # Process the audio file
    asyncio.run(process_audio(audio_file))

# Main execution block
if __name__ == "__main__":
    import asyncio
    SpeakText("Hello! I'll try to figure out which song is playing!")
    main()

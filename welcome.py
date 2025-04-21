import speech_recognition as sr
import pyttsx3
import wikipedia
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import webbrowser
import os
import subprocess
import winapps
import psutil
import asyncio
import audio_analyzer
import time
import requests

def SpeakText(command):
    engine = pyttsx3.init()
    voices = engine.getProperty('voices')
    engine.setProperty('voice', voices[1].id)
    engine.say(command)
    engine.runAndWait()

def search(command):
    search_string = command
    chrome_options = Options()
    chrome_options.add_experimental_option("detach", True)
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)
    driver.maximize_window()
    driver.get("https://www.google.com/search?q=" + search_string)
    return driver

def play_song(command):
    search_string = command
    chrome_options = Options()
    chrome_options.add_experimental_option("detach", True)
    chrome_options.add_argument("user-data-dir=C:\\Temp\\ChromeProfile")  # use a real browser profile
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-extensions")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--start-maximized")

    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)
    driver.get("https://www.youtube.com/results?search_query=" + search_string)

    try:
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, '//ytd-video-renderer//a[@id="video-title"]'))
        )
        first_video = driver.find_element(By.XPATH, '//ytd-video-renderer//a[@id="video-title"]')
        first_video.click()
        print(f"Playing the song: {search_string}")
        SpeakText(f"Playing the song: {search_string}")
    except Exception as e:
        print(f"Error playing song: {e}")
        SpeakText("Sorry, I couldn't play the song.")


def wiki(command):
    random_array = ["for", "search", "on", "wikipedia", "this"]
    query = [x for x in command.split() if x not in random_array]
    query = " ".join(query)
    try:
        result = wikipedia.summary(query, sentences=2, auto_suggest=False, redirect=True)
        print(result)
        SpeakText(result)
    except wikipedia.exceptions.PageError:
        print("Page not found on Wikipedia.")
        SpeakText("Sorry, I couldn't find that on Wikipedia.")
    except wikipedia.exceptions.DisambiguationError as e:
        print(e)
        SpeakText("There are multiple options for that query. Please be more specific.")

def process():
    global MyText
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        r.adjust_for_ambient_noise(source, duration=0.5)
        audio = r.listen(source)
    try:
        print("Recognizing...")
        MyText = r.recognize_google(audio).lower()
        print("You said: " + MyText)
        return MyText
    except sr.UnknownValueError:
        print("Could not understand audio")
        SpeakText("Sorry, I didn't catch that.")
        return ""
    except sr.RequestError as e:
        print(f"Speech recognition error: {e}")
        SpeakText("Sorry, I'm having trouble connecting to the internet.")
        return ""

def find_app(name):
    possible_locations = [
        os.path.join(os.getenv("PROGRAMFILES"), name, f"{name}.exe"),
        os.path.join(os.getenv("PROGRAMFILES(X86)"), name, f"{name}.exe"),
        os.path.join(os.getenv("LOCALAPPDATA"), name, f"{name}.exe"),
    ]
    for location in possible_locations:
        if os.path.exists(location):
            return location
    for root, _, files in os.walk("C:\\"):
        for file in files:
            if file.lower() == f"{name}.exe":
                return os.path.join(root, file)
    print(f"Could not find {name} on your system.")
    return None

def open_app(name):
    app_path = find_app(name)
    if app_path:
        try:
            subprocess.Popen(app_path)
            print(f"Running {name} at path: {app_path}")
            SpeakText(f"Opening {name}")
        except Exception as e:
            print(f"Failed to run {name}: {e}")
            SpeakText(f"Sorry, I couldn't open {name}.")
    else:
        print(f"Could not find the installation path of {name}")
        SpeakText(f"Sorry, I couldn't find {name} on your computer.")

async def identify_song():
    audio_file = "recorded_audio.wav"
    audio_analyzer.record_audio(audio_file, duration=16)
    track_info = await audio_analyzer.process_audio(audio_file)
    if track_info:
        print(f"Found song: {track_info['title']} by {track_info['subtitle']}")
        SpeakText(f"Found the song: {track_info['title']} by {track_info['subtitle']}")
    else:
        print("No song found.")
        SpeakText("Sorry, I couldn't identify the song.")


def ask_groq(prompt):
    headers = {
        "Authorization": "Bearer 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",  
        "Content-Type": "application/json"
    }

    data = {
        "model": "llama3-8b-8192",
        "messages": [
            {"role": "user", "content": prompt}
        ]
    }

    try:
        response = requests.post("https://api.groq.com/openai/v1/chat/completions", headers=headers, json=data)
        reply = response.json()["choices"][0]["message"]["content"]
        print("\n Groq says:\n" + reply + "\n")

    except Exception as e:
        print(f"Groq error: {e}")
        SpeakText("Sorry, I couldn't get a response from Groq.")



if __name__ == "__main__":
    import logging
    logging.getLogger("selenium").setLevel(logging.ERROR)
    logging.getLogger("pdh").setLevel(logging.ERROR)

    MyText = None
    SpeakText("Hello, how can I help you?")

    while True:
        MyText = process()
        if not MyText:
            continue

        if 'wikipedia' in MyText:
            wiki(MyText)
            time.sleep(3)
            continue

        elif 'bye' in MyText or 'exit' in MyText or 'quit' in MyText or 'ok thanks' in MyText:
            SpeakText("Goodbye!")
            exit()

        elif 'open' in MyText:
            temp = MyText.split()
            if len(temp) > 1:
                app_name = temp[1]
                open_app(app_name)
            else:
                SpeakText("Please tell me which application you want to open.")
            time.sleep(5)
            break

        elif 'search' in MyText or 'tell me' in MyText or 'what is' in MyText:
            search_term = MyText.replace('search', '', 1).strip()
            if search_term:
                search(search_term)
            else:
                SpeakText("What do you want me to search for?")
            time.sleep(5)
            break
        elif 'play' in MyText:
            search_term = MyText.replace('play', '', 1).strip()
            if search_term:
                play_song(search_term)
            else:
                SpeakText("What do you want me to play?")
            break

        elif ('which song' in MyText or
              'what song' in MyText or
              'identify this song' in MyText or
              'find this song' in MyText):
            asyncio.run(identify_song())
            time.sleep(3)
            continue

        else:
            ask_groq(MyText)
            time.sleep(3)
            continue

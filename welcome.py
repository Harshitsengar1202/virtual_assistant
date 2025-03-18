import speech_recognition as sr
import pyttsx3
import wikipedia
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
import webbrowser
import os
import subprocess
import winapps
import psutil
import asyncio  # Import asyncio
import audio_analyzer

def SpeakText(command):
    """Initializes the text-to-speech engine and speaks the given command."""
    engine = pyttsx3.init()
    voices = engine.getProperty('voices')
    engine.setProperty('voice', voices[1].id)  # Use a different voice if desired
    engine.say(command)
    engine.runAndWait()

def search(command):
    """Searches Google for the given command using Selenium."""
    search_string = command
    chrome_options = Options()
    chrome_options.add_experimental_option("detach", True)  # Keep browser open
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)
    driver.maximize_window()
    driver.get("https://www.google.com/search?q=" + search_string)
    return driver

def wiki(command):
    """Searches Wikipedia for the given command and speaks a summary."""
    random_array = ["for", "search", "on", "wikipedia", "this"]
    query = [x for x in command.split() if x not in random_array]
    query = " ".join(query)
    try:
        # Use auto_suggest=False to prevent suggestions
        # Use sentences=2 to get the first 2 sentences
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
    """Listens for audio input and converts it to text using Google Speech Recognition."""
    global MyText
    r = sr.Recognizer()  # Create a new recognizer instance each time
    with sr.Microphone() as source:
        print("Listening...")
        r.adjust_for_ambient_noise(source, duration=0.2)
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
        print("Could not request results from Google Speech Recognition service; {0}".format(e))
        SpeakText("Sorry, I'm having trouble connecting to the internet.")
        return ""

def find_app(name):
    """Attempts to find the executable path of an application by directly searching for .exe files."""
    # Try to find the executable by searching in common program locations
    possible_locations = [
        os.path.join(os.getenv("PROGRAMFILES"), name, f"{name}.exe"),
        os.path.join(os.getenv("PROGRAMFILES(X86)"), name, f"{name}.exe"),
        os.path.join(os.getenv("LOCALAPPDATA"), name, f"{name}.exe"),
    ]

    for location in possible_locations:
        if os.path.exists(location):
            return location

    # If not found in standard program directories, search the entire system for a matching executable.
    for root, _, files in os.walk("C:\\"):  # Search from C drive
        for file in files:
            if file.lower() == f"{name}.exe":
                return os.path.join(root, file)

    print(f"Could not find {name} on your system.")
    return None

def open_app(name):
    """Opens the application with the given name."""
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
        SpeakText("Please Speak the command. What's the song. or Identify the song.")
        song_search=process()
        audio_file = "recorded_audio.wav"
        audio_analyzer.record_audio(audio_file, duration=3)

        #Run the audio analysis and search asynchronously
        track_info = await audio_analyzer.process_audio(audio_file)

        if track_info:
            print(f"Found song in my script: {track_info['title']} by {track_info['subtitle']}")
        else:
            print("No song found in my script.")

# Main program loop
if __name__ == "__main__":
    MyText = None
    mytext = "Hello, how can I help you?"
    SpeakText(mytext)

    while True:
        MyText = process()
        if not MyText:
            continue  # If process() returns an empty string, restart the loop

        if 'wikipedia' in MyText:
            print(MyText)
            wiki(MyText)
            break
        elif 'bye' in MyText or 'exit' in MyText or 'quit' in MyText:
            SpeakText("Goodbye!")
            exit()
        elif 'open' in MyText:
            print(MyText)
            temp = MyText.split()
            if len(temp) > 1:
                app_name = temp[1]
                open_app(app_name)
                break
            else:
                SpeakText("Please tell me which application you want to open.")
                break
        elif 'search' in MyText or 'tell me about' in MyText or 'what is' in MyText:
            search_term = MyText.replace('search', '', 1).strip()  # remove "search" from the string
            if search_term:
                print("Results for " + search_term)
                search(search_term)
                break
            else:
                SpeakText("What do you want me to search for?")
                break
        elif 'which song' in MyText or 'what song' in MyText or 'identify this song' in MyText:
           asyncio.run(identify_song())
           break   
        else:
            print("Results for " + MyText)
            search(MyText)
            break

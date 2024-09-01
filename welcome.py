import tkinter as tk
from gtts import gTTS
from playsound import playsound
import os
import subprocess
import speech_recognition as sr
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
import pyttsx3
import wikipedia
from selenium import webdriver
import googlesearch
from PIL import Image, ImageTk
from itertools import count
import time
import pyautogui
import winapps

def SpeakText(command):
    engine = pyttsx3.init()
    voice = engine.getProperty('voices')
    engine.setProperty('voice', voice[1].id)
    engine.say(command)
    engine.runAndWait()

def search(command):
    search_string = command
    s=Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=s)
    driver.maximize_window()
    driver.get("https://www.google.com/search?q=" + search_string + "&start=" + str(0))
    return driver

def wiki(command):
    import random
    random_array=["for","search","on","wikipedia","this"]
    query=[x for x in command.split() if x not in random_array]
    try:
        wiki=wikipedia.page(query,auto_suggest=False)
    except wikipedia.DisambiguationError as e:
        s=random.choice(e.options)
        wiki=wikipedia.page(s,auto_suggest=False)

    result=wikipedia.summary(wiki)
    print(result)
    result2=wikipedia.summary(command,sentences=2)
    print(result)
    SpeakText(result2)

    
'''
def wiki(command):
    random_array=["for","search","on","wikipedia","this"]
    query=[x for x in command.split() if x not in random_array]
    query=" ".join(query)
    search_string = query
    s=Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=s)
    driver.maximize_window()
    driver.get('https://en.wikipedia.org/wiki/'+ search_string)
    return driver
'''


def process():
    global MyText
    n=1
    while(n):
        try:
            with sr.Microphone() as source2:
                r.adjust_for_ambient_noise(source2, duration=0.2)
                audio2 = r.listen(source2)
                MyText = r.recognize_google(audio2)
                MyText = MyText.lower()
                n=0
                return MyText
        except sr.RequestError as e:
            print("Could not request results; {0}".format(e))
        except sr.UnknownValueError:
            print("unknown error occured")

def find_app(name):
    for item in winapps.search_installed(name):
        if hasattr(item, 'install_location'):
            return str(item.install_location)
    return None

MyText=None
mytext='Hello Harshit How can I help you'
r = sr.Recognizer()
SpeakText(mytext)
MyText=process()
if 'wikipedia' in MyText:
    print(MyText)
    driver=wiki(MyText)
elif 'bye' in MyText:
    exit()
elif 'open' in MyText:
    print(MyText)
    temp=MyText.split()
    x=temp[1]
    app_path=find_app(x)
    if app_path:
        try:
            # Run the executable at the specified path
            executable_path = os.path.join(app_path, x + '.exe')
            if os.path.exists(executable_path):
                subprocess.Popen(executable_path)
                print(f"Running {x} at path: {executable_path}")
            else:
                print(f"Could not find the executable {x}.exe at path: {app_path}")
        except Exception as e:
            print(f"Failed to run {x}: {e}")
    else:
        print(f"Could not find the installation path of {x}")
else:
    print("Results for "+MyText)
    driver=search(MyText)

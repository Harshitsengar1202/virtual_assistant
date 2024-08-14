from tkinter import *
from gtts import gTTS
from playsound import playsound
import os
import speech_recognition as sr
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
import pyttsx3
import wikipedia
#import webbrowser as web
from selenium import webdriver
import googlesearch
import tkinter as tk
#from PIL import Image, ImageTk
from itertools import count
import time

def SpeakText(command):
    engine = pyttsx3.init()
    voice = engine.getProperty('voices')
    engine.setProperty('voice', voice[1].id)
    engine.say(command)
    engine.runAndWait()

def search(command):
    search_string = command
    s = Service(ChromeDriverManager().install())
    try:
        driver = webdriver.Chrome(service=s)
        driver.maximize_window()
        driver.get("https://www.google.com/search?q=" + search_string + "&start=" + str(0))
        return driver
    except Exception as e:
        print(f"An error occurred: {e}")
    #driver.find_element(By.NAME, 'q').send_keys(search_string)
    '''browser = webdriver.Chrome('D:\\chromedriver.exe')
    for i in range(1):
        matched_elements = browser.get("https://www.google.com/search?q=" +search_string + "&start=" + str(i))'''
    '''path = "C:/Program Files (x86)/Google/Chrome/Application/chrome.exe %s"
    web.get(path).open(command)'''
    #for j in googlesearch.search(command, tld="com", num=10, stop=10, pause=2):
        #print(j)

def wiki(command):
    result=wikipedia.summary(command)
    result2=wikipedia.summary(command,sentences=2)
    print(result)
    SpeakText(result2)

'''    
class ImageLabel(tk.Label):
    """a label that displays images, and plays them if they are gifs"""
    def load(self, im):
        if isinstance(im, str):
            im = Image.open(im)
        self.loc = 0
        self.frames = []

        try:
            for i in count(1):
                self.frames.append(ImageTk.PhotoImage(im.copy()))
                im.seek(i)
        except EOFError:
            pass

        try:
            self.delay = im.info['duration']
        except:
            self.delay = 100

        if len(self.frames) == 1:
            self.config(image=self.frames[0])
        else:
            self.next_frame()

    def unload(self):
        self.config(image="")
        self.frames = None

    def next_frame(self):
        if self.frames:
            self.loc += 1
            self.loc %= len(self.frames)
            self.config(image=self.frames[self.loc])
            self.after(self.delay, self.next_frame)



def animation():
    root = tk.Tk()
    lbl = ImageLabel(root)
    lbl.pack()
    lbl.load('myai.gif')
    b1=Button(root,text="Listen",command=process,height=30,width=80)
    b1.pack()
    logo=PhotoImage(file='mic.png')
    b1.config(image=logo,compound=LEFT)
    small_logo=logo.subsample(10,10)
    b1.config(image=small_logo)
    root.mainloop()
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

MyText=None
mytext='Hello Harshit How can I help you'
r = sr.Recognizer()
SpeakText(mytext)
#animation()
MyText=process()
if 'wikipedia' in MyText:
    print("Results for "+MyText)
    wiki(MyText)
elif 'bye' in MyText:
    exit()
elif 'open' in MyText:
    SpeakText('Trying to open the file')
    temp=MyText.split()
    x=temp[1]
    open(x+'.exe')
    time.sleep(3600)
else:
    print("Results for "+MyText)
    driver=search(MyText)

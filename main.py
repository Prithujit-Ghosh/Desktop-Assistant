import speech_recognition as sr
import webbrowser
import pyttsx3
import musicLibrary
import requests
import re
import os
import pyautogui
import datetime
import time
from dotenv import load_dotenv

r=sr.Recognizer()#creating an instance of speech recognizer class
engine=pyttsx3.init()#Constructs a new TTS engine instance

#loading environment variables from .env
load_dotenv()
GEMINI_API_KEY=os.getenv("GEMINI_API_KEY")
WEATHER_API_KEY=os.getenv("WEATHER_API_KEY")
NEWS_API_KEY=os.getenv("NEWS_API_KEY")

def speak(text):#Building the speak function
    engine.stop()
    engine.say(text)
    engine.runAndWait()

def ProcessByAI(command):
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key={GEMINI_API_KEY}"
    command_mod=command+". Please answer in short"
    data = {
        "contents": [
            {"parts": [{"text": command_mod}]}
        ],
        "generationConfig": {
            "maxOutputTokens": 1200,   #limit response length
            "temperature": 0.7        #creativity control
        }
    }

    response = requests.post(url, json=data)
    if response.status_code == 200:
        result = response.json()
        ai_reply = result["candidates"][0]["content"]["parts"][0]["text"]
        speak("AI:"+ ai_reply)
        print("AI:"+ai_reply)
    else:
        speak("Error from Gemini:"+ response.text)
        print("Error from Gemini:"+ response.text)
        speak("Sorry, I couldn't process that with AI.")

def safe_speak(text):
    if text:
        # Remove non-ASCII characters (like emojis)
        clean_text = re.sub(r'[^\x00-\x7F]+', ' ', text)
        # Replace problematic characters (newlines, tabs)
        clean_text = clean_text.replace("\n", " ").replace("\r", " ").replace("\t", " ")
        return clean_text.strip()
    
def get_weather(city="Kolkata"):
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={WEATHER_API_KEY}&units=metric"
    response = requests.get(url)
    if response.status_code == 200:
        print("status_code=200")
        data = response.json()
        temp = data["main"]["temp"]
        desc = data["weather"][0]["description"]
        return f"The temperature in {city} is {temp}°C with {desc}."
    else:
        return "Sorry, I couldn't fetch the weather right now."

def processCommand(command):
    if "open google" in command.lower():
        webbrowser.open("https://google.com")
    elif "open whatsapp" in command.lower():
        webbrowser.open("https://web.whatsapp.com")
    elif "open linkedin" in command.lower():
        webbrowser.open("https://linkedin.com")
    elif "open github" in command.lower():
        webbrowser.open("https://github.com")
    elif "open youtube" in command.lower():
        webbrowser.open("https://youtube.com")
    elif "open calculator" in command.lower():
        os.system("start calc")
    elif "open notepad" in command.lower():
        os.system("start notepad")
    elif "open onenote" in command.lower() or "open one note" in command.lower():
        os.system("start onenote")
    elif "open browser" in command.lower():
        os.system("start msedge")
    elif "open paint" in command.lower():
        os.system("start mspaint")
    elif "open file explorer" in command.lower():
        os.system("start explorer")
    elif "open command prompt" in command.lower():
        os.system("start cmd")
    elif "open powershell" in command.lower():
        os.system("start powershell")
    elif "open recycle bin" in command.lower():
        os.system("start shell:RecycleBinFolder")
    elif "open clock" in command.lower():
        os.system("start ms-clock:")
    elif "open photos" in command.lower():
        os.system("start ms-photos:")
    elif command.lower().startswith("play"):
        musi=command.lower().split(" ")[1]
        webbrowser.open(musicLibrary.music[musi])
    elif command.lower() == "take screenshot":
        screenshot=pyautogui.screenshot()
        filename=f"C:/Users/mrinm/OneDrive/Pictures/Screenshots/screenshot_{datetime.datetime.now().strftime("%Y_%m_%d_%H_%M_%S")}.png"
        screenshot.save(filename)
        speak("Screenshot has been taken.")
        print("Screenshot has been taken.")
    elif command.lower() == "what is the time":
        time_str=datetime.datetime.now().strftime("%H:%M:%S")
        print(time_str)
        speak(f"It's now {time_str}")
    elif "what date is it" in command.lower():
        strfDate = datetime.datetime.now().strftime("%A, %B %d, %Y")
        speak(f"Today is {strfDate}")
        print(f"Today is {strfDate}")
    elif "temperature" in command.lower():
        # Default city or extract from command
        if "in" in command.lower():
            city = command.lower().split("in")[-1].strip()
        else:
            city = "Kolkata"  # default city
        weather_report = get_weather(city)
        print(weather_report)
        speak(weather_report)

    elif "headlines" in command.lower():
        response = requests.get(
            f"https://newsapi.org/v2/top-headlines?country=us&apiKey={NEWS_API_KEY}"
        )
        if response.status_code == 200:
            print("Showing headlines...")
            data = response.json()
            if data.get("totalResults")==0:
                speak("No headlines available")
            else:
                Headline_list=[]
                for item in data["articles"]:
                    headline = item.get("title", "")
                    Headline_list.append(safe_speak(headline))
                combined_headlines=". Next headline: ".join(Headline_list)
                speak(combined_headlines)
                print(combined_headlines)
        else:
            speak("Sorry, fail to fetch news")
    else:
        ProcessByAI(command)


if __name__=="__main__":
    speak("Initializing Jarvis...")
    flag=True
    while flag:
        print("recognizing..")
        try:
            with sr.Microphone() as source:
                print("Listening...")
                audio=r.listen(source,timeout=3,phrase_time_limit=2)
            word=r.recognize_google(audio)
            print(word)
            if ("shutdown" in word.lower() or "shut down" in word.lower()):
                speak("Goodbye")
                time.sleep(1)
                print("Goodbye")
                break
            elif (word.lower()=="jarvis"):
                print("About to speak 'Ya'")
                engine.say("Ya")
                with sr.Microphone() as source:
                    
                    print("Jarvis active...")
                    audio=r.listen(source,timeout=3,phrase_time_limit=6)
                    command=r.recognize_google(audio)
                    print("command received:",command)
                    if (command.lower()=="shutdown" or command.lower()=="shut down"):
                        speak("Goodbye")
                        time.sleep(1)
                        print("Goodbye")
                        break
                    processCommand(command)
        except sr.WaitTimeoutError:
            print("Sorry, I didn't hear anything")
        except sr.UnknownValueError:
            print("Can't understand the audio")
        except sr.RequestError as e:
            print(f"Error: {e}")
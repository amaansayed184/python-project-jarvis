import speech_recognition as sr
import pyttsx3
import webbrowser
import datetime
from time import sleep
import pyautogui
import pyfreeze
import time as tt
import random
import psutil
recognizer = sr.Recognizer()
engine = pyttsx3.init()

def speak(text):
    engine.say(text)
    engine.runAndWait()

def sendmsg(phone_no, message):
    try:
        url = f'https://web.whatsapp.com/send?phone={phone_no}&text={message}'
        webbrowser.open(url)
        sleep(10)  # Increase sleep time for loading
        pyautogui.press('enter')
        speak("Message sent successfully.")
    except Exception as e:
        print(f"Error sending message: {e}")
        speak("Failed to send the message.")
def battery():
    battery=psutil.sensors_battery()
    percent=battery.percent
    status= battery.power_plugged
    speak( "your battery percentage is "+ str(percent))
    if status==True:
        speak("and your device is on charging")
    else:
        speak("and your device is not on charging")
def screenshot():
    name_img= tt.time()
    name_img=f'D:\\progg lang\\python\\venv\\screenshot\\{name_img}.png'
    img=pyautogui.screenshot(name_img)
    img.show()
def flip():
    speak("flipping a coin")
    coin=['heads','tails']
    toss= random.choice(coin)
    speak("i flipped the coin and you got " + toss)
def die():
    speak("rolling a die")
    die=['1','2','3','4','5','6']
    toss= random.choice(die)
    speak("i rolled die and you got " + toss)
def processCommand(c):
    if "google" in c.lower():
        webbrowser.open("https://google.com")
    elif "youtube" in c.lower():
        webbrowser.open("http://youtube.com") #corrected youtube address
    elif "linkedin" in c.lower():
        webbrowser.open("https://linkedin.com")
    elif "movies" in c.lower():
        webbrowser.open("https://moviesmod.gift")
    elif "instagram" in c.lower():
        webbrowser.open("https://instagram.com")
    elif "screenshot" in c.lower():
        screenshot()
    elif "die" in c.lower():
        die()
    elif "battery" in c.lower():
        battery()
    
    elif "time" in c.lower():
        times = datetime.datetime.now().strftime("%I:%M:%S")
        speak(times)
    elif "flip" in c.lower():
        flip()
    elif "message" in c.lower():
        user_name = {
            'john': '+9184XXXXXXXX',
            'alex': '+919307788197'}

        try:
            speak("To whom do you want to send a message?")
            with sr.Microphone() as source:
                audio = recognizer.listen(source, timeout=3000, phrase_time_limit=3000)
                name = recognizer.recognize_google(audio).lower().strip()

            if name in user_name:
                phone_no = user_name[name]
                speak("What is the message?")
                with sr.Microphone() as source:
                    print("Listening for message...")
                    audio_msg = recognizer.listen(source, timeout=3000, phrase_time_limit=3000)
                message = recognizer.recognize_google(audio_msg)
                print(f"Recognized Message: {message}")
                sendmsg(phone_no, message)
                pyautogui.press('enter')
                
            else:
                speak("Person is not in the list.")
        except Exception as e:
            print(f"Error processing message: {e}")
            speak("Not able to send the message.")

if __name__ == "__main__":
    speak("Initializing Jarvis...")
    while True:
        r = sr.Recognizer()
        print("Recognizing...")
        try:
            with sr.Microphone() as source:
                print("Listening...")
                audio = r.listen(source, timeout=3000, phrase_time_limit=3000)
                word = r.recognize_google(audio)
                if word.lower() == "hello":
                    speak("Yes sir.")
                    with sr.Microphone() as source:
                        print("Jarvis activated...")
                        audio = r.listen(source)
                        command = r.recognize_google(audio)
                        processCommand(command)
        except Exception as e:
            print(f"Error: {e}")

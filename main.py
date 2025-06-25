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
import requests # Added for weather API

recognizer = sr.Recognizer()
engine = pyttsx3.init()

# --- Weather Functionality ---
OPENWEATHERMAP_API_KEY = "YOUR_API_KEY_HERE" # IMPORTANT: Replace with your OpenWeatherMap API key

def get_weather(city_name):
    """Fetches weather information for a given city using OpenWeatherMap API."""
    if OPENWEATHERMAP_API_KEY == "YOUR_API_KEY_HERE":
        return "Weather API key not configured. Please set it up in the script by replacing YOUR_API_KEY_HERE with your actual key."

    base_url = "http://api.openweathermap.org/data/2.5/weather"
    params = {
        "q": city_name,
        "appid": OPENWEATHERMAP_API_KEY,
        "units": "metric"  # Use Celsius
    }
    try:
        response = requests.get(base_url, params=params)
        response.raise_for_status()  # Raise an exception for bad status codes (4xx or 5xx)
        weather_data = response.json()

        if weather_data.get("cod") == 200: # Check if 'cod' key exists and is 200
            main_weather = weather_data["weather"][0]["main"]
            description = weather_data["weather"][0]["description"]
            temp = weather_data["main"]["temp"]
            feels_like = weather_data["main"]["feels_like"]
            humidity = weather_data["main"]["humidity"]
            wind_speed = weather_data["wind"]["speed"]

            report = (
                f"Currently in {city_name}: {main_weather} ({description}). "
                f"Temperature is {temp}°C, feels like {feels_like}°C. "
                f"Humidity is {humidity}%, and wind speed is {wind_speed} meters per second."
            )
            return report
        elif str(weather_data.get("cod")) == "404": # API returns "404" as a string
            return f"Sorry, I couldn't find weather data for {city_name}. Please check the city name."
        else:
            # Log the actual error message from the API if available
            error_message = weather_data.get("message", "No specific error message provided by API.")
            return f"Sorry, I couldn't retrieve the weather. API Error Code: {weather_data.get('cod')}, Message: {error_message}"
    except requests.exceptions.HTTPError as http_err:
        # Handle specific HTTP errors like 401 for API key issues
        # Check if response object exists before accessing its attributes
        status_code = http_err.response.status_code if http_err.response is not None else "Unknown"
        if status_code == 401:
             # More informative message for API key issues
            return "Failed to get weather data. This might be due to an invalid or unauthorized API key. Please check your OpenWeatherMap API key and subscription."
        return f"HTTP error occurred: {http_err} (Status code: {status_code}). Could not fetch weather for {city_name}."
    except requests.exceptions.RequestException as req_err:
        # Catch other request-related errors (DNS failure, connection timeout, etc.)
        return f"A network request error occurred: {req_err}. Could not fetch weather for {city_name}."
    except KeyError as key_err:
        # Catch errors if the expected keys are not in the JSON response
        return f"Unexpected data format received from weather API: missing key {key_err}. Could not parse weather for {city_name}."
    except Exception as e:
        # Generic catch-all for other unexpected errors
        return f"An unexpected error occurred while fetching weather: {e}"

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
    name_img=f'D:\\progg lang\\python\\venv\\screenshot\\{name_img}.png' # Consider making this path relative or configurable
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
    elif "weather in" in c.lower():
        try:
            city = c.lower().split("weather in")[-1].strip()
            if city:
                weather_report = get_weather(city)
                speak(weather_report)
            else:
                speak("Please specify a city name for the weather forecast.")
        except Exception as e:
            print(f"Error getting weather: {e}")
            speak("Sorry, I encountered an error while trying to get the weather forecast.")
    elif "message" in c.lower():
        user_name = {
            'john': '+9184XXXXXXXX', # Example, replace with actual numbers or a better contact management
            'alex': '+9193XXXXXXXX'}

        try:
            speak("To whom do you want to send a message?")
            with sr.Microphone() as source:
                recognizer.adjust_for_ambient_noise(source) # Adjust for noise
                print("Listening for recipient's name...")
                audio = recognizer.listen(source, timeout=5, phrase_time_limit=5) # Adjusted timeout
            name = recognizer.recognize_google(audio).lower().strip()
            print(f"Recognized name: {name}")

            if name in user_name:
                phone_no = user_name[name]
                speak("What is the message?")
                with sr.Microphone() as source:
                    recognizer.adjust_for_ambient_noise(source) # Adjust for noise
                    print("Listening for message...")
                    audio_msg = recognizer.listen(source, timeout=10, phrase_time_limit=10) # Adjusted timeout for message
                message = recognizer.recognize_google(audio_msg)
                print(f"Recognized Message: {message}")
                sendmsg(phone_no, message)
                # pyautogui.press('enter') # sendmsg already handles this

            else:
                speak(f"Sorry, {name} is not in the contact list.")
        except sr.WaitTimeoutError:
            speak("I didn't hear anything. Please try again.")
        except sr.UnknownValueError:
            speak("Sorry, I could not understand the audio. Please try again.")
        except Exception as e:
            print(f"Error processing message: {e}")
            speak("Sorry, I was not able to send the message.")

if __name__ == "__main__":
    speak("Initializing Jarvis...")
    # Prompt for API key if not set
    if OPENWEATHERMAP_API_KEY == "YOUR_API_KEY_HERE":
        print("IMPORTANT: OpenWeatherMap API key is not set. Weather functionality will not work.")
        speak("Warning: OpenWeatherMap API key is not set. Weather functionality will be disabled. Please update the script with your API key.")

    while True:
        r = sr.Recognizer()
        # print("Recognizing...") # Less verbose
        try:
            with sr.Microphone() as source:
                r.adjust_for_ambient_noise(source, duration=0.5) # Adjust for ambient noise
                print("Listening for activation word (e.g., 'hello')...")
                audio = r.listen(source, timeout=5, phrase_time_limit=3) # Shorter timeout for activation
            word = r.recognize_google(audio)
            if word.lower() == "hello": # Consider making activation word configurable
                speak("Yes sir.")
                with sr.Microphone() as source:
                    r.adjust_for_ambient_noise(source, duration=0.5)
                    print("Jarvis activated. Listening for command...")
                    audio_command = r.listen(source, timeout=7, phrase_time_limit=7) # Longer timeout for command
                command = r.recognize_google(audio_command)
                print(f"Recognized command: {command}")
                processCommand(command)
            # else: # Optional: respond if activation word is not recognized
                # print(f"Heard: {word}, but not the activation word.")

        except sr.WaitTimeoutError:
            # print("No speech detected within timeout.") # Less verbose, expected during normal operation
            pass
        except sr.UnknownValueError:
            # speak("Sorry, I could not understand the audio.") # Can be too chatty if always responding
            print("Could not understand audio.")
            pass
        except Exception as e:
            print(f"An error occurred in the main loop: {e}")
            # speak("An unexpected error occurred. Please try again.") # Optional: inform user of error
            pass # Continue loop

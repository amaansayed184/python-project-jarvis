# python-project-jarvis
This is a voice-controlled personal assistant named Jarvis, built using Python. It performs various tasks like opening websites, checking battery status, sending WhatsApp messages, taking screenshots, flipping a coin, rolling a die, and telling the time.
📌 Features
1.Voice Recognition:
  Uses speech_recognition to understand voice commands.
  
2.Text-to-Speech: 
  Uses pyttsx3 to speak responses.

3.Automated Web Actions:
  Opens Google, YouTube, LinkedIn, Instagram, and other websites.

4.WhatsApp Messaging:
  Sends messages via WhatsApp Web using webbrowser and pyautogui.

5.Battery Status Check:
  Uses psutil to check battery percentage and charging status.

6.Screenshot Capture:
  Takes screenshots using pyautogui and saves them.

7.Coin Flip & Dice Roll:
  Simulates flipping a coin and rolling a die.

8.Real-time Clock:
  Tells the current time when asked.

9.Weather Forecast:
  Fetches and announces the current weather for a specified city using the OpenWeatherMap API.
  To use this feature, you need to:
    - Sign up for a free API key at [OpenWeatherMap](https://openweathermap.org/appid).
    - Replace `"YOUR_API_KEY_HERE"` in `main.py` with your actual API key.
  Command: "Jarvis, what's the weather in [city name]?" (after activation word)

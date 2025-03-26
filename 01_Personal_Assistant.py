import speech_recognition as sr
import pyttsx3
import datetime
import requests
import json

def speak(text):
    engine = pyttsx3.init()
    engine.say(text)
    engine.runAndWait()

def listen():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)
    
    try:
        command = recognizer.recognize_google(audio)
        print("You said:", command)
        return command.lower()
    except sr.UnknownValueError:
        speak("Sorry, I couldn't understand that.")
        return ""
    except sr.RequestError:
        speak("There was an issue with the speech recognition service.")
        return ""

def get_weather():
    api_key = "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"  # Replace with your actual API key
    city = "Hyderbad"  # Replace with your city
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
    
    try:
        response = requests.get(url)
        weather_data = json.loads(response.text)
        temp = weather_data["main"]["temp"]
        description = weather_data["weather"][0]["description"]
        return f"The current temperature in {city} is {temp} degrees Celsius with {description}."
    except:
        return "Sorry, I couldn't fetch the weather information."

def set_reminder(task):
    with open("reminders.txt", "a") as file:
        file.write(task + "\n")
    return "Reminder set for: " + task

def read_news():
    news = ["News headline 1", "News headline 2", "News headline 3"]  # Replace with actual API call if needed
    return "Here are today's top news headlines: " + ", ".join(news)

def main():
    speak("Hello! How can I Help You?")
    
    while True:
        command = listen()
        
        if "weather" in command:
            response = get_weather()
        elif "reminder" in command:
            speak("What should I remind you about?")
            task = listen()
            response = set_reminder(task)
        elif "news" in command:
            response = read_news()
        elif "exit" in command or "stop" in command:
            speak("Goodbye!")
            break
        else:
            response = "Sorry, I didn't understand that."
        
        speak(response)

if __name__ == "__main__":
    main()

import pygame
import pyttsx3
import datetime
import speech_recognition as sr
import wikipedia
import webbrowser
import os
import cv2
import openai
import pywhatkit

openai.api_key = "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"

engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')

current_gender = 'male'  # Default to male voice

def speak(audio):
    global current_gender
    if current_gender == 'male':
        engine.setProperty('voice', voices[0].id)  # Male voice
        current_gender = 'female'  # Switch to female for next output
    else:
        engine.setProperty('voice', voices[1].id)  # Female voice
        current_gender = 'male'  # Switch to male for next output

    engine.say(audio)
    engine.runAndWait()

def wishMe():
    hour = datetime.datetime.now().hour
    if 0 <= hour < 12:
        speak("Good morning")
    elif 12 <= hour < 16:
        speak("Good afternoon")
    elif 16 <= hour < 21:
        speak("Good evening")
    else:
        speak("Good night")
    speak("Hello, I am JARVIS AI. How can I help you?")

def takeCommand():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        r.pause_threshold = 0.6
        audio = r.listen(source)

    try:
        print("Recognizing...")
        query = r.recognize_google(audio, language='en-in')
        speak("user said"+query)
        print(f"User said: {query}\n")
    except Exception as e:
        print(e)
        print("Please repeat...")
        return "None"
    return query

def generate_response(prompt):
    response = openai.Completion.create(
        engine="davinci-002",
        prompt=prompt,
        max_tokens=3000,
        n=1,
        stop=None,
        temperature=0.7,
        api_key="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"
    )
    return response["choices"][0]["text"]

def open_camera():
    cap = cv2.VideoCapture(0)
    while True:
        ret, frame = cap.read()
        cv2.imshow('Camera', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    wishMe()
    while True:
        query = takeCommand().lower()
        if 'wikipedia' in query:
            speak("Searching Wikipedia....")
            query = query.replace("wikipedia", "")
            results = wikipedia.summary(query, sentences=2)
            speak("According to Wikipedia")
            print(results)
            speak(results)
        elif 'open youtube' in query:
            speak("opening youtube.....")
            webbrowser.open("https://www.youtube.com/")
        elif 'open google' in query:
            speak("opening google.....")
            webbrowser.open("https://www.google.com/")
        elif 'open wikipedia' in query:
            speak("opening wikipedia.....")
            webbrowser.open("https://www.wikipedia.org/")
        elif 'time' in query:
            strTime = datetime.datetime.now().strftime("%H:%M:%S")
            print(strTime)
            speak(f"the time is {strTime}")
        elif 'open code' in query:
            codePath = "C:\\Program Files\\MATLAB\\R2023a\\bin\\matlab.exe"
            os.startfile(codePath)
        elif 'play music' in query:
            speak("Playing music...")
            pygame.mixer.init()
            pygame.mixer.music.load("C:\\Users\\subha\\Music\\Pehle Bhi Main Ringtone Download - MobCup.Com.Co.mp3")
            pygame.mixer.music.play()
        elif 'stop music' in query:
            pygame.mixer.music.stop()
            speak("Music stopped.")
        elif 'open camera' in query:
            speak("opening camera.....")
            open_camera()
        elif 'my music' in query:
            speak("playing your favourite jukebox.....")
            webbrowser.open("https://www.youtube.com/watch?v=Tx_SyNQXhgY")
        elif 'generate response' in query:
            speak("Sure, please wait...")
            prompt = "What do you want to generate a response for?"
            speak(prompt)
            user_input = takeCommand().lower()
            response = generate_response(user_input)
            speak(response)
        elif 'play' in query:
            speak('Playing on YouTube...')
            pywhatkit.playonyt(query)
        elif 'search' in query:
            speak("Searching on Google...")
            search_query = query.replace("search", "").strip()
            search_url = f"https://www.google.com/search?q={search_query}"
            webbrowser.open(search_url)
        elif 'exit' in query:
            speak("Goodbye!")
            break

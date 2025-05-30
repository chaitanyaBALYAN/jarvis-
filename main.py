import speech_recognition as sr
import webbrowser as wb
import pyttsx3
import musiclibrary
import requests
import google.generativeai as genai

recognizer = sr.Recognizer()
engine = pyttsx3.init()
newsapi="1e937e4ca9264ae6bdfb2b42ab693e79"
genai.configure(api_key="AIzaSyDE47GKq0mayUQTXZBTqt6kGN4aRlVHmgw")

# ✨ Load the Gemini model
model = genai.GenerativeModel(model_name="models/gemini-1.5-flash")

def speak(text):
    print("Jarvis:", text)
    engine.say(text)
    engine.runAndWait()

def processcommand(c):
    c = c.lower()
    if "open youtube" in c:
        speak("Opening YouTube")
        wb.open("https://www.youtube.com")
    elif "open google" in c:
        speak("Opening Google")
        wb.open("https://www.google.com")
    elif "open stack overflow" in c:
        speak("Opening Stack Overflow")
        wb.open("https://stackoverflow.com")
    elif "open github" in c:
        speak("Opening GitHub")
        wb.open("https://github.com")
    elif "play " in c:
        song = c.replace("play ", "").strip()
        link = musiclibrary.music.get(song.lower())
        if link:
            speak(f"Playing {song}")
            wb.open(link)
        else:
            speak(f"Sorry, I couldn't find the song '{song}' in your library.")
    elif "news" in c:
        r=requests.get("https://newsapi.org/v2/top-headlines?country=us&category=business&apiKey=1e937e4ca9264ae6bdfb2b42ab693e79")
        if r.status_code==200:
            data = r.json()
            articles = data.get('articles', [])
            for article in articles:
                speak(article['title'])

    else:
        try:
            model = genai.GenerativeModel("gemini-1.5-flash")
            response = model.generate_content(c)
            speak(response.text)
        except Exception as e:
            speak("Sorry, I couldn't get a response from Gemini.")
            print(f"Error: {e}")



if __name__ == "__main__":
    speak("Initializing Jarvis...")
    while True:
        try:
            with sr.Microphone() as source:
                print("Listening for wake word 'Jarvis'...")
                audio = recognizer.listen(source, timeout=6, phrase_time_limit=5)
                word = recognizer.recognize_google(audio)
                print("Heard:", word)

            if "jarvis" in word.lower():
                speak("Yes sir, how can I help you?")
                with sr.Microphone() as source:
                    print("Listening for your command...")
                    audio = recognizer.listen(source, timeout=6, phrase_time_limit=5)
                    command = recognizer.recognize_google(audio)
                    print("Command:", command)
                    processcommand(command)

        except sr.WaitTimeoutError:
            print("Timeout: No speech detected.")
        except sr.UnknownValueError:
            print("Speech Recognition could not understand the audio.")
        except sr.RequestError as e:
            print(f"Could not request results from Google Speech Recognition service; {e}")
        except Exception as e:
            print("Other error:", e)
